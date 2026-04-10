from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        return self.db.execute(select(User).where(User.email == email)).scalar_one_or_none()

<<<<<<< HEAD
    def get_by_login(self, login: str) -> User | None:
        return self.db.execute(select(User).where(User.login == login)).scalar_one_or_none()

    def get_by_email_or_login(self, email: str, login: str) -> User | None:
        return self.db.execute(select(User).where(or_(User.email == email, User.login == login))).scalar_one_or_none()

    def create(self, *, email: str, login: str, hashed_password: str) -> User:
        user = User(
            email=email,
            login=login,
=======
    def get_by_username(self, username: str) -> User | None:
        return self.db.execute(select(User).where(User.username == username)).scalar_one_or_none()

    def get_by_email_or_username(self, email: str, username: str) -> User | None:
        return self.db.execute(select(User).where(or_(User.email == email, User.username == username))).scalar_one_or_none()

    def create(self, *, email: str, username: str, hashed_password: str) -> User:
        user = User(
            email=email,
            username=username,
>>>>>>> e9df211 (initial commit)
            hashed_password=hashed_password,
            is_active=True,
            is_superuser=False,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
