from collections.abc import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.database import get_db
from app.models import Base, User
from app.security import create_access_token
from app.services.compliance_assistant import (
    ComplianceAnswerResult,
    ComplianceServiceUnavailable,
    CitationResult,
)
from app.services.wiring import get_compliance_answer_service
from app.routes.compliance import router


class FakeComplianceService:
    def __init__(self):
        self.calls = []
        self.failure = None

    def ask(self, session, *, user_id, question):
        self.calls.append((user_id, question))
        if self.failure is not None:
            raise self.failure
        return ComplianceAnswerResult(
            query_id=1,
            outcome="answered",
            answer="A supported procedure.",
            message=None,
            abstention_reason=None,
            citations=(
                CitationResult(
                    chunk_id="chunk-1",
                    document_title="Sample Act",
                    issuing_body="SECP",
                    source_url="https://example.test/source",
                    section="1",
                    page_number=2,
                    effective_date="2026-06-30",
                    consolidation_date=None,
                    retrieved_at=None,
                ),
            ),
        )


@pytest.fixture
def client_and_service():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        founder = User(
            email="founder@example.test",
            full_name="Founder",
            hashed_password="unused",
            role="founder",
        )
        mentor = User(
            email="mentor@example.test",
            full_name="Mentor",
            hashed_password="unused",
            role="mentor",
        )
        session.add_all([founder, mentor])
        session.commit()
        session.refresh(founder)
        session.refresh(mentor)
        founder_id = founder.id
        mentor_id = mentor.id

    service = FakeComplianceService()
    app = FastAPI()
    app.include_router(router)

    def override_db() -> Generator[Session, None, None]:
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[get_compliance_answer_service] = lambda: service
    with TestClient(app) as client:
        yield client, service, founder_id, mentor_id
    engine.dispose()


def test_compliance_questions_require_a_token(client_and_service):
    client, _, _, _ = client_and_service

    response = client.post("/api/v1/compliance/questions", json={"question": "What is the procedure?"})

    assert response.status_code == 401


def test_only_founders_can_submit_compliance_questions(client_and_service):
    client, service, _, mentor_id = client_and_service
    token = create_access_token(subject=str(mentor_id), role="mentor")

    response = client.post(
        "/api/v1/compliance/questions",
        json={"question": "What is the procedure?"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403
    assert service.calls == []


def test_founder_question_returns_structured_answer_and_citations(client_and_service):
    client, service, founder_id, _ = client_and_service
    token = create_access_token(subject=str(founder_id), role="founder")

    response = client.post(
        "/api/v1/compliance/questions",
        json={"question": "  What is the procedure?  "},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["outcome"] == "answered"
    assert payload["citations"][0]["document_title"] == "Sample Act"
    assert payload["informational_notice"] == "This information is not legal or tax advice."
    assert service.calls == [(founder_id, "What is the procedure?")]


def test_provider_failure_returns_generic_503_without_internal_details(client_and_service):
    client, service, founder_id, _ = client_and_service
    service.failure = ComplianceServiceUnavailable("private provider traceback detail")
    token = create_access_token(subject=str(founder_id), role="founder")

    response = client.post(
        "/api/v1/compliance/questions",
        json={"question": "What is the procedure?"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 503
    assert response.json() == {"detail": "Compliance assistant is temporarily unavailable"}
    assert "private provider traceback detail" not in response.text
