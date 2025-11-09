from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    OWM_APPID: str
    OWM_FORECAST_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
