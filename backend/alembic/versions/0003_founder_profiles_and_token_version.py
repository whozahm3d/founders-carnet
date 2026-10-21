"""Add founder profiles, startup records, and token invalidation (FR-1, FR-23, NFR-22).

Revision ID: 0003
Revises: 0002
"""

import sqlalchemy as sa

from alembic import op

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("token_version", sa.Integer(), server_default="0", nullable=False),
    )
    op.create_table(
        "founder_profiles",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column("consent_version", sa.String(length=50), nullable=False),
        sa.Column(
            "consented_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_table(
        "startups",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("founder_profile_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("sector", sa.String(length=100), nullable=False),
        sa.Column("stage", sa.String(length=30), nullable=False),
        sa.Column("location", sa.String(length=255), nullable=False),
        sa.Column("business_model", sa.String(length=255), nullable=False),
        sa.Column("traction_summary", sa.Text(), nullable=False),
        sa.Column("customer_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("monthly_revenue", sa.Numeric(14, 2), nullable=True),
        sa.Column("skills", sa.JSON(), nullable=False),
        sa.Column("funding_need_min", sa.Numeric(14, 2), nullable=True),
        sa.Column("funding_need_max", sa.Numeric(14, 2), nullable=True),
        sa.Column("is_verified", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "stage IN ('idea', 'mvp', 'growth', 'scaling')",
            name="ck_startups_stage",
        ),
        sa.CheckConstraint("customer_count >= 0", name="ck_startups_customer_count"),
        sa.CheckConstraint(
            "monthly_revenue IS NULL OR monthly_revenue >= 0",
            name="ck_startups_monthly_revenue",
        ),
        sa.CheckConstraint(
            "funding_need_min IS NULL OR funding_need_min >= 0",
            name="ck_startups_funding_need_min",
        ),
        sa.CheckConstraint(
            "funding_need_max IS NULL OR funding_need_max >= funding_need_min",
            name="ck_startups_funding_need_range",
        ),
        sa.ForeignKeyConstraint(
            ["founder_profile_id"],
            ["founder_profiles.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_startups_founder_profile_id",
        "startups",
        ["founder_profile_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_startups_founder_profile_id", table_name="startups")
    op.drop_table("startups")
    op.drop_table("founder_profiles")
    op.drop_column("users", "token_version")
