<<<<<<< HEAD
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskRead:
    service = TaskService(db)
    return service.create_task(payload, creator_id=current_user.id, current_user=current_user)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> TaskRead:
    service = TaskService(db)
    return service.get_task(task_id, current_user)


@router.get("", response_model=list[TaskRead])
def list_tasks(
    project_id: int = Query(..., ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[TaskRead]:
    service = TaskService(db)
    return service.list_tasks(project_id, current_user)


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskRead:
    service = TaskService(db)
    return service.update_task(task_id, payload, current_user)
=======
from fastapi import APIRouter

router = APIRouter(prefix="/tasks", tags=["Tasks"])
>>>>>>> e9df211 (initial commit)
