# Pending report changes

Changes the code or tooling has already made that the report (`main.tex`), the master document and the diagrams do not yet reflect. Fix each one in the report later, add the `docs/DECISIONS.md` entry, then delete the row here.

| Date | What changed | Report says | Now | Where to fix | DECISIONS entry |
| --- | --- | --- | --- | --- | --- |
| 2026-10-17 | Provisional compliance embedding default | Compare multilingual sentence-transformer candidates on the planned benchmark before choosing | The backend defaults to `paraphrase-multilingual-mpnet-base-v2` for local operation; model evaluation remains pending | `main.tex` Chapter 3 embedding method and Chapter 6 evaluation | 2026-10-17 "Configure a provisional multilingual embedding default" |
| 2026-10-17 | PSEB page snapshot retrieval date | Last modified 19 August 2026; accessed 4 October 2026 | Current official snapshot retrieved 17 October 2026; last-modified date remains 19 August 2026 | `main.tex` Table `tab:corpus` | 2026-10-17 "Use a current, scope-filtered PSEB page snapshot" |
| 2026-10-16 | Scope: all 12 FYP-1 features attempted; unfinished work moves to FYP-2 | Chapter 6 objectives table lists "Main flows in FYP-2" | Update after Nov 8 to match what was actually cut | `main.tex` Chapter 6 objectives table (about line 2258) | 2026-10-16 "All 12 FYP-1 features" |
| 2026-10-16 | Limitations | Chapter 6 limitations (about line 2288) | Add every feature that is cut or partial on Nov 8 | `main.tex` Chapter 6 | same |
| 2026-10-16 | Data dictionary FR numbers | Data dictionary (approved 5 Oct) cites FR-1 to FR-6 and FR-22 to FR-26 under an older numbering; its pitch table has 5 feedback areas, FR-3 says clarity, confidence and content | Use the Chapter 4 numbering; reconcile the pitch areas | Data dictionary, before it goes into Chapter 4 or 5 | to add |
| 2026-10-16 | Sprint 4 corpus list | `SPRINT_PLAN.md` lists 5 documents and a stale section number | The corpus is 11 documents (`rag/corpus_manifest.md`) | `SPRINT_PLAN.md` | to add |
| 2026-10-17 | CI (NFR-23): ci.yml not yet confirmed on GitHub | main.tex now says the workflow is written but not yet confirmed on GitHub (hedged 2026-10-18) | `ci.yml` has never run on GitHub; it is untested. Do not claim CI runs on every PR until a test branch confirms it. Once confirmed, close this row. | `main.tex` wherever NFR-23 CI is described | to add |
| 2026-10-17 | Build-order (verification, admin, consent, guides) is internal only | No report text to change | The proposed build order is a team proposal; it stays in `docs/context/coding-plan.md` and is not added to the report. No report edit needed. Close this row once the build is finished and Chapter 6 is written. | `main.tex` Chapter 6 (if it appears there — check before closing) | to add |
| 2026-10-18 | Pitch rubric decided: four areas | main.tex FR-3 now uses the four areas (done 2026-10-18). Data dictionary table (five areas) and master `.docx` FR-3 and FR-10 rows still old | FR-3 and the `pitch_feedback.feedback_area` row use clarity, market_understanding, number_defensibility, pushback_handling | `data_dictionary_section.tex`; master `.docx` rebuild | 2026-10-18 pitch rubric |
| 2026-10-18 | Section 4.8 shows the 12 built screens; ten screens are D3 | main.tex Section 4.8 is the figure-grid version (done 2026-10-18) and says ten screens are added in D3 | After D3: swap new images into `Figures/gui/`, update the "ten screens" and uncovered-FR sentences, re-check against `SPEC_NAV_fig07-11.md` | `main.tex` Section 4.8 | 2026-10-18 Request match |
| 2026-10-18 | Roman-Urdu-Parl counts | main.tex now uses the file numbers (6,407,268 total; 6,365,808 train) | Master document still has 6,374,678 and 6,333,218. Hugging Face card not yet checked | Master document; HF card check | 2026-10-17 "Roman-Urdu-Parl split numbers discrepancy" |
| 2026-10-18 | Gulati et al. author order in `fypbib.bib` | Now follows arXiv (Gulati, Kumar, Agarwal, Sharma) | Springer ASONAM 2025 page not verified; change if the published order differs | `fypbib.bib` `ref:gulati2025` | none |
| 2026-10-18 | Master `.docx` rebuild | Old wording in FR-3, FR-10, 15.1, 15.4 | Rebuild from the master md after the midterm | `TheFoundersCarnet_Master_Document.docx` | none |

Closed on 2026-10-18 (done in `main.tex` and `fypbib.bib`, PR #3): final-7 dataset table and intro with licences; Parl licence and informal-source note; "None states a license" sentence removed; StartUp Investments blank rows; Crunchbase impossible dates and missing rates; tech filter wording ("at least"); tech niche in Chapter 2 scope; corpus path and manifest sentence; AI coding tools in Chapter 5; Mustafa et al. cited; Gulati et al. analysis and LinkedIn dataset limits; Roman Urdu critical analysis narrowed with Butt et al.; dataset limitations and resume optimizer pilot wording; ATS and old Resume-Job rows removed. The declaration date is for Ali to change.

The three rows that were here earlier are closed:

- Node.js 20 to 24: `main.tex` and the master document now say Node 24. Logged in `docs/DECISIONS.md` on 2026-10-15 and 2026-10-16.
- Python 3.11: `main.tex` already names Python 3.11. The master document names no Python version. Logged in `docs/DECISIONS.md` on 2026-10-15.
- GSD Core `.planning/` out of git: no report change needed. Logged in `docs/DECISIONS.md` on 2026-10-15.

## Verified facts behind the closed rows

- Node 20 reached end of life on 2026-04-30 (source: the Node.js release schedule, `nodejs/Release`, `schedule.json`).
- Node 24 is supported until 2028-04-30. It moves from active LTS to maintenance on 2026-10-20, which does not matter for this project.
- GSD Core declares `engines.node >= 24.0.0` in its `package.json`.
- Python 3.11.9 is the last 3.11 release with a Windows installer. Later 3.11 releases are source-only and security-fix only.

## Still open (undecided — add a row to this table and a DECISIONS entry once each is decided)

These items need a decision before the report can be finalised. They are listed here so nothing is forgotten.

- **DESIGN.md brand:** brand name, palette and logo not yet in the report.
- **Readiness reviewers:** who the 2 or 3 reviewers are is not stated in the report.
- **SECP cross-check:** how the SECP cross-check works is not described in the report.
- **Migration tool:** Alembic is planned but not confirmed; report does not name a migration tool.
- **Lint tool:** `CLAUDE.md` plans `ruff`; report names no lint tool. Once confirmed, add one line to the report.
- **Hosting:** report says "Railway or Render" everywhere. Once one is chosen, update `main.tex`, the master document and `CLAUDE.md`, and log it.
- **Feature freeze date:** not stated in the report; log it when confirmed.
