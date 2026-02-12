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


def _login_headers(username="sec_admin", role="admin"):
    client.post(
        "/auth/register",
        json={"username": username, "email": f"{username}@x.io", "password": PASSWORD, "role": role},
    )
    login = client.post("/auth/login", json={"username": username, "password": PASSWORD}).json()
    return {"Authorization": f"Bearer {login['access_token']}", "X-CSRF-Token": login["csrf_token"]}


def test_csrf_missing_rejected():
    headers = _login_headers()
    del headers["X-CSRF-Token"]
    resp = client.post(
        "/events",
        headers=headers,
        json={
            "name": "NoCSRF",
            "start_time": datetime.now(UTC).isoformat(),
            "end_time": (datetime.now(UTC) + timedelta(hours=1)).isoformat(),
            "status": "draft",
        },
    )
    assert resp.status_code == 403


def test_auth_bypass_without_token_denied():
    resp = client.get("/audit")
    assert resp.status_code in {401, 403}


def test_sqli_style_username_not_bypass_auth():
    client.post(
        "/auth/register",
        json={"username": "alice", "email": "alice@x.io", "password": PASSWORD, "role": "user"},
    )
    resp = client.post("/auth/login", json={"username": "' OR 1=1 --", "password": "anything"})
    assert resp.status_code == 401


def test_xss_payload_is_sanitized_in_hint():
    headers = _login_headers("xss_admin")
    event = client.post(
        "/events",
        headers=headers,
        json={
            "name": "XSSTest",
            "start_time": datetime.now(UTC).isoformat(),
            "end_time": (datetime.now(UTC) + timedelta(hours=2)).isoformat(),
            "status": "live",
        },
    ).json()
    challenge = client.post(
        "/challenges",
        headers=headers,
        json={
            "event_id": event["id"],
            "title": "XSS",
            "category": "web",
            "difficulty": "easy",
            "type": "standard",
            "hierarchical_rule": {},
            "visibility": "public",
        },
    ).json()
    hint = client.post(
        f"/challenges/{challenge['id']}/hints",
        headers=headers,
        json={"content": "<script>alert(1)</script>", "penalty": 10, "enabled": True},
    )
    assert hint.status_code == 200
    assert "<script>" not in hint.json()["content"]
