from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app
from app.repositories.memory_store import store

client = TestClient(app)
PASSWORD = "VeryStrongPassword123!"


def setup_function():
    store.users.clear()
    store.challenges.clear()
    store.sub_challenges.clear()
    store.hints.clear()
    store.submissions.clear()
    store.events.clear()
    store.notifications.clear()
    store.audit_logs.clear()
    for key in store._ids:
        store._ids[key] = 0
    settings.app_env = "development"
    settings.evidence_lock_mode = False


def _auth(role: str, username: str):
    client.post(
        "/auth/register",
        json={
            "username": username,
            "email": f"{username}@example.com",
            "password": PASSWORD,
            "role": role,
        },
    )
    login = client.post("/auth/login", json={"username": username, "password": PASSWORD}).json()
    return {
        "Authorization": f"Bearer {login['access_token']}",
        "X-CSRF-Token": login["csrf_token"],
        "X-User-Id": "1",
    }


def test_user_cannot_create_event_but_admin_can():
    user_headers = _auth("user", "plain_user")
    admin_headers = _auth("admin", "admin_user")

    payload = {
        "name": "RBAC Event",
        "start_time": datetime.now(UTC).isoformat(),
        "end_time": (datetime.now(UTC) + timedelta(hours=1)).isoformat(),
        "status": "draft",
    }

    denied = client.post("/events", headers=user_headers, json=payload)
    assert denied.status_code == 403

    allowed = client.post("/events", headers=admin_headers, json=payload)
    assert allowed.status_code == 200
