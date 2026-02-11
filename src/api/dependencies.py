from fastapi import Depends
from pydantic import BaseModel, ConfigDict

from src.exceptions import InvalidCredentialsError
from src.models import UserModel
from src.security.jwt import decode_token
from src.settings import oauth2_scheme, PostgresSettings


async def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    payload = decode_token(token)
    user_id = payload.get('sub')

    if not user_id:
        raise InvalidCredentialsError()

    async with PostgresSettings.get_session()() as session:
        user = await session.get(UserModel, int(user_id))

        if not user:
            raise InvalidCredentialsError()

        return user


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        from_attributes=True
    )
