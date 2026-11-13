"""Starter-set loader, deterministic split, and CSV evaluation harness."""

from __future__ import annotations

import csv
import json
import random
import argparse
import math
from datetime import date
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import numpy as np

from rag.compliance.chunking import chunk_pages, split_chunks_for_model
from rag.compliance.documents import ExtractedPage, cached_pdf_pages
from rag.compliance.embeddings import SentenceTransformerEncoder
from rag.compliance.ingestion import parse_manifest, verify_corpus_file
from rag.compliance.retrieve import RetrievedChunk, bm25, hybrid
from rag.compliance.scoping import apply_corpus_scope

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
SEED = 42
MODEL_IDS = (
    "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
    "intfloat/multilingual-e5-base",
    "BAAI/bge-m3",
)
RETRIEVERS = {"dense": None, "bm25": bm25, "hybrid": hybrid}


@dataclass(frozen=True)
class GoldQuestion:
    id: str
    question: str
    relevant_chunk_ids: tuple[str, ...]
    should_abstain: bool | None
    expected_effective_date: str | None
    split: str | None = None


def load_questions(path: Path = ROOT / "gold_questions.jsonl") -> tuple[GoldQuestion, ...]:
    questions: list[GoldQuestion] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        raw = json.loads(line)
        if {"supporting_chunk_ids", "answerable"} <= raw.keys():
            relevant_chunk_ids = raw["supporting_chunk_ids"]
            should_abstain = not bool(raw["answerable"])
        elif {"relevant_chunk_ids", "should_abstain"} <= raw.keys():
            relevant_chunk_ids = raw["relevant_chunk_ids"]
            should_abstain = raw["should_abstain"]
        elif {"answerable", "supporting_sections"} <= raw.keys():
            # Preserve the repository's pre-existing human-authored question set.
            # Section labels are not chunk IDs, so retrieval scoring remains gated
            # until a reviewed chunk mapping is added.
            relevant_chunk_ids = []
            should_abstain = not bool(raw["answerable"])
        else:
            raise ValueError(
                f"{path}:{line_number}: expected chunk labels or answerable/supporting_sections"
            )
        if not raw.get("question", "").strip() or should_abstain is None:
            continue
        questions.append(
            GoldQuestion(
                id=str(raw["id"]),
                question=str(raw["question"]),
                relevant_chunk_ids=tuple(relevant_chunk_ids),
                should_abstain=should_abstain,
                expected_effective_date=raw.get("expected_effective_date"),
                split=raw.get("split"),
            )
        )
    return tuple(questions)


def split_dev_test(
    questions: tuple[GoldQuestion, ...], seed: int = SEED
) -> tuple[tuple[GoldQuestion, ...], tuple[GoldQuestion, ...]]:
    if questions and all(question.split in {"dev", "test"} for question in questions):
        return (
            tuple(question for question in questions if question.split == "dev"),
            tuple(question for question in questions if question.split == "test"),
        )
    rows = list(questions)
    random.Random(seed).shuffle(rows)
    if len(rows) < 2:
        return tuple(rows), ()
    dev_size = max(1, int(len(rows) * 0.8))
    return tuple(rows[:dev_size]), tuple(rows[dev_size:])


def write_empty_csvs(model_ids: tuple[str, ...] | None = None) -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    headers: dict[str, list[str]] = {
        "retrieval.csv": ["model_id", "retriever", "split", "query_id", "relevant_count", "recall_at_5", "reciprocal_rank", "top_score", "abstention_threshold", "abstained", "should_abstain", "status"],
        "e2e.csv": ["variant", "query_id", "citation_correct", "unsupported_claim_rate", "abstained", "should_abstain", "date_correct", "latency_ms", "failure_cause", "status"],
        "split_sizes.csv": ["seed", "dev_count", "test_count", "complete_question_count", "starter_count"],
        "run_metadata.csv": ["run_date", "corpus_hashes", "model_ids", "status", "not_run_reason"],
        "test_cases.csv": ["id", "test", "requirement", "status", "actual_result"],
        "failure_causes.csv": ["failure_cause", "count"],
    }
    questions = load_questions()
    dev, test = split_dev_test(questions)
    with (RESULTS / "split_sizes.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(headers["split_sizes.csv"])
        writer.writerow([SEED, len(dev), len(test), len(questions), len(questions)])
    manifest = (ROOT.parent / "corpus_manifest.md").read_text(encoding="utf-8")
    import re
    hashes = ";".join(
        f"{filename}:{digest}"
        for filename, digest in re.findall(
            r"\| `([^`]+)` \|[^\n]*?`([0-9a-f]{64})`", manifest
        )
    )
    selected_model_ids = ";".join(model_ids if model_ids is not None else MODEL_IDS)
    with (RESULTS / "run_metadata.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(headers["run_metadata.csv"])
        writer.writerow([date.today().isoformat(), hashes, selected_model_ids, "dev_only_pending", "User-confirmed chunk mappings are recorded. No Gemini or end-to-end baseline run. No conflict-handling measurement. Section 65F not indexed. PSEB has only 2 chunks, making q012 a weak retrieval test. Test split is held out."])
    for name, fields in headers.items():
        if name in {"split_sizes.csv", "run_metadata.csv"}:
            continue
        with (RESULTS / name).open("w", newline="", encoding="utf-8") as stream:
            csv.writer(stream).writerow(fields)


def recall_mrr(ranked_ids: list[str], relevant_ids: tuple[str, ...], k: int = 5) -> tuple[float, float]:
    if not relevant_ids:
        raise ValueError("Question has no relevant chunk labels")
    relevant = set(relevant_ids)
    top = ranked_ids[:k]
    recall = len(relevant.intersection(top)) / len(relevant)
    reciprocal_rank = next((1.0 / rank for rank, item in enumerate(ranked_ids, 1) if item in relevant), 0.0)
    return recall, reciprocal_rank


def load_corpus_chunks() -> tuple[Any, ...]:
    """Load only manifested active PDFs and reviewed TXT sources; never read HTML."""
    repository = ROOT.parents[1]
    data_dir = repository / "rag" / "data"
    cache_dir = repository / "rag" / "cache"
    documents = parse_manifest((repository / "rag" / "corpus_manifest.md").read_text(encoding="utf-8"))
    chunks = []
    for document in documents:
        if not document.is_active or document.file.lower().endswith(".html"):
            continue
        path = data_dir / document.file
        verify_corpus_file(path, document.content_sha256)
        if path.suffix.lower() == ".pdf":
            pages = cached_pdf_pages(path, cache_dir)
        elif path.suffix.lower() == ".txt":
            text = path.read_text(encoding="utf-8").strip()
            pages = (ExtractedPage(1, text),) if text else ()
        else:
            continue
        scoped = apply_corpus_scope(document, pages)
        chunks.extend(chunk_pages(document, scoped))
    return tuple(chunks)


def _canonical_chunk_id(chunk_id: str) -> str:
    return chunk_id.rsplit(":continuation-", 1)[0]


def _numpy_dense(
    query_embedding: tuple[float, ...] | list[float],
    chunks: tuple[Any, ...] | list[Any],
    *,
    top_k: int = 8,
    minimum_score: float = 0.0,
) -> tuple[RetrievedChunk, ...]:
    """In-memory cosine retrieval using normalized NumPy vectors."""
    if not chunks:
        return ()
    query = np.asarray(query_embedding, dtype=np.float32)
    query_norm = np.linalg.norm(query)
    if query_norm == 0:
        return ()
    query = query / query_norm
    valid = [(chunk, getattr(chunk, "embedding", None)) for chunk in chunks]
    valid = [(chunk, vector) for chunk, vector in valid if vector is not None]
    if not valid:
        return ()
    matrix = np.asarray([vector for _, vector in valid], dtype=np.float32)
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0] = 1
    scores = (matrix / norms) @ query
    ranked = [
        RetrievedChunk(chunk, float(score), "dense")
        for (chunk, _), score in zip(valid, scores, strict=True)
        if float(score) >= minimum_score
    ]
    ranked.sort(key=lambda item: (-item.score, item.chunk.id))
    return tuple(ranked[:top_k])


def _tune_abstention_threshold(
    scores: dict[str, float], should_abstain: dict[str, bool]
) -> float:
    """Select the dev threshold maximizing balanced accuracy; lower wins ties."""
    candidates = {0.0, 1.0}
    for score in scores.values():
        candidates.add(max(0.0, min(1.0, score)))
        candidates.add(math.nextafter(max(0.0, min(1.0, score)), math.inf))
    positives = sum(not value for value in should_abstain.values())
    negatives = sum(should_abstain.values())
    best_threshold = 0.0
    best_metric = -1.0
    for threshold in sorted(candidates):
        true_positive = sum(
            not should_abstain[qid] and scores[qid] >= threshold for qid in scores
        )
        true_negative = sum(
            should_abstain[qid] and scores[qid] < threshold for qid in scores
        )
        sensitivity = true_positive / positives if positives else 0.0
        specificity = true_negative / negatives if negatives else 0.0
        balanced_accuracy = (sensitivity + specificity) / 2
        if balanced_accuracy > best_metric:
            best_metric = balanced_accuracy
            best_threshold = threshold
    return best_threshold


def _encode_passages_batched(encoder: SentenceTransformerEncoder, texts: list[str]) -> tuple[tuple[float, ...], ...]:
    vectors: list[tuple[float, ...]] = []
    for offset in range(0, len(texts), 16):
        vectors.extend(encoder.encode_passages(texts[offset : offset + 16]))
    return tuple(vectors)


def _chunk_token_limit(model_id: str, model: Any) -> int:
    """Reserve room for the E5 passage prefix before splitting source chunks."""
    maximum = int(model.max_seq_length)
    if model_id.startswith("intfloat/multilingual-e5"):
        prefix_tokens = len(
            model.tokenizer("passage: ", add_special_tokens=False)["input_ids"]
        )
        maximum -= prefix_tokens
    return maximum


def run_retrieval(
    questions: tuple[GoldQuestion, ...],
    *,
    model_ids: tuple[str, ...],
) -> None:
    dev, _test = split_dev_test(questions)
    answerable_dev = tuple(question for question in dev if question.relevant_chunk_ids)
    if not answerable_dev:
        print("Retrieval comparison not run: dev split has no labeled relevant chunks.")
        return

    base_chunks = load_corpus_chunks()
    rows: list[dict[str, object]] = []
    dev_by_id = {question.id: question for question in dev}
    for model_id in model_ids:
        encoder = SentenceTransformerEncoder(model_id)
        model = encoder._load_model()
        model_chunks = split_chunks_for_model(
            base_chunks,
            model.tokenizer,
            _chunk_token_limit(model_id, model),
        )
        vectors = _encode_passages_batched(encoder, [chunk.text for chunk in model_chunks])
        embedded = tuple(
            SimpleNamespace(id=index, chunk_id=chunk.chunk_id, text=chunk.text, embedding=vector)
            for index, (chunk, vector) in enumerate(zip(model_chunks, vectors, strict=True))
        )
        per_retriever: dict[str, dict[str, tuple[float, tuple[RetrievedChunk, ...]]]] = {
            name: {} for name in RETRIEVERS
        }
        for question in dev:
            vector = encoder.encode_query([question.question])[0]
            for retriever_name in RETRIEVERS:
                if retriever_name == "bm25":
                    ranked = bm25(question.question, embedded, top_k=5)
                elif retriever_name == "dense":
                    ranked = _numpy_dense(vector, embedded, top_k=5)
                else:
                    ranked = hybrid(
                        question.question,
                        vector,
                        embedded,
                        top_k=5,
                        rrf_k=60,
                        dense_retriever=_numpy_dense,
                    )
                per_retriever[retriever_name][question.id] = (
                    ranked[0].similarity if ranked else 0.0,
                    ranked,
                )
        for retriever_name, results_by_question in per_retriever.items():
            score_map = {qid: value[0] for qid, value in results_by_question.items()}
            labels = {qid: question.should_abstain is True for qid, question in dev_by_id.items()}
            threshold = _tune_abstention_threshold(score_map, labels)
            for question in dev:
                top_score, ranked = results_by_question[question.id]
                relevant = tuple(_canonical_chunk_id(item) for item in question.relevant_chunk_ids)
                recall, reciprocal_rank = (
                    recall_mrr(
                        [_canonical_chunk_id(item.chunk.chunk_id) for item in ranked],
                        relevant,
                    )
                    if relevant
                    else ("", "")
                )
                rows.append(
                    {
                        "model_id": model_id,
                        "retriever": retriever_name,
                        "split": "dev",
                        "query_id": question.id,
                        "relevant_count": len(set(relevant)),
                        "recall_at_5": recall,
                        "reciprocal_rank": reciprocal_rank,
                        "top_score": round(top_score, 6),
                        "abstention_threshold": round(threshold, 6),
                        "abstained": top_score < threshold,
                        "should_abstain": question.should_abstain,
                        "status": "dev_threshold_tuning",
                    }
                )
    with (RESULTS / "retrieval.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=["model_id", "retriever", "split", "query_id", "relevant_count", "recall_at_5", "reciprocal_rank", "top_score", "abstention_threshold", "abstained", "should_abstain", "status"])
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-id", action="append", choices=MODEL_IDS, required=True)
    args = parser.parse_args()
    write_empty_csvs(tuple(dict.fromkeys(args.model_id)))
    questions = load_questions()
    complete = len(questions)
    print(f"Loaded {complete} existing question records; no gold answers were generated.")
    print(f"Wrote CSV headers and fixed-seed split counts to {RESULTS}.")
    if complete:
        run_retrieval(questions, model_ids=tuple(dict.fromkeys(args.model_id)))
