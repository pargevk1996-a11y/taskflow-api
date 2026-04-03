from app.services.auth_service import AuthService
from app.services.workspace_service import WorkspaceService
from app.services.project_service import ProjectService
from app.repositories.user_repository import UserRepository
from app.schemas.auth import RegisterRequest
from app.schemas.workspace import WorkspaceCreate
from app.schemas.project import ProjectCreate


def test_create_project(db):
    auth_service = AuthService(db)
    auth_service.register(
        RegisterRequest(
            email="project-owner@example.com",
            login="projectowner",
            password="strongpassword123",
            confirm_password="strongpassword123",
        )
    )

    workspace = WorkspaceService(db).create_workspace(
        WorkspaceCreate(name="Workspace", slug="workspace-project"),
        owner_id=1,
    )
    current_user = UserRepository(db).get_by_id(1)
    assert current_user is not None

    project = ProjectService(db).create_project(
        ProjectCreate(workspace_id=workspace.id, name="Project A", description="Demo"),
        created_by_id=1,
        current_user=current_user,
    )
    assert project.name == "Project A"
