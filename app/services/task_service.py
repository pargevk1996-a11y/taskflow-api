from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
<<<<<<< HEAD
from app.core.permissions import ensure_workspace_access
from app.models.task import TaskPriority, TaskStatus
from app.models.user import User
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.repositories.workspace_repository import WorkspaceRepository
=======
from app.models.task import TaskPriority, TaskStatus
from app.repositories.task_repository import TaskRepository
>>>>>>> e9df211 (initial commit)
from app.schemas.task import TaskCreate, TaskRead, TaskStatusSchema, TaskUpdate


class TaskService:
    def __init__(self, db: Session) -> None:
        self.task_repository = TaskRepository(db)
<<<<<<< HEAD
        self.project_repository = ProjectRepository(db)
        self.workspace_repository = WorkspaceRepository(db)

    def create_task(self, payload: TaskCreate, creator_id: int | None, current_user: User) -> TaskRead:
        project = self.project_repository.get_by_id(payload.project_id)
        if not project:
            raise NotFoundError("Project not found")
        ensure_workspace_access(
            workspace_id=project.workspace_id,
            user=current_user,
            workspace_repository=self.workspace_repository,
        )
=======

    def create_task(self, payload: TaskCreate, creator_id: int | None) -> TaskRead:
>>>>>>> e9df211 (initial commit)
        task = self.task_repository.create(
            project_id=payload.project_id,
            creator_id=creator_id,
            title=payload.title,
            description=payload.description,
            assignee_id=payload.assignee_id,
            priority=TaskPriority(payload.priority.value),
            due_date=payload.due_date,
        )
        return TaskRead.model_validate(task)

<<<<<<< HEAD
    def get_task(self, task_id: int, current_user: User) -> TaskRead:
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
        return TaskRead.model_validate(task)

    def list_tasks(self, project_id: int, current_user: User) -> list[TaskRead]:
        project = self.project_repository.get_by_id(project_id)
        if not project:
            raise NotFoundError("Project not found")
        ensure_workspace_access(
            workspace_id=project.workspace_id,
            user=current_user,
            workspace_repository=self.workspace_repository,
        )
        tasks = self.task_repository.list_by_project(project_id)
        return [TaskRead.model_validate(task) for task in tasks]

    def update_task(self, task_id: int, payload: TaskUpdate, current_user: User) -> TaskRead:
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
=======
    def get_task(self, task_id: int) -> TaskRead:
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise NotFoundError("Task not found")
        return TaskRead.model_validate(task)

    def update_task(self, task_id: int, payload: TaskUpdate) -> TaskRead:
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise NotFoundError("Task not found")
>>>>>>> e9df211 (initial commit)

        if payload.title is not None:
            task.title = payload.title
        if payload.description is not None:
            task.description = payload.description
        if payload.assignee_id is not None:
            task.assignee_id = payload.assignee_id
        if payload.priority is not None:
            task.priority = TaskPriority(payload.priority.value)
        if payload.status is not None:
            task.status = TaskStatus(payload.status.value)
        if payload.due_date is not None:
            task.due_date = payload.due_date

<<<<<<< HEAD
        task = self.task_repository.update(task)
        return TaskRead.model_validate(task)

    def update_status(self, task_id: int, status: TaskStatusSchema, current_user: User) -> TaskRead:
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
=======
        self.task_repository.db.add(task)
        self.task_repository.db.commit()
        self.task_repository.db.refresh(task)
        return TaskRead.model_validate(task)

    def update_status(self, task_id: int, status: TaskStatusSchema) -> TaskRead:
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise NotFoundError("Task not found")
>>>>>>> e9df211 (initial commit)
        updated = self.task_repository.update_status(task, TaskStatus(status.value))
        return TaskRead.model_validate(updated)
