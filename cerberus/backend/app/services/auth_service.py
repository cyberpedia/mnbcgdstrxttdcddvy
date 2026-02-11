from __future__ import annotations

from secrets import token_urlsafe

from fastapi import HTTPException, status

from app.core.rbac import ROLE_HIERARCHY
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.repositories.memory_store import MemoryStore


class AuthService:
    def __init__(self, db: MemoryStore):
        self.db = db

    def register(self, username: str, email: str, password: str, role: str) -> dict:
        if role not in ROLE_HIERARCHY:
            raise HTTPException(status_code=400, detail="Unknown role")

        if any(u["username"] == username for u in self.db.users.values()):
            raise HTTPException(status_code=409, detail="Username already exists")

        user_id = self.db.next_id("users")
        user = {
            "id": user_id,
            "username": username,
            "email": email,
            "hashed_password": hash_password(password),
            "role": role,
            "tenant_id": "default",
        }
        self.db.users[user_id] = user
        self.db.audit(user_id, "auth.register", f"user:{user_id}", after={"username": username, "role": role})
        return user

    def login(self, username: str, password: str) -> dict:
        user = next((u for u in self.db.users.values() if u["username"] == username), None)
        if not user or not verify_password(password, user["hashed_password"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        csrf = token_urlsafe(24)
        access = create_access_token(subject=str(user["id"]), role=user["role"], csrf_token=csrf)
        refresh = create_refresh_token(subject=str(user["id"]))
        self.db.audit(user["id"], "auth.login", f"user:{user['id']}")
        return {"access_token": access, "refresh_token": refresh, "csrf_token": csrf}

    def refresh(self, refresh_token: str) -> dict:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        user_id = int(payload["sub"])
        user = self.db.users.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        csrf = token_urlsafe(24)
        access = create_access_token(subject=str(user_id), role=user["role"], csrf_token=csrf)
        return {"access_token": access, "refresh_token": refresh_token, "csrf_token": csrf}
