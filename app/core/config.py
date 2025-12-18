from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    OWM_APPID: SecretStr
    OWM_FORECAST_URL: str

    SECRET_KEY: SecretStr
    ALGORITHM: SecretStr
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    DB_USER: SecretStr
    DB_PASSWORD: SecretStr
    DB_NAME: SecretStr

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_FORECAST_EXPIRE_SEC: int

    ALLOW_ORIGINS: list[str]
    ALLOW_METHODS: list[str]
    ALLOW_HEADERS: list[str]


settings = Settings()
