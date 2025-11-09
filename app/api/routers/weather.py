from fastapi import APIRouter, Query, Depends, status

from typing import Annotated

from app.schemas.forecast_schemas import Forecast
from app.services.weather import WeatherService
from app.api.dependencies import get_weather_service


router = APIRouter(prefix="/api/forecast", tags=["Weather"])


@router.get("/", response_model=Forecast, status_code=status.HTTP_200_OK)
async def get_city_weather(
    city: Annotated[str, Query(..., min_length=3, max_length=50)],
    weather_service: Annotated[WeatherService, Depends(get_weather_service)]
):
    """
    Возвращает прогноз погоды на 5 дней для указанного города
    """
    res = await weather_service.get_forecast(city)

    return res
