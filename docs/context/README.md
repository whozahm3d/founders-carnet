# Project context

Short summaries of `main.tex` (the project report) for people and AI agents. Read these instead of the 2,300-line report. They are a digest, not a replacement.

| File | What it covers |
| --- | --- |
| `scope.md` | What we build, what we do not, and the legal limits |
| `ai-features.md` | Which features are a trained model (the re-ranker and three offline classifiers) and which are prompted LLM calls |
| `architecture.md` | Client, gateway, six services, database, queue, LLM Gateway, and the strategy choices |
| `requirements.md` | FR-1 to FR-31 and NFR-1 to NFR-23, with the semester each is built in |
| `build-order.md` | The delivery priority, what is dropped first, and the FYP-2 plan |
| `coding-plan.md` | Oct 19 to Nov 8 build plan: per feature the FR and NFR IDs, minimum slice, cut line, risk, owner (proposed) |
| `corpus.md` | The 11 compliance documents, versions, and indexing rules |
| `decisions.md` | Decisions already settled, with a pointer to `docs/DECISIONS.md` |

## Naming note

The master document and some older notes say "Phase 1" and "Phase 2". Phase 1 means FYP-1 plus FYP-2 (the whole FYP). The report and this repo use FYP-1 (this semester) and FYP-2 (next semester).

## Rules for these files

- The report is the source of truth. If a file here disagrees with `main.tex`, the report wins, and the file here is wrong. Fix it.
- When the report changes, update the matching file here in the same pull request.
- Requirement IDs are never renumbered. Cite them in code comments, tests, and pull requests (for example `# FR-8, NFR-13`).
- The approved data dictionary uses an older FR numbering (for example, it cites FR-3 for readiness and FR-4 for pitch). Take FR IDs only from `requirements.md`, never from the data dictionary.
- Last checked against the report: 2026-10-19 (supporting classifiers added to the summaries).
