from app.services.auth_service import AuthService
from app.core.config import settings
from app.core.exceptions import BadRequestError, TokenInvalidError, UserAlreadyExistsError
from app.schemas.auth import LoginRequest, RegisterRequest
from jose import jwt
import pytest
from datetime import UTC, datetime, timedelta


def test_register_and_login(db):
    service = AuthService(db)

    token = service.register(
        RegisterRequest(
            username="authuser",
            password="strongpassword123",
        )
    )
    assert token.access_token
    assert token.refresh_token

    login_token = service.login(
        LoginRequest(
            username="authuser",
            password="strongpassword123",
        )
    )
    assert login_token is None


def test_login_with_username(db):
    service = AuthService(db)

    service.register(
        RegisterRequest(
            username="username_login",
            password="strongpassword123",
        )
    )

    issued = service.issue_token(LoginRequest(username="username_login", password="strongpassword123"))
    assert issued.access_token


def test_register_rejects_forbidden_password_symbols(db):
    service = AuthService(db)

    with pytest.raises(BadRequestError, match=r"Password must not contain"):
        service.register(
            RegisterRequest(
                username="badpassworduser",
                password="bad.password",
            )
        )


def test_register_requires_unique_username(db):
    service = AuthService(db)
    service.register(RegisterRequest(username="duplicate", password="strongpassword123"))

    with pytest.raises(UserAlreadyExistsError, match="Username is already taken"):
        service.register(RegisterRequest(username="duplicate", password="anotherpassword"))


def test_refresh(db):
    service = AuthService(db)
    token = service.register(
        RegisterRequest(
            username="refreshuser",
            password="strongpassword123",
        )
    )

    refreshed = service.refresh(token.refresh_token)
    assert refreshed.access_token
    assert refreshed.refresh_token


def test_refresh_with_non_numeric_sub_raises_token_invalid(db):
    service = AuthService(db)
    invalid_refresh_token = jwt.encode(
        {"sub": "not-a-number", "type": "refresh"},
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    with pytest.raises(TokenInvalidError):
        service.refresh(invalid_refresh_token)


def test_refresh_with_malformed_token_raises_token_invalid(db):
    service = AuthService(db)
    with pytest.raises(TokenInvalidError):
        service.refresh("this-is-not-a-jwt")


def test_refresh_with_expired_token_raises_token_invalid(db):
    service = AuthService(db)
    expired_refresh_token = jwt.encode(
        {
            "sub": "1",
            "type": "refresh",
            "exp": datetime.now(UTC) - timedelta(minutes=1),
        },
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
    with pytest.raises(TokenInvalidError):
        service.refresh(expired_refresh_token)


def test_refresh_with_revoked_token_raises_token_invalid(db):
    service = AuthService(db)
    token = service.register(
        RegisterRequest(
            username="revokeduser",
            password="strongpassword123",
        )
    )
    service.revoke_refresh_token(token.refresh_token)
    with pytest.raises(TokenInvalidError):
        service.refresh(token.refresh_token)
