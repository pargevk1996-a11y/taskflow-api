from datetime import UTC, datetime

from sqlalchemy import delete

from app.db.session import SessionLocal
from app.models.refresh_token import RefreshToken
from app.tasks.celery_app import celery_app


@celery_app.task(name="taskflow.cleanup.expired_refresh_tokens")
def cleanup_expired_refresh_tokens() -> int:
    db = SessionLocal()
    try:
        stmt = delete(RefreshToken).where(RefreshToken.expires_at <= datetime.now(UTC))
        result = db.execute(stmt)
        db.commit()
        return int(result.rowcount or 0)
    finally:
        db.close()
