# Compliance corpus

Source: report Chapter 3 (3.3.2, corpus table `tab:corpus`) and Chapter 4 (FR-8, NFR-12 to NFR-14). The file-by-file list with hashes is `rag/corpus_manifest.md`.

The corpus is 11 logical sources: 9 PDF sources and two web pages (the FBR "register income tax" page and the PSEB Industry Facilitation page). The PSEB page and FBR page each have an HTML capture and a text copy; index one text copy per page. The VOSS PDF is a scanned source, so index its reviewed hand transcription and keep the scan inactive for provenance. The superseded PSEB PDF also stays inactive. The files are committed in `rag/data/` (public official documents, about 61 MB, so it is an exception to the raw-data rule). The manifest contains 15 physical file entries; the indexer uses 11 active source texts after skipping duplicate HTML and inactive PDFs. `rag/corpus_manifest.md` lists each file's source and SHA-256. Never replace a file without updating the manifest and `docs/DECISIONS.md`.

## Rules

- Index official sources only, at the versions the manifest lists. Never index a superseded version.
- Tax answers come from the Income Tax Ordinance and the Finance Act. The PSEB page is for registration, documents and fees only. Strip its tax sections before indexing.
- Companies Act 2017: index Parts I and IV and sections 462 to 473 only. Not the whole 418 pages.
- The Virtual One Stop Shop circular is a scanned page. Its reviewed hand transcription is in the manifest and is the file to index; the original PDF remains for provenance.
- Not in the corpus: the Iris login manual and the 2015 Urdu guide (excluded), and the Companies Regulations 2024 (still "being considered").
- Do not add a document without a row in the manifest and a reason in `docs/DECISIONS.md`.
- Every chunk keeps its document title, section, and the document's effective date, so a citation can show them (NFR-12, NFR-14).
- English only in FYP-1.

## How the manifest maps to the database

The manifest columns match the `corpus_document` table in the data dictionary: title, issuing_body, document_type, source_url, effective_date, consolidation_date, retrieved_at, content_sha256, scope_note, is_active. Load the manifest into that table; do not retype the values.

## Checking the files

`rag/corpus_profile/profile_corpus.py` profiles the folder and prints the SHA-256 of each file. Compare with the manifest before indexing. If a hash differs, the file is not the version the report names. Stop and tell the team.
