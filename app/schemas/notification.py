from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class NotificationTypeSchema(str, Enum):
    task_assigned = "task_assigned"
    task_commented = "task_commented"
    workspace_invite = "workspace_invite"
    system = "system"


class NotificationCreate(BaseModel):
    user_id: int
    type: NotificationTypeSchema
    title: str = Field(min_length=1, max_length=255)
    message: str = Field(min_length=1, max_length=5000)


class NotificationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    type: NotificationTypeSchema
    title: str
    message: str
    is_read: bool
    created_at: datetime
