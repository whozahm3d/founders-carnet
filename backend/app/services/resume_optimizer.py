"""Private PDF storage and text extraction for resume suggestions (FR-5, NFR-7)."""

from __future__ import annotations

import hashlib
import io
import re
import uuid
from pathlib import Path

from pypdf import PdfReader

from app.config import _REPOSITORY_ROOT, get_settings


MAX_RESUME_BYTES = 5 * 1024 * 1024
MAX_RESUME_PAGES = 20
MAX_RESUME_TEXT_CHARS = 30_000
MAX_RESUME_LINES = 120
MAX_PAGE_CONTENT_STREAM_BYTES = 2_000_000
_STORAGE_KEY_PATTERN = re.compile(r"^[a-f0-9]{32}$")


class ResumeFileError(ValueError):
    """A PDF is invalid, unsupported, or cannot be safely processed."""


def extract_resume_lines(content: bytes) -> list[str]:
    try:
        reader = PdfReader(io.BytesIO(content), strict=False)
        if reader.is_encrypted:
            raise ResumeFileError("Password-protected PDFs are not supported")
        if not 1 <= len(reader.pages) <= MAX_RESUME_PAGES:
            raise ResumeFileError("PDF must contain between 1 and 20 pages")

        extracted_pages: list[str] = []
        for page in reader.pages:
            content_stream = page.get_contents()
            if content_stream is not None and len(content_stream.get_data()) > MAX_PAGE_CONTENT_STREAM_BYTES:
                raise ResumeFileError("PDF page is too complex to process")
            extracted_pages.append(page.extract_text() or "")
    except ResumeFileError:
        raise
    except Exception as exc:
        raise ResumeFileError("PDF could not be read") from exc

    text = "\n".join(extracted_pages)
    if len(text) > MAX_RESUME_TEXT_CHARS:
        raise ResumeFileError("Extracted resume text exceeds the processing limit")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        raise ResumeFileError("No selectable text found; scanned PDFs are not supported")
    if len(lines) > MAX_RESUME_LINES:
        raise ResumeFileError("Resume contains too many lines to process")
    return lines


def store_resume_pdf(content: bytes) -> tuple[str, str]:
    root = _private_storage_root()
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    storage_key = uuid.uuid4().hex
    destination = root / f"{storage_key}.pdf"
    if destination.resolve().parent != root:
        raise RuntimeError("Invalid private storage path")
    try:
        with destination.open("xb") as resume_file:
            resume_file.write(content)
    except OSError:
        destination.unlink(missing_ok=True)
        raise
    return storage_key, hashlib.sha256(content).hexdigest()


def delete_resume_pdf(storage_key: str) -> None:
    if not _STORAGE_KEY_PATTERN.fullmatch(storage_key):
        raise RuntimeError("Invalid private storage key")
    root = _private_storage_root()
    destination = root / f"{storage_key}.pdf"
    if destination.resolve().parent != root:
        raise RuntimeError("Invalid private storage path")
    destination.unlink(missing_ok=True)


def _private_storage_root() -> Path:
    root = get_settings().resume_storage_dir.expanduser().resolve()
    private_base = (_REPOSITORY_ROOT / "backend" / ".private").resolve()
    served_directory = (_REPOSITORY_ROOT / "frontend" / "public").resolve()
    if (
        root == served_directory
        or served_directory in root.parents
        or (root.is_relative_to(_REPOSITORY_ROOT.resolve()) and not root.is_relative_to(private_base))
    ):
        raise RuntimeError("Resume storage must be private and outside served source directories")
    return root
