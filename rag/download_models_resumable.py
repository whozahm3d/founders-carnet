"""Sequential, resumable CPU model downloads with BGE-M3 idle timeout."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

MODELS = (
    "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
    "intfloat/multilingual-e5-base",
    "BAAI/bge-m3",
)
ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "rag" / "cache" / "models"
SCRIPTS = ROOT / "rag" / ".venv" / "Scripts"
HUB_CLI = SCRIPTS / "hf.exe"
MODEL_PATTERNS = [
    "*.json",
    "*.safetensors",
    "*.model",
    "*.txt",
    "tokenizer.*",
    "spiece.model",
    "sentencepiece.bpe.model",
    "1_Pooling/*",
    "2_Normalize/*",
]


def emit(**event: object) -> None:
    print(json.dumps(event, ensure_ascii=False), flush=True)


def repo_cache(model_id: str) -> Path:
    return CACHE / ("models--" + model_id.replace("/", "--"))


def progress_bytes(path: Path) -> tuple[int, float]:
    size = 0
    modified = 0.0
    if path.exists():
        for item in path.rglob("*"):
            try:
                if item.is_file():
                    stat = item.stat()
                    size += stat.st_size
                    modified = max(modified, stat.st_mtime)
            except OSError:
                continue
    return size, modified


def run_child(command: list[str], model_id: str, *, idle_timeout: int | None) -> int:
    safe_id = model_id.replace("/", "__")
    attempt = "snapshot" if "-c" in command else "hf-cli"
    out_path = CACHE / f"download-{safe_id}-{attempt}.stdout.log"
    err_path = CACHE / f"download-{safe_id}-{attempt}.stderr.log"
    emit(event="download_attempt", model_id=model_id, method=attempt, resume=True)
    with out_path.open("w", encoding="utf-8") as stdout, err_path.open(
        "w", encoding="utf-8"
    ) as stderr:
        process = subprocess.Popen(command, cwd=ROOT, stdout=stdout, stderr=stderr)
        last_progress = time.monotonic()
        previous = progress_bytes(repo_cache(model_id))
        last_logged = last_progress
        while process.poll() is None:
            time.sleep(20)
            current = progress_bytes(repo_cache(model_id))
            now = time.monotonic()
            if current != previous:
                last_progress = now
                previous = current
                emit(
                    event="download_progress",
                    model_id=model_id,
                    cached_bytes=current[0],
                    method=attempt,
                )
            elif now - last_logged >= 60:
                emit(
                    event="download_waiting",
                    model_id=model_id,
                    cached_bytes=current[0],
                    idle_seconds=int(now - last_progress),
                    method=attempt,
                )
                last_logged = now
            if idle_timeout is not None and now - last_progress >= idle_timeout:
                process.terminate()
                try:
                    process.wait(timeout=15)
                except subprocess.TimeoutExpired:
                    process.kill()
                emit(
                    event="download_skipped_no_progress",
                    model_id=model_id,
                    idle_seconds=idle_timeout,
                    cached_bytes=current[0],
                )
                return 124
        return int(process.returncode or 0)


def download(model_id: str) -> bool:
    code = run_child(
        [
            sys.executable,
            "-c",
            ("from huggingface_hub import snapshot_download; import sys; "
            "import json; print(snapshot_download(sys.argv[1], cache_dir=sys.argv[2], "
            "max_workers=1, allow_patterns=json.loads(sys.argv[3])), flush=True)"),
            model_id,
            str(CACHE),
            json.dumps(MODEL_PATTERNS),
        ],
        model_id,
        idle_timeout=1200 if model_id == "BAAI/bge-m3" else None,
    )
    if code != 0:
        if code == 124:
            return False
        emit(event="snapshot_download_failed", model_id=model_id, exit_code=code)
        code = run_child(
            [
                str(HUB_CLI),
                "download",
                model_id,
                "--cache-dir",
                str(CACHE),
                "--max-workers",
                "1",
                "--include",
                "*.json",
                "*.safetensors",
                "--include",
                "*.model",
                "--include",
                "*.txt",
                "--format",
                "json",
            ],
            model_id,
            idle_timeout=1200 if model_id == "BAAI/bge-m3" else None,
        )
    if code != 0:
        emit(event="download_failed", model_id=model_id, exit_code=code)
        return False
    return True


def inspect_model(model_id: str) -> bool:
    from sentence_transformers import SentenceTransformer

    emit(event="loading_local_model", model_id=model_id)
    model = SentenceTransformer(model_id, device="cpu", cache_folder=str(CACHE))
    from rag.evaluation.evaluate import load_corpus_chunks

    chunks = load_corpus_chunks()
    maximum = int(model.max_seq_length)
    tokenizer = model.tokenizer
    prefix = "passage: " if model_id == "intfloat/multilingual-e5-base" else ""
    exceeds = sum(
        len(tokenizer(prefix + chunk.text, add_special_tokens=True, truncation=False)["input_ids"])
        > maximum
        for chunk in chunks
    )
    emit(
        event="model_ready",
        model_id=model_id,
        max_seq_length=maximum,
        vector_dimension=model.get_sentence_embedding_dimension(),
        chunk_count=len(chunks),
        chunks_exceeding_limit=exceeds,
    )
    del model
    return True


def main() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    for model_id in MODELS:
        emit(event="model_start", model_id=model_id)
        if not download(model_id):
            if model_id == "BAAI/bge-m3":
                continue
            continue
        try:
            inspect_model(model_id)
        except Exception as exc:  # noqa: BLE001 - log and continue to the next approved model
            emit(
                event="model_inspection_failed",
                model_id=model_id,
                error_type=type(exc).__name__,
                error=str(exc),
            )


if __name__ == "__main__":
    main()
