from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings

engine = create_async_engine(settings.POSTGRES_URL, future=True)


async def get_session() -> AsyncSession:
    """
    The get_session function is a factory function that creates an instance
    of the AsyncSession class. The AsyncSession class inherits from the Session
    class and adds functionality to it. This allows us to use async with
    statements in order to create asynchronous sessions, which are used by our
    database models.
    """
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session
