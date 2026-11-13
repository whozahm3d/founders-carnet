import logging

import pytest
from google.genai.errors import ServerError
from sqlalchemy import create_engine, event, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.models import Base, ComplianceChunk, ComplianceDocument, ComplianceQuery, User
from app.services.compliance_assistant import (
    AnswerDraft,
    ComplianceAnswerService,
    ComplianceServiceUnavailable,
    GroundingValidation,
)
from app.services.llm_gateway import GeminiGateway


class FakeEncoder:
    def __init__(self, vector=(1.0, 0.0)):
        self.calls = 0
        self.vector = vector

    def encode(self, texts):
        self.calls += 1
        return (self.vector,)


class FakeGateway:
    prompt_version = "compliance-answer-test-v1"

    def __init__(
        self,
        *,
        citation_id="source:1:0",
        supported=True,
        answer="The cited source describes this procedure.",
    ):
        self.citation_id = citation_id
        self.supported = supported
        self.answer = answer
        self.generation_calls = 0
        self.validation_calls = 0

    def generate_answer(self, question, passages):
        self.generation_calls += 1
        return AnswerDraft(
            answer=self.answer,
            citation_chunk_ids=[self.citation_id] if self.citation_id else [],
        )

    def validate_answer(self, question, answer, passages):
        self.validation_calls += 1
        return GroundingValidation(is_supported=self.supported)


def _database(
    *,
    file_name="sample.pdf",
    document_title="Sample Act",
    document_text="The source describes a procedure.",
    source_url="https://example.test/source",
    effective_date="2026-06-30",
):
    engine = create_engine("sqlite://", poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)
    session = Session(engine)
    fake_password_hash = "not-a-real-password-hash"
    user = User(
        email="founder@example.test",
        full_name="Test Founder",
        hashed_password=fake_password_hash,
        role="founder",
    )
    document = ComplianceDocument(
        file_name=file_name,
        title=document_title,
        issuing_body="SECP",
        document_type="statute",
        source_url=source_url,
        effective_date=effective_date,
        consolidation_date=None,
        retrieved_at=None,
        content_sha256="a" * 64,
        scope_note="Test source.",
        is_active=True,
    )
    session.add_all([user, document])
    session.flush()
    chunk = ComplianceChunk(
        document=document,
        chunk_id="source:1:0",
        page_number=1,
        section="1",
        text=document_text,
        embedding=[1.0, 0.0],
        embedding_model="candidate-v1",
    )
    session.add(chunk)
    session.commit()
    return engine, session, user


def test_supported_answer_is_saved_with_its_citation():
    engine, session, user = _database()
    encoder = FakeEncoder()
    gateway = FakeGateway()
    assistant = ComplianceAnswerService(
        encoder=encoder,
        gateway=gateway,
        embedding_model="candidate-v1",
        minimum_similarity=0.8,
    )

    result = assistant.ask(
        session, user_id=user.id, question="What does the source say?"
    )

    saved_query = session.scalar(select(ComplianceQuery))
    assert result.outcome == "answered"
    assert result.answer == "The cited source describes this procedure."
    assert result.citations[0].document_title == "Sample Act"
    assert result.citations[0].effective_date == "2026-06-30"
    assert saved_query is not None
    assert saved_query.outcome == "answered"
    assert saved_query.prompt_version == gateway.prompt_version
    assert encoder.calls == 1
    assert gateway.generation_calls == 1
    assert gateway.validation_calls == 1
    engine.dispose()


def test_case_specific_license_question_abstains_before_embedding_or_generation():
    engine, session, user = _database()
    encoder = FakeEncoder()
    gateway = FakeGateway()
    assistant = ComplianceAnswerService(
        encoder=encoder,
        gateway=gateway,
        embedding_model="candidate-v1",
    )

    result = assistant.ask(
        session,
        user_id=user.id,
        question="Does my startup need a license from SECP?",
    )

    assert result.outcome == "abstained"
    assert result.abstention_reason == "case_specific_advice"
    assert result.citations == ()
    assert encoder.calls == 0
    assert gateway.generation_calls == 0
    engine.dispose()


def test_invalid_citation_or_failed_grounding_validation_abstains():
    for gateway in (
        FakeGateway(citation_id="not-retrieved"),
        FakeGateway(supported=False),
    ):
        engine, session, user = _database()
        assistant = ComplianceAnswerService(
            encoder=FakeEncoder(),
            gateway=gateway,
            embedding_model="candidate-v1",
            minimum_similarity=0.8,
        )

        result = assistant.ask(
            session, user_id=user.id, question="What procedure is described?"
        )

        assert result.outcome == "abstained"
        assert result.answer is None
        assert result.citations == ()
        engine.dispose()


def test_retrieval_below_threshold_abstains_without_calling_gateway():
    engine, session, user = _database()
    encoder = FakeEncoder(vector=(0.0, 1.0))
    gateway = FakeGateway()
    assistant = ComplianceAnswerService(
        encoder=encoder,
        gateway=gateway,
        embedding_model="candidate-v1",
        minimum_similarity=0.8,
    )

    result = assistant.ask(session, user_id=user.id, question="Unrelated question?")

    assert result.outcome == "abstained"
    assert result.abstention_reason == "no_supporting_passage"
    assert gateway.generation_calls == 0
    engine.dispose()


def test_empty_structured_answer_is_recorded_as_abstention():
    engine, session, user = _database()
    gateway = FakeGateway(answer="", citation_id="")
    assistant = ComplianceAnswerService(
        encoder=FakeEncoder(),
        gateway=gateway,
        embedding_model="candidate-v1",
    )

    result = assistant.ask(session, user_id=user.id, question="Question with evidence?")

    assert result.outcome == "abstained"
    assert result.abstention_reason == "model_abstained"
    assert result.answer is None
    engine.dispose()


def test_unrelated_question_with_no_indexed_corpus_is_saved_as_abstention(caplog):
    engine, session, user = _database()
    session.query(ComplianceChunk).delete()
    session.query(ComplianceDocument).delete()
    session.commit()
    gateway = FakeGateway()
    assistant = ComplianceAnswerService(
        encoder=FakeEncoder(),
        gateway=gateway,
        embedding_model="candidate-v1",
        minimum_similarity=0.8,
    )

    with caplog.at_level(logging.INFO, logger="app.services.compliance_assistant"):
        result = assistant.ask(
            session, user_id=user.id, question="Give me random startup ideas"
        )

    saved_query = session.scalar(select(ComplianceQuery))
    assert result.outcome == "abstained"
    assert result.abstention_reason == "no_supporting_passage"
    assert saved_query is not None and saved_query.outcome == "abstained"
    assert result.outcome == "abstained"
    assert result.message == "I do not have a supported answer in the indexed corpus."
    assert result.citations == ()
    assert result.query_id == saved_query.id
    assert gateway.validation_calls == 0
    assert gateway.generation_calls == 0
    assert assistant.encoder.calls == 0
    index_log = next(
        record
        for record in caplog.records
        if record.getMessage() == "Compliance retrieval index state"
    )
    retrieval_log = next(
        record
        for record in caplog.records
        if record.getMessage() == "Compliance retrieval completed"
    )
    assert index_log.document_count == 0
    assert index_log.active_document_count == 0
    assert index_log.active_chunk_count == 0
    assert index_log.embedded_chunk_count == 0
    assert index_log.compatible_chunk_count == 0
    assert retrieval_log.retrieved_passage_count == 0
    assert "random startup ideas" not in caplog.text
    engine.dispose()


def test_what_is_secp_retrieves_manifested_position_paper_and_logs_counts(caplog):
    # Exact cover-page excerpt from the manifest-listed SECP position paper.
    source_excerpt = (
        "POSITION PAPER www.secp.gov.pk SECURITIES AND EXCHANGE COMMISSION OF PAKISTAN "
        "HOLISTIC FRAMEWORK FOR BUILDING A SUPPORTIVE START-UP ECOSYSTEM IN PAKISTAN"
    )
    engine, session, user = _database(
        file_name="Start-up ecosystem position paper, 30 Oct 2024 (SECP).pdf",
        document_title="Start-up ecosystem position paper",
        document_text=source_excerpt,
        source_url="https://www.secp.gov.pk/document/rsb-position-paper/",
        effective_date="2024-10-30",
    )
    assistant = ComplianceAnswerService(
        encoder=FakeEncoder(),
        gateway=FakeGateway(
            answer="SECP is the Securities and Exchange Commission of Pakistan."
        ),
        embedding_model="candidate-v1",
        minimum_similarity=0.4,
    )

    with caplog.at_level(logging.INFO, logger="app.services.compliance_assistant"):
        result = assistant.ask(session, user_id=user.id, question="What is SECP?")

    assert result.outcome == "answered"
    assert (
        result.answer == "SECP is the Securities and Exchange Commission of Pakistan."
    )
    assert result.citations[0].document_title == "Start-up ecosystem position paper"
    assert result.citations[0].effective_date == "2024-10-30"
    index_log = next(
        record
        for record in caplog.records
        if record.getMessage() == "Compliance retrieval index state"
    )
    retrieval_log = next(
        record
        for record in caplog.records
        if record.getMessage() == "Compliance retrieval completed"
    )
    assert index_log.active_document_count == 1
    assert index_log.document_count == 1
    assert index_log.active_chunk_count == 1
    assert index_log.embedded_chunk_count == 1
    assert index_log.compatible_chunk_count == 1
    assert retrieval_log.retrieved_passage_count == 1
    assert retrieval_log.top_similarity == 1.0
    assert "What is SECP?" not in caplog.text
    engine.dispose()


def test_retrieval_error_is_logged_and_failed_query_is_recorded(caplog):
    engine, session, user = _database()

    class FailingEncoder:
        def encode(self, texts):
            raise RuntimeError("embedding provider unavailable")

    assistant = ComplianceAnswerService(
        encoder=FailingEncoder(),
        gateway=FakeGateway(),
        embedding_model="candidate-v1",
    )

    with (
        caplog.at_level(logging.ERROR, logger="app.services.compliance_assistant"),
        pytest.raises(ComplianceServiceUnavailable) as caught,
    ):
        assistant.ask(session, user_id=user.id, question="What does the source say?")

    saved_query = session.scalar(select(ComplianceQuery))
    assert str(caught.value) == "Compliance retrieval failed"
    assert isinstance(caught.value.__cause__, RuntimeError)
    assert "Compliance retrieval failed" in caplog.text
    assert "Traceback (most recent call last)" in caplog.text
    assert "embedding provider unavailable" in caplog.text
    assert saved_query is not None and saved_query.outcome == "failed"
    engine.dispose()


def test_gemini_error_is_logged_and_failed_query_is_recorded(caplog):
    engine, session, user = _database()

    class FailingGateway(FakeGateway):
        def generate_answer(self, question, passages):
            raise RuntimeError("provider quota or network failure")

    assistant = ComplianceAnswerService(
        encoder=FakeEncoder(),
        gateway=FailingGateway(),
        embedding_model="candidate-v1",
        minimum_similarity=0.8,
    )

    with (
        caplog.at_level(logging.ERROR, logger="app.services.compliance_assistant"),
        pytest.raises(ComplianceServiceUnavailable) as caught,
    ):
        assistant.ask(session, user_id=user.id, question="What procedure is described?")

    saved_query = session.scalar(select(ComplianceQuery))
    assert str(caught.value) == "Compliance answer generation failed"
    assert isinstance(caught.value.__cause__, RuntimeError)
    assert "Compliance answer generation failed" in caplog.text
    assert "Traceback (most recent call last)" in caplog.text
    assert "provider quota or network failure" in caplog.text
    assert saved_query is not None and saved_query.outcome == "failed"
    engine.dispose()


def test_gateway_generation_failure_is_logged_once_and_failed_query_is_saved(caplog):
    engine, session, user = _database()

    class FailingModels:
        def generate_content(self, **kwargs):
            raise ServerError(
                code=504,
                response_json={
                    "error": {
                        "message": "Deadline expired before operation could complete.",
                        "status": "DEADLINE_EXCEEDED",
                    }
                },
            )

    gateway = GeminiGateway(
        api_key="test-key",
        model_name="configured-model",
        client=type("Client", (), {"models": FailingModels()})(),
    )
    assistant = ComplianceAnswerService(
        encoder=FakeEncoder(),
        gateway=gateway,
        embedding_model="candidate-v1",
        minimum_similarity=0.8,
    )

    with caplog.at_level(logging.ERROR), pytest.raises(ComplianceServiceUnavailable):
        assistant.ask(session, user_id=user.id, question="What does the source say?")

    saved_query = session.scalar(select(ComplianceQuery))
    assert saved_query is not None and saved_query.outcome == "failed"
    assert (
        sum(
            record.message.startswith("Gemini generation failed")
            for record in caplog.records
        )
        == 1
    )
    assert not any(
        record.message.startswith("Compliance answer generation failed")
        for record in caplog.records
    )
    assert sum(record.exc_info is not None for record in caplog.records) == 1
    engine.dispose()


def test_failed_query_write_does_not_mask_original_provider_error(caplog):
    engine, session, user = _database()

    class FailingEncoder:
        def encode(self, texts):
            raise RuntimeError("original embedding failure")

    def reject_failed_query(mapper, connection, target):
        if target.outcome == "failed":
            raise RuntimeError("query log database failure")

    event.listen(ComplianceQuery, "before_insert", reject_failed_query)
    assistant = ComplianceAnswerService(
        encoder=FailingEncoder(),
        gateway=FakeGateway(),
        embedding_model="candidate-v1",
    )

    try:
        with (
            caplog.at_level(logging.ERROR, logger="app.services.compliance_assistant"),
            pytest.raises(ComplianceServiceUnavailable) as caught,
        ):
            assistant.ask(
                session, user_id=user.id, question="What does the source say?"
            )
    finally:
        event.remove(ComplianceQuery, "before_insert", reject_failed_query)

    assert isinstance(caught.value.__cause__, RuntimeError)
    assert str(caught.value.__cause__) == "original embedding failure"
    assert "Could not record failed compliance query" in caplog.text
    session.rollback()
    engine.dispose()
