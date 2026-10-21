"""Configured embeddings and the sole Gemini gateway for Features 1, 3, and 4."""

from functools import lru_cache

from fastapi import HTTPException, status

from app.config import get_settings
from app.services.llm_gateway import GeminiGateway
from rag.compliance.embeddings import SentenceTransformerEncoder


@lru_cache(maxsize=1)
def get_gateway() -> GeminiGateway:
    settings = get_settings()
    if settings.gemini_api_key is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="AI service is not configured")
    return GeminiGateway(api_key=settings.gemini_api_key.get_secret_value(), model_name=settings.gemini_model)


@lru_cache(maxsize=1)
def get_encoder() -> SentenceTransformerEncoder:
    settings = get_settings()
    if not settings.embedding_model_name:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Embedding model is not configured")
    return SentenceTransformerEncoder(settings.embedding_model_name)


def clear_feature_clients() -> None:
    if get_gateway.cache_info().currsize:
        get_gateway().close()
    get_gateway.cache_clear()
    get_encoder.cache_clear()
