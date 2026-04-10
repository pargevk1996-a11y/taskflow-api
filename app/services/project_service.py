from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
<<<<<<< HEAD
from app.core.permissions import ensure_workspace_access, ensure_workspace_admin
from app.models.user import User
from app.repositories.project_repository import ProjectRepository
from app.repositories.workspace_repository import WorkspaceRepository
=======
from app.repositories.project_repository import ProjectRepository
>>>>>>> e9df211 (initial commit)
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate


class ProjectService:
    def __init__(self, db: Session) -> None:
        self.project_repository = ProjectRepository(db)
<<<<<<< HEAD
        self.workspace_repository = WorkspaceRepository(db)

    def create_project(self, payload: ProjectCreate, created_by_id: int | None, current_user: User) -> ProjectRead:
        ensure_workspace_admin(
            workspace_id=payload.workspace_id,
            user=current_user,
            workspace_repository=self.workspace_repository,
        )
=======

    def create_project(self, payload: ProjectCreate, created_by_id: int | None) -> ProjectRead:
>>>>>>> e9df211 (initial commit)
        project = self.project_repository.create(
            workspace_id=payload.workspace_id,
            name=payload.name,
            description=payload.description,
            created_by_id=created_by_id,
        )
        return ProjectRead.model_validate(project)

<<<<<<< HEAD
    def get_project(self, project_id: int, current_user: User) -> ProjectRead:
        project = self.project_repository.get_by_id(project_id)
        if not project:
            raise NotFoundError("Project not found")
        ensure_workspace_access(
            workspace_id=project.workspace_id,
            user=current_user,
            workspace_repository=self.workspace_repository,
        )
        return ProjectRead.model_validate(project)

    def update_project(self, project_id: int, payload: ProjectUpdate, current_user: User) -> ProjectRead:
        project = self.project_repository.get_by_id(project_id)
        if not project:
            raise NotFoundError("Project not found")
        ensure_workspace_admin(
            workspace_id=project.workspace_id,
            user=current_user,
            workspace_repository=self.workspace_repository,
        )
=======
    def get_project(self, project_id: int) -> ProjectRead:
        project = self.project_repository.get_by_id(project_id)
        if not project:
            raise NotFoundError("Project not found")
        return ProjectRead.model_validate(project)

    def update_project(self, project_id: int, payload: ProjectUpdate) -> ProjectRead:
        project = self.project_repository.get_by_id(project_id)
        if not project:
            raise NotFoundError("Project not found")
>>>>>>> e9df211 (initial commit)
        if payload.name is not None:
            project.name = payload.name
        if payload.description is not None:
            project.description = payload.description

        self.project_repository.db.add(project)
        self.project_repository.db.commit()
        self.project_repository.db.refresh(project)
        return ProjectRead.model_validate(project)
