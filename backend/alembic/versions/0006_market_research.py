"""Store market research interpretations and their public-web evidence (FR-4, NFR-22).

Revision ID: 0006
Revises: 0005
"""

import sqlalchemy as sa

from alembic import op

revision = "0006"
down_revision = "0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "market_research_reports",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("startup_id", sa.Integer(), nullable=False),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("interpretation", sa.JSON(), nullable=True),
        sa.Column("evidence", sa.JSON(), nullable=False),
        sa.Column("prompt_version", sa.String(length=80), nullable=False),
        sa.Column("model_name", sa.String(length=100), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["startup_id"], ["startups.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_market_research_startup_created",
        "market_research_reports",
        ["startup_id", "created_at"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_market_research_startup_created", table_name="market_research_reports"
    )
    op.drop_table("market_research_reports")
