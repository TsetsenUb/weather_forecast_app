import pytest_asyncio
from pytest_mock import MockerFixture
from unittest.mock import MagicMock

from app.crud.users import UserCrud


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
async def mock_owm_client(
    mocker: MockerFixture,
    owm_forecast_response,
) -> MagicMock:
    """Фикстура для мока OpenWeatherMapClient"""

    mocker.patch(
        "test_services_weather.OpenWeatherMapClient.__call__",
        return_value=owm_forecast_response,
    )
