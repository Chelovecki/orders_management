from sqlalchemy import select

from src.exceptions import InvalidCredentialsError
from src.models import UserModel
from src.security.jwt import create_access_token
from src.security.passwords import verify_password
from src.services import BaseService
from src.settings import PostgresSettings


class AuthServices(BaseService):
    def __init__(self, session):
        super().__init__(session)

    async def authenticate(self, email: str, password: str) -> str:
        async with self.session_factory() as session:
            user = await session.scalar(
                select(UserModel).where(UserModel.email == email)
            )

            if not user:
                raise InvalidCredentialsError()

            if not verify_password(password, user.password_hash):
                raise InvalidCredentialsError()

            return create_access_token(subject=str(user.id))


auth_services = AuthServices(session=PostgresSettings.get_session())
