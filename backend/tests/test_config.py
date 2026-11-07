from pathlib import Path

from app.config import Settings


def test_settings_load_repository_root_env_and_use_documented_embedding_default() -> None:
    repository_root = Path(__file__).resolve().parents[2]

    assert Settings.model_config["env_file"] == repository_root / ".env"
    assert (
        Settings().embedding_model_name
        == "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    )


def test_settings_accept_documented_jwt_names_and_psycopg3_url() -> None:
    jwt_stub = "unit-test-secret"
    settings = Settings(
        JWT_SECRET=jwt_stub,
        JWT_ALGORITHM="HS512",
        DATABASE_URL="postgresql://user:password@localhost/carnet",
    )

    assert settings.secret_key == "unit-test-secret"
    assert settings.algorithm == "HS512"
    assert settings.database_url.startswith("postgresql+psycopg://")


def test_settings_provide_bounded_gemini_request_timeout() -> None:
    assert Settings().gemini_request_timeout_ms == 60_000
    assert Settings(GEMINI_REQUEST_TIMEOUT_MS=45_000).gemini_request_timeout_ms == 45_000


def test_settings_read_optional_gemini_fallback_model() -> None:
    assert Settings(GEMINI_FALLBACK_MODEL="configured-fallback").gemini_fallback_model == (
        "configured-fallback"
    )
    assert Settings(GEMINI_FALLBACK_MODEL="").gemini_fallback_model is None
