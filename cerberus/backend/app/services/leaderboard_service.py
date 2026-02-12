from __future__ import annotations

from collections import defaultdict

from fastapi import HTTPException

from app.core.signing import SigningService
from app.repositories.memory_store import MemoryStore


class LeaderboardService:
    def __init__(self, db: MemoryStore):
        self.db = db

    def submit(self, actor_id: int, payload: dict) -> dict:
        if payload["challenge_id"] not in self.db.challenges:
            raise HTTPException(status_code=404, detail="Challenge not found")

        challenge_service = payload["challenge_service"]
        if not challenge_service.is_unlocked(actor_id, payload["challenge_id"]):
            raise HTTPException(status_code=403, detail="Challenge is locked")

        correct_flags = [
            sc["flag"]
            for sc in self.db.sub_challenges.values()
            if sc["challenge_id"] == payload["challenge_id"]
            and (payload.get("sub_challenge_id") is None or sc["id"] == payload.get("sub_challenge_id"))
        ]
        result = "correct" if payload["flag"] in correct_flags else "incorrect"
        submission = {
            "id": len(self.db.submissions) + 1,
            "user_id": actor_id,
            "event_id": payload["event_id"],
            "challenge_id": payload["challenge_id"],
            "sub_challenge_id": payload.get("sub_challenge_id"),
            "flag": payload["flag"],
            "result": result,
        }
        self.db.submissions.append(submission)
        self.db.audit(
            actor_id,
            "submission.create",
            f"submission:{submission['id']}",
            after={k: v for k, v in submission.items() if k != "flag"},
        )
        return submission

    def calculate(self, event_id: int) -> dict:
        self.db.audit(actor_id, "submission.create", f"submission:{submission['id']}", after=submission)
        return submission

    def calculate(self, event_id: int) -> list[dict]:
        scores = defaultdict(int)
        for sub in self.db.submissions:
            if sub["event_id"] != event_id:
                continue
            if sub["result"] == "correct":
                scores[sub["user_id"]] += 100

        penalties = defaultdict(int)
        for hint in self.db.hints.values():
            if hint["enabled"]:
                challenge_id = hint["challenge_id"]
                users_for_challenge = {
                    s["user_id"] for s in self.db.submissions if s["challenge_id"] == challenge_id
                }
                users_for_challenge = {s["user_id"] for s in self.db.submissions if s["challenge_id"] == challenge_id}
                for uid in users_for_challenge:
                    penalties[uid] += hint["penalty"]

        rows = []
        for user_id, score in scores.items():
            rows.append({"user_id": user_id, "score": max(0, score - penalties[user_id])})
        rows.sort(key=lambda r: r["score"], reverse=True)

        payload = {"event_id": event_id, "rows": rows}
        signature = SigningService.sign(payload)
        return {**payload, "signature": signature}
        return rows
