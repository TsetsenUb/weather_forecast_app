from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, Depends
from redis.asyncio import Redis
from typing import AsyncGenerator, Annotated

from app.database.connection import async_session_maker
from app.crud.users import UserCrud


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Предоставляет асинхронную сессию SQLAlchemy для работы с базой данных PostgreSQL.
    """
    async with async_session_maker() as async_session:
        yield async_session


async def get_user_crud(
        db_session: Annotated[AsyncSession, Depends(get_async_db)]
) -> UserCrud:
    """
    Возвращает объект класса UserCrud для работы с базой данных
    """
    return UserCrud(db_session)


async def get_redis(request: Request) -> Redis:
    """
    Возвращает Redis из app.state
    """
    return request.app.state.redis
