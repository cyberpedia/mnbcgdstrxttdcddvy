from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from app.api.dependencies import get_notification_service, require_capability, require_csrf
from app.schemas.notification import AdminAlert, EmailNotification, NotificationCreate, SupportTicketCreate
from app.services.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("/ws-send")
async def send_ws(
    payload: NotificationCreate,
    current_user: dict = Depends(require_capability("send_notifications")),
    svc: NotificationService = Depends(get_notification_service),
):
    return await svc.push_ws(current_user["id"], payload.user_id, payload.model_dump())


@router.post("/email")
def send_email(
    payload: EmailNotification,
    current_user: dict = Depends(require_capability("send_notifications")),
    svc: NotificationService = Depends(get_notification_service),
):
    return svc.send_email(current_user["id"], payload.to, payload.subject, payload.body)


@router.post("/admin-alert")
def admin_alert(
    payload: AdminAlert,
    svc: NotificationService = Depends(get_notification_service),
):
    # This endpoint is designed for automation systems (Alertmanager webhook).
    return svc.send_admin_alert(payload.model_dump())


@router.post("/support-ticket")
def support_ticket(
    payload: SupportTicketCreate,
    current_user: dict = Depends(require_csrf),
    svc: NotificationService = Depends(get_notification_service),
):
    return svc.create_support_ticket(current_user["id"], payload.subject, payload.message)


@router.websocket("/ws/{user_id}")
async def ws_endpoint(user_id: int, websocket: WebSocket):
    svc = get_notification_service()
    await svc.connect(user_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        svc.disconnect(user_id, websocket)
