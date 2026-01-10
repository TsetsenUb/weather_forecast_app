import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.users import UserCrud
from app.core.security import verify_password
from app.schemas.users import UserIn
from app.models.users import User


@pytest.mark.smoke
@pytest.mark.user_crud
class TestUserCrud:

    async def test_crud_create_user(
        self,
        db_session: AsyncSession,
        user_data: UserIn,
    ) -> None:
        """
        Тестирование UserCrud.create_user
        Создание нового пользователя в тестовой БД
        и проверка корректности данных нового пользователя
        """

        user_crud = UserCrud(db_session)
        result = await user_crud.create_user(user_data)

        assert result.id == 1
        assert result.name == user_data.name
        assert result.address == user_data.address
        assert result.email == user_data.email
        assert result.is_active is True
        assert verify_password(user_data.password, result.hashed_password)

    async def test_crud_get_active_user(
        self,
        db_session: AsyncSession,
        active_db_user: User,
    ) -> None:
        """
        Тестирование UserCrud.get_user
        Получения активного пользователя из тестовой БД
        и проверка корректности данных полученного пользователя
        """

        user_crud = UserCrud(db_session)
        result = await user_crud.get_user(1)

        assert result == active_db_user

    async def test_crud_get_not_active_user(
        self,
        db_session: AsyncSession,
        not_active_db_user: User,
    ) -> None:
        """
        Тестирование UserCrud.get_user
        Получения не активного пользователя из тестовой БД
        и проверка что вернулось None
        """

        assert not_active_db_user.is_active is False

        user_crud = UserCrud(db_session)
        result = await user_crud.get_user(1)

        assert result is None

    async def test_crud_update_user(
        self,
        db_session: AsyncSession,
        active_db_user: User,
        data_for_update: dict,
    ) -> None:
        """
        Тестирование UserCrud.update_user
        Обновление данных пользователя в тестовой БД
        и проверка корректности обновления
        """

        assert active_db_user.name != data_for_update["name"]
        assert active_db_user.address != data_for_update["address"]
        assert active_db_user.email != data_for_update["email"]
        assert active_db_user.hashed_password != data_for_update["hashed_password"]

        user_crud = UserCrud(db_session)
        result = await user_crud.update_user(1, data_for_update)

        assert result.name == data_for_update["name"]
        assert result.address == data_for_update["address"]
        assert result.email == data_for_update["email"]
        assert result.hashed_password == data_for_update["hashed_password"]

    async def test_crud_not_update_user(
        self,
        db_session: AsyncSession,
        data_for_update: dict,
    ) -> None:
        """
        Тестирование UserCrud.update_user
        Попытка обновления несуществующего пользователя в тестовой БД
        и проверка на то что вернулось None
        """

        user_crud = UserCrud(db_session)
        result = await user_crud.update_user(1, data_for_update)

        assert result is None

    async def test_crud_get_user_by_email(
        self,
        db_session: AsyncSession,
        active_db_user: User,
    ) -> None:
        """
        Тестирование UserCrud.get_user_by_email
        Получение пользователя по email из тестовой БД
        или None если пользователя с таким email нет
        """

        user_crud = UserCrud(db_session)
        result = await user_crud.get_user_by_email(active_db_user.email)

        assert active_db_user == result

        result = await user_crud.get_user_by_email("not_exist@examle.com")

        assert result is None
