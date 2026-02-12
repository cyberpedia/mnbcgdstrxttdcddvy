from __future__ import annotations

from collections import defaultdict
from datetime import UTC, datetime

from fastapi import WebSocket

from app.core.security import sanitize_text
from app.repositories.memory_store import MemoryStore


class NotificationService:
    def __init__(self, db: MemoryStore):
        self.db = db
        self.connections: dict[int, list[WebSocket]] = defaultdict(list)

    async def connect(self, user_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        self.connections[user_id].append(websocket)

    def disconnect(self, user_id: int, websocket: WebSocket) -> None:
        if websocket in self.connections[user_id]:
            self.connections[user_id].remove(websocket)

    async def push_ws(self, actor_id: int, user_id: int, payload: dict) -> dict:
        item = {
            "id": self.db.next_id("notifications"),
            "user_id": user_id,
            "type": payload["type"],
            "content": sanitize_text(payload["content"]),
        }
        self.db.notifications.append(item)
        for ws in self.connections[user_id]:
            await ws.send_json(item)
        self.db.audit(actor_id, "notification.ws", f"notification:{item['id']}", after=item)
        return item

    def send_email(self, actor_id: int, to: str, subject: str, body: str) -> dict:
        # Stubbed for integration with actual email provider.
        result = {"to": to, "subject": sanitize_text(subject), "body": sanitize_text(body), "status": "queued"}
        self.db.audit(actor_id, "notification.email", f"email:{to}", after=result)
        return result

    def send_admin_alert(self, payload: dict) -> dict:
        alert = {
            "id": self.db.next_id("notifications"),
            "type": "admin_alert",
            "severity": payload["severity"],
            "source": sanitize_text(payload["source"]),
            "summary": sanitize_text(payload["summary"]),
            "created_at": datetime.now(UTC).isoformat(),
        }
        self.db.notifications.append(alert)
        self.db.audit(None, "notification.admin_alert", f"alert:{alert['id']}", after=alert)
        return {"status": "accepted", "alert": alert}

    def create_support_ticket(self, user_id: int, subject: str, message: str) -> dict:
        ticket = {
            "id": self.db.next_id("support_tickets"),
            "user_id": user_id,
            "subject": sanitize_text(subject),
            "message": sanitize_text(message),
            "status": "open",
            "created_at": datetime.now(UTC).isoformat(),
        }
        self.db.support_tickets.append(ticket)
        self.db.audit(user_id, "support.ticket.create", f"ticket:{ticket['id']}", after=ticket)
        return ticket
