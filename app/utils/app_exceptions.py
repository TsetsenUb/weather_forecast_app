from fastapi import HTTPException, status


UNAUTHORIZED_401 = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Не удалось подтвердить учетные данные",
    headers={"WWW-Authenticate": "Bearer"},
)

EXPIRED_401 = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Срок действия токена истек",
    headers={"WWW-Authenticate": "Bearer"},
)

BAD_REQUEST_NOT_DATA_400 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Нет данных для обновления"
)

BAD_REQUEST_EMAIL_400 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Почта уже зарегистрирована"
)

BAD_REQUEST_USER_400 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Пользователь не найден"
)
