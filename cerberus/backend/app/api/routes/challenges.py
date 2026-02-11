from fastapi import APIRouter, Depends

from app.api.dependencies import get_challenge_service, require_capability
from app.schemas.challenge import (
    ChallengeCreate,
    ChallengeUpdate,
    HintCreate,
    SubChallengeCreate,
)
from app.services.challenge_service import ChallengeService

router = APIRouter(prefix="/challenges", tags=["challenges"])


@router.post("")
def create_challenge(
    payload: ChallengeCreate,
    current_user: dict = Depends(require_capability("manage_challenges")),
    svc: ChallengeService = Depends(get_challenge_service),
):
    return svc.create_challenge(current_user["id"], payload.model_dump())


@router.patch("/{challenge_id}")
def update_challenge(
    challenge_id: int,
    payload: ChallengeUpdate,
    current_user: dict = Depends(require_capability("manage_challenges")),
    svc: ChallengeService = Depends(get_challenge_service),
):
    return svc.update_challenge(current_user["id"], challenge_id, payload.model_dump(exclude_none=True))


@router.post("/{challenge_id}/sub-challenges")
def create_sub_challenge(
    challenge_id: int,
    payload: SubChallengeCreate,
    current_user: dict = Depends(require_capability("manage_challenges")),
    svc: ChallengeService = Depends(get_challenge_service),
):
    return svc.create_sub_challenge(current_user["id"], challenge_id, payload.model_dump())


@router.post("/{challenge_id}/hints")
def add_hint(
    challenge_id: int,
    payload: HintCreate,
    current_user: dict = Depends(require_capability("manage_hints")),
    svc: ChallengeService = Depends(get_challenge_service),
):
    return svc.add_hint(current_user["id"], challenge_id, payload.model_dump())


@router.post("/hints/{hint_id}/toggle")
def toggle_hint(
    hint_id: int,
    enabled: bool,
    current_user: dict = Depends(require_capability("manage_hints")),
    svc: ChallengeService = Depends(get_challenge_service),
):
    return svc.set_hint_enabled(current_user["id"], hint_id, enabled)
