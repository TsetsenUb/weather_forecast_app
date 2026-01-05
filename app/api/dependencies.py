from fastapi import Depends, Query
from typing import Annotated

from app.clients.open_weather_map.client import OpenWeatherMapClient
from app.clients.open_weather_map.parsers import OpenWeatherMapForecastParser
from app.services.weather import WeatherService
from app.core.config import settings
from app.crud.users import UserCrud
from app.models.users import User
from app.services.users import UserService
from app.database.dependencies import get_user_crud
from app.core.auth import oauth2_scheme, get_authorized_user


def get_owp_client() -> OpenWeatherMapClient:
    """
    Возвращает объект класса OpenWeatherMapClient
    """
    return OpenWeatherMapClient(
        settings.OWM_APPID.get_secret_value(),
        settings.OWM_FORECAST_URL,
    )


def get_owp_parser() -> OpenWeatherMapForecastParser:
    """
    Возвращает объект класса OpenWeatherMapForecastParser
    """
    return OpenWeatherMapForecastParser()


def get_weather_service(
        owp_client: Annotated[OpenWeatherMapClient, Depends(get_owp_client)],
        owp_parser: Annotated[OpenWeatherMapForecastParser, Depends(get_owp_parser)]
) -> WeatherService:
    """
    Возвращает объект класса WeatherService
    """
    return WeatherService(owp_client, owp_parser)


def get_user_service(
        user_crud: Annotated[UserCrud, Depends(get_user_crud)]
) -> UserService:
    """
    Возвращает объект класса UserService
    """
    return UserService(user_crud)


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        user_crud: Annotated[UserService, Depends(get_user_service)]
) -> User:
    """
    Возвращает текущего авторизированного пользователя
    """
    current_user = await get_authorized_user(token, user_crud)
    return current_user


async def get_query_city(
        city: Annotated[str, Query(..., min_length=3, max_length=50)]
) -> str:
    """
    Возвращает Query-параметр city, после применения методов strip и title
    """
    return city.strip().title()
