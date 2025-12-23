from fastapi import HTTPException, status


class Unauthorized401(HTTPException):
    def __init__(
            self,
            detail: str = "Не удалось подтвердить учетные данные",
            headers: dict = {"WWW-Authenticate": "Bearer"},
    ):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers=headers,
        )


class Expired401(HTTPException):
    def __init__(
            self,
            detail: str = "Срок действия токена истек",
            headers: dict = {"WWW-Authenticate": "Bearer"},
    ):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers=headers,
        )


class BadRequestNotData400(HTTPException):
    def __init__(
            self,
            detail: str = "Нет данных для обновления",
    ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class BadRequestEmail400(HTTPException):
    def __init__(
            self,
            detail: str = "Почта уже зарегистрирована",
    ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class BadRequestUser400(HTTPException):
    def __init__(
            self,
            detail: str = "Пользователь не найден",
    ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )
