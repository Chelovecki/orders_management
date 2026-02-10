from fastapi import APIRouter
from .services import auth_services
from .schemas import UserRegisterSchema, UserSchema


auth_router = APIRouter(prefix='/auth')


@auth_router.post('/register')
async def user_register(form_data: UserRegisterSchema):
    saved = await auth_services.save_user(
        name=form_data.name,
        email=form_data.email
    )
    return UserSchema.model_validate(saved)
