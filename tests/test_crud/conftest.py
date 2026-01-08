import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

from app.database.connection import Base
from app.schemas.users import UserIn
from app.models.users import User
from app.core.security import hash_password
from app.core.config import settings


@pytest_asyncio.fixture()
async def test_async_engine() -> AsyncGenerator[AsyncEngine, None]:
    """Фикстура для создания асинхронного движка базы данных."""

    engine = create_async_engine(
        settings.TEST_DATABASE_URL,
        echo=False,
        future=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    try:
        yield engine
    finally:
        await engine.dispose()


@pytest_asyncio.fixture()
async def async_sessionmaker(
    test_async_engine: AsyncEngine,
) -> sessionmaker[AsyncSession]:
    """Фикстура для создания фабрики асинхронных сессий."""

    return sessionmaker(
        test_async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


@pytest_asyncio.fixture()
async def db_session(
    async_sessionmaker: sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    """Фикстура для создания асинхронной сессии базы данных."""

    async with async_sessionmaker() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest_asyncio.fixture(scope="class")
def new_user_data() -> dict:
    return {
        "name": "User2",
        "address": "Saint Petersburg",
        "email": "user2@example.com",
        "hashed_password": hash_password("123456789"),
    }


@pytest_asyncio.fixture
async def active_db_user(
    db_session: AsyncSession,
    user_data: UserIn
) -> User:
    """Фикстура для создания тестового пользователя в БД"""

    test_user = User(
        name=user_data.name,
        address=user_data.address,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )

    db_session.add(test_user)
    await db_session.flush()
    await db_session.refresh(test_user)

    return test_user


@pytest_asyncio.fixture
async def not_active_db_user(
    db_session: AsyncSession,
    user_data: UserIn
) -> User:
    """Фикстура для создания тестового пользователя в БД"""

    test_user = User(
        name=user_data.name,
        address=user_data.address,
        email=user_data.email,
        is_active=False,
        hashed_password=hash_password(user_data.password),
    )

    db_session.add(test_user)
    await db_session.flush()
    await db_session.refresh(test_user)

    return test_user
