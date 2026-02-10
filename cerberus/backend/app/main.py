from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import (
    audit,
    auth,
    challenges,
    events,
    leaderboard,
    notifications,
    ui_config,
)
from app.core.config import settings
from app.core.rate_limit import InMemoryRateLimiter

app = FastAPI(title=settings.app_name, debug=settings.app_debug)

app.add_middleware(InMemoryRateLimiter)
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


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
