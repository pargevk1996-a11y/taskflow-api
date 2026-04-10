from sqlalchemy.orm import Session

<<<<<<< HEAD
from app.core.permissions import ensure_workspace_access, ensure_workspace_admin
from app.models.user import User
=======
from app.core.exceptions import NotFoundError
>>>>>>> e9df211 (initial commit)
from app.repositories.workspace_repository import WorkspaceRepository
from app.schemas.workspace import WorkspaceCreate, WorkspaceRead, WorkspaceUpdate


class WorkspaceService:
    def __init__(self, db: Session) -> None:
        self.workspace_repository = WorkspaceRepository(db)

    def create_workspace(self, payload: WorkspaceCreate, owner_id: int) -> WorkspaceRead:
        workspace = self.workspace_repository.create(name=payload.name, slug=payload.slug, owner_id=owner_id)
        return WorkspaceRead.model_validate(workspace)

<<<<<<< HEAD
    def get_workspace(self, workspace_id: int, current_user: User) -> WorkspaceRead:
        ensure_workspace_access(
            workspace_id=workspace_id,
            user=current_user,
            workspace_repository=self.workspace_repository,
        )
        workspace = self.workspace_repository.get_by_id(workspace_id)
        return WorkspaceRead.model_validate(workspace)

    def update_workspace(self, workspace_id: int, payload: WorkspaceUpdate, current_user: User) -> WorkspaceRead:
        ensure_workspace_admin(
            workspace_id=workspace_id,
            user=current_user,
            workspace_repository=self.workspace_repository,
        )
        workspace = self.workspace_repository.get_by_id(workspace_id)
=======
    def get_workspace(self, workspace_id: int) -> WorkspaceRead:
        workspace = self.workspace_repository.get_by_id(workspace_id)
        if not workspace:
            raise NotFoundError("Workspace not found")
        return WorkspaceRead.model_validate(workspace)

    def update_workspace(self, workspace_id: int, payload: WorkspaceUpdate) -> WorkspaceRead:
        workspace = self.workspace_repository.get_by_id(workspace_id)
        if not workspace:
            raise NotFoundError("Workspace not found")
>>>>>>> e9df211 (initial commit)
        if payload.name is not None:
            workspace.name = payload.name

        self.workspace_repository.db.add(workspace)
        self.workspace_repository.db.commit()
        self.workspace_repository.db.refresh(workspace)
        return WorkspaceRead.model_validate(workspace)
