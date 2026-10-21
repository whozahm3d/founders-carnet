from pathlib import Path

from alembic.config import Config
from sqlalchemy import create_engine, inspect
from sqlalchemy.pool import StaticPool

from alembic import command

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
        }.issubset(tables)
        assert "alembic_version" in tables
        assert {"consent_version", "consented_at", "embedding"}.issubset(
            {column["name"] for column in inspect(connection).get_columns("ecosystem_profiles")}
        )
        assert {"factors", "similarity", "score", "founder_accepted", "candidate_accepted"}.issubset(
            {column["name"] for column in inspect(connection).get_columns("match_records")}
        )
        assert {"id", "email", "hashed_password", "role"}.issubset(
            {column["name"] for column in inspect(connection).get_columns("users")}
        )
        assert "token_version" in {
            column["name"] for column in inspect(connection).get_columns("users")
        }

    engine.dispose()
