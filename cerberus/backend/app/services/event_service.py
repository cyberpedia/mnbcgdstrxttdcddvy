from __future__ import annotations

from datetime import UTC, datetime

from fastapi import HTTPException

from app.core.signing import SigningService
from app.repositories.memory_store import MemoryStore


class EventService:
    ALLOWED = {"draft", "scheduled", "live", "freeze", "archived"}

    def __init__(self, db: MemoryStore):
        self.db = db

    def create_event(self, actor_id: int, payload: dict) -> dict:
        if payload["end_time"] <= payload["start_time"]:
            raise HTTPException(status_code=400, detail="end_time must be later than start_time")
        if payload["status"] not in self.ALLOWED:
            raise HTTPException(status_code=400, detail="Invalid event status")
        event_id = self.db.next_id("events")
        event = {"id": event_id, **payload}
        event["signature"] = SigningService.sign(event)
        self.db.events[event_id] = event
        self.db.audit(actor_id, "event.create", f"event:{event_id}", after=event)
        return event

    def set_status(self, actor_id: int, event_id: int, status: str) -> dict:
        event = self.db.events.get(event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        if status not in self.ALLOWED:
            raise HTTPException(status_code=400, detail="Invalid event status")
        before = event.copy()
        event["status"] = status
        event["updated_at"] = datetime.now(UTC).isoformat()
        event["signature"] = SigningService.sign({k: v for k, v in event.items() if k != "signature"})
        self.db.audit(actor_id, "event.status", f"event:{event_id}", before=before, after=event)
        return event
