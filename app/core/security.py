from pwdlib import PasswordHash


pwd_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Преобразует пароль в хеш с использованием argon2.
    """
    return pwd_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет, соответствует ли введённый пароль сохранённому хешу.
    """
    return pwd_hash.verify(plain_password, hashed_password)
