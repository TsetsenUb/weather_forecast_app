import pytest_asyncio
import logging
from pytest_mock import MockerFixture
from unittest.mock import AsyncMock
from httpx import AsyncClient, ASGITransport
from redis.asyncio import Redis
from typing import AsyncGenerator

from app.main import app
from app.services.weather import WeatherService
from app.database.dependencies import get_redis
from app.api.dependencies import get_weather_service


@pytest_asyncio.fixture(autouse=True)
async def disable_logging() -> AsyncGenerator[None, None]:
    """
    Отключает логирование для всех тестов
    """

    try:
        logging.disable(logging.CRITICAL)
        yield
    finally:
        logging.disable(logging.NOTSET)


@pytest_asyncio.fixture()
async def mock_redis(
    mocker: MockerFixture,
) -> AsyncGenerator[AsyncMock, None]:
    """
    Переопределяет get_redis зависимость и возвращает mock_redis
    """

    try:
        mock = mocker.AsyncMock(spec=Redis)
        mock.get = AsyncMock()
        mock.setex = AsyncMock()
        app.dependency_overrides[get_redis] = lambda: mock

        yield mock
    finally:
        app.dependency_overrides.pop(get_redis, None)


@pytest_asyncio.fixture()
async def mock_weather_service(
    mocker: MockerFixture,
) -> AsyncGenerator[AsyncMock, None]:
    """
    Переопределяет get_weather_service зависимость и возвращает mock_weather_service
    """

    try:
        mock = mocker.AsyncMock(spec=WeatherService)
        mock.get_forecast = mocker.AsyncMock()
        app.dependency_overrides[get_weather_service] = lambda: mock

        yield mock
    finally:
        app.dependency_overrides.pop(get_weather_service, None)


@pytest_asyncio.fixture
async def test_client() -> AsyncGenerator[AsyncClient, None]:
    """
    Асинхронный тестовый клиент
    """

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
