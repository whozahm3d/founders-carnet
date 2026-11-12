# Architecture

Source: report Chapter 5 (High-Level and Low-Level Design). Figures 13 to 23 in the report.

## Shape

```
Next.js client
   |  (only talks to the gateway)
FastAPI API gateway  -- JWT check, role check, request validation, routing
   |
   +-- Startup Intelligence Service  (readiness, pitch practice, market research)
   +-- RAG Compliance Service        (cited answers from retrieved passages)
   +-- Matching and Ranking Service  (candidate ranking, FYP-2 re-ranker)
   +-- Authentication Service        (registration, login)
   +-- Profile Service               (user profiles)
   +-- Admin and Moderation Service  (human review of escalated profiles)

All services share: PostgreSQL 16 with pgvector (records and embeddings)
Background jobs:     Redis + Celery
Model calls:         one internal LLM Gateway -> Gemini
Collection:          Firecrawl (regulatory and market sources), Playwright (public org pages)
```

## Hard rules

- The client never calls an LLM provider, matching, or RAG directly.
- The LLM Gateway is the only path to Gemini. It holds prompt templates, enforces the concurrency limit (about five at once), and logs prompts sent, evidence, and versions.
- Matching never calls a language model.
- JWT is issued at login and checked by gateway middleware on every request. Role claims limit endpoints and investor visibility.
- Contact details appear only after both sides accept. No API response may carry them before (NFR-6).
- The API keeps no session state (NFR-21).
- Secrets and configuration come from environment variables (NFR-8). Provider, model tier, concurrency limits, and verification thresholds are configuration, not code.
- Prompts, rubrics, and corpus documents are versioned. A readiness assessment stores the rubric version. Each corpus document stores source, publication date, effective date, and a file hash.

## Subsystems

**Matching.** A background job embeds a profile when it is saved. Stage 1: top-K by pgvector cosine similarity with hard filters (sector, stage, geography). Stage 2: rank by five factors and weights (FYP-1) or the trained re-ranker (FYP-2). Each result stores its factors. Mutual acceptance gate last.

**Compliance retrieval.** Embed the question, retrieve top passages. If nothing supports an answer, decline before generating. Otherwise generate with citations (issuing body, section, effective date) and run a validation step that checks nothing goes beyond the passages. If validation fails, or the question asks for case-specific advice, abstain. Every query is logged with outcome, passage count, latency, and abstention reason. English only in FYP-1.

**Profile verification.** Five signals: LinkedIn OAuth, SECP cross-check, profile completeness, GitHub activity (talent), portfolio link consistency. High score verifies, low score rejects with a reason, middle goes to a human reviewer. An auto-rejected user can appeal once. A reviewer's decision is final. Every decision logs reason, signals, threshold version, and consent record.

**Background pipeline.** Ingestion of whitelisted SECP, FBR, and PSEB pages (chunk, embed, index). Directory seeding. Signal collection and link check after a profile is submitted. Embedding regeneration on profile edit or model change. FYP-2 adds a relevance-label tool and a batch re-ranker training job. The three supporting classifiers (resume role, startup outcome, follow-on funding) are trained offline from scripts in `ml/` and are not a service. Anything from them that ships goes through `backend/`.

## Strategy choices already made

- One LLM Gateway, not an SDK per service (changing provider is a config change).
- pgvector in PostgreSQL, not a dedicated vector database (one store, one query for filters and vectors).
- Two-stage matching (cheap first stage, costlier second on a short list).
- Grounded generation with abstention, no fine-tuning on the corpus.
- Services split by responsibility in code, deployed together as a few containers. Full microservices rejected for a team of three and free-tier limits.
- Slow work in a queue, never in the request path.
- Visible degradation: queue at the concurrency limit and show "queued"; keep the previous readiness assessment if a model call fails; if a verification signal is missing, score with the rest and send more profiles to a reviewer.

## Repo and tooling

Monorepo, four folders: `frontend/`, `backend/`, `rag/`, `ml/`. Python 3.11, Node 24, PostgreSQL 16. Schema changes are versioned migrations that can rebuild an empty database (NFR-22). Linting and tests on every pull request (NFR-23). Docker Compose for local runs is in the report and added after the first services run. Frontend on Vercel, backend and workers on Railway or Render.

The 41-table, 264-attribute schema and the 23-class domain model are design baselines. If the real schema differs, update the data dictionary and ER diagrams.
