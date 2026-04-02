class EmailService:
    def send_email(self, *, to_email: str, subject: str, body: str) -> None:
        # Stub implementation. Real SMTP integration will be added with Celery tasks.
        _ = (to_email, subject, body)
