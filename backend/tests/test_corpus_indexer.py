import hashlib
from pathlib import Path

from rag.compliance.documents import ExtractedPage
from rag.compliance.ingestion import CorpusDocument
from rag.compliance.scoping import apply_corpus_scope
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.models import Base, ComplianceChunk, ComplianceDocument
from app.services.corpus_indexer import index_corpus


class FakeEncoder:
    def encode(self, texts):
        return tuple((1.0, 0.0) for _ in texts)


def _corpus_document(file_name: str) -> CorpusDocument:
    return CorpusDocument(
        file=file_name,
        title="Test document",
        issuing_body="Test issuer",
        document_type="statute",
        source_url="https://example.test/source",
        effective_date=None,
        consolidation_date=None,
        retrieved_at=None,
        content_sha256="0" * 64,
        scope_note="Test scope",
        is_active=True,
    )


def test_companies_act_scope_keeps_allowed_parts_and_sections():
    pages = (
        ExtractedPage(
            page_number=1,
            text=(
                "PART I\n1. Preliminary\nallowed part one\n"
                "PART II\n3. Court\nexcluded part two\n"
                "PART IV\n9. Incorporation\nallowed part four\n"
                "PART V\n10. Shares\nexcluded part five\n"
                "PART XII\n462. Registration offices\nallowed exception\n"
                "474. Enforcing compliance\nexcluded exception\n"
            ),
        ),
    )

    scoped = apply_corpus_scope(
        _corpus_document("Companies Act 2017, updated 18 Aug 2022 (SECP).pdf"),
        pages,
    )

    text = "\n".join(page.text for page in scoped)
    assert "allowed part one" in text
    assert "allowed part four" in text
    assert "allowed exception" in text
    assert "excluded part two" not in text
    assert "excluded part five" not in text
    assert "excluded exception" not in text


def test_income_tax_scope_keeps_only_manifested_sections_and_division():
    pages = (
        ExtractedPage(
            page_number=1,
            text=(
                "2. Definitions\n(62A) permitted definition\n(62B) excluded definition\n"
                "154A. Permitted section\npermitted section text\n"
                "154B. Excluded section\nexcluded section text\n"
                "FIRST SCHEDULE\nPART II\nDIVISION IVA\nwrong part\n"
                "PART III\nDIVISION IVA\npermitted division\n"
                "DIVISION IVB\nexcluded division\n"
            ),
        ),
    )

    scoped = apply_corpus_scope(
        _corpus_document("Income Tax Ordinance 2001, amended to 30 Jun 2026 (FBR).pdf"),
        pages,
    )

    text = "\n".join(page.text for page in scoped)
    assert "permitted definition" in text
    assert "excluded definition" not in text
    assert "permitted section text" in text
    assert "excluded section text" not in text
    assert "permitted division" in text
    assert "wrong part" not in text
    assert "excluded division" not in text


def test_indexer_verifies_and_persists_text_source_chunks(tmp_path: Path):
    corpus_dir = tmp_path / "data"
    corpus_dir.mkdir()
    source_path = corpus_dir / "sample.txt"
    source_text = "Section 1. Procedure\nFollow the published steps."
    source_path.write_text(source_text, encoding="utf-8")
    source_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
    manifest_path = tmp_path / "corpus_manifest.md"
    manifest_path.write_text(
        """| file | title | issuing_body | document_type | source_url | effective_date | consolidation_date | retrieved_at | content_sha256 | scope_note | is_active |
|---|---|---|---|---|---|---|---|---|---|---|
| `sample.txt` | Sample Guide | FBR | guide | <https://example.test/source> | 2026-06-30 |  | 2026-10-04 | `"""
        + source_hash
        + "` | Procedure only. | true |\n",
        encoding="utf-8",
    )
    engine = create_engine("sqlite://", poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        summary = index_corpus(
            session,
            manifest_path=manifest_path,
            corpus_dir=corpus_dir,
            encoder=FakeEncoder(),
            embedding_model="candidate-v1",
        )
        document = session.scalar(select(ComplianceDocument))
        chunks = session.scalars(select(ComplianceChunk)).all()

        assert summary.indexed_files == ("sample.txt",)
        assert summary.chunk_count == 1
        assert document is not None
        assert document.content_sha256 == source_hash
        assert chunks[0].embedding_model == "candidate-v1"
        assert chunks[0].embedding == [1.0, 0.0]
        assert chunks[0].section == "1"

    engine.dispose()


def test_indexer_repairs_missing_chunks_and_null_embeddings_without_duplicates(
    tmp_path: Path,
):
    corpus_dir = tmp_path / "data"
    corpus_dir.mkdir()
    source_path = corpus_dir / "sample.txt"
    source_text = "Section 1. Procedure\n" + ("Follow the published steps. " * 80)
    source_path.write_text(source_text, encoding="utf-8")
    source_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
    manifest_path = tmp_path / "corpus_manifest.md"
    manifest_path.write_text(
        """| file | title | issuing_body | document_type | source_url | effective_date | consolidation_date | retrieved_at | content_sha256 | scope_note | is_active |
|---|---|---|---|---|---|---|---|---|---|---|
| `sample.txt` | Sample Guide | FBR | guide | <https://example.test/source> | 2026-06-30 |  | 2026-10-04 | `"""
        + source_hash
        + "` | Procedure only. | true |\n",
        encoding="utf-8",
    )
    engine = create_engine("sqlite://", poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        index_corpus(
            session,
            manifest_path=manifest_path,
            corpus_dir=corpus_dir,
            encoder=FakeEncoder(),
            embedding_model="candidate-v1",
        )
        document = session.scalar(select(ComplianceDocument))
        chunks = session.scalars(select(ComplianceChunk)).all()
        assert document is not None
        assert len(chunks) >= 2

        # Simulate a prior interrupted/partial index: one vector is missing and
        # one expected chunk was never persisted.
        chunks[0].embedding = None
        session.delete(chunks[-1])
        session.commit()

        repaired = index_corpus(
            session,
            manifest_path=manifest_path,
            corpus_dir=corpus_dir,
            encoder=FakeEncoder(),
            embedding_model="candidate-v1",
        )
        repaired_chunks = session.scalars(
            select(ComplianceChunk).where(ComplianceChunk.document_id == document.id)
        ).all()
        assert repaired.indexed_files == ("sample.txt",)
        assert repaired.chunk_count == 2
        assert len(repaired_chunks) == len(chunks)
        assert all(chunk.embedding == [1.0, 0.0] for chunk in repaired_chunks)

        repeated = index_corpus(
            session,
            manifest_path=manifest_path,
            corpus_dir=corpus_dir,
            encoder=FakeEncoder(),
            embedding_model="candidate-v1",
        )
        assert repeated.indexed_files == ()
        assert len(session.scalars(select(ComplianceChunk)).all()) == len(chunks)

    engine.dispose()
