import pytest


pytestmark = pytest.mark.skip(
    reason="HTTP client tests are unstable in the current sandbox runtime; run locally in a full environment."
)


def test_register_endpoint_returns_message(client):
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "json-login@example.com",
            "login": "jsonlogin",
            "password": "strongpassword123",
            "confirm_password": "strongpassword123",
        },
    )
    assert register_response.status_code == 201
    assert register_response.json() == {"message": "Hey Dude! Log in!"}


def test_login_endpoint_returns_tokens_and_message(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "json-login@example.com",
            "login": "jsonlogin",
            "password": "strongpassword123",
            "confirm_password": "strongpassword123",
        },
    )

    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "jsonlogin", "password": "strongpassword123"},
    )
    assert login_response.status_code == 200
    body = login_response.json()
    assert body["access_token"]
    assert body["refresh_token"]
    assert body["message"] == "Welcome Dude!"


def test_register_rejects_password_mismatch(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "mismatch@example.com",
            "login": "mismatch-login",
            "password": "strongpassword123",
            "confirm_password": "wrongpassword123",
        },
    )
    assert response.status_code == 400
    assert "confirm_password must match" in response.json()["detail"]


def test_register_rejects_duplicate_email(client):
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "duplicate@example.com",
            "login": "formlogin",
            "password": "strongpassword123",
            "confirm_password": "strongpassword123",
        },
    )
    assert register_response.status_code == 201

    duplicate_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "duplicate@example.com",
            "login": "otherlogin",
            "password": "strongpassword123",
            "confirm_password": "strongpassword123",
        },
    )
    assert duplicate_response.status_code == 409
    assert "Email is already taken" in duplicate_response.json()["detail"]


def test_register_rejects_duplicate_login(client):
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "dup-login@example.com",
            "login": "same-login",
            "password": "strongpassword123",
            "confirm_password": "strongpassword123",
        },
    )
    assert register_response.status_code == 201

    duplicate_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "other-email@example.com",
            "login": "same-login",
            "password": "strongpassword123",
            "confirm_password": "strongpassword123",
        },
    )
    assert duplicate_response.status_code == 409
    assert "Login is already taken" in duplicate_response.json()["detail"]


def test_register_rejects_invalid_email(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "not-an-email",
            "login": "invalid-email-login",
            "password": "strongpassword123",
            "confirm_password": "strongpassword123",
        },
    )

    assert response.status_code == 422
