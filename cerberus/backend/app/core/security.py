from __future__ import annotations

from datetime import UTC, datetime, timedelta
from html import escape
from typing import Any
from uuid import uuid4

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def _make_token(subject: str, token_type: str, expires_minutes: int, extra: dict[str, Any] | None = None) -> str:
    now = datetime.now(UTC)
    payload: dict[str, Any] = {
        "sub": subject,
        "type": token_type,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=expires_minutes)).timestamp()),
        "jti": str(uuid4()),
    }
    if extra:
        payload.update(extra)
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def create_access_token(subject: str, role: str, csrf_token: str) -> str:
    return _make_token(
        subject=subject,
        token_type="access",
        expires_minutes=settings.access_token_exp_minutes,
        extra={"role": role, "csrf": csrf_token},
    )


def create_refresh_token(subject: str) -> str:
    return _make_token(subject=subject, token_type="refresh", expires_minutes=settings.refresh_token_exp_minutes)


def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise ValueError("Invalid token") from exc


def sanitize_text(value: str) -> str:
    return escape(value, quote=True)
