from fastapi import APIRouter, Depends

from app.api.dependencies import get_event_service, require_capability
from app.schemas.event import EventCreate, EventStatusUpdate
from app.services.event_service import EventService

router = APIRouter(prefix="/events", tags=["events"])


@router.post("")
def create_event(
    payload: EventCreate,
    current_user: dict = Depends(require_capability("manage_events")),
    svc: EventService = Depends(get_event_service),
):
    return svc.create_event(current_user["id"], payload.model_dump())


@router.post("/{event_id}/status")
def set_status(
    event_id: int,
    payload: EventStatusUpdate,
    current_user: dict = Depends(require_capability("manage_events")),
    svc: EventService = Depends(get_event_service),
):
    return svc.set_status(current_user["id"], event_id, payload.status)
