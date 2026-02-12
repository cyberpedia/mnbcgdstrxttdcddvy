from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.api.dependencies import require_capability
from app.core.file_security import FileSecurityService

router = APIRouter(prefix="/files", tags=["files"])


class FileVerifyRequest(BaseModel):
    path: str = Field(min_length=1)
    expected_sha256: str = Field(min_length=64, max_length=64)


@router.post("/verify")
def verify_file(
    payload: FileVerifyRequest,
    _user: dict = Depends(require_capability("manage_ui_config")),
):
    antivirus = FileSecurityService.scan_antivirus(payload.path)
    hash_valid = FileSecurityService.verify_hash(payload.path, payload.expected_sha256)
    return {"hash_valid": hash_valid, "antivirus": antivirus}
