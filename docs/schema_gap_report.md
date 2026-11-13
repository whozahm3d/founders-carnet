# FYP-1 schema gap report

Date: 2026-11-12

## Scope and method

This report compares the 37 FYP-1 tables shown in the existing ER diagrams with
the SQLAlchemy metadata and Alembic migrations currently in the backend. The
four grey FYP-2 tables are excluded: `subscription`, `event_listing`,
`resource_link`, and `placement_fee_event`.

The project data dictionary and the referenced Backend Implementation Guide are
not present in this checkout. Therefore, the FYP-1 baseline names come from the
ER diagrams in `docs/report/Figures/`, and the implementation comparison comes
from `backend/app/models.py`, `backend/app/feature_models.py`, route/service
models, and the nine migrations. Column differences below are against the
baseline table intent represented by those diagrams, not against an unavailable
formal data-dictionary column listing.

Status meanings:

- **exists**: the concept is implemented as a dedicated table, even if the
  implementation uses a plural or different physical table name.
- **merged**: the concept is implemented together with another baseline
  concept in one table.
- **partial**: only a subset is implemented, commonly as JSON or inline fields.
- **missing**: no corresponding persisted table or equivalent structure exists;
  these remain designed, not built.

## Summary

| Status | Count |
| --- | ---: |
| exists | 15 |
| merged | 4 |
| partial | 9 |
| missing | 9 |
| **Total FYP-1 tables** | **37** |

The backend currently materializes 21 physical tables. Several physical tables
cover multiple baseline concepts, so the physical-table count is lower than the
37-table FYP-1 design count.

## Accounts and profiles

| FYP-1 table | Status | Actual implementation | Differing columns or notes |
| --- | --- | --- | --- |
| `user_account` | exists | `users` | Physical name differs. `users` has `id`, `email`, `full_name`, `hashed_password`, `role`, `is_active`, `token_version`, `created_at`; no separate account-status history or consent relation. |
| `oauth_identity` | missing | — | Designed, not built. No provider, provider subject, or user foreign-key table. |
| `founder_profile` | exists | `founder_profiles` | Physical name differs. Implemented fields are `user_id`, `bio`, `location`, `consent_version`, `consented_at`, timestamps; startup and verification concepts remain separate. |
| `startup` | exists | `startups` | Physical name differs. Includes founder link, identity, sector/stage/location, business fields, traction, customer count, revenue, skills, funding range, verification flag, timestamps. |
| `talent_profile` | missing | — | Designed, not built. No dedicated talent profile table. |
| `mentor_profile` | missing | — | Designed, not built. Mentor data is not persisted as a dedicated profile. |
| `investor_profile` | missing | — | Designed, not built. Investor data is not persisted as a dedicated profile. |
| `mentor_expertise` | missing | — | Designed, not built. No expertise junction table. |
| `investor_thesis_sector` | missing | — | Designed, not built. No investor-sector junction table. |
| `consent_record` | missing | — | Designed, not built. Consent is currently represented by inline fields on selected profile and resume tables rather than a reusable record. |

## Verification and trust

| FYP-1 table | Status | Actual implementation | Differing columns or notes |
| --- | --- | --- | --- |
| `verification_case` | exists | `profile_verifications` | Physical name differs. Includes user, portfolio, SECP fields, status, score, band, signals, reason, threshold version, consent/trust-notice fields, lock, and timestamps. It is not named as a generic case table. |
| `verification_signal` | partial | `profile_verifications.signals` | Signals are stored in one JSON field; there is no one-row-per-signal table with signal name, input, outcome, or reason. |
| `review_decision` | exists | `verification_decisions` | Physical name differs. Includes verification, reviewer, decision, reason, score, band, signals, threshold version, and timestamp. |
| `appeal` | exists | `verification_appeals` | Physical name differs. Includes verification, reason, evidence, status, decision reason, reviewer, review time, and creation time. |
| `report_flag` | exists | `profile_reports` | Physical name differs. Includes reporter, target, reason, and creation time; no separate moderation-state history is present. |
| `audit_log` | missing | — | Designed, not built. No general immutable audit-event table. |

## Founder services

| FYP-1 table | Status | Actual implementation | Differing columns or notes |
| --- | --- | --- | --- |
| `readiness_assessment` | exists | `readiness_assessments` | Physical name differs. Includes startup, rubric version, result JSON, and creation time. |
| `readiness_dimension_score` | partial | `readiness_assessments.result` | Dimension scores are embedded in the assessment result JSON; no separate dimension rows or score columns. |
| `pitch_session` | exists | `pitch_sessions` | Physical name differs. Includes user, startup, persona, status, scores JSON, rubric version, and completion timestamps. |
| `pitch_feedback` | partial | `pitch_sessions.scores` and `pitch_turns` | Feedback is represented through session scores and conversation turns; no dedicated feedback table with author, score, and text fields. |
| `market_research_request` | merged | `market_research_reports` | Request question and processing status are stored in the report row; no separate request lifecycle table. |
| `market_research_output` | merged | `market_research_reports` | Interpretation and evidence are stored with the request; no separate output row or one-to-many result relation. |
| `resume_document` | merged | `resume_optimizations` | File storage key, hash, target role, and processing consent are stored with the optimization record; no reusable document table. |
| `resume_suggestion` | partial | `resume_optimizations.suggestions` | Suggestions are stored in JSON; no separate suggestion rows with ordering, category, or status. |

## Matching and jobs

| FYP-1 table | Status | Actual implementation | Differing columns or notes |
| --- | --- | --- | --- |
| `match_request` | merged | `match_records` | Requester, request status, and acceptance flags are stored with the match; no separate request table. |
| `match_result` | merged | `match_records` | Candidate, similarity, and score are stored with the request; no separate result table. |
| `match_factor` | partial | `match_records.factors` | Factors are stored in JSON; no one-row-per-factor name, weight, input, and contribution structure. |
| `embedding_record` | partial | `ecosystem_profiles.embedding`, `compliance_chunks.embedding` | Embeddings exist in feature-specific tables; there is no general embedding table with source type, source id, model version, hash, and timestamps. |
| `model_version` | missing | — | Designed, not built. Version strings exist inline on selected feature tables, but there is no reusable model registry table. |
| `job_listing` | exists | `job_listings` | Physical name differs. Includes startup, title, description, employment type, location, remote flag, status, and timestamps. |
| `application` | exists | `job_applications` | Physical name differs. Includes job, candidate, cover letter, status, and timestamps. |
| `saved_listing` | exists | `job_saves` | Physical name differs. Includes job, user, and creation time. |

## Compliance tables (regression-only scope)

These rows document the existing frozen compliance schema only. No compliance
code, migrations, tests, indexing, or retrieval behavior is changed by this
step.

| FYP-1 table | Status | Actual implementation | Differing columns or notes |
| --- | --- | --- | --- |
| `corpus_document` | exists | `compliance_documents` | Physical name differs. Includes filename/title, issuing body, type, source, dates, retrieval, hash, scope, and active flag. |
| `document_chunk` | exists | `compliance_chunks` | Physical name differs. Includes document, chunk id, page, section, text, embedding, and embedding model. |
| `compliance_query` | exists | `compliance_queries` | Physical name differs. Includes user, question, inline answer, outcome, abstention reason, passage count, latency, prompt version, and timestamp. |
| `compliance_answer` | partial | `compliance_queries.answer_text` | Answer is inline on the query row; there is no separate answer table. |
| `answer_citation` | exists | `compliance_citations` | Physical name differs. Includes query, chunk, and rank. |

## Consequences for later steps

- This step makes no schema changes.
- The nine missing tables are designed, not built, and should only be added in
  the feature step that requires them after an approved table design.
- JSON or inline representations should not be treated as equivalent to
  normalized tables when planning verification, matching, audit, or background
  job work.
- The missing Backend Implementation Guide prevents authoritative BT-01..BT-12
  mapping; the test ledger records that limitation instead of inventing IDs.
