from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    login: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(BaseModel):
    login: str | None = Field(default=None, min_length=3, max_length=100)
    is_active: bool | None = None


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    login: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
