from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Labore Portal API"
    environment: str = "development"
    database_url: str = "postgresql+psycopg://labore_app:change-me-locally@localhost:5432/labore"
    audit_log_retention_days: int = 2555
    document_trash_retention_days: int = 30
    storage_root: str = "./storage/clientes"
    max_upload_size_bytes: int = 50 * 1024 * 1024

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local"),
        env_prefix="LABORE_",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
