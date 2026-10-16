# The Founder's Carnet: instructions for AI coding agents

This file is for any AI coding agent that does not read `CLAUDE.md` (Gemini in Antigravity, Codex, Cursor and similar).

**Read `CLAUDE.md` in this folder first and follow it.** It holds the project scope, architecture rules, data rules, git workflow and safety rules. This file does not replace it. If the two ever disagree, `CLAUDE.md` wins.

## Project context

Read `CLAUDE.md` first. For what the project is and how it is built, read the short summaries in `docs/context/` (start with `docs/context/README.md`) instead of the full report `main.tex`. If a summary disagrees with the report, the report wins.

## The rules that matter most

These are copied from `CLAUDE.md` so they apply even if you read only this file.

- Do not edit, overwrite, rename, move or delete an existing file unless the user asked for that change in this conversation. Creating a new file is fine.
- Never delete files or folders. Never run `git push`, `git reset`, `git clean`, `git restore`, `git rebase` or any forced git command.
- Do not run `git commit` unless the user asks.
- Do not change: `.claude/settings.json`, `.claude/hooks/`, `scripts/backup.py`, `scripts/backup_config.json`, any real `.env` file (`.env`, `.env.local`, and similar; `.env.example` is allowed), `.git/`, `_backup_mirror/`, `.claude/backups/`.
- Do not read real `.env` files (`.env.example` is fine). Never print, log or commit an API key.
- Before changing an existing file, back it up with `python scripts/backup.py snapshot <path>`, name the file, and say what will change. Restore with `python scripts/backup.py restore <path>`.
- Do not install packages, start a paid service, or begin a long or costly task without asking first.
- If you are unsure what the user wants, ask. Do not guess on anything that is hard to undo.
- Large, non-reproducible or private files (models, exports, backups) go to the shared Drive (link in SETUP.md), not git. Log them in docs/dataset-links.md.

Nothing technical enforces these rules for agents other than Claude Code. They only hold if you follow them.

## Where things are

| Folder | Holds |
| --- | --- |
| `frontend/` | Next.js client |
| `backend/` | FastAPI gateway, services, LLM Gateway, database, Celery jobs |
| `rag/` | Compliance corpus, chunking, embedding, retrieval, answer validation |
| `ml/` | Dataset preprocessing and profiling, matching and re-ranker experiments |
| `docs/` | `DECISIONS.md`, `context/` (report summaries) and notes |

Skills the team uses are in `.claude/skills/<name>/SKILL.md`. They are plain Markdown. Read one when its topic fits your task.

## Using a different tool than Claude Code (Codex, Antigravity, Cursor)

- Codex reads `AGENTS.md` and skills from `.agents/skills/`. Antigravity reads `AGENTS.md` or `GEMINI.md` and workspace skills from `.agents/skills/`. Neither reads `.claude/skills/`. Run `python scripts/sync_agent_skills.py` once after cloning or pulling. It copies `.claude/skills/*` to `.agents/skills/` and never deletes anything. `.agents/skills/` is not committed.
- If both `AGENTS.md` and `GEMINI.md` exist, Antigravity's order of precedence is not documented. Both files say the same thing: read `CLAUDE.md` first. Start a session with "Read AGENTS.md and CLAUDE.md first" if the agent seems to skip them.
- Before you start a feature, read `docs/context/coding-plan.md` for its minimum slice, cut line and the FR and NFR IDs to cite.
- Before you touch `rag/`, read `docs/context/corpus.md`. The 11 corpus files are committed in `rag/data/`.
- The rules in `.claude/settings.json` and `.claude/hooks/guard.py` block risky commands for Claude Code only. For every other tool the safety rules above are instructions, not blocks. Follow them anyway.
- Windows and PowerShell: use commands and paths that work there. Prefer Python scripts to shell scripts.
- Do not install any skill, plugin or MCP server that is not on the list in `THIRD_PARTY.md`.
- After finishing any piece of a feature, add a short entry to `docs/build-log.md`: date, who, feature and FR/NFR IDs, what was built, what was tested, what was cut. Do this in the same pull request as the code.
- If what you built differs from the report in any way (a name, a field, a flow, a number, a cut feature), do two things in the same pull request: add a dated entry to `docs/DECISIONS.md` with the reason, and add a row to `docs/pending-report-changes.md` saying what the report says now and what it should say. The reason is required. Nobody updates the report from a difference with no reason.
