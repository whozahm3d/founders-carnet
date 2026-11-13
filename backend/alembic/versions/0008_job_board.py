"""Add verified-founder job listings and talent applications (FR-6, FR-24, FR-25, NFR-22).

Revision ID: 0008
Revises: 0007
"""

import sqlalchemy as sa

from alembic import op

revision = "0008"
down_revision = "0007"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "job_listings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("startup_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("employment_type", sa.String(length=20), nullable=False),
        sa.Column("location", sa.String(length=255), nullable=False),
        sa.Column("is_remote", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column(
            "status", sa.String(length=20), nullable=False, server_default="open"
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")
        ),
        sa.CheckConstraint(
            "employment_type IN ('job', 'internship')", name="ck_job_listings_type"
        ),
        sa.CheckConstraint(
            "status IN ('open', 'closed')", name="ck_job_listings_status"
        ),
        sa.ForeignKeyConstraint(["startup_id"], ["startups.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_job_listings_status_created", "job_listings", ["status", "created_at"]
    )
    op.create_index("ix_job_listings_startup_id", "job_listings", ["startup_id"])

    op.create_table(
        "job_saves",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("job_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["job_id"], ["job_listings.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("job_id", "user_id", name="uq_job_saves_job_user"),
    )
    op.create_index("ix_job_saves_user_created", "job_saves", ["user_id", "created_at"])

    op.create_table(
        "job_applications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("job_id", sa.Integer(), nullable=False),
        sa.Column("candidate_user_id", sa.Integer(), nullable=False),
        sa.Column("cover_letter", sa.Text()),
        sa.Column(
            "status", sa.String(length=20), nullable=False, server_default="submitted"
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")
        ),
        sa.CheckConstraint(
            "status IN ('submitted', 'reviewing', 'shortlisted', 'rejected', 'withdrawn')",
            name="ck_job_applications_status",
        ),
        sa.ForeignKeyConstraint(["job_id"], ["job_listings.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["candidate_user_id"], ["users.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "job_id", "candidate_user_id", name="uq_job_applications_job_candidate"
        ),
    )
    op.create_index(
        "ix_job_applications_job_created", "job_applications", ["job_id", "created_at"]
    )
    op.create_index(
        "ix_job_applications_candidate_created",
        "job_applications",
        ["candidate_user_id", "created_at"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_job_applications_candidate_created", table_name="job_applications"
    )
    op.drop_index("ix_job_applications_job_created", table_name="job_applications")
    op.drop_table("job_applications")
    op.drop_index("ix_job_saves_user_created", table_name="job_saves")
    op.drop_table("job_saves")
    op.drop_index("ix_job_listings_startup_id", table_name="job_listings")
    op.drop_index("ix_job_listings_status_created", table_name="job_listings")
    op.drop_table("job_listings")
