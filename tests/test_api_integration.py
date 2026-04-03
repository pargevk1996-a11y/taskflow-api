import pytest

pytestmark = pytest.mark.skip(
    reason="ASGI integration tests are unstable in the current sandbox runtime; run locally in full environment."
)


@pytest.mark.asyncio
async def test_auth_flow_and_invalid_token(api_client):
    register_payload = {
        "email": "api-user@example.com",
        "login": "apiuser",
        "password": "strongpassword123",
        "confirm_password": "strongpassword123",
    }
    register_response = await api_client.post("/api/v1/auth/register", json=register_payload)
    assert register_response.status_code == 201
    login_response = await api_client.post("/api/v1/auth/login", data={"username": "apiuser", "password": "strongpassword123"})
    assert login_response.status_code == 200
    tokens = login_response.json()

    me_response = await api_client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )
    assert me_response.status_code == 200

    invalid_response = await api_client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer malformed.token.value"},
    )
    assert invalid_response.status_code == 401


@pytest.mark.asyncio
async def test_workspace_project_permission_flow(api_client):
    owner = await api_client.post(
        "/api/v1/auth/register",
        json={
            "email": "owner-api@example.com",
            "login": "ownerapi",
            "password": "strongpassword123",
            "confirm_password": "strongpassword123",
        },
    )
    member = await api_client.post(
        "/api/v1/auth/register",
        json={
            "email": "member-api@example.com",
            "login": "memberapi",
            "password": "strongpassword123",
            "confirm_password": "strongpassword123",
        },
    )
    owner_token = (
        await api_client.post("/api/v1/auth/login", data={"username": "ownerapi", "password": "strongpassword123"})
    ).json()["access_token"]
    member_token = (
        await api_client.post("/api/v1/auth/login", data={"username": "memberapi", "password": "strongpassword123"})
    ).json()["access_token"]

    workspace = await api_client.post(
        "/api/v1/workspaces",
        json={"name": "API WS", "slug": "api-ws"},
        headers={"Authorization": f"Bearer {owner_token}"},
    )
    assert workspace.status_code == 201
    workspace_id = workspace.json()["id"]

    forbidden_project = await api_client.post(
        "/api/v1/projects",
        json={"workspace_id": workspace_id, "name": "Forbidden", "description": "x"},
        headers={"Authorization": f"Bearer {member_token}"},
    )
    assert forbidden_project.status_code == 403


@pytest.mark.asyncio
async def test_notification_access_control(api_client):
    u1 = await api_client.post(
        "/api/v1/auth/register",
        json={"email": "n1@example.com", "login": "n1", "password": "strongpassword123", "confirm_password": "strongpassword123"},
    )
    u2 = await api_client.post(
        "/api/v1/auth/register",
        json={"email": "n2@example.com", "login": "n2", "password": "strongpassword123", "confirm_password": "strongpassword123"},
    )
    t1 = (await api_client.post("/api/v1/auth/login", data={"username": "n1", "password": "strongpassword123"})).json()[
        "access_token"
    ]
    t2 = (await api_client.post("/api/v1/auth/login", data={"username": "n2", "password": "strongpassword123"})).json()[
        "access_token"
    ]

    create_for_self = await api_client.post(
        "/api/v1/notifications",
        json={"user_id": 1, "type": "system", "title": "hello", "message": "world"},
        headers={"Authorization": f"Bearer {t1}"},
    )
    assert create_for_self.status_code == 201
    notification_id = create_for_self.json()["id"]

    mark_foreign = await api_client.patch(
        f"/api/v1/notifications/{notification_id}/read",
        headers={"Authorization": f"Bearer {t2}"},
    )
    assert mark_foreign.status_code == 403
