from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient

from app.main import app
from app.repositories.memory_store import store

client = TestClient(app)


def _register_and_login(username: str, role: str):
    register = client.post(
        "/auth/register",
        json={
            "username": username,
            "email": f"{username}@example.com",
            "password": "VeryStrongPassword123!",
            "role": role,
        },
    )
    assert register.status_code == 200
    login = client.post("/auth/login", json={"username": username, "password": "VeryStrongPassword123!"})
    assert login.status_code == 200
    data = login.json()
    headers = {"Authorization": f"Bearer {data['access_token']}", "X-CSRF-Token": data["csrf_token"]}
    return headers


def setup_function():
    store.users.clear()
    store.challenges.clear()
    store.sub_challenges.clear()
    store.hints.clear()
    store.submissions.clear()
    store.events.clear()
    store.notifications.clear()
    store.audit_logs.clear()
    store.ui_config.clear()
    for k in store._ids:
        store._ids[k] = 0


def test_auth_refresh_flow():
    client.post(
        "/auth/register",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "VeryStrongPassword123!",
            "role": "admin",
        },
    )
    login = client.post("/auth/login", json={"username": "alice", "password": "VeryStrongPassword123!"})
    assert login.status_code == 200
    refresh = client.post("/auth/refresh", json={"refresh_token": login.json()["refresh_token"]})
    assert refresh.status_code == 200
    assert refresh.json()["access_token"]


def test_rbac_and_csrf_enforced():
    user_headers = _register_and_login("user1", "user")
    event_resp = client.post(
        "/events",
        headers=user_headers,
        json={
            "name": "Event",
            "start_time": datetime.now(UTC).isoformat(),
            "end_time": (datetime.now(UTC) + timedelta(hours=2)).isoformat(),
            "status": "draft",
        },
    )
    assert event_resp.status_code == 403

    admin_headers = _register_and_login("admin1", "admin")
    no_csrf = {"Authorization": admin_headers["Authorization"]}
    denied = client.post(
        "/events",
        headers=no_csrf,
        json={
            "name": "Event2",
            "start_time": datetime.now(UTC).isoformat(),
            "end_time": (datetime.now(UTC) + timedelta(hours=2)).isoformat(),
            "status": "draft",
        },
    )
    assert denied.status_code == 403


def test_challenge_submission_and_leaderboard():
    admin_headers = _register_and_login("admin2", "admin")
    user_headers = _register_and_login("user2", "user")

    event_resp = client.post(
        "/events",
        headers=admin_headers,
        json={
            "name": "CTF 2026",
            "start_time": datetime.now(UTC).isoformat(),
            "end_time": (datetime.now(UTC) + timedelta(hours=4)).isoformat(),
            "status": "live",
        },
    )
    assert event_resp.status_code == 200
    event_id = event_resp.json()["id"]

    challenge = client.post(
        "/challenges",
        headers=admin_headers,
        json={
            "event_id": event_id,
            "title": "Warmup",
            "category": "web",
            "difficulty": "easy",
            "type": "standard",
            "hierarchical_rule": {},
            "visibility": "public",
        },
    )
    assert challenge.status_code == 200
    challenge_id = challenge.json()["id"]

    sub = client.post(
        f"/challenges/{challenge_id}/sub-challenges",
        headers=admin_headers,
        json={"title": "Part A", "order": 1, "flag": "flag{ok}"},
    )
    assert sub.status_code == 200

    submit = client.post(
        "/leaderboard/submit",
        headers=user_headers,
        params={"event_id": event_id, "challenge_id": challenge_id, "flag": "flag{ok}"},
    )
    assert submit.status_code == 200
    assert submit.json()["result"] == "correct"

    board = client.get(f"/leaderboard/{event_id}", headers=user_headers)
    assert board.status_code == 200
    assert board.json()[0]["score"] == 100


def test_ui_config_and_audit():
    admin_headers = _register_and_login("infra", "super_admin")

    set_cfg = client.put(
        "/ui-config",
        headers=admin_headers,
        json={
            "theme": "dark",
            "logo_url": "https://cdn.example.com/logo.png",
            "primary_color": "#000000",
            "secondary_color": "#ffffff",
            "assets": {"banner": "https://cdn.example.com/banner.png"},
        },
    )
    assert set_cfg.status_code == 200

    audit = client.get("/audit", headers=admin_headers)
    assert audit.status_code == 200
    assert any(entry["action"] == "ui_config.update" for entry in audit.json())
