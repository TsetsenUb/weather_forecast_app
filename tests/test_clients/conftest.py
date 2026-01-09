import pytest_asyncio
import httpx
from pytest_mock import MockerFixture

from app.schemas.owm_schemas import OWMForecastResponse


@pytest_asyncio.fixture(scope="session")
async def open_weather_map_response_example() -> str:
    """
    Фикстура для считывания примера ответа open weather map из json файла
    """

    path = "tests/test_clients/test_open_weather_map/json/owm_response_example.json"

    with open(path, "r", encoding="utf-8") as file:
        response = file.read()

    return response


@pytest_asyncio.fixture(scope="session")
async def owm_forecast_response(
    open_weather_map_response_example: str,
) -> OWMForecastResponse:
    """
    Фикстура для получения объекта OWMForecastResponse из строки
    """

    return OWMForecastResponse.model_validate_json(
        open_weather_map_response_example
    )


@pytest_asyncio.fixture
async def mock_httpx_async_get_200(
    open_weather_map_response_example: str,
    mocker: MockerFixture,
) -> None:
    """
    Фикстура для мока httpx.AsyncClient (status_code=200)
    """

    mock_response = mocker.AsyncMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.text = open_weather_map_response_example

    mocker.patch.object(
        httpx.AsyncClient,
        "get",
        return_value=mock_response,
    )


@pytest_asyncio.fixture
async def mock_httpx_async_get_404(
    mocker: MockerFixture,
) -> None:
    """
    Фикстура для мока httpx.AsyncClient (status_code=404)
    """

    mock_response = mocker.AsyncMock(spec=httpx.Response)
    mock_response.status_code = 404
    mock_response.json.return_value = {"message": "Not found"}

    mocker.patch.object(
        httpx.AsyncClient,
        "get",
        return_value=mock_response,
    )
