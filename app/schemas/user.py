from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
<<<<<<< HEAD
    login: str = Field(min_length=3, max_length=100)
=======
    username: str = Field(min_length=3, max_length=100)
>>>>>>> e9df211 (initial commit)
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(BaseModel):
<<<<<<< HEAD
    login: str | None = Field(default=None, min_length=3, max_length=100)
=======
    username: str | None = Field(default=None, min_length=3, max_length=100)
>>>>>>> e9df211 (initial commit)
    is_active: bool | None = None


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
<<<<<<< HEAD
    login: str
=======
    username: str
>>>>>>> e9df211 (initial commit)
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
