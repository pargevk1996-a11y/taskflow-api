from sqlalchemy.orm import Session

from app.repositories.activity_log_repository import ActivityLogRepository


class ActivityLogService:
    def __init__(self, db: Session) -> None:
        self.activity_log_repository = ActivityLogRepository(db)

    def log(
        self,
        *,
        action: str,
        entity_type: str,
        entity_id: int | None = None,
        details: str | None = None,
        user_id: int | None = None,
    ) -> None:
        self.activity_log_repository.create(
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details,
            user_id=user_id,
        )
