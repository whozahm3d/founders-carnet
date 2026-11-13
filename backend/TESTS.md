# Backend test ledger

The Backend Implementation Guide referenced by the project instructions is not
present at `docs/context/backend-implementation-guide.md`, so BT-01..BT-12 cannot
be mapped without inventing test IDs. The rows below are the step 1 tests; the
BT mapping will be completed when that guide is restored.

| Test ID | file::function | requirement | feature step | result | date |
| --- | --- | --- | --- | --- | --- |
| step1-infra-01 | tests/test_infrastructure.py::test_celery_uses_configured_redis_url | NFR-2, NFR-21 | 1 | PASS | 2026-11-12 |
| step1-infra-02 | tests/test_infrastructure.py::test_celery_app_has_json_safe_worker_defaults | NFR-2, NFR-19 | 1 | PASS | 2026-11-12 |
| step1-infra-03 | tests/test_infrastructure.py::test_compose_declares_database_redis_api_worker_and_beat_services | NFR-2, NFR-21 | 1, 9 | PASS | 2026-11-13 |
| step1-infra-04 | tests/test_infrastructure.py::test_openapi_export_contains_existing_api_routes | NFR-23 | 1 | PASS | 2026-11-12 |
| docker-compose-config | docker compose config --quiet | NFR-21 | 1 | NOT RUN: Docker is not installed or available on PATH | 2026-11-12 |
| local-ruff | python -m ruff check app tests scripts | NFR-23 | 1 | NOT RUN: Ruff is not installed in the local backend .venv; CI installs it | 2026-11-12 |
| step2-schema-gap-suite | pytest -v --tb=short | Schema inventory regression check; no runtime behavior changed | 2 | PASS | 2026-11-12 |
| step3-auth-01 | tests/test_auth_consent_oauth.py::test_registration_requires_explicit_consent_and_does_not_create_user | FR-17, NFR-9 | 3 | PASS | 2026-11-12 |
| step3-auth-02 | tests/test_auth_consent_oauth.py::test_registration_role_is_in_path_and_admin_cannot_be_selected | FR-22, NFR-5 | 3 | PASS | 2026-11-12 |
| step3-auth-03 | tests/test_auth_consent_oauth.py::test_consent_can_be_withdrawn_without_exposing_password_or_token | FR-27, NFR-4, NFR-9 | 3 | PASS | 2026-11-12 |
| step3-auth-04 | tests/test_auth_consent_oauth.py::test_deletion_request_disables_account_and_invalidates_token | FR-27, NFR-5, NFR-11 | 3 | PASS | 2026-11-12 |
| step3-auth-05 | tests/test_auth_consent_oauth.py::test_fake_linkedin_provider_creates_identity_and_reuses_it | FR-22, NFR-4 | 3 | PASS | 2026-11-12 |
| step3-migration-01 | tests/test_migrations.py::test_migrations_build_user_schema_from_empty_database | NFR-22, FR-17, FR-22, FR-27 | 3 | PASS | 2026-11-12 |
| step4-profile-01 | tests/test_profiles_verification_step4.py::test_talent_profile_stores_optional_github_link_and_requires_talent_role | FR-13, NFR-9 | 4 | PASS | 2026-11-12 |
| step4-profile-02 | tests/test_profiles_verification_step4.py::test_talent_verification_stores_all_five_signals_and_only_calls_gateway_for_link | FR-12, FR-19, FR-20, NFR-15, NFR-19 | 4 | PASS | 2026-11-12 |
| step4-profile-03 | tests/test_profiles_verification_step4.py::test_verified_secp_and_complete_signals_can_auto_verify | FR-14, FR-15 | 4 | PASS | 2026-11-12 |
| step4-migration-01 | tests/test_migrations.py::test_migrations_build_user_schema_from_empty_database | FR-13, FR-19, NFR-22 | 4 | PASS | 2026-11-12 |
| BT-06 | tests/test_admin_verification.py::test_admin_approves_appeal_records_reviewer_and_makes_status_visible | FR-21, FR-26 | 5 | PASS | 2026-11-12 |
| BT-07 | tests/test_admin_verification.py::test_admin_requires_nonblank_reason_and_rejects_forbidden_second_transition | FR-16, FR-26 | 5 | PASS | 2026-11-12 |
| test_admin_queue_is_admin_only_and_contains_signals_without_contact_details | tests/test_admin_verification.py::test_admin_queue_is_admin_only_and_contains_signals_without_contact_details | FR-26 | 5 | PASS | 2026-11-12 |
| test_admin_rejection_is_final_and_records_reviewer_reason | tests/test_admin_verification.py::test_admin_rejection_is_final_and_records_reviewer_reason | FR-15, FR-26 | 5 | PASS | 2026-11-12 |
| test_denied_appeal_is_final_and_cannot_be_appealed_again | tests/test_admin_verification.py::test_denied_appeal_is_final_and_cannot_be_appealed_again | FR-21, FR-26 | 5 | PASS | 2026-11-12 |
| test_reported_profile_returns_to_queue_with_score_locked | tests/test_admin_verification.py::test_reported_profile_returns_to_queue_with_score_locked | FR-16, FR-26 | 5 | PASS | 2026-11-12 |
| step7-match-01 | tests/test_intelligence.py::test_matching_explanation_and_contact_require_both_acceptances | FR-7, NFR-6 | 7 | PASS | 2026-11-13 |
| step7-match-02 | tests/test_intelligence.py::test_closed_mentor_is_not_recommended | FR-29 | 7 | PASS | 2026-11-13 |
| step7-match-03 | tests/test_intelligence.py::test_closed_mentor_does_not_consume_founder_match_page_limit | FR-29, NFR-3 | 7 | PASS | 2026-11-13 |
| step7-match-04 | tests/test_intelligence.py::test_inactive_candidate_is_not_returned_in_founder_match_list | FR-7, NFR-5 | 7 | PASS | 2026-11-13 |
| step7-match-05 | tests/test_intelligence.py::test_postgres_candidate_filters_are_applied_before_similarity_limit | FR-7, FR-10, FR-29, NFR-3 | 7 | PASS | 2026-11-13 |
| step7-match-06 | tests/test_intelligence.py::test_investors_only_see_verified_startups_with_readiness | FR-10 | 7 | PASS | 2026-11-13 |
| step9-profile-embedding | tests/test_background_tasks.py::test_profile_embedding_task_regenerates_with_current_model | FR-7, NFR-20 | 9 | PASS | 2026-11-13 |
| step9-deletion-purge | tests/test_background_tasks.py::test_account_purge_removes_due_user_data_and_private_resume_and_cache | FR-27, NFR-10, NFR-11 | 9 | PASS | 2026-11-13 |
| step9-task-registration | tests/test_background_tasks.py::test_celery_tasks_are_registered_without_running_a_worker | NFR-2, NFR-21 | 9 | PASS | 2026-11-13 |
| step9-purge-schedule | tests/test_infrastructure.py::test_celery_schedules_due_account_purges | NFR-10, NFR-11, NFR-21 | 9 | PASS | 2026-11-13 |
| step8-jobs-01 | tests/test_jobs.py::test_verified_founder_and_talent_complete_listing_application_flow | FR-6, FR-24, FR-25 | 8 | PASS | 2026-11-13 |
| step8-jobs-02 | tests/test_jobs.py::test_unverified_or_non_owner_founder_cannot_manage_job_listings | FR-24, NFR-5 | 8 | PASS | 2026-11-13 |
| step8-jobs-03 | tests/test_jobs.py::test_open_listing_cannot_be_saved_after_startup_loses_verification | FR-6, FR-25 | 8 | PASS | 2026-11-13 |
| step8-jobs-04 | tests/test_jobs.py::test_job_listing_rejects_whitespace_only_required_fields_on_create_and_patch | FR-24 | 8 | PASS | 2026-11-13 |
| step6-gateway-01 | tests/test_llm_gateway.py::test_structured_generation_caches_by_user_input_and_prompt_version | NFR-8, NFR-11, NFR-19 | 6 | PASS | 2026-11-12 |
| step6-gateway-02 | tests/test_llm_gateway.py::test_structured_cache_expiry_forces_provider_call | NFR-8, NFR-19 | 6 | PASS | 2026-11-12 |
| step6-gateway-03 | tests/test_llm_gateway.py::test_structured_cache_clear_removes_only_the_requested_scope | NFR-11 | 6 | PASS | 2026-11-12 |
| step6-gateway-04 | tests/test_llm_gateway.py::test_compliance_generation_does_not_use_structured_response_cache | FR-8, NFR-19 | 6 | PASS | 2026-11-12 |
| step6-gateway-05 | tests/test_llm_gateway.py::test_generation_queue_records_waiting_position | NFR-2, NFR-19 | 6 | PASS | 2026-11-12 |
| step6-gateway-06 | tests/test_llm_gateway.py::test_gateway_call_metadata_is_persisted_without_prompt_content | NFR-11, NFR-19 | 6 | PASS | 2026-11-12 |
| step6-gateway-07 | tests/test_auth_consent_oauth.py::test_deletion_request_disables_account_invalidates_token_and_clears_llm_cache | NFR-11 | 6 | PASS | 2026-11-12 |

Compliance and RAG tests are regression-only and out of scope. They are included
in the full-suite totals below but are not part of BT-01..BT-12 mapping.

## History

| Run | command | passed | failed | skipped | warnings | coverage |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| 2026-11-12 step1 focused | `pytest -q tests/test_infrastructure.py --tb=short` | 4 | 0 | 0 | 0 | Not measured |
| 2026-11-12 step1 backend suite | `pytest -v --tb=short --junitxml=docs/test-results/step1-containers-20261112-2200.xml` | 94 | 0 | 0 | 1 | Not measured |
| 2026-11-12 step2 backend suite | `pytest -v --tb=short --junitxml=docs/test-results/step2-schema-gap-20261112-2215.xml` | 94 | 0 | 0 | 1 | Not measured |
| 2026-11-12 step3 backend suite | `pytest -v --tb=short --junitxml=docs/test-results/step3-auth-20261112-2226.xml` | 99 | 0 | 0 | 1 | Not measured |
| 2026-11-12 step4 backend suite | `pytest -v --tb=short --junitxml=docs/test-results/step4-profiles-verification-20261112-2308.xml` | 102 | 0 | 0 | 1 | Not measured |
| 2026-11-12 step5 focused | `pytest -q tests/test_admin_verification.py --tb=short` | 6 | 0 | 0 | 1 | Not measured |
| 2026-11-12 step5 backend suite | `pytest -v --tb=short --junitxml=docs/test-results/step5-admin-20261112-2320.xml` | 108 | 0 | 0 | 1 | Not measured |
| 2026-11-12 step5 RAG regression only | `pytest rag/tests -v --tb=short --junitxml=docs/test-results/step5-compliance-rag-regression-20261112-2316.xml` | 11 | 0 | 0 | 0 | Not measured |
| 2026-11-12 step5 compliance regression only | `pytest tests/test_compliance_api.py tests/test_compliance_assistant.py tests/test_compliance_models.py tests/test_compliance_retrieval.py tests/test_corpus_indexer.py -v --tb=short --junitxml=docs/test-results/step5-compliance-regression-20261112-2320.xml` | 22 | 0 | 0 | 1 | Not measured |
| 2026-11-12 step6 focused gateway/migration/deletion | `pytest tests/test_llm_gateway.py tests/test_migrations.py tests/test_auth_consent_oauth.py -q --tb=short` | 24 | 0 | 0 | 1 | Not measured |
| 2026-11-12 step6 backend suite | `pytest -v --tb=short --junitxml=docs/test-results/step6-llm-gateway-20261112-2345.xml` | 114 | 0 | 0 | 1 | Not measured |
| 2026-11-12 step6 RAG regression only | `pytest rag/tests -v --tb=short --junitxml=docs/test-results/step6-rag-regression-20261112-2345.xml` | 11 | 0 | 0 | 0 | Not measured |
| 2026-11-12 step6 compliance regression only | `pytest tests/test_compliance_api.py tests/test_compliance_assistant.py tests/test_compliance_models.py tests/test_compliance_retrieval.py tests/test_corpus_indexer.py -v --tb=short --junitxml=docs/test-results/step6-compliance-regression-20261112-2345.xml` | 22 | 0 | 0 | 1 | Not measured |
| 2026-11-13 step7 focused matching | `pytest tests/test_intelligence.py -q --tb=short` | 15 | 0 | 0 | 1 | Not measured |
| 2026-11-13 step7 backend suite | `pytest -v --tb=short --junitxml=docs/test-results/step7-matching-20261113-0010.xml` | 116 | 0 | 0 | 1 | Not measured |
| 2026-11-13 step7 RAG regression only | `pytest rag/tests -v --tb=short --junitxml=docs/test-results/step7-rag-regression-20261113-0010.xml` | 11 | 0 | 0 | 0 | Not measured |
| 2026-11-13 step7 compliance regression only | `pytest tests/test_compliance_api.py tests/test_compliance_assistant.py tests/test_compliance_models.py tests/test_compliance_retrieval.py tests/test_corpus_indexer.py -v --tb=short --junitxml=docs/test-results/step7-compliance-regression-20261113-0010.xml` | 22 | 0 | 0 | 1 | Not measured |
| 2026-11-13 step8 focused jobs | `pytest tests/test_jobs.py -q --tb=short` | 4 | 0 | 0 | 1 | Not measured |
| 2026-11-13 step8 backend suite | `pytest -v --tb=short --junitxml=docs/test-results/step8-jobs-20261113-0020.xml` | 118 | 0 | 0 | 1 | Not measured |
| 2026-11-13 step8 RAG regression only | `pytest rag/tests -v --tb=short --junitxml=docs/test-results/step8-rag-regression-20261113-0020.xml` | 11 | 0 | 0 | 0 | Not measured |
| 2026-11-13 step8 compliance regression only | `pytest tests/test_compliance_api.py tests/test_compliance_assistant.py tests/test_compliance_models.py tests/test_compliance_retrieval.py tests/test_corpus_indexer.py -v --tb=short --junitxml=docs/test-results/step8-compliance-regression-20261113-0020.xml` | 22 | 0 | 0 | 1 | Not measured |
| 2026-11-13 step9 backend with app line tracing | `python ../docs/test-results/step9_coverage_runner.py` | 122 | 0 | 0 | 1 | 93.8% (848/904 app line starts) |
| 2026-11-13 step9 dependency-seam follow-up | `pytest tests/test_background_tasks.py tests/test_infrastructure.py tests/test_intelligence.py tests/test_admin_verification.py -q` | 29 | 0 | 0 | 1 | Not measured |
| 2026-11-13 step9 RAG regression only | `pytest rag/tests -q --junitxml=docs/test-results/step9-rag-regression-20261113.xml` | 11 | 0 | 0 | 0 | Not measured |
| 2026-11-13 step9 compliance regression only | `pytest tests/test_compliance_api.py tests/test_compliance_assistant.py tests/test_compliance_models.py tests/test_compliance_retrieval.py tests/test_corpus_indexer.py -q --junitxml=docs/test-results/step9-compliance-regression-20261113.xml` | 22 | 0 | 0 | 1 | Not measured |

The Step 9 backend results are [step9-backend-20261113.xml](../docs/test-results/step9-backend-20261113.xml)
and [step9-backend-20261113.txt](../docs/test-results/step9-backend-20261113.txt). App line coverage is
summarized in [step9-coverage-20261113.txt](../docs/test-results/step9-coverage-20261113.txt); the runner is
[step9_coverage_runner.py](../docs/test-results/step9_coverage_runner.py).

The Step 9 RAG regression-only results are [step9-rag-regression-20261113.xml](../docs/test-results/step9-rag-regression-20261113.xml)
and [step9-rag-regression-20261113.txt](../docs/test-results/step9-rag-regression-20261113.txt).

The Step 9 compliance regression-only results are [step9-compliance-regression-20261113.xml](../docs/test-results/step9-compliance-regression-20261113.xml)
and [step9-compliance-regression-20261113.txt](../docs/test-results/step9-compliance-regression-20261113.txt).
The required result files are [step1-containers-20261112-2200.xml](../docs/test-results/step1-containers-20261112-2200.xml)
and [step1-containers-20261112-2200.txt](../docs/test-results/step1-containers-20261112-2200.txt).

The step 2 result files are [step2-schema-gap-20261112-2215.xml](../docs/test-results/step2-schema-gap-20261112-2215.xml)
and [step2-schema-gap-20261112-2215.txt](../docs/test-results/step2-schema-gap-20261112-2215.txt).

The step 3 result files are [step3-auth-20261112-2226.xml](../docs/test-results/step3-auth-20261112-2226.xml)
and [step3-auth-20261112-2226.txt](../docs/test-results/step3-auth-20261112-2226.txt).

The step 4 result files are [step4-profiles-verification-20261112-2308.xml](../docs/test-results/step4-profiles-verification-20261112-2308.xml)
and [step4-profiles-verification-20261112-2308.txt](../docs/test-results/step4-profiles-verification-20261112-2308.txt).

The step 5 result files are [step5-admin-20261112-2320.xml](../docs/test-results/step5-admin-20261112-2320.xml)
and [step5-admin-20261112-2320.txt](../docs/test-results/step5-admin-20261112-2320.txt).

The Step 5 RAG regression-only files are [step5-compliance-rag-regression-20261112-2316.xml](../docs/test-results/step5-compliance-rag-regression-20261112-2316.xml)
and [step5-compliance-rag-regression-20261112-2316.txt](../docs/test-results/step5-compliance-rag-regression-20261112-2316.txt).

The Step 5 compliance regression-only files are [step5-compliance-regression-20261112-2320.xml](../docs/test-results/step5-compliance-regression-20261112-2320.xml)
and [step5-compliance-regression-20261112-2320.txt](../docs/test-results/step5-compliance-regression-20261112-2320.txt).

The Step 6 backend result files are [step6-llm-gateway-20261112-2345.xml](../docs/test-results/step6-llm-gateway-20261112-2345.xml)
and [step6-llm-gateway-20261112-2345.txt](../docs/test-results/step6-llm-gateway-20261112-2345.txt).

The Step 6 RAG regression-only files are [step6-rag-regression-20261112-2345.xml](../docs/test-results/step6-rag-regression-20261112-2345.xml)
and [step6-rag-regression-20261112-2345.txt](../docs/test-results/step6-rag-regression-20261112-2345.txt).

The Step 6 compliance regression-only files are [step6-compliance-regression-20261112-2345.xml](../docs/test-results/step6-compliance-regression-20261112-2345.xml)
and [step6-compliance-regression-20261112-2345.txt](../docs/test-results/step6-compliance-regression-20261112-2345.txt).

The Step 7 backend result files are [step7-matching-20261113-0010.xml](../docs/test-results/step7-matching-20261113-0010.xml)
and [step7-matching-20261113-0010.txt](../docs/test-results/step7-matching-20261113-0010.txt).

The Step 7 RAG regression-only files are [step7-rag-regression-20261113-0010.xml](../docs/test-results/step7-rag-regression-20261113-0010.xml)
and [step7-rag-regression-20261113-0010.txt](../docs/test-results/step7-rag-regression-20261113-0010.txt).

The Step 7 compliance regression-only files are [step7-compliance-regression-20261113-0010.xml](../docs/test-results/step7-compliance-regression-20261113-0010.xml)
and [step7-compliance-regression-20261113-0010.txt](../docs/test-results/step7-compliance-regression-20261113-0010.txt).

The Step 8 backend result files are [step8-jobs-20261113-0020.xml](../docs/test-results/step8-jobs-20261113-0020.xml)
and [step8-jobs-20261113-0020.txt](../docs/test-results/step8-jobs-20261113-0020.txt).

The Step 8 RAG regression-only files are [step8-rag-regression-20261113-0020.xml](../docs/test-results/step8-rag-regression-20261113-0020.xml)
and [step8-rag-regression-20261113-0020.txt](../docs/test-results/step8-rag-regression-20261113-0020.txt).

The Step 8 compliance regression-only files are [step8-compliance-regression-20261113-0020.xml](../docs/test-results/step8-compliance-regression-20261113-0020.xml)
and [step8-compliance-regression-20261113-0020.txt](../docs/test-results/step8-compliance-regression-20261113-0020.txt).

## Step 3 quality summary

- Coverage: not measured; coverage is not proof of quality.
- Tests executed: 99.
- Passed: 99.
- Failed: 0.
- Defect density: 0.00 failures per 100 executed tests.

## Step 5 quality summary

- Coverage: not measured; coverage is not proof of quality.
- Backend tests executed: 108; passed: 108; failed: 0; skipped: 0.
- RAG regression tests executed: 11; passed: 11; failed: 0; skipped: 0. Compliance and RAG remain regression-only and out of scope.
- Isolated compliance regression tests executed: 22; passed: 22; failed: 0; skipped: 0. Regression only, out of scope.
- Warnings: one existing Starlette/AnyIO deprecation warning in the backend run.
- Block-profile routing: not run; no block operation exists in the current API, and adding one would expand the approved contract.

## Step 6 quality summary

- Coverage: not measured; coverage is not proof of quality.
- Backend tests executed: 114; passed: 114; failed: 0; skipped: 0.
- RAG regression tests executed: 11; passed: 11; failed: 0; skipped: 0. Regression only, out of scope.
- Isolated compliance regression tests executed: 22; passed: 22; failed: 0; skipped: 0. Regression only, out of scope.
- Focused gateway, migration, and deletion tests: 24 passed; one existing Starlette/AnyIO warning.
- Warnings: one existing Starlette/AnyIO deprecation warning in backend and compliance runs.

## Step 7 quality summary

- Coverage: not measured; coverage is not proof of quality.
- Backend tests executed: 116; passed: 116; failed: 0; skipped: 0.
- RAG regression tests executed: 11; passed: 11; failed: 0; skipped: 0. Regression only, out of scope.
- Isolated compliance regression tests executed: 22; passed: 22; failed: 0; skipped: 0. Regression only, out of scope.
- Matching focused tests: 15 passed; one existing Starlette/AnyIO deprecation warning.
- Warnings: one existing Starlette/AnyIO deprecation warning in backend and compliance runs.

## Step 8 quality summary

- Coverage: not measured; coverage is not proof of quality.
- Backend tests executed: 118; passed: 118; failed: 0; skipped: 0.
- RAG regression tests executed: 11; passed: 11; failed: 0; skipped: 0. Regression only, out of scope.
- Isolated compliance regression tests executed: 22; passed: 22; failed: 0; skipped: 0. Regression only, out of scope.
- Focused jobs tests: 4 passed; one existing Starlette/AnyIO deprecation warning.
- Warnings: one existing Starlette/AnyIO deprecation warning in backend and compliance runs.

## Step 9 quality summary

- Coverage: 93.8% of backend application executable line starts (848/904), measured with Python's standard-library tracing. This is line coverage, not branch coverage.
- Backend: 122 passed, 0 failed, 0 skipped; one existing Starlette/AnyIO deprecation warning. Traced run took 2329.72 seconds. After final test dependency wiring, the 29 focused task, infrastructure, matching, and admin tests also passed.
- RAG regression: 11 passed, 0 failed, 0 skipped; regression-only and out of scope.
- Isolated compliance regression: 22 passed, 0 failed, 0 skipped; one existing Starlette/AnyIO deprecation warning. Regression-only and out of scope.

## Step 4 quality summary

- Coverage: not measured; coverage is not proof of quality.
- Tests executed: 102.
- Passed: 102.
- Failed: 0.
- Defect density: 0.00 failures per 100 executed tests.
