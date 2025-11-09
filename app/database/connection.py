from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    pass


async_engine = create_async_engine(
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@postgres_db:5432/{settings.DB_NAME}"
)

async_session_maker = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)


async def create_db_and_tables() -> None:
    """
    Создает базу данных и таблицы
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
