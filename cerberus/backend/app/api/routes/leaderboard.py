from fastapi import APIRouter, Depends

from app.api.dependencies import (
    get_challenge_service,
    get_leaderboard_service,
    require_capability,
    require_csrf,
)
from app.services.challenge_service import ChallengeService
from app.services.leaderboard_service import LeaderboardService

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.post("/submit")
def submit(
    event_id: int,
    challenge_id: int,
    flag: str,
    sub_challenge_id: int | None = None,
    current_user: dict = Depends(require_capability("submit_flags")),
    svc: LeaderboardService = Depends(get_leaderboard_service),
    challenge_service: ChallengeService = Depends(get_challenge_service),
):
    payload = {
        "event_id": event_id,
        "challenge_id": challenge_id,
        "sub_challenge_id": sub_challenge_id,
        "flag": flag,
        "challenge_service": challenge_service,
    }
    return svc.submit(current_user["id"], payload)


@router.get("/{event_id}")
def get_board(
    event_id: int,
    _user: dict = Depends(require_csrf),
    svc: LeaderboardService = Depends(get_leaderboard_service),
):
    return svc.calculate(event_id)
