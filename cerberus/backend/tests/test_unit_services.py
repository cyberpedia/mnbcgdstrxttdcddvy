from app.repositories.memory_store import MemoryStore
from app.services.challenge_service import ChallengeService
from app.services.event_service import EventService
from app.services.leaderboard_service import LeaderboardService


def test_challenge_unlock_logic():
    db = MemoryStore()
    svc = ChallengeService(db)

    c1 = svc.create_challenge(
        actor_id=1,
        payload={
            "event_id": 1,
            "title": "Base",
            "category": "web",
            "difficulty": "easy",
            "type": "standard",
            "hierarchical_rule": {},
            "visibility": "public",
        },
    )
    c2 = svc.create_challenge(
        actor_id=1,
        payload={
            "event_id": 1,
            "title": "Locked",
            "category": "web",
            "difficulty": "medium",
            "type": "standard",
            "hierarchical_rule": {"requires_challenge_id": c1["id"]},
            "visibility": "public",
        },
    )

    assert not svc.is_unlocked(user_id=99, challenge_id=c2["id"])
    db.submissions.append(
        {
            "id": 1,
            "user_id": 99,
            "event_id": 1,
            "challenge_id": c1["id"],
            "sub_challenge_id": None,
            "flag": "flag{ok}",
            "result": "correct",
        }
    )
    assert svc.is_unlocked(user_id=99, challenge_id=c2["id"])


def test_leaderboard_penalty_flow():
    db = MemoryStore()
    challenge_service = ChallengeService(db)
    leaderboard = LeaderboardService(db)

    challenge = challenge_service.create_challenge(
        actor_id=1,
        payload={
            "event_id": 1,
            "title": "Warmup",
            "category": "web",
            "difficulty": "easy",
            "type": "standard",
            "hierarchical_rule": {},
            "visibility": "public",
        },
    )
    sub = challenge_service.create_sub_challenge(
        actor_id=1,
        challenge_id=challenge["id"],
        payload={"title": "Part A", "order": 1, "flag": "flag{ok}"},
    )
    hint = challenge_service.add_hint(
        actor_id=1,
        challenge_id=challenge["id"],
        payload={"content": "peek", "penalty": 25, "enabled": False},
    )

    leaderboard.submit(
        actor_id=7,
        payload={
            "event_id": 1,
            "challenge_id": challenge["id"],
            "sub_challenge_id": sub["id"],
            "flag": "flag{ok}",
            "challenge_service": challenge_service,
        },
    )

    board = leaderboard.calculate(event_id=1)
    assert board["rows"][0]["score"] == 100

    challenge_service.set_hint_enabled(actor_id=1, hint_id=hint["id"], enabled=True)
    board2 = leaderboard.calculate(event_id=1)
    assert board2["rows"][0]["score"] == 75


def test_event_signing_present():
    db = MemoryStore()
    svc = EventService(db)
    event = svc.create_event(
        actor_id=1,
        payload={
            "name": "Event",
            "start_time": "2026-01-01T00:00:00Z",
            "end_time": "2026-01-01T03:00:00Z",
            "theme": "dark",
            "status": "draft",
        },
    )
    assert "signature" in event
