from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "taskflow_worker",
    broker=settings.celery_broker_dsn,
    backend=settings.celery_backend_dsn,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)
