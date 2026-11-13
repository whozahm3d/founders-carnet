"""Hash the manifest's canonical text representation on Windows checkouts."""

from __future__ import annotations

import hashlib

import pytest
from rag.compliance.ingestion import CorpusIntegrityError, verify_corpus_file


def test_crlf_text_copy_matches_lf_manifest_hash(tmp_path) -> None:
    canonical = b"first line\nsecond line\n"
    path = tmp_path / "corpus.txt"
    path.write_bytes(canonical.replace(b"\n", b"\r\n"))

    assert verify_corpus_file(path, hashlib.sha256(canonical).hexdigest()) == hashlib.sha256(
        canonical
    ).hexdigest()


def test_crlf_text_copy_accepts_exact_legacy_raw_hash(tmp_path) -> None:
    raw = b"first line\r\nsecond line\r\n"
    path = tmp_path / "legacy.txt"
    path.write_bytes(raw)

    assert verify_corpus_file(path, hashlib.sha256(raw).hexdigest()) == hashlib.sha256(
        raw
    ).hexdigest()


def test_changed_text_character_does_not_match_manifest_hash(tmp_path) -> None:
    expected = b"first line\nsecond line\n"
    path = tmp_path / "corpus.txt"
    path.write_bytes(b"first line\nsecond Line\n")

    with pytest.raises(CorpusIntegrityError, match="SHA-256 mismatch"):
        verify_corpus_file(path, hashlib.sha256(expected).hexdigest())


def test_pdf_hash_uses_raw_bytes(tmp_path) -> None:
    raw_pdf_bytes = b"%PDF-1.7\r\ncontent\r\n%%EOF\r\n"
    path = tmp_path / "corpus.pdf"
    path.write_bytes(raw_pdf_bytes)
    raw_hash = hashlib.sha256(raw_pdf_bytes).hexdigest()

    assert verify_corpus_file(path, raw_hash) == raw_hash
    with pytest.raises(CorpusIntegrityError, match="SHA-256 mismatch"):
        verify_corpus_file(path, hashlib.sha256(raw_pdf_bytes.replace(b"\r\n", b"\n")).hexdigest())
