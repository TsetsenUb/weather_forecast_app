from fastapi import HTTPException
import httpx

from app.schemas.owm_schemas import OWMForecastResponse


class OpenWeatherMapClient:
    def __init__(self, appid: str, base_url: str) -> None:
        self.base_url = base_url
        self.__appid = appid

    async def __call__(
            self,
            city: str,
            units: str = "metric",
            lang: str = "ru"
    ) -> OWMForecastResponse:
        """
        Отправляет get запрос на open weather map
        для получения прогноза погоды для указанного города.
        Валидирует полученный прогноз с помощью pydantic модели
        OWMForecastResponse и возвращает его
        """

        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.base_url,
                params={
                    "q": city,
                    "type": "like",
                    "units": units,
                    "lang": lang,
                    "APPID": self.__appid
                }
            )
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=response.json()["message"])

            return OWMForecastResponse.model_validate_json(response.text)
