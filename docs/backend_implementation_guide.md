# The Founder's Carnet: Backend Implementation Guide

Nov 11, 2026 · @Ali

This guide covers the backend and database part of the implementation chapter (template Chapter 7, your Chapter 6) and gives prompts that build the FastAPI services from the architecture in main.tex.

## 0. Read first: the backend already exists

Updated 12 November 2026 after reading github.com/whozahm3d/founders-carnet and the approved data dictionary. I read the code, the migrations and the docs. I did not run the tests, the migrations or the API, so "built" means the code is there. Below, "build" in the prompts means "extend what is there".

| Area | What the repo has | Gap |
| --- | --- | --- |
| Stack | FastAPI 0.115, SQLAlchemy 2.0, Alembic 1.14, psycopg 3, pgvector, passlib with bcrypt, python-jose, google-genai, pydantic 2 | No Celery, Redis or ruff in requirements.txt. compose.yaml runs only the database, and as PostgreSQL 17 (the report says 16) |
| Auth | register (founder, talent, mentor or investor only), login, logout, current user, token version, sanitized validation errors | No consent record at registration, no LinkedIn, no consent withdrawal, no deletion request |
| Founder data | profile (with consent version) and startups: create, read, update |  |
| Compliance (FR-8) | indexer, chunking, embeddings, dense retrieval, answer, LLM grounding check, abstention with reasons, citations, query log | Gold set, evaluation, BM25 or hybrid, rule-based number check |
| LLM gateway | five-slot semaphore, retry, fallback model, logging | Disk cache, persisted call log, visible queue position |
| Matching (FR-7) | ecosystem profiles, five weighted factors blended with semantic similarity, stored factors, accept by both sides, contact email only after mutual acceptance | Confirm hard filters on sector, stage and geography; confirm pgvector use (the code imports a Python cosine function); investor visibility rule (FR-10); no re-rank score column |
| Readiness, pitch | endpoints, schemas, tables, four-area pitch rubric | Calibration (FYP-2) |
| Admin | one statistics endpoint | Review queue, appeals, decision log |
| Not started | verification scoring, jobs and applications, market research, resume optimizer, consent management, background jobs |  |
| Migrations | 0001 users, 0002 compliance, 0003 founder profiles and token version, 0004 matching, readiness and pitch |  |
| Tests | about 56 test functions in 12 files, plus 11 in rag/ | CI is written and has never run on GitHub |

**The schema is the biggest gap.** The approved data dictionary has 41 tables, 4 of them tagged FYP-2, which leaves 37. The code has 12 tables (users, founder\_profiles, startups, compliance\_documents, compliance\_chunks, compliance\_queries, compliance\_citations, ecosystem\_profiles, match\_records, readiness\_assessments, pitch\_sessions, pitch\_turns). They use integer ids, where the dictionary uses uuid, and several dictionary tables are merged or missing. The missing ones include verification\_case, verification\_signal, review\_decision, appeal, report\_flag, audit\_log, consent\_record, oauth\_identity, job\_listing, application, model\_version and the answer and match detail tables. CLAUDE.md allows the schema to differ and says to update the dictionary and ER diagrams to match. Decide how, in prompt B2.

**Four decisions for you**

1. **Schema route.** Regenerate the dictionary and ER figures from the real models and mark the rest as designed (fast), or migrate toward the dictionary (slow, and not realistic before D3).
2. **PostgreSQL version.** The report says 16 and compose uses 17. Change one and log it.
3. **Consent at registration.** FR-17 says consent comes before profile data. The register endpoint takes no consent. Today consent is captured with the profile writes. Either add it to registration (B3) or change the report's wording.
4. **Redis and Celery.** The report depends on them for slow jobs, and compose has neither. Decide whether they are in scope for D3 or documented as FYP-2.

**Rules the agents must follow here (from CLAUDE.md).** Plan first and wait for your yes. Never commit, push, delete or move files. Back up an existing file before editing it with `python scripts/backup.py snapshot <path>`. Ask before installing a package, adding a migration or a table, or changing an API contract. Python 3.11 in a `.venv`, pinned versions in requirements.txt, PowerShell commands. Add a docs/build-log.md entry per finished piece, and a DECISIONS entry plus a pending-report row when the code differs from the report.

## 1. What the report chapter must say about the backend

The backend goes in subsections 6.1.1 (backend and API), 6.1.2 (database) and 6.1.4 (LLM gateway) of your implementation chapter. template.tex asks for algorithmic and procedural detail, the platform and the APIs, not code.

| Report part | Write | Evidence |
| --- | --- | --- |
| Platform | Python 3.11, FastAPI, SQLAlchemy 2 with Alembic, PostgreSQL with pgvector (the report says 16 and compose runs 17), Redis and Celery (not set up yet), Docker Compose, GitHub Actions (written, never run), pytest. Nothing is deployed | requirements file, Dockerfile |
| Gateway and services | The API gateway checks login, role and request format. Behind it sit six services: startup intelligence, compliance retrieval, matching and ranking, authentication, profiles, administration. State which are built and which are stubs | Service list, router files |
| Endpoint table | Method, path, role allowed, requirement, one line | The generated OpenAPI file |
| Authentication | Email and password, LinkedIn OAuth, signed token, role-limited endpoints, logout (FR-22, FR-23) | Auth tests |
| Consent and mutual reveal | The state machine: request, accept by both sides, then contact details visible. Describe it as numbered steps and a state diagram | State figure |
| Verification | Five signals, weighted score, three bands (auto verified, auto rejected, human review), logged reason, one appeal (FR-14, FR-19, FR-21) | Score log sample |
| Database | The tables you actually created, grouped in the report's five modules, with a data dictionary. Mark the tables deferred to FYP-2 | Schema export |
| Background jobs | Ingestion of whitelisted pages, embedding regeneration when a profile changes | Job list |
| Backend tests | BT-01 to BT-12 in Section 5, and the AI tests in the playbook | pytest output |

The report says the schema has 41 tables in five modules, and calls those numbers planning figures. The repo has migrated 12 tables so far (migrations 0001 to 0004), with different names from the dictionary. Write the real count and names, and say which of the 41 are designed but not built.

## 2. What to give the coding agents from main.tex

Do not hand the agent the whole 150 KB report. Extract these into the repository first, so the agent works from your own decisions:

1. `/docs/architecture.md`: the system overview and the system architecture text from the High-Level and Low-Level Design chapter, and the five-module database design with the ER figures exported as images. This is the source for service names and the table list.
2. `/docs/requirements.md`: the functional requirements FR-1 to FR-31 and the non-functional requirements (NFR-1 and up), each with its role and semester tag. The agent must skip every item tagged FYP-2.
3. `/docs/constraints.md`: introduction only, no equity, no money handling, no compliance claims until a lawyer has reviewed them, public sources only for scraping, consent before any profile data, and no paid infrastructure.
4. `/docs/data_dictionary.md`: start empty. Prompt B2 fills it.
5. The AI prompts from the playbook, Section 18 (gateway, RAG, re-ranker). The backend prompts below do not repeat them.

One decision to make before B2: the report's schema has deferred FYP-2 tables drawn in gray. Write the list of those tables into `/docs/architecture.md`, so the agent does not build them. Building them now adds work you do not need and promises features you have not tested.

These files already exist in the repo under docs/context/: architecture.md, requirements.md, scope.md, build-order.md, coding-plan.md, corpus.md, ai-features.md and decisions.md. Point the agent there instead of creating copies in /docs. The only new file worth making is the list of FYP-2 tables. Take FR IDs from requirements.md, never from the data dictionary, which uses an older numbering.

## 3. Services, build order and requirements

The report deploys the services together but splits them by responsibility. Build them in this order, because each one needs the one before it.

| Order | Service or part | Responsibilities | Requirement |
| --- | --- | --- | --- |
| 1 | Repository, Docker, database, CI | Containers for API, Postgres with pgvector, Redis, worker | NFR-20 |
| 2 | Database and migrations | Five modules, data dictionary | Database chapter |
| 3 | Authentication | Register, login, LinkedIn OAuth, token, roles, logout, consent record, deletion request | FR-17, FR-22, FR-23, FR-27 |
| 4 | API gateway | Checks token, role and request format, routes to services | Architecture |
| 5 | Profiles and verification | Profiles per role, five-signal score, bands, status and reason, link consistency | FR-1, FR-12, FR-14, FR-15, FR-19, FR-20 |
| 6 | Administration | Review queue, appeals, decision log, blocked and reported profiles | FR-16, FR-21, FR-26 |
| 7 | LLM gateway | See the playbook, Prompt 1 | NFR-2, NFR-19 |
| 8 | Matching and ranking | Cosine retrieval with hard filters, feature score, mutual acceptance gate, mentor availability. Never calls a language model | FR-7, FR-10, FR-29 |
| 9 | Jobs and applications | Post, edit, close, delete listings, save, apply, track | FR-6, FR-24, FR-25 |
| 10 | Background jobs | Ingestion, embedding regeneration | Architecture |
| 11 | Startup intelligence, compliance retrieval | The AI endpoints from the playbook | FR-2, FR-3, FR-4, FR-8 |

FR-9 (multilingual), FR-11 (placement fee), FR-30 and FR-31 are tagged FYP-2 in main.tex. Leave them out of D3. The placement-fee requirement also sits uneasily with the introduction-only rule, so ask your supervisor how it is phrased before you build anything near it.

Status against this order: rows 1 and 2 are partly done (database and four migrations, no Redis, no API container). Row 3 is mostly done. Row 4 is one FastAPI app with a role dependency, not a separate gateway process. Rows 5, 6, 9 and 10 are not started. Rows 7, 8 and 11 exist and need extending. Section 0 has the detail.

## 4. Prompts B1 to B8, copy-paste

Merge the shared context into your existing AGENTS.md and CLAUDE.md. Run the prompts in order, one at a time. The AI prompts (gateway, RAG, re-ranker) are in the playbook, Section 18. Run the playbook's Prompt 1 (extend the gateway) before B6 and B8, because they use its queue and call log.

### Shared backend context

```text
Project: The Founder's Carnet, an introduction-only startup ecosystem platform for Pakistan. Roles: founder, talent, mentor, investor, admin.
Backend: /backend. Python 3.11, FastAPI, pydantic v2, SQLAlchemy 2 with Alembic, PostgreSQL with pgvector, pytest. Routes are in app/routes, services in app/services, models in app/models.py and app/feature_models.py, schemas in app/schemas.py and app/feature_schemas.py, endpoints under /api/v1.
Read CLAUDE.md first. Its safety rules win over this prompt: plan first and wait for my yes; never commit, push, delete or move files; back up an existing file before editing it (python scripts/backup.py snapshot <path>); ask before installing a package, creating a migration or table, or changing an API contract; PowerShell commands; a .venv per folder; pinned versions in requirements.txt.
Requirements and design: docs/context/ (requirements.md, architecture.md, scope.md, coding-plan.md, ai-features.md, decisions.md). Build only items not tagged FYP-2. Cite FR and NFR IDs from requirements.md in code comments and tests, never from the data dictionary, whose numbering is older.
Existing code is extended, never replaced. Read the relevant files and their tests before planning.
Rules:
- Introduction only. No equity, no money handling, no compliance claims, no funding probability.
- Contact details are never returned by any endpoint until both sides have accepted.
- Personal data only from self-registration with recorded consent. Public organisation pages only for scraping, never personal profiles (PECA 2016).
- Every endpoint has pydantic request and response models and a role check. No endpoint reads a role from the request body. Never echo passwords or secrets in errors or logs.
- Every decision about a person (verification band, match) stores its inputs and reason (NFR-15).
- Matching never calls a language model. Every language model call goes through the LLM gateway.
- Schema changes go through Alembic only, and only after I approve the table design. When the schema differs from the data dictionary or the report, update docs/data_dictionary or add a DECISIONS entry and a pending-report row.
- Write tests first for anything with a rule. Run pytest from backend/ and report the real output. Say what was not tested.
- Add a docs/build-log.md entry per finished piece.
```

### B1: containers, Redis, Celery and the CI check

```text
The FastAPI app, settings, Alembic and the tests already exist in /backend, and compose.yaml runs only the database (pgvector, PostgreSQL 17). Do not recreate any of that. Read compose.yaml, backend/README.md, .env.example and .github/workflows/ci.yml, then show a plan and wait for my yes.
Then, as separate small changes: (a) add Redis and a Celery worker to compose.yaml, and an API container, keeping the database as it is (tell me before editing compose.yaml and before any install); (b) a script that exports the OpenAPI schema to backend/openapi.json; (c) tell me what is needed to make the CI workflow run for the first time on a test branch, since it has never run on GitHub. Do not edit the workflow without asking. Note that the report says PostgreSQL 16 and compose uses 17: do not change it, but list both options in docs/DECISIONS.md as a draft for me. Add a build-log entry. Do not commit.
```

### B2: database gap report and schema decision

```text
Do not create or change any table in this task. Read backend/app/models.py, backend/app/feature_models.py, the four Alembic migrations, and the approved data dictionary I will put in docs/data_dictionary.md. The dictionary has 41 tables in five modules; subscription, event_listing, resource_link and placement_fee_event are tagged FYP-2. The code has 12 tables with different names and integer ids.
Write docs/schema_gap_report.md: one row for each of the 37 FYP-1 dictionary tables with its status (exists under this name, merged into this table, partly, or missing), and for each existing table the dictionary table it maps to. Then list every column that differs in name, type or meaning, and every feature that stores data the dictionary has no table for.
End with two options, each with cost: (A) regenerate the data dictionary and the ER diagrams from the real models, and mark the unbuilt tables as designed; (B) add the missing tables in new migrations. Recommend one and wait for my choice. Do not commit.
```

### B3: consent, deletion and LinkedIn on top of the existing auth

```text
Authentication already exists: register (founder, talent, mentor or investor only), login with a signed token, logout through a token version, current user, role dependencies and sanitized validation errors, with tests in backend/tests/test_auth.py and test_auth_sessions.py. Do not change the token approach without asking. Read those files, then show a plan and wait for my yes.
Add, one at a time: (1) FR-17: a consent record stored when the user accepts the notice, and registration refused without it. Show me the table design first and wait before creating a migration. (2) FR-27: consent withdrawal for non-essential processing, and an account deletion request that disables the account at once and records the request (the 30-day purge job is not built, so state that). (3) LinkedIn sign-in behind an interface with a fake provider for tests (FR-22). The coding plan allows cutting this if the OAuth app is not approved, so say what you can and cannot finish without real credentials.
Tests: registration without consent is refused, withdrawal is recorded, a deletion request disables the account, wrong role gets 403, missing token gets 401. Do not commit.
```

### B4: profiles and automatic verification

```text
Founder profiles and startups exist (backend/app/routes/founders.py). Mentor and investor details live in ecosystem profiles. Talent has no profile table. Read the models and the dictionary's profile and verification tables, then show a plan and wait for my yes.
Implement, with table designs shown to me before any migration: (1) the talent profile (FR-13 GitHub link optional), (2) automatic verification scoring (FR-12, FR-14, FR-15, FR-19, FR-20). The score is a weighted sum of five signals: LinkedIn OAuth, SECP cross-check, completeness, GitHub activity (talent only) and portfolio link consistency. Four are rules we write; only the link check is a prompted call, through the gateway. Weights and thresholds live in a versioned config file. A high score verifies at once, a low score rejects with a logged reason, a middle score goes to the human review queue. Store the score, every signal value, the band, the threshold version and the reason. Expose a status endpoint returning status and reason (FR-15). Write the SECP check and the link check behind interfaces with fakes. The coding plan says how the SECP check is done is not settled: ask me and record my answer in DECISIONS.
Tests: injected complete, incomplete and inconsistent profiles land in the expected bands, and the log row holds every signal. Do not commit.
```

### B5: administration and appeals

```text
Implement the administration service: a review queue of profiles in the middle band and of appeals with their score and signals (FR-26), approve or reject with a required reason, a decision log tied to the reviewer, blocked and reported profiles returning to review without being scored again (FR-16), and the appeal rule: an auto-rejected user can appeal once with text evidence, a reviewer decides, and the decision is final and visible to the user (FR-21). Tests: a second appeal is rejected, a reviewer cannot decide without a reason, every decision is logged.
```

### B6: review and complete the matching service

```text
Matching exists: backend/app/services/matching.py and the matching routes in backend/app/routes/intelligence.py. Weights (sector 0.25, stage 0.20, skills 0.25, availability 0.15, ticket 0.15, blended 0.5 with semantic similarity) are logged in docs/DECISIONS.md on 2026-10-17. Do not change them. It makes no model call, and must not.
Read the code and tests, then write a short review against FR-7, FR-10, FR-29, NFR-3, NFR-6 and NFR-15 and wait for my yes. Check and report: (a) are hard filters on sector, stage and geography applied before ranking, as the report says; (b) is candidate retrieval done with pgvector, or with a Python cosine function; (c) do investors see only verified startups that finished a readiness assessment (FR-10); (d) are closed mentors left out (FR-29); (e) is contact information returned only after mutual acceptance, including on the list endpoints; (f) the match table has no re-rank score column.
Fix only what I approve. Add tests for each rule above, including a test that no response contains contact details before both sides accept. Any schema change needs my approval first. Do not commit.
```

### B7: jobs and applications

```text
Implement the jobs module (FR-6, FR-24, FR-25): verified founders create, edit, close and delete listings and see applicants; talent browse listings, save, apply, and track status; applicants' details are visible to the listing's founder only. Tests: an unverified founder cannot post, a founder cannot see another founder's applicants, deleting a listing handles its applications consistently.
```

### B8: background jobs and the full test run

```text
Celery and Redis are not set up yet (REDIS_URL exists only in .env.example). After B1 adds them, move two jobs into Celery: corpus indexing (now run by hand with python -m app.services.corpus_indexer) and embedding regeneration when a profile changes or the embedding model changes (store a hash of the source text so unchanged rows are skipped). The 11 compliance documents are committed in rag/data with hashes in rag/corpus_manifest.md, so no live crawling is needed for compliance. Firecrawl is only for market research (FR-4) and any directory seeding from public organisation pages, never personal profiles. Make each job safe to run twice, and log its outcome. Ask before installing. Then run the whole test suite with coverage from backend/ and rag/, and write backend/TESTS.md listing each test, the requirement it covers and its result. Report the real numbers. Do not commit.
```

## 5. Backend test cases and metrics for the report

Use the template's test case table for each. The status stays Not executed until you run the test. Check every requirement ID against main.tex before you write it down.

| ID | Test | Requirement |
| --- | --- | --- |
| BT-01 | A request without a token returns 401, and a token of the wrong role returns 403 | FR-23 |
| BT-02 | Registration without consent is rejected | FR-17 |
| BT-03 | Admin cannot be chosen as a role at registration | FR-22 |
| BT-04 | A deletion request is recorded and scheduled | FR-27 |
| BT-05 | Injected complete, incomplete and inconsistent profiles land in the expected verification bands, and the log stores every signal | FR-14, FR-19 |
| BT-06 | A user can appeal an automatic rejection once, and a second appeal is refused | FR-21 |
| BT-07 | A reviewer decision without a reason is refused, and every decision is logged | FR-26 |
| BT-08 | Matching results never include a wrong sector, stage or geography, or a closed mentor | FR-7, FR-29 |
| BT-09 | No endpoint returns contact details until both sides accepted | FR-7 |
| BT-10 | Every forbidden match state transition is refused | FR-7 |
| BT-11 | An unverified founder cannot post a listing, and a founder cannot see another founder's applicants | FR-24 |
| BT-12 | Migrating the empty database up and down works, and the table count matches the data dictionary | Database chapter |

The AI tests (gateway cache, queue of five, abstention, citations, split leakage) are in the playbook, Section 19.3. Together with these they make one table in the chapter.

Metrics for the template table: number of test cases, passed, failed, defect density (failed times 100 divided by executed), and a traceability matrix with one row per requirement above. Add the coverage percentage from B8 as a line of text, and do not present it as proof of quality. Test case effectiveness needs a log of defects found, so leave it for FYP-II if you have not kept one.

Existing tests, which I did not run: test\_auth, test\_auth\_sessions, test\_founder\_profiles, test\_intelligence (matching, readiness, pitch), test\_compliance\_api, test\_compliance\_assistant, test\_compliance\_retrieval, test\_compliance\_models, test\_llm\_gateway, test\_migrations, test\_config and test\_corpus\_indexer. Map each BT line above to an existing test before you write a new one, and add only what is missing. BT-03 may already pass, since registration allows only four roles. BT-02 cannot pass until consent is added to registration. BT-05, BT-06, BT-07 and BT-11 test features that do not exist yet.

## 6. Rules: privacy, consent, security

The report makes promises on these points. A panel can test each one, so the code must keep them.

- **Introduction only.** No endpoint handles money, equity or a legal decision. FR-11 (placement fee) is FYP-2 and conflicts in spirit with this rule. Do not build it for D3.
- **Consent first.** No profile data is stored before the consent record exists. Consent withdrawal and deletion requests must work, since FR-27 is tagged FYP-1.
- **Public sources only.** The scraper reads a whitelist of public organisation pages. It never reads personal profiles. Keep the whitelist file in the repository and quote it in the report. The report's PECA 2016 sourcing rule applies.
- **Explainable decisions.** Verification and matching store inputs and reasons, which is also what NFR-15 requires.
- **Secrets.** Keys for Gemini, LinkedIn and the database live in environment variables. Rotate any key that was ever pasted into a chat or a prompt.
- **No real personal data in tests or prompts.** Use fakes and synthetic users.
- **Free tier limits.** Gemini 2.5 or lower, five concurrent requests, queue the rest. Do not add a paid service. If you move to another provider, only the gateway configuration changes (NFR-19).
- **Do not claim compliance.** The report waits for a lawyer's review of the introduction-only boundary before it makes any compliance claim.

Security checks to run before you describe the backend as secure: no endpoint without a role check, passwords hashed, input validated, rate limit on login and on the AI endpoints, and no stack traces in responses. Report what you checked, and say what you did not check, such as a penetration test.

Repo-specific rules to keep: the key scan in CI must stay green, so no key in any file; model ids stay in configuration, Gemini 2.5 or below, with the fallback inside the gateway; age and gender are never matching features; do not store names, birth dates or contact fields from external datasets; anything from ml/ that ships goes through the backend as a service, never as a notebook.
