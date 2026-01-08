import pytest_asyncio

from app.schemas.users import UserIn


@pytest_asyncio.fixture(scope="session")
def user_data() -> UserIn:
    """Фикстура с данными о новом пользователе"""

    return UserIn(
        name="User1",
        address="Moscow",
        email="user1@example.com",
        password="12345678",
    )
