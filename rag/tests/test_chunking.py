from rag.compliance.documents import ExtractedPage
from rag.compliance.ingestion import CorpusDocument
from rag.compliance.chunking import chunk_pages


def test_chunks_keep_sections_page_numbers_and_citation_metadata():
    document = CorpusDocument(
        file="sample.pdf",
        title="Sample Act",
        issuing_body="SECP",
        document_type="statute",
        source_url="https://example.test/sample",
        effective_date="2026-06-30",
        consolidation_date=None,
        retrieved_at=None,
        content_sha256="a" * 64,
        scope_note="Sections 1 and 2 only.",
        is_active=True,
    )
    pages = (
        ExtractedPage(
            page_number=7,
            text=(
                "Section 1. Short title\nThis Act may be called the Sample Act.\n"
                "Section 2. Definitions\nIn this Act, the terms have the meanings below."
            ),
        ),
    )

    chunks = chunk_pages(document, pages, max_chars=500, overlap_chars=40)

    assert [chunk.section for chunk in chunks] == ["1", "2"]
    assert all(chunk.page_number == 7 for chunk in chunks)
    assert all(chunk.document_title == "Sample Act" for chunk in chunks)
    assert all(chunk.issuing_body == "SECP" for chunk in chunks)
    assert all(chunk.effective_date == "2026-06-30" for chunk in chunks)
    assert all(chunk.source_sha256 == "a" * 64 for chunk in chunks)
    assert "Short title" in chunks[0].text
    assert "Definitions" in chunks[1].text
