"""Build or validate the per-page PDF extraction cache (FR-8, NFR-13)."""

from __future__ import annotations

import argparse
from pathlib import Path

from rag.compliance.documents import cached_pdf_pages


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("cache", type=Path)
    args = parser.parse_args()
    pages = cached_pdf_pages(args.pdf, args.cache)
    print(f"{args.pdf.name}: cached {len(pages)} page records")


if __name__ == "__main__":
    main()
