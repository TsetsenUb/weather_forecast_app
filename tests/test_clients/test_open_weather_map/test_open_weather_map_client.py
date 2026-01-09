import pytest
from fastapi import HTTPException

from app.clients.open_weather_map.client import OpenWeatherMapClient
from app.schemas.owm_schemas import OWMForecastResponse


@pytest.mark.smoke
@pytest.mark.open_weather_map
async def test_open_weather_map_client_200(
    owm_forecast_response: OWMForecastResponse,
    mock_httpx_async_get_200,
) -> None:
    """
    Тестирование OpenWeatherMapClient.__call__
    Код ответа get-запроса 200
    Возвращается объект OWMForecastResponse
    """

    client = OpenWeatherMapClient("appid", "base_url")
    result = await client("Moscow")

    assert isinstance(result, OWMForecastResponse)
    assert result == owm_forecast_response


@pytest.mark.smoke
@pytest.mark.open_weather_map
async def test_open_weather_map_client_404(
    mock_httpx_async_get_404,
) -> None:
    """
    Тестирование OpenWeatherMapClient.__call__
    Код ответа get-запроса 404
    """

    client = OpenWeatherMapClient("appid", "base_url")
    with pytest.raises(HTTPException) as excinfo:
        await client("Moscow")

    exc_value = str(excinfo)
    assert "200" not in exc_value
    assert "404" in exc_value
    assert "Not found" in exc_value
