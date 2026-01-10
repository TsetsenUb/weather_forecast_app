import pytest

from app.services.weather import WeatherService
from app.clients.open_weather_map.client import OpenWeatherMapClient
from app.clients.open_weather_map.parsers import OpenWeatherMapForecastParser
from app.schemas.forecast_schemas import Forecast, ForecastObj
from app.schemas.owm_schemas import OWMForecastResponse


@pytest.mark.smoke
@pytest.mark.weather_service
class TestWeatherService:

    async def test_service_get_forecast(
        self,
        mock_owm_client,
        owm_forecast_response: OWMForecastResponse,
    ) -> None:
        """
        Тестирование WeatherService
        Получение прогноза погоды с помощью мок клиента и парсинг полученных данных
        Проверка полученных данных на соответствие типов данных
        """

        service = WeatherService(
            OpenWeatherMapClient("appid", "base_url"),
            OpenWeatherMapForecastParser(),
        )
        result = await service.get_forecast("Moscow")

        assert isinstance(result, Forecast)
        assert isinstance(result.forecasts[0][0], ForecastObj)
        assert result.name == owm_forecast_response.city.name
