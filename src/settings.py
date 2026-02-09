import os
from dotenv import load_dotenv

load_dotenv('docker/.env')


class PostgresSettings:
    POSTGRES_DB = os.getenv('POSTGRES_DB', )
    POSTGRES_USERNAME = os.getenv('POSTGRES_USERNAME')
    POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', '5432'))
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

    if not POSTGRES_PASSWORD:
        raise Exception('The password is required. Set it in ".env"')
