from datetime import UTC, datetime, timedelta
from pathlib import Path

from fastapi.testclient import TestClient

from app.core.config import settings
from app.core.signing import SigningService

from fastapi.testclient import TestClient

from app.main import app
from app.repositories.memory_store import store

client = TestClient(app)


STRONG_PASSWORD = "VeryStrongPassword123!"


def _register_and_login(username: str, role: str):
    register = client.post(
        "/auth/register",
        json={
            "username": username,
            "email": f"{username}@example.com",
            "password": STRONG_PASSWORD,
            "password": "VeryStrongPassword123!",
            "role": role,
        },
    )
    assert register.status_code == 200
    login = client.post(
        "/auth/login",
        json={"username": username, "password": STRONG_PASSWORD},
    )
    assert login.status_code == 200
    data = login.json()
    headers = {
        "Authorization": f"Bearer {data['access_token']}",
        "X-CSRF-Token": data["csrf_token"],
        "X-User-Id": str(register.json()["id"]),
    }
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
    for key in store._ids:
        store._ids[key] = 0
    settings.evidence_lock_mode = False
    settings.app_env = "development"
    for k in store._ids:
        store._ids[k] = 0


def test_auth_refresh_flow():
    client.post(
        "/auth/register",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": STRONG_PASSWORD,
            "role": "admin",
        },
    )
    login = client.post(
        "/auth/login",
        json={"username": "alice", "password": STRONG_PASSWORD},
    )
    assert login.status_code == 200
    refresh = client.post(
        "/auth/refresh",
        json={"refresh_token": login.json()["refresh_token"]},
    )
            "password": "VeryStrongPassword123!",
            "role": "admin",
        },
    )
    login = client.post("/auth/login", json={"username": "alice", "password": "VeryStrongPassword123!"})
    assert login.status_code == 200
    refresh = client.post("/auth/refresh", json={"refresh_token": login.json()["refresh_token"]})
    assert refresh.status_code == 200
    assert refresh.json()["access_token"]


def test_rbac_csrf_and_admin_confirmation():
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
    event = client.post(
        "/events",
        headers=admin_headers,
    no_csrf = {"Authorization": admin_headers["Authorization"]}
    denied = client.post(
        "/events",
        headers=no_csrf,
        json={
            "name": "Event2",
            "start_time": datetime.now(UTC).isoformat(),
            "end_time": (datetime.now(UTC) + timedelta(hours=2)).isoformat(),
            "status": "live",
        },
    )
    assert event.status_code == 200
    ch = client.post(
        "/challenges",
        headers=admin_headers,
        json={
            "event_id": event.json()["id"],
            "title": "Warmup",
            "category": "web",
            "difficulty": "easy",
            "type": "standard",
            "hierarchical_rule": {},
            "visibility": "public",
        },
    )
    assert ch.status_code == 200
    no_confirm = client.delete(f"/challenges/{ch.json()['id']}", headers=admin_headers)
    assert no_confirm.status_code == 412
    with_confirm = client.delete(
        f"/challenges/{ch.json()['id']}",
        headers={**admin_headers, "X-Admin-Confirmation": settings.admin_confirmation_phrase},
    )
    assert with_confirm.status_code == 200


def test_leaderboard_signing_and_submission():
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

    board = client.get(f"/leaderboard/{event_id}", headers=user_headers)
    assert board.status_code == 200
    payload = board.json()
    assert payload["rows"][0]["score"] == 100
    assert SigningService.verify(
        {"event_id": payload["event_id"], "rows": payload["rows"]},
        payload["signature"],
    )


def test_evidence_lock_and_file_security(tmp_path: Path):
    admin_headers = _register_and_login("infra", "super_admin")

    settings.evidence_lock_mode = True
    denied = client.post(
        "/events",
        headers=admin_headers,
        json={
            "name": "Blocked",
            "start_time": datetime.now(UTC).isoformat(),
            "end_time": (datetime.now(UTC) + timedelta(hours=1)).isoformat(),
            "status": "draft",
        },
    )
    assert denied.status_code == 423

    settings.evidence_lock_mode = False
    sample = tmp_path / "upload.bin"
    sample.write_bytes(b"cerberus-security")
    digest = __import__("hashlib").sha256(b"cerberus-security").hexdigest()

    verify = client.post(
        "/files/verify",
        headers=admin_headers,
        json={"path": str(sample), "expected_sha256": digest},
    )
    assert verify.status_code == 200
    assert verify.json()["hash_valid"] is True
    assert verify.json()["antivirus"]["status"] == "clean"


def test_https_header_enforced_outside_dev():
    settings.app_env = "production"
    r = client.get("/health", headers={"x-forwarded-proto": "http"})
    assert r.status_code == 426
    ok = client.get("/health", headers={"x-forwarded-proto": "https"})
    assert ok.status_code == 200
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
