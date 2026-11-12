"""Add scored profile verification, appeals, reports, and decision history (FR-12 to FR-21)."""

from alembic import op
import sqlalchemy as sa


revision = "0009"
down_revision = "0008"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "profile_verifications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("portfolio_url", sa.String(length=2048), nullable=False),
        sa.Column("secp_entity_name", sa.String(length=255), nullable=False),
        sa.Column("secp_registration_number", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("band", sa.String(length=20), nullable=False),
        sa.Column("signals", sa.JSON(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("threshold_version", sa.String(length=100), nullable=False),
        sa.Column("consent_version", sa.String(length=80), nullable=False),
        sa.Column("consented_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("trust_notice_version", sa.String(length=80), nullable=False),
        sa.Column("trust_notice_accepted_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("rescore_locked", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.CheckConstraint("score >= 0 AND score <= 1", name="ck_profile_verifications_score"),
        sa.CheckConstraint(
            "status IN ('pending_review', 'auto_verified', 'auto_rejected', 'appeal_pending', 'verified', 'rejected', 'blocked')",
            name="ck_profile_verifications_status",
        ),
        sa.CheckConstraint("band IN ('high', 'review', 'low')", name="ck_profile_verifications_band"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("user_id", name="uq_profile_verifications_user"),
    )
    op.create_index(
        "ix_profile_verifications_status_created",
        "profile_verifications",
        ["status", "created_at"],
    )

    op.create_table(
        "verification_appeals",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("verification_id", sa.Integer(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("added_evidence", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=20), server_default="pending", nullable=False),
        sa.Column("decision_reason", sa.Text()),
        sa.Column("reviewed_by", sa.Integer()),
        sa.Column("reviewed_at", sa.DateTime()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.CheckConstraint("status IN ('pending', 'approved', 'rejected')", name="ck_verification_appeals_status"),
        sa.ForeignKeyConstraint(["verification_id"], ["profile_verifications.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["reviewed_by"], ["users.id"], ondelete="SET NULL"),
        sa.UniqueConstraint("verification_id", name="uq_verification_appeals_verification"),
    )
    op.create_index("ix_verification_appeals_status_created", "verification_appeals", ["status", "created_at"])

    op.create_table(
        "profile_reports",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("reporter_user_id", sa.Integer(), nullable=False),
        sa.Column("target_user_id", sa.Integer(), nullable=False),
        sa.Column("reason", sa.String(length=1000), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["reporter_user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["target_user_id"], ["users.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("reporter_user_id", "target_user_id", name="uq_profile_reports_reporter_target"),
    )
    op.create_index("ix_profile_reports_target_created", "profile_reports", ["target_user_id", "created_at"])

    op.create_table(
        "verification_decisions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("verification_id", sa.Integer(), nullable=False),
        sa.Column("reviewer_user_id", sa.Integer()),
        sa.Column("decision", sa.String(length=30), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("band", sa.String(length=20), nullable=False),
        sa.Column("signals", sa.JSON(), nullable=False),
        sa.Column("threshold_version", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["verification_id"], ["profile_verifications.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["reviewer_user_id"], ["users.id"], ondelete="SET NULL"),
    )
    op.create_index(
        "ix_verification_decisions_profile_created",
        "verification_decisions",
        ["verification_id", "created_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_verification_decisions_profile_created", table_name="verification_decisions")
    op.drop_table("verification_decisions")
    op.drop_index("ix_profile_reports_target_created", table_name="profile_reports")
    op.drop_table("profile_reports")
    op.drop_index("ix_verification_appeals_status_created", table_name="verification_appeals")
    op.drop_table("verification_appeals")
    op.drop_index("ix_profile_verifications_status_created", table_name="profile_verifications")
    op.drop_table("profile_verifications")
