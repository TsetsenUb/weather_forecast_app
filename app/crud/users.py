from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User
from app.schemas.users import UserIn
from app.core.security import hash_password


class UserCrud:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def create_user(self, user: UserIn) -> User:
        """
        Создает нового пользователя и хеширует его пароль для хранения в базе данных
        """

        new_user = User(
            name=user.name,
            email=user.email,
            address=user.address,
            hashed_password=hash_password(user.password)
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user

    async def get_user(self, user_id: int, active: bool = True) -> User | None:
        """
        Возвращает пользователя с указанным ID, если такого пользователя нет, вернется None
        """

        db_user = await self.db.get(User, user_id)
        if db_user and db_user.is_active == active:
            return db_user

    async def update_user(self, user_id: int, new_user_data: dict) -> User | None:
        """
        Обновляет данные пользователя с указанным ID и возвращает обновленные данные.
        Если пользователя с указанным ID не найден - возвращает None
        """
        updated_user = await self.db.get(User, user_id)
        if not updated_user:
            return

        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(**new_user_data)
        )
        await self.db.commit()
        await self.db.refresh(updated_user)
        return updated_user

    async def get_user_by_email(self, email: str) -> User | None:
        """
        Ищет пользователя по почте.
        Если находит пользователя возвращает его,
        иначе - None
        """

        db_user = await self.db.scalar(
            select(User)
            .where(User.email == email)
        )
        return db_user
