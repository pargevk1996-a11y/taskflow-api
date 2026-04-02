from app.services.auth_service import AuthService
from app.core.config import settings
from app.core.exceptions import TokenInvalidError
from app.schemas.auth import LoginRequest, RegisterRequest
from jose import jwt
import pytest
from datetime import UTC, datetime, timedelta


def test_register_and_login(db):
    service = AuthService(db)

    token = service.register(
        RegisterRequest(
            email="authuser@example.com",
            username="authuser",
            password="strongpassword123",
        )
    )
    assert token.access_token
    assert token.refresh_token

    login_token = service.login(
        LoginRequest(
            email="authuser@example.com",
            password="strongpassword123",
        )
    )
    assert login_token.access_token


def test_refresh(db):
    service = AuthService(db)
    token = service.register(
        RegisterRequest(
            email="refresh@example.com",
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
            email="revoked@example.com",
            username="revokeduser",
            password="strongpassword123",
        )
    )
    service.revoke_refresh_token(token.refresh_token)
    with pytest.raises(TokenInvalidError):
        service.refresh(token.refresh_token)
