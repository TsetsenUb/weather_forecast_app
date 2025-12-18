from pydantic import BaseModel, Field, ConfigDict, EmailStr, field_validator


class UserBase(BaseModel):
    """
    Базовая схема пользователя
    """
    address: str | None = Field(
        default=None,
        description="Название города",
        examples=["Москва", "Moscow"]
    )

    @field_validator("address", mode="after")
    def validate_address(cls, v: str):
        if v == "":
            return None
        return v.strip().title()


class UserIn(UserBase):
    """
    Схема для создания пользователя
    """
    name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Имя пользователя"
    )

    email: EmailStr = Field(
        ...,
        max_length=100,
        description="Почта пользователя",
        examples=["user_1@example.com"]
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=255,
        description="Пароль (минимум 8 символов)"
    )


class UserOut(UserBase):
    """
    Схема для возврата данных о пользователе
    """
    id: int = Field(..., description="Уникальный идентификатор пользователя")
    name: str = Field(..., description="Имя пользователя")
    email: EmailStr = Field(..., description="Почта пользователя")
    is_active: bool = Field(..., description="Активность пользователя")

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(UserBase):
    """
    Схема для обновления пользователя
    """
    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=50,
        description="Имя пользователя"
    )

    email: EmailStr | None = Field(
        default=None,
        max_length=100,
        description="Почта пользователя",
        examples=["user_1@example.com"]
    )

    password: str | None = Field(
        default=None,
        min_length=8,
        max_length=255,
        description="Пароль (минимум 8 символов)"
    )
