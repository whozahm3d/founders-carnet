# backend

FastAPI gateway and services (auth, profile, startup intelligence, matching, compliance, admin), the LLM Gateway, database models and migrations, and Celery jobs.

## Local database and API

The repository-root `compose.yaml` provides a local PostgreSQL 17 server with pgvector. In the repository-root `.env`, set `CARNET_DB_PASSWORD` to a random 32-character alphanumeric value and set `DATABASE_URL` to the same value in the URL below. Keep `.env` private.

```env
CARNET_DB_PASSWORD=your-random-32-character-value
DATABASE_URL=postgresql+psycopg://founders_carnet:your-random-32-character-value@localhost:5432/founders_carnet
```

Start the database from the repository root, then run migrations and the API from `backend/`:

```powershell
docker compose up -d db
Set-Location backend
.\.venv\Scripts\Activate.ps1
python -m alembic upgrade head
python -m uvicorn app.main:app --reload
```

The database port is bound to localhost only. Its data persists in the `founders_carnet_pgdata` Docker volume.

The compliance endpoint is `POST /api/v1/compliance/questions` and requires a founder token. Backend settings load the repository-root `.env` even when commands run from `backend/`. Set `GEMINI_API_KEY` there. `GEMINI_REQUEST_TIMEOUT_MS` defaults to `60000` and accepts values from `10000` to `120000`. `EMBEDDING_MODEL_NAME` defaults to `sentence-transformers/paraphrase-multilingual-mpnet-base-v2`; override it only before indexing, because query and corpus embeddings must use the same model.

After migrations and environment configuration, index the corpus with:

```powershell
python -m app.services.corpus_indexer
```

The first run downloads the configured sentence-transformer weights to the local model cache. It does not write model weights into the repository.

## Backend slices 0 to 4

- Accounts: `POST /api/v1/auth/register`, `POST /api/v1/auth/login`, `POST /api/v1/auth/logout`, and `GET /api/v1/users/me`.
- Founder data: `PUT /api/v1/founders/me/profile` and `POST/GET /api/v1/founders/me/startups`; startup updates use `PATCH /api/v1/founders/me/startups/{id}`.
- Compliance: `POST /api/v1/compliance/questions`; sources are indexed by `python -m app.services.corpus_indexer`.
- Matching: mentors, investors, and talent save an opt-in profile at `PUT /api/v1/matching/me/profile`. Founders request candidates at `GET /api/v1/matching/startups/{startup_id}`; either side accepts with `POST /api/v1/matching/{match_id}/accept`. Contact email is returned only after both sides accept.
- Readiness: `POST /api/v1/startups/{startup_id}/readiness` creates a versioned assessment; `GET` on the same path returns history.
- Pitch: `POST /api/v1/pitch/sessions` starts practice, `POST /api/v1/pitch/sessions/{id}/turns` continues it, `POST /api/v1/pitch/sessions/{id}/abandon` preserves an incomplete transcript, and `GET /api/v1/pitch/history` returns sessions and scores.

Matching, readiness, and pitch use the configured embedding model or Gemini key when the relevant feature needs them. These providers are not called in the test suite. Use PostgreSQL with pgvector for the production retrieval path; SQLite is only used for local unit tests. Investors only receive verified startups with a saved readiness assessment. Startup verification is provided by the later verification feature, so unverified startups return no investor matches.
