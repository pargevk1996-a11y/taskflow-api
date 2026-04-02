from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, PermissionDeniedError
from app.models.notification import NotificationType
from app.models.user import User
from app.repositories.notification_repository import NotificationRepository
from app.schemas.notification import NotificationCreate, NotificationRead


class NotificationService:
    def __init__(self, db: Session) -> None:
        self.notification_repository = NotificationRepository(db)

    def create_notification(self, payload: NotificationCreate, current_user: User) -> NotificationRead:
        if payload.user_id != current_user.id and not current_user.is_superuser:
            raise PermissionDeniedError("You can create notifications only for yourself")
        notification = self.notification_repository.create(
            user_id=payload.user_id,
            type=NotificationType(payload.type.value),
            title=payload.title,
            message=payload.message,
        )
        return NotificationRead.model_validate(notification)

    def list_user_notifications(self, user_id: int) -> list[NotificationRead]:
        notifications = self.notification_repository.list_by_user(user_id)
        return [NotificationRead.model_validate(item) for item in notifications]

    def mark_as_read(self, notification_id: int, current_user: User) -> NotificationRead:
        notification = self.notification_repository.get_by_id(notification_id)
        if not notification:
            raise NotFoundError("Notification not found")
        if notification.user_id != current_user.id and not current_user.is_superuser:
            raise PermissionDeniedError("You can mark only your own notifications as read")
        updated = self.notification_repository.mark_as_read(notification)
        return NotificationRead.model_validate(updated)
