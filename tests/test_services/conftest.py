import pytest_asyncio
from pytest_mock import MockerFixture
from unittest.mock import MagicMock

from app.crud.users import UserCrud
from app.schemas.users import UserIn, UserUpdate
from app.models.users import User
from app.core.security import hash_password


@pytest_asyncio.fixture
async def mock_user_crud(mocker: MockerFixture) -> MagicMock:
    """Фикстура для мока UserCrud"""

    user_crud_mock = mocker.MagicMock(spec=UserCrud)

    user_crud_mock.create_user = mocker.AsyncMock()
    user_crud_mock.get_user = mocker.AsyncMock()
    user_crud_mock.update_user = mocker.AsyncMock()
    user_crud_mock.get_user_by_email = mocker.AsyncMock()

    return user_crud_mock


@pytest_asyncio.fixture
async def db_user(user_data: UserIn) -> User:
    """Фикстура для получения БД пользователя"""

    return User(
        id=1,
        name=user_data.name,
        email=user_data.email,
        is_active=True,
        hashed_password=hash_password(user_data.password),
        address=user_data.address,
    )


@pytest_asyncio.fixture
async def user_update(new_user_data: UserIn) -> UserUpdate:
    """Фикстура для получения UserUpdate"""

    return UserUpdate(**new_user_data.model_dump())


@pytest_asyncio.fixture
async def updated_db_user(new_user_data: UserIn) -> User:
    """Фикстура для получения обновленного БД пользователя"""

    return User(
        id=1,
        name=new_user_data.name,
        email=new_user_data.email,
        is_active=True,
        hashed_password=hash_password(new_user_data.password),
        address=new_user_data.address,
    )
