from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.engine import URL
from redis.asyncio import Redis

from app.core.config import settings


class Base(DeclarativeBase):
    pass


async_engine = create_async_engine(
    URL.create(
        drivername="postgresql+asyncpg",
        username=settings.DB_USER.get_secret_value(),
        password=settings.DB_PASSWORD.get_secret_value(),
        host="postgres_db",
        port=5432,
        database=settings.DB_NAME.get_secret_value(),
    )
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


async def connect_to_redis(db: int = 0) -> Redis:
    """
    Подключение к redis
    """
    redis = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=db,
    )

    return redis
