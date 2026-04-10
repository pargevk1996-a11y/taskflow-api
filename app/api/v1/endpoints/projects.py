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
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProjectRead:
    service = ProjectService(db)
<<<<<<< HEAD
    return service.create_project(payload, created_by_id=current_user.id, current_user=current_user)
=======
    return service.create_project(payload, created_by_id=current_user.id)
>>>>>>> e9df211 (initial commit)


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
<<<<<<< HEAD
    current_user: User = Depends(get_current_user),
) -> ProjectRead:
    service = ProjectService(db)
    return service.get_project(project_id, current_user)
=======
    _: User = Depends(get_current_user),
) -> ProjectRead:
    service = ProjectService(db)
    try:
        return service.get_project(project_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
>>>>>>> e9df211 (initial commit)


@router.patch("/{project_id}", response_model=ProjectRead)
def update_project(
    project_id: int,
    payload: ProjectUpdate,
    db: Session = Depends(get_db),
<<<<<<< HEAD
    current_user: User = Depends(get_current_user),
) -> ProjectRead:
    service = ProjectService(db)
    return service.update_project(project_id, payload, current_user)
=======
    _: User = Depends(get_current_user),
) -> ProjectRead:
    service = ProjectService(db)
    try:
        return service.update_project(project_id, payload)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
>>>>>>> e9df211 (initial commit)
