from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    # App
    app_name: str = "Orders API"
    debug: bool = False
    secret_key: str                  # ← OBLIGATORIO, no tiene default
    environment: str = "development"

    # Base de datos
    database_url: str = "sqlite:///./orders.db"

    # JWT
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",             # lee desde .env automáticamente
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


# Singleton cacheado — se carga una sola vez
@lru_cache
def get_settings() -> Settings:
    return Settings()