from sqlalchemy.orm import Session

<<<<<<< HEAD
from app.core.exceptions import NotFoundError, UserAlreadyExistsError
=======
from app.core.exceptions import NotFoundError
>>>>>>> e9df211 (initial commit)
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserRead, UserUpdate


class UserService:
    def __init__(self, db: Session) -> None:
        self.user_repository = UserRepository(db)

    def get_user(self, user_id: int) -> UserRead:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return UserRead.model_validate(user)

    def update_user(self, user_id: int, payload: UserUpdate) -> UserRead:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")

<<<<<<< HEAD
        if payload.login is not None:
            existing_user = self.user_repository.get_by_login(payload.login)
            if existing_user and existing_user.id != user_id:
                raise UserAlreadyExistsError("Login is already taken")
            user.login = payload.login
=======
        if payload.username is not None:
            user.username = payload.username
>>>>>>> e9df211 (initial commit)
        if payload.is_active is not None:
            user.is_active = payload.is_active

        self.user_repository.db.add(user)
        self.user_repository.db.commit()
        self.user_repository.db.refresh(user)
        return UserRead.model_validate(user)
