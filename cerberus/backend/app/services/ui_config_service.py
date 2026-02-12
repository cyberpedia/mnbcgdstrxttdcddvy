from __future__ import annotations

from app.core.security import sanitize_text
from app.repositories.memory_store import MemoryStore


class UIConfigService:
    def __init__(self, db: MemoryStore):
        self.db = db

    def set_config(self, actor_id: int, payload: dict) -> dict:
        clean = {
            "theme": sanitize_text(payload["theme"]),
            "logo_url": str(payload["logo_url"]),
            "primary_color": sanitize_text(payload["primary_color"]),
            "secondary_color": sanitize_text(payload["secondary_color"]),
            "assets": {k: sanitize_text(v) for k, v in payload.get("assets", {}).items()},
        }
        before = self.db.ui_config.copy()
        self.db.ui_config = clean
        self.db.audit(actor_id, "ui_config.update", "ui_config:global", before=before, after=clean)
        return clean

    def get_config(self) -> dict:
        return self.db.ui_config
