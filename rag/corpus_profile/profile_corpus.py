"""
Profile the compliance-corpus documents for Chapter 3, Section 3.3.2.

PDFs  : page count, metadata dates, file size, SHA-256, text-layer check,
        word count, and a short preview of page 1.
Pages : fetches each URL, saves a dated HTML snapshot plus extracted text,
        and records HTTP status, final URL, title, any last-updated date
        the page or server exposes, word count, and SHA-256.

Install once:
    pip install pypdf requests beautifulsoup4

Run:
    python profile_corpus.py --pdf-dir ./corpus
    python profile_corpus.py --pdf-dir ./corpus --url https://example.com/other-page/

Outputs (in ./corpus_profile/):
    profile_report.md    readable report for 3.3.2
    profile_report.json  same data, machine-readable
    snapshots/           dated HTML and extracted text for each web page
"""

import argparse
import datetime as dt
import hashlib
import json
import os
import re
from pathlib import Path

# Clean up stale CA bundle environment variables pointing to deleted paths
for cert_env in ("REQUESTS_CA_BUNDLE", "SSL_CERT_FILE"):
    val = os.environ.get(cert_env)
    if val and not os.path.exists(val):
        os.environ.pop(cert_env, None)


DEFAULT_URLS = [
    "https://techdestination.com/industry-facilitation/",
]

# A page with fewer extracted characters than this is treated as having no text layer.
MIN_CHARS_PER_PAGE = 50
TODAY = dt.date.today().isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def clean_pdf_date(value) -> str:
    """Turn PDF dates like D:20260220101500+05'00' into 2026-02-20."""
    if not value:
        return "not stated"
    s = str(value)
    m = re.search(r"(\d{4})(\d{2})(\d{2})", s)
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else s


def profile_pdf(path: Path) -> dict:
    from pypdf import PdfReader

    raw = path.read_bytes()
    rec = {
        "type": "pdf",
        "file": path.name,
        "size_mb": round(len(raw) / 1_048_576, 2),
        "sha256": sha256_bytes(raw),
        "access_date": TODAY,
    }
    try:
        reader = PdfReader(str(path))
        if reader.is_encrypted:
            try:
                reader.decrypt("")
            except Exception:  # noqa: BLE001 - profiler must not stop on one bad file
                rec["error"] = "encrypted, could not open"
                return rec

        meta = reader.metadata or {}
        rec["title"] = (getattr(meta, "title", None) or "not stated")
        rec["created"] = clean_pdf_date(meta.get("/CreationDate"))
        rec["modified"] = clean_pdf_date(meta.get("/ModDate"))
        rec["producer"] = str(meta.get("/Producer") or "not stated")

        pages = reader.pages
        rec["pages"] = len(pages)

        text_pages, total_words, preview = 0, 0, ""
        for i, page in enumerate(pages):
            try:
                txt = page.extract_text() or ""
            except Exception:  # noqa: BLE001 - one unreadable page counts as empty text, not a crash
                txt = ""
            if len(txt.strip()) >= MIN_CHARS_PER_PAGE:
                text_pages += 1
            total_words += len(txt.split())
            if i == 0:
                preview = " ".join(txt.split())[:300]

        rec["pages_with_text"] = text_pages
        rec["text_layer_pct"] = round(100 * text_pages / max(len(pages), 1), 1)
        if rec["text_layer_pct"] >= 95:
            rec["text_layer"] = "yes"
        elif rec["text_layer_pct"] == 0:
            rec["text_layer"] = "no (scanned, needs OCR)"
        else:
            rec["text_layer"] = "partial (some pages need OCR)"
        rec["words"] = total_words
        rec["page1_preview"] = preview or "(no extractable text on page 1)"
    except Exception as exc:  # noqa: BLE001 - profiler must record a bad PDF and keep going
        rec["error"] = f"{type(exc).__name__}: {exc}"
    return rec


def find_page_date(soup, headers) -> str:
    """Look for a last-updated date in common meta tags, JSON-LD, then the HTTP header."""
    for attr, name in [
        ("property", "article:modified_time"),
        ("property", "og:updated_time"),
        ("name", "last-modified"),
        ("itemprop", "dateModified"),
    ]:
        tag = soup.find("meta", attrs={attr: name})
        if tag and tag.get("content"):
            return f"{tag['content']} (from <meta {name}>)"
    for script in soup.find_all("script", type="application/ld+json"):
        m = re.search(r'"dateModified"\s*:\s*"([^"]+)"', script.string or "")
        if m:
            return f"{m.group(1)} (from JSON-LD dateModified)"
    if headers.get("Last-Modified"):
        return f"{headers['Last-Modified']} (from HTTP header, may be server-generated)"
    return "not stated"


def profile_url(url: str, snap_dir: Path) -> dict:
    import requests
    from bs4 import BeautifulSoup

    rec = {"type": "web", "url": url, "access_date": TODAY}
    try:
        resp = requests.get(
            url,
            timeout=30,
            headers={"User-Agent": "Mozilla/5.0 (corpus profiling for academic project)"},
        )
        rec["http_status"] = resp.status_code
        rec["final_url"] = resp.url
        html = resp.content

        slug = re.sub(r"[^a-z0-9]+", "_", url.lower().split("//", 1)[-1]).strip("_")[:80]
        html_path = snap_dir / f"{slug}_{TODAY}.html"
        html_path.write_bytes(html)
        rec["html_snapshot"] = str(html_path)
        rec["html_sha256"] = sha256_bytes(html)

        soup = BeautifulSoup(html, "html.parser")
        rec["title"] = soup.title.get_text(strip=True) if soup.title else "not stated"
        rec["last_updated"] = find_page_date(soup, resp.headers)

        for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "form"]):
            tag.decompose()
        text = "\n".join(
            line.strip() for line in soup.get_text("\n").splitlines() if line.strip()
        )
        txt_path = snap_dir / f"{slug}_{TODAY}.txt"
        txt_path.write_text(text, encoding="utf-8")
        rec["text_snapshot"] = str(txt_path)
        rec["words"] = len(text.split())
        rec["text_preview"] = " ".join(text.split())[:300]
        if rec["words"] < 100:
            rec["warning"] = (
                "very little text extracted; the page may load content with JavaScript. "
                "Use the browser 'Save as PDF' copy as the corpus source instead."
            )
    except Exception as exc:  # noqa: BLE001 - profiler must record a bad web page and keep going
        rec["error"] = f"{type(exc).__name__}: {exc}"
    return rec


def write_report(records: list, out_dir: Path) -> Path:
    lines = ["# Corpus profiling report", "", f"Run date: {TODAY}", ""]

    pdfs = [r for r in records if r["type"] == "pdf"]
    webs = [r for r in records if r["type"] == "web"]

    if pdfs:
        lines += [
            "## PDF documents",
            "",
            "| File | Pages | Text layer | Words | Created | Modified | Size (MB) |",
            "|---|---|---|---|---|---|---|",
        ]
        for r in pdfs:
            if "error" in r:
                lines.append(f"| {r['file']} | ERROR: {r['error']} | | | | | {r['size_mb']} |")
            else:
                lines.append(
                    f"| {r['file']} | {r['pages']} | {r['text_layer']} ({r['text_layer_pct']}%) | "
                    f"{r['words']:,} | {r['created']} | {r['modified']} | {r['size_mb']} |"
                )
        lines.append("")
        for r in pdfs:
            if "error" not in r:
                lines += [f"**{r['file']}**", "",
                          f"- Title metadata: {r['title']}",
                          f"- Producer: {r['producer']}",
                          f"- SHA-256: `{r['sha256']}`",
                          f"- Page 1 preview: {r['page1_preview']}", ""]

    if webs:
        lines += ["## Web pages", ""]
        for r in webs:
            lines += [f"**{r['url']}**", ""]
            if "error" in r:
                lines += [f"- ERROR: {r['error']}", ""]
                continue
            lines += [
                f"- Access date: {r['access_date']}",
                f"- HTTP status: {r['http_status']}  |  Final URL: {r['final_url']}",
                f"- Title: {r['title']}",
                f"- Last updated: {r['last_updated']}",
                f"- Words extracted: {r['words']:,}",
                f"- HTML SHA-256: `{r['html_sha256']}`",
                f"- Snapshots: {r['html_snapshot']}, {r['text_snapshot']}",
                f"- Preview: {r['text_preview']}",
            ]
            if "warning" in r:
                lines.append(f"- WARNING: {r['warning']}")
            lines.append("")

    md_path = out_dir / "profile_report.md"
    md_path.write_text("\n".join(lines), encoding="utf-8")
    (out_dir / "profile_report.json").write_text(json.dumps(records, indent=2), encoding="utf-8")
    return md_path


def main():
    ap = argparse.ArgumentParser(description="Profile corpus PDFs and web pages.")
    ap.add_argument("--pdf-dir", default="./corpus", help="folder containing the PDFs")
    ap.add_argument("--url", action="append", default=[], help="extra URL to profile (repeatable)")
    ap.add_argument("--no-default-urls", action="store_true", help="skip the built-in PSEB URL")
    ap.add_argument("--out", default="./corpus_profile", help="output folder")
    args = ap.parse_args()

    out_dir = Path(args.out)
    snap_dir = out_dir / "snapshots"
    snap_dir.mkdir(parents=True, exist_ok=True)

    records = []
    pdf_dir = Path(args.pdf_dir)
    pdf_files = sorted(pdf_dir.glob("*.pdf")) if pdf_dir.exists() else []
    if not pdf_files and Path(".").glob("*.pdf"):
        pdf_dir = Path(".")
        pdf_files = sorted(pdf_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDFs found in {pdf_dir.resolve()}")
    for p in pdf_files:
        print(f"PDF  {p.name}")
        records.append(profile_pdf(p))

    urls = ([] if args.no_default_urls else DEFAULT_URLS) + args.url
    for u in urls:
        print(f"WEB  {u}")
        records.append(profile_url(u, snap_dir))

    report = write_report(records, out_dir)
    print(f"\nDone. Report: {report.resolve()}")


if __name__ == "__main__":
    main()
