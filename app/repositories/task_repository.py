from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import Task, TaskPriority, TaskStatus


class TaskRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, task_id: int) -> Task | None:
        return self.db.get(Task, task_id)

    def list_by_project(self, project_id: int) -> list[Task]:
        return list(self.db.execute(select(Task).where(Task.project_id == project_id)).scalars().all())

    def create(
        self,
        *,
        project_id: int,
        creator_id: int | None,
        title: str,
        description: str | None,
        assignee_id: int | None,
        priority: TaskPriority = TaskPriority.medium,
        due_date: datetime | None = None,
    ) -> Task:
        task = Task(
            project_id=project_id,
            creator_id=creator_id,
            title=title,
            description=description,
            assignee_id=assignee_id,
            priority=priority,
            due_date=due_date,
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

<<<<<<< HEAD
    def update(self, task: Task) -> Task:
=======
    def update_status(self, task: Task, status: TaskStatus) -> Task:
        task.status = status
>>>>>>> e9df211 (initial commit)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task
<<<<<<< HEAD

    def update_status(self, task: Task, status: TaskStatus) -> Task:
        task.status = status
        return self.update(task)
=======
>>>>>>> e9df211 (initial commit)
