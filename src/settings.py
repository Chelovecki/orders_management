import os

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

load_dotenv("docker/.env")


class PostgresSettings:
    HOST = os.getenv("POSTGRES_HOST")
    DB = os.getenv("POSTGRES_DB")
    USERNAME = os.getenv("POSTGRES_USERNAME")
    PORT = int(os.getenv("POSTGRES_PORT", "5432"))
    PASSWORD = os.getenv("POSTGRES_PASSWORD")
    async_url = f"postgresql+asyncpg://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}"
    sync_url = f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}"

    ENGINE = create_async_engine(
        async_url,
        pool_pre_ping=True,
        pool_size=20,
        max_overflow=40,
        # echo=True,
    )

    if not PASSWORD:
        raise Exception('The password is required. Set it in ".env"')

    @classmethod
    def get_session(cls):
        return async_sessionmaker(
            bind=cls.ENGINE, class_=AsyncSession, expire_on_commit=False
        )


class JWT:
    SECRET = os.getenv("JWT_SECRET")
    ALGORITHM = os.getenv("JWT_ALGORITHM")

    if not SECRET:
        raise Exception("JWT secret token doesn't set up")
    if not ALGORITHM:
        raise Exception("JWT algorithm doesn't set up")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


class RedisSettings:
    HOST = os.getenv("REDIS_HOST", "localhost")
    PORT = int(os.getenv("REDIS_PORT", "6379"))
    DB_CACHE_ORDERS = int(os.getenv("REDIS_DB_CACHE_ORDERS", "0"))
    DB_CELERY = int(os.getenv("REDIS_DB_CELERY", "1"))


# src/settings.py
class RabbitSettings:
    HOST = os.getenv("RABBITMQ_HOST", "localhost")
    PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
    USER = os.getenv("RABBITMQ_USER", "guest")
    PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")

    URL = f"amqp://{USER}:{PASSWORD}@{HOST}:{PORT}/"
