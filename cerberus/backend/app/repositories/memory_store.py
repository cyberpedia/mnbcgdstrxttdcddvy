from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class MemoryStore:
    users: dict[int, dict] = field(default_factory=dict)
    challenges: dict[int, dict] = field(default_factory=dict)
    sub_challenges: dict[int, dict] = field(default_factory=dict)
    hints: dict[int, dict] = field(default_factory=dict)
    submissions: list[dict] = field(default_factory=list)
    events: dict[int, dict] = field(default_factory=dict)
    notifications: list[dict] = field(default_factory=list)
    audit_logs: list[dict] = field(default_factory=list)
    ui_config: dict[str, str] = field(default_factory=dict)

    _ids: dict[str, int] = field(default_factory=lambda: {
        "users": 0,
        "challenges": 0,
        "sub_challenges": 0,
        "hints": 0,
        "events": 0,
        "notifications": 0,
    })

    def next_id(self, key: str) -> int:
        self._ids[key] += 1
        return self._ids[key]

    def audit(self, actor_id: int | None, action: str, target: str, before=None, after=None) -> None:
        self.audit_logs.append(
            {
                "actor_id": actor_id,
                "action": action,
                "target": target,
                "before": before,
                "after": after,
                "timestamp": datetime.now(UTC),
            }
        )


store = MemoryStore()
