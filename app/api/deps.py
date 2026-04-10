from collections.abc import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.db.session import get_db as db_session_dependency
from app.models.user import User
from app.repositories.user_repository import UserRepository


def get_db() -> Generator[Session, None, None]:
    yield from db_session_dependency()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
    except ValueError as exc:
        raise credentials_error from exc

    if payload.get("type") != "access":
        raise credentials_error
    sub = payload.get("sub")
    if not sub:
        raise credentials_error
<<<<<<< HEAD
    try:
        user_id = int(sub)
    except (TypeError, ValueError) as exc:
        raise credentials_error from exc

    user = UserRepository(db).get_by_id(user_id)
=======

    user = UserRepository(db).get_by_id(int(sub))
>>>>>>> e9df211 (initial commit)
    if not user:
        raise credentials_error
    return user
