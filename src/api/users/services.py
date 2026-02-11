from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from src.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from src.models import UserModel
from src.security.passwords import hash_password
from src.services import BaseService
from src.settings import PostgresSettings, oauth2_scheme
from src.security.jwt import decode_token


class UserServices(BaseService):
    def __init__(self, session):
        super().__init__(session)

    async def save_user(self, name: str, email: str, password: str) -> UserModel:
        async with self.session_factory() as session:
            hashed_password = hash_password(password)
            
            user = UserModel(name=name, email=email, password_hash=hashed_password)
            session.add(user)

            try:
                await session.commit()
                await session.refresh(user)
                return user
            except IntegrityError as e:
                await session.rollback()

                # Парсим ошибку, чтобы понять что именно не уникально
                error_msg = str(e.orig)

                if "users_name_key" in error_msg:
                    raise UserAlreadyExistsError('name', name)
                elif "users_email_key" in error_msg:
                    raise UserAlreadyExistsError('email', email)
                else:
                    raise UserAlreadyExistsError('user', 'Unknown')


user_services = UserServices(PostgresSettings.get_session())
