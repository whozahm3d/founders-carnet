# Coding plan (Oct 19 to Nov 8, 2026)

Source: report Chapter 2 (Delivery Priority and Fallback Plan, 2.6.7), Chapter 4 (feature table 4.1, FR and NFR tables), Chapter 5 (Development Methods), Chapter 6 (limitations, FYP-2 plan), and `SPRINT_PLAN.md` v3 (Sprints 6 to 8).

This file turns the report into a build plan. It adds nothing to scope. Anything the report does not settle is marked **not in report** and is a proposal for the team to accept or change (record it in `docs/DECISIONS.md` when you do). If this file and the report disagree, the report wins.

## Decision already taken

All 12 FYP-1 features are attempted. Each has a minimum slice (the smallest version that still counts as the feature) and a cut line. Whatever is unfinished on Nov 8 goes into the Chapter 6 limitations list and moves to FYP-2. See `docs/DECISIONS.md` (2026-10-16 entry on scope).

## Build order (from the report's fallback list)

If work falls behind, items lower in this list are dropped first.

1. Foundations: authentication, role-based access, profiles.
2. Compliance assistant and its evaluation (the FYP-1 checkpoint).
3. Matching baseline.
4. Readiness, then pitch simulator, then market research.
5. Resume optimizer and job board.
6. English, Urdu, Roman Urdu benchmark (FYP-2, not built now).
7. Supporting classifiers on the FINAL datasets (FYP-2, not built now). Only the dataset cleaning in `docs/datasets.md` can start in FYP-1.

Where verification, the admin console, consent, usage guides and job posting sit in this order is **not in report**. The proposal below puts verification, admin console and consent right after foundations (they gate investor visibility, FR-10, and contact reveal, NFR-6), guides last (FR-18 is text), and job posting with the job board.

## Week map (proposal, not in report)

| Sprint | Dates | Goal |
| --- | --- | --- |
| 6 | Oct 19 to 25 | Foundations, corpus pipeline running, frontend shell and role dashboards |
| 7 | Oct 26 to Nov 1 | Compliance end to end plus the formal gold-set run; matching baseline; verification and admin console; readiness |
| 8 | Nov 2 to 8 | Pitch, market research, resume, job board and posting, guides, integration, early Turnitin submission |

Proposed feature freeze: about Nov 6. Nov 7 and 8 are for integration, tests, screenshots for the report, and bug fixes only. The report is due Nov 11.

## Per-feature plan

Owners are proposals: Ali (AI/ML), Shahzeb (frontend), Taha (backend). Every feature needs a backend route, a frontend screen and a test. "Slice" is the minimum that counts. "Cut" is what is dropped first.

### 0. Account and profile foundations (FR-22, FR-23, FR-1, NFR-4, NFR-5, NFR-8, NFR-22)

- Slice: register with email and password and pick one role; login issues a JWT; gateway middleware checks it on every request and limits each endpoint to the caller's role; logout ends the session; founder profile with traction and business data; first versioned migration.
- Cut: LinkedIn sign-in (needs OAuth app approval, assumption A-2 in the report). Email and password alone is enough for the slice.
- Tests: no token, wrong role, expired token on a protected route (NFR-5). Passwords never in logs (NFR-4).
- Risk: low. Protected, do not cut.

### 1. Compliance assistant (FR-8, NFR-12, NFR-13, NFR-14, NFR-11, NFR-20; R-2, R-3, R-4)

- Slice: ingest the 11 corpus documents (`docs/context/corpus.md`), section-aware chunks, embeddings in pgvector, retrieval, a Gemini answer through the LLM Gateway built only from retrieved passages, citations with document title and effective date, a validation step, "no supported answer" when nothing supports it, query logging.
- Evaluation: hand-verified gold question set (the sprint plan says 20 to 22 questions). Measure citation correctness, retrieval recall, and correct abstention. RAGAS is supporting only. Out-of-scope questions are tagged with the six Peng et al. categories. English only.
- Checkpoint: if it cannot give cited answers and abstain correctly on a held-out set, no lower item is extended in FYP-2 until it can.
- Never: answer tax from PSEB pages; say whether a licence applies to a case (R-4); index a superseded version.
- Cut: query log view for admins. Never cut abstention or citations.
- Risk: medium (the VOSS circular is a scanned page and needs OCR or hand transcription). Protected, do not cut.

### 2. Ecosystem matching, FYP-1 baseline (FR-7, FR-10, FR-13, FR-29, NFR-3, NFR-6, NFR-15, NFR-20)

- Slice: embeddings and pgvector similarity plus five factor weights (sector_fit, stage_fit, skill_overlap, availability_fit, ticket_fit); results store their factors so "why was I matched" is a database read; mutual accept before contact details show; mentors can be open or closed (FR-29); investors see only verified startups with a completed readiness assessment (FR-10); GitHub link feeds the skill factor (FR-13, basic).
- No LLM call in matching. Ever.
- Evaluation: seeded demo dataset for the 2 second target (NFR-3). Trained re-ranker, NDCG@K and MRR, and the 150 to 300 labeled pairs are FYP-2. The FYP-1 result is stated as a baseline or pilot result (R-1).
- Cut: GitHub signal (FR-13).
- Risk: medium. Protected.

### 3. Startup readiness scoring (FR-2, NFR-15, NFR-2)

- Slice: seven dimensions scored 1 to 5, each with reasoning and a next action, stored with the rubric version; structured output validated by a Pydantic model.
- Evaluation: the report plans a comparison against 2 or 3 human reviewers on 10 to 15 ideas (Spearman) in FYP-2. Who the reviewers are is **not in report**. FYP-1 reports the score as uncalibrated.
- Risk: medium (no calibration yet).

### 4. Pitch simulator (FR-3, FR-28)

- Slice: multi-turn investor conversation, scored for clarity, confidence and content against a fixed rubric, saved per session; founders can view their history with scores (FR-28).
- **Not in report:** the data dictionary lists five scoring areas for pitch; FR-3 says three. Use FR-3 (the report) and fix the data dictionary.
- Cut: history screen detail (keep the list).
- Risk: medium. Sits below matching in the fallback list.

### 5. Market research synthesis (FR-4)

- Slice: competitor and market-size summary from live web search (Firecrawl), with evidence kept apart from interpretation and the sources listed. Public pages only, no scraping of individual personal profiles (PECA 2016).
- Cut: caching and refresh. Keep one working query path.
- Risk: medium-high (Firecrawl free-tier limits, R-5).

### 6. Resume and profile optimizer (FR-5)

- Slice: upload a CV (type and size checked, stored outside the served folder, NFR-7), get line-level before and after suggestions through the LLM Gateway.
- Test data: the team's own resumes and resumes shared with consent. No external resume dataset.
- Risk: medium. Low in the fallback list, so cut early if behind.

### 7. Job and internship board (FR-6, FR-25) and job posting (FR-24)

- Slice: verified founders publish, edit, close and delete listings and see applications (FR-24); talent browses, saves, applies and tracks status (FR-25, FR-6).
- Cut: filters, saved-listing polish. Posting and board are one build.
- Risk: low technically, low priority. Cut early if behind.

### 8. Hybrid profile verification (FR-12, FR-14, FR-15, FR-16, FR-19, FR-20, FR-21, NFR-9)

- Slice: score each mentor or investor profile from the signals (LinkedIn OAuth, SECP cross-check, completeness, GitHub activity, portfolio link check); thresholds in configuration; high score verifies, low score rejects with a logged reason, middle goes to human review; status and reason visible to the user (FR-15); one appeal (FR-21); reported or blocked profiles go to review and are not re-scored (FR-16). Log score, signal values and band (FR-19).
- The portfolio link check (FR-20) is the only prompted call. The other four signals are rules the team writes.
- **Not in report:** how the SECP cross-check is done (manual lookup, public search, or a stub). Decide and record it.
- Cut: LinkedIn OAuth signal if the OAuth app is not approved (A-2). Run on the remaining signals and say so.
- Risk: high. Claim only that the rules raise the cost of casual fakery (R-7).

### 9. Administrative review console (FR-26)

- Slice: list escalated profiles and appeals with signals and score; reviewer approves or rejects with a reason; each decision recorded against the reviewer.
- Risk: low. Needed for verification to be testable end to end.

### 10. Consent management (FR-17, FR-27, NFR-9, NFR-10, NFR-11)

- Slice: consent notice and trust note before profile data is submitted; users can review or withdraw consent for non-essential processing; account deletion request disables the account at once.
- Cut: the 30-day purge job (NFR-10). Record the request and disable the account; say the purge is not automated if it is not.
- Risk: low.

### 11. Usage guides (FR-18)

- Slice: team-written guides reachable from every dashboard. Static pages.
- Risk: none. Do it last.

### 12. Supporting classifiers (FYP-2; not an FYP-1 feature)

- Adopted 2026-10-19; supervisor approval pending. Three offline classifiers: resume role (haider, Bhawal as external check), startup outcome (Success/Fail), follow-on funding (Investments). Labels and rules are in `docs/datasets.md`.
- FYP-1 slice: only the cleaning of the datasets (the Success/Fail 1990 to 2015 date filter and the haider deduplication). No training and no FR or NFR ID.
- Never: show a classifier output to a user as a probability of success, failure or funding; claim accuracy before a run exists.
- Cut: all of it. It sits below everything else and is dropped first.
- Risk: low for the build, medium for the claims. The two Crunchbase sets are global data.

## Cut order if time runs short

Cut from the bottom of this list upward. The first items go first.

0. Supporting classifier work, including the dataset cleaning for it.
1. Usage guides polish, consent purge job, query-log view.
2. Job board filters and saved listings; job posting extras.
3. Resume optimizer.
4. Market research caching; market research itself.
5. Pitch history screen; pitch simulator depth.
6. LinkedIn OAuth and GitHub signals.
7. Readiness, then verification, then matching.
8. Compliance assistant and foundations are never cut.

Cut items are reported in Chapter 6 limitations and moved to FYP-2. Do not leave a half-working feature in the demo without saying so.

## Tests and evaluation that must exist by Nov 8

- Role-scoped access: no token, wrong role, before and after mutual acceptance (NFR-5, NFR-6).
- No contact details in any API response before both sides accept (NFR-6).
- Unit tests on the factor scoring and ranking (matching).
- Compliance gold-set run with the three measures above, results saved for Chapter 6.
- CI (NFR-23): lint and tests on every pull request. `ci.yml` has not run on GitHub yet. Push a trivial branch early in Sprint 6 to confirm it works.
- Versioned migrations rebuild an empty database (NFR-22).

## Not in report (open, team decides)

- Which `DESIGN.md` brand to use. Not decided; discuss after most of the functionality is done. Do not copy a `DESIGN.md` until then.
- Who the 2 or 3 readiness reviewers are, and how the SECP cross-check works. Not decided; to be discussed later.
- Where verification, admin console, consent and guides sit in the build order (proposal above).
- Lint tool beyond `ruff`, and Railway versus Render.
- Feature freeze date (proposed Nov 6).
- Classifier column names, split sizes and the Investments label rule. Set them when the scripts are written and log them in `docs/DECISIONS.md`.
