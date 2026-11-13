# Contributing

The Founder's Carnet is a Final Year Project at FAST NUCES Lahore, built by Ali Ahmad, Shahzeb Imran and Taha Nawaz. Outside contributions are welcome, but the team reviews them on a best-effort basis. For setup, see [SETUP.md](SETUP.md).

## Before You Start

- For anything bigger than a small fix, open an issue first so we can agree on the approach.
- Read `docs/DECISIONS.md`. It records why key choices were made (the model, the data, the stack). If a change goes against an entry, add a new decision entry with `docs/decision-entry-template.md` instead of silently overriding it.
- Report security problems privately, as described in [SECURITY.md](SECURITY.md). Do not open a public issue.

## Project Layout

| Folder | Content |
| ------ | ------- |
| `backend/` | FastAPI app, SQLAlchemy models, Alembic migrations, tests |
| `frontend/` | Next.js and React web client |
| `rag/` | Compliance corpus ingestion, chunking and embeddings |
| `ml/` | Matching and re-ranker experiments |
| `docs/` | Decisions, build log, datasets, report |

## Workflow

1. Fork the repository and create a branch from `main`, named `feature/<short-name>` or `fix/<short-name>`.
2. Make one focused change per pull request.
3. Run the checks below and make sure they pass.
4. Open a pull request that says what changed, why, and how you tested it. Link the issue.

Commit messages are short and in the imperative mood, for example `Add token version check on logout`.

## Checks

```bash
# Backend
cd backend && python -m pytest

# Retrieval package
cd rag && python -m pytest

# Frontend
cd frontend && npm run lint
```

- Use Python 3.11. The `rag` package does not support other minor versions.
- Tests must not call live services. Use the existing fake gateway and fake embedding fixtures instead of the real Gemini API.
- A new endpoint, rule or algorithm needs a test. A bug fix needs a test that fails without the fix.
- A schema change needs an Alembic migration, never an edit of an old one.

## Rules That Are Not Negotiable

- All language model calls go through the single LLM gateway. Do not call a provider directly.
- The compliance assistant must cite its sources or refuse. Do not add a path that answers without a citation.
- Never commit secrets, `.env` files, API keys or real user data. Use made-up names and emails in tests and examples.
- Contact details stay hidden until both sides accept a match.
- Add only dependencies with a licence that fits the project, and list them in `THIRD_PARTY.md`.
- Follow the visual rules in `DESIGN.md`.

## Reporting Bugs

Open an issue with the steps to reproduce, the expected and the actual result, and your Python or Node version. Remove any personal data or keys from logs first.
