from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import BadRequestError, InvalidCredentialsError, TokenInvalidError, UserAlreadyExistsError
from app.core.security import create_access_token, create_refresh_token, decode_token, get_password_hash, verify_password
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse
from app.schemas.token import Token


class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.user_repository = UserRepository(db)

    def register(self, payload: RegisterRequest) -> RegisterResponse:
        login = self._validate_login(payload.login)
        self._validate_passwords(payload.password, payload.confirm_password)

        if self.user_repository.get_by_email(payload.email):
            raise UserAlreadyExistsError("Email is already taken")
        if self.user_repository.get_by_login(login):
            raise UserAlreadyExistsError("Login is already taken")

        user = self.user_repository.create(
            email=payload.email,
            login=login,
            hashed_password=get_password_hash(payload.password),
        )
        _ = user
        return RegisterResponse(message="Hey Dude! Log in!")

    def login(self, payload: LoginRequest) -> LoginResponse:
        user = self.authenticate(payload)
        token = self._issue_tokens_for_user(user)
        return LoginResponse(
            access_token=token.access_token,
            refresh_token=token.refresh_token,
            token_type=token.token_type,
            message="Welcome Dude!",
        )

    def authenticate(self, payload: LoginRequest) -> User:
        login = self._validate_login(payload.login)
        self._validate_password_string(payload.password)

        user = self.user_repository.get_by_login(login)
        if not user:
            raise InvalidCredentialsError("Invalid login or password")
        if not verify_password(payload.password, user.hashed_password):
            raise InvalidCredentialsError("Invalid login or password")
        if not user.is_active:
            raise InvalidCredentialsError("User is inactive")

        return user

    def refresh(self, refresh_token: str) -> Token:
        token_payload = self._validate_refresh_token(refresh_token)
        try:
            user_id = int(token_payload["sub"])
        except (TypeError, ValueError) as exc:
            raise TokenInvalidError("Token subject is invalid") from exc

        user = self.db.get(User, user_id)
        if not user or not user.is_active:
            raise TokenInvalidError("User not found or inactive")

        stored_token = self.db.execute(
            select(RefreshToken).where(RefreshToken.user_id == user_id, RefreshToken.token == refresh_token)
        ).scalar_one_or_none()
        if not stored_token:
            raise TokenInvalidError("Refresh token not found")
        expires_at = stored_token.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=UTC)

        if expires_at <= datetime.now(UTC):
            self.db.delete(stored_token)
            self.db.commit()
            raise TokenInvalidError("Refresh token expired")

        self.db.delete(stored_token)
        self.db.commit()
        return self._issue_tokens_for_user(user)

    def revoke_refresh_token(self, refresh_token: str) -> None:
        stored_token = self.db.execute(select(RefreshToken).where(RefreshToken.token == refresh_token)).scalar_one_or_none()
        if stored_token:
            self.db.delete(stored_token)
            self.db.commit()

    def _validate_login(self, login: str) -> str:
        if not isinstance(login, str) or not login.strip():
            raise BadRequestError("Login is required and must be a non-empty string")
        return login.strip()

    def _validate_password_string(self, password: str) -> None:
        if not isinstance(password, str) or password == "":
            raise BadRequestError("Password is required and must be a string")

    def _validate_passwords(self, password: str, confirm_password: str) -> None:
        self._validate_password_string(password)
        self._validate_password_string(confirm_password)
        if password != confirm_password:
            raise BadRequestError("Password and confirm_password must match")

    def _issue_tokens_for_user(self, user: User) -> Token:
        subject = str(user.id)
        access_token = create_access_token(subject=subject)
        refresh_token = create_refresh_token(subject=subject)
        refresh_expires_at = datetime.now(UTC) + timedelta(days=settings.refresh_token_expire_days)

        db_refresh_token = RefreshToken(user_id=user.id, token=refresh_token, expires_at=refresh_expires_at)
        self.db.add(db_refresh_token)
        self.db.commit()

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )

    @staticmethod
    def _validate_refresh_token(token: str) -> dict:
        try:
            payload = decode_token(token)
        except ValueError as exc:
            raise TokenInvalidError("Invalid token") from exc

        if payload.get("type") != "refresh":
            raise TokenInvalidError("Token type is not refresh")
        if "sub" not in payload:
            raise TokenInvalidError("Token subject is missing")
        return payload
