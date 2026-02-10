from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from src.exceptions import UserAlreadyExistsError
from src.models import UserModel
from src.services import BaseService
from src.settings import PostgresSettings


class UserServices(BaseService):
    def __init__(self, session):
        super().__init__(session)

    async def save_user(self, name: str, email: str) -> UserModel:
        async with self.session_factory() as session:
            user = UserModel(name=name, email=email)
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


auth_services = UserServices(PostgresSettings.get_session())
