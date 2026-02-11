from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from src.api.users.services import user_services
from src.api.users.schemas import UserRegisterSchema, UserSchema
from src.api.auth.services import auth_services

auth_router = APIRouter(prefix='/auth', tags=['auth'])


@auth_router.post('/token')
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    token = await auth_services.authenticate(
        email=form_data.username,
        password=form_data.password
    )
    return {
        'access_token': token,
        'token_type': 'bearer'
    }
