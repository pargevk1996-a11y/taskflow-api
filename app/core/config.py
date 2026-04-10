from functools import lru_cache
<<<<<<< HEAD
from typing import Any, Literal

from pydantic import computed_field, field_validator
=======
from typing import Literal

from pydantic import computed_field
>>>>>>> e9df211 (initial commit)
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "TaskFlow API"
    app_env: Literal["development", "staging", "production"] = "development"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"
    host: str = "0.0.0.0"
    port: int = 8000

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "taskflow"
    postgres_user: str = "taskflow_user"
    postgres_password: str = "taskflow_password"
    database_url: str | None = None

<<<<<<< HEAD
    jwt_secret_key: str = "change_me_dev_secret"
=======
    jwt_secret_key: str
>>>>>>> e9df211 (initial commit)
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_url: str | None = None

    celery_broker_url: str | None = None
    celery_result_backend: str | None = None

    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    log_level: str = "INFO"

    smtp_host: str = "smtp.example.com"
    smtp_port: int = 587
    smtp_user: str = "example_user"
    smtp_password: str = "example_password"
    smtp_from: str = "noreply@example.com"

<<<<<<< HEAD
    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug(cls, value: Any) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"1", "true", "yes", "on", "debug"}:
                return True
            if normalized in {"0", "false", "no", "off", "release", "prod", "production"}:
                return False
        return bool(value)

=======
>>>>>>> e9df211 (initial commit)
    @computed_field
    @property
    def sqlalchemy_database_uri(self) -> str:
        if self.database_url:
            return self.database_url
        return (
            f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @computed_field
    @property
    def redis_dsn(self) -> str:
        if self.redis_url:
            return self.redis_url
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    @computed_field
    @property
    def celery_broker_dsn(self) -> str:
        if self.celery_broker_url:
            return self.celery_broker_url
        return self.redis_dsn

    @computed_field
    @property
    def celery_backend_dsn(self) -> str:
        if self.celery_result_backend:
            return self.celery_result_backend
        return self.redis_dsn

    @computed_field
    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
