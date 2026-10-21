from functools import lru_cache

from fastapi import HTTPException, status
from rag.compliance.embeddings import SentenceTransformerEncoder

from app.config import get_settings
from app.services.compliance_assistant import ComplianceAnswerService
from app.services.llm_gateway import GeminiGateway


@lru_cache(maxsize=1)
def get_compliance_answer_service() -> ComplianceAnswerService:
    settings = get_settings()
    if settings.gemini_api_key is None or settings.embedding_model_name is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Compliance assistant is not configured",
        )

    gateway = GeminiGateway(
        api_key=settings.gemini_api_key.get_secret_value(),
        model_name=settings.gemini_model,
        fallback_model=settings.gemini_fallback_model,
        request_timeout_ms=settings.gemini_request_timeout_ms,
    )
    encoder = SentenceTransformerEncoder(settings.embedding_model_name)
    return ComplianceAnswerService(
        encoder=encoder,
        gateway=gateway,
        embedding_model=settings.embedding_model_name,
        top_k=settings.compliance_top_k,
        minimum_similarity=settings.compliance_minimum_similarity,
    )


def close_compliance_answer_service() -> None:
    if get_compliance_answer_service.cache_info().currsize:
        get_compliance_answer_service().close()
    get_compliance_answer_service.cache_clear()
