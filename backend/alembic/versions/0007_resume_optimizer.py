"""Store resume optimizer ownership and suggestions (FR-5, NFR-7, NFR-22).

Revision ID: 0007
Revises: 0006
"""

import sqlalchemy as sa

from alembic import op

revision = "0007"
down_revision = "0006"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "resume_optimizations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("storage_key", sa.String(length=32), nullable=False),
        sa.Column("file_sha256", sa.String(length=64), nullable=False),
        sa.Column("target_role", sa.String(length=120), nullable=False),
        sa.Column("processing_consent_version", sa.String(length=80), nullable=False),
        sa.Column(
            "processing_consented_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("suggestions", sa.JSON(), nullable=True),
        sa.Column("prompt_version", sa.String(length=80), nullable=False),
        sa.Column("model_name", sa.String(length=100), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("storage_key", name="uq_resume_optimizations_storage_key"),
    )
    op.create_index(
        "ix_resume_optimizations_user_created",
        "resume_optimizations",
        ["user_id", "created_at"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_resume_optimizations_user_created", table_name="resume_optimizations"
    )
    op.drop_table("resume_optimizations")
