from fastapi import APIRouter, Depends

from app.api.dependencies import get_auth_service
from app.schemas.auth import (
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(payload: RegisterRequest, svc: AuthService = Depends(get_auth_service)):
    return svc.register(payload.username, payload.email, payload.password, payload.role)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, svc: AuthService = Depends(get_auth_service)):
    return svc.login(payload.username, payload.password)


@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: RefreshRequest, svc: AuthService = Depends(get_auth_service)):
    return svc.refresh(payload.refresh_token)
