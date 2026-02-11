from datetime import datetime

from pydantic import BaseModel


class MessageResponse(BaseModel):
    message: str


class AuditEntry(BaseModel):
    actor_id: int | None
    action: str
    target: str
    before: dict | None = None
    after: dict | None = None
    timestamp: datetime
