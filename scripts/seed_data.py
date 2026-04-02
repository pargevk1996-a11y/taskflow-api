"""Seed demo data for local development.

Usage:
    python -m scripts.seed_data
"""

from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.user import User
from app.models.workspace import Workspace


def main() -> None:
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == "demo@example.com").one_or_none()
        if not user:
            user = User(
                email="demo@example.com",
                username="demo",
                hashed_password=get_password_hash("demo12345"),
                is_active=True,
                is_superuser=False,
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        workspace = db.query(Workspace).filter(Workspace.slug == "demo-workspace").one_or_none()
        if not workspace:
            workspace = Workspace(name="Demo Workspace", slug="demo-workspace", owner_id=user.id)
            db.add(workspace)
            db.commit()

        print("Seed data created")
    finally:
        db.close()


if __name__ == "__main__":
    main()
