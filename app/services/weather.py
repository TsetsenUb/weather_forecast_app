from app.clients.open_weather_map.client import OpenWeatherMapClient
from app.clients.open_weather_map.parsers import OpenWeatherMapForecastParser
from app.schemas.forecast_schemas import Forecast


class WeatherService:
    def __init__(
            self,
            client: OpenWeatherMapClient,
            parser: OpenWeatherMapForecastParser
    ) -> None:
        self.client = client
        self.parser = parser

    async def get_forecast(self, city: str) -> Forecast:
        """
        Запрашивает прогноз погоды для указанного города с внешнего API (Open weather map)
        И возвращает полученные данные в нужном формате (Forecast)
        """
        response = await self.client(city)
        return self.parser(response)
