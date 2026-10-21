"""Configurable SentenceTransformer embeddings (FR-8, NFR-20)."""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Any


class EmbeddingError(ValueError):
    """Raised for invalid text input or malformed embedding output."""


class SentenceTransformerEncoder:
    def __init__(self, model_name: str, *, model: Any | None = None) -> None:
        if not model_name.strip():
            raise ValueError("An embedding model name must be configured")
        self.model_name = model_name
        self._model = model

    def encode(self, texts: Sequence[str]) -> tuple[tuple[float, ...], ...]:
        if not texts:
            return ()
        if any(not text.strip() for text in texts):
            raise EmbeddingError("Embedding inputs must not be empty")

        model = self._model or self._load_model()
        raw_embeddings = model.encode(
            list(texts),
            normalize_embeddings=True,
            convert_to_numpy=True,
        )
        vectors = tuple(tuple(float(value) for value in vector) for vector in raw_embeddings)
        if len(vectors) != len(texts):
            raise EmbeddingError("Embedding model returned an unexpected number of vectors")
        if not vectors or not vectors[0]:
            raise EmbeddingError("Embedding model returned an empty vector")

        dimensions = len(vectors[0])
        if any(len(vector) != dimensions for vector in vectors):
            raise EmbeddingError("Embedding model returned inconsistent dimensions")
        if any(not math.isfinite(value) for vector in vectors for value in vector):
            raise EmbeddingError("Embedding model returned non-finite values")
        return vectors

    def _load_model(self) -> Any:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise RuntimeError(
                "Install the pinned rag requirements before generating embeddings"
            ) from exc

        self._model = SentenceTransformer(self.model_name)
        return self._model
