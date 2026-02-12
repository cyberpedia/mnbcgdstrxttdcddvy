from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import (
    audit,
    auth,
    challenges,
    events,
    files,
    leaderboard,
    notifications,
    ui_config,
)
from app.core.config import settings
from app.core.security_middleware import (
    AdaptiveRateLimiterMiddleware,
    AuditMiddleware,
    EvidenceLockMiddleware,
    SecurityHeadersMiddleware,
)

app = FastAPI(title=settings.app_name, debug=settings.app_debug)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(AdaptiveRateLimiterMiddleware)
app.add_middleware(EvidenceLockMiddleware)
app.add_middleware(AuditMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(events.router)
app.include_router(challenges.router)
app.include_router(leaderboard.router)
app.include_router(notifications.router)
app.include_router(ui_config.router)
app.include_router(audit.router)
app.include_router(files.router)


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "tls_min_version": settings.tls_min_version,
    }
