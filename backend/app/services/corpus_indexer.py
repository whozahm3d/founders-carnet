"""Verify, chunk, embed, and persist whitelisted corpus sources (FR-8, NFR-12, NFR-14, NFR-20)."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import SessionLocal
from app.models import ComplianceChunk, ComplianceDocument
from rag.compliance.chunking import CitationChunk, chunk_pages
from rag.compliance.documents import ExtractedPage, NoExtractableTextError, extract_pdf_pages
from rag.compliance.embeddings import SentenceTransformerEncoder
from rag.compliance.ingestion import CorpusDocument, parse_manifest, verify_corpus_file
from rag.compliance.scoping import apply_corpus_scope


_SCOPE_EXCLUSIONS = {
    "PSEB Industry Facilitation page.pdf": (
        "Superseded by the dated PSEB HTML snapshot; this PDF is retained for provenance only."
    ),
}


class IndexConflictError(RuntimeError):
    """Raised rather than silently replacing an already-indexed source."""


@dataclass(frozen=True, slots=True)
class IndexSummary:
    indexed_files: tuple[str, ...]
    skipped_files: dict[str, str]
    chunk_count: int


def index_corpus(
    session: Session,
    *,
    manifest_path: Path,
    corpus_dir: Path,
    encoder: SentenceTransformerEncoder,
    embedding_model: str,
    batch_size: int = 32,
) -> IndexSummary:
    """Index only verified, text-extractable sources whose scope is enforced."""
    if batch_size < 1:
        raise ValueError("batch_size must be positive")
    if not embedding_model.strip():
        raise ValueError("embedding_model must not be empty")

    documents = parse_manifest(manifest_path.read_text(encoding="utf-8"))
    paths = {document.file: corpus_dir / document.file for document in documents}
    for document in documents:
        verify_corpus_file(paths[document.file], document.content_sha256)

    indexed_files: list[str] = []
    skipped_files: dict[str, str] = {}
    total_chunks = 0

    try:
        for document in documents:
            if not document.is_active:
                skipped_files[document.file] = "Document is inactive in the manifest."
                continue
            if document.file in _SCOPE_EXCLUSIONS:
                skipped_files[document.file] = _SCOPE_EXCLUSIONS[document.file]
                continue
            if _is_duplicate_html(document, documents):
                skipped_files[document.file] = "The text snapshot for this source is indexed instead."
                continue

            try:
                pages = _read_pages(paths[document.file])
            except NoExtractableTextError as exc:
                skipped_files[document.file] = str(exc)
                continue

            pages = apply_corpus_scope(document, pages)
            chunks = chunk_pages(document, pages)
            if not chunks:
                skipped_files[document.file] = "Source contains no extractable text."
                continue

            existing = session.scalar(
                select(ComplianceDocument).where(
                    ComplianceDocument.file_name == document.file
                )
            )
            if existing is None:
                indexed_document = _document_model(document)
                session.add(indexed_document)
                session.flush()
                chunks_to_encode = list(chunks)
                existing_chunks: dict[str, ComplianceChunk] = {}
            else:
                if existing.content_sha256 != document.content_sha256:
                    raise IndexConflictError(
                        f"{document.file} is already indexed with a different source hash"
                    )
                indexed_document = existing
                stored_chunks = session.scalars(
                    select(ComplianceChunk).where(
                        ComplianceChunk.document_id == existing.id
                    )
                ).all()
                existing_chunks = {chunk.chunk_id: chunk for chunk in stored_chunks}
                expected_by_id = {chunk.chunk_id: chunk for chunk in chunks}
                if set(existing_chunks) - set(expected_by_id):
                    raise IndexConflictError(
                        f"{document.file} has stored chunks absent from the verified source"
                    )
                for chunk_id, stored in existing_chunks.items():
                    expected = expected_by_id[chunk_id]
                    if (
                        stored.page_number != expected.page_number
                        or stored.section != expected.section
                        or stored.text != expected.text
                    ):
                        raise IndexConflictError(
                            f"{document.file} has stored content that differs from its source"
                        )
                chunks_to_encode = [
                    chunk
                    for chunk in chunks
                    if chunk.chunk_id not in existing_chunks
                    or existing_chunks[chunk.chunk_id].embedding is None
                    or existing_chunks[chunk.chunk_id].embedding_model != embedding_model
                ]

            if not chunks_to_encode:
                skipped_files[document.file] = "Source hash, chunks, and embeddings are already indexed."
                continue

            vectors = _encode_chunks(encoder, chunks_to_encode, batch_size)
            for chunk, vector in zip(chunks_to_encode, vectors, strict=True):
                stored = existing_chunks.get(chunk.chunk_id)
                if stored is None:
                    session.add_all(
                        _chunk_models(indexed_document.id, [chunk], [vector], embedding_model)
                    )
                else:
                    stored.embedding = list(vector)
                    stored.embedding_model = embedding_model
            indexed_files.append(document.file)
            total_chunks += len(chunks_to_encode)

        session.commit()
    except Exception:
        session.rollback()
        raise

    return IndexSummary(
        indexed_files=tuple(indexed_files),
        skipped_files=skipped_files,
        chunk_count=total_chunks,
    )


def _read_pages(path: Path) -> tuple[ExtractedPage, ...]:
    if path.suffix.lower() == ".pdf":
        return extract_pdf_pages(path)
    if path.suffix.lower() == ".txt":
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            raise NoExtractableTextError(f"No text in {path.name}")
        return (ExtractedPage(page_number=1, text=text),)
    raise NoExtractableTextError(f"Unsupported corpus format: {path.suffix}")


def _is_duplicate_html(document: CorpusDocument, documents: Sequence[CorpusDocument]) -> bool:
    return document.file.lower().endswith(".html") and any(
        other.source_url == document.source_url and other.file.lower().endswith(".txt")
        for other in documents
    )


def _encode_chunks(
    encoder: SentenceTransformerEncoder,
    chunks: Sequence[CitationChunk],
    batch_size: int,
) -> tuple[tuple[float, ...], ...]:
    vectors: list[tuple[float, ...]] = []
    expected_dimensions: int | None = None
    for start in range(0, len(chunks), batch_size):
        batch = chunks[start : start + batch_size]
        batch_vectors = encoder.encode([chunk.text for chunk in batch])
        if len(batch_vectors) != len(batch):
            raise ValueError("Embedding count does not match chunk count")
        for vector in batch_vectors:
            normalized = tuple(float(value) for value in vector)
            if not normalized:
                raise ValueError("Embedding vectors must not be empty")
            if expected_dimensions is None:
                expected_dimensions = len(normalized)
            elif len(normalized) != expected_dimensions:
                raise ValueError("Embedding dimensions are inconsistent")
            vectors.append(normalized)
    return tuple(vectors)


def _document_model(source: CorpusDocument) -> ComplianceDocument:
    return ComplianceDocument(
        file_name=source.file,
        title=source.title,
        issuing_body=source.issuing_body,
        document_type=source.document_type,
        source_url=source.source_url,
        effective_date=source.effective_date,
        consolidation_date=source.consolidation_date,
        retrieved_at=source.retrieved_at,
        content_sha256=source.content_sha256,
        scope_note=source.scope_note,
        is_active=source.is_active,
    )


def _chunk_models(
    document_id: int,
    chunks: Sequence[CitationChunk],
    vectors: Sequence[Sequence[float]],
    embedding_model: str,
) -> list[ComplianceChunk]:
    return [
        ComplianceChunk(
            document_id=document_id,
            chunk_id=chunk.chunk_id,
            page_number=chunk.page_number,
            section=chunk.section,
            text=chunk.text,
            embedding=list(vector),
            embedding_model=embedding_model,
        )
        for chunk, vector in zip(chunks, vectors, strict=True)
    ]


def main() -> None:
    settings = get_settings()
    if not settings.embedding_model_name:
        raise SystemExit("Configure EMBEDDING_MODEL_NAME before indexing the corpus")

    repository_root = Path(__file__).resolve().parents[3]
    with SessionLocal() as session:
        summary = index_corpus(
            session,
            manifest_path=repository_root / "rag" / "corpus_manifest.md",
            corpus_dir=repository_root / "rag" / "data",
            encoder=SentenceTransformerEncoder(settings.embedding_model_name),
            embedding_model=settings.embedding_model_name,
        )

    print(f"Indexed {len(summary.indexed_files)} documents and {summary.chunk_count} chunks")
    for file_name, reason in summary.skipped_files.items():
        print(f"Skipped {file_name}: {reason}")


if __name__ == "__main__":
    main()
