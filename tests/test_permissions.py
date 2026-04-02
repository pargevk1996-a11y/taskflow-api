import pytest

from app.core.exceptions import PermissionDeniedError
from app.models.workspace_member import WorkspaceMember, WorkspaceRole
from app.repositories.user_repository import UserRepository
from app.schemas.auth import RegisterRequest
from app.schemas.comment import CommentCreate, CommentUpdate
from app.schemas.project import ProjectCreate
from app.schemas.task import TaskCreate
from app.schemas.workspace import WorkspaceCreate
from app.services.auth_service import AuthService
from app.services.comment_service import CommentService
from app.services.project_service import ProjectService
from app.services.task_service import TaskService
from app.services.workspace_service import WorkspaceService


def test_member_cannot_create_project_in_workspace(db):
    auth = AuthService(db)
    auth.register(RegisterRequest(email="owner@x.com", username="owner", password="strongpassword123"))
    auth.register(RegisterRequest(email="member@x.com", username="member", password="strongpassword123"))

    owner = UserRepository(db).get_by_id(1)
    member = UserRepository(db).get_by_id(2)
    assert owner and member

    workspace = WorkspaceService(db).create_workspace(
        WorkspaceCreate(name="WS", slug="ws-member-create-project"),
        owner_id=owner.id,
    )

    db.add(WorkspaceMember(workspace_id=workspace.id, user_id=member.id, role=WorkspaceRole.member))
    db.commit()

    with pytest.raises(PermissionDeniedError):
        ProjectService(db).create_project(
            ProjectCreate(workspace_id=workspace.id, name="Forbidden", description="x"),
            created_by_id=member.id,
            current_user=member,
        )


def test_non_member_cannot_list_workspace_tasks(db):
    auth = AuthService(db)
    auth.register(RegisterRequest(email="owner2@x.com", username="owner2", password="strongpassword123"))
    auth.register(RegisterRequest(email="stranger@x.com", username="stranger", password="strongpassword123"))

    owner = UserRepository(db).get_by_id(1)
    stranger = UserRepository(db).get_by_id(2)
    assert owner and stranger

    workspace = WorkspaceService(db).create_workspace(
        WorkspaceCreate(name="WS2", slug="ws-non-member-tasks"),
        owner_id=owner.id,
    )
    project = ProjectService(db).create_project(
        ProjectCreate(workspace_id=workspace.id, name="Proj", description="d"),
        created_by_id=owner.id,
        current_user=owner,
    )
    TaskService(db).create_task(
        TaskCreate(project_id=project.id, title="T1", description="desc"),
        creator_id=owner.id,
        current_user=owner,
    )

    with pytest.raises(PermissionDeniedError):
        TaskService(db).list_tasks(project.id, current_user=stranger)


def test_user_cannot_edit_foreign_comment(db):
    auth = AuthService(db)
    auth.register(RegisterRequest(email="author@x.com", username="author", password="strongpassword123"))
    auth.register(RegisterRequest(email="other@x.com", username="other", password="strongpassword123"))

    author = UserRepository(db).get_by_id(1)
    other = UserRepository(db).get_by_id(2)
    assert author and other

    workspace = WorkspaceService(db).create_workspace(
        WorkspaceCreate(name="WS3", slug="ws-comment-edit"),
        owner_id=author.id,
    )
    project = ProjectService(db).create_project(
        ProjectCreate(workspace_id=workspace.id, name="P3", description="d"),
        created_by_id=author.id,
        current_user=author,
    )
    task = TaskService(db).create_task(
        TaskCreate(project_id=project.id, title="Task", description="desc"),
        creator_id=author.id,
        current_user=author,
    )
    comment = CommentService(db).create_comment(
        CommentCreate(task_id=task.id, body="original"),
        author_id=author.id,
        current_user=author,
    )

    with pytest.raises(PermissionDeniedError):
        CommentService(db).update_comment(comment.id, CommentUpdate(body="hacked"), current_user=other)
