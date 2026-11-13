import hashlib

from rag.compliance import documents
from rag.compliance.documents import ExtractedPage, cached_pdf_pages


def test_cache_rebuilds_when_pdf_hash_changes(tmp_path, monkeypatch):
    source = tmp_path / "sample.pdf"
    source.write_bytes(b"first pdf")
    extracted = []

    def fake_extract(path):
        extracted.append(path.read_bytes())
        return (ExtractedPage(1, path.read_bytes().decode("ascii")),)

    monkeypatch.setattr(documents, "extract_pdf_pages", fake_extract)
    cache = tmp_path / "cache"
    assert cached_pdf_pages(source, cache)[0].text == "first pdf"
    assert cached_pdf_pages(source, cache)[0].text == "first pdf"
    source.write_bytes(b"second pdf")
    assert cached_pdf_pages(source, cache)[0].text == "second pdf"
    assert extracted == [b"first pdf", b"second pdf"]
    record = (cache / "sample.pages.jsonl").read_text(encoding="utf-8")
    assert hashlib.sha256(b"second pdf").hexdigest() in record


def test_cache_keeps_blank_pages_as_page_records(tmp_path, monkeypatch):
    source = tmp_path / "pages.pdf"
    source.write_bytes(b"source")
    monkeypatch.setattr(
        documents,
        "extract_pdf_pages",
        lambda _: (ExtractedPage(1, ""), ExtractedPage(2, "visible")),
    )
    pages = cached_pdf_pages(source, tmp_path / "cache")
    assert [(page.page_number, page.text) for page in pages] == [(1, ""), (2, "visible")]
