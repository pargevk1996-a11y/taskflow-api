from app.services.auth_service import AuthService
from app.services.workspace_service import WorkspaceService
from app.services.project_service import ProjectService
from app.services.task_service import TaskService
from app.repositories.user_repository import UserRepository
from app.schemas.auth import RegisterRequest
from app.schemas.workspace import WorkspaceCreate
from app.schemas.project import ProjectCreate
from app.schemas.task import TaskCreate


def test_create_task(db):
    auth_service = AuthService(db)
    auth_service.register(
        RegisterRequest(
            email="task-owner@example.com",
            username="taskowner",
            password="strongpassword123",
        )
    )

    workspace = WorkspaceService(db).create_workspace(
        WorkspaceCreate(name="Task WS", slug="workspace-task"),
        owner_id=1,
    )
    current_user = UserRepository(db).get_by_id(1)
    assert current_user is not None
    project = ProjectService(db).create_project(
        ProjectCreate(workspace_id=workspace.id, name="Project B", description="Demo"),
        created_by_id=1,
        current_user=current_user,
    )

    task = TaskService(db).create_task(
        TaskCreate(project_id=project.id, title="First task", description="Task desc"),
        creator_id=1,
        current_user=current_user,
    )
    assert task.title == "First task"
