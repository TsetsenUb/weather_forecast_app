from app.utils import converters as conv
from app.schemas.owm_schemas import OWMForecastResponse, ForecastItem
from app.schemas.forecast_schemas import ForecastObj, Forecast


class OpenWeatherMapForecastParser:

    def __call__(self, owm_response: OWMForecastResponse) -> Forecast:
        """
        Парсит данные OWMForecastResponse и возвращает Forecast
        """

        forecasts = self.__parse_forecasts(owm_response.list)

        return Forecast(
            name=owm_response.city.name,
            country=owm_response.city.country,
            lat=owm_response.city.coord.lat,
            lon=owm_response.city.coord.lon,
            timezone_sec=owm_response.city.timezone,
            forecasts=forecasts
        )

    def __parse_forecasts(self, forecast_list: list[ForecastItem]) -> list[list[ForecastObj]]:
        """
        Парсит данные из OWMForecastResponse.list
        и возвращает список со списками содержащими ForecastObj
        """
        res = []
        tmp = []
        prev_date = None

        for item in forecast_list:
            dt_date, dt_time = conv.convert_datetime(item.dt)

            obj = ForecastObj(
                dt_date=dt_date,
                dt_time=dt_time,
                temperature=round(item.main.temp),
                pressure=conv.hPa_to_mmHg(item.main.pressure),
                humidity=item.main.humidity,
                weather_description=item.weather[0].description.capitalize(),
                weather_icon=item.weather[0].icon,
                wind_speed=item.wind.speed,
                wind_direction=conv.degrees_to_direction(item.wind.deg)
            )

            if prev_date is None or prev_date == dt_date:
                tmp.append(obj)
            else:
                res.append(tmp)
                tmp = [obj]
            prev_date = dt_date
        else:
            if len(tmp) > 0:
                res.append(tmp)

        return res
