import os
import sys
from functools import lru_cache
from pydantic import BaseSettings, validator, PostgresDsn, Field
from datetime import timedelta
from typing import Any, Dict, Optional


class Settings(BaseSettings):
    APP_NAME: str = "Modulaptop Store"
    APP_ROOT_PATH: str = "/"
    SERVICE_ENV: str = "dev"
    VERSION: float = 0.1
    DEBUG: bool = False
    APPLICATION_PORT: int = 9030
    HTTP_CLIENT_TIMEOUT: timedelta = Field("PT60S")

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5439"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "modulaptop_store_db"
    POSTGRES_APPLICATION_NAME: str = "modulaptop_store"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        env_nested_delimiter = "__"
        env_file = os.environ.get("SETTINGS_ENV", ".env")


class TestSettings(Settings):
    @validator("POSTGRES_DB", pre=True)
    def rewrite_test_db(cls, value: str, values: dict[str, Any]) -> str:
        if not value.endswith("_test"):
            value = f"{value}_test"
        return value


@lru_cache
def get_settings() -> Settings:
    if "pytest" in sys.modules:
        return TestSettings()
    return Settings()


settings = get_settings()
