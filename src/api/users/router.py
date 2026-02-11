from fastapi import APIRouter

from src.api.users.schemas import UserRegisterSchema, UserSchema
from src.api.users.services import user_services


user_router = APIRouter(prefix='/user')


@user_router.post('/register')
async def user_register(form_data: UserRegisterSchema):
    saved = await user_services.save_user(
        name=form_data.name,
        email=form_data.email,
        password=form_data.password
    )
    return UserSchema.model_validate(saved)
