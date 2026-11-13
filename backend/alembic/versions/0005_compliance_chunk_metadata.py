"""Add citation metadata to existing compliance chunks (FR-8, NFR-12, NFR-14)."""

import sqlalchemy as sa
from alembic import op

revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("compliance_chunks", sa.Column("heading_path", sa.JSON(), nullable=True))
    op.add_column("compliance_chunks", sa.Column("effective_date", sa.String(length=32)))
    op.add_column("compliance_chunks", sa.Column("corpus_version", sa.String(length=64)))
    op.execute("UPDATE compliance_chunks SET heading_path = '[]' WHERE heading_path IS NULL")
    with op.batch_alter_table("compliance_chunks") as batch_op:
        batch_op.alter_column("heading_path", existing_type=sa.JSON(), nullable=False)


def downgrade() -> None:
    op.drop_column("compliance_chunks", "corpus_version")
    op.drop_column("compliance_chunks", "effective_date")
    op.drop_column("compliance_chunks", "heading_path")
