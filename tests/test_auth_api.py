import pytest


@pytest.mark.asyncio
async def test_login_endpoint_returns_welcome_message(api_client):
    register_response = await api_client.post(
        "/api/v1/auth/register",
        json={
            "username": "jsonlogin",
            "password": "strongpassword123",
        },
    )
    assert register_response.status_code == 201

    login_response = await api_client.post(
        "/api/v1/auth/login",
        data={"username": "jsonlogin", "password": "strongpassword123"},
    )
    assert login_response.status_code == 200
    assert login_response.json() == {"message": "Welcome dude!"}


@pytest.mark.asyncio
async def test_token_endpoint_accepts_oauth_form_body(api_client):
    register_response = await api_client.post(
        "/api/v1/auth/register",
        json={
            "username": "formlogin",
            "password": "strongpassword123",
        },
    )
    assert register_response.status_code == 201

    login_response = await api_client.post(
        "/api/v1/auth/token",
        data={
            "username": "formlogin",
            "password": "strongpassword123",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login_response.status_code == 200
    body = login_response.json()
    assert body["access_token"]
    assert body["refresh_token"]


@pytest.mark.asyncio
async def test_register_rejects_forbidden_password_symbols(api_client):
    response = await api_client.post(
        "/api/v1/auth/register",
        json={
            "username": "invalidpassuser",
            "password": "hello!",
        },
    )

    assert response.status_code == 400
    assert "Password must not contain" in response.json()["detail"]
