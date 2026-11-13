"""Add compliance corpus, chunks, query log, and citations (FR-8, NFR-11, NFR-12, NFR-13, NFR-14, NFR-22).

Revision ID: 0002
Revises: 0001
"""

import sqlalchemy as sa
from pgvector.sqlalchemy import VECTOR

from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    vector_type = VECTOR().with_variant(sa.JSON(), "sqlite")

    op.create_table(
        "compliance_documents",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("file_name", sa.String(length=255), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("issuing_body", sa.String(length=100), nullable=False),
        sa.Column("document_type", sa.String(length=50), nullable=False),
        sa.Column("source_url", sa.Text(), nullable=False),
        sa.Column("effective_date", sa.String(length=32), nullable=True),
        sa.Column("consolidation_date", sa.String(length=32), nullable=True),
        sa.Column("retrieved_at", sa.String(length=32), nullable=True),
        sa.Column("content_sha256", sa.String(length=64), nullable=False),
        sa.Column("scope_note", sa.Text(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("file_name"),
    )
    op.create_index(
        "ix_compliance_documents_active",
        "compliance_documents",
        ["is_active"],
    )

    op.create_table(
        "compliance_chunks",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("document_id", sa.Integer(), nullable=False),
        sa.Column("chunk_id", sa.String(length=512), nullable=False),
        sa.Column("page_number", sa.Integer(), nullable=False),
        sa.Column("section", sa.String(length=100), nullable=True),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("embedding", vector_type, nullable=True),
        sa.Column("embedding_model", sa.String(length=255), nullable=True),
        sa.CheckConstraint("page_number >= 1", name="ck_compliance_chunks_page_number"),
        sa.ForeignKeyConstraint(
            ["document_id"],
            ["compliance_documents.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("chunk_id", name="uq_compliance_chunks_chunk_id"),
    )
    op.create_index(
        "ix_compliance_chunks_document_id",
        "compliance_chunks",
        ["document_id"],
    )

    op.create_table(
        "compliance_queries",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("answer_text", sa.Text(), nullable=True),
        sa.Column("outcome", sa.String(length=20), nullable=False),
        sa.Column("abstention_reason", sa.String(length=100), nullable=True),
        sa.Column("passage_count", sa.Integer(), nullable=False),
        sa.Column("latency_ms", sa.Integer(), nullable=False),
        sa.Column("prompt_version", sa.String(length=100), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "outcome IN ('answered', 'abstained', 'failed')",
            name="ck_compliance_queries_outcome",
        ),
        sa.CheckConstraint(
            "passage_count >= 0", name="ck_compliance_queries_passage_count"
        ),
        sa.CheckConstraint("latency_ms >= 0", name="ck_compliance_queries_latency"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_compliance_queries_user_id", "compliance_queries", ["user_id"])

    op.create_table(
        "compliance_citations",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("query_id", sa.Integer(), nullable=False),
        sa.Column("chunk_id", sa.Integer(), nullable=False),
        sa.Column("rank", sa.Integer(), nullable=False),
        sa.CheckConstraint("rank >= 1", name="ck_compliance_citations_rank"),
        sa.ForeignKeyConstraint(
            ["chunk_id"], ["compliance_chunks.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["query_id"], ["compliance_queries.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "query_id", "chunk_id", name="uq_compliance_citations_query_chunk"
        ),
    )


def downgrade() -> None:
    op.drop_table("compliance_citations")
    op.drop_index("ix_compliance_queries_user_id", table_name="compliance_queries")
    op.drop_table("compliance_queries")
    op.drop_index("ix_compliance_chunks_document_id", table_name="compliance_chunks")
    op.drop_table("compliance_chunks")
    op.drop_index("ix_compliance_documents_active", table_name="compliance_documents")
    op.drop_table("compliance_documents")
