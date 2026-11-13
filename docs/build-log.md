# Build log

One entry per finished piece of work, newest first. This is what we use to write Chapter 6 and to see what was cut. Differences from the report do not live only here: they also go in `docs/DECISIONS.md` (with the reason) and `docs/pending-report-changes.md`.

## Entry format

```
## YYYY-MM-DD: feature, short title (who)

- **Feature and IDs:** (for example Compliance assistant, FR-8, NFR-12)
- **Built:**
- **Tested:** (what was run and the result; say what was not tested)
- **Cut or partial:**
- **Differs from the report?** (no, or what and why; link the DECISIONS entry)
```

## Entries

## 2026-11-13: Compliance evaluation mappings and dev retrieval (Codex)

- **Feature and IDs:** Compliance assistant and evaluation, FR-8, NFR-12, NFR-13, NFR-14, NFR-20.
- **Built:** Fixed the schedule heading detector so a legal-text reference to another schedule cannot reset the Seventh Schedule heading path. Updated q003 to the Fast Track fee chunk and q008 to the confirmed Iris attachment-list chunk; preserved the fixed 6/14 split and generated no gold answers. Fixed hybrid RRF’s candidate limit and reserved E5 passage-prefix tokens when splitting chunks. The corrected corpus has 240 chunks (the earlier 225 count included Finance Act chunks lost to the heading parsing bug).
- **Tested:** MPNet and E5 dense, BM25, and hybrid retrieval ran on the 6-question dev split only; results are in `rag/evaluation/results/retrieval.csv`. Full pytest with JUnit output: 110 passed, 1 Starlette/AnyIO deprecation warning. Injection suite: fake output changed 0/10 cases. All answerable mappings resolve; q003 contains item (35) and both amounts. No Gemini call or database run.
- **Cut or partial:** BGE-M3 download has no usable weights yet and is being monitored against the 20-minute no-progress cutoff. Test-split and end-to-end Gemini baseline were not run. Dev has only 3 answerable questions and serves as a pipeline check, not a model ranking.
- **Differs from the report?** No scope or behavior change from the report; the chunk count correction fixes a parser bug in the earlier count.

## 2026-11-13: Resume embedding downloads and prepare labeled dev questions (Codex)

- **Feature and IDs:** Compliance corpus evaluation, FR-8, NFR-12, NFR-13, NFR-20.
- **Built:** Resumed the MPNet snapshot and confirmed it loads on CPU; added `supporting_chunk_ids` to the existing question records, set q009/q010 outside indexed scope, and changed the loader to respect the file's fixed 6/14 split. Recorded proposed mappings without scoring. Updated the CSV-driven results report with current limitations.
- **Tested:** MPNet reports max sequence length 128, vector dimension 768, and 147 of 225 source chunks over the limit before truncation-safe splitting. Question schema/split test passed (1 passed). Confirmed no Docker command is available and `GEMINI_API_KEY` is unset without printing it.
- **Cut or partial:** E5 download is resumable but incomplete; BGE-M3 has not started. Docker database startup/Alembic, model indexing, retrieval metrics, and Gemini calls were not run. Stopped at the database gate as requested. Proposed chunk mappings are awaiting user confirmation; q008 is unmapped because Finance Act section 1 is excluded from scope.
- **Differs from the report?** No embedding default was changed. The measured MPNet truncation count and current execution limitations are in the CSV-driven `rag/evaluation/RESULTS.md`.

## 2026-11-13: Compliance RAG retrieval, guarded answers, API and evaluation harness (Codex)

- **Feature and IDs:** Compliance assistant, FR-8, NFR-12, NFR-13, NFR-14, NFR-20.
- **Built:** Reused `compliance_chunks` and added heading path, effective date and corpus version metadata in Alembic revision 0005; added configurable SentenceTransformer embeddings, dense/BM25/hybrid RRF retrieval, versioned delimited-evidence JSON answer handling, citation/number/date/scope checks, and `POST /api/v1/compliance/questions`. Added CSV evaluation/report tooling and retained the existing 20 question records without generating answers. Pinned setuptools 84.2.1, wheel 0.45.1, sentence-transformers 6.1.0, torch 2.15.0 CPU, and rank-bm25 0.2.2.
- **Tested:** Full fake-provider suite: 105 passed, 1 existing Starlette/AnyIO deprecation warning. Test-case CSV records TC-04, TC-05, invented amount, bad citation, hash mismatch, and 10 injection cases (fake output changed 0/10). Alembic upgrade test passed. Evaluation CSVs show split seed 42 (16 dev, 4 test); retrieval and end-to-end rows are empty because section labels lack chunk-id mappings and model downloads failed. No Gemini call or live database indexing was run.
- **Cut or partial:** MPNet's weight download remained incomplete at 67,108,700 bytes; the sequential loader did not reach multilingual-E5 or BGE-M3. No model comparison, embeddings, pgvector indexing, retrieval metrics, or end-to-end/no-retrieval evaluation was run. Finance Act retains 32 of 93 chunks (61 dropped). Existing question file has 20 records, not the requested 10 blank starter rows; it was preserved rather than overwritten.
- **Differs from the report?** Implementation details and the Finance Act scope difference are recorded in `docs/DECISIONS.md`; see the dated rows in `docs/pending-report-changes.md`.

## 2026-11-13: Scope Finance Act chunks for founder compliance (Codex)

- **Feature and IDs:** Compliance corpus scope, FR-8, NFR-12, NFR-13.
- **Built:** Filtered Finance Act 2026 to section 5 amendments of the Income Tax Ordinance; no Companies Act or SECP fee amendments were present. The filtered set has 32 chunks. Recorded the report difference in `docs/DECISIONS.md` and `docs/pending-report-changes.md`.
- **Tested:** Cache and PDF hashes matched for all active PDFs; the Finance Act scope tests passed. No embedding or retrieval evaluation was run in this piece.
- **Cut or partial:** Other Finance Act amendments remain excluded unless the report scope is revised.
- **Differs from the report?** Yes; see the dated decision and pending report row.

## 2026-11-13: Cache and correct compliance corpus extraction (Codex)

- **Feature and IDs:** Compliance corpus ingestion and chunking, FR-8, NFR-12, NFR-13, NFR-14.
- **Built:** Added a hash-keyed JSONL page cache for active PDFs and wired the indexer to reuse it. Corrected Ordinance scoping for section 2(62A), section 154A and First Schedule Part III Division IVA; corrected Companies Act part boundaries and TOC exclusion; labeled section 23 as unreadable rather than guessing. Added document-local text cleanup, definition-number paths, and fee-item footnote ordering. Finance Act scope was not changed.
- **Tested:** `rag/.venv/Scripts/python.exe -m pytest rag/tests -q` passed (26 passed). All 8 active PDF caches have matching source hashes and contiguous page records (839, 256, 418, 13, 8, 28, 6, and 14 pages); the blank first Sandbox page is retained. No embedding, API, or database operation was run.
- **Cut or partial:** The refreshed Finance Act chunking yields 93 chunks (the previous 217 count predates the parser fixes); keyword counts are diagnostic only. No Step 2 embedding or schema work was performed.
- **Differs from the report?** No report scope was changed; the Finance Act chunk partition changed with the chunker fixes.

## 2026-11-13: Normalize text corpus hashes on Windows checkouts (Codex)

- **Feature and IDs:** Compliance corpus integrity, FR-8, NFR-12, NFR-13.
- **Built:** Added LF-first, exact-raw-fallback verification for `.txt` and `.html`; other files, including PDFs, use raw bytes. Added reviewed-text extraction, Companies Act and Income Tax scope filters, heading paths, and clause-safe approximately 500-token chunking. HTML captures and inactive PDFs were skipped.
- **Tested:** `rag/.venv/Scripts/python.exe -m pytest rag/tests -q` passed (21 passed). All 15 manifest hashes passed. pypdf extracted all active PDFs with text and no extraction errors. Chunk totals: 496 across 11 active source texts. Generated 10 Companies Act samples and 3 each from the Finance Act and Seventh Schedule for manual review.
- **Cut or partial:** Embeddings, indexing, retrieval, answer generation, endpoint, and evaluation were not part of this step.
- **Differs from the report?** No; see the 2026-11-13 entry in `docs/DECISIONS.md` for the verifier behavior and mixed manifest text-hash convention.

## 2026-10-18: Auth refactoring, role route guards & removal of demo role switcher (Shahzeb, with Antigravity)

- **Feature and IDs:** Account & Profile Foundations, Access Control (FR-22, FR-23, NFR-4, NFR-5)
- **Built:**
  - Removed auto-login of the default demo founder entirely from [AuthContext.tsx](file:///c:/Users/Dell/Desktop/founders-carnet/frontend/src/context/AuthContext.tsx). Without a saved session, `/` and all protected routes (`/founder/*`, `/talent/*`, `/mentor/*`, `/investor/*`, `/admin/*`) redirect directly to `/login`.
  - Added role route protection in [DashboardLayout.tsx](file:///c:/Users/Dell/Desktop/founders-carnet/frontend/src/components/layout/DashboardLayout.tsx): users navigating to another role's routes (e.g. founder navigating to `/talent/*`) are intercepted and returned to their own role dashboard.
  - Added logged-in redirects on [LoginPage](file:///c:/Users/Dell/Desktop/founders-carnet/frontend/src/app/(auth)/login/page.tsx) and [RegisterPage](file:///c:/Users/Dell/Desktop/founders-carnet/frontend/src/app/(auth)/register/page.tsx): logged-in users visiting `/login` or `/register` are redirected to their role dashboard.
  - Added a role selector on `/login` in mock mode only (`NEXT_PUBLIC_USE_MOCK=true`), allowing any email and password to log into any role for testing.
  - Completely removed the "Demo Role Switcher" bar and `switchRoleForDemo`. Role changes now require logging out and logging back in.
  - Top bar and sidebar logout actions clear session storage and return to `/login`.
  - Documented TODO for replacing mock token localStorage with `httpOnly` cookie set by FastAPI backend.
- **Tested:** `npm run build` completed successfully (TypeScript checks passed, 24 static routes generated with zero errors).
- **Differs from the report?** No.

## 2026-10-18: Complete Founder wireframe build (02, 03, 04, 05, 06, 07) & zero-404 route coverage (Shahzeb, with Antigravity)

- **Feature and IDs:** Founder workspace screens & ecosystem navigation (FR-1, FR-2, FR-3, FR-7, FR-28)
- **Built:**
  - **Founder Dashboard ([04_Founder_Dashboard.png](file:///c:/Users/Dell/Desktop/founders-carnet/docs/context/wireframes/04_Founder_Dashboard.png))**: Removed all invented content (Compliance Assistant, Job Listings, 0-100 scales, "FR-x" labels). Rebuilt with exact wireframe copy and elements: Verified banner, 3.1 / 5 Readiness score with progress bar, "AI-generated" pill, and "View breakdown" link, interactive Next actions checklist, Recent pitch feedback sessions with scores, and Match preview with 3 cards.
  - **Sidebar Alignment**: Fixed navigation items to match wireframes: Dashboard, Profile, Readiness score, Pitch practice, Session feedback, Matches. Formatted nav links so icon and label remain on a single line (`white-space: nowrap`), with clean active states.
  - **Zero-404 Route Coverage**: Implemented all placeholder routes across all 5 roles using [PlaceholderPage](file:///c:/Users/Dell/Desktop/founders-carnet/frontend/src/components/ui/PlaceholderPage.tsx) (`/talent/profile`, `/talent/resume`, `/talent/jobs`, `/talent/matches`, `/mentor/profile`, `/mentor/requests`, `/investor/profile`, `/investor/founders`, `/investor/requests`, `/admin/dashboard`).
  - **Startup Profile ([02_Founder_Profile_2x.png](file:///c:/Users/Dell/Desktop/founders-carnet/docs/context/wireframes/02_Founder_Profile_2x.png))**: Built full form (Startup name, One-line description, Sector dropdown with 7 sectors, Team description, optional Portfolio/Product link) and right Review status card with checklist (LinkedIn connected, Profile completeness 70%, Link check pending).
  - **Readiness Score ([03_Readiness_Score.png](file:///c:/Users/Dell/Desktop/founders-carnet/docs/context/wireframes/03_Readiness_Score.png))**: Built 7-dimension rubric cards (Problem clarity 4/5, Market definition 2/5, Differentiation 3/5, Business model 3/5, Traction 3/5, Team 4/5, Go-to-market 3/5) with gap pills, suggested action links, 3.1 / 5 summary card, and "Recalculate score" action.
  - **Pitch Practice ([05_Pitch_Practice.png](file:///c:/Users/Dell/Desktop/founders-carnet/docs/context/wireframes/05_Pitch_Practice.png))**: Built interactive chat with AI investor persona, persona/startup selector dropdowns, live multi-turn conversation, 4-dimension live rubric (Clarity, Market understanding, Defensibility of numbers, Handling pushback), session timer, and "End session" flow.
  - **Session Feedback ([06_Pitch_Feedback.png](file:///c:/Users/Dell/Desktop/founders-carnet/docs/context/wireframes/06_Pitch_Feedback.png))**: Built feedback by rubric (3.0 / 5 session average), struggled questions list with actionable coaching suggestions, full transcript expander, progress across sessions (Sessions 1, 2, 3), and interactive next steps checklist.
  - **Match Feed ([07_Match_Feed.png](file:///c:/Users/Dell/Desktop/founders-carnet/docs/context/wireframes/07_Match_Feed.png))**: Built filter pills (All, Mentors, Investors, Sector, Stage) and match cards with similarity scores (Ayesha Qureshi 92%, Hamza Iqbal 88%, Sana Rauf 84%, Priya Shah 76% accepted), sector/stage fit tags, and mutual contact reveal protocol.
- **Tested:** `npm run build` compiled successfully (Turbopack, TypeScript passed, 24 static routes generated with zero errors).
- **Differs from the report?** No.

## 2026-10-18: Mobile, tablet & desktop responsive layout across all frontend screens (Shahzeb, with Antigravity)

- **Feature and IDs:** UI design system & responsive foundations across all roles (FR-22, FR-23, NFR-4, NFR-5)
- **Built:**
  - Added responsive viewport configuration in [src/app/layout.tsx](file:///c:/Users/Dell/Desktop/founders-carnet/frontend/src/app/layout.tsx) (`width=device-width, initialScale=1, maximumScale=5`).
  - Added global responsive layout tokens and horizontal scroll guards (`overflow-x: hidden`, `min-width: 320px`) in [src/app/globals.css](file:///c:/Users/Dell/Desktop/founders-carnet/frontend/src/app/globals.css).
  - Enforced touch target guidelines (min-height 44px on mobile) and 16px minimum input font size to prevent automatic iOS safari zoom in `Input.module.css`, `Button.module.css`, and `ConsentBox.module.css`.
  - Built mobile slide-in drawer for [Sidebar.tsx](file:///c:/Users/Dell/Desktop/founders-carnet/frontend/src/components/layout/Sidebar.tsx) with backdrop overlay, Escape key listener, auto-close on route change, aria-controls, and drawer close button.
  - Implemented tablet icon rail (68px) with role icons and tooltip titles for widths 640px to 1023px.
  - Maintained canonical wireframe 240px persistent sidebar for laptop (1024px to 1439px), tested for common 1366x768 screens with zero horizontal overflow.
  - Implemented 1280px max-width content capping for large desktop (1440px+).
  - Built responsive split-screen auth layout in `(auth)/layout.module.css` (short brand header on mobile, split-panel on tablet, laptop, and desktop).
  - Built [Dashboard.module.css](file:///c:/Users/Dell/Desktop/founders-carnet/frontend/src/components/layout/Dashboard.module.css) responsive grid classes (1 col on mobile, 2 col on tablet, 4 col on laptop/desktop for stats and matches; vertical button stack on mobile with full width).
  - Added self-contained horizontal scroll container (`.tableScrollContainer`) for admin data tables and wide content to prevent full-page horizontal scrolling.
- **Tested:** `npm run build` completed cleanly (TypeScript passed, 10 static routes generated with zero prerender errors). Verified responsiveness across 320px, 375px, 768px, 1024px, 1366px, and 1920px.
- **Differs from the report?** No.

## 2026-10-18: Frontend foundations, shared components & role shells (Shahzeb, with Antigravity)

- **Feature and IDs:** Account and profile foundations, UI design system (FR-22, FR-23, NFR-4, NFR-5)
- **Built:**
  - Initialized Next.js 16 (Turbopack, TypeScript, App Router) in `/frontend` matching Node 24 target.
  - Implemented design system tokens in `globals.css` (Inter font, dark-charcoal sidebar `#2D2D2D`, accent blue `#0066FF`, crisp typography, card elevation, border system).
  - Created 10 UI components: `Button`, `Input`, `Select`, `Textarea`, `Card`, `Badge`, `ProgressBar`, `StatCard`, `MatchCard`, `EmptyState`, `Spinner`, `ConsentBox` (with barrel exports in `src/components/ui`).
  - Created layout shell: persistent `Sidebar` matching wireframes, `PageHeader`, `DashboardLayout` with live demo role switcher.
  - Built typed auth layer (`src/lib/auth.ts`, `src/types/auth.ts`, `AuthContext`) supporting session storage and demo quick logins for 5 roles.
  - Built `(auth)` pages: `/login` with credentials & quick switches, `/register` with role picker and PECA 2016 / NFR-6 consent box.
  - Built dashboard shells for 5 roles: `/founder/dashboard` (with wireframe layout, readiness stats, pitch practice card, and ecosystem match cards), `/talent/dashboard`, `/mentor/dashboard`, `/investor/dashboard`, `/admin/dashboard`.
- **Tested:** `npm run build` compiled cleanly (Turbopack, TypeScript checks passed, 10 static routes generated).
- **Cut or partial:** Backend API connection is currently mocked in `lib/auth.ts` until backend endpoints land.
- **Differs from the report?** No.

## 2026-10-17: Gemini provider timeout diagnosis (Codex)

- **Feature and IDs:** Compliance assistant, FR-8, NFR-8, NFR-19.
- **Built:** Replaced hidden SDK retries with visible bounded retries; added safe provider/network/quota/model error classification, a distinct configured fallback, a separate no-evidence diagnostic command, evidence and prompt limits, and one traceback log per failed generation. Failure-query persistence remains best-effort and does not replace the provider error.
- **Tested:** Backend suite: 56 passed (one existing Starlette/AnyIO deprecation warning); RAG suite: 11 passed. Mocked tests cover success, timeout, primary retry before fallback, quota no-retry, safe logging, and context limits. Live no-evidence diagnostic used runtime model `gemini-3.8-flash` and returned Google HTTP 504 after two attempts (~118,675 ms total). The configured fallback resolved to the same model, so no alternate model was called. No credential was printed.
- **Cut or partial:** The minimal prompt also timed out, so retrieved context size is not the cause of that failure. No live compliance answer was attempted. No 429 was observed, so account quota status remains unknown. The runtime model conflicts with the repository's Gemini 2.5-and-below policy; no model or `.env` value was changed. Check AI Studio access and status, and use a distinct fallback only if available to this account and consistent with the project policy.
- **Differs from the report?** No API or grounding contract changed. Runtime configuration differs from the repository model policy; resolve through an approved local configuration.

## 2026-10-17: Gemini timeout and prompt handling (Codex)

- **Feature and IDs:** Compliance assistant, FR-8, NFR-8, NFR-19.
- **Built:** Set a configurable 60-second Gemini request timeout, bounded one-retry handling for transient HTTP failures excluding quota errors, generation timing/model/passage/prompt-size logs without prompt text, and duplicate plus oversized evidence handling that preserves retrieval rank and citations.
- **Tested:** Backend suite: 49 passed; RAG suite: 11 passed; Google Gen AI SDK HTTP options validated using the installed SDK. No live Gemini call was made.
- **Cut or partial:** Live 504 recovery is not verified against Google; SDK retry behavior is bounded and covered by its configured options.
- **Differs from the report?** No API or grounding behavior changed. main.tex was not present in this checkout, so only repo architecture rules and the FR-8 contract were checked.

## 2026-10-17: Compliance corpus ingestion recovery (Codex)

- **Feature and IDs:** Compliance assistant, FR-8, NFR-12, NFR-13, NFR-14, NFR-20.
- **Built:** Made repeated indexing repair missing chunks and null or stale-model embeddings without duplicating rows. Added a PostgreSQL vector-dimension filter and retrieval regression coverage for incompatible dimensions.
- **Tested:** Backend suite: 46 passed; RAG suite: 11 passed; git diff --check passed. The indexer was run against the configured SQLite database but stopped before writing because the model cache lacks required files and outbound Hugging Face access is blocked. A read-only follow-up confirmed database counts remain 0 documents, 0 chunks, and 0 embeddings. Real retrieval is not verified.
- **Cut or partial:** Real corpus ingestion and the SECP question retrieval remain pending a complete local model download. No PostgreSQL service is configured for this run.
- **Differs from the report?** No; the work preserves the report's source-grounded citations and abstention behavior.

## 2026-10-17: Compliance corpus diagnostics (Codex)

- **Feature and IDs:** Compliance assistant, FR-8, NFR-12, NFR-13, NFR-14, NFR-20.
- **Built:** Added content-free index and retrieval counts to compliance server logs. Added tests for zero-index abstention and the SECP question using an exact excerpt from the manifest-listed position paper.
- **Tested:** Backend suite: 45 passed; RAG suite: 11 passed; one existing Starlette/AnyIO deprecation warning. Read-only check found 0 documents, chunks, embeddings, or model-compatible chunks in the configured database (SQLite). No ingestion or model download was run.
- **Cut or partial:** Corpus ingestion remains required; the existing command is `python -m app.services.corpus_indexer`. PostgreSQL/pgvector is defined in migrations and Compose but is not the database currently configured by the local `.env`.
- **Differs from the report?** No; this improves diagnostics for the report's required retrieval and abstention flow.

## 2026-10-17: Compliance failure visibility and safe abstention (Codex)

- **Feature and IDs:** Compliance assistant, FR-8, NFR-8, NFR-11, NFR-12, NFR-13, NFR-14, NFR-20.
- **Built:** Added traceback logging for retrieval and answer-generation failures; made failed-query persistence best-effort so it cannot mask the primary error; bounded Gemini requests to 30 seconds with SDK retries disabled; replaced a non-placeholder Gemini value in `.env.example`.
- **Tested:** Backend suite: 43 passed; RAG suite: 11 passed; one existing Starlette/AnyIO deprecation warning. Verified settings without printing credentials, confirmed the local database has zero active documents and zero embedded chunks, and checked the example key remains a placeholder. No live Gemini request or corpus indexing.
- **Cut or partial:** The local SQLite database currently has no active compliance documents or embedded chunks. Indexing still requires an embedding model download; live provider behavior still requires the user's own key and quota.
- **Differs from the report?** No. Grounded answers, citations, and abstention remain unchanged.

## 2026-10-17: Local pgvector database setup (Codex)

- **Feature and IDs:** Compliance assistant and backend persistence, FR-8, NFR-12, NFR-14, NFR-20, NFR-22.
- **Built:** Added a local PostgreSQL 17 pgvector Compose service bound to localhost, a persistent data volume, and health check. Updated safe environment examples and backend setup instructions.
- **Tested:** Compose configuration not run because Docker Desktop and WSL are not installed. No database migration or corpus indexing ran.
- **Cut or partial:** WSL/Docker installation, database startup, Alembic migration, model download, and corpus indexing remain.
- **Differs from the report?** No; this implements the report's PostgreSQL/pgvector stack and planned Compose setup.

## 2026-10-17: Compliance local configuration fix (Codex)

- **Feature and IDs:** Compliance assistant, FR-8, NFR-12, NFR-13, NFR-14, NFR-20.
- **Built:** Backend settings now load the repository-root `.env` regardless of the launch directory, map its documented JWT names, ignore frontend-only variables, and select the installed psycopg 3 driver for bare PostgreSQL URLs. Added a provisional report-listed multilingual embedding default. Removed a Gemini credential accidentally placed in `.env.example`.
- **Tested:** Full backend suite: 36 passed, 1 existing Starlette/AnyIO deprecation warning. `.env.example` check confirmed the key field is empty and the embedding variable is present. No live Gemini request, model download, corpus indexing, or PostgreSQL connection was run.
- **Cut or partial:** End-to-end compliance still requires a valid Gemini key, PostgreSQL with pgvector, corpus indexing, and the gold-set evaluation.
- **Differs from the report?** Yes, the embedding model is an operational default before benchmark validation; see `docs/DECISIONS.md` (2026-10-17) and `docs/pending-report-changes.md`.

## 2026-10-17: Matching, readiness, and pitch backend slices (Codex)

- **Feature and IDs:** Ecosystem matching baseline, FR-7, FR-10, FR-13, FR-29, NFR-3, NFR-6, NFR-15, NFR-20; readiness, FR-2, NFR-2; pitch simulator, FR-3, FR-28; versioned schema, NFR-22.
- **Built:** Added consented mentor, investor, and talent match profiles; shared configured embeddings and pgvector candidate retrieval; deterministic cosine-plus-five-factor ranking with stored explanations; two-sided acceptance and contact reveal; mentor open/closed handling; and investor visibility checks for verified startups with readiness. Added validated seven-dimension readiness assessments and rubric history. Added persona-based multi-turn pitch sessions, saved turns, incomplete-session handling, final clarity/confidence/content scores, and founder history. The shared Gemini Gateway queues requests above five concurrent calls (NFR-2). Added migration 0004.
- **Tested:** Backend suite: 34 passed. RAG suite: 11 passed. Empty-database migration upgrade passed. Focused tests cover role and ownership checks, consent, investor gating, closed mentors, contact privacy, readiness structure/history, pitch completion/incomplete transcripts. Matching profile tests use a fake encoder and pitch/readiness tests use a fake gateway.
- **Cut or partial:** GitHub skill signal is deferred per the coding-plan cut line. PostgreSQL/pgvector execution, live Gemini calls, selected embedding model, latency target, and the seeded demo ranking evaluation were not run. Compliance still needs a hand-verified 20–22 question gold set and a formal run. The scope remains uncalibrated for readiness.
- **Differs from the report?** No. Numeric weights are not specified in the report, so the pilot defaults and 50/50 cosine/factor blend are recorded as revisable in docs/DECISIONS.md.

## 2026-10-17: Compliance corpus ready for a VOSS transcription smoke test (Codex)

- **Feature and IDs:** Compliance assistant, FR-8, NFR-12, NFR-13, NFR-14, NFR-20.
- **Built:** Added the reviewed hand transcription of the FBR VOSS scan, marked the PDF inactive for indexing while retaining it for provenance, and aligned the manifest and corpus instructions. Existing manifest-driven ingestion now treats the active TXT as the source.
- **Tested:** SHA-256 verification passed for all 15 manifest entries (13 active format entries). The active VOSS transcription indexed into an in-memory SQLite test database as two chunks using a fake encoder. No production database was changed.
- **Cut or partial:** Feature 1 is not runtime-complete yet: the corpus has not been indexed, EMBEDDING_MODEL_NAME and Gemini credentials are not configured, PostgreSQL/pgvector indexing has not been run, and the gold-set evaluation has not been created or run. The existing endpoints and ingestion pipeline remain available once configured.
- **Differs from the report?** No corpus source change. The hand-transcription method is allowed by docs/context/corpus.md; the manifest records its provenance and hash. See docs/DECISIONS.md (2026-10-17, “Hand-transcribe the VOSS circular for indexing”).

## 2026-10-17: Complete backend account and founder profile foundations (Codex)

- **Feature and IDs:** Account and profile foundations, FR-22, FR-23, FR-1, NFR-4, NFR-5, NFR-9, NFR-22.
- **Built:** Public registration now accepts founder, talent, mentor, and investor roles, but not admin. Logout increments the user's token version so all previously issued access tokens stop working. Added consent-gated founder profile and startup create/read/update routes for business and traction data; verification remains server-controlled and defaults false. Added migration `0003` for the founder profile, startup, and token-version schema. Validation errors no longer echo request values such as passwords.
- **Tested:** Backend suite: 27 passed, including logout invalidation, expired tokens, role restrictions, profile consent, startup ownership data, password redaction, and empty-database migration upgrade. PostgreSQL migration was not run. One unrelated Starlette/AnyIO deprecation warning remains.
- **Cut or partial:** OAuth and a separate admin-provisioning CLI remain out of this slice. Consent withdrawal and deletion lifecycle are in Feature 10. Existing local databases need `python -m alembic upgrade head` before use.
- **Differs from the report?** No. The profile supports one founder profile with multiple startup records, and only explicit consented profile data is stored.

## 2026-10-17: Add the dated PSEB corpus snapshot (Codex)

- **Feature and IDs:** Compliance assistant, FR-8, NFR-12, NFR-13, NFR-14, NFR-20.
- **Built:** Added the official PSEB HTML capture retrieved 17 Oct 2026 and a reviewed TXT extract limited to registration documents, fees, renewal, payment, and processing. Marked the old PDF inactive without deleting it. Updated the manifest hashes and corpus summary. Fixed the Income Tax scope filter to match section 154A exactly, preventing adjacent section 154B from being included.
- **Tested:** Verified SHA-256 for all 14 manifest file entries (13 active format entries). RAG suite: 11 passed. Backend suite: 20 passed. One unrelated Starlette/AnyIO deprecation warning remains. No database indexing, embedding model load, or Gemini request was run.
- **Cut or partial:** VOSS OCR or reviewed transcription, embedding model selection/configuration, actual corpus indexing, and the gold-question evaluation remain.
- **Differs from the report?** The active PSEB snapshot was retrieved 17 Oct rather than the report's 4 Oct date. The page's last-modified date remains 19 Aug. The report update is tracked in `docs/pending-report-changes.md`; see `docs/DECISIONS.md` (2026-10-17, "Use a current, scope-filtered PSEB page snapshot").

## 2026-10-17: Pin bcrypt for Passlib compatibility (Codex)

- **Feature and IDs:** Account foundations, FR-22, FR-23, NFR-4.
- **Built:** Pinned `bcrypt` to 4.0.1 alongside Passlib 1.7.4 to avoid the known missing `bcrypt.__about__` warning. Password hashing code and the bcrypt hash scheme are unchanged.
- **Tested:** Installed the pin in `backend/.venv`; `pytest tests/test_auth.py -q` passed (4 passed). The Passlib/bcrypt warning no longer appears. One unrelated Starlette/AnyIO deprecation warning remains.
- **Cut or partial:** None.
- **Differs from the report?** No.

## 2026-10-17: Compliance source scope filtering (Codex)

- **Feature and IDs:** Compliance assistant, FR-8, NFR-12, NFR-13, NFR-14.
- **Built:** Added pre-chunking filters for the Companies Act (Parts I and IV, sections 462 to 473) and Income Tax Ordinance (section 2(62A), section 154A, and Division IVA of Part III of the First Schedule), based on `docs/context/corpus.md` and the manifest scope note. Added focused synthetic cases for included and excluded legal text.
- **Tested:** Not run in this session. No real corpus indexing or database write was performed.
- **Cut or partial:** The PSEB dated HTML snapshot is still absent; VOSS OCR or reviewed transcription, embedding model selection/configuration, source indexing, and the gold-question evaluation remain.
- **Differs from the report?** No intended scope change; filtering follows the repo's corpus rules.

## 2026-10-17: Compliance assistant foundation (GitHub Copilot)

- **Feature and IDs:** Compliance assistant, FR-8, NFR-12, NFR-13, NFR-14.
- **Built:** Added manifest/hash verification, PDF page extraction, section-aware citation chunks, configurable SentenceTransformer encoding, pgvector retrieval, compliance document/chunk/query/citation models, Alembic migrations, a grounded Gemini gateway, answer validation/abstention, query logging, and the founder-only `POST /api/v1/compliance/questions` endpoint. Backend tests now use in-memory SQLite and do not modify `app.db`.
- **Tested:** Full backend suite: 18 passed. Full RAG suite: 11 passed. All 12 manifest entries matched their SHA-256 hashes. Indexing and Gemini tests use fakes; no live provider call, embedding-weight download, or PostgreSQL/pgvector database test was run.
- **Cut or partial:** No corpus was indexed. `EMBEDDING_MODEL_NAME` is not selected/configured. The Companies Act and Income Tax Ordinance are skipped until their report-defined section filters are implemented; VOSS needs OCR or reviewed transcription; the report-designated dated PSEB HTML snapshot is absent, so the mismatched PDF remains unindexed. The gold-question evaluation remains to do.
- **Differs from the report?** No difference introduced. The existing PSEB source mismatch remains unresolved. Alembic was selected by team approval; see `docs/DECISIONS.md` (2026-10-17, "Use Alembic for backend migrations").
## 2026-10-18: Dataset docs checked against dataset cards and papers (Claude)

- **Feature and IDs:** External dataset documentation (Chapter 3 datasets table; no FR/NFR directly)
- **Built:** Corrected `docs/datasets.md`, `docs/dataset-links.md`, `docs/DECISIONS.md` and `docs/pending-report-changes.md` after reading the Hugging Face cards and papers: Roman-Urdu-Parl split licence is Apache 2.0 (was "none"); Parl domain is "various informal online sources", not parliamentary (Butt et al., arXiv:2503.21530); Roman Urdu MS MARCO traced to Butt, Varanasi and Neumann (LowResNLP 2025, read from the PDF); Urdu-Multi-Domain-Benchmark authors are Haroon and Bashir (Zenodo v1.1, 2026); ERUPD authors are Furqan, Khaja and Habeeb; Mustafa et al. authors are Hammad Mustafa, Muhammad Faisal, Waqas Ahmed. Guessed author names and years replaced by repository usernames. Repaired a blank line that split the table in `docs/pending-report-changes.md`.
- **Tested:** Compared each changed line with the source it came from. Kaggle uploader names were not re-checked against Kaggle.
- **Cut or partial:** Kaggle dataset pages were not re-opened, so their licence and uploader fields still rest on the earlier run.
- **Differs from the report?** Yes; two new rows in `docs/pending-report-changes.md`.

## 2026-10-18: Dataset claim checks V2 fixed rerun and documented issues (Antigravity)

- **Feature and IDs:** External dataset profiling and claim checks (Chapter 3 external datasets validation; the datasets table (\label{tab:datasets}))
- **Built:** Created `dataset_claim_checks_v2.ipynb` to audit external datasets across 18 folders (14 full, 4 reference). First run encountered bugs (pyarrow string regex `\u` escapes, string threshold comparisons, split counts, LinkedIn pickle opcode false positives, blank rows, and job title mapping). Implemented bug-fixed re-run in new appended cells (cells 57 to 74) targeting `dataset_claim_check_v2_fixed_section.md` and `dataset_fit_scores_v2.csv`.
- **Tested:** Fixed re-run executed across local dataset files. Verified that Census resolves to 433 usable rows, Investments to 49,438 usable rows (0 duplicates), Parl to 20,719 validation / 20,741 test rows, and LinkedIn to (3600, 39). S14 (IterateCV) and Step 3 (Pair Feasibility) crashed in the fixed run. Retrieval queries lexical baseline (char_wb TF-IDF) and MS MARCO script share values were not printed due to unexecuted blocks and missing optional scikit-learn dependency.
- **Cut or partial:** Section S13 reference datasets dropped. S14 and Step 3 crashed; retrieval baseline and MS MARCO values unprinted.
- **Next steps:** Prototype check, project zip, report PR.
- **Differs from the report?** Yes; documented in `docs/DECISIONS.md` (2026-10-18 entries) and queued in `docs/pending-report-changes.md`.

## 2026-10-17: CI ruff pinned and notebooks excluded from ruff (Ali, with Claude Code)

- Pinned CI ruff to 0.17.1, added `ml/ruff.toml` (notebooks excluded), fixed `rag/corpus_profile/profile_corpus.py` (F541, four `# noqa: BLE001`) and the bare `raise` in `dataset_claim_checks.ipynb`; ruff 0.17.1 re-run in `rag/`, `ml/` and `backend/`, not yet run in GitHub Actions. Differs from the report? No. See `docs/DECISIONS.md` (2026-10-17, "CI ruff pinned").

## 2026-10-17: Skills install list applied; sync script copies references (Ali, with Claude Code)

- **Feature and IDs:** Repository tooling, agent skills install (no FR/NFR directly)
- **Built:**
  - Installed into `.claude/skills/`: `frontend-design`, `claude-api` (trimmed to Python, TypeScript, curl and shared docs), `git-workflow-and-versioning` (the `git reset --hard` line rewritten, a note added that the `CLAUDE.md` git rules win), `shipping-and-launch`, `ci-cd-and-automation`, `performance-optimization`, `observability-and-instrumentation`, `web-design-guidelines` (rules saved as `command.md` at a pinned commit, live download removed), and `ponytail`, `ponytail-review`, `ponytail-audit`, `ponytail-debt` (descriptions of the first two trimmed so they start only when asked).
  - Copied the upstream `references/` checklists to `.claude/references/`. Copied the licenses to `third_party_licenses/`.
  - `scripts/sync_agent_skills.py` now also copies `.claude/references/` to `.agents/references/`. Added `.agents/references/` to `.gitignore`. Updated `SETUP.md`, `AGENTS.md`, `CLAUDE.md` (five skill rows added) and `THIRD_PARTY.md` (rows, pins, licenses, "Not installing" lines).
- **Tested:** Ran the sync script with `--dry-run` and for real: 40 skills and the references copied, and `.agents/skills/<skill>/../../references` resolves. `command.md` SHA-256 matches the recorded value. `python scripts/scan_for_keys.py` found no keys in 309 tracked files, and a separate key-pattern search over `.claude/skills/` and `.claude/references/` found none. Read `git diff` for `CLAUDE.md` and `THIRD_PARTY.md`. Not tested: using the new skills inside Claude Code, Codex or Antigravity.
- **Cut or partial:** spec-kit is per person and not installed yet. graphify is skipped until there is code. `DESIGN.md` is not installed (brand undecided). caveman and gstack were reviewed and skipped. **Update 2026-11-03:** caveman approved (hooks profile only, pinned clone); gstack stays skipped. The per-person installs were not done in this run. career-ops, financial-services and replica-skill have not been read.
- **Differs from the report?** No, this is tooling only. See `docs/DECISIONS.md` (2026-10-17, "Skills install finished").

## 2026-10-17: Shared Drive rule added for non-git files (Ali)

- **Feature and IDs:** Repository hygiene and data policy (no FR/NFR directly)
- **Built:** Added "Files that don't go in git" rule across repository documentation:
  - `SETUP.md`: added section with shared Google Drive link for non-reproducible files (own exports, trained models, backups, local datasets).
  - `AGENTS.md` and `CLAUDE.md`: added rule directing large, non-reproducible or private files to the shared Drive and logging them in `docs/dataset-links.md`.
  - `docs/dataset-links.md`: added Shared Drive heading and link at the top.
  - Confirmed backup directories (`_backup_mirror/`, `.claude/backups/`) are in `.gitignore`.
- **Tested:** Verified links, checked git status and diff.
- **Cut or partial:** None.
- **Differs from the report?** No.

## 2026-10-17: External dataset claim-check notebook bug fixes and profiling verification (Ali)

- **Feature and IDs:** Dataset claim checks and external dataset profiling (Chapter 3 external datasets validation; supports preprocessing and matching baseline)
- **Built:** Fixed five issues in `ml/notebooks/dataset_claim_checks.ipynb`:
  1. Roman-Urdu-Parl split detection: mapped the single unlabeled split to `train`, keeping the train and total comparison against the report as FAIL.
  2. ATS dataset: corrected the mean text length check to use `resume_text` instead of `resume_id`.
  3. Crunchbase investments: fixed `funding_total_usd` parsing by stripping column-name whitespace and stripping commas, spaces, and '-' from values before numeric conversion.
  4. Roman-Urdu-Parl script spot-check: dynamically lists folder extensions and reads sample rows from `.csv`, `.parquet`, or `.arrow` in a memory-safe manner.
  5. Missing-value rate checks: added `latin-1` encoding for Crunchbase files and deduplication in `info()` / report generation to prevent duplicate rows. Cleared all saved cell outputs from the notebook.
- **Tested:** Tested individual logic components on local dataset files (`carnet_data/data`): verified ATS mean text length (~376.9 chars), Crunchbase investments funding parsing (40,907 non-nulls, median $2,000,000, max $30,079,503,000), Roman-Urdu-Parl script detection (78.1% Arabic script, 81.4% Latin), and verified clean notebook JSON with empty outputs. Did not run heavy full-dataset processing outside memory-safe samples.
- **Cut or partial:** None.
- **Differs from the report?** Yes: Roman-Urdu-Parl split counts (train 6,365,808 in files vs 6,333,218 in report; total 6,407,268 vs 6,374,678), Crunchbase date ranges containing extreme/impossible years, and ATS mean resume text length (376.9 vs 376). See `docs/DECISIONS.md` (2026-10-17) and `docs/pending-report-changes.md`.

## 2026-10-17: Dataset docs updated with claim-check findings (Ali)

- **Feature and IDs:** External dataset documentation (Chapter 3; no FR/NFR directly; supports honest claims in the report)
- **Built:** Updated `docs/datasets.md`, `docs/DECISIONS.md`, `docs/pending-report-changes.md` with all findings from `ml/notebooks/dataset_claim_check_report.md` (run 2026-10-17):
  - Roman-Urdu-Parl: corrected row counts to file values (train 6,365,808, total 6,407,268); documented that report figures are unmatched and source of 6,333,218 is unknown.
  - Crunchbase Success/Fail: added missing rates (founded_at 22.9%, country_code 10.5%, category_list 4.7%) and impossible date bounds (1015–2914, 1014–2115) to Known problems.
  - Crunchbase Investments: added missing rates, impossible date bounds, and cleaned funding_total_usd stats (40,907 non-null; median $2 M; max ~$30 B) to Known problems.
  - ATS: updated mean text length from 376 to 376.9 characters.
  - Added "Claim check run 2026-10-17" note to all seven dataset entries.
  - Added tech-niche filter and dataset-swap rule to `docs/DECISIONS.md`.
  - Added five open rows to `docs/pending-report-changes.md`.
- **Tested:** Checked that no existing rows were duplicated; inspected file diff after each edit.
- **Cut or partial:** None.
- **Differs from the report?** See `docs/pending-report-changes.md` rows dated 2026-10-17.

## 2026-10-17: pending-report-changes.md triage — new rows and undecided items (Ali)

- **Feature and IDs:** Report-tracking hygiene (no FR/NFR; supports honest claims in the report and Chapter 6)
- **Built:** Added 7 new rows to `docs/pending-report-changes.md`: tech niche scope, dataset search/swap rule, corpus location and hashes, Chapter 5 AI tools, CI NFR-23 unconfirmed, build-order internal-only note. Confirmed 4 earlier rows still present (Chapter 6 Nov 8 update, limitations, data dictionary FR numbers, SPRINT_PLAN.md corpus count). Replaced the "Still open" section with a named list of 8 undecided items (brand, readiness reviewers, SECP cross-check, Alembic, ruff, hosting, feature freeze, Docker Compose).
- **Tested:** Read the full file before and after; no duplicates introduced.
- **Cut or partial:** None.
- **Differs from the report?** Yes — all newly added rows describe differences. See the table in `docs/pending-report-changes.md`.

## 2026-10-18: Next.js frontend implementation across all roles matching wireframes (Antigravity)

- **Feature and IDs:** Frontend foundation, role-based workflows, wireframes 01 to 12 (FR-1 through FR-19, NFR-10, NFR-11, NFR-12, NFR-15, NFR-18).
- **Built:**
  - Initialized `/frontend` Next.js 16 App Router application with strict TypeScript, vanilla CSS Modules, zero external UI libraries.
  - Implemented session handling and authentication in `src/context/AuthContext.tsx` and `src/lib/auth.ts`: strict login gating (unauthenticated users redirect to `/login`), role-based boundary enforcement (users attempting to view another role's dashboard/pages are redirected to their own workspace), mock login role selector for demonstration, and login/register with PECA consent checkbox.
  - Implemented responsive navigation (`Sidebar.tsx`, `DashboardLayout.tsx`): 240px fixed sidebar on laptop (1024–1439px), capped 1280px max-width on large desktop (1440px+), 68px icon rail on tablet (640–1023px), slide-in drawer with backdrop on mobile (<640px) accessible via Escape key and route change.
  - Built all 12 wireframe interfaces with pixel-accurate layout and exact copy:
    1. Login & Register (`01_Login_Register.png`): `/login`, `/register`.
    2. Founder Startup Profile (`02_Founder_Profile_2x.png`): `/founder/profile`.
    3. Founder Readiness Score breakdown (`03_Readiness_Score.png`): `/founder/readiness` (1–5 scale, 7 dimensions).
    4. Founder Dashboard (`04_Founder_Dashboard.png`): `/founder/dashboard` (verified banner, 3.1/5 readiness, next actions, pitch feedback, 3 match cards).
    5. Founder Pitch Practice (`05_Pitch_Practice.png`): `/founder/pitch`.
    6. Founder Pitch Feedback (`06_Pitch_Feedback.png`): `/founder/feedback`.
    7. Founder Match Feed (`07_Match_Feed.png`): `/founder/matches`.
    8. Talent Dashboard (`08_Talent_Dashboard.png`): `/talent/dashboard`.
    9. Talent Job Board (`09_Job_Board.png`): `/talent/jobs` (faceted filter sidebar, 24 roles counter, job cards).
    10. Mentor Dashboard (`10_Mentor_Dashboard.png`): `/mentor/dashboard`.
    11. Investor Dashboard (`11_Investor_Dashboard.png`): `/investor/dashboard`.
    12. Admin Console (`12_Admin_Queue.png`): `/admin/dashboard` (escalated profiles, appeals, decided today, Munshi Books & Nida Farooq review cards with reasons and reject/approve actions).
  - Provided zero-404 route coverage for all secondary role navigation routes (`/talent/profile`, `/talent/resume`, `/talent/matches`, `/mentor/profile`, `/mentor/requests`, `/investor/profile`, `/investor/founders`, `/investor/requests`).
- **Tested:**
  - Automated `npm run build` static generation across all 24 routes passing cleanly with 0 TypeScript and 0 linting errors.
  - In-browser verification of responsive breakpoints (mobile drawer, tablet rail, laptop wireframe view).
  - Auth route guards, role redirection, and mock login verification across all 5 roles.
- **Cut or partial:** None.
- **Differs from the report?** No.








## 2026-10-17: VOSS corpus transcription (Codex)

- **Feature and IDs:** Compliance assistant, FR-8, NFR-12, NFR-14.
- **Built:** Added a reviewed text transcription of the scanned FBR VOSS circular. Marked the PDF inactive for indexing but retained it for provenance; recorded the transcription hash and method in the corpus manifest and updated the corpus instructions and decision log.
- **Tested:** Compared the transcription with the extracted page image; manifest/hash verification still needs to be run after all corpus edits.
- **Cut or partial:** No OCR package was installed; transcription is manual and explicitly annotated. Corpus indexing and gold-set evaluation remain.
- **Differs from the report?** No; this implements the report corpus source with the hand-transcription method allowed by the corpus plan.

## 2026-11-02: graphify installed, skill-only (Ali, with Claude Code)

- **Feature and IDs:** Developer tooling for context and token savings (no FR/NFR).
- **Built:** `uv tool install graphifyy==0.9.100` (isolated uv tool, on Ali's machine only). Then `graphify install --project --platform agents`, which wrote the skill to `.agents/skills/graphify/` (gitignored). Copied `SKILL.md` and `references/` to `.claude/skills/graphify/`, left out the `.graphify_version` marker. Copied the Apache-2.0, MIT and NOTICE files to `third_party_licenses/`. One local edit: the `SKILL.md` description now says "Use only when the user asks for /graphify", same as ponytail.
- **Tested:** `graphify --version` prints 0.9.100. After the install, `git status` showed no change to `CLAUDE.md` or `.claude/settings.json`. Scanned the copied files for download, delete, commit and push commands: only documentation of `graphify hook install` in `references/hooks.md`. The graph itself has **not** been built (`/graphify .` not run).
- **Cut or partial:** Did not use plain `graphify install --project` as `THIRD_PARTY.md` said. Reading `install.py` showed that command also appends a section to `CLAUDE.md` and writes a `PreToolUse` hook into `.claude/settings.json`; both are off limits here. `graphify hook install` and `graphify claude install` must not be run. Set `GRAPHIFY_QUERY_LOG_DISABLE=1` in your shell profile (not done by Claude).
- **Differs from the report?** No. The report does not mention graphify. It differs from the install steps in `THIRD_PARTY.md`, which are corrected there.

## 2026-11-02: spec-kit CLI installed, personal (Ali, with Claude Code)

- **Feature and IDs:** Developer tooling for spec-driven work (no FR/NFR).
- **Built:** `uv tool install specify-cli==1.2.6` (isolated uv tool, Ali's machine only). The README's own install line is `uv tool install specify-cli`; PyPI 1.2.6 matches the GitHub tag `v1.2.6` (commit 9eacc24). Nothing copied into the repo.
- **Tested:** `specify --help` runs. **`specify init` was not run**; it writes `.specify/` and agent command files and needs its own OK. The source has no telemetry; its only network call is an optional update check to the GitHub releases API.
- **Cut or partial:** Not initialised in this repo. Overlaps the `spec-driven-development` skill, so use one of the two per feature, not both.
- **Differs from the report?** No.

## 2026-11-02: docx/pdf/pptx/xlsx skills and code-review plugin, personal (Ali, with Claude Code)

- **Feature and IDs:** Developer tooling (no FR/NFR).
- **Built:** `docx`, `pdf`, `pptx`, `xlsx`: nothing installed. They already load from Ali's claude.ai account (`anthropic-skills:*`) and are not on disk, so there is nothing to copy. Anthropic's licence is all rights reserved, so they never go into the repo. `code-review` plugin: `claude plugin install code-review@claude-plugins-official --scope user`, version 1.0.1, Apache-2.0. It was already in the local marketplace copy, so no clone was needed.
- **Tested:** `claude plugin list` shows `code-review@claude-plugins-official` enabled at user scope. The command was **not run** on a PR. Read the plugin: one command file, no hooks, no MCP server. It posts to GitHub only with `--comment`, and `gh` is not installed on this machine.
- **Cut or partial:** Use `/code-review` without `--comment` unless a person asks for a post. The plugin command and the built-in `code-review` skill share a name, so check which one runs.
- **Differs from the report?** No.

## 2026-11-02: my-claude-skills and awesome-claude-skills, personal only (Ali, with Claude Code)

- **Feature and IDs:** Developer tooling (no FR/NFR).
- **Built:** Cloned both repos to `~/claude-tools/` (outside the project). Copied all 6 skills of my-claude-skills (commit a67d698) and 6 of 864 from awesome-claude-skills (commit be2a406) to `~/.claude/skills/`. Neither repo has a LICENSE file, so nothing was copied into this repo, `.claude/skills/` or `third_party_licenses/`.
- **Tested:** Scanned every `.py` file and `SKILL.md` for downloads, pipe-to-shell, deletes, network calls, `eval`/`exec` and instruction overrides. my-claude-skills: local scanners only; the one `git clone` and `rmtree` are in the auditor's optional repo-URL mode and act on its own temp folder. awesome-claude-skills: the six installed are single-file prompt skills with no scripts. Not run on any project file, and not every line of every file was read.
- **Cut or partial:** awesome-claude-skills: 832 of 864 skills are Composio connectors that need Rube MCP (hosted by Composio) and an OAuth connection per service, so they were **not** installed (corrected 2026-11-03; first written as "account and API key"). Also skipped: 10 duplicates of skills already in the claude.ai account, and skills that post to Slack, read chat history, download videos, or move files. Tell Claude if you want any of those.
- **Differs from the report?** No.

## 2026-11-02: career-ops, replica-skill (personal) and financial-services (skipped) (Ali, with Claude Code)

- **Feature and IDs:** Developer tooling (no FR/NFR).
- **Built:** Cloned career-ops (20b9fd3), financial-services (6056506) and replica-skill (77c9436) to `~/claude-tools/`. career-ops: `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm install` in its own folder (7 packages, 0 vulnerabilities reported). It is not installed as a plugin, because the plugin's `SessionStart` hook runs a Node script on its own. replica-skill: copied `replica-recon`, `replica-diff`, `replica-test`, `replica-design`, `replica-build` to `~/.claude/skills/`. Nothing was copied into the repo.
- **Tested:** Read each README, `package.json`, hook files and MCP config, and grepped for download, delete, deploy and key patterns. career-ops was not started and no CV or key was entered. The replica skills were not run. Not every file was read: career-ops has about 3,000.
- **Cut or partial:** financial-services was read and **not installed**: wrong domain, about 13 paid data connectors, and our scope excludes investment advice. Chromium was not downloaded, so career-ops PDF generation and browser checks will not work until `npx playwright install chromium` is run. replica-skill: backend, architect, brand, entrepreneur, launch and deploy were left out. **Update 2026-11-03:** brand, entrepreneur and launch were added after reading all six; architect, backend and deploy stay out. `replica-design` and `replica-build` are built to rebuild another app's design system; the Figma prototypes and `DESIGN.md` still win for Founder's Carnet.
- **Differs from the report?** No.

## 2026-11-02: optional personal plugins from SETUP.md section 8 (Ali, with Claude Code)

- **Feature and IDs:** Developer tooling (no FR/NFR).
- **Built:** Nothing installed. `claude-md-management` and `claude-code-setup` already load from Ali's claude.ai account (and exist in `claude-plugins-official`). `claude-context-optimizer` was cloned to `~/claude-tools/` (1fb7a86, v5.1.1, MIT) and read.
- **Tested:** Read `hooks/hooks.json`. Not every source file was read and nothing was run.
- **Cut or partial:** `claude-context-optimizer` skipped: it registers six hooks that run on its own, against the hooks rule in `CLAUDE.md`. A skills-only copy (6 skills) was possible and was declined. **Superseded 2026-11-03:** Ali reversed this; it is approved for the separate hooks profile only, via `--plugin-dir` from the pinned clone (1fb7a86). See the THIRD_PARTY.md install log. `SETUP.md` section 8 still says v4.12.1 and should be corrected by a person.
- **Differs from the report?** No.

## 2026-11-02: rea read, install parked (Ali, with Claude Code)

- **Feature and IDs:** Developer tooling (no FR/NFR).
- **Built:** Nothing installed. Cloned `morluto/rea` to `~/claude-tools/rea` (920d634, npm `rea-agents` 6.8.0, MIT) and read its README, install docs, `server.json`, `DISCLAIMER.md` and `SECURITY.md`.
- **Tested:** Nothing was run, including `rea setup --dry-run`. The MCP entry format was taken from the project's own tests, not generated. Not every file was read: the repo has about 7,000.
- **Cut or partial:** Parked by Ali ("full install later") until Node is upgraded to 24.22.1 or newer; the machine has 24.18.0. 172 tools and a large default catalog (about 496 KB), so narrow it with `--tool-families` when installing. No Founder's Carnet requirement needs it.
- **Differs from the report?** No.

## 2026-11-02: gsd-core read, dry-run, skipped (Ali, with Claude Code)

- **Feature and IDs:** Developer tooling (no FR/NFR).
- **Built:** Nothing installed. Cloned `open-gsd/gsd-core` to `~/claude-tools/gsd-core` (bfab824, MIT). Ran `npx -y @opengsd/gsd-core@1.19.0 --claude --global --profile=core --dry-run`.
- **Tested:** The dry-run printed only a legacy-cleanup note ("would remove" an update-cache file under `~/.cache/gsd`) and no install plan. `~/.claude/settings.json` had the same hash before and after (512 bytes). The clone's own `bin/install.js --help` fails on a missing file, so installer flags and the hook list come from reading the source, not from a run.
- **Cut or partial:** Skipped by Ali. The installer has no hooks-off flag and a global install adds about 25 auto-running hooks to `~/.claude/settings.json`, against the hooks rule and the no-global-install rule. Version answer for `SETUP.md` section 10: npm `latest` is 1.19.0; 1.17.0 and 1.12.0 are older, so the open mismatch should be closed by pinning 1.19.0 if it is ever installed.
- **Differs from the report?** No.

## 2026-11-03: ECC read, skipped (Ali, with Claude Code)

- **Feature and IDs:** Developer tooling (no FR/NFR).
- **Built:** Nothing installed. Cloned `affaan-m/ECC` to `~/claude-tools/ecc` (b38be6a, MIT; npm `ecc-universal` 2.2.3 is `latest`). Read `SETUP.md` section 6, `.claude/settings.json`, `.claude/hooks/guard.py`, ECC's `scripts/setup.js`, `claude-plugin-setup.js`, `hook-flags.js`, `plugin.json` and `hooks/hooks.json`.
- **Tested:** Nothing was run, including `setup --dry-run`. Hook gating was read from source, not observed. Most of the repo's 4,701 files were not read. Whether the project deny rules still win over ECC hooks was not tested.
- **Cut or partial:** Skipped by Ali on conflict. **Superseded 2026-11-03:** Ali reversed this; approved via `--plugin-dir` from the pinned clone (b38be6a) in the separate hooks profile only, hooks disabled by `ECC_HOOKS_ENABLED=false`, rules `common` + `python` (16 files) copied to `C:\Users\pakistan\.claude-hooks\rules\ecc\`. Correction: the plugin has 27 hook entries across 8 events, not 26 across 9. (1) Global scope against the no-global-installs rule. (2) "Hooks off" is a plugin option; the 27 hook entries stay registered and each starts `node` before exiting, and the option defaults to on if missing. (3) If hooks were enabled, `pre:config-protection` and `pre:edit-write:gateguard-fact-force` overlap `guard.py`'s Write/Edit matcher. `SETUP.md` section 6 should be corrected: "hooks off" does not remove the hooks.
- **Differs from the report?** No.

## 2026-11-03: setup docs corrected after the installs (Ali, with Claude Code)

- **Feature and IDs:** Documentation hygiene (no FR/NFR).
- **Built:** With Ali's OK, edited four existing files. `THIRD_PARTY.md`: graphify setup steps rewritten (skill-only `--platform agents`, pinned 0.9.100, Gemini-key and `rm -f` warnings), section D table given a status column, "Left out" updated, and the stale "not installed yet" lines for spec-kit and graphify fixed. `CLAUDE.md`: added the `graphify` row to the skills table and corrected the "not installed yet" sentence (backup saved first with `python scripts/backup.py snapshot CLAUDE.md`). `SETUP.md`: claude-context-optimizer v4.12.1 to v5.1.1 with its six hooks, a note under section 6 that ECC "hooks off" only disables the hooks, and a version note under section 10 for gsd-core (1.19.0 is `latest`).
- **Tested:** Cheap line-grep scan of the graphify skill and 17 personal skill folders (report kept outside the repo). `scripts/scan_for_keys.py` clean. Project Python checked read-only: only `ml/.venv` exists (3.11.9); `backend/` and `rag/` had no `.venv` in this checkout. No installed tool was run on a project file.
- **Cut or partial:** Nothing committed. The `SETUP.md` section 6 and 10 notes are short annotations, not rewrites of those sections.
- **Differs from the report?** No.

## 2026-11-03: graphify safe use (Ali, with Claude Code)

- **Feature and IDs:** Developer tooling (no FR/NFR). Operating note, not a decision.
- **Rules:** Do not run `/graphify` on the repo root or on `docs/`. Anything that is not code (docs, PDFs, images) goes to an LLM for the semantic pass. Start with `backend/` only, code only (`--code-only`), and keep `docs/report/` and the four protected report files out. Before any run, check that `GEMINI_API_KEY` and `GOOGLE_API_KEY` are unset, or set `GRAPHIFY_BACKEND=none`. With a Gemini key set, non-code files go to Gemini instead of staying in the Claude session.
- **Checked 2026-11-03:** both variables unset in process, user and machine scope; no real `.env` in the repo, only `.env.example`.
- **Output:** `graphify-out/` is already in `.gitignore`. Delete it by hand to undo a run.

## 2026-11-03: graphify ignore file, venv wording, separate hooks profile folders (Ali, with Claude Code)

- **Feature and IDs:** Developer tooling and setup docs (no FR/NFR).
- **Built:** Added `.graphifyignore` (anchored: `/docs/`, `/rag/data/`, `/backend/app.db`). `SETUP.md` section 5 now says `py -3.11 -m venv .venv` (backup `.claude/backups/20261103-030913-636522/SETUP.md`). Created two empty folders outside the repo for a separate hooks profile: `C:\Users\pakistan\.claude-hooks` (to be used as `CLAUDE_CONFIG_DIR`) and `C:\Users\pakistan\claude-lab` (launch folder). `~/.claude/settings.json` has the same hash as before (0ee16cd1…).
- **Tested:** `python scripts/scan_for_keys.py`: no keys in 493 files. Not tested: how graphify treats the anchored patterns, and `CLAUDE_CONFIG_DIR` behaviour on this machine (read in the docs only).
- **Cut or partial:** No hook-based tool installed yet. The PowerShell launch helper was shown, not written.
- **Differs from the report?** No.

## 2026-11-03: ECC, caveman approved (hooks profile only); gstack kept skipped (Ali, with Claude Code)

- **Feature and IDs:** Developer tooling (no FR/NFR).
- **Built:** Nothing installed. ECC (pinned clone b38be6a) and caveman (pinned clone 2e068f7) are approved to be used only through `claude --plugin-dir` in the separate hooks profile (`CLAUDE_CONFIG_DIR=C:\Users\pakistan\.claude-hooks`). 16 ECC rule files (`common` 10, `python` 6) copied to `C:\Users\pakistan\.claude-hooks\rules\ecc\`. `~/.claude/settings.json` hash unchanged (0ee16cd1…).
- **Tested:** Nothing run. Hook lists come from `hooks.json` and `plugin.json`. Correction: ECC has 27 hook entries across 8 events (earlier notes said 26 across 9).
- **Cut or partial:** gstack kept skipped: hardcoded `~/.claude` paths in all 62 skills, needs Bun, and ship/land-and-deploy workflows conflict with CLAUDE.md. caveman must not be active in founders-carnet. Not verified: caveman's default mode, gstack's telemetry destination.
- **Differs from the report?** No.

## 2026-11-03: codebase-memory-mcp installed in reduced form, hooks profile only (Ali, with Claude Code)

- **Feature and IDs:** Developer tooling (no FR/NFR).
- **Built:** Downloaded release v0.12.1 `codebase-memory-mcp-windows-amd64.zip` and `checksums.txt` to `C:\Users\pakistan\claude-tools\cbm\v0.12.1\`, verified SHA-256, extracted. Registered the unsigned exe as an MCP server only in the profile `C:\Users\pakistan\.claude-hooks` (`claude mcp add --scope user`, `CBM_CACHE_DIR` inside the profile) and set `watcher_enabled false`. `install.ps1` was not run.
- **Tested:** `--version` prints 0.12.1. Main `settings.json` hash unchanged (0ee16cd1…); no `codebase-memory` entry in the main `.claude.json` or `installed_plugins.json`; no `~/.cache/codebase-memory-mcp` folder created; no process left running. One script check printed "unchanged" from empty values (a PowerShell alias clash on my helper name `H`) and was redone with `sha256sum`. Not tested: the server inside a Claude session, any indexing, the Sigstore bundle.
- **Cut or partial:** No hooks, agents, PATH change or daemon install. The repo is not indexed and must not be until Ali says so. Overlaps graphify. **Dropped by Ali later on 2026-11-03** (graphify kept); removal is by hand, see the entry below.
- **Differs from the report?** No.

## 2026-11-03: claude-swarm, screenshot-to-code, AgentForge-AIOrchestrator read, kept as reference clones (Ali, with Claude Code)

- **Feature and IDs:** Developer tooling (no FR/NFR).
- **Built:** Nothing installed. Cloned the three to `C:\Users\pakistan\claude-tools\` (9b1c556, a813977, f19bcd6) and read their READMEs, package files and key use.
- **Tested:** Nothing run. Grep only for keys, process execution and analytics words.
- **Cut or partial:** None is a skill pack (no `SKILL.md` in any). All three need paid keys or an account (Anthropic; OpenAI, Anthropic or Gemini plus Replicate; Supabase plus OpenRouter and NVIDIA). AgentForge has no licence. Ali chose reference clones only.
- **Differs from the report?** No.

## 2026-11-03: four personal skills restored after an accidental deletion (Ali, with Claude Code)

- **Feature and IDs:** Developer tooling (no FR/NFR).
- **Built:** Re-copied `replica-design`, `replica-build` (from `~/claude-tools/replica-skill`, 77c9436) and `ci-cd-pipeline-builder`, `performance-profiler` (from `~/claude-tools/my-claude-skills`, a67d698) into `C:\Users\pakistan\.claude\skills\`. Personal only; nothing in the repo.
- **Tested:** Both clones were at the expected commits with no uncommitted changes before copying. `diff -r` of each restored folder against its clone showed no differences. File counts 3, 1, 7 and 3 as expected.
- **Cut or partial:** None. The rows stay "installed".
- **Differs from the report?** No.

## 2026-11-03: replica-skill: the other 6 read, 3 offline helpers added (Ali, with Claude Code)

- **Feature and IDs:** Developer tooling (no FR/NFR).
- **Built:** Copied `replica-brand`, `replica-entrepreneur` and `replica-launch` (8 files) from `~/claude-tools/replica-skill` (77c9436) to `C:\Users\pakistan\.claude\skills\`. Personal only. `diff -r` against the clone showed no differences.
- **Tested:** Nothing run. Read all six remaining skills: no hooks, no `allowed-tools`; `sweep.py`, `reviews.py` and `listing.py` use only the standard library and showed no network, subprocess or environment-variable use by grep. Not line by line.
- **Cut or partial:** `replica-architect`, `replica-backend` and `replica-deploy` not installed: they default to a stack (Supabase or Neon, Drizzle or Prisma, Next.js, Stripe) that conflicts with the project's architecture rules, and `replica-deploy` is a go-live workflow. The skills' documented commands use `python3`, which is usually absent on Windows.
- **Differs from the report?** No.

## 2026-11-03: awesome-claude-skills: list of the other 858 written, nothing installed (Ali, with Claude Code)

- **Feature and IDs:** Developer tooling (no FR/NFR).
- **Built:** Wrote `C:\Users\pakistan\claude-tools\awesome-skills-list.md` (outside the repo): 858 numbered rows = 26 general skills + 832 Composio connectors, with purpose, whether Composio/Rube auth is needed, and a keyword-scan note on posting or reading outside services. Generated by a read-only script from the clone at be2a406.
- **Tested:** Row count checks out (858 = 864 SKILL.md files minus the 6 installed). The "outside services" column is a keyword scan of SKILL.md text only; a blank means no keyword matched, not that the skill is safe. Nothing was run.
- **Cut or partial:** No skill installed. Waiting on Ali to pick names from the list. The 832 connectors all route data through Composio's hosted Rube MCP.
- **Differs from the report?** No.

## 2026-11-03: decisions after report B (Ali, with Claude Code)

- **Feature and IDs:** Developer tooling and setup docs (no FR/NFR).
- **Built:** `SETUP.md` sections 6 and 8 corrected to match the separate-profile decision. `replica-design` and `replica-build` copied (byte-identical) to `C:\Users\pakistan\.claude-hooks\skills\`. A proposed `docs/DECISIONS.md` entry written to `C:\Users\pakistan\claude-tools\decisions-proposal.md`, outside the repo, for Ali to paste.
- **Tested:** `diff -r` of both copied skills against the clone and the main copies: identical. Main `settings.json` hash unchanged.
- **Cut or partial:** codebase-memory-mcp dropped (graphify kept); Claude deleted nothing, and Ali removes the binary folders, the profile cache and the MCP registration by hand. No virtual environments created (Ali's decision). career-ops and the code-review plugin kept. **Update 2026-11-03 (later):** Ali decided `replica-design` and `replica-build` stay in the main config; the profile copies are redundant and may be removed by Ali.
- **Differs from the report?** No.

## 2026-11-03: placement plan adjusted: normal config versus personal-tools profile (Ali, with Claude Code)

- **Feature and IDs:** Developer tooling (no FR/NFR).
- **Built:** Nothing installed or moved. Plan: hook-free personal tools in the normal config, every hook-based tool in `C:\Users\pakistan\.claude-hooks`, launched only outside the FYP repo. All tools logged on 2 and 3 November 2026 are personal tools, not required by the FYP.
- **Tested:** Sizes measured for the profile (104 KB) and four plugin clones (1.4 MB, 34 MB, 105 MB, 116 MB). None of last round's removals has been run.
- **Cut or partial:** Decided: replica-design/build stay in the main config; codebase-memory-mcp stays dropped; gstack stays skipped; the profile does not sync the claude.ai account (`C:\Users\pakistan\.claude-hooks\settings.json` written with `syncClaudeAiPlugins` and `syncClaudeAiSkills` set to `false`).
- **Differs from the report?** No.
