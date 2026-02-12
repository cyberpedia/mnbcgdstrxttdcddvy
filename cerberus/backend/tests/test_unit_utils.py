from app.core.file_security import FileSecurityService
from app.core.security import sanitize_text
from app.core.signing import SigningService


def test_signing_roundtrip():
    payload = {"event_id": 1, "rows": [{"user_id": 2, "score": 100}]}
    signature = SigningService.sign(payload)
    assert SigningService.verify(payload, signature)
    assert not SigningService.verify(payload, signature + "0")


def test_sanitize_text_xss_payload():
    raw = '<img src=x onerror=alert(1)>'
    clean = sanitize_text(raw)
    assert "<img" not in clean
    assert "&lt;img" in clean


def test_file_hash_verification(tmp_path):
    sample = tmp_path / "sample.bin"
    sample.write_bytes(b"cerberus-unit")
    digest = FileSecurityService.sha256_file(str(sample))
    assert FileSecurityService.verify_hash(str(sample), digest)
