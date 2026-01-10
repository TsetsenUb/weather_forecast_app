import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException

from app.models.users import User
from app.schemas.users import UserIn, UserUpdate
from app.services.users import UserService
from app.utils.app_exceptions import (
    Unauthorized401,
    BadRequestEmail400,
    BadRequestUser400,
    BadRequestNotData400,
)


@pytest.mark.smoke
@pytest.mark.user_service
class TestUserService:

    @staticmethod
    def check_exception(
        excinfo: pytest.ExceptionInfo,
        exc: HTTPException,
    ) -> None:
        """
        Проверяет чтобы код ошибки и сообщение ExceptionInfo
        соответствовали указанному исключению
        """

        exc_value = str(excinfo.value)
        exception = exc()
        assert exception.detail in exc_value
        assert str(exception.status_code) in exc_value

    async def test_service_login_user(
        self,
        mock_user_crud: MagicMock,
        db_user: User,
        user_data: UserIn,
    ) -> None:
        """
        Тестирование UserService.login_user
        Проверка с успешной верификацией
        """

        mock_user_crud.get_user_by_email.return_value = db_user

        user_service = UserService(mock_user_crud)
        result = await user_service.login_user(user_data.email, user_data.password)

        assert result == db_user

    async def test_service_login_user_unauthorized_missing_user(
        self,
        mock_user_crud: MagicMock,
        user_data: UserIn,
    ) -> None:
        """
        Тестирование UserService.login_user
        Проверка не успешной верификации (ошибка Unauthorized401):
            - get_user_by_email возвращает None
        """

        mock_user_crud.get_user_by_email.return_value = None
        user_service = UserService(mock_user_crud)
        with pytest.raises(Unauthorized401) as excinfo:
            await user_service.login_user(user_data.email, user_data.password)

        self.check_exception(
            excinfo,
            Unauthorized401,
        )

    async def test_service_login_user_unauthorized_wrong_password(
        self,
        mock_user_crud: MagicMock,
        db_user: User,
        user_data: UserIn,
    ) -> None:
        """
        Тестирование UserService.login_user
        Проверка не успешной верификации (ошибка Unauthorized401):
            - передан неверный пароль
        """

        mock_user_crud.get_user_by_email.return_value = db_user
        user_service = UserService(mock_user_crud)
        with pytest.raises(Unauthorized401) as excinfo:
            await user_service.login_user(user_data.email, user_data.password+"1")

        self.check_exception(
            excinfo,
            Unauthorized401,
        )

    async def test_service_login_user_unauthorized_not_active_user(
        self,
        mock_user_crud: MagicMock,
        db_user: User,
        user_data: UserIn,
    ) -> None:
        """
        Тестирование UserService.login_user
        Проверка не успешной верификации (ошибка Unauthorized401):
            - get_user_by_email возвращает неактивного пользователя
        """

        db_user.is_active = False
        mock_user_crud.get_user_by_email.return_value = db_user
        user_service = UserService(mock_user_crud)
        with pytest.raises(Unauthorized401) as excinfo:
            await user_service.login_user(user_data.email, user_data.password)

        self.check_exception(
            excinfo,
            Unauthorized401,
        )

    async def test_service_create_user_successful(
        self,
        mock_user_crud: MagicMock,
        db_user: User,
        user_data: UserIn,
    ) -> None:
        """
        Тестирование UserService.create_user
        Успешное создание нового пользователя
        """

        mock_user_crud.get_user_by_email.return_value = None
        mock_user_crud.create_user.return_value = db_user

        user_service = UserService(mock_user_crud)
        result = await user_service.create_user(user_data)

        assert result == db_user

    async def test_service_create_user_badrequest(
        self,
        mock_user_crud: MagicMock,
        db_user: User,
        user_data: UserIn,
    ) -> None:
        """
        Тестирование UserService.create_user
        Email уже используется - исключение BadRequestEmail400
        """

        mock_user_crud.get_user_by_email.return_value = db_user

        user_service = UserService(mock_user_crud)
        with pytest.raises(BadRequestEmail400) as excinfo:
            await user_service.create_user(user_data)

        self.check_exception(
            excinfo,
            BadRequestEmail400,
        )

    async def test_service_get_user_active(
        self,
        mock_user_crud: MagicMock,
        db_user: User,
    ) -> None:
        """
        Тестирование UserService.get_user
        Если существует активный пользователь с указанным id
        """

        mock_user_crud.get_user.return_value = db_user
        user_service = UserService(mock_user_crud)
        result = await user_service.get_user(1)

        assert result is not None
        assert result.id == 1
        assert result.is_active is True

    async def test_service_get_user_not_active(
        self,
        mock_user_crud: MagicMock,
        db_user: User,
    ) -> None:
        """
        Тестирование UserService.get_user
        Если существует не активный пользователь с указанным id
        """

        db_user.is_active = False
        mock_user_crud.get_user.return_value = db_user
        user_service = UserService(mock_user_crud)
        result = await user_service.get_user(1, False)

        assert result is not None
        assert result.id == 1
        assert result.is_active is False

    async def test_service_get_user_badrequest(
        self,
        mock_user_crud: MagicMock,
    ) -> None:
        """
        Тестирование UserService.get_user
        Если активный пользователь с указанным id не существует
        """

        mock_user_crud.get_user.return_value = None
        user_service = UserService(mock_user_crud)
        with pytest.raises(BadRequestUser400) as excinfo:
            await user_service.get_user(1)

        self.check_exception(
            excinfo,
            BadRequestUser400,
        )

    async def test_service_update_user_all_data(
        self,
        mock_user_crud: MagicMock,
        db_user: User,
        updated_db_user: User,
        user_update: UserUpdate,
    ) -> None:
        """
        Тестирование UserService.update_user
        Обновление корректных данных (name, address, email, password)
        """

        mock_user_crud.get_user_by_email.return_value = None
        mock_user_crud.update_user.return_value = updated_db_user

        user_service = UserService(mock_user_crud)
        result = await user_service.update_user(db_user.id, user_update)

        assert result == updated_db_user

    async def test_service_update_user_badrequest_email(
        self,
        mock_user_crud: MagicMock,
        db_user: User,
        updated_db_user: User,
        user_update: UserUpdate,
    ) -> None:
        """
        Тестирование UserService.update_user
        Попытка обновления с уже используемым паролем
        (исключение BadRequestEmail400)
        """

        mock_user_crud.get_user_by_email.return_value = db_user
        updated_db_user.email = db_user.email

        user_service = UserService(mock_user_crud)
        with pytest.raises(BadRequestEmail400) as excinfo:
            await user_service.update_user(db_user.id, user_update)

        self.check_exception(
            excinfo,
            BadRequestEmail400,
        )

    async def test_service_update_user_badrequest_not_data(
        self,
        mock_user_crud: MagicMock,
    ) -> None:
        """
        Тестирование UserService.update_user
        Попытка обновления без новых данных
        (исключение BadRequestNotData400)
        """

        mock_user_crud.get_user_by_email.return_value = None

        user_service = UserService(mock_user_crud)
        with pytest.raises(BadRequestNotData400) as excinfo:
            await user_service.update_user(1, UserUpdate())

        self.check_exception(
            excinfo,
            BadRequestNotData400,
        )

    async def test_service_update_user_badrequest_user(
        self,
        mock_user_crud: MagicMock,
        user_update: UserUpdate,
    ) -> None:
        """
        Тестирование UserService.update_user
        Попытка обновления не существующего пользователя
        (исключение BadRequestUser400)
        """

        mock_user_crud.get_user_by_email.return_value = None
        mock_user_crud.update_user.return_value = None

        user_service = UserService(mock_user_crud)
        with pytest.raises(BadRequestUser400) as excinfo:
            await user_service.update_user(1, user_update)

        self.check_exception(
            excinfo,
            BadRequestUser400,
        )
