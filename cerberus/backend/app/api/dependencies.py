from __future__ import annotations

from fastapi import Depends, Header, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings
from app.core.rbac import has_capability
from app.core.security import decode_token
from app.repositories.memory_store import store
from app.services.auth_service import AuthService
from app.services.challenge_service import ChallengeService
from app.services.event_service import EventService
from app.services.leaderboard_service import LeaderboardService
from app.services.notification_service import NotificationService
from app.services.ui_config_service import UIConfigService

bearer = HTTPBearer(auto_error=True)
notification_service = NotificationService(store)


def get_auth_service() -> AuthService:
    return AuthService(store)


def get_challenge_service() -> ChallengeService:
    return ChallengeService(store)


def get_event_service() -> EventService:
    return EventService(store)


def get_leaderboard_service() -> LeaderboardService:
    return LeaderboardService(store)


def get_notification_service() -> NotificationService:
    return notification_service


def get_ui_config_service() -> UIConfigService:
    return UIConfigService(store)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
) -> dict:
    payload = decode_token(credentials.credentials)
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Not an access token")
    user_id = int(payload["sub"])
    user = store.users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = user.copy()
    user["csrf"] = payload.get("csrf")
    return user


def require_csrf(
    request: Request,
    current_user: dict = Depends(get_current_user),
    x_csrf_token: str | None = Header(default=None),
) -> dict:
    if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
        if not x_csrf_token or x_csrf_token != current_user.get("csrf"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="CSRF token missing or invalid")
    return current_user


def require_capability(capability: str):
    def dep(user: dict = Depends(require_csrf)) -> dict:
        if not has_capability(user["role"], capability):
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user

    return dep


def require_admin_confirmation(
    x_admin_confirmation: str | None = Header(default=None),
) -> None:
    if x_admin_confirmation != settings.admin_confirmation_phrase:
        raise HTTPException(status_code=412, detail="Admin action confirmation required")
