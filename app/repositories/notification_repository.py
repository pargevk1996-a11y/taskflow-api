from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.notification import Notification, NotificationType


class NotificationRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, notification_id: int) -> Notification | None:
        return self.db.get(Notification, notification_id)

    def list_by_user(self, user_id: int) -> list[Notification]:
        return list(
            self.db.execute(select(Notification).where(Notification.user_id == user_id).order_by(Notification.created_at.desc()))
            .scalars()
            .all()
        )

    def create(self, *, user_id: int, type: NotificationType, title: str, message: str) -> Notification:
        notification = Notification(
            user_id=user_id,
            type=type,
            title=title,
            message=message,
            is_read=False,
        )
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification

    def mark_as_read(self, notification: Notification) -> Notification:
        notification.is_read = True
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification
