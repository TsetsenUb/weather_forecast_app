import pytest
from fastapi import status
from unittest.mock import AsyncMock
import httpx
import jwt

from app.models.users import User
from app.core.config import settings


@pytest.mark.smoke
@pytest.mark.users
class TestUserRouter:

    @staticmethod
    def check_response(
        response: httpx.Response,
        db_user: User,
        status_code: status,
    ) -> None:
        """
        Проверка ответа эндпоинта на корректность
        """

        assert response.status_code == status_code
        assert response.headers["content-type"] == "application/json"

        res_data = response.json()
        assert res_data["id"] == db_user.id
        assert res_data["name"] == db_user.name
        assert res_data["address"] == db_user.address
        assert res_data["email"] == db_user.email
        assert res_data["is_active"] is True
        assert "hashed_password" not in res_data

    @staticmethod
    def check_token(
        response: httpx.Response,
        db_user: User,
        status_code: status,
    ) -> dict:
        """
        Проверка токена на корректность
        """

        assert response.status_code == status_code

        res_data = response.json()
        assert res_data["token_type"] == "bearer"

        payload = jwt.decode(
            res_data["access_token"],
            settings.SECRET_KEY.get_secret_value(),
            algorithms=settings.ALGORITHM.get_secret_value(),
        )

        assert db_user.id == payload["id"]
        assert db_user.email == payload["sub"]
        assert db_user.name == payload["name"]
        assert db_user.address == payload["address"]
        assert "hashed_password" not in payload
        assert "password" not in payload

        return payload

    async def test_get_user(
        self,
        test_client: httpx.AsyncClient,
        mock_user_service: AsyncMock,
        db_user: User,
    ) -> None:
        """
        Тестирование эндпоинта GET api/users/{user_id}
        """

        mock_user_service.get_user.return_value = db_user

        response = await test_client.get("api/users/1")

        self.check_response(
            response,
            db_user,
            status_code=status.HTTP_200_OK,
        )

    async def test_create_user(
        self,
        test_client: httpx.AsyncClient,
        mock_user_service: AsyncMock,
        dict_user_data: dict,
        db_user: User,
    ) -> None:
        """
        Тестирование эндпоинта POST api/users/
        """

        mock_user_service.create_user.return_value = db_user

        response = await test_client.post(
            "api/users/",
            json=dict_user_data,
        )

        self.check_response(
            response,
            db_user,
            status_code=status.HTTP_201_CREATED,
        )

    async def test_login(
        self,
        test_client: httpx.AsyncClient,
        mock_user_service: AsyncMock,
        dict_user_data: dict,
        db_user: User,
    ) -> None:
        """
        Тестирование эндпоинта POST api/users/token
        Проверка корректности вернувшегося токена
        """

        mock_user_service.login_user.return_value = db_user

        response = await test_client.post(
            "api/users/token",
            data={
                "username": dict_user_data["email"],
                "password": dict_user_data["password"]
            },
        )

        self.check_token(
            response=response,
            db_user=db_user,
            status_code=status.HTTP_201_CREATED,
        )

    async def test_update_user(
        self,
        test_client: httpx.AsyncClient,
        mock_user_service: AsyncMock,
        dict_new_user_data: dict,
        updated_db_user: User,
        mock_current_user: User,
    ) -> None:
        """
        Тестирование эндпоинта PATCH api/users/
        Проверка корректности вернувшегося токена
        Проверка на то что данные изменились
        """

        mock_user_service.update_user.return_value = updated_db_user

        response = await test_client.patch(
            "api/users/",
            json=dict_new_user_data,
        )

        payload = self.check_token(
            response=response,
            db_user=updated_db_user,
            status_code=status.HTTP_200_OK,
        )

        assert mock_current_user.id == payload["id"]
        assert mock_current_user.email != payload["sub"]
        assert mock_current_user.name != payload["name"]
        assert mock_current_user.address != payload["address"]
