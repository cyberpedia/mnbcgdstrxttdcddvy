from datetime import datetime

from pydantic import BaseModel, Field


class EventCreate(BaseModel):
    name: str = Field(min_length=3, max_length=128)
    start_time: datetime
    end_time: datetime
    theme: str | None = None
    status: str = "draft"


class EventStatusUpdate(BaseModel):
    status: str
