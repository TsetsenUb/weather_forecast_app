import pytest
from unittest.mock import AsyncMock
from httpx import AsyncClient

from app.schemas.forecast_schemas import Forecast


@pytest.mark.smoke
@pytest.mark.forecast
class TestForecastRouter:

    async def test_get_city_weather_cache_hit(
        self,
        test_client: AsyncClient,
        mock_redis: AsyncMock,
        mock_weather_service: AsyncMock,
        forecast_example: str,
        forecast: Forecast,
    ):
        """
        Тестирование эндпоинта GET /api/forecast
        Тест когда в кэше есть данных
        """

        mock_redis.get.return_value = forecast_example

        result = await test_client.get("api/forecast/", params={"city": "москва"})

        assert result.status_code == 200
        assert result.headers["content-type"] == "application/json"
        assert forecast.model_dump() == result.json()

    async def test_get_city_weather_cache_miss(
        self,
        test_client: AsyncClient,
        mock_redis: AsyncMock,
        mock_weather_service: AsyncMock,
        forecast: Forecast,
    ):
        """
        Тестирование эндпоинта GET /api/forecast
        Тест когда в кэше нет данных
        """

        mock_redis.get.return_value = None
        mock_weather_service.get_forecast.return_value = forecast

        result = await test_client.get("api/forecast/", params={"city": "москва"})

        assert result.status_code == 200
        assert result.headers["content-type"] == "application/json"
        assert forecast.model_dump() == result.json()
