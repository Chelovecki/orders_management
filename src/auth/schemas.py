from pydantic import BaseModel, ConfigDict, Field, EmailStr


class UserRegisterSchema(BaseModel):
    name: str = Field(
        ...,
        max_length=100,
        description='Input your username'
    )
    email: EmailStr = Field(..., description='Input your email')

    model_config = ConfigDict(
        extra='forbid',
        from_attributes=True
    )


class UserSchema(UserRegisterSchema):
    id: int
