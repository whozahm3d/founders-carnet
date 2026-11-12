import itertools

from rag.compliance.chunking import chunk_pages
from rag.compliance.documents import ExtractedPage
from rag.compliance.ingestion import CorpusDocument


def _document() -> CorpusDocument:
    return CorpusDocument(
        file="sample.pdf",
        title="Sample Act",
        issuing_body="SECP",
        document_type="statute",
        source_url="https://example.test/sample",
        effective_date="2026-06-30",
        consolidation_date=None,
        retrieved_at=None,
        content_sha256="a" * 64,
        scope_note="Test source.",
        is_active=True,
    )


def test_numbered_list_items_do_not_start_new_sections():
    pages = (
        ExtractedPage(
            page_number=4,
            text=(
                "Section 3. Duties\n"
                "1. first requirement\n"
                "2. second requirement"
            ),
        ),
    )

    chunks = chunk_pages(_document(), pages)

    assert len(chunks) == 1
    assert chunks[0].section == "3"


def test_long_section_splits_with_overlap_without_exceeding_limit():
    long_text = "Section 4. Requirements\n" + "requirement detail " * 30
    pages = (ExtractedPage(page_number=9, text=long_text),)

    chunks = chunk_pages(_document(), pages, max_chars=100, overlap_chars=20)

    assert len(chunks) > 1
    assert all(len(chunk.text) <= 100 for chunk in chunks)
    assert all(chunk.section == "4" for chunk in chunks)
    assert any(
        set(first.text.split()) & set(second.text.split())
        for first, second in itertools.pairwise(chunks)
    )
