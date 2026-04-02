from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentRead, CommentUpdate
from app.services.comment_service import CommentService

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
def create_comment(
    payload: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CommentRead:
    service = CommentService(db)
    return service.create_comment(payload, author_id=current_user.id, current_user=current_user)


@router.get("", response_model=list[CommentRead])
def list_comments(
    task_id: int = Query(..., ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[CommentRead]:
    service = CommentService(db)
    return service.list_task_comments(task_id, current_user)


@router.patch("/{comment_id}", response_model=CommentRead)
def update_comment(
    comment_id: int,
    payload: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CommentRead:
    service = CommentService(db)
    return service.update_comment(comment_id, payload, current_user)
