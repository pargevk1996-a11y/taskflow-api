from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr | None = None
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str
