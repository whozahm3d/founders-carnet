# Pending report changes

Changes the code or tooling has already made that the report (`main.tex`), the master document and the diagrams do not yet reflect. Fix each one in the report later, add the `docs/DECISIONS.md` entry, then delete the row here.

| Date | What changed | Report says | Now | Where to fix | DECISIONS entry |
| --- | --- | --- | --- | --- | --- |
| 2026-11-12 | Private structured-response cache and sanitized gateway call logs | Gateway architecture describes prompt/evidence logging | Gateway persists sanitized per-attempt metadata only; private user-scoped structured cache expires after 24 hours and is cleared on account deletion; queue position is internal, not returned by APIs | `main.tex` Chapter 5 LLM Gateway and privacy description | 2026-11-12 "Private structured response cache and sanitized gateway call logs" |
| 2026-11-12 | Admin verification API and final appeal audit fields | FR-21/FR-26 describe one final appeal decision and an admin console showing escalated profiles, signals, scores, and reviewer-attributed reasons; route paths and appeal audit columns are not specified in the available report summary | Two admin-only endpoints expose the queue with per-signal score, outcome, input, and reason; final decisions retain reviewer ID/reason and appeals retain reviewer, outcome, reason, and decision time | `main.tex` Chapter 4 FR-21/FR-26 and backend API description | 2026-11-12 "Admin verification queue and appeal decision record" |
| 2026-11-12 | PostgreSQL and queue services | Architecture summary names PostgreSQL 16 and does not yet describe Redis/Celery in the local stack | Compose keeps PostgreSQL 17 and now includes Redis, an API container, and a Celery worker | `main.tex` Chapter 5 architecture and technology stack | 2026-11-12 "Keep PostgreSQL 17 and include Redis/Celery in step 1" |
| 2026-11-12 | Registration consent, role path, and fake LinkedIn provider | Earlier plan text cuts LinkedIn OAuth and does not describe registration consent or the new auth endpoints | Registration requires consent; role is a validated path parameter; fake LinkedIn provider, `consent_records`, `oauth_identities`, and immediate deletion disablement are implemented | `main.tex` Chapter 4 authentication and privacy requirements | 2026-11-12 "Registration consent, role transport, and fake LinkedIn boundary" |
| 2026-11-12 | Full talent verification and five signal audit | Report/coding plan does not describe talent verification storage or normalized signal rows | Talent has an optional GitHub profile, full verification status, five versioned signals, and `verification_signals` input/reason rows; SECP remains manual | `main.tex` Chapter 4 profile verification and privacy requirements | 2026-11-12 "Full verification for talent and manual SECP boundary" |
| 2026-11-10 | Matching sector/stage scoring | Sector, stage, and geography are hard candidate filters | Sector and stage contribute weighted fit scores; geography and eligibility rules remain hard filters | `main.tex` matching architecture and ranking description | 2026-11-10 "Sector and stage remain weighted matching factors" |
| 2026-10-17 | Provisional compliance embedding default | Compare multilingual sentence-transformer candidates on the planned benchmark before choosing | The backend defaults to `paraphrase-multilingual-mpnet-base-v2` for local operation; model evaluation remains pending | `main.tex` Chapter 3 embedding method and Chapter 6 evaluation | 2026-10-17 "Configure a provisional multilingual embedding default" |
| 2026-10-17 | PSEB page snapshot retrieval date | Last modified 19 August 2026; accessed 4 October 2026 | Current official snapshot retrieved 17 October 2026; last-modified date remains 19 August 2026 | `main.tex` Table `tab:corpus` | 2026-10-17 "Use a current, scope-filtered PSEB page snapshot" |
| 2026-10-16 | Scope: all 12 FYP-1 features attempted; unfinished work moves to FYP-2 | Chapter 6 objectives table lists "Main flows in FYP-2" | Update after Nov 8 to match what was actually cut | `main.tex` Chapter 6 objectives table (about line 2258) | 2026-10-16 "All 12 FYP-1 features" |
| 2026-10-16 | Limitations | Chapter 6 limitations (about line 2288) | Add every feature that is cut or partial on Nov 8 | `main.tex` Chapter 6 | same |
| 2026-10-16 | Data dictionary FR numbers | Data dictionary (approved 5 Oct) cites FR-1 to FR-6 and FR-22 to FR-26 under an older numbering; its pitch table has 5 feedback areas, FR-3 says clarity, confidence and content | Use the Chapter 4 numbering; reconcile the pitch areas | Data dictionary, before it goes into Chapter 4 or 5 | to add |
| 2026-10-16 | Sprint 4 corpus list | `SPRINT_PLAN.md` lists 5 documents and a stale section number | The corpus is 11 documents (`rag/corpus_manifest.md`) | `SPRINT_PLAN.md` | to add |
| 2026-10-17 | Roman-Urdu-Parl split numbers | 6,374,678 total (6,333,218 train, 20,719 validation, 20,741 test) | Files show 6,407,268 total (6,365,808 train, 20,719 validation, 20,741 test). Check HF dataset card, then update report to file numbers unless source for 6,333,218 is found | `main.tex` Chapter 3 external datasets table | 2026-10-17 "Roman-Urdu-Parl split numbers discrepancy" |
| 2026-10-17 | Crunchbase impossible date ranges | Date ranges described without impossible outlier bounds | Both Crunchbase files have impossible dates: success/fail founded_at 1015 to 2914; investments first_funding_at as early as year 0001 | `main.tex` Chapter 3 data quality | to add |
| 2026-10-17 | ATS mean resume text length | 376 characters | Observed mean resume text is 376.9 characters; report could say 377 | `main.tex` Chapter 3 ATS dataset description | to add |
| 2026-10-17 | Crunchbase Success/Fail missing rates | Report mentions missing founded_at (no rate given) | Missing rates: founded_at 22.9%, country_code 10.5%, category_list 4.7%. Add these rates to Chapter 3 data quality notes for this dataset | `main.tex` Chapter 3 data quality | 2026-10-17 "Tech-niche focus and dataset search/swap rules" |
| 2026-10-17 | Crunchbase Investments funding_total_usd | Report does not state a missing rate or a cleaned max value | True missing (treating "-" as null): ~24.7% (40,907 non-null of 54,294). After cleaning: median $2 M, max ~$30 B. Add to Chapter 3 data quality | `main.tex` Chapter 3 data quality | 2026-10-17 "Tech-niche focus and dataset search/swap rules" |
| 2026-10-17 | Tech niche: project scope | Check whether the report explicitly names tech as the one niche it targets; if not, state it | Team decision 2026-10-17: the platform targets one niche — tech. Reason: scope discipline. | `main.tex` Chapter 1 scope or Chapter 3 intro; wherever the target niche is first stated | 2026-10-17 "Tech-niche focus and dataset search/swap rules" |
| 2026-10-17 | Dataset search and swap rule | No rule stated in the report | Team plan: search Kaggle and Hugging Face after D2 or mid-term; any swap must update the report's dataset table before the swap is used. | `main.tex` Chapter 3 external datasets intro | to add |
| 2026-10-17 | Corpus: location and integrity | Report's corpus section does not state where files are committed or that hashes exist | 11 corpus files committed in `rag/data/` (~59 MB); SHA-256 hashes in `rag/corpus_manifest.md`. Check whether Chapter 3 or Chapter 4 should name the path and manifest. | `main.tex` Chapter 3 or 4 corpus section | to add |
| 2026-10-17 | Chapter 5 development methods: AI tools | Report's tools text does not mention AI coding agents | Team uses Claude Code, Codex, Antigravity and Gemini. All read `AGENTS.md` and `CLAUDE.md`. Skills sync via `scripts/sync_agent_skills.py`. Check whether Chapter 5 should name these tools and the guard-rail files. | `main.tex` Chapter 5 development methods | to add |
| 2026-10-17 | CI (NFR-23): ci.yml not yet confirmed on GitHub | Report or NFR-23 may claim CI runs on every pull request | `ci.yml` has never run on GitHub; it is untested. Do not claim CI runs on every PR until a test branch confirms it. Once confirmed, close this row. | `main.tex` wherever NFR-23 CI is described | to add |
| 2026-10-17 | Build-order (verification, admin, consent, guides) is internal only | No report text to change | The proposed build order is a team proposal; it stays in `docs/context/coding-plan.md` and is not added to the report. No report edit needed. Close this row once the build is finished and Chapter 6 is written. | `main.tex` Chapter 6 (if it appears there — check before closing) | to add |

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
