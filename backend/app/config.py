from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field, SecretStr, field_validator, model_validator
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
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        validation_alias=AliasChoices("REDIS_URL", "redis_url"),
    )
    gemini_api_key: SecretStr | None = None
    firecrawl_api_key: SecretStr | None = None
    firecrawl_request_timeout_ms: int = Field(
        default=25_000,
        ge=5_000,
        le=55_000,
        validation_alias="FIRECRAWL_REQUEST_TIMEOUT_MS",
    )
    resume_storage_dir: Path = Field(
        default=_REPOSITORY_ROOT / "backend" / ".private" / "resumes",
        validation_alias="RESUME_STORAGE_DIR",
    )
    llm_cache_dir: Path = Field(
        default=_REPOSITORY_ROOT / "backend" / ".private" / "llm-cache",
        validation_alias="LLM_CACHE_DIR",
    )
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
    verification_low_threshold: float = Field(default=0.5, ge=0.0, le=1.0)
    verification_high_threshold: float = Field(default=0.85, ge=0.0, le=1.0)
    verification_rule_version: str = "profile-verification-v2"
    verification_linkedin_weight: float = Field(default=0.15, ge=0.0, le=1.0)
    verification_secp_weight: float = Field(default=0.25, ge=0.0, le=1.0)
    verification_completeness_weight: float = Field(default=0.20, ge=0.0, le=1.0)
    verification_github_weight: float = Field(default=0.15, ge=0.0, le=1.0)
    verification_portfolio_weight: float = Field(default=0.25, ge=0.0, le=1.0)

    @model_validator(mode="after")
    def validate_verification_thresholds(self) -> "Settings":
        if self.verification_high_threshold <= self.verification_low_threshold:
            raise ValueError("Verification high threshold must exceed the low threshold")
        weights = (
            self.verification_linkedin_weight,
            self.verification_secp_weight,
            self.verification_completeness_weight,
            self.verification_github_weight,
            self.verification_portfolio_weight,
        )
        if abs(sum(weights) - 1.0) > 0.0001:
            raise ValueError("Verification signal weights must sum to 1")
        return self

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
