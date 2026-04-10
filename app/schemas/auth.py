<<<<<<< HEAD
from pydantic import BaseModel, EmailStr
=======
from pydantic import BaseModel, EmailStr, Field
>>>>>>> e9df211 (initial commit)


class RegisterRequest(BaseModel):
    email: EmailStr
<<<<<<< HEAD
    login: str
    password: str
    confirm_password: str


class LoginRequest(BaseModel):
    login: str
    password: str


class RegisterResponse(BaseModel):
    message: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    message: str
=======
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
>>>>>>> e9df211 (initial commit)
