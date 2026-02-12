import os

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

load_dotenv("docker/.env.local")


class PostgresSettings:
    HOST = os.getenv("POSTGRES_HOST")
    DB = os.getenv("POSTGRES_DB")
    USERNAME = os.getenv("POSTGRES_USERNAME")
    PORT = int(os.getenv("POSTGRES_PORT", "5432"))
    PASSWORD = os.getenv("POSTGRES_PASSWORD")

    if not PASSWORD:
        raise Exception('The password is required. Set it in ".env"')

    @classmethod
    def get_async_url(cls):
        return f"postgresql+asyncpg://{cls.USERNAME}:{cls.PASSWORD}@{cls.HOST}:{cls.PORT}/{cls.DB}"

    @classmethod
    def get_sync_url(cls):
        return f"postgresql+psycopg2://{cls.USERNAME}:{cls.PASSWORD}@{cls.HOST}:{cls.PORT}/{cls.DB}"

    @classmethod
    def get_session(cls):
        return async_sessionmaker(
            bind=cls.ENGINE(), class_=AsyncSession, expire_on_commit=False
        )

    ENGINE = create_async_engine(
        get_async_url(),
        pool_pre_ping=True,
        pool_size=20,
        max_overflow=40,
        echo=True,
    )


class JWT:
    SECRET = os.getenv("JWT_SECRET")
    ALGORITHM = os.getenv("JWT_ALGORITHM")

    if not SECRET:
        raise Exception("JWT secret token doesn't set up")
    if not ALGORITHM:
        raise Exception("JWT algorithm doesn't set up")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
