"""Add talent profiles and normalized verification signals (FR-13, FR-19, NFR-15)."""

from alembic import op
import sqlalchemy as sa


revision = "0011"
down_revision = "0010"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "talent_profiles",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("github_url", sa.String(length=2048), nullable=True),
        sa.Column("consent_version", sa.String(length=80), nullable=False),
        sa.Column("consented_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", name="uq_talent_profiles_user"),
    )
    op.create_table(
        "verification_signals",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("verification_id", sa.Integer(), nullable=False),
        sa.Column("signal_name", sa.String(length=80), nullable=False),
        sa.Column("input_snapshot", sa.JSON(), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("outcome", sa.String(length=80), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["verification_id"], ["profile_verifications.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("verification_id", "signal_name", name="uq_verification_signals_case_name"),
    )
    op.create_index("ix_verification_signals_verification_id", "verification_signals", ["verification_id"])


def downgrade() -> None:
    op.drop_index("ix_verification_signals_verification_id", table_name="verification_signals")
    op.drop_table("verification_signals")
    op.drop_table("talent_profiles")
