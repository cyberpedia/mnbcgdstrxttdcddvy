from fastapi import APIRouter, Depends

from app.api.dependencies import get_ui_config_service, require_capability
from app.schemas.ui_config import UIConfigPayload
from app.services.ui_config_service import UIConfigService

router = APIRouter(prefix="/ui-config", tags=["ui-config"])


@router.put("")
def set_ui_config(
    payload: UIConfigPayload,
    current_user: dict = Depends(require_capability("manage_ui_config")),
    svc: UIConfigService = Depends(get_ui_config_service),
):
    return svc.set_config(current_user["id"], payload.model_dump())


@router.get("")
def get_ui_config(svc: UIConfigService = Depends(get_ui_config_service)):
    return svc.get_config()
