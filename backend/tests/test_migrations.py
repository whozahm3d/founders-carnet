from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.pool import StaticPool


BACKEND_ROOT = Path(__file__).resolve().parents[1]


def test_migrations_build_user_schema_from_empty_database():
    config = Config(str(BACKEND_ROOT / "alembic.ini"))
    engine = create_engine("sqlite://", poolclass=StaticPool)

    with engine.begin() as connection:
        config.attributes["connection"] = connection
        command.upgrade(config, "head")

        tables = inspect(connection).get_table_names()
        assert "users" in tables
        assert {
            "compliance_documents",
            "compliance_chunks",
            "compliance_queries",
            "compliance_citations",
            "founder_profiles",
            "startups",
            "ecosystem_profiles",
            "match_records",
            "readiness_assessments",
            "pitch_sessions",
            "pitch_turns",
            "market_research_reports",
            "resume_optimizations",
            "job_listings",
            "job_saves",
            "job_applications",
            "profile_verifications",
            "verification_appeals",
            "profile_reports",
            "verification_decisions",
            "consent_records",
            "oauth_identities",
            "talent_profiles",
            "verification_signals",
            "llm_gateway_call_logs",
        }.issubset(tables)
        assert "alembic_version" in tables
        assert {"consent_version", "consented_at", "embedding"}.issubset(
            {column["name"] for column in inspect(connection).get_columns("ecosystem_profiles")}
        )
        assert {"factors", "similarity", "score", "founder_accepted", "candidate_accepted"}.issubset(
            {column["name"] for column in inspect(connection).get_columns("match_records")}
        )
        assert {"request_status", "requester_user_id"}.issubset(
            {column["name"] for column in inspect(connection).get_columns("match_records")}
        )
        assert {
            "question", "status", "interpretation", "evidence", "prompt_version", "model_name",
        }.issubset(
            {column["name"] for column in inspect(connection).get_columns("market_research_reports")}
        )
        assert {
            "user_id", "storage_key", "file_sha256", "target_role", "processing_consent_version",
            "processing_consented_at", "status", "suggestions",
            "prompt_version", "model_name",
        }.issubset(
            {column["name"] for column in inspect(connection).get_columns("resume_optimizations")}
        )
        assert {"id", "email", "hashed_password", "role"}.issubset(
            {column["name"] for column in inspect(connection).get_columns("users")}
        )
        assert "token_version" in {
            column["name"] for column in inspect(connection).get_columns("users")
        }
        assert {"deletion_requested_at", "deletion_scheduled_for"}.issubset(
            {column["name"] for column in inspect(connection).get_columns("users")}
        )
        assert {"user_id", "consent_type", "consent_version", "withdrawn_at", "source"}.issubset(
            {column["name"] for column in inspect(connection).get_columns("consent_records")}
        )
        assert {"user_id", "provider", "provider_subject"}.issubset(
            {column["name"] for column in inspect(connection).get_columns("oauth_identities")}
        )
        assert {"user_id", "github_url", "consent_version"}.issubset(
            {column["name"] for column in inspect(connection).get_columns("talent_profiles")}
        )
        assert {"verification_id", "signal_name", "input_snapshot", "score", "outcome", "reason"}.issubset(
            {column["name"] for column in inspect(connection).get_columns("verification_signals")}
        )
        assert {
            "request_id", "operation", "model_name", "prompt_version", "attempt_number",
            "queue_position", "passage_count", "approximate_prompt_chars", "cache_hit",
            "outcome", "failure_category", "elapsed_ms", "created_at",
        }.issubset(
            {column["name"] for column in inspect(connection).get_columns("llm_gateway_call_logs")}
        )
        assert {"startup_id", "title", "employment_type", "status"}.issubset(
            {column["name"] for column in inspect(connection).get_columns("job_listings")}
        )
        assert {"job_id", "user_id"}.issubset(
            {column["name"] for column in inspect(connection).get_columns("job_saves")}
        )
        assert {"job_id", "candidate_user_id", "status"}.issubset(
            {column["name"] for column in inspect(connection).get_columns("job_applications")}
        )
        assert {"user_id", "score", "band", "signals", "status"}.issubset(
            {column["name"] for column in inspect(connection).get_columns("profile_verifications")}
        )
        assert {"verification_id", "added_evidence", "status"}.issubset(
            {column["name"] for column in inspect(connection).get_columns("verification_appeals")}
        )
        assert {"reporter_user_id", "target_user_id", "reason"}.issubset(
            {column["name"] for column in inspect(connection).get_columns("profile_reports")}
        )
        assert {"reviewer_user_id", "decision", "threshold_version"}.issubset(
            {column["name"] for column in inspect(connection).get_columns("verification_decisions")}
        )

    engine.dispose()


def test_match_request_migration_backfills_existing_acceptance_flags():
    config = Config(str(BACKEND_ROOT / "alembic.ini"))
    engine = create_engine("sqlite://", poolclass=StaticPool)

    with engine.begin() as connection:
        config.attributes["connection"] = connection
        command.upgrade(config, "0004")
        connection.execute(
            text(
                """
                INSERT INTO users (id, email, full_name, hashed_password, role)
                VALUES (1, 'founder@example.com', 'Founder', 'hash', 'founder'),
                       (2, 'candidate-2@example.com', 'Candidate 2', 'hash', 'mentor'),
                       (3, 'candidate-3@example.com', 'Candidate 3', 'hash', 'mentor'),
                       (4, 'candidate-4@example.com', 'Candidate 4', 'hash', 'talent'),
                       (5, 'candidate-5@example.com', 'Candidate 5', 'hash', 'investor')
                """
            )
        )
        connection.execute(
            text(
                """
                INSERT INTO founder_profiles (id, user_id, consent_version)
                VALUES (1, 1, 'founder-profile-v1')
                """
            )
        )
        connection.execute(
            text(
                """
                INSERT INTO startups (
                    id, founder_profile_id, name, description, sector, stage, location,
                    business_model, traction_summary, skills
                ) VALUES (
                    1, 1, 'Demo Startup', 'Demo description', 'logistics', 'mvp', 'Lahore',
                    'Subscription', 'Pilot users', '[]'
                )
                """
            )
        )
        connection.execute(
            text(
                """
                INSERT INTO match_records (
                    id, startup_id, candidate_user_id, factors, score,
                    founder_accepted, candidate_accepted
                ) VALUES
                    (1, 1, 2, '{}', 0.5, false, false),
                    (2, 1, 3, '{}', 0.5, true, false),
                    (3, 1, 4, '{}', 0.5, false, true),
                    (4, 1, 5, '{}', 0.5, true, true)
                """
            )
        )

        command.upgrade(config, "head")
        states = connection.execute(
            text(
                """
                SELECT request_status, requester_user_id
                FROM match_records
                ORDER BY id
                """
            )
        ).all()

    assert states == [
        ("recommended", None),
        ("pending", 1),
        ("pending", 4),
        ("accepted", 1),
    ]
    engine.dispose()
