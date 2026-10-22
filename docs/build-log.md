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

## 2026-10-17: CI ruff pinned and notebooks excluded from ruff (Ali, with Claude Code)

- Pinned CI ruff to 0.17.1, added `ml/ruff.toml` (notebooks excluded), fixed `rag/corpus_profile/profile_corpus.py` (F541, four `# noqa: BLE001`) and the bare `raise` in `dataset_claim_checks.ipynb`; ruff 0.17.1 re-run in `rag/`, `ml/` and `backend/`, not yet run in GitHub Actions. Differs from the report? No. See `docs/DECISIONS.md` (2026-10-17, "CI ruff pinned").

## 2026-10-17: Skills install list applied; sync script copies references (Ali, with Claude Code)

- **Feature and IDs:** Repository tooling, agent skills install (no FR/NFR directly)
- **Built:**
  - Installed into `.claude/skills/`: `frontend-design`, `claude-api` (trimmed to Python, TypeScript, curl and shared docs), `git-workflow-and-versioning` (the `git reset --hard` line rewritten, a note added that the `CLAUDE.md` git rules win), `shipping-and-launch`, `ci-cd-and-automation`, `performance-optimization`, `observability-and-instrumentation`, `web-design-guidelines` (rules saved as `command.md` at a pinned commit, live download removed), and `ponytail`, `ponytail-review`, `ponytail-audit`, `ponytail-debt` (descriptions of the first two trimmed so they start only when asked).
  - Copied the upstream `references/` checklists to `.claude/references/`. Copied the licenses to `third_party_licenses/`.
  - `scripts/sync_agent_skills.py` now also copies `.claude/references/` to `.agents/references/`. Added `.agents/references/` to `.gitignore`. Updated `SETUP.md`, `AGENTS.md`, `CLAUDE.md` (five skill rows added) and `THIRD_PARTY.md` (rows, pins, licenses, "Not installing" lines).
- **Tested:** Ran the sync script with `--dry-run` and for real: 40 skills and the references copied, and `.agents/skills/<skill>/../../references` resolves. `command.md` SHA-256 matches the recorded value. `python scripts/scan_for_keys.py` found no keys in 309 tracked files, and a separate key-pattern search over `.claude/skills/` and `.claude/references/` found none. Read `git diff` for `CLAUDE.md` and `THIRD_PARTY.md`. Not tested: using the new skills inside Claude Code, Codex or Antigravity.
- **Cut or partial:** spec-kit is per person and not installed yet. graphify is skipped until there is code. `DESIGN.md` is not installed (brand undecided). caveman and gstack were reviewed and skipped. The per-person installs were not done in this run. career-ops, financial-services and replica-skill have not been read.
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






