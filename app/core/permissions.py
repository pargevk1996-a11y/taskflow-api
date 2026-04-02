from app.core.exceptions import NotFoundError, PermissionDeniedError
from app.models.user import User
from app.models.workspace_member import WorkspaceMember, WorkspaceRole
from app.repositories.workspace_repository import WorkspaceRepository


def ensure_superuser(user: User) -> None:
    if not user.is_superuser:
        raise PermissionDeniedError("Only superuser can perform this action")


def ensure_workspace_access(*, workspace_id: int, user: User, workspace_repository: WorkspaceRepository) -> None:
    workspace = workspace_repository.get_by_id(workspace_id)
    if not workspace:
        raise NotFoundError("Workspace not found")

    if workspace.owner_id == user.id:
        return

    member = (
        workspace_repository.db.query(WorkspaceMember)
        .filter(WorkspaceMember.workspace_id == workspace_id, WorkspaceMember.user_id == user.id)
        .one_or_none()
    )
    if not member:
        raise PermissionDeniedError("You do not have access to this workspace")


def ensure_workspace_admin(*, workspace_id: int, user: User, workspace_repository: WorkspaceRepository) -> None:
    workspace = workspace_repository.get_by_id(workspace_id)
    if not workspace:
        raise NotFoundError("Workspace not found")

    if workspace.owner_id == user.id:
        return

    member = (
        workspace_repository.db.query(WorkspaceMember)
        .filter(WorkspaceMember.workspace_id == workspace_id, WorkspaceMember.user_id == user.id)
        .one_or_none()
    )
    if not member or member.role not in {WorkspaceRole.admin, WorkspaceRole.owner}:
        raise PermissionDeniedError("Admin or owner role required")
