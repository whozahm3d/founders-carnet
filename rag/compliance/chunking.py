"""Build citation-ready, clause-safe chunks (FR-8, NFR-12, NFR-14)."""

from __future__ import annotations

import re
from dataclasses import dataclass, replace
from typing import Any

from rag.compliance.documents import ExtractedPage
from rag.compliance.ingestion import CorpusDocument

_SECTION_HEADING = re.compile(
    r"^\s*(?:(?i:section)\s+)?(?P<section>\d+[A-Z]?)\.\s+(?P<title>[A-Z][^\n]{1,})$"
)
_EXPORT_HEADING = re.compile(r"^\s*\d+\[\s*(?P<section>154A)\.\s+(?P<title>[A-Z][^\n]{1,})$")
_FOOTNOTE_SECTION_HEADING = re.compile(r"^\s*\d+\[\s*(?P<section>\d+[A-Z]?)\.\s+(?P<title>[A-Z][^\n]{1,})$")
_PART_HEADING = re.compile(r"^\s*PART\s+([IVXLCDM]+)\s*$", re.IGNORECASE)
_CHAPTER_HEADING = re.compile(r"^\s*CHAPTER\s+([IVXLCDM0-9]+)\b", re.IGNORECASE)
_DIVISION_HEADING = re.compile(
    r"^\s*(?:\d+\s*[\[(]\s*)?DIVISION\s+([IVXLCDM]+[A-Z]?)\b",
    re.IGNORECASE,
)
_SCHEDULE_HEADING = re.compile(
    r"^\s*(?:THE\s+)?(FIRST|SECOND|THIRD|FOURTH|FIFTH|SIXTH|SEVENTH)\s+SCHEDULE"
    r"(?:\s*[-_]+\s*PART\s+[IVXLCDM]+[_\s]*)?\s*$",
    re.IGNORECASE,
)
_SCHEDULE_PART_HEADING = re.compile(
    r"^\s*(?:THE\s+)?FIRST\s+SCHEDULE.*?\bPART\s+([IVXLCDM]+)(?![A-Z])",
    re.IGNORECASE,
)
_CLAUSE_HEADING = re.compile(
    r"^\s*(?:\d+\s*[\[(]\s*)?\((?P<number>\d+[A-Z]?)\)\s*"
)
_NUMBERED_ITEM = re.compile(r"^\s*(?P<number>\d{1,3})\.\s+\S")
_LEXICAL_TOKEN = re.compile(r"\w+(?:['\u2019]\w+)*|[^\w\s]", re.UNICODE)
_FOOTNOTE_LINE = re.compile(r"^\s*\d+\s+(?:Substituted|Inserted|Omitted|Added|Division|Clause)\b", re.IGNORECASE)


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
    heading_path: tuple[str, ...]
    token_count: int
    text: str


@dataclass(frozen=True, slots=True)
class _Block:
    page_number: int
    heading_path: tuple[str, ...]
    text: str


@dataclass(frozen=True, slots=True)
class _Section:
    section: str | None
    title: str | None
    heading_path: tuple[str, ...]
    blocks: tuple[_Block, ...]


def chunk_pages(
    document: CorpusDocument,
    pages: tuple[ExtractedPage, ...],
    *,
    target_tokens: int = 500,
) -> tuple[CitationChunk, ...]:
    """Pack whole legal clauses into roughly target-sized headed chunks.

    Token counts use a stable lexical estimate (words and punctuation). A long
    numbered clause remains intact even when it exceeds ``target_tokens``.
    """
    if target_tokens < 1:
        raise ValueError("target_tokens must be positive")

    pages = clean_document_pages(pages)
    sections = _parse_sections(pages)
    chunks: list[CitationChunk] = []
    for group in sections:
        batches = _pack_blocks(group.blocks, target_tokens)
        multi_chunk = len(batches) > 1
        for batch in batches:
            body = "\n\n".join(block.text for block in batch)
            prefix = (
                f"Section {group.section} - {group.title}\n"
                if (multi_chunk or group.blocks) and group.section and group.title
                else ""
            )
            text = f"{prefix}{body}".strip()
            common_path = _batch_heading_path(batch, group.heading_path) or (document.title,)
            chunks.append(
                CitationChunk(
                    chunk_id=f"{document.file}:{batch[0].page_number}:{len(chunks)}",
                    document_file=document.file,
                    document_title=document.title,
                    issuing_body=document.issuing_body,
                    document_type=document.document_type,
                    source_url=document.source_url,
                    effective_date=document.effective_date,
                    consolidation_date=document.consolidation_date,
                    retrieved_at=document.retrieved_at,
                    source_sha256=document.content_sha256,
                    page_number=batch[0].page_number,
                    section=group.section,
                    heading_path=common_path,
                    token_count=_token_count(text),
                    text=text,
                )
            )
    return tuple(chunks)


def _parse_sections(pages: tuple[ExtractedPage, ...]) -> tuple[_Section, ...]:
    groups: list[_Section] = []
    path: list[str] = []
    section: str | None = None
    title: str | None = None
    section_path: tuple[str, ...] = ()
    blocks: list[_Block] = []
    buffer: list[str] = []
    buffer_page = 1
    buffer_path: tuple[str, ...] = ()
    in_numbered_clause = False
    seen_definition_numbers: set[str] = set()
    in_definitions = False
    definition_section = False

    def flush_block() -> None:
        nonlocal buffer
        notes = [line for line in buffer if _FOOTNOTE_LINE.match(line)]
        body = [line for line in buffer if not _FOOTNOTE_LINE.match(line)]
        text = "\n".join((*body, *notes)).strip()
        if text:
            blocks.append(_Block(buffer_page, buffer_path, text))
        buffer = []

    def flush_section() -> None:
        nonlocal blocks, seen_definition_numbers, in_definitions, definition_section
        flush_block()
        if blocks:
            groups.append(_Section(section, title, section_path, tuple(blocks)))
        blocks = []
        seen_definition_numbers = set()
        in_definitions = False
        definition_section = False

    def begin_block(page_number: int, block_path: tuple[str, ...], line: str) -> None:
        nonlocal buffer_page, buffer_path, buffer
        buffer_page = page_number
        buffer_path = block_path
        buffer = [line.strip()]

    for page in pages:
        for line in page.text.splitlines():
            part = _PART_HEADING.match(line)
            chapter = _CHAPTER_HEADING.match(line)
            division = _DIVISION_HEADING.match(line)
            schedule = _SCHEDULE_HEADING.match(line)
            schedule_part = _SCHEDULE_PART_HEADING.match(line)
            heading = (
                _SECTION_HEADING.match(line)
                or _EXPORT_HEADING.match(line)
                or _FOOTNOTE_SECTION_HEADING.match(line)
            )
            malformed_23 = re.match(r"^\s*23\.\s*8\s*\[.*", line)

            if chapter and section is not None and f"CHAPTER {chapter.group(1).upper()}" in path:
                continue
            if any(item.startswith("DIVISION ") for item in path) and any(item.startswith("SCHEDULE ") for item in path):
                heading = None

            if part or chapter or division or schedule:
                flush_section()
                headings = []
                if part:
                    headings.append(("PART", part.group(1).upper()))
                if chapter:
                    headings.append(("CHAPTER", chapter.group(1).upper()))
                if division:
                    headings.append(("DIVISION", division.group(1).upper()))
                if schedule:
                    headings.append(("SCHEDULE", schedule.group(1).title()))
                if schedule_part:
                    headings.append(("PART", schedule_part.group(1).upper()))
                for kind, value in headings:
                    path = [item for item in path if not item.startswith(f"{kind} ")]
                    path.append(f"{kind} {value}")
                section = title = None
                section_path = tuple(path)
                in_numbered_clause = False
                continue

            if heading or malformed_23:
                flush_section()
                section = heading.group("section") if heading else "23"
                raw_title = heading.group("title") if heading else _recover_section_23_title(page.text)
                if not raw_title:
                    raw_title = "title unreadable"
                title, leading_clause = _split_section_heading(raw_title)
                section_path = (
                    (*path, "Section 23 (title unreadable)")
                    if malformed_23 and title == "title unreadable"
                    else (*path, f"Section {section} - {title}")
                )
                in_numbered_clause = False
                seen_definition_numbers = set()
                definition_section = section == "2" and "definition" in title.casefold()
                if leading_clause:
                    clause = _CLAUSE_HEADING.match(leading_clause)
                    if clause:
                        if definition_section:
                            seen_definition_numbers.add(clause.group("number"))
                        begin_block(
                            page.page_number,
                            (*section_path, f"Subsection ({clause.group('number')})"),
                            leading_clause,
                        )
                        in_numbered_clause = True
                    else:
                        begin_block(page.page_number, section_path, leading_clause)
                continue

            if not line.strip():
                if not in_numbered_clause:
                    flush_block()
                continue

            clause = _CLAUSE_HEADING.match(line)
            numbered_item = _NUMBERED_ITEM.match(line)
            if clause or numbered_item:
                if clause and definition_section:
                    number = clause.group("number")
                    if number in seen_definition_numbers:
                        in_definitions = True
                    else:
                        seen_definition_numbers.add(number)
                flush_block()
                label = (
                    f"Definition {clause.group('number')}" if clause and in_definitions
                    else f"Subsection ({clause.group('number')})"
                    if clause
                    else f"Item {numbered_item.group('number')}"
                )
                begin_block(page.page_number, (*section_path, label), line)
                in_numbered_clause = True
                continue

            if not buffer:
                begin_block(page.page_number, section_path or tuple(path), line)
            else:
                buffer.append(line.strip())

    flush_section()
    return tuple(groups)


def _split_section_heading(value: str) -> tuple[str, str | None]:
    """Separate an inline first subsection from a PDF's section heading line."""
    clause = re.search(r"(?<!\w)(?:\d+\s*[\[(]\s*)?\(\d+[A-Z]?\)", value)
    if not clause:
        return value.strip().rstrip(" .-\ufffd\u2014"), None
    title = value[: clause.start()].strip().rstrip(" .-\ufffd\u2014")
    return title or value.strip(), value[clause.start() :].strip()


def _recover_section_23_title(page_text: str) -> str | None:
    """Use the repeated quoted section heading when the PDF heading is corrupt."""
    flattened = re.sub(r"\s+", " ", page_text)
    match = re.search(
        r"(?<!\w)23\.\s*(?P<title>[A-Z][^.]{3,120}?)\s*(?:\.?—|\.|–)\s*(?:\(1\)|$)",
        flattened,
    )
    if not match:
        return None
    return match.group("title").strip()


def _pack_blocks(
    blocks: tuple[_Block, ...],
    target_tokens: int,
) -> tuple[tuple[_Block, ...], ...]:
    batches: list[tuple[_Block, ...]] = []
    current: list[_Block] = []
    current_tokens = 0
    for block in blocks:
        block_tokens = _token_count(block.text)
        if current and current_tokens + block_tokens > target_tokens:
            batches.append(tuple(current))
            current = []
            current_tokens = 0
        current.append(block)
        current_tokens += block_tokens
    if current:
        batches.append(tuple(current))
    return tuple(batches)


def _batch_heading_path(
    batch: tuple[_Block, ...],
    fallback: tuple[str, ...],
) -> tuple[str, ...]:
    """Keep the section path and identify sibling clauses packed together."""
    paths = [block.heading_path for block in batch]
    if len(paths) == 1 and paths[0] and paths[0][-1].startswith("Definition "):
        number = re.search(r"\d+", paths[0][-1]).group()
        return (*paths[0][:-1], f"definitions ({number})-({number})")
    shared_length = 0
    while paths and all(len(path) > shared_length for path in paths) and len(
        {path[shared_length] for path in paths}
    ) == 1:
        shared_length += 1

    shared = paths[0][:shared_length] if paths else fallback
    labels = [path[shared_length:] for path in paths]
    definition_values = [
        int(re.search(r"\d+", label[0]).group())
        for label in labels
        if len(label) == 1 and label[0].startswith("Definition ")
    ]
    if definition_values:
        return (*shared, f"definitions ({min(definition_values)})-({max(definition_values)})")
    if labels and all(len(label) == 1 for label in labels):
        values = [label[0] for label in labels]
        if all(value.startswith("Definition ") for value in values):
            numbers = [int(re.search(r"\d+", value).group()) for value in values]
            return (*shared, f"definitions ({min(numbers)}-{max(numbers)})")
        if all(value.startswith("Subsection ") for value in values):
            suffix = ", ".join(value.removeprefix("Subsection ") for value in values)
            return (*shared, f"Subsections {suffix}")
        if all(value.startswith("Item ") for value in values):
            suffix = ", ".join(value.removeprefix("Item ") for value in values)
            return (*shared, f"Items {suffix}")
    return shared or fallback


def _token_count(text: str) -> int:
    """Return a reproducible lexical token estimate without model downloads."""
    return len(_LEXICAL_TOKEN.findall(text))


def clean_document_pages(pages: tuple[ExtractedPage, ...]) -> tuple[ExtractedPage, ...]:
    """Repair known OCR/extraction artifacts before chunking without changing numerals."""
    all_text = "\n".join(page.text for page in pages)
    vocabulary = {word.casefold() for word in re.findall(r"[A-Za-z]{3,}", all_text)}
    cleaned: list[ExtractedPage] = []
    for page in pages:
        lines: list[str] = []
        footnotes: list[str] = []
        for line in page.text.splitlines():
            if re.fullmatch(r"\s*\d+\s*", line) or re.fullmatch(r"\s*\d+\s*\[\s*", line):
                continue
            if _FOOTNOTE_LINE.match(line):
                footnotes.append(line)
                continue
            line = (
                line.replace("‘‘", '"')
                .replace("’’", '"')
                .replace("\u00e2\u20ac\u201d", "\u2014")
                .replace("\u201c", '"')
                .replace("\u201d", '"')
                .replace("\u2018", "'")
                .replace("\u2019", "'")
                .replace("\u00e2\u20ac\u0153", '"')
                .replace("\u00e2\u20ac\u009d", '"')
                .replace("\u00e2\u20ac\u02dc", "'")
                .replace("\u00e2\u20ac\u2122", "'")
                .replace("\u00e2\u20ac\u2014", "\u2014")
                .replace("\u00e2\u20ac\u2013", "\u2013")
                .replace("\u00e2\u20ac\u2022", "\u2015")
                .replace("―", "—")
            )
            common_fragments = {"a", "i", "an", "in", "to", "of", "is", "he", "be", "as", "at", "on", "or", "by", "if", "it", "we", "do", "no", "up", "us", "my", "me", "so", "am"}
            while True:
                changed = False
                matches = list(re.finditer(r"(?=(?<!\w)([A-Za-z]{1,3})\s+([A-Za-z]{1,5})(?!\w))", line))
                for match in reversed(matches):
                    left, right = match.group(1), match.group(2)
                    if (left + right).casefold() in vocabulary and left.casefold() not in common_fragments:
                        line = line[:match.start(1)] + left + right + line[match.end(2):]
                        changed = True
                if not changed:
                    break
            lines.append(line)
        lines.extend(footnotes)
        cleaned.append(ExtractedPage(page.page_number, "\n".join(lines)))
    return tuple(cleaned)


def split_chunks_for_model(
    chunks: tuple[CitationChunk, ...], tokenizer: Any, max_seq_length: int
) -> tuple[CitationChunk, ...]:
    """Keep each embedding input within a model's true token limit.

    Long clauses become ordered continuation chunks; the section heading and
    full heading path are repeated so each fragment remains independently citable.
    """
    if max_seq_length < 8:
        raise ValueError("max_seq_length must be at least 8")
    result: list[CitationChunk] = []
    for chunk in chunks:
        if _model_token_count(tokenizer, chunk.text) <= max_seq_length:
            result.append(replace(chunk, token_count=_model_token_count(tokenizer, chunk.text)))
            continue
        match = re.match(r"^(Section [^\n]+\n)(.*)$", chunk.text, flags=re.DOTALL)
        heading = match.group(1) if match else ""
        body = match.group(2) if match else chunk.text
        heading_tokens = _model_token_count(tokenizer, heading) if heading else 0
        budget = max_seq_length - heading_tokens - 2
        if budget < 4:
            raise ValueError(f"Section heading exceeds token limit for {chunk.chunk_id}")
        pieces = _split_text_on_token_boundaries(body, tokenizer, budget)
        for index, piece in enumerate(pieces, start=1):
            text = f"{heading}{piece}".strip()
            actual_count = _model_token_count(tokenizer, text)
            if actual_count > max_seq_length:
                raise ValueError(f"Token-safe split failed for {chunk.chunk_id}")
            result.append(
                replace(
                    chunk,
                    chunk_id=f"{chunk.chunk_id}:continuation-{index}",
                    heading_path=(*chunk.heading_path, f"Continuation {index}/{len(pieces)}"),
                    token_count=actual_count,
                    text=text,
                )
            )
    return tuple(result)


def _model_token_count(tokenizer: Any, text: str) -> int:
    encoded = tokenizer(text, add_special_tokens=True, truncation=False)
    return len(encoded["input_ids"])


def _split_text_on_token_boundaries(text: str, tokenizer: Any, max_tokens: int) -> list[str]:
    encoded = tokenizer(text, add_special_tokens=False, truncation=False, return_offsets_mapping=True)
    ids = encoded["input_ids"]
    offsets = encoded.get("offset_mapping")
    if not ids or offsets is None:
        return [text]
    pieces: list[str] = []
    cursor = 0
    token_start = 0
    while token_start < len(ids):
        token_end = min(token_start + max_tokens, len(ids))
        char_end = offsets[token_end - 1][1]
        if token_end < len(ids):
            boundary = text.rfind(" ", cursor, char_end)
            if boundary > cursor:
                char_end = boundary
                token_end = max(
                    token_start + 1,
                    next(
                        (i for i, (_, end) in enumerate(offsets, start=1) if end >= char_end),
                        token_end,
                    ),
                )
        piece = text[cursor:char_end]
        if not piece.strip():
            char_end = offsets[token_end - 1][1]
            piece = text[cursor:char_end]
        pieces.append(piece)
        cursor = char_end
        while cursor < len(text) and text[cursor].isspace():
            cursor += 1
        token_start = next(
            (i for i, (start, end) in enumerate(offsets) if end > cursor or start >= cursor),
            len(ids),
        )
    if cursor < len(text):
        pieces.append(text[cursor:])
    return [piece for piece in pieces if piece.strip()]
