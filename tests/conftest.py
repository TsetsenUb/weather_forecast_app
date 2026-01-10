import pytest_asyncio

from app.schemas.users import UserIn, UserUpdate
from app.schemas.owm_schemas import OWMForecastResponse
from app.schemas.forecast_schemas import Forecast
from app.models.users import User
from app.core.security import hash_password


@pytest_asyncio.fixture(scope="session")
def dict_user_data() -> dict:
    """
    Фикстура для получения словаря с данными пользователя
    """

    return {
        "name": "User1",
        "address": "Moscow",
        "email": "user1@example.com",
        "password": "12345678",
    }


@pytest_asyncio.fixture(scope="session")
def dict_new_user_data() -> dict:
    """
    Фикстура для получения словаря с новыми данными пользователя
    """

    return {
        "name": "User2",
        "address": "Saint Petersburg",
        "email": "user2@example.com",
        "password": "123456789",
    }


@pytest_asyncio.fixture(scope="session")
def user_data(dict_user_data: dict) -> UserIn:
    """
    Фикстура с данными о новом пользователе
    """

    return UserIn(**dict_user_data)


@pytest_asyncio.fixture(scope="session")
def new_user_data(dict_new_user_data: dict) -> UserIn:
    """
    Фикстура с данными для обновления пользователя
    """

    return UserIn(**dict_new_user_data)


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
async def updated_db_user(dict_new_user_data: dict) -> User:
    """Фикстура для получения обновленного БД пользователя"""

    return User(
        id=1,
        name=dict_new_user_data["name"],
        email=dict_new_user_data["email"],
        is_active=True,
        hashed_password=hash_password(dict_new_user_data["password"]),
        address=dict_new_user_data["address"],
    )


@pytest_asyncio.fixture(scope="session")
async def user_update(dict_new_user_data: dict) -> UserUpdate:
    """Фикстура для получения UserUpdate"""

    return UserUpdate(**dict_new_user_data)


@pytest_asyncio.fixture(scope="session")
async def open_weather_map_response_example() -> str:
    """
    Фикстура для считывания примера ответа open weather map из json файла
    """

    with open("tests/json/owm_response_example.json", "r", encoding="utf-8") as file:
        return file.read()


@pytest_asyncio.fixture(scope="session")
async def owm_forecast_response(
    open_weather_map_response_example: str,
) -> OWMForecastResponse:
    """
    Фикстура для получения объекта OWMForecastResponse
    """

    return OWMForecastResponse.model_validate_json(
        open_weather_map_response_example
    )


@pytest_asyncio.fixture(scope="session")
async def forecast_example() -> str:
    """
    Фикстура для считывания примера Forecast из json файла
    """

    with open("tests/json/forecast_example.json", "r", encoding="utf-8") as file:
        return file.read()


@pytest_asyncio.fixture(scope="session")
async def forecast(
    forecast_example: str,
) -> Forecast:
    """
    Фикстура для получения объекта Forecast
    """

    return Forecast.model_validate_json(forecast_example)
