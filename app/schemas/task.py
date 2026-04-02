from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class TaskStatusSchema(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class TaskPrioritySchema(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskCreate(BaseModel):
    project_id: int
    title: str = Field(min_length=2, max_length=255)
    description: str | None = None
    assignee_id: int | None = None
    priority: TaskPrioritySchema = TaskPrioritySchema.medium
    due_date: datetime | None = None


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=255)
    description: str | None = None
    status: TaskStatusSchema | None = None
    priority: TaskPrioritySchema | None = None
    assignee_id: int | None = None
    due_date: datetime | None = None


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    creator_id: int | None
    assignee_id: int | None
    title: str
    description: str | None
    status: TaskStatusSchema
    priority: TaskPrioritySchema
    due_date: datetime | None
    created_at: datetime
    updated_at: datetime
