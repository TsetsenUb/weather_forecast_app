from fastapi import APIRouter, Depends, status
from redis.asyncio import Redis

from typing import Annotated

from app.schemas.forecast_schemas import Forecast
from app.services.weather import WeatherService
from app.api.dependencies import get_weather_service, get_query_city
from app.database.dependencies import get_redis
from app.core.config import settings


router = APIRouter(prefix="/forecast", tags=["Forecast"])


@router.get("/", response_model=Forecast, status_code=status.HTTP_200_OK)
async def get_city_weather(
    city: Annotated[str, Depends(get_query_city)],
    redis: Annotated[Redis, Depends(get_redis)],
    weather_service: Annotated[WeatherService, Depends(get_weather_service)]
):
    """
    Возвращает прогноз погоды на 5 дней для указанного города.
    Проверяет наличие прогноза для заданного города в redis,
    Если есть - возвращает его, если нет - то запрашивает прогноз с внешнего api,
    сохраняет в redis и возвращает полученный прогноз.
    """

    redis_key = f"forecast:{city}"

    redis_city_forecast = await redis.get(redis_key)

    if redis_city_forecast:
        res = Forecast.model_validate_json(redis_city_forecast)
    else:
        res = await weather_service.get_forecast(city)
        await redis.setex(
            redis_key,
            settings.REDIS_FORECAST_EXPIRE_SEC,
            res.model_dump_json(),
        )

    return res
