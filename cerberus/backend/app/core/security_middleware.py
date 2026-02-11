from __future__ import annotations

import time
from collections import defaultdict, deque
from collections.abc import Awaitable, Callable

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.repositories.memory_store import store


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable]):
        proto = request.headers.get("x-forwarded-proto", request.url.scheme)
        if settings.enforce_https and settings.app_env != "development" and proto != "https":
            return JSONResponse(status_code=426, content={"detail": "HTTPS is required"})

        response = await call_next(request)
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none'"
        return response


class EvidenceLockMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable]):
        if settings.evidence_lock_mode and request.method in {"POST", "PUT", "PATCH", "DELETE"}:
            if not request.url.path.startswith("/auth"):
                return JSONResponse(status_code=423, content={"detail": "Evidence lock mode enabled"})
        return await call_next(request)


class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable]):
        started = time.time()
        response = await call_next(request)
        store.audit(
            actor_id=None,
            action="http.request",
            target=request.url.path,
            after={
                "method": request.method,
                "status_code": response.status_code,
                "latency_ms": round((time.time() - started) * 1000, 2),
            },
        )
        return response


class AdaptiveRateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.window_seconds = 60
        self.ip_hits: dict[str, deque[float]] = defaultdict(deque)
        self.user_hits: dict[str, deque[float]] = defaultdict(deque)
        self.team_hits: dict[str, deque[float]] = defaultdict(deque)

    def _allow(self, bucket: deque[float], limit: int) -> bool:
        now = time.time()
        while bucket and (now - bucket[0]) > self.window_seconds:
            bucket.popleft()
        if len(bucket) >= limit:
            return False
        bucket.append(now)
        return True

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable]):
        ip = request.client.host if request.client else "unknown"
        user_key = request.headers.get("x-user-id", "anon")
        team_key = request.headers.get("x-team-id", "solo")

        if not self._allow(self.ip_hits[f"{ip}:{request.url.path}"], settings.rate_limit_per_minute_ip):
            return JSONResponse(status_code=429, content={"detail": "IP rate limit exceeded"})
        if user_key != "anon" and not self._allow(self.user_hits[user_key], settings.rate_limit_per_minute_user):
            return JSONResponse(status_code=429, content={"detail": "User rate limit exceeded"})
        if team_key != "solo" and not self._allow(self.team_hits[team_key], settings.rate_limit_per_minute_team):
            return JSONResponse(status_code=429, content={"detail": "Team rate limit exceeded"})

        return await call_next(request)
