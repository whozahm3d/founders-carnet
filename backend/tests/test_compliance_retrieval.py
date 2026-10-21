from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.models import Base, ComplianceChunk, ComplianceDocument
from app.services.compliance_retrieval import (
    get_retrieval_index_stats,
    retrieve_top_chunks,
)


def test_empty_index_reports_no_active_documents_or_embeddings():
    engine = create_engine("sqlite://", poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        stats = get_retrieval_index_stats(session, embedding_model="candidate-v1")

    assert stats.active_document_count == 0
    assert stats.document_count == 0
    assert stats.active_chunk_count == 0
    assert stats.embedded_chunk_count == 0
    assert stats.compatible_chunk_count == 0
    engine.dispose()


def test_retrieval_returns_only_active_chunks_from_configured_model():
    engine = create_engine("sqlite://", poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        active_document = ComplianceDocument(
            file_name="active.pdf",
            title="Income Tax Ordinance",
            issuing_body="FBR",
            document_type="statute",
            source_url="https://example.test/active",
            effective_date="2026-06-30",
            consolidation_date=None,
            retrieved_at=None,
            content_sha256="a" * 64,
            scope_note="Relevant tax provisions.",
            is_active=True,
        )
        inactive_document = ComplianceDocument(
            file_name="inactive.pdf",
            title="Superseded schedule",
            issuing_body="SECP",
            document_type="fee schedule",
            source_url="https://example.test/inactive",
            effective_date="2025-04-20",
            consolidation_date=None,
            retrieved_at=None,
            content_sha256="b" * 64,
            scope_note="Superseded.",
            is_active=False,
        )
        session.add_all(
            [
                active_document,
                inactive_document,
                ComplianceChunk(
                    document=active_document,
                    chunk_id="active:1:0",
                    page_number=1,
                    section="1",
                    text="Current tax provision.",
                    embedding=[1.0, 0.0],
                    embedding_model="candidate-v1",
                ),
                ComplianceChunk(
                    document=active_document,
                    chunk_id="active:1:1",
                    page_number=1,
                    section="2",
                    text="Orthogonal passage.",
                    embedding=[0.0, 1.0],
                    embedding_model="candidate-v1",
                ),
                ComplianceChunk(
                    document=inactive_document,
                    chunk_id="inactive:1:0",
                    page_number=1,
                    section="1",
                    text="Old provision.",
                    embedding=[1.0, 0.0],
                    embedding_model="candidate-v1",
                ),
                ComplianceChunk(
                    document=active_document,
                    chunk_id="active:1:2",
                    page_number=1,
                    section="3",
                    text="Different model passage.",
                    embedding=[1.0, 0.0],
                    embedding_model="old-model",
                ),
                ComplianceChunk(
                    document=active_document,
                    chunk_id="active:1:3",
                    page_number=1,
                    section="4",
                    text="Incompatible dimension passage.",
                    embedding=[1.0, 0.0, 0.0],
                    embedding_model="candidate-v1",
                ),
            ]
        )
        session.commit()

        stats = get_retrieval_index_stats(session, embedding_model="candidate-v1")
        assert stats.document_count == 2
        assert stats.active_document_count == 1
        assert stats.active_chunk_count == 4
        assert stats.embedded_chunk_count == 4
        assert stats.compatible_chunk_count == 3

        results = retrieve_top_chunks(
            session,
            query_embedding=[1.0, 0.0],
            embedding_model="candidate-v1",
            top_k=3,
            minimum_similarity=0.8,
        )
        assert len(results) == 1
        assert results[0].chunk.chunk_id == "active:1:0"
        assert results[0].chunk.document.title == "Income Tax Ordinance"
        assert results[0].similarity == 1.0
    engine.dispose()
