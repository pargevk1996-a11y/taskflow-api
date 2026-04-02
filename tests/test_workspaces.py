from app.services.auth_service import AuthService
from app.services.workspace_service import WorkspaceService
from app.schemas.auth import RegisterRequest
from app.schemas.workspace import WorkspaceCreate


def test_create_workspace(db):
    auth_service = AuthService(db)
    auth_service.register(
        RegisterRequest(
            email="owner@example.com",
            username="owner",
            password="strongpassword123",
        )
    )

    service = WorkspaceService(db)
    workspace = service.create_workspace(
        WorkspaceCreate(name="Test Workspace", slug="test-workspace"),
        owner_id=1,
    )
    assert workspace.slug == "test-workspace"
