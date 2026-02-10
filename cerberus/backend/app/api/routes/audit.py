from fastapi import APIRouter, Depends

from app.api.dependencies import require_capability
from app.repositories.memory_store import store

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("")
def get_audit_logs(_user: dict = Depends(require_capability("view_audit"))):
    return store.audit_logs
