from app.services.email_service import EmailService
from app.tasks.celery_app import celery_app


@celery_app.task(name="taskflow.email.send")
def send_email_task(to_email: str, subject: str, body: str) -> None:
    EmailService().send_email(to_email=to_email, subject=subject, body=body)
