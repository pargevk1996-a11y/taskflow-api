from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.workspace import Workspace


class WorkspaceRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, workspace_id: int) -> Workspace | None:
        return self.db.get(Workspace, workspace_id)

    def get_by_slug(self, slug: str) -> Workspace | None:
        return self.db.execute(select(Workspace).where(Workspace.slug == slug)).scalar_one_or_none()

    def list_by_owner(self, owner_id: int) -> list[Workspace]:
        return list(self.db.execute(select(Workspace).where(Workspace.owner_id == owner_id)).scalars().all())

    def create(self, *, name: str, slug: str, owner_id: int) -> Workspace:
        workspace = Workspace(name=name, slug=slug, owner_id=owner_id)
        self.db.add(workspace)
        self.db.commit()
        self.db.refresh(workspace)
        return workspace
