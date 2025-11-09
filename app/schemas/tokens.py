from pydantic import BaseModel


class Token(BaseModel):
    """
    Схема для возвращения jwt-токена на frontend
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Схема для валидации данных payload jwt-токена
    """
    sub: str
    name: str
    id: int
    address: str
    exp: int
