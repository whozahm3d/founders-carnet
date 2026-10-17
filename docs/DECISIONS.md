# Decisions log

Dated entries, newest first. Each entry has the context, what was tried, what was found, what was decided, and why. Add an entry every time the code or the report is changed so the two agree.

## 2026-10-17: CI ruff pinned to 0.17.1; notebooks excluded from ruff

**Context:** The CI job "Python (rag)" failed on ruff in `rag/corpus_profile/profile_corpus.py`, and "Python (ml)" fails on the two notebooks in `ml/notebooks/`. `.github/workflows/ci.yml` installed ruff with no version (`pip install ruff pytest`) and the repo has no ruff config. This touches NFR-23 (linting on every pull request).

**What we tried:** Ran ruff 0.17.1 with `uvx` in `rag/`, `ml/` and the repo root, and read the settings it resolved.

**What we found:** With no config, ruff 0.17.1 enables 407 rules by default, including BLE001, FURB167, PLE0704, S112, RUF046 and SIM115, and it lints `.ipynb` and `.md` files too. `rag/` had one F541 and four deliberate broad excepts (BLE001). `ml/` had 30 errors, all in the two notebooks. The repo root had 280, of which 246 are in `.claude/skills/`, 3 in `.claude/hooks/guard.py` and 1 in `scripts/backup.py`. CI only lints inside `backend/`, `rag/` and `ml/`.

**Decision:**

- CI installs `ruff==0.17.1` (`ci.yml`, the install step). An unpinned install meant the default rules could change under us on any ruff release.
- Notebooks are excluded from ruff with `ml/ruff.toml` (`extend-exclude = ["*.ipynb"]`), because they are analysis scratch work. `.py` files stay linted.
- `rag/corpus_profile/profile_corpus.py`: removed the extra `f` prefix. The four broad excepts are deliberate (the profiler must record a bad file and keep going), so each carries `# noqa: BLE001` with a reason.
- `ml/notebooks/dataset_claim_checks.ipynb`: the bare `raise` in `read_csv_chunks` now raises a `ValueError` that names the file. Nothing else in the notebook changed.
- The repo root and `.claude/` are not linted by CI. No root ruff config was added, and `.claude/skills/`, `.claude/hooks/guard.py` and `scripts/backup.py` were not changed.

**Why:** A pinned version keeps CI results the same until we choose to upgrade. Notebooks are for exploration, not shipped code, so linting them adds noise.

**Follow-ups:** To upgrade ruff, change the pin on purpose and re-run the folders. Anything in `ml/` that ships moves into a `.py` module with tests, where ruff applies. The `.claude/hooks/guard.py` and `scripts/backup.py` findings are left for the team to decide.

## 2026-10-17: Skills install finished; what is and is not installed

**Context:** The install run against the "Final install list" in `THIRD_PARTY.md`. It touches `.claude/skills/`, `.claude/references/` and `scripts/sync_agent_skills.py`. It corrects the 2026-10-16 entry "Skills and plugins install list fixed", which says spec-kit, graphify, awesome-design-md and rea are installed. That entry is left as it was, as history.

**What we tried:** Cloned each source repo into a scratch folder outside the repo, read the skills, checked licenses, pinned commits, and copied only what the list allows.

**What we found:** `frontend-design`, `claude-api` (trimmed), `git-workflow-and-versioning`, `shipping-and-launch`, `ci-cd-and-automation`, `performance-optimization`, `observability-and-instrumentation`, `web-design-guidelines` (rules file saved locally, no live download) and four `ponytail` skills went into `.claude/skills/`. The upstream `references/` checklists went into `.claude/references/`, because the new and the older skills link to `../../references/`. Codex and Antigravity could not follow those links, because the sync script copied only the skills.

**Decision:**

- spec-kit is per person and not installed yet. Each person runs `uv tool install specify-cli==<version>` on their own laptop. Nothing is copied into the repo, and `specify init` needs its own OK.
- graphify is skipped until `backend/` or `frontend/` has code.
- `DESIGN.md` is not installed because the brand is undecided.
- caveman was reviewed and skipped: its own README calls the gain "inside the noise", and most of its skills use the hosted Caveman Cloud gateway or rewrite `CLAUDE.md`-style files.
- gstack was reviewed and skipped: it is not skills-only. It needs a runtime install, has hooks and a telemetry step, and some skills commit, push and deploy.
- `scripts/sync_agent_skills.py` now also copies `.claude/references/` to `.agents/references/` (copy only, never deletes). `.agents/references/` is in `.gitignore` next to `.agents/skills/`. `SETUP.md`, `AGENTS.md`, `CLAUDE.md` and `THIRD_PARTY.md` say so.

**Why:** Keep to the rules in `CLAUDE.md`: no hooks that run on their own, no tool that commits, pushes or deploys for us, and no hosted gateway between us and the model. Codex and Antigravity users should see the same skills and the same checklists as Claude Code.

**Follow-ups:** Choose the `DESIGN.md` brand. Each person installs spec-kit when they want it. Run graphify once there is code. Read career-ops, financial-services and replica-skill before deciding on them. Do the per-person installs (docx, pdf, pptx, xlsx, the code-review plugin, rea, the no-license repos).

## 2026-10-17: Roman-Urdu-Parl split numbers discrepancy between files and report

**Context:** The report (Chapter 3, Table of external datasets) states Roman-Urdu-Parl has 6,374,678 pairs (6,333,218 train, 20,719 validation, 20,741 test).

**What we tried:** Checked the dataset files using `ml/notebooks/dataset_claim_checks.ipynb`.

**What we found:** In the local files, validation (20,719) and test (20,741) match the report exactly. However, the train split has 6,365,808 rows (which matches the original paper's headline figure), versus 6,333,218 in the report. The total count in the files is 6,407,268 versus 6,374,678 in the report.

**Decision:** Treat the unlabeled split in the files as train and keep the claim check as FAIL. State that the source of 6,333,218 is unknown. Do not claim it is wrong until the Hugging Face dataset card is checked.

**Why:** The files and the report disagree. Keeping the claim as FAIL ensures the mismatch is tracked honestly and logged for resolution.

**Follow-ups:** Check the Hugging Face dataset card for `Mavkif/Roman-Urdu-Parl-split`. Update the report to the file numbers (6,365,808 train; 6,407,268 total) unless a source for 6,333,218 is found. Logged in `docs/pending-report-changes.md`.

## 2026-10-17: Tech-niche focus and dataset search/swap rules

**Context:** The Crunchbase datasets cover companies across all sectors. The platform targets the Pakistani tech startup niche.

**What we decided:**

1. **Tech filter:** When using Crunchbase data for schema design or profiling, filter rows to tech categories using the `category_list` column. LinkedIn and HSE have no equivalent tech filter; use them as-is with awareness of that limitation.

2. **Dataset search rule:** The team may look for better or more Pakistan-specific datasets on Kaggle and Hugging Face after the D2 or mid-term milestone. Before any new dataset is used, it must have an entry in `docs/datasets.md` (what it contains, why it was chosen, which user input it serves) and a reason logged here in `docs/DECISIONS.md`. If it replaces one of the five kept datasets, add a row to `docs/pending-report-changes.md` so the report's dataset table is updated.

**Why:** Scope discipline. The report targets one niche; the datasets must match.

## 2026-10-16: All 12 FYP-1 features are attempted, with cut lines

**Context:** The report lists 12 features for FYP-1 and a fallback order if work falls behind. The coding window is Oct 19 to Nov 8 (Sprints 6 to 8) and the report is due Nov 11.

**What we tried:** Read the Chapter 4 feature table, the Delivery Priority section, and the Chapter 6 plan to see what a smaller FYP-1 would have to drop.

**What we found:** The report does not drop any of the 12. It only says that items lower in the fallback list are dropped first. Not in the report: where verification, the admin console, consent and usage guides sit in that order, who the readiness reviewers are, and how the SECP cross-check works.

**Decision:** We attempt all 12. Each has a minimum slice and a cut line in `docs/context/coding-plan.md`. Foundations and the compliance assistant are never cut. What is unfinished on Nov 8 is listed in the Chapter 6 limitations and moves to FYP-2.

**Why:** It follows the report's fallback list and keeps every claim in the report honest.

**Also settled (2026-10-16):** the proposed build order for verification, admin console, consent and guides is accepted as an internal plan and is not added to the report. Undecided for now: the readiness reviewers, the SECP cross-check method, the migration tool.

**Follow-ups:** Update the Chapter 6 objectives table ("Main flows in FYP-2") and the limitations list once we know what was cut (see `docs/pending-report-changes.md`). Decide the "not in report" items listed in the coding plan.

## 2026-10-16: Compliance corpus is 11 documents, committed in rag/data/ with a manifest

**Context:** The report fixes the corpus. The files are large (the Finance Act PDF is 42 MB; about 59 MB in total).

**What we tried:** Collected the 10 PDFs and one page snapshot into `rag/data/` and compared each file's SHA-256 with `rag/corpus_profile/profile_report.md`.

**What we found:** The hashes match (the `.txt` copy of the FBR page is not in the profile report). The Seventh Schedule URL slug says 2023, but the file is the 20 Apr 2026 version.

**Decision:** The 11 files are committed in `rag/data/`, so Taha and Shahzeb get them on clone and the evaluation can be reproduced. This is an exception to the raw-data rule: they are public official documents, not datasets. `rag/corpus_manifest.md` is committed too and mirrors the `corpus_document` table. `docs/context/corpus.md` holds the indexing rules.

**Why:** Easier for the team and for evaluation. A committed file stays in git history, so a replaced version adds size; update a file only for a reason that is logged here.

**Follow-ups:** Load the manifest into `corpus_document`. Decide OCR or hand transcription for the VOSS scanned page. The Sprint 4 corpus list in `SPRINT_PLAN.md` (5 documents) is stale.

## 2026-10-16: Skills and plugins install list fixed; Codex and Antigravity supported

**Context:** The team has one Claude Code seat. Taha and Shahzeb mostly use Codex and Antigravity, which do not read `.claude/skills/`.

**What we tried:** Read the install and skills documentation of both tools and the README of each candidate repo.

**What we found:** Codex reads skills from `<repo>/.agents/skills`. Antigravity reads workspace skills from `<project>/.agents/skills/` and rules from `AGENTS.md` or `GEMINI.md`. Which of the two wins when both exist is not documented.

**Decision:** The final install list is in `THIRD_PARTY.md`. Not installed: codebase-memory-mcp, claude-swarm, screenshot-to-code, AgentForge. awesome-design-md, spec-kit, graphify and rea are installed. `scripts/sync_agent_skills.py` copies `.claude/skills/*` to `.agents/skills/` (gitignored). `GEMINI.md` points to `AGENTS.md`.

**Why:** One source of skills, no hooks that run on their own, and the same rules for every tool.

**Follow-ups:** Choose one `DESIGN.md` brand. Fill in commit hashes and licenses in `THIRD_PARTY.md` after the install. Read career-ops, financial-services and replica-skill before deciding on them.

## 2026-10-16: Report updated to Node 24 and four top-level folders

**Context:** The report said Node.js 20 and described three top-level directories. The repo uses Node 24 and has four folders: `frontend/`, `backend/`, `rag/`, `ml/`.

**What we tried:** Compared `main.tex` and the master document with `CLAUDE.md` and the two 2026-10-15 entries below.

**What we found:** `main.tex` named Node 20 in the technology list, and described "three top-level directories" in the source control section and "frontend, backend, and retrieval and machine learning directories" in the quality attributes table. The master document had no Node version in its tech table and no folder count. Python 3.11 was already correct in both.

**Decision:** Changed the report to match the code. `main.tex` now says Node.js 24 and lists four directories (frontend, backend, retrieval (rag), machine learning (ml)). The master document tech table now says "React / Next.js (TypeScript) on Node.js 24".

**Why:** The code and the report must agree (see `CLAUDE.md`, Source of truth).

**Follow-ups:** Remove the Node row from `docs/pending-report-changes.md`. Rebuild the report PDF and the master document docx before they are shared.

**Also settled on 2026-10-16:**

- Hosting: `main.tex` said "Railway" while the master document and `CLAUDE.md` said "Railway or Render". `main.tex` now says "Railway or Render" in the budget text, the tools list, and the deployment text. The choice between the two is still open until we deploy.
- Docker: the report and master document specify Docker Compose, and `CLAUDE.md` said Docker is deferred. These do not conflict, because deferred means not set up yet. Docker stays in the report. `CLAUDE.md` now says the report specifies it, we add it after the first services run, and the code must stay containerizable.
- Lint tool: the report names none and `CLAUDE.md` plans `ruff`. No change. If the team picks a different tool, change `CLAUDE.md`, and add the tool to the report if it should name one.

## 2026-10-15: Move from Node 20 to Node 24

**Context:** Node.js version used in the frontend, CI, and all development machines.

**What we tried:** Installed Node 24 on the frontend, CI, and all three machines to meet GSD Core's requirement of Node 24 or newer.

**What we found:** Node 20 reached end of life on 2026-04-30. GSD Core declares `engines.node >= 24.0.0` in its package.json. Not yet verified: a full `npm run build` of the Next.js app on Node 24 (there is no frontend code yet).

**Decision:** The report still says Node 20 and must be updated to Node 24 wherever it names the Node version.

**Why:** Node 20 is end-of-life and the planning tool requires Node 24 as a minimum.

**Follow-ups:** Update main.tex and the master document to name Node 24 in the stack and tools text, any technology table, and deployment diagram. No team member needs to act separately.

## 2026-10-15: Python 3.11 only, in every folder

**Context:** Python version used in backend, RAG, and ML folders, each with its own `.venv`.

**What we tried:** Installed Python 3.11.9 (the last 3.11 release with a Windows installer) on all three machines. Python 3.14 was removed from the lead machine.

**What we found:** Each folder uses Python 3.11 in its own virtual environment. One version avoids "works on my machine" differences between three laptops, and CI uses the same version.

**Decision:** The report must name Python 3.11 wherever it names a Python version (stack and tools text, any technology table, the ML and RAG environment description).

**Why:** A single version prevents environmental drift across the team.

**Follow-ups:** Update main.tex and the master document. No team member needs to act separately.

## 2026-10-15: GSD Core's `.planning/` folder stays out of git

**Context:** GSD Core (planning tool) keeps its plans, roadmap, and state in the `.planning/` folder.

**What we tried:** GSD Core's default is to commit those files on its own. Its config.json can hold API keys in plain text, and each person's `.planning/` copy changes constantly.

**What we found:** Committing `.planning/` would cause merge conflicts between three people and expose secrets. We added `.planning/` to `.gitignore` and turned off GSD's `commit_docs` setting.

**Decision:** Decisions the team needs to track go into `docs/DECISIONS.md` and the report by hand. No report change is needed.

**Why:** Avoids merge conflicts on personal state and reduces the risk of committing secrets.

**Follow-ups:** Revisit this decision if more than one person starts using GSD for shared planning across the team.

## 2026-10-17: Page snapshots in rag/corpus_profile/snapshots/

**Decision:** Commit the techdestination.com industry facilitation page snapshot (html and txt, saved 2026-10-04 by rag/corpus_profile/profile_corpus.py).

**Reason:** It is the evidence for the Chapter 3 corpus profiling (profile_report.md). It is a public page, about 2 MB.

**Note:** These are profiling copies, not corpus files. They are not in rag/corpus_manifest.md. Do not index them without a manifest row and a reason here.
