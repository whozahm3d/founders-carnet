"""Extract searchable page text from corpus PDFs (FR-8, NFR-12, NFR-13)."""

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path

from pypdf import PdfReader


@dataclass(frozen=True, slots=True)
class ExtractedPage:
    page_number: int
    text: str


class NoExtractableTextError(ValueError):
    """Raised when a PDF has no text layer and needs OCR or transcription."""


def extract_pdf_pages(path: Path) -> tuple[ExtractedPage, ...]:
    """Return non-empty page text while retaining the PDF's original page numbers."""
    reader = PdfReader(path)
    pages = tuple(
        ExtractedPage(page_number=page_number, text=(page.extract_text() or "").strip())
        for page_number, page in enumerate(reader.pages, start=1)
    )
    if not any(page.text for page in pages):
        raise NoExtractableTextError(
            f"No text layer in {path.name}; it needs OCR or a reviewed transcription"
        )
    return pages


def cached_pdf_pages(path: Path, cache_dir: Path) -> tuple[ExtractedPage, ...]:
    """Load one-page-per-record extraction cache, rebuilding on PDF hash change."""
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / f"{path.stem}.pages.jsonl"
    if cache_path.is_file():
        try:
            records = [json.loads(line) for line in cache_path.read_text(encoding="utf-8").split("\n") if line]
            page_numbers = [int(record["page_number"]) for record in records]
            if records and page_numbers == list(range(1, len(records) + 1)) and all(record.get("pdf_sha256") == digest for record in records):
                return tuple(ExtractedPage(int(record["page_number"]), record["text"]) for record in records)
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            pass
    pages = extract_pdf_pages(path)
    temp_path = cache_path.with_suffix(cache_path.suffix + ".tmp")
    temp_path.write_text(
        "".join(json.dumps({"pdf_sha256": digest, "page_number": page.page_number, "text": page.text}, ensure_ascii=True) + "\n" for page in pages),
        encoding="utf-8",
    )
    temp_path.replace(cache_path)
    return pages


def extract_text_pages(path: Path) -> tuple[ExtractedPage, ...]:
    """Read an approved reviewed text source as one citation page."""
    text = path.read_text(encoding="utf-8-sig").strip()
    if not text:
        raise NoExtractableTextError(f"No text in {path.name}")
    return (ExtractedPage(page_number=1, text=text),)
