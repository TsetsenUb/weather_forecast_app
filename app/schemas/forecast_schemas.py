from pydantic import BaseModel


class ForecastObj(BaseModel):
    """
    Схема с прогнозом за определенный период (обычно 3-х часовой)
    """
    dt_date: str
    dt_time: str
    temperature: int
    pressure: int
    humidity: int
    weather_description: str
    weather_icon: str
    wind_speed: float
    wind_direction: str


class Forecast(BaseModel):
    """
    Схема прогноза погоды
    """
    name: str
    country: str
    lat: float
    lon: float
    timezone_sec: int
    forecasts: list[list[ForecastObj]]
