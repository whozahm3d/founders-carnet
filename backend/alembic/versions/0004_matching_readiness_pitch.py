"""Add ecosystem matching, readiness, and pitch records (FR-2, FR-3, FR-7, FR-10, FR-28, FR-29, NFR-22).

Revision ID: 0004
Revises: 0003
"""

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import VECTOR


revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    vector_type = VECTOR().with_variant(sa.JSON(), "sqlite")
    op.create_table(
        "ecosystem_profiles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("sector", sa.String(100), nullable=False),
        sa.Column("stages", sa.JSON(), nullable=False),
        sa.Column("skills", sa.JSON(), nullable=False),
        sa.Column("availability", sa.String(30), nullable=False),
        sa.Column("ticket_min", sa.Float()),
        sa.Column("ticket_max", sa.Float()),
        sa.Column("location", sa.String(255), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("consent_version", sa.String(50), nullable=False),
        sa.Column("consented_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("is_open", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("embedding", vector_type),
        sa.Column("embedding_model", sa.String(255)),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.CheckConstraint("user_id > 0", name="ck_ecosystem_profiles_user_id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index("ix_ecosystem_profiles_open", "ecosystem_profiles", ["is_open"])

    op.create_table(
        "match_records",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("startup_id", sa.Integer(), nullable=False),
        sa.Column("candidate_user_id", sa.Integer(), nullable=False),
        sa.Column("factors", sa.JSON(), nullable=False),
        sa.Column("similarity", sa.Float(), nullable=False, server_default="0"),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("founder_accepted", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("candidate_accepted", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.CheckConstraint("score >= 0 AND score <= 1", name="ck_match_records_score"),
        sa.ForeignKeyConstraint(["startup_id"], ["startups.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["candidate_user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("startup_id", "candidate_user_id", name="uq_match_startup_candidate"),
    )
    op.create_index("ix_match_records_startup_id", "match_records", ["startup_id"])

    op.create_table(
        "readiness_assessments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("startup_id", sa.Integer(), nullable=False),
        sa.Column("rubric_version", sa.String(50), nullable=False),
        sa.Column("result", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["startup_id"], ["startups.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_readiness_startup_created", "readiness_assessments", ["startup_id", "created_at"])

    op.create_table(
        "pitch_sessions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("startup_id", sa.Integer(), nullable=False),
        sa.Column("persona", sa.String(100), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="active"),
        sa.Column("scores", sa.JSON()),
        sa.Column("rubric_version", sa.String(50), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("completed_at", sa.DateTime()),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["startup_id"], ["startups.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_pitch_sessions_user_created", "pitch_sessions", ["user_id", "created_at"])

    op.create_table(
        "pitch_turns",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("session_id", sa.Integer(), nullable=False),
        sa.Column("turn_number", sa.Integer(), nullable=False),
        sa.Column("speaker", sa.String(20), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.CheckConstraint("turn_number >= 1", name="ck_pitch_turns_turn_number"),
        sa.ForeignKeyConstraint(["session_id"], ["pitch_sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("session_id", "turn_number", name="uq_pitch_session_turn"),
    )


def downgrade() -> None:
    op.drop_table("pitch_turns")
    op.drop_index("ix_pitch_sessions_user_created", table_name="pitch_sessions")
    op.drop_table("pitch_sessions")
    op.drop_index("ix_readiness_startup_created", table_name="readiness_assessments")
    op.drop_table("readiness_assessments")
    op.drop_index("ix_match_records_startup_id", table_name="match_records")
    op.drop_table("match_records")
    op.drop_index("ix_ecosystem_profiles_open", table_name="ecosystem_profiles")
    op.drop_table("ecosystem_profiles")
