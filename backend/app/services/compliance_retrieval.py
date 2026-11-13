"""Query section-aware compliance chunks through pgvector (FR-8, NFR-12, NFR-13, NFR-20)."""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass

from sqlalchemy import and_, case, distinct, func, select
from sqlalchemy.orm import Session

from app.models import ComplianceChunk, ComplianceDocument
from rag.compliance.retrieve import (
    RetrievedChunk,
    bm25 as bm25_retrieve,
    dense as dense_retrieve,
    hybrid as hybrid_retrieve,
)

from typing import Literal


@dataclass(frozen=True, slots=True)
class RetrievalIndexStats:
    document_count: int
    active_document_count: int
    active_chunk_count: int
    embedded_chunk_count: int
    compatible_chunk_count: int


def get_retrieval_index_stats(
    session: Session,
    *,
    embedding_model: str,
) -> RetrievalIndexStats:
    """Count active corpus rows and vectors compatible with the configured model."""
    if not embedding_model.strip():
        raise ValueError("embedding_model must not be empty")
    statement = (
        select(
            func.count(distinct(ComplianceDocument.id)),
            func.count(
                distinct(
                    case(
                        (
                            ComplianceDocument.is_active.is_(True),
                            ComplianceDocument.id,
                        )
                    )
                )
            ),
            func.count(
                case(
                    (
                        and_(
                            ComplianceDocument.is_active.is_(True),
                            ComplianceChunk.id.is_not(None),
                        ),
                        1,
                    )
                )
            ),
            func.count(
                case(
                    (
                        and_(
                            ComplianceDocument.is_active.is_(True),
                            ComplianceChunk.id.is_not(None),
                            ComplianceChunk.embedding.is_not(None),
                        ),
                        1,
                    )
                )
            ),
            func.count(
                case(
                    (
                        and_(
                            ComplianceDocument.is_active.is_(True),
                            ComplianceChunk.id.is_not(None),
                            ComplianceChunk.embedding.is_not(None),
                            ComplianceChunk.embedding_model == embedding_model,
                        ),
                        1,
                    )
                )
            ),
        )
        .select_from(ComplianceDocument)
        .outerjoin(ComplianceChunk)
    )
    documents, active_documents, active_chunks, embedded_chunks, compatible_chunks = (
        session.execute(statement).one()
    )
    return RetrievalIndexStats(
        document_count=int(documents or 0),
        active_document_count=int(active_documents or 0),
        active_chunk_count=int(active_chunks or 0),
        embedded_chunk_count=int(embedded_chunks or 0),
        compatible_chunk_count=int(compatible_chunks or 0),
    )


def retrieve_top_chunks(
    session: Session,
    *,
    query_embedding: Sequence[float],
    embedding_model: str,
    top_k: int = 5,
    minimum_similarity: float = 0.0,
    query: str = "",
    method: Literal["dense", "bm25", "hybrid"] = "dense",
) -> tuple[RetrievedChunk, ...]:
    """Return active-source chunks from the same embedding model, best match first."""
    query_vector = _validate_embedding(query_embedding)
    if not embedding_model.strip():
        raise ValueError("embedding_model must not be empty")
    if not 1 <= top_k <= 20:
        raise ValueError("top_k must be between 1 and 20")
    if not -1.0 <= minimum_similarity <= 1.0:
        raise ValueError("minimum_similarity must be between -1 and 1")

    statement = select(ComplianceChunk).join(ComplianceDocument).where(
        ComplianceDocument.is_active.is_(True)
    )
    if method in {"dense", "hybrid"}:
        statement = statement.where(
            ComplianceChunk.embedding_model == embedding_model,
            ComplianceChunk.embedding.is_not(None),
        )
    if method == "dense" and session.get_bind().dialect.name == "postgresql":
        statement = statement.where(
            func.vector_dims(ComplianceChunk.embedding) == len(query_vector)
        )
        distance = ComplianceChunk.embedding.cosine_distance(query_vector)
        rows = session.execute(
            statement.add_columns(distance.label("distance"))
            .where(distance <= 1.0 - minimum_similarity)
            .order_by(distance, ComplianceChunk.id)
            .limit(top_k)
        ).all()
        return tuple(
            RetrievedChunk(chunk, 1.0 - float(distance_value), "dense")
            for chunk, distance_value in rows
        )
    rows = session.scalars(statement).all()
    if method == "bm25":
        return bm25_retrieve(
            query, rows, top_k=top_k, minimum_score=minimum_similarity
        )
    if method == "hybrid":
        return hybrid_retrieve(
            query,
            query_vector,
            rows,
            top_k=top_k,
            minimum_score=minimum_similarity,
        )
    return dense_retrieve(
        query_vector, rows, top_k=top_k, minimum_score=minimum_similarity
    )


def cosine_similarity(first: Sequence[float], second: Sequence[float]) -> float:
    """Calculate cosine similarity for deterministic local SQLite tests."""
    first_vector = _validate_embedding(first)
    second_vector = _validate_embedding(second)
    if len(first_vector) != len(second_vector):
        raise ValueError("Embedding dimensions do not match")

    first_norm = math.sqrt(math.fsum(value * value for value in first_vector))
    second_norm = math.sqrt(math.fsum(value * value for value in second_vector))
    if first_norm == 0.0 or second_norm == 0.0:
        return 0.0

    dot_product = math.fsum(
        a * b for a, b in zip(first_vector, second_vector, strict=True)
    )
    return dot_product / (first_norm * second_norm)


def _validate_embedding(values: Sequence[float]) -> list[float]:
    vector = [float(value) for value in values]
    if not vector:
        raise ValueError("Embedding must not be empty")
    if not all(math.isfinite(value) for value in vector):
        raise ValueError("Embedding values must be finite numbers")
    return vector
