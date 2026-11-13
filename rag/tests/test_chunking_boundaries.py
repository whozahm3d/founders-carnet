from rag.compliance.chunking import chunk_pages, clean_document_pages, split_chunks_for_model
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


def test_long_section_repeats_title_and_keeps_heading_path():
    long_text = (
        "PART IV\nCHAPTER I\nSection 4. Requirements\n"
        + "\n".join(f"({i}) requirement detail for clause {i}." for i in range(1, 9))
    )
    pages = (ExtractedPage(page_number=9, text=long_text),)

    chunks = chunk_pages(_document(), pages, target_tokens=22)

    assert len(chunks) > 1
    assert all(chunk.section == "4" for chunk in chunks)
    assert all(chunk.heading_path[:2] == ("PART IV", "CHAPTER I") for chunk in chunks)
    assert all("Section 4 - Requirements" in chunk.heading_path for chunk in chunks)
    assert all(chunk.heading_path[-1].startswith("Subsections") for chunk in chunks)
    assert all(chunk.text.startswith("Section 4 - Requirements") for chunk in chunks)
    assert all(chunk.token_count > 0 for chunk in chunks)


def test_oversized_numbered_clause_is_kept_whole():
    clause = "(1) " + "important obligation " * 40
    pages = (
        ExtractedPage(
            page_number=12,
            text=f"Section 5. Obligations\n{clause}\n(2) final clause.",
        ),
    )

    chunks = chunk_pages(_document(), pages, target_tokens=12)

    clause_chunks = [chunk for chunk in chunks if "important obligation" in chunk.text]
    assert len(clause_chunks) == 1
    assert clause_chunks[0].text.count("important obligation") == 40
    assert clause_chunks[0].heading_path[-1] == "Subsection (1)"
    assert clause_chunks[0].token_count > 12


def test_model_safe_split_repeats_section_title_and_respects_maximum():
    class Tokenizer:
        def __call__(self, text, *, add_special_tokens, truncation, return_offsets_mapping=False):
            matches = list(__import__("re").finditer(r"\S+", text))
            data = {"input_ids": list(range(len(matches) + (2 if add_special_tokens else 0)))}
            if return_offsets_mapping:
                data["offset_mapping"] = [(item.start(), item.end()) for item in matches]
            return data

    clause = "(1) " + "word " * 30
    chunk = chunk_pages(
        _document(),
        (ExtractedPage(1, "Section 5. Obligations\n" + clause),),
        target_tokens=100,
    )[0]

    split = split_chunks_for_model((chunk,), Tokenizer(), max_seq_length=12)

    assert len(split) > 1
    assert all("Section 5 - Obligations" in item.text for item in split)
    assert all(item.token_count <= 12 for item in split)
    assert all(item.heading_path[-1].startswith("Continuation") for item in split)
    assert "".join(item.text.split("\n", 1)[-1] for item in split).replace(" ", "") == clause.replace(" ", "")


def test_inline_first_clause_is_not_misread_as_the_section_title():
    pages = (
        ExtractedPage(
            page_number=1,
            text="1. Short title and commencement.\u2014 (1) First clause text.\n(2) Second clause.",
        ),
    )

    chunks = chunk_pages(_document(), pages, target_tokens=12)

    assert chunks[0].heading_path[-2] == "Section 1 - Short title and commencement"
    assert "First clause text" in " ".join(chunk.text for chunk in chunks)
    assert sum(chunk.text.count("First clause text") for chunk in chunks) == 1


def test_schedule_part_and_footnote_prefixed_division_enter_heading_path():
    pages = (
        ExtractedPage(
            page_number=2,
            text="First Schedule - Part III______\n10[DIVISION IVA\n(1) Export service rate.",
        ),
    )

    chunks = chunk_pages(_document(), pages)

    assert chunks[0].heading_path[:3] == (
        "SCHEDULE First",
        "PART III",
        "DIVISION IVA",
    )


def test_cleanup_repairs_known_words_and_preserves_numbers():
    text = "The t he acted after af ter the th e date 30 June 2025: Rs. 500 ― ‘‘quoted’’\n12\n3 ["
    cleaned = clean_document_pages((ExtractedPage(1, text),))[0].text
    assert "the acted after after the the date" in cleaned
    assert "30 June 2025" in cleaned and "Rs. 500" in cleaned
    assert '"quoted"' in cleaned and "12" not in cleaned and "3 [" not in cleaned


def test_cleanup_keeps_horizontal_bar_as_punctuation_and_normalizes_double_quotes():
    cleaned = clean_document_pages(
        (ExtractedPage(1, "Rule ― ‘‘quoted text’’; 30 June 2026; Rs. 75,000."),)
    )[0].text
    assert 'Rule — "quoted text"; 30 June 2026; Rs. 75,000.' in cleaned


def test_cleanup_repairs_pdf_utf8_quote_artifacts():
    source = "\u00e2\u20ac\u0153quoted\u00e2\u20ac\u009d \u00e2\u20ac\u201d text"
    cleaned = clean_document_pages((ExtractedPage(1, source),))[0].text
    assert cleaned == '"quoted" — text'


def test_section_two_definition_ranges_and_malformed_heading_fallback():
    pages = (ExtractedPage(51, "PART I\n2. Definitions\n(1) In this Act, terms include:\n(1) advocate means lawyer;\n(2) company means company.\n23. 8[�]\nOmitted by amendment."),)
    chunks = chunk_pages(_document(), pages, target_tokens=500)
    assert any("definitions (1)-(2)" in part for chunk in chunks for part in chunk.heading_path)
    assert any("Section 23 (title unreadable)" in part for chunk in chunks for part in chunk.heading_path)


def test_malformed_section_23_uses_repeated_title_from_the_body_text():
    pages = (
        ExtractedPage(
            51,
            "PART IV\n23. 8[�]\nsection was read as under:\n"
            "“23. Company to have common seal.—(1) Every company shall have a common seal.",
        ),
    )
    chunks = chunk_pages(_document(), pages)
    assert any(
        "Section 23 - Company to have common seal" in part
        for chunk in chunks
        for part in chunk.heading_path
    )


def test_seventh_schedule_fee_item_keeps_both_amounts_before_footnote():
    pages = (ExtractedPage(1, "(1) For electronic filing, a fee of Rs. 100 applies; for physical filing, Rs. 200 applies.\n1 Substituted item (1) vide notification dated 1 January 2026."),)
    chunks = chunk_pages(_document(), pages, target_tokens=5)
    assert len(chunks) == 1
    text = chunks[0].text
    assert "Rs. 100" in text and "Rs. 200" in text
    assert text.index("Rs. 200") < text.index("Substituted item")


def test_embedded_schedule_reference_does_not_reset_schedule_heading_path():
    document = CorpusDocument(
        file="Seventh Schedule, fees.pdf",
        title="Seventh Schedule",
        issuing_body="SECP",
        document_type="fee schedule",
        source_url="https://example.test/fees",
        effective_date="2026-04-20",
        consolidation_date=None,
        retrieved_at=None,
        content_sha256="b" * 64,
        scope_note="Fees only.",
        is_active=True,
    )
    pages = (
        ExtractedPage(
            11,
            "SEVENTH SCHEDULE\n"
            "(34) preceding item.\n"
            "fourth schedule or fifth schedule, a fee of Rs. 10 applies.\n"
            "(35) Fast Track Registration Services fee applies.",
        ),
    )
    chunks = chunk_pages(document, pages)
    target = next(chunk for chunk in chunks if "Fast Track" in chunk.text)
    assert "SCHEDULE Seventh" in target.heading_path
    assert "SCHEDULE Fourth" not in target.heading_path
