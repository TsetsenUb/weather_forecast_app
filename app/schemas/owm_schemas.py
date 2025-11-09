from pydantic import BaseModel, Field
from typing import List, Optional


class Coord(BaseModel):
    """
    Схема для обработки ключа "coord" json-ответа Open weather map
    """
    lat: float
    lon: float


class City(BaseModel):
    """
    Схема для обработки ключа "city" json-ответа Open weather map
    """
    id: int
    name: str
    coord: Coord
    country: str
    population: int
    timezone: int
    sunrise: Optional[int] = None
    sunset: Optional[int] = None


class WeatherItem(BaseModel):
    """
    Схема для обработки элемента списка ключа "weather" json-ответа Open weather map
    """
    id: int
    main: str
    description: str
    icon: str


class Main(BaseModel):
    """
    Схема для обработки ключа "main" json-ответа Open weather map
    """
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    sea_level: Optional[int] = None
    grnd_level: Optional[int] = None
    humidity: int
    temp_kf: Optional[float] = None


class Clouds(BaseModel):
    """
    Схема для обработки ключа "clouds" json-ответа Open weather map
    """
    all: int


class Wind(BaseModel):
    """
    Схема для обработки ключа "wind" json-ответа Open weather map
    """
    speed: float
    deg: int
    gust: Optional[float] = None


class Rain(BaseModel):
    """
    Схема для обработки ключа "rain" json-ответа Open weather map
    """
    one_hour: Optional[float] = Field(None, alias='1h')
    three_hours: Optional[float] = Field(None, alias='3h')


class Snow(BaseModel):
    """
    Схема для обработки ключа "snow" json-ответа Open weather map
    """
    one_hour: Optional[float] = Field(None, alias='1h')
    three_hours: Optional[float] = Field(None, alias='3h')


class Sys(BaseModel):
    """
    Схема для обработки ключа "sys" json-ответа Open weather map
    """
    pod: str


class ForecastItem(BaseModel):
    """
    Схема для обработки элемента списка ключа "list" json-ответа Open weather map
    """
    dt: int
    main: Main
    weather: List[WeatherItem]
    clouds: Clouds
    wind: Wind
    visibility: Optional[int] = None
    pop: float
    rain: Optional[Rain] = None
    snow: Optional[Snow] = None
    sys: Sys
    dt_txt: str


class OWMForecastResponse(BaseModel):
    """
    Схема для обработки json-ответа Open weather map
    """
    cod: str
    message: int
    cnt: int
    list: List[ForecastItem]
    city: City
