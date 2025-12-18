from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from pydantic import ValidationError
import jwt

from app.models.users import User
from app.schemas.tokens import TokenData
from app.core.config import settings
from app.services.users import UserService
from app.utils import app_exceptions


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/token")


def create_access_token(data: dict) -> str:
    """
    Создаёт JWT с payload (sub, name, id, address, exp).
    """

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY.get_secret_value(),
        algorithm=settings.ALGORITHM.get_secret_value(),
    )


async def get_authorized_user(
        token: str,
        user_service: UserService
) -> User:
    """
    Проверяет JWT и возвращает пользователя из базы.
    """

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY.get_secret_value(),
            algorithms=settings.ALGORITHM.get_secret_value(),
        )
        token_data = TokenData(**payload)
    except jwt.ExpiredSignatureError:
        raise app_exceptions.EXPIRED_401
    except (jwt.PyJWKError, ValidationError):
        raise app_exceptions.UNAUTHORIZED_401

    user = await user_service.get_user(token_data.id)
    return user
