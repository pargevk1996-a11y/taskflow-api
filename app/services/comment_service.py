from sqlalchemy.orm import Session

<<<<<<< HEAD
from app.core.exceptions import NotFoundError, PermissionDeniedError
from app.core.permissions import ensure_workspace_access, ensure_workspace_admin
from app.models.user import User
from app.repositories.project_repository import ProjectRepository
from app.repositories.comment_repository import CommentRepository
from app.repositories.task_repository import TaskRepository
from app.repositories.workspace_repository import WorkspaceRepository
=======
from app.core.exceptions import NotFoundError
from app.repositories.comment_repository import CommentRepository
>>>>>>> e9df211 (initial commit)
from app.schemas.comment import CommentCreate, CommentRead, CommentUpdate


class CommentService:
    def __init__(self, db: Session) -> None:
        self.comment_repository = CommentRepository(db)
<<<<<<< HEAD
        self.task_repository = TaskRepository(db)
        self.project_repository = ProjectRepository(db)
        self.workspace_repository = WorkspaceRepository(db)

    def create_comment(self, payload: CommentCreate, author_id: int | None, current_user: User) -> CommentRead:
        task = self.task_repository.get_by_id(payload.task_id)
        if not task:
            raise NotFoundError("Task not found")
        project = self.project_repository.get_by_id(task.project_id)
        if not project:
            raise NotFoundError("Project not found")
        ensure_workspace_access(
            workspace_id=project.workspace_id,
            user=current_user,
            workspace_repository=self.workspace_repository,
        )
        comment = self.comment_repository.create(task_id=payload.task_id, author_id=author_id, body=payload.body)
        return CommentRead.model_validate(comment)

    def list_task_comments(self, task_id: int, current_user: User) -> list[CommentRead]:
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise NotFoundError("Task not found")
        project = self.project_repository.get_by_id(task.project_id)
        if not project:
            raise NotFoundError("Project not found")
        ensure_workspace_access(
            workspace_id=project.workspace_id,
            user=current_user,
            workspace_repository=self.workspace_repository,
        )
        comments = self.comment_repository.list_by_task(task_id)
        return [CommentRead.model_validate(comment) for comment in comments]

    def update_comment(self, comment_id: int, payload: CommentUpdate, current_user: User) -> CommentRead:
        comment = self.comment_repository.get_by_id(comment_id)
        if not comment:
            raise NotFoundError("Comment not found")
        task = self.task_repository.get_by_id(comment.task_id)
        if not task:
            raise NotFoundError("Task not found")
        project = self.project_repository.get_by_id(task.project_id)
        if not project:
            raise NotFoundError("Project not found")

        if comment.author_id != current_user.id:
            try:
                ensure_workspace_admin(
                    workspace_id=project.workspace_id,
                    user=current_user,
                    workspace_repository=self.workspace_repository,
                )
            except (NotFoundError, PermissionDeniedError):
                raise PermissionDeniedError("You can edit only your own comment") from None

        comment.body = payload.body
        comment = self.comment_repository.update(comment)
=======

    def create_comment(self, payload: CommentCreate, author_id: int | None) -> CommentRead:
        comment = self.comment_repository.create(task_id=payload.task_id, author_id=author_id, body=payload.body)
        return CommentRead.model_validate(comment)

    def update_comment(self, comment_id: int, payload: CommentUpdate) -> CommentRead:
        comment = self.comment_repository.get_by_id(comment_id)
        if not comment:
            raise NotFoundError("Comment not found")

        comment.body = payload.body
        self.comment_repository.db.add(comment)
        self.comment_repository.db.commit()
        self.comment_repository.db.refresh(comment)
>>>>>>> e9df211 (initial commit)
        return CommentRead.model_validate(comment)
