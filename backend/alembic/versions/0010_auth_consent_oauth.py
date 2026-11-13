"""Add consent records, OAuth identities, and deletion scheduling (FR-17, FR-22, FR-27)."""

import sqlalchemy as sa

from alembic import op

revision = "0010"
down_revision = "0009"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users", sa.Column("deletion_requested_at", sa.DateTime(), nullable=True)
    )
    op.add_column(
        "users", sa.Column("deletion_scheduled_for", sa.DateTime(), nullable=True)
    )
    op.create_table(
        "consent_records",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("consent_type", sa.String(length=80), nullable=False),
        sa.Column("consent_version", sa.String(length=80), nullable=False),
        sa.Column(
            "accepted_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("withdrawn_at", sa.DateTime(), nullable=True),
        sa.Column("source", sa.String(length=30), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "user_id", "consent_type", name="uq_consent_records_user_type"
        ),
    )
    op.create_index(
        "ix_consent_records_user_type", "consent_records", ["user_id", "consent_type"]
    )
    op.create_table(
        "oauth_identities",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("provider", sa.String(length=40), nullable=False),
        sa.Column("provider_subject", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "provider", "provider_subject", name="uq_oauth_provider_subject"
        ),
        sa.UniqueConstraint("user_id", "provider", name="uq_oauth_user_provider"),
    )


def downgrade() -> None:
    op.drop_table("oauth_identities")
    op.drop_index("ix_consent_records_user_type", table_name="consent_records")
    op.drop_table("consent_records")
    op.drop_column("users", "deletion_scheduled_for")
    op.drop_column("users", "deletion_requested_at")
