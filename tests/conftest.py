import pytest_asyncio

from app.schemas.users import UserIn
from app.schemas.owm_schemas import OWMForecastResponse
from app.schemas.forecast_schemas import Forecast


@pytest_asyncio.fixture(scope="session")
def user_data() -> UserIn:
    """Фикстура с данными о новом пользователе"""

    return UserIn(
        name="User1",
        address="Moscow",
        email="user1@example.com",
        password="12345678",
    )


@pytest_asyncio.fixture(scope="session")
def new_user_data() -> UserIn:
    """Фикстура с данными для обновления пользователя"""

    return UserIn(
        name="User2",
        address="Saint Petersburg",
        email="user2@example.com",
        password="123456789",
    )


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
