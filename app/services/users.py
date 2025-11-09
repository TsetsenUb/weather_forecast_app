from app.crud.users import UserCrud
from app.schemas.users import UserIn
from app.models.users import User
from app.core.security import verify_password, hash_password
from app.utils import app_exc


class UserService:
    def __init__(self, user_crud: UserCrud) -> None:
        self.user_crud = user_crud

    async def login_user(self, email: str, password: str) -> User:
        """
        Находит пользователя по почте и проводит верификацию пароля
        Если проверка успешна возвращает пользователя
        иначе - ошибка 401
        """

        db_user = await self.user_crud.get_user_by_email(email)

        if not db_user or db_user.is_active is False or \
           not verify_password(password, db_user.hashed_password):
            raise app_exc.UNAUTHORIZED_401

        return db_user

    async def create_user(self, user: UserIn) -> User:
        """
        Проверяет почту, если она уже используется выбрасывает исключение, иначе
        создает нового пользователя и возвращает данные о созданном пользователе
        """

        if await self.user_crud.get_user_by_email(user.email):
            raise app_exc.BAD_REQUEST_EMAIL_400

        new_user = await self.user_crud.create_user(user)
        return new_user

    async def get_user(self, user_id: int, active: bool = True) -> User:
        """
        Возвращает пользователя с указанным ID
        """

        db_user = await self.user_crud.get_user(user_id, active)
        if not db_user:
            raise app_exc.BAD_REQUEST_USER_400
        return db_user

    async def update_user(self, user_id: int, user_data: UserIn) -> User:
        """
        Обновляет данные пользователя с указанным ID
        """
        new_user_data = user_data.model_dump(exclude_unset=True)

        new_email = new_user_data.pop("email", None)
        if new_email:
            if await self.user_crud.get_user_by_email(new_email):
                raise app_exc.BAD_REQUEST_EMAIL_400
            new_user_data.update({"email": new_email})

        new_password = new_user_data.pop("password", None)
        if new_password:
            new_user_data.update({"hashed_password": hash_password(new_password)})

        if not new_user_data:
            raise app_exc.BAD_REQUEST_NOT_DATA_400

        updated_user = await self.user_crud.update_user(user_id, new_user_data)
        if not updated_user:
            raise app_exc.BAD_REQUEST_USER_400

        return updated_user
