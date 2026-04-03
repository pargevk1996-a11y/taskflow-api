from app.services.auth_service import AuthService
from app.services.workspace_service import WorkspaceService
from app.services.project_service import ProjectService
from app.services.task_service import TaskService
from app.services.comment_service import CommentService
from app.repositories.user_repository import UserRepository
from app.schemas.auth import RegisterRequest
from app.schemas.workspace import WorkspaceCreate
from app.schemas.project import ProjectCreate
from app.schemas.task import TaskCreate
from app.schemas.comment import CommentCreate


def test_create_comment(db):
    auth_service = AuthService(db)
    auth_service.register(
        RegisterRequest(
            email="comment-owner@example.com",
            login="commentowner",
            password="strongpassword123",
            confirm_password="strongpassword123",
        )
    )

    workspace = WorkspaceService(db).create_workspace(
        WorkspaceCreate(name="Comment WS", slug="workspace-comment"),
        owner_id=1,
    )
    current_user = UserRepository(db).get_by_id(1)
    assert current_user is not None
    project = ProjectService(db).create_project(
        ProjectCreate(workspace_id=workspace.id, name="Project C", description="Demo"),
        created_by_id=1,
        current_user=current_user,
    )
    task = TaskService(db).create_task(
        TaskCreate(project_id=project.id, title="Task", description="Task desc"),
        creator_id=1,
        current_user=current_user,
    )

    comment = CommentService(db).create_comment(
        CommentCreate(task_id=task.id, body="Looks good"),
        author_id=1,
        current_user=current_user,
    )
    assert comment.body == "Looks good"
