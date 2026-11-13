"""Persist metadata for Gemini attempts and structured cache hits (NFR-2, NFR-19)."""

import sqlalchemy as sa

from alembic import op

revision = "0012"
down_revision = "0011"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "llm_gateway_call_logs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("request_id", sa.String(length=36), nullable=False),
        sa.Column("operation", sa.String(length=100), nullable=False),
        sa.Column("model_name", sa.String(length=120), nullable=False),
        sa.Column("prompt_version", sa.String(length=120), nullable=True),
        sa.Column("attempt_number", sa.Integer(), nullable=False),
        sa.Column("queue_position", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("passage_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "approximate_prompt_chars", sa.Integer(), nullable=False, server_default="0"
        ),
        sa.Column("cache_hit", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("outcome", sa.String(length=16), nullable=False),
        sa.Column("failure_category", sa.String(length=80), nullable=True),
        sa.Column("elapsed_ms", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "outcome IN ('success', 'failure', 'cache_hit')",
            name="ck_llm_gateway_call_logs_outcome",
        ),
        sa.CheckConstraint(
            "attempt_number >= 0", name="ck_llm_gateway_call_logs_attempt"
        ),
        sa.CheckConstraint(
            "queue_position >= 0", name="ck_llm_gateway_call_logs_queue_position"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_llm_gateway_call_logs_created_at",
        "llm_gateway_call_logs",
        ["created_at"],
    )
    op.create_index(
        "ix_llm_gateway_call_logs_request_id",
        "llm_gateway_call_logs",
        ["request_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_llm_gateway_call_logs_request_id", table_name="llm_gateway_call_logs"
    )
    op.drop_index(
        "ix_llm_gateway_call_logs_created_at", table_name="llm_gateway_call_logs"
    )
    op.drop_table("llm_gateway_call_logs")
