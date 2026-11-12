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

## 2026-11-12: Admin verification queue and appeals (Codex)

- **Feature and IDs:** Administrative review and profile verification appeals, FR-16, FR-21, FR-26.
- **Built:** Extended the admin-only queue with all persisted signal values, outcomes, input snapshots, and reasons. Added coverage for 401/403 access, both queue statuses, privacy, approve/reject decisions, reviewer attribution, trimmed non-empty reasons, final appeal outcomes, the one-appeal limit, report-to-queue rescore locking, and status visibility. Kept the existing tables and migration history; refreshed `backend/openapi.json` with both admin routes.
- **Tested:** Focused admin tests: 6 passed. Full backend suite: 108 passed, 0 failed, 1 existing Starlette/AnyIO warning. Isolated compliance regression tests: 22 passed; RAG regression tests: 11 passed. Compliance and RAG are regression-only and out of scope. Console and JUnit results are saved under `docs/test-results/step5-admin-20261112-2320.*`, `docs/test-results/step5-compliance-regression-20261112-2320.*`, and `docs/test-results/step5-compliance-rag-regression-20261112-2316.*`.
- **Cut or partial:** No block-profile operation exists in the current API, so blocked-profile routing was not added or tested; a new operation would exceed the approved contract. PostgreSQL/production behavior was not exercised; tests use SQLite.
- **Differs from the report?** The available requirement summary does not specify route paths, per-signal response fields, or appeal audit columns. The specific API contract and report follow-up are recorded in `docs/DECISIONS.md` and `docs/pending-report-changes.md`.

## 2026-11-12: Containers, Redis, Celery worker, and OpenAPI export (Codex)

- **Feature and IDs:** Backend infrastructure, NFR-2, NFR-19, NFR-21, NFR-23.
- **Built:** Added Redis, API, and Celery worker services beside the existing PostgreSQL 17 service; added pinned Celery and Redis dependencies, Redis settings, a worker entrypoint, an API Dockerfile, and an OpenAPI export script. Added focused infrastructure tests and the backend test ledger.
- **Tested:** Focused infrastructure tests: 4 passed. Full backend suite: 94 passed, 0 failed, 1 existing Starlette/AnyIO deprecation warning. Console and JUnit output are saved under `docs/test-results/step1-containers-20261112-2200.*`. Docker Compose validation was not run because Docker is unavailable. Local Ruff validation was not run because Ruff is not installed locally; CI installs it.
- **Cut or partial:** No Celery feature tasks were added; profile embedding regeneration and deletion purge remain scheduled for step 9. The Backend Implementation Guide was not present, so BT-01..BT-12 mapping remains pending.

## 2026-11-11: Profile verification scoring and appeals (Codex)

- **Feature and IDs:** Hybrid profile verification, FR-12, FR-14, FR-15, FR-16, FR-19, FR-20, FR-21, NFR-9, NFR-11, NFR-19, NFR-22.
- **Built:** Added consented mentor/investor verification, Firecrawl portfolio extraction and Gateway-based consistency assessment, configurable score bands, persisted signals and threshold version, status history, one appeal, report-to-review handling, and rescore lock. Matching now returns mentors/investors only when their verification status is verified. Added migration `0009`.
- **Tested:** Backend suite: 90 passed; RAG suite: 11 passed; focused verification, matching, and migration tests: 23 passed. One existing Starlette/AnyIO deprecation warning remains. Firecrawl and Gemini calls were mocked; no live provider or PostgreSQL server was used.
- **Cut or partial:** LinkedIn OAuth is cut; SECP identity checking is manual, and the admin review/decision routes are the next feature. High scores remain pending until a reviewer confirms SECP identity. Threshold defaults are not calibrated.
- **Differs from the report?** No; the method for the report's SECP cross-check is recorded in `docs/DECISIONS.md`.

## 2026-11-11: Job and internship board (Codex)

- **Feature and IDs:** Job and internship board, FR-6, FR-24, FR-25, NFR-5.
- **Built:** Verified founders can create, edit, close, delete listings and review applicants. Talent can browse, save, apply, and track application status. Added migration `0008` and documented the routes.
- **Tested:** Backend suite: 81 passed (one existing Starlette/AnyIO deprecation warning); RAG suite: 11 passed. Job tests cover role/owner checks, verification gates, duplicate applications, closed listings, status changes, and cascading deletion. Migration test checks all three tables. No live PostgreSQL server was used.
- **Cut or partial:** Search/filter polish and candidate application withdrawal are not included in this minimum slice.
- **Differs from the report?** No; implements FR-6, FR-24, and FR-25.

## 2026-11-11: Private resume upload and line edits (Codex)

- **Feature and IDs:** Resume and profile optimizer, FR-5, NFR-7, NFR-19, NFR-22.
- **Built:** Added a talent-only raw-PDF upload API with a 5 MiB cap, MIME and signature checks, PDF page/text limits, explicit processing consent recorded by version and time, and storage outside served/source directories. The LLM Gateway returns structured line edits; each `before` must match the exact numbered extracted line. Saved owner-scoped history and a delete endpoint remove the stored file. Added migration `0007`; private local storage is ignored by git. No package was installed.
- **Tested:** Backend suite: 79 passed (one existing Starlette/AnyIO deprecation warning); RAG suite: 11 passed; `git diff --check` passed; Alembic head is `0007`. Tests use synthetic PDFs and a mocked gateway to cover upload limits, consent, PDF extraction, ownership, deletion, line validation, and provider failure. No live Gemini call was made.
- **Cut or partial:** PDF only; DOCX and scanned-PDF OCR are not supported. A working Gemini configuration is still required for real suggestions.
- **Differs from the report?** No; this implements the report's consented CV upload, private storage, and line-level suggestions.

## 2026-11-11: Market research with saved evidence (Codex)

- **Feature and IDs:** Market research synthesis, FR-4, NFR-19, NFR-22.
- **Built:** Added founder-only `POST /api/v1/market-research` and paged startup-owned history. Firecrawl search is bounded to five public web results, excludes major social-profile domains, validates and truncates source content, and logs counts/timing without the query or API key. Gemini receives only the retrieved evidence and produces a structured interpretation with source IDs. The API validates every source ID, returns evidence separately, and stores query, evidence, interpretation, model, and prompt version. Empty evidence is recorded as `insufficient_evidence`; failed synthesis remains `generation_failed` with evidence saved. Added migration `0006` and configuration examples.
- **Tested:** Backend suite: 70 passed (one existing Starlette/AnyIO deprecation warning); RAG suite: 11 passed; `git diff --check` passed. Mocked HTTP tests cover Firecrawl request/response handling and sanitized failures; API tests cover source-grounded output, empty search, invalid citations, provider failure, history, and startup ownership. No live Firecrawl or Gemini request was made.
- **Cut or partial:** Configure `FIRECRAWL_API_KEY` and a working Gemini key/model before using live search and synthesis. Search uses a synchronous request with a 25-second provider limit; caching/refresh remain cut per plan.
- **Differs from the report?** No; this implements the report's evidence-separated synthesis and saved output/evidence log.

## 2026-11-11: Pitch simulator rubric and failure recovery (Codex)

- **Feature and IDs:** Pitch simulator, FR-3, FR-28, NFR-15.
- **Built:** Added fixed 1-to-5 anchors for clarity, written confidence, and content. The rubric scores the full founder transcript, explains evidence, and avoids inferring emotional state or predicting funding. Kept model calls behind the LLM Gateway and preserved the submitted founder answer before generation.
- **Tested:** Backend suite: 62 passed (one existing Starlette/AnyIO deprecation warning); RAG suite: 11 passed; `git diff --check` passed. Mocked tests check rubric delivery, completed-session scores/history, and transcript preservation after a generation failure.
- **Cut or partial:** No live Gemini pitch session was run; provider availability still depends on the configured account/model. Readiness was already implemented with seven validated dimensions, versioned storage, and founder history.
- **Differs from the report?** No; this makes the report's fixed rubric concrete while retaining its three scoring areas.

## 2026-11-10: Matching ranking and mutual-accept request lifecycle (Codex)

- **Feature and IDs:** Ecosystem matching baseline, FR-7, FR-10, FR-29, NFR-3, NFR-6, NFR-15, NFR-20.
- **Built:** Added the report's top-K range (1 to 3, default 3). Role, active-account, open-profile, embedding-model, geography, and investor verification/readiness eligibility are applied before PostgreSQL's vector limit. Sector and stage remain weighted factors per the coding plan. Excluded vector-dimension mismatches before cosine distance; select only needed user fields; join saved match records to avoid per-candidate lookups. Added explicit request, accept, and decline routes with stored request status and requester, mutual-accept contact reveal, and a migration that backfills existing acceptance flags. The legacy accept route remains compatible by treating its first call as the request.
- **Tested:** Backend suite: 61 passed (one existing Starlette/AnyIO deprecation warning); RAG suite: 11 passed. PostgreSQL-dialect compilation checks candidate filtering before vector top-K and avoids selecting password hashes; migration tests cover legacy-state backfill. The actual PostgreSQL/pgvector server and seeded two-second performance target were not tested because Docker and PostgreSQL are unavailable here.
- **Cut or partial:** The seeded demo performance evaluation remains. Report alignment for weighted sector/stage scoring is recorded in `docs/DECISIONS.md` and `docs/pending-report-changes.md`.
- **Differs from the report?** Yes: sector and stage are weighted ranking factors per the coding plan, while the report currently describes them as hard filters. The reason and required report update are recorded in the decision log and pending changes table.

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

## 2026-11-12: FYP-1 schema gap report (Codex)

- **Feature and IDs:** Schema inventory; supports FR-6, FR-8, FR-10, FR-12, FR-13, FR-14, FR-15, FR-16, FR-17, FR-19, FR-20, FR-21, FR-22, FR-24, FR-25, FR-26, FR-27, FR-29 and NFR-15. Compliance rows are regression-only and out of scope.
- **Built:** Added `docs/schema_gap_report.md`, mapping all 37 FYP-1 ER-diagram tables to their current implementation status and documenting differing physical names and columns.
- **Tested:** Ran the existing backend suite with results saved under `docs/test-results/`; no schema or application behavior changed.
- **Cut or partial:** No migrations, tables, API contracts, or compliance changes. The missing Backend Implementation Guide leaves BT-01..BT-12 mapping pending.
- **Differs from the report?** The report baseline is represented by existing ER diagrams because the formal data dictionary is not present in this checkout.

## 2026-11-12: Auth consent, deletion, and fake LinkedIn provider (Codex)

- **Feature and IDs:** FR-17, FR-22, FR-27, NFR-4, NFR-5, NFR-9, NFR-11, NFR-22.
- **Built:** Added registration consent records, validated role path registration with no public admin role, consent withdrawal, immediate account disablement with a 30-day purge schedule, `oauth_identities`, and a fake LinkedIn provider behind a provider interface. Added migration `0010` and updated existing registration tests for the approved contract.
- **Tested:** 99 backend tests passed with one existing Starlette/AnyIO deprecation warning; compliance/RAG tests ran only as regression tests and remain out of scope.
- **Cut or partial:** Real LinkedIn OAuth credentials and network integration are not included; the purge worker remains step 9.
- **Differs from the report?** Yes. The report still needs to describe the new auth endpoints and the fake-provider boundary; see `docs/pending-report-changes.md`.

## 2026-11-12: Talent profiles and five-signal verification (Codex)

- **Feature and IDs:** FR-12, FR-13, FR-14, FR-15, FR-19, FR-20, NFR-9, NFR-15, NFR-22.
- **Built:** Added `talent_profiles` and `verification_signals` in migration `0011`; added optional validated GitHub links, full talent verification, versioned configurable weights/thresholds, manual-SECP and portfolio interfaces, all five signal inputs/outcomes/reasons, and auto-verified/review/auto-rejected band handling.
- **Tested:** 102 backend tests passed with one existing Starlette/AnyIO deprecation warning; compliance/RAG tests ran only for regression and remain frozen/out of scope.
- **Cut or partial:** GitHub activity metrics are represented by optional link presence in this slice; real SECP lookup is intentionally not implemented. High scores remain pending while the manual SECP signal is pending.
- **Differs from the report?** Yes. The report needs to describe full talent verification and normalized signal audit storage; see `docs/pending-report-changes.md`.
## 2026-11-12: LLM Gateway cache, queue position, and call metadata (Codex)

- **Feature and IDs:** NFR-2, NFR-8, NFR-11, NFR-19, NFR-22.
- **Built:** Added a private per-user disk cache for non-compliance structured results with a 24-hour expiry and account-deletion cleanup; a FIFO tracker reports waiting position in internal logs and persisted metadata; migration `0012` stores sanitized per-attempt gateway metadata without prompt, evidence, input, or output content. Public route contracts and compliance generation signatures/behavior remain unchanged.
- **Tested:** 114 backend tests passed; 22 compliance regression tests passed; 11 RAG regression tests passed. Each run has console and JUnit output in `docs/test-results/`. One existing Starlette/AnyIO deprecation warning appeared in backend and compliance runs.
- **Cut or partial:** Cache is process-local filesystem storage; no distributed cache or API queue-position field was added. Report follow-up is in `docs/pending-report-changes.md`.
- **Differs from the report?** Yes. The report currently describes prompt/evidence logging; update it to describe sanitized metadata and the private cache as specified in `docs/pending-report-changes.md`.
## 2026-11-13: Matching eligibility and contact visibility review (Codex)

- **Feature and IDs:** Matching, FR-7, FR-10, FR-29, NFR-3, NFR-5, NFR-6.
- **Built:** Fixed founder match history to filter closed profiles and inactive candidates in the database query before pagination. Added regressions for page filling, inactive candidates, contact visibility while acceptance is pending, and the PostgreSQL pgvector cosine-distance query. Existing ranking weights and sector/stage scoring decision were preserved.
- **Tested:** 15 focused matching tests, 116 backend tests, 22 isolated compliance regression tests, and 11 RAG regression tests passed. Saved console and JUnit output under `docs/test-results/`; `git diff --check` passed.
- **Cut or partial:** No live PostgreSQL/pgvector server was used; PostgreSQL SQL compilation and the local Python cosine path were tested. Match records remain startup-anchored, so the direct talent–mentor pairing named by FR-7 is not implemented and needs an API/domain-model decision.
- **Differs from the report?** Sector/stage weights remain as already recorded in `docs/DECISIONS.md` and `docs/pending-report-changes.md`. `main.tex` is absent from this checkout, so review used `docs/context/requirements.md` and `docs/context/architecture.md`.
## 2026-11-13: Job board eligibility and listing validation (Codex)

- **Feature and IDs:** Job and internship board, FR-6, FR-24, FR-25, NFR-5, NFR-22.
- **Built:** Talent can save only open listings from verified startups, matching browse and application eligibility. Listing create and patch now reject whitespace-only titles, descriptions, and locations. No endpoint or database contract was added.
- **Tested:** 4 focused job tests, 118 backend tests, 22 isolated compliance regression tests, and 11 RAG regression tests passed. Console and JUnit output is saved under `docs/test-results/`; `git diff --check` passed.
- **Cut or partial:** No frontend job-board walkthrough or live deployment test was run. The report source `main.tex` is absent; the behavior was compared with `docs/context/requirements.md` and the coding plan.
- **Differs from the report?** No change to the feature flow or schema; this closes consistency and input-validation gaps in the existing contract.

## 2026-11-13: Background profile embeddings and account deletion purge (Codex)

- **Feature and IDs:** Profile matching embeddings (FR-7, NFR-20); consent deletion (FR-27, NFR-10, NFR-11); worker and scheduler (NFR-2, NFR-21).
- **Built:** Added retryable, result-free Celery tasks to regenerate saved profile embeddings and purge inactive accounts once their 30-day deletion date is due. Purge clears per-user response cache, private resume PDFs, and cascaded user data. A single Beat service queues purges every 15 minutes. Profile saves enqueue embedding work and fall back to synchronous generation if Redis is unavailable. No migration or endpoint contract changed.
- **Tested:** 122 backend tests passed with 93.8% app line coverage (848/904 executable line starts; 2329.72 seconds). After final test dependency wiring, 29 focused task, infrastructure, matching, and admin tests passed. The isolated compliance regression suite passed 22 tests and the RAG regression suite passed 11. One existing Starlette/AnyIO deprecation warning appeared in backend and compliance runs. Console, JUnit, and coverage outputs are recorded in `docs/test-results/` and `backend/TESTS.md`.
- **Cut or partial:** No live Redis/Celery deployment or PostgreSQL purge run was performed; task behavior was verified with isolated SQLite, private disk-cache, and PDF fixtures.
- **Differs from the report?** No known difference from the available requirements summary; `main.tex` is absent from this checkout.
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
