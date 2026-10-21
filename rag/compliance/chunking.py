"""Build citation-ready, section-aware text chunks (FR-8, NFR-12, NFR-14)."""

from __future__ import annotations

import re
from dataclasses import dataclass

from rag.compliance.documents import ExtractedPage
from rag.compliance.ingestion import CorpusDocument

_SECTION_HEADING = re.compile(
    r"^\s*(?:(?i:section)\s+)?(?P<section>\d+[A-Z]?(?:\([0-9A-Z]+\))*)"
    r"(?:[.):])\s+(?P<title>[A-Z][^\n]{2,})\s*$",
)


@dataclass(frozen=True, slots=True)
class CitationChunk:
    chunk_id: str
    document_file: str
    document_title: str
    issuing_body: str
    document_type: str
    source_url: str
    effective_date: str | None
    consolidation_date: str | None
    retrieved_at: str | None
    source_sha256: str
    page_number: int
    section: str | None
    text: str


def chunk_pages(
    document: CorpusDocument,
    pages: tuple[ExtractedPage, ...],
    *,
    max_chars: int = 1200,
    overlap_chars: int = 150,
) -> tuple[CitationChunk, ...]:
    """Split pages at section headings and attach source metadata to each chunk."""
    if max_chars < 1:
        raise ValueError("max_chars must be positive")
    if overlap_chars < 0 or overlap_chars >= max_chars:
        raise ValueError("overlap_chars must be between zero and max_chars")

    chunks: list[CitationChunk] = []
    for page in pages:
        section_segments = _split_page_sections(page.text)
        page_chunk_number = 0
        for section, text in section_segments:
            for chunk_text in _split_text(text, max_chars, overlap_chars):
                chunks.append(
                    CitationChunk(
                        chunk_id=f"{document.file}:{page.page_number}:{page_chunk_number}",
                        document_file=document.file,
                        document_title=document.title,
                        issuing_body=document.issuing_body,
                        document_type=document.document_type,
                        source_url=document.source_url,
                        effective_date=document.effective_date,
                        consolidation_date=document.consolidation_date,
                        retrieved_at=document.retrieved_at,
                        source_sha256=document.content_sha256,
                        page_number=page.page_number,
                        section=section,
                        text=chunk_text,
                    )
                )
                page_chunk_number += 1
    return tuple(chunks)


def _split_page_sections(text: str) -> list[tuple[str | None, str]]:
    segments: list[tuple[str | None, str]] = []
    current_section: str | None = None
    current_lines: list[str] = []

    for line in text.splitlines():
        heading = _SECTION_HEADING.match(line)
        if heading:
            _append_segment(segments, current_section, current_lines)
            current_section = heading.group("section")
            current_lines = [line.strip()]
        elif line.strip():
            current_lines.append(line.strip())
        elif current_lines and current_lines[-1] != "":
            current_lines.append("")

    _append_segment(segments, current_section, current_lines)
    return segments


def _append_segment(
    segments: list[tuple[str | None, str]],
    section: str | None,
    lines: list[str],
) -> None:
    text = "\n".join(lines).strip()
    if text:
        segments.append((section, text))


def _split_text(text: str, max_chars: int, overlap_chars: int) -> tuple[str, ...]:
    remaining = text.strip()
    chunks: list[str] = []

    while len(remaining) > max_chars:
        split_at = remaining.rfind(" ", 0, max_chars + 1)
        if split_at < max_chars // 2:
            split_at = max_chars
        chunks.append(remaining[:split_at].strip())
        next_start = split_at
        if overlap_chars:
            next_start = max(0, split_at - overlap_chars)
            while next_start > 0 and not remaining[next_start - 1].isspace():
                next_start -= 1
        remaining = remaining[next_start:].strip()

    if remaining:
        chunks.append(remaining)
    return tuple(chunks)
