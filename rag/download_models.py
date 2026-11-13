"""Download and inspect the approved compliance embedding models."""

from __future__ import annotations

import json
from pathlib import Path

from sentence_transformers import SentenceTransformer

MODELS = (
    "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
    "intfloat/multilingual-e5-base",
    "BAAI/bge-m3",
)


def main() -> None:
    cache_dir = Path(__file__).resolve().parent / "cache" / "models"
    cache_dir.mkdir(parents=True, exist_ok=True)
    for model_id in MODELS:
        print(json.dumps({"event": "loading", "model_id": model_id}), flush=True)
        model = SentenceTransformer(model_id, device="cpu", cache_folder=str(cache_dir))
        dimensions = model.get_sentence_embedding_dimension()
        print(
            json.dumps(
                {
                    "event": "loaded",
                    "model_id": model_id,
                    "max_seq_length": model.max_seq_length,
                    "dimensions": dimensions,
                }
            ),
            flush=True,
        )
        del model


if __name__ == "__main__":
    main()
