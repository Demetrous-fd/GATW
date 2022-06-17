from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import MetaData, create_engine

from backend.config import settings

metadata = MetaData()

engine = create_engine(settings.POSTGRES_URL)
async_engine = create_async_engine(
    f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DATABASE}"
)

SessionLocal = sessionmaker(engine)
AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


def get_session() -> Session:
    with SessionLocal.begin() as session:
        yield session


async def get_async_session() -> AsyncSession:
    async with AsyncSessionLocal.begin() as session:
        yield session
