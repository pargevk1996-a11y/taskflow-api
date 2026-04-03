import pytest


@pytest.mark.asyncio
async def test_login_endpoint_accepts_json_body(api_client):
    register_response = await api_client.post(
        "/api/v1/auth/register",
        json={
            "email": "json-login@example.com",
            "username": "jsonlogin",
            "password": "strongpassword123",
        },
    )
    assert register_response.status_code == 201

    login_response = await api_client.post(
        "/api/v1/auth/login",
        json={
            "email": "json-login@example.com",
            "password": "strongpassword123",
        },
    )
    assert login_response.status_code == 200
    body = login_response.json()
    assert body["access_token"]
    assert body["refresh_token"]


@pytest.mark.asyncio
async def test_login_endpoint_accepts_oauth_form_body(api_client):
    register_response = await api_client.post(
        "/api/v1/auth/register",
        json={
            "email": "form-login@example.com",
            "username": "formlogin",
            "password": "strongpassword123",
        },
    )
    assert register_response.status_code == 201

    login_response = await api_client.post(
        "/api/v1/auth/login",
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
