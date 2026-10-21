from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


_REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"


class Settings(BaseSettings):
    app_name: str = "Founders Carnet API"
    secret_key: str = Field(
        default="dev-secret-key-change-me",
        validation_alias=AliasChoices("JWT_SECRET", "SECRET_KEY"),
    )
    algorithm: str = Field(
        default="HS256",
        validation_alias=AliasChoices("JWT_ALGORITHM", "ALGORITHM"),
    )
    access_token_expire_minutes: int = 60 * 24
    database_url: str = Field(
        default="sqlite:///./app.db",
        validation_alias=AliasChoices("DATABASE_URL", "database_url"),
    )
    gemini_api_key: SecretStr | None = None
    gemini_model: str = "gemini-2.5-flash"
    gemini_fallback_model: str | None = Field(
        default=None,
        validation_alias="GEMINI_FALLBACK_MODEL",
    )
    gemini_request_timeout_ms: int = Field(
        default=60_000,
        ge=10_000,
        le=120_000,
        validation_alias="GEMINI_REQUEST_TIMEOUT_MS",
    )
    embedding_model_name: str = _DEFAULT_EMBEDDING_MODEL
    compliance_top_k: int = 5
    compliance_minimum_similarity: float = 0.4

    @field_validator("database_url", mode="before")
    @classmethod
    def select_installed_postgres_driver(cls, value: object) -> object:
        # requirements.txt installs psycopg 3, while bare postgresql:// selects psycopg2.
        if isinstance(value, str) and value.startswith("postgresql://"):
            return value.replace("postgresql://", "postgresql+psycopg://", 1)
        return value

    @field_validator("gemini_fallback_model", mode="before")
    @classmethod
    def normalize_gemini_fallback_model(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip() or None
        return value

    model_config = SettingsConfigDict(
        env_file=_REPOSITORY_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
