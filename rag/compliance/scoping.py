"""Apply the provision limits in the corpus report and manifest (FR-8)."""

from __future__ import annotations

import re

from rag.compliance.documents import ExtractedPage
from rag.compliance.ingestion import CorpusDocument

_PART_HEADING = re.compile(r"^\s*PART\s+([IVXLCDM]+)\s*$", re.IGNORECASE)
_CHAPTER_HEADING = re.compile(r"^\s*CHAPTER\s+([IVXLCDM0-9]+)\b", re.IGNORECASE)
_SECTION_HEADING = re.compile(
    r"^\s*(?:(?i:section)\s+)?(?P<section>\d+[A-Z]?)\.\s+(?P<title>\S.*)$"
)
_EXPORT_HEADING = re.compile(r"^\s*\d+\[\s*154A\.\s+(?P<title>\S.*)$")
_FOOTNOTE_SECTION_HEADING = re.compile(r"^\s*\d+\[\s*(?P<section>\d+[A-Z]?)\.\s+(?P<title>\S.*)$")
_SUBSECTION_HEADING = re.compile(
    r"^\s*(?:\d+\s*[\[(]\s*)?\((?P<subsection>\d+[A-Z]?)\)\s*"
)
_DIVISION_HEADING = re.compile(
    r"^\s*(?:\d+\s*[\[(]\s*)?DIVISION\s+([IVXLCDM]+[A-Z]?)\b",
    re.IGNORECASE,
)
_SCHEDULE_HEADING = re.compile(
    r"^\s*(?:THE\s+)?(FIRST|SECOND|THIRD|FOURTH|FIFTH|SIXTH|SEVENTH)\s+SCHEDULE\b",
    re.IGNORECASE,
)
_SCHEDULE_TITLE_LINE = re.compile(
    r"^\s*(?:THE\s+)?(?:FIRST|SECOND|THIRD|FOURTH|FIFTH|SIXTH|SEVENTH)\s+SCHEDULE(?:\s*(?:[-\u2014_].*)?)\s*$",
    re.IGNORECASE,
)
_SCHEDULE_PART_HEADING = re.compile(
    r"^\s*(?:THE\s+)?FIRST\s+SCHEDULE.*?\bPART\s+([IVXLCDM]+)(?![A-Z])",
    re.IGNORECASE,
)
_TOC_DOT_LEADER = re.compile(r"\.{5,}")

_COMPANIES_ACT = "Companies Act 2017, updated 18 Aug 2022 (SECP).pdf"
_INCOME_TAX_ORDINANCE = (
    "Income Tax Ordinance 2001, amended to 30 Jun 2026 (FBR).pdf"
)
_FINANCE_ACT = "Finance Act 2026, gazette of 26 Jun 2026.pdf"

# Companies Act: Parts I and IV, and sections 462–473 (docs/context/corpus.md).
_COMPANIES_PARTS = {"I", "IV"}
_COMPANIES_SECTIONS = range(462, 474)

# Income Tax Ordinance scope as enumerated in rag/corpus_manifest.md:
# section 2(62A), section 154A, and First Schedule Part III Division IVA.
_INCOME_TAX_STARTUP_SUBSECTION = "62A"
_INCOME_TAX_EXPORT_SECTION = "154A"
_INCOME_TAX_SCHEDULE = "FIRST"
_INCOME_TAX_SCHEDULE_PART = "III"
_INCOME_TAX_SCHEDULE_DIVISION = "IVA"


def apply_corpus_scope(
    document: CorpusDocument,
    pages: tuple[ExtractedPage, ...],
) -> tuple[ExtractedPage, ...]:
    """Keep only the sections approved for the two long legal sources."""
    if document.file == _COMPANIES_ACT:
        return _filter_companies_act(pages)
    if document.file == _INCOME_TAX_ORDINANCE:
        return _filter_income_tax_ordinance(pages)
    if document.file == _FINANCE_ACT:
        return _filter_finance_act(pages)
    return pages


def _filter_finance_act(
    pages: tuple[ExtractedPage, ...],
) -> tuple[ExtractedPage, ...]:
    """Keep Finance Act provisions amending the Income Tax Ordinance only."""
    in_target_provision = False
    filtered: list[ExtractedPage] = []
    start = re.compile(
        r"^\s*5\.\s+Amendments of the Income Tax Ordinance\b", re.IGNORECASE
    )
    stop = re.compile(
        r"^\s*6\.\s+Amendments of the Federal Excise Act\b", re.IGNORECASE
    )

    for page in pages:
        lines = page.text.splitlines()
        kept: list[str] = []
        for line in lines:
            if not in_target_provision:
                if start.match(line):
                    in_target_provision = True
                else:
                    continue
            if stop.match(line):
                in_target_provision = False
                break
            kept.append(line)
        _append_filtered_page(filtered, page, kept)
        if not in_target_provision and any(stop.match(line) for line in lines):
            break
    return tuple(filtered)


def _filter_companies_act(
    pages: tuple[ExtractedPage, ...],
) -> tuple[ExtractedPage, ...]:
    current_part: str | None = None
    current_section: int | None = None
    started_act_body = False
    in_schedule = False
    filtered: list[ExtractedPage] = []

    for page in pages:
        lines = page.text.splitlines()
        if _is_contents_page(page.text):
            continue
        has_section = any(_SECTION_HEADING.match(line) for line in lines)
        if not started_act_body and not has_section:
            continue
        if has_section:
            started_act_body = True

        kept_lines: list[str] = []
        for line in lines:
            if _SCHEDULE_TITLE_LINE.match(line):
                in_schedule = True
                current_part = None
                current_section = None
                continue
            if in_schedule:
                continue
            part_heading = _PART_HEADING.match(line)
            if part_heading:
                current_part = part_heading.group(1).upper()
                current_section = None
                # Keep structural markers so the chunker can reset part paths.
                kept_lines.append(line)
                continue

            section_heading = _SECTION_HEADING.match(line)
            if section_heading:
                current_section = _section_number(section_heading.group("section"))

            if current_part in _COMPANIES_PARTS or current_section in _COMPANIES_SECTIONS:
                kept_lines.append(line)

        _append_filtered_page(filtered, page, kept_lines)
    return tuple(filtered)


def _is_contents_page(text: str) -> bool:
    if "TABLE OF CONTENTS" in text.upper():
        return True
    first_line = next((line.strip() for line in text.splitlines() if line.strip()), "")
    if re.fullmatch(r"[IVXLCDM]+", first_line, re.IGNORECASE) and _TOC_DOT_LEADER.search(
        text
    ):
        return True
    return sum(bool(_TOC_DOT_LEADER.search(line)) for line in text.splitlines()) >= 2


def _filter_income_tax_ordinance(
    pages: tuple[ExtractedPage, ...],
) -> tuple[ExtractedPage, ...]:
    current_section: str | None = None
    current_subsection: str | None = None
    current_part: str | None = None
    in_first_schedule = False
    in_target_division = False
    started_ordinance_body = False
    has_commencement_heading = any(
        (heading := _SECTION_HEADING.match(line)) is not None
        and heading.group("section").upper() == "1"
        and re.search(r"\bTHIS\s+ORDINANCE\b", line, re.IGNORECASE) is not None
        for page in pages
        for line in page.text.splitlines()
    )
    filtered: list[ExtractedPage] = []

    for page in pages:
        lines = page.text.splitlines()
        if not started_ordinance_body:
            if not has_commencement_heading:
                started_ordinance_body = True
            else:
                starts_ordinance = any(
                    (heading := _SECTION_HEADING.match(line)) is not None
                    and heading.group("section").upper() == "1"
                    and re.search(r"\bTHIS\s+ORDINANCE\b", line, re.IGNORECASE) is not None
                    for line in lines
                )
                if not starts_ordinance:
                    continue
                started_ordinance_body = True

        kept_lines: list[str] = []
        chapter_line = next((line for line in lines if _CHAPTER_HEADING.match(line)), None)
        if chapter_line and (current_section == _INCOME_TAX_EXPORT_SECTION or current_section == "2" and current_subsection == _INCOME_TAX_STARTUP_SUBSECTION):
            kept_lines.append(chapter_line)
        chapter_added = bool(kept_lines)
        for line in lines:
            schedule_heading = _SCHEDULE_HEADING.match(line)
            if schedule_heading:
                in_first_schedule = (
                    schedule_heading.group(1).upper() == _INCOME_TAX_SCHEDULE
                )
                in_target_division = False
                current_section = None
                current_subsection = None
                schedule_part = _SCHEDULE_PART_HEADING.match(line)
                current_part = schedule_part.group(1).upper() if schedule_part else None

            part_heading = _PART_HEADING.match(line)
            if part_heading and in_first_schedule:
                current_part = part_heading.group(1).upper()
                in_target_division = False

            division_heading = _DIVISION_HEADING.match(line)
            if division_heading and in_first_schedule:
                in_target_division = (
                    current_part == _INCOME_TAX_SCHEDULE_PART
                    and division_heading.group(1).upper()
                    == _INCOME_TAX_SCHEDULE_DIVISION
                )
                if in_target_division:
                    kept_lines.extend(("First Schedule - Part III", line))
                continue

            section_heading = _SECTION_HEADING.match(line)
            export_heading = _EXPORT_HEADING.match(line)
            if export_heading:
                current_section = _INCOME_TAX_EXPORT_SECTION
                current_subsection = None
                if chapter_line and not chapter_added:
                    kept_lines.append(chapter_line)
                    chapter_added = True
            footnote_section = _FOOTNOTE_SECTION_HEADING.match(line)
            if current_section == _INCOME_TAX_EXPORT_SECTION and footnote_section and footnote_section.group("section").upper() != _INCOME_TAX_EXPORT_SECTION:
                current_section = None
                current_subsection = None
                continue
            if section_heading:
                current_section = section_heading.group("section").upper()
                current_subsection = None

            if current_section == "2":
                subsection_heading = _SUBSECTION_HEADING.match(line)
                if subsection_heading:
                    current_subsection = subsection_heading.group("subsection").upper()
                    if current_subsection == _INCOME_TAX_STARTUP_SUBSECTION:
                        if chapter_line and not chapter_added:
                            kept_lines.append(chapter_line)
                            chapter_added = True
                        kept_lines.append("2. Definitions")

            if (
                current_section == _INCOME_TAX_EXPORT_SECTION
                or current_section == "2"
                and current_subsection == _INCOME_TAX_STARTUP_SUBSECTION
                or in_first_schedule and in_target_division
            ):
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
