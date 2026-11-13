from rag.compliance.documents import ExtractedPage
from rag.compliance.ingestion import CorpusDocument
from rag.compliance.scoping import apply_corpus_scope


def _document(name: str) -> CorpusDocument:
    return CorpusDocument(
        file=name,
        title="Test statute",
        issuing_body="FBR",
        document_type="statute",
        source_url="https://example.test/statute",
        effective_date=None,
        consolidation_date=None,
        retrieved_at=None,
        content_sha256="a" * 64,
        scope_note="Test only.",
        is_active=True,
    )


def _text(pages: tuple[ExtractedPage, ...]) -> str:
    return "\n".join(page.text for page in pages)


def test_companies_act_keeps_only_approved_parts_and_sections():
    contents = (
        "I\nTABLE OF CONTENTS\nPART I ................................ 1\n"
        "1. False contents entry .............................. 1"
    )
    source = (
        "PART I\n1. Short title\nPart I content.\n"
        "PART II\n20. Other section\nPart II must be excluded.\n"
        "PART IV\n55. Filing\nPart IV content.\n"
        "PART VII\n462. Approved provision\nKeep section 462.\n"
        "473. Last approved provision\nKeep section 473.\n"
        "474. Outside range\nExclude section 474."
    )
    pages = apply_corpus_scope(
        _document("Companies Act 2017, updated 18 Aug 2022 (SECP).pdf"),
        (
            ExtractedPage(page_number=1, text=contents),
            ExtractedPage(page_number=2, text="ISLAMABAD, MAY 31, 2017\nPART I"),
            ExtractedPage(page_number=3, text=source),
        ),
    )
    kept = _text(pages)

    assert "Part I content" in kept
    assert "Part IV content" in kept
    assert "False contents entry" not in kept
    assert "Keep section 462" in kept
    assert "Keep section 473" in kept
    assert "Part II must be excluded" not in kept
    assert "Exclude section 474" not in kept


def test_income_tax_keeps_only_manifest_provisions():
    source = (
        "2. Definitions\n9[(62A) startup definition.\n(63) unrelated definition.\n"
        "154A. Export of services\nExport provision.\n"
        "154B. Other withholding\nExclude this section.\n"
        "First Schedule - Part III______\n10[DIVISION IVA\nApproved export rates.\n"
        "DIVISION IVB\nExclude other division.\n"
        "SECOND SCHEDULE\nExclude other schedule."
    )
    pages = apply_corpus_scope(
        _document("Income Tax Ordinance 2001, amended to 30 Jun 2026 (FBR).pdf"),
        (
            ExtractedPage(
                page_number=1,
                text="TABLE OF CONTENTS\n2. Definitions 1\n154A. Export of services 337",
            ),
            ExtractedPage(
                page_number=2,
                text="1. Short title, extent and commencement. (1) This  Ordinance may be called this Ordinance.",
            ),
            ExtractedPage(page_number=3, text=source),
        ),
    )
    kept = _text(pages)

    assert "startup definition" in kept
    assert "Export provision" in kept
    assert "Approved export rates" in kept
    assert "unrelated definition" not in kept
    assert "Exclude this section" not in kept
    assert "Exclude other division" not in kept
    assert "Exclude other schedule" not in kept


def test_scoping_preserves_original_page_numbers():
    doc = _document("Companies Act 2017, updated 18 Aug 2022 (SECP).pdf")
    pages = apply_corpus_scope(
        doc,
        (
            ExtractedPage(page_number=8, text="PART I\n1. Short title\nText."),
            ExtractedPage(page_number=9, text="2. Interpretation\nMore text."),
        ),
    )

    assert [page.page_number for page in pages] == [8, 9]


def test_finance_act_keeps_income_tax_amendments_only():
    pages = (
        ExtractedPage(1, "2. Amendments of the West Pakistan Motor Vehicles Taxation Act\nExclude motor vehicle tax."),
        ExtractedPage(2, "5. Amendments of the Income Tax Ordinance, 2001\nKeep income tax amendment."),
        ExtractedPage(3, "Continuation of income tax amendment."),
        ExtractedPage(4, "6. Amendments of the Federal Excise Act, 2005\nExclude excise."),
    )
    scoped = apply_corpus_scope(
        _document("Finance Act 2026, gazette of 26 Jun 2026.pdf"), pages
    )
    kept = _text(scoped)
    assert "Keep income tax amendment" in kept
    assert "Continuation of income tax amendment" in kept
    assert "motor vehicle tax" not in kept
    assert "excise" not in kept


def test_finance_act_stops_at_next_heading_on_same_page():
    pages = (
        ExtractedPage(
            1,
            "5. Amendments of the Income Tax Ordinance, 2001\nKeep tax text.\n"
            "6. Amendments of the Federal Excise Act, 2005\nDrop excise text.",
        ),
    )
    scoped = apply_corpus_scope(
        _document("Finance Act 2026, gazette of 26 Jun 2026.pdf"), pages
    )
    assert "Keep tax text" in _text(scoped)
    assert "Drop excise text" not in _text(scoped)
