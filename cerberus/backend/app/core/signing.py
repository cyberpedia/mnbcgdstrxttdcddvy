from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any

from app.core.config import settings


class SigningService:
    @staticmethod
    def _normalize(payload: dict[str, Any]) -> bytes:
        return json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

    @staticmethod
    def sign(payload: dict[str, Any]) -> str:
        normalized = SigningService._normalize(payload)
        return hmac.new(
            settings.signing_secret.encode("utf-8"),
            normalized,
            hashlib.sha256,
        ).hexdigest()

    @staticmethod
    def verify(payload: dict[str, Any], signature: str) -> bool:
        expected = SigningService.sign(payload)
        return hmac.compare_digest(expected, signature)
