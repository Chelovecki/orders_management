from pydantic import EmailStr, Field

from src.api.dependencies import BaseSchema


class UserSchema(BaseSchema):
    id: int
    name: str
    email: EmailStr


class UserRegisterSchema(BaseSchema):
    name: str = Field(..., max_length=100, description="Input your username")
    email: EmailStr = Field(..., description="Input your email")
    password: str
