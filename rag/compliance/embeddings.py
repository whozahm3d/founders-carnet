"""Configurable SentenceTransformer embeddings (FR-8, NFR-20)."""

from __future__ import annotations

import math
from collections.abc import Sequence
from pathlib import Path
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
        return self._encode(texts, role="passage")

    def encode_query(self, texts: Sequence[str]) -> tuple[tuple[float, ...], ...]:
        return self._encode(texts, role="query")

    def encode_passages(self, texts: Sequence[str]) -> tuple[tuple[float, ...], ...]:
        return self._encode(texts, role="passage")

    def prepare_chunks(self, chunks: tuple[Any, ...]) -> tuple[Any, ...]:
        from rag.compliance.chunking import split_chunks_for_model

        model = self._model or self._load_model()
        return split_chunks_for_model(chunks, model.tokenizer, model.max_seq_length)

    def _encode(
        self, texts: Sequence[str], *, role: str
    ) -> tuple[tuple[float, ...], ...]:
        if not texts:
            return ()
        if any(not text.strip() for text in texts):
            raise EmbeddingError("Embedding inputs must not be empty")

        model = self._model or self._load_model()
        prefix = "query: " if role == "query" else "passage: "
        model_texts = [
            (prefix + text)
            if self.model_name.startswith("intfloat/multilingual-e5")
            and not text.casefold().startswith(("query: ", "passage: "))
            else text
            for text in texts
        ]
        maximum = int(getattr(model, "max_seq_length", 0) or 0)
        tokenizer = getattr(model, "tokenizer", None)
        if maximum and tokenizer is not None:
            for text in model_texts:
                token_count = len(
                    tokenizer(text, add_special_tokens=True, truncation=False)["input_ids"]
                )
                if token_count > maximum:
                    raise EmbeddingError(
                        f"Input has {token_count} tokens; {self.model_name} limit is {maximum}"
                    )
        raw_embeddings = model.encode(
            model_texts,
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

        cache_folder = Path(__file__).resolve().parents[1] / "cache" / "models"
        self._model = SentenceTransformer(
            self.model_name, cache_folder=str(cache_folder)
        )
        return self._model
