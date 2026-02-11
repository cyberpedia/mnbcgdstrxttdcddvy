from __future__ import annotations

import hashlib
from pathlib import Path


class FileSecurityService:
    @staticmethod
    def sha256_file(path: str) -> str:
        digest = hashlib.sha256()
        with Path(path).open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    @staticmethod
    def verify_hash(path: str, expected_sha256: str) -> bool:
        return FileSecurityService.sha256_file(path) == expected_sha256.lower()

    @staticmethod
    def scan_antivirus(path: str) -> dict:
        # ClamAV integration point. Keep deterministic fallback for CI.
        _ = path
        return {"engine": "stub", "status": "clean"}
