from fastapi import APIRouter
<<<<<<< HEAD
from fastapi import Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
=======
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.exceptions import NotFoundError
>>>>>>> e9df211 (initial commit)
from app.models.user import User
from app.schemas.workspace import WorkspaceCreate, WorkspaceRead, WorkspaceUpdate
from app.services.workspace_service import WorkspaceService

router = APIRouter(prefix="/workspaces", tags=["Workspaces"])


@router.post("", response_model=WorkspaceRead, status_code=status.HTTP_201_CREATED)
def create_workspace(
    payload: WorkspaceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> WorkspaceRead:
    service = WorkspaceService(db)
    return service.create_workspace(payload, owner_id=current_user.id)


@router.get("/{workspace_id}", response_model=WorkspaceRead)
def get_workspace(
    workspace_id: int,
    db: Session = Depends(get_db),
<<<<<<< HEAD
    current_user: User = Depends(get_current_user),
) -> WorkspaceRead:
    service = WorkspaceService(db)
    return service.get_workspace(workspace_id, current_user)
=======
    _: User = Depends(get_current_user),
) -> WorkspaceRead:
    service = WorkspaceService(db)
    try:
        return service.get_workspace(workspace_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
>>>>>>> e9df211 (initial commit)


@router.patch("/{workspace_id}", response_model=WorkspaceRead)
def update_workspace(
    workspace_id: int,
    payload: WorkspaceUpdate,
    db: Session = Depends(get_db),
<<<<<<< HEAD
    current_user: User = Depends(get_current_user),
) -> WorkspaceRead:
    service = WorkspaceService(db)
    return service.update_workspace(workspace_id, payload, current_user)
=======
    _: User = Depends(get_current_user),
) -> WorkspaceRead:
    service = WorkspaceService(db)
    try:
        return service.update_workspace(workspace_id, payload)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
>>>>>>> e9df211 (initial commit)
