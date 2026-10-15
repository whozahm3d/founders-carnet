# The Founder's Carnet: instructions for AI coding agents

This file is for any AI coding agent that does not read `CLAUDE.md` (Gemini in Antigravity, Codex, Cursor and similar).

**Read `CLAUDE.md` in this folder first and follow it.** It holds the project scope, architecture rules, data rules, git workflow and safety rules. This file does not replace it. If the two ever disagree, `CLAUDE.md` wins.

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

Nothing technical enforces these rules for agents other than Claude Code. They only hold if you follow them.

## Where things are

| Folder | Holds |
| --- | --- |
| `frontend/` | Next.js client |
| `backend/` | FastAPI gateway, services, LLM Gateway, database, Celery jobs |
| `rag/` | Compliance corpus, chunking, embedding, retrieval, answer validation |
| `ml/` | Dataset preprocessing and profiling, matching and re-ranker experiments |
| `docs/` | `DECISIONS.md` and notes |

Skills the team uses with Claude Code are in `.claude/skills/<name>/SKILL.md`. They are plain Markdown. Read one when its topic fits your task.
