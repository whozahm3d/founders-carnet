"""Dense, BM25, and reciprocal-rank-fusion retrieval (FR-8, NFR-12, NFR-13)."""

from __future__ import annotations

import math
import re
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any

from rank_bm25 import BM25Plus


@dataclass(frozen=True, slots=True)
class RetrievedChunk:
    chunk: Any
    similarity: float
    method: str = "dense"

    @property
    def score(self) -> float:
        return self.similarity


def dense(
    query_embedding: Sequence[float],
    chunks: Sequence[Any],
    *,
    top_k: int = 8,
    minimum_score: float = 0.0,
) -> tuple[RetrievedChunk, ...]:
    query = _vector(query_embedding)
    ranked: list[RetrievedChunk] = []
    for chunk in chunks:
        embedding = getattr(chunk, "embedding", None)
        if embedding is None:
            continue
        score = _cosine(query, _vector(embedding))
        if score >= minimum_score:
            ranked.append(RetrievedChunk(chunk, score, "dense"))
    ranked.sort(key=lambda item: (-item.score, item.chunk.id))
    return tuple(ranked[:_top_k(top_k)])


def bm25(
    query: str,
    chunks: Sequence[Any],
    *,
    top_k: int = 8,
    minimum_score: float = 0.0,
) -> tuple[RetrievedChunk, ...]:
    if not chunks:
        return ()
    tokenized = [_tokens(chunk.text) for chunk in chunks]
    query_tokens = _tokens(query)
    if not query_tokens:
        return ()
    model = BM25Plus(tokenized)
    scores = model.get_scores(query_tokens)
    maximum = max(scores, default=0.0)
    if maximum <= 0.0:
        return ()
    ranked = [
        RetrievedChunk(chunk, float(score / maximum) if maximum > 0 else 0.0, "bm25")
        for index, (chunk, score) in enumerate(zip(chunks, scores, strict=True))
        if set(query_tokens).intersection(tokenized[index])
        and (float(score / maximum) if maximum > 0 else 0.0) >= minimum_score
    ]
    ranked.sort(key=lambda item: (-item.score, item.chunk.id))
    return tuple(ranked[:_top_k(top_k)])


def hybrid(
    query: str,
    query_embedding: Sequence[float],
    chunks: Sequence[Any],
    *,
    top_k: int = 8,
    rrf_k: int = 60,
    dense_retriever: Callable[..., tuple[RetrievedChunk, ...]] = dense,
    minimum_score: float = 0.0,
) -> tuple[RetrievedChunk, ...]:
    """Fuse dense and BM25 rankings using standard RRF with k=60 by default."""
    if rrf_k < 1:
        raise ValueError("rrf_k must be positive")
    # dense() and bm25() both cap their public result count at 20.
    candidate_k = min(len(chunks), 20, max(32, top_k * 4))
    dense_rows = dense_retriever(
        query_embedding, chunks, top_k=candidate_k, minimum_score=minimum_score
    )
    lexical_rows = bm25(
        query, chunks, top_k=candidate_k, minimum_score=minimum_score
    )
    scores: dict[str, float] = {}
    by_id: dict[str, Any] = {}
    for ranking in (dense_rows, lexical_rows):
        for rank, row in enumerate(ranking, start=1):
            key = str(row.chunk.chunk_id)
            by_id[key] = row.chunk
            scores[key] = scores.get(key, 0.0) + 1.0 / (rrf_k + rank)
    ranked = [
        RetrievedChunk(chunk, min(1.0, score * (rrf_k + 1) / 2.0), "hybrid")
        for key, chunk in by_id.items()
        if (score := scores[key]) * (rrf_k + 1) / 2.0 >= minimum_score
    ]
    ranked.sort(key=lambda item: (-item.score, item.chunk.id))
    return tuple(ranked[:_top_k(top_k)])


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.casefold())


def _vector(values: Sequence[float]) -> tuple[float, ...]:
    vector = tuple(float(value) for value in values)
    if not vector or any(not math.isfinite(value) for value in vector):
        raise ValueError("Embedding must contain finite values")
    return vector


def _cosine(first: Sequence[float], second: Sequence[float]) -> float:
    if len(first) != len(second):
        return -1.0
    denominator = math.sqrt(sum(value * value for value in first)) * math.sqrt(
        sum(value * value for value in second)
    )
    if denominator == 0.0:
        return 0.0
    return sum(a * b for a, b in zip(first, second, strict=True)) / denominator


def _top_k(value: int) -> int:
    if not 1 <= value <= 20:
        raise ValueError("top_k must be between 1 and 20")
    return value
