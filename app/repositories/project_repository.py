from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project import Project


class ProjectRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, project_id: int) -> Project | None:
        return self.db.get(Project, project_id)

    def list_by_workspace(self, workspace_id: int) -> list[Project]:
        return list(self.db.execute(select(Project).where(Project.workspace_id == workspace_id)).scalars().all())

    def create(self, *, workspace_id: int, name: str, description: str | None, created_by_id: int | None) -> Project:
        project = Project(
            workspace_id=workspace_id,
            name=name,
            description=description,
            created_by_id=created_by_id,
        )
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project
