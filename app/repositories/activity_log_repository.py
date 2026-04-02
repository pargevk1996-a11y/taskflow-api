from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.activity_log import ActivityLog


class ActivityLogRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        *,
        action: str,
        entity_type: str,
        entity_id: int | None = None,
        details: str | None = None,
        user_id: int | None = None,
    ) -> ActivityLog:
        activity = ActivityLog(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details,
        )
        self.db.add(activity)
        self.db.commit()
        self.db.refresh(activity)
        return activity

    def list_recent(self, limit: int = 50) -> list[ActivityLog]:
        return list(self.db.execute(select(ActivityLog).order_by(ActivityLog.created_at.desc()).limit(limit)).scalars().all())
