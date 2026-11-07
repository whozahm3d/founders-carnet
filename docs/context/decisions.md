# Decisions settled so far

The full log with context and reasoning is `docs/DECISIONS.md`. This is only the short list. If the two disagree, `docs/DECISIONS.md` wins. Add a dated entry there whenever code and report are changed to agree.

| Decision | Detail |
| --- | --- |
| Python | 3.11 in every folder, each with its own `.venv` |
| Node | 24 (Node 20 reached end of life 2026-04-30). Report updated 2026-10-16 |
| Repo folders | Four: `frontend/`, `backend/`, `rag/`, `ml/`. Report updated 2026-10-16 |
| LLM | Gemini 2.5 or lower on the Google AI Studio free tier. Newer models unreliable under free-tier load. Model IDs in config. Fallback to an older model lives in the LLM Gateway |
| Hosting | Vercel for frontend. Railway or Render for backend and workers, undecided until we deploy. Nothing deployed yet |
| Docker | Docker Compose is in the report. Added after the first services run. Code must stay containerizable |
| Lint tool | Report names none. `ruff` planned for Python. Change `CLAUDE.md` if the team picks another |
| GSD Core | `.planning/` stays out of git. Decisions go to `docs/DECISIONS.md` by hand |
| Schema | 41 tables and 264 attributes in the report are a design baseline and may change. If they do, update the data dictionary and ER diagrams |
| Datasets | Record each one in `docs/datasets.md` before use. External datasets are for profiling, schema design and, for three FINAL datasets, the supporting classifiers. They never train the deployed re-ranker |
| Supporting classifiers (2026-10-19) | Three small classifiers trained offline in FYP-2: resume role (haider resumes, Bhawal as external check), startup outcome (Success/Fail, closed against not closed), follow-on funding (Investments). No user-facing probability. Supervisor approval pending. See `docs/datasets.md` and `docs/DECISIONS.md` |
| Matching-data wording (2026-10-19) | Write "we found no public labeled dataset for Pakistani founder-mentor or investor matching". Never write that none exists or that its absence is confirmed |
| Corpus versions | Income Tax Ordinance amended up to 30 June 2026. Seventh Schedule fees effective 20 April 2026. Never index a superseded version. Tax answers come from the Ordinance. PSEB pages are for registration procedure, documents, and fees only |

## Still open

- Lint tool beyond `ruff`: not chosen.
- Railway or Render: not chosen.
- Incubator partnership for labels and users: none yet (R-16).
- Legal review of the fee model: not done (R-15).
- Supervisor approval of the supporting classifiers: pending.
- Classifier column names, split sizes and the Investments label rule: set when the training scripts are written.
