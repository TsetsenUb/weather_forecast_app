from fastapi import APIRouter, Path, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from app.models.users import User
from app.schemas.users import UserIn, UserOut, UserUpdate
from app.schemas.tokens import Token
from app.services.users import UserService
from app.api.dependencies import get_user_service, get_current_user
from app.core.auth import create_access_token


router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/{user_id}", response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_user(
    user_id: Annotated[int, Path(gt=0)],
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    """
    Возвращает пользователя с указанным ID
    """
    user = await user_service.get_user(user_id)
    return user


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserIn,
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    """
    Регистрирует нового пользователя
    """
    new_user = await user_service.create_user(user)
    return new_user


@router.post("/token", response_model=Token, status_code=status.HTTP_201_CREATED)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    """
    Аутентифицирует пользователя и возвращает JWT-token.
    """
    db_user = await user_service.login_user(form_data.username, form_data.password)

    access_token = create_access_token(data={
        "sub": db_user.email,
        "name": db_user.name,
        "id": db_user.id,
        "address": db_user.address,
    })

    return Token(access_token=access_token, token_type="bearer")


@router.patch("/", response_model=Token, status_code=status.HTTP_200_OK)
async def update_user(
    user_data: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    """
    Обновляет данные пользователя и возвращает новый JWT-token
    """
    updated_user = await user_service.update_user(current_user.id, user_data)

    access_token = create_access_token(data={
        "sub": updated_user.email,
        "name": updated_user.name,
        "id": updated_user.id,
        "address": updated_user.address,
    })

    return Token(access_token=access_token, token_type="bearer")
