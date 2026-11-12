# backend

FastAPI gateway and services (auth, profile, startup intelligence, matching, compliance, admin), the LLM Gateway, database models and migrations, and Celery jobs.

## Local database and API

The repository-root `compose.yaml` provides a local PostgreSQL 17 server with pgvector. In the repository-root `.env`, set `CARNET_DB_PASSWORD` to a random 32-character alphanumeric value and set `DATABASE_URL` to the same value in the URL below. Keep `.env` private.

```env
CARNET_DB_PASSWORD=your-random-32-character-value
DATABASE_URL=postgresql+psycopg://founders_carnet:your-random-32-character-value@localhost:5432/founders_carnet
```

Start the database, Redis, API, worker, and the single Celery Beat scheduler from the repository root:

```powershell
docker compose up -d db redis api worker beat
Set-Location backend
.\.venv\Scripts\Activate.ps1
python -m alembic upgrade head
```

The database and Redis ports are bound to localhost only. Their data persists in the
`founders_carnet_pgdata` and `founders_carnet_redisdata` Docker volumes. The API is
available at `http://localhost:8000`. Profile embedding updates are queued for the
worker after a matching profile is saved. If Redis cannot accept the task, the API
regenerates that embedding synchronously. Beat queues the due-account purge every
15 minutes; run exactly one Beat scheduler for this schedule.

To export the current gateway contract after route changes:

```powershell
Set-Location ..
.\backend\.venv\Scripts\python.exe scripts\export_openapi.py
```

The generated schema is saved at `backend/openapi.json`.

The compliance endpoint is `POST /api/v1/compliance/questions` and requires a founder token. Backend settings load the repository-root `.env` even when commands run from `backend/`. Set `GEMINI_API_KEY` there. `GEMINI_REQUEST_TIMEOUT_MS` defaults to `60000` and accepts values from `10000` to `120000`. `EMBEDDING_MODEL_NAME` defaults to `sentence-transformers/paraphrase-multilingual-mpnet-base-v2`; override it only before indexing, because query and corpus embeddings must use the same model.

After migrations and environment configuration, index the corpus with:

```powershell
python -m app.services.corpus_indexer
```

The first run downloads the configured sentence-transformer weights to the local model cache. It does not write model weights into the repository.

## Backend slices 0 to 4

- Accounts: `POST /api/v1/auth/register/{role}`, `POST /api/v1/auth/linkedin/{role}`, `POST /api/v1/auth/login`, `POST /api/v1/auth/logout`, `GET /api/v1/users/me`, `POST /api/v1/users/me/consent/withdraw`, and `POST /api/v1/users/me/deletion-request`. Registration requires explicit consent; public roles are founder, talent, mentor, and investor, while admin is never selectable. Deletion disables the account immediately and schedules the step 9 purge after 30 days.
- Founder data: `PUT /api/v1/founders/me/profile` and `POST/GET /api/v1/founders/me/startups`; startup updates use `PATCH /api/v1/founders/me/startups/{id}`.
- Compliance: `POST /api/v1/compliance/questions`; sources are indexed by `python -m app.services.corpus_indexer`.
- Matching: mentors, investors, and talent save an opt-in profile at `PUT /api/v1/matching/me/profile`. Founders get up to three ranked candidates at `GET /api/v1/matching/startups/{startup_id}` and may send a request with `POST /api/v1/matching/{match_id}/request`. The recipient accepts with `/accept` or declines with `/decline`. The first call to the existing `/accept` endpoint still starts a request for older clients. Contact email appears only after the requester and recipient have both accepted.
- Readiness: `POST /api/v1/startups/{startup_id}/readiness` creates a versioned assessment; `GET` on the same path returns history.
- Pitch: `POST /api/v1/pitch/sessions` starts practice, `POST /api/v1/pitch/sessions/{id}/turns` continues it, `POST /api/v1/pitch/sessions/{id}/abandon` preserves an incomplete transcript, and `GET /api/v1/pitch/history` returns sessions and scores.
- Market research: configure `FIRECRAWL_API_KEY`, then founders can create a cited evidence report with `POST /api/v1/market-research` using `startup_id` and a research `question`. Source evidence and the separate interpretation are saved; `GET /api/v1/startups/{startup_id}/market-research` returns that founder's history. Apply migrations with `python -m alembic upgrade head` before using it.
- Resume optimizer: talent users send a PDF as the raw request body to `POST /api/v1/resumes/optimize?target_role=Backend%20Engineer` with `Content-Type: application/pdf` and `X-Resume-Processing-Consent: true`. The 5 MiB upload cap, PDF signature, page/text limits, and exact source lines are checked. PDFs are stored under `backend/.private/resumes` (or `RESUME_STORAGE_DIR`), never served by the API; `GET /api/v1/resumes/history` lists suggestions and `DELETE /api/v1/resumes/{id}` removes the record and file. Scanned PDFs and DOCX are not supported in this slice. Apply migrations before use.
- Job board: verified founders create listings with `POST /api/v1/startups/{startup_id}/jobs`, view startup listings at `GET /api/v1/startups/{startup_id}/jobs`, edit or close a listing with `PATCH /api/v1/jobs/{job_id}`, and delete it with `DELETE /api/v1/jobs/{job_id}`. Talent can browse open listings at `GET /api/v1/jobs`, save/unsave via `POST/DELETE /api/v1/jobs/{job_id}/save`, apply at `POST /api/v1/jobs/{job_id}/applications`, and see saved listings and application status at `GET /api/v1/jobs/saved` and `GET /api/v1/jobs/applications/me`. Founders review applicants at `GET /api/v1/startups/{startup_id}/job-applications` and update status with `PATCH /api/v1/job-applications/{application_id}`. Apply migrations before use.
- Profile verification: mentors, investors, and talent opt in with `POST /api/v1/verification/me` after creating a matching profile. Talent stores an optional GitHub link at `PUT /api/v1/talent/me/profile`. Verification evaluates five versioned signals, stores each input/outcome/reason in `verification_signals`, checks the submitted HTTPS portfolio through Firecrawl and the LLM Gateway, and exposes score, band, status, threshold version, and reason at `GET /api/v1/verification/me`. Auto-rejected users can submit one appeal at `POST /api/v1/verification/me/appeals`; authenticated users can report a profile at `POST /api/v1/verification/profiles/{user_id}/reports`. Configure `FIRECRAWL_API_KEY`, the Gemini key/model, and optional verification thresholds/weights. A reviewer must manually cross-check submitted SECP entity details; the default fake SECP checker keeps that signal pending until Step 5. Apply migrations before use.

Matching, readiness, and pitch use the configured embedding model or Gemini key when the relevant feature needs them. These providers are not called in the test suite. Use PostgreSQL with pgvector for the production retrieval path; SQLite is only used for local unit tests. Investors only receive verified startups with a saved readiness assessment. Startup verification is provided by the later verification feature, so unverified startups return no investor matches.
