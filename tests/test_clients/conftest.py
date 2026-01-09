import pytest_asyncio
import httpx
from pytest_mock import MockerFixture


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
