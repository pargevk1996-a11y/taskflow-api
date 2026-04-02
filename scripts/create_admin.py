"""Create superuser from environment variables.

Usage:
    python -m scripts.create_admin
"""

from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.user import User

ADMIN_EMAIL = "admin@example.com"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "change_me_admin"


def main() -> None:
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == ADMIN_EMAIL).one_or_none()
        if existing:
            print("Admin already exists")
            return

        admin = User(
            email=ADMIN_EMAIL,
            username=ADMIN_USERNAME,
            hashed_password=get_password_hash(ADMIN_PASSWORD),
            is_active=True,
            is_superuser=True,
        )
        db.add(admin)
        db.commit()
        print("Admin created")
    finally:
        db.close()


if __name__ == "__main__":
    main()
