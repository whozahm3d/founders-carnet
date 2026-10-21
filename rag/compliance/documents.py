"""Extract searchable page text from corpus PDFs (FR-8, NFR-12, NFR-13)."""

from dataclasses import dataclass
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
        ExtractedPage(page_number=page_number, text=text)
        for page_number, page in enumerate(reader.pages, start=1)
        if (text := (page.extract_text() or "").strip())
    )
    if not pages:
        raise NoExtractableTextError(
            f"No text layer in {path.name}; it needs OCR or a reviewed transcription"
        )
    return pages
