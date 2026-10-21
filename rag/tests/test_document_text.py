from pathlib import Path

import pytest

from rag.compliance.documents import NoExtractableTextError, extract_pdf_pages


RAG_ROOT = Path(__file__).resolve().parents[1]


def test_extract_pdf_pages_keeps_original_page_numbers():
    pdf_path = RAG_ROOT / "data" / "Registration of Individual on Iris, 25 May 2019 (FBR).pdf"

    pages = extract_pdf_pages(pdf_path)

    assert len(pages) == 6
    assert pages[0].page_number == 1
    normalized_text = " ".join(pages[0].text.upper().split())
    assert "REGISTRATION OF INDIVIDUAL ON IRIS" in normalized_text


def test_extract_pdf_pages_rejects_scanned_source_without_ocr():
    pdf_path = RAG_ROOT / "data" / "Virtual One Stop Shop circular, 27 Mar 2018 (FBR).pdf"

    with pytest.raises(NoExtractableTextError, match="OCR or a reviewed transcription"):
        extract_pdf_pages(pdf_path)
