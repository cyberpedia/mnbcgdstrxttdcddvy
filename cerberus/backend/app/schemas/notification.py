from pydantic import BaseModel, EmailStr, Field


class NotificationCreate(BaseModel):
    user_id: int
    type: str = Field(default="system", max_length=64)
    content: str


class EmailNotification(BaseModel):
    to: EmailStr
    subject: str = Field(max_length=128)
    body: str
