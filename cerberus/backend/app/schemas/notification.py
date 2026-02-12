from pydantic import BaseModel, EmailStr, Field


class NotificationCreate(BaseModel):
    user_id: int
    type: str = Field(default="system", max_length=64)
    content: str


class EmailNotification(BaseModel):
    to: EmailStr
    subject: str = Field(max_length=128)
    body: str


class AdminAlert(BaseModel):
    summary: str = Field(max_length=180)
    severity: str = Field(default="warning", pattern="^(info|warning|critical)$")
    source: str = Field(default="monitoring", max_length=64)


class SupportTicketCreate(BaseModel):
    subject: str = Field(max_length=120)
    message: str = Field(max_length=5000)
