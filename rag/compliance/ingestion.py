"""Read corpus provenance and verify source files before indexing.

FR-8, NFR-12, NFR-13, NFR-14.
"""

from __future__ import annotations

import csv
import hashlib
import hmac
import re
from dataclasses import dataclass
from pathlib import Path

_REQUIRED_COLUMNS = (
    "file",
    "title",
    "issuing_body",
    "document_type",
    "source_url",
    "effective_date",
    "consolidation_date",
    "retrieved_at",
    "content_sha256",
    "scope_note",
    "is_active",
)
_SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")


@dataclass(frozen=True, slots=True)
class CorpusDocument:
    file: str
    title: str
    issuing_body: str
    document_type: str
    source_url: str
    effective_date: str | None
    consolidation_date: str | None
    retrieved_at: str | None
    content_sha256: str
    scope_note: str
    is_active: bool


class CorpusIntegrityError(ValueError):
    """Raised when a source is missing or differs from its manifest hash."""


def parse_manifest(contents: str) -> list[CorpusDocument]:
    """Parse the pipe-delimited corpus table from ``corpus_manifest.md``."""
    headers: list[str] | None = None
    documents: list[CorpusDocument] = []

    for line in contents.splitlines():
        if not line.strip().startswith("|"):
            continue

        cells = next(csv.reader([line.strip().strip("|")], delimiter="|"))
        cells = [cell.strip() for cell in cells]
        if not cells or all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue

        if headers is None:
            headers = [cell.lower() for cell in cells]
            missing = set(_REQUIRED_COLUMNS) - set(headers)
            if missing:
                raise ValueError(f"Manifest is missing columns: {', '.join(sorted(missing))}")
            continue

        if len(cells) != len(headers):
            raise ValueError("Manifest row has a different number of cells than its header")

        row = dict(zip(headers, cells, strict=True))
        active_value = _clean_cell(row["is_active"]).lower()
        if active_value not in {"true", "false"}:
            raise ValueError(f"Invalid is_active value for {row['file']!r}")

        documents.append(
            CorpusDocument(
                file=_clean_cell(row["file"]),
                title=_clean_cell(row["title"]),
                issuing_body=_clean_cell(row["issuing_body"]),
                document_type=_clean_cell(row["document_type"]),
                source_url=_clean_url(row["source_url"]),
                effective_date=_optional_cell(row["effective_date"]),
                consolidation_date=_optional_cell(row["consolidation_date"]),
                retrieved_at=_optional_cell(row["retrieved_at"]),
                content_sha256=_clean_cell(row["content_sha256"]).lower(),
                scope_note=_clean_cell(row["scope_note"]),
                is_active=active_value == "true",
            )
        )

    if headers is None:
        raise ValueError("Manifest table was not found")
    return documents


def verify_corpus_file(path: Path, expected_sha256: str) -> str:
    """Return the file hash, raising if the source is absent or has changed."""
    expected = expected_sha256.lower()
    if not _SHA256_PATTERN.fullmatch(expected):
        raise ValueError("Expected SHA-256 must contain 64 hexadecimal characters")
    if not path.is_file():
        raise CorpusIntegrityError(f"Corpus file not found: {path.name}")

    with path.open("rb") as source:
        actual = hashlib.file_digest(source, "sha256").hexdigest()

    if not hmac.compare_digest(actual, expected):
        raise CorpusIntegrityError(
            f"SHA-256 mismatch for {path.name}: expected {expected}, got {actual}"
        )
    return actual


def _clean_cell(value: str) -> str:
    return value.strip().strip("`").strip()


def _clean_url(value: str) -> str:
    return _clean_cell(value).removeprefix("<").removesuffix(">").strip()


def _optional_cell(value: str) -> str | None:
    cleaned = _clean_cell(value)
    return cleaned or None
