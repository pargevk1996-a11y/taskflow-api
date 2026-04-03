from datetime import UTC, datetime, timedelta

import pytest
from jose import jwt

from app.core.config import settings
from app.core.exceptions import BadRequestError, InvalidCredentialsError, TokenInvalidError, UserAlreadyExistsError
from app.schemas.auth import LoginRequest, RegisterRequest
from app.services.auth_service import AuthService


def test_register_and_login(db):
    service = AuthService(db)

    register_response = service.register(
        RegisterRequest(
            email="authuser@example.com",
            login="authuser",
            password="strongpassword123",
            confirm_password="strongpassword123",
        )
    )
    assert register_response.message == "Hey Dude! Log in!"

    login_response = service.login(LoginRequest(login="authuser", password="strongpassword123"))
    assert login_response.access_token
    assert login_response.refresh_token
    assert login_response.message == "Welcome Dude!"


def test_register_rejects_password_mismatch(db):
    service = AuthService(db)

    with pytest.raises(BadRequestError, match="confirm_password must match"):
        service.register(
            RegisterRequest(
                email="mismatch@example.com",
                login="mismatch",
                password="strongpassword123",
                confirm_password="wrongpassword123",
            )
        )


def test_register_requires_unique_email(db):
    service = AuthService(db)
    service.register(
        RegisterRequest(
            email="authuser@example.com",
            login="authuser",
            password="strongpassword123",
            confirm_password="strongpassword123",
        )
    )

    with pytest.raises(UserAlreadyExistsError, match="Email is already taken"):
        service.register(
            RegisterRequest(
                email="authuser@example.com",
                login="another-login",
                password="strongpassword123",
                confirm_password="strongpassword123",
            )
        )


def test_register_requires_unique_login(db):
    service = AuthService(db)
    service.register(
        RegisterRequest(
            email="unique-login@example.com",
            login="duplicate-login",
            password="strongpassword123",
            confirm_password="strongpassword123",
        )
    )

    with pytest.raises(UserAlreadyExistsError, match="Login is already taken"):
        service.register(
            RegisterRequest(
                email="other@example.com",
                login="duplicate-login",
                password="anotherpassword123",
                confirm_password="anotherpassword123",
            )
        )


def test_login_with_invalid_login_raises(db):
    service = AuthService(db)

    with pytest.raises(InvalidCredentialsError, match="Invalid login or password"):
        service.login(LoginRequest(login="missing", password="strongpassword123"))


def test_login_with_invalid_password_raises(db):
    service = AuthService(db)
    service.register(
        RegisterRequest(
            email="bad-password@example.com",
            login="bad-password-login",
            password="strongpassword123",
            confirm_password="strongpassword123",
        )
    )

    with pytest.raises(InvalidCredentialsError, match="Invalid login or password"):
        service.login(LoginRequest(login="bad-password-login", password="wrongpassword"))


def test_login_with_inactive_user_raises(db):
    service = AuthService(db)
    service.register(
        RegisterRequest(
            email="inactive@example.com",
            login="inactive-login",
            password="strongpassword123",
            confirm_password="strongpassword123",
        )
    )
    user = service.user_repository.get_by_login("inactive-login")
    assert user is not None
    user.is_active = False
    db.add(user)
    db.commit()

    with pytest.raises(InvalidCredentialsError, match="User is inactive"):
        service.login(LoginRequest(login="inactive-login", password="strongpassword123"))


def test_refresh(db):
    service = AuthService(db)
    service.register(
        RegisterRequest(
            email="refresh@example.com",
            login="refreshuser",
            password="strongpassword123",
            confirm_password="strongpassword123",
        )
    )
    token = service.login(LoginRequest(login="refreshuser", password="strongpassword123"))

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
    service.register(
        RegisterRequest(
            email="revoked@example.com",
            login="revokeduser",
            password="strongpassword123",
            confirm_password="strongpassword123",
        )
    )
    token = service.login(LoginRequest(login="revokeduser", password="strongpassword123"))
    service.revoke_refresh_token(token.refresh_token)
    with pytest.raises(TokenInvalidError):
        service.refresh(token.refresh_token)
