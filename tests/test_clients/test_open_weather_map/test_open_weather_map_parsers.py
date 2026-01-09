import pytest

from app.clients.open_weather_map.parsers import OpenWeatherMapForecastParser
from app.schemas.owm_schemas import OWMForecastResponse
from app.schemas.forecast_schemas import Forecast, ForecastObj


@pytest.mark.smoke
@pytest.mark.open_weather_map
async def test_owm_forecast_parser(
    owm_forecast_response: OWMForecastResponse,
) -> None:
    """
    Тестирование OpenWeatherMapForecastParser.__call__
    Преобразование объекта OWMForecastResponse в объект Forecast
    Проверка возвращаемых данных на соответствие типов данных
    """

    parser = OpenWeatherMapForecastParser()
    result = parser(owm_forecast_response)

    assert isinstance(result, Forecast)
    assert result.name == owm_forecast_response.city.name
    assert isinstance(result.forecasts[0][0], ForecastObj)
