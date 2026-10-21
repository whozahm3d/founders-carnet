"""Apply the source-specific limits in the compliance corpus manifest (FR-8)."""

from __future__ import annotations

import re

from rag.compliance.documents import ExtractedPage
from rag.compliance.ingestion import CorpusDocument


_PART_HEADING = re.compile(r"^\s*PART\s+([IVXLCDM]+)\b", re.IGNORECASE)
_SECTION_HEADING = re.compile(
    r"^\s*(\d+[A-Z]?)\.\s+\S",
    re.IGNORECASE,
)
_SUBSECTION_HEADING = re.compile(r"^\s*\((\d+[A-Z]?)\)\s*")
_DIVISION_HEADING = re.compile(
    r"^\s*DIVISION\s+([IVXLCDM]+[A-Z]?)\b",
    re.IGNORECASE,
)
_SCHEDULE_HEADING = re.compile(
    r"^\s*(?:THE\s+)?(FIRST|SECOND|THIRD|FOURTH|FIFTH|SIXTH|SEVENTH)\s+SCHEDULE\b",
    re.IGNORECASE,
)

_COMPANIES_ACT = "Companies Act 2017, updated 18 Aug 2022 (SECP).pdf"
_INCOME_TAX_ORDINANCE = (
    "Income Tax Ordinance 2001, amended to 30 Jun 2026 (FBR).pdf"
)


def apply_corpus_scope(
    document: CorpusDocument,
    pages: tuple[ExtractedPage, ...],
) -> tuple[ExtractedPage, ...]:
    """Keep only the sections approved for the two long legal sources."""
    if document.file == _COMPANIES_ACT:
        return _filter_companies_act(pages)
    if document.file == _INCOME_TAX_ORDINANCE:
        return _filter_income_tax_ordinance(pages)
    return pages


def _filter_companies_act(
    pages: tuple[ExtractedPage, ...],
) -> tuple[ExtractedPage, ...]:
    current_part: str | None = None
    current_section: int | None = None
    filtered: list[ExtractedPage] = []

    for page in pages:
        kept_lines: list[str] = []
        for line in page.text.splitlines():
            part_heading = _PART_HEADING.match(line)
            if part_heading:
                current_part = part_heading.group(1).upper()
                if current_part in {"I", "IV"}:
                    kept_lines.append(line)
                continue

            section_heading = _SECTION_HEADING.match(line)
            if section_heading:
                current_section = _section_number(section_heading.group(1))

            if current_part in {"I", "IV"} or (
                current_section is not None and 462 <= current_section <= 473
            ):
                kept_lines.append(line)

        _append_filtered_page(filtered, page, kept_lines)
    return tuple(filtered)


def _filter_income_tax_ordinance(
    pages: tuple[ExtractedPage, ...],
) -> tuple[ExtractedPage, ...]:
    current_section: str | None = None
    current_subsection: str | None = None
    current_part: str | None = None
    in_first_schedule = False
    in_target_division = False
    filtered: list[ExtractedPage] = []

    for page in pages:
        kept_lines: list[str] = []
        for line in page.text.splitlines():
            schedule_heading = _SCHEDULE_HEADING.match(line)
            if schedule_heading:
                in_first_schedule = schedule_heading.group(1).upper() == "FIRST"
                in_target_division = False
                current_section = None
                current_subsection = None
                current_part = None

            part_heading = _PART_HEADING.match(line)
            if part_heading and in_first_schedule:
                current_part = part_heading.group(1).upper()
                in_target_division = False

            division_heading = _DIVISION_HEADING.match(line)
            if division_heading and in_first_schedule:
                in_target_division = (
                    current_part == "III"
                    and division_heading.group(1).upper() == "IVA"
                )

            section_heading = _SECTION_HEADING.match(line)
            if section_heading:
                current_section = section_heading.group(1).upper()
                current_subsection = None

            if current_section == "2":
                subsection_heading = _SUBSECTION_HEADING.match(line)
                if subsection_heading:
                    current_subsection = subsection_heading.group(1).upper()

            if current_section == "154A" or (
                current_section == "2" and current_subsection == "62A"
            ):
                kept_lines.append(line)
            elif in_first_schedule and in_target_division:
                kept_lines.append(line)

        _append_filtered_page(filtered, page, kept_lines)
    return tuple(filtered)


def _section_number(value: str) -> int:
    return int(re.match(r"\d+", value).group())


def _append_filtered_page(
    pages: list[ExtractedPage],
    source_page: ExtractedPage,
    lines: list[str],
) -> None:
    text = "\n".join(lines).strip()
    if text:
        pages.append(ExtractedPage(page_number=source_page.page_number, text=text))
