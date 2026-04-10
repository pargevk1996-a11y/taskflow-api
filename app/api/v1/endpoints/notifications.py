<<<<<<< HEAD
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.notification import NotificationCreate, NotificationRead
from app.services.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.post("", response_model=NotificationRead, status_code=status.HTTP_201_CREATED)
def create_notification(
    payload: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> NotificationRead:
    service = NotificationService(db)
    return service.create_notification(payload, current_user)


@router.get("/me", response_model=list[NotificationRead])
def list_my_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[NotificationRead]:
    service = NotificationService(db)
    return service.list_user_notifications(current_user.id)


@router.patch("/{notification_id}/read", response_model=NotificationRead)
def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> NotificationRead:
    service = NotificationService(db)
    return service.mark_as_read(notification_id, current_user)
=======
from fastapi import APIRouter

router = APIRouter(prefix="/notifications", tags=["Notifications"])
>>>>>>> e9df211 (initial commit)
