import os
from dotenv import load_dotenv

load_dotenv('docker/.env')


class PostgresSettings:
    HOST = os.getenv('POSTGRES_HOST')
    DB = os.getenv('POSTGRES_DB')
    USERNAME = os.getenv('POSTGRES_USERNAME')
    PORT = int(os.getenv('POSTGRES_PORT', '5432'))
    PASSWORD = os.getenv('POSTGRES_PASSWORD')

    if not PASSWORD:
        raise Exception('The password is required. Set it in ".env"')

    @classmethod
    def get_async_url(cls):
        return f"postgresql+asyncpg://{cls.USERNAME}:{cls.PASSWORD}@{cls.HOST}:{cls.PORT}/{cls.DB}"

    @classmethod
    def get_sync_url(cls):
        return f"postgresql+psycopg2://{cls.USERNAME}:{cls.PASSWORD}@{cls.HOST}:{cls.PORT}/{cls.DB}"


