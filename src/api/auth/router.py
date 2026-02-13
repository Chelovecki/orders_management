from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.api.auth.services import auth_services

auth_router = APIRouter(tags=["auth"])


@auth_router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    token = await auth_services.authenticate(
        email=form_data.username, password=form_data.password
    )
    return {"access_token": token, "token_type": "bearer"}
