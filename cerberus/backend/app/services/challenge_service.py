from __future__ import annotations

from fastapi import HTTPException

from app.core.security import sanitize_text
from app.repositories.memory_store import MemoryStore


class ChallengeService:
    def __init__(self, db: MemoryStore):
        self.db = db

    def create_challenge(self, actor_id: int, payload: dict) -> dict:
        challenge_id = self.db.next_id("challenges")
        payload = payload.copy()
        payload.update({"id": challenge_id, "title": sanitize_text(payload["title"])})
        self.db.challenges[challenge_id] = payload
        self.db.audit(actor_id, "challenge.create", f"challenge:{challenge_id}", after=payload)
        return payload

    def update_challenge(self, actor_id: int, challenge_id: int, patch: dict) -> dict:
        challenge = self.db.challenges.get(challenge_id)
        if not challenge:
            raise HTTPException(status_code=404, detail="Challenge not found")
        before = challenge.copy()
        for key, value in patch.items():
            if value is not None:
                challenge[key] = sanitize_text(value) if isinstance(value, str) else value
        self.db.audit(actor_id, "challenge.update", f"challenge:{challenge_id}", before=before, after=challenge)
        return challenge

    def delete_challenge(self, actor_id: int, challenge_id: int) -> dict:
        challenge = self.db.challenges.pop(challenge_id, None)
        if not challenge:
            raise HTTPException(status_code=404, detail="Challenge not found")
        self.db.audit(actor_id, "challenge.delete", f"challenge:{challenge_id}", before=challenge)
        return {"deleted": True, "id": challenge_id}

    def create_sub_challenge(self, actor_id: int, challenge_id: int, payload: dict) -> dict:
        if challenge_id not in self.db.challenges:
            raise HTTPException(status_code=404, detail="Challenge not found")
        sid = self.db.next_id("sub_challenges")
        entry = {"id": sid, "challenge_id": challenge_id, **payload}
        if any(
            sc["challenge_id"] == challenge_id and sc["order"] == payload["order"]
            for sc in self.db.sub_challenges.values()
        ):
        if any(sc["challenge_id"] == challenge_id and sc["order"] == payload["order"] for sc in self.db.sub_challenges.values()):
            raise HTTPException(status_code=409, detail="Duplicate sub-challenge order")
        self.db.sub_challenges[sid] = entry
        self.db.audit(actor_id, "sub_challenge.create", f"sub_challenge:{sid}", after=entry)
        return entry

    def add_hint(self, actor_id: int, challenge_id: int, payload: dict) -> dict:
        if challenge_id not in self.db.challenges:
            raise HTTPException(status_code=404, detail="Challenge not found")
        hid = self.db.next_id("hints")
        entry = {
            "id": hid,
            "challenge_id": challenge_id,
            "content": sanitize_text(payload["content"]),
            "penalty": payload["penalty"],
            "enabled": payload["enabled"],
        }
        entry = {"id": hid, "challenge_id": challenge_id, "content": sanitize_text(payload["content"]), "penalty": payload["penalty"], "enabled": payload["enabled"]}
        self.db.hints[hid] = entry
        self.db.audit(actor_id, "hint.create", f"hint:{hid}", after=entry)
        return entry

    def set_hint_enabled(self, actor_id: int, hint_id: int, enabled: bool) -> dict:
        hint = self.db.hints.get(hint_id)
        if not hint:
            raise HTTPException(status_code=404, detail="Hint not found")
        before = hint.copy()
        hint["enabled"] = enabled
        self.db.audit(actor_id, "hint.toggle", f"hint:{hint_id}", before=before, after=hint)
        return hint

    def is_unlocked(self, user_id: int, challenge_id: int) -> bool:
        challenge = self.db.challenges.get(challenge_id)
        if not challenge:
            return False
        prereq = challenge.get("hierarchical_rule", {}).get("requires_challenge_id")
        if not prereq:
            return True
        return any(
            s["user_id"] == user_id
            and s["challenge_id"] == prereq
            and s["result"] == "correct"
            s["user_id"] == user_id and s["challenge_id"] == prereq and s["result"] == "correct"
            for s in self.db.submissions
        )
