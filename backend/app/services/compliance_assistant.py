"""Grounded compliance-answer orchestration (FR-8, NFR-11 to NFR-14)."""

from __future__ import annotations

import logging
import re
from collections.abc import Sequence
from time import perf_counter
from typing import Literal, Protocol

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.models import ComplianceCitation, ComplianceQuery
from rag.compliance.answer import ANSWER_PROMPT_VERSION, AnswerOutput
from app.services.compliance_retrieval import (
    RetrievedChunk,
    get_retrieval_index_stats,
    retrieve_top_chunks,
)

PROMPT_VERSION = ANSWER_PROMPT_VERSION
INFORMATIONAL_NOTICE = "This information is not legal or tax advice."
_ABSTENTION_MESSAGE = "I do not have a supported answer in the indexed corpus."
_CASE_SPECIFIC_ADVICE = re.compile(
    r"\b(?:do i|does my|should i|am i)\b.{0,120}"
    r"\b(?:need|have to|required to|register|apply for)\b.{0,120}"
    r"\b(?:licen[cs]e|permit|registration)\b",
    re.IGNORECASE,
)
_MONEY_OR_RATE = re.compile(
    r"(?:\d+(?:\.\d+)?\s*%|\b(?:PKR|Rs\.?)\s*[\d,]+)", re.IGNORECASE
)
logger = logging.getLogger(__name__)


AnswerDraft = AnswerOutput


class GroundingValidation(BaseModel):
    is_supported: bool
    unsupported_claims: list[str] = Field(default_factory=list)


class AnswerGateway(Protocol):
    prompt_version: str

    def generate_answer(
        self,
        question: str,
        passages: Sequence[RetrievedChunk],
    ) -> AnswerDraft: ...

    def validate_answer(
        self,
        question: str,
        answer: str,
        passages: Sequence[RetrievedChunk],
    ) -> GroundingValidation: ...


class TextEncoder(Protocol):
    def encode(self, texts: Sequence[str]) -> Sequence[Sequence[float]]: ...


class CitationResult(BaseModel):
    chunk_id: str
    document_title: str
    issuing_body: str
    source_url: str
    section: str | None
    page_number: int
    effective_date: str | None
    consolidation_date: str | None
    retrieved_at: str | None


class ComplianceAnswerResult(BaseModel):
    query_id: int
    outcome: Literal["answered", "abstained"]
    answer: str | None
    message: str | None
    abstention_reason: str | None
    citations: tuple[CitationResult, ...]
    informational_notice: str = INFORMATIONAL_NOTICE


class ComplianceServiceUnavailable(RuntimeError):
    """Raised when the answer provider fails; details are not exposed to clients."""


class ComplianceAnswerService:
    def __init__(
        self,
        *,
        encoder: TextEncoder,
        gateway: AnswerGateway,
        embedding_model: str,
        top_k: int = 5,
        minimum_similarity: float = 0.0,
    ) -> None:
        self.encoder = encoder
        self.gateway = gateway
        self.embedding_model = embedding_model
        self.top_k = top_k
        self.minimum_similarity = minimum_similarity

    def close(self) -> None:
        close = getattr(self.gateway, "close", None)
        if close is not None:
            close()

    def ask(
        self, session: Session, *, user_id: int, question: str
    ) -> ComplianceAnswerResult:
        normalized_question = question.strip()
        if not normalized_question:
            raise ValueError("Question must not be empty")

        started_at = perf_counter()
        if _CASE_SPECIFIC_ADVICE.search(normalized_question):
            return self._save_result(
                session,
                user_id=user_id,
                question=normalized_question,
                outcome="abstained",
                answer=None,
                message="I cannot determine whether a specific business needs a license or registration.",
                reason="case_specific_advice",
                passages=(),
                citation_results=(),
                started_at=started_at,
            )

        try:
            index_stats = get_retrieval_index_stats(
                session,
                embedding_model=self.embedding_model,
            )
            logger.info(
                "Compliance retrieval index state",
                extra={
                    "user_id": user_id,
                    "embedding_model": self.embedding_model,
                    "document_count": index_stats.document_count,
                    "active_document_count": index_stats.active_document_count,
                    "active_chunk_count": index_stats.active_chunk_count,
                    "embedded_chunk_count": index_stats.embedded_chunk_count,
                    "compatible_chunk_count": index_stats.compatible_chunk_count,
                    "minimum_similarity": self.minimum_similarity,
                    "top_k": self.top_k,
                },
            )
            if index_stats.compatible_chunk_count:
                encode_query = getattr(self.encoder, "encode_query", self.encoder.encode)
                vectors = encode_query([normalized_question])
                if len(vectors) != 1:
                    raise ValueError("Embedding provider returned an invalid result")
                passages = retrieve_top_chunks(
                    session,
                    query_embedding=vectors[0],
                    embedding_model=self.embedding_model,
                    top_k=self.top_k,
                    minimum_similarity=self.minimum_similarity,
                    query=normalized_question,
                    method="hybrid",
                )
            else:
                passages = ()
            logger.info(
                "Compliance retrieval completed",
                extra={
                    "user_id": user_id,
                    "retrieved_passage_count": len(passages),
                    "top_similarity": passages[0].similarity if passages else None,
                },
            )
        except Exception as exc:
            logger.exception("Compliance retrieval failed for user_id=%s", user_id)
            self._save_failed_query(
                session,
                user_id=user_id,
                question=normalized_question,
                passage_count=0,
                started_at=started_at,
            )
            raise ComplianceServiceUnavailable("Compliance retrieval failed") from exc
        if not passages:
            return self._save_result(
                session,
                user_id=user_id,
                question=normalized_question,
                outcome="abstained",
                answer=None,
                message=_ABSTENTION_MESSAGE,
                reason="no_supporting_passage",
                passages=(),
                citation_results=(),
                started_at=started_at,
            )

        try:
            draft = AnswerDraft.model_validate(
                self.gateway.generate_answer(normalized_question, passages)
            )
            if draft.abstain or not draft.answer.strip():
                return self._abstain_after_retrieval(
                    session,
                    user_id=user_id,
                    question=normalized_question,
                    reason="model_abstained",
                    passages=passages,
                    started_at=started_at,
                )
            passage_by_id = {passage.chunk.chunk_id: passage for passage in passages}
            cited_ids = tuple(dict.fromkeys(draft.citation_chunk_ids))
            if not cited_ids or any(
                chunk_id not in passage_by_id for chunk_id in cited_ids
            ):
                return self._abstain_after_retrieval(
                    session,
                    user_id=user_id,
                    question=normalized_question,
                    reason="invalid_citation",
                    passages=passages,
                    started_at=started_at,
                )

            cited_passages = tuple(passage_by_id[chunk_id] for chunk_id in cited_ids)
            if not _numeric_claims_are_supported(draft.answer, cited_passages):
                return self._abstain_after_retrieval(
                    session,
                    user_id=user_id,
                    question=normalized_question,
                    reason="unsupported_number_or_date",
                    passages=passages,
                    started_at=started_at,
                )
            if any(
                not (
                    getattr(passage.chunk, "effective_date", None)
                    or passage.chunk.document.effective_date
                )
            if _MONEY_OR_RATE.search(draft.answer) and any(
                passage.chunk.document.effective_date is None
                for passage in cited_passages
            ):
                return self._abstain_after_retrieval(
                    session,
                    user_id=user_id,
                    question=normalized_question,
                    reason="missing_effective_date",
                    passages=passages,
                    started_at=started_at,
                )

            validation = GroundingValidation.model_validate(
                self.gateway.validate_answer(
                    normalized_question, draft.answer, cited_passages
                )
            )
            if not validation.is_supported:
                return self._abstain_after_retrieval(
                    session,
                    user_id=user_id,
                    question=normalized_question,
                    reason="validation_failed",
                    passages=passages,
                    started_at=started_at,
                )

            citation_results = tuple(
                _citation_result(passage) for passage in cited_passages
            )
            return self._save_result(
                session,
                user_id=user_id,
                question=normalized_question,
                outcome="answered",
                answer=draft.answer,
                message=None,
                reason=None,
                passages=passages,
                citation_results=citation_results,
                started_at=started_at,
            )
        except Exception as exc:
            if not getattr(exc, "_carnet_generation_failure_logged", False):
                logger.exception(
                    "Compliance answer generation failed for user_id=%s", user_id
                )
            self._save_failed_query(
                session,
                user_id=user_id,
                question=normalized_question,
                passage_count=len(passages),
                started_at=started_at,
            )
            raise ComplianceServiceUnavailable(
                "Compliance answer generation failed"
            ) from exc

    def _abstain_after_retrieval(
        self,
        session: Session,
        *,
        user_id: int,
        question: str,
        reason: str,
        passages: Sequence[RetrievedChunk],
        started_at: float,
    ) -> ComplianceAnswerResult:
        return self._save_result(
            session,
            user_id=user_id,
            question=question,
            outcome="abstained",
            answer=None,
            message=_ABSTENTION_MESSAGE,
            reason=reason,
            passages=passages,
            citation_results=(),
            started_at=started_at,
        )

    def _save_result(
        self,
        session: Session,
        *,
        user_id: int,
        question: str,
        outcome: Literal["answered", "abstained"],
        answer: str | None,
        message: str | None,
        reason: str | None,
        passages: Sequence[RetrievedChunk],
        citation_results: tuple[CitationResult, ...],
        started_at: float,
    ) -> ComplianceAnswerResult:
        query = ComplianceQuery(
            user_id=user_id,
            question=question,
            answer_text=answer,
            outcome=outcome,
            abstention_reason=reason,
            passage_count=len(passages),
            latency_ms=max(0, int((perf_counter() - started_at) * 1000)),
            prompt_version=self.gateway.prompt_version
            if outcome == "answered"
            else None,
        )
        session.add(query)
        session.flush()
        passage_by_id = {passage.chunk.chunk_id: passage for passage in passages}
        for rank, citation in enumerate(citation_results, start=1):
            chunk = passage_by_id[citation.chunk_id].chunk
            session.add(
                ComplianceCitation(query_id=query.id, chunk_id=chunk.id, rank=rank)
            )
        session.commit()
        session.refresh(query)
        return ComplianceAnswerResult(
            query_id=query.id,
            outcome=outcome,
            answer=answer,
            message=message,
            abstention_reason=reason,
            citations=citation_results,
        )

    def _save_failed_query(
        self,
        session: Session,
        *,
        user_id: int,
        question: str,
        passage_count: int,
        started_at: float,
    ) -> None:
        try:
            session.rollback()
            session.add(
                ComplianceQuery(
                    user_id=user_id,
                    question=question,
                    outcome="failed",
                    abstention_reason="provider_failure",
                    passage_count=passage_count,
                    latency_ms=max(0, int((perf_counter() - started_at) * 1000)),
                    prompt_version=self.gateway.prompt_version,
                )
            )
            session.commit()
        except Exception:
            logger.exception(
                "Could not record failed compliance query for user_id=%s", user_id
            )
            try:
                session.rollback()
            except Exception:
                logger.exception(
                    "Could not reset database session after failed query logging"
                )


def _citation_result(passage: RetrievedChunk) -> CitationResult:
    chunk = passage.chunk
    document = chunk.document
    return CitationResult(
        chunk_id=chunk.chunk_id,
        document_title=document.title,
        issuing_body=document.issuing_body,
        source_url=document.source_url,
        section=chunk.section,
        page_number=chunk.page_number,
        effective_date=document.effective_date,
        consolidation_date=document.consolidation_date,
        retrieved_at=document.retrieved_at,
    )


_NUMERIC_CLAIM_PATTERNS = (
    re.compile(r"\b(?:PKR|Rs\.?|rupees?)\s*[\d,]+(?:\.\d+)?\b", re.IGNORECASE),
    re.compile(r"\b\d+(?:[.,]\d+)?\s*%"),
    re.compile(r"\b(?:section|s\.)\s*\d+[A-Z]?(?:\(\d+[A-Z]?\))*", re.IGNORECASE),
    re.compile(r"\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b"),
    re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),
    re.compile(
        r"\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b",
        re.IGNORECASE,
    ),
    re.compile(r"\b(?:tax year|financial year|FY)\s+\d{4}\b", re.IGNORECASE),
)


def _numeric_claims_are_supported(
    answer: str, passages: Sequence[RetrievedChunk]
) -> bool:
    cited_text = " ".join(
        " ".join(
            (
                passage.chunk.text,
                str(passage.chunk.section or ""),
                " ".join(getattr(passage.chunk, "heading_path", ()) or ()),
                str(
                    getattr(passage.chunk, "effective_date", None)
                    or passage.chunk.document.effective_date
                    or ""
                ),
            )
        )
        for passage in passages
    ).casefold()
    for pattern in _NUMERIC_CLAIM_PATTERNS:
        for match in pattern.finditer(answer):
            claim = re.sub(r"\s+", " ", match.group(0)).casefold()
            compact_claim = re.sub(r"[^a-z0-9]+", "", claim)
            compact_source = re.sub(r"[^a-z0-9]+", "", cited_text)
            if claim.startswith(("section", "s.")):
                parts = re.findall(r"\d+[a-z]?", claim)
                supported = all(part in compact_source for part in parts)
            else:
                supported = compact_claim in compact_source
            if not supported:
                return False
    return True
