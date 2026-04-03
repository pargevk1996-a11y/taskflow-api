from collections.abc import Generator

from fastapi import Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.db.session import get_db as db_session_dependency
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest


def get_db() -> Generator[Session, None, None]:
    yield from db_session_dependency()


def get_login_form(
    username: str = Form(...),
    password: str = Form(...),
) -> LoginRequest:
    return LoginRequest(username=username, password=password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


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
    try:
        user_id = int(sub)
    except (TypeError, ValueError) as exc:
        raise credentials_error from exc

    user = UserRepository(db).get_by_id(user_id)
    if not user:
        raise credentials_error
    return user
