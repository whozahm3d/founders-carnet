"""Corpus provenance checks for the compliance assistant (FR-8)."""

import hashlib
from pathlib import Path

import pytest
from rag.compliance.ingestion import (
    CorpusIntegrityError,
    parse_manifest,
    verify_corpus_file,
)


def test_parse_manifest_preserves_source_and_citation_metadata():
    manifest = """\
| file | title | issuing_body | document_type | source_url | effective_date | consolidation_date | retrieved_at | content_sha256 | scope_note | is_active |
|---|---|---|---|---|---|---|---|---|---|---|
| `sample.pdf` | Sample Act | SECP | statute | <https://example.test/sample> | 2026-06-30 |  |  | `abc123` | Sections 1 to 3 only. | true |
"""

    documents = parse_manifest(manifest)

    assert len(documents) == 1
    assert documents[0].file == "sample.pdf"
    assert documents[0].title == "Sample Act"
    assert documents[0].issuing_body == "SECP"
    assert documents[0].source_url == "https://example.test/sample"
    assert documents[0].effective_date == "2026-06-30"
    assert documents[0].scope_note == "Sections 1 to 3 only."
    assert documents[0].is_active is True


def test_verify_corpus_file_accepts_matching_hash(tmp_path: Path):
    corpus_file = tmp_path / "sample.txt"
    corpus_file.write_text("official source text", encoding="utf-8")
    expected_hash = hashlib.sha256(corpus_file.read_bytes()).hexdigest()

    verify_corpus_file(corpus_file, expected_hash)


def test_verify_corpus_file_rejects_changed_source(tmp_path: Path):
    corpus_file = tmp_path / "sample.txt"
    corpus_file.write_text("changed source text", encoding="utf-8")

    with pytest.raises(CorpusIntegrityError, match="SHA-256 mismatch"):
        verify_corpus_file(corpus_file, "0" * 64)
