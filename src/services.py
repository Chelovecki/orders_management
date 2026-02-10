from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


class BaseService:
    def __init__(self, session):
        self.session_factory: async_sessionmaker[AsyncSession] = session
