from sqlalchemy import func, select
from fastapi.testclient import TestClient

from app.feature_models import (
    ProfileVerification,
    ProfileReport,
    VerificationAppeal,
    VerificationDecision,
    VerificationSignal,
)
from app.main import app
from app.models import User
from app.services.feature_ai import get_encoder, get_gateway
from app.services.portfolio_verification import get_portfolio_fetcher
from conftest import TestSessionLocal


client = TestClient(app)


class FakeEncoder:
    model_name = "test-encoder"

    def encode(self, texts):
        return [[0.1, 0.2, 0.3] for _ in texts]


class FakePortfolioFetcher:
    def __init__(self, content="A product site for the fintech company described in the profile."):
        self.content = content

    def fetch(self, _url):
        return self.content


class FakeGateway:
    def __init__(self, result):
        self.result = result

    def generate_structured(self, **_kwargs):
        from app.verification_schemas import PortfolioLinkAssessment

        return PortfolioLinkAssessment.model_validate(self.result)


def setup_function():
    app.dependency_overrides[get_encoder] = FakeEncoder


def teardown_function():
    app.dependency_overrides.pop(get_encoder, None)
    app.dependency_overrides.pop(get_gateway, None)
    app.dependency_overrides.pop(get_portfolio_fetcher, None)


def create_user(email, role):
    created = client.post(f"/api/v1/auth/register/{role}", json={
        "email": email,
        "password": "SecurePass123!",
        "full_name": role.title(),
        "consent_accepted": True,
    })
    assert created.status_code == 201, created.text
    token = client.post("/api/v1/auth/login", json={
        "email": email,
        "password": "SecurePass123!",
    })
    assert token.status_code == 200, token.text
    return {"Authorization": f"Bearer {token.json()['access_token']}"}


def create_admin(email="admin-review@example.com"):
    create_user(email, "mentor")
    with TestSessionLocal() as session:
        user = session.scalar(select(User).where(User.email == email))
        user.role = "admin"
        session.commit()
    return create_user_token(email)


def create_user_token(email):
    token = client.post("/api/v1/auth/login", json={
        "email": email,
        "password": "SecurePass123!",
    })
    assert token.status_code == 200, token.text
    return {"Authorization": f"Bearer {token.json()['access_token']}"}


def create_match_profile(headers):
    response = client.put("/api/v1/matching/me/profile", headers=headers, json={
        "consent_accepted": True,
        "sector": "fintech",
        "stages": ["mvp"],
        "skills": ["strategy"],
        "availability": "open",
        "location": "Lahore",
        "summary": "Mentor in fintech product strategy with startup experience.",
    })
    assert response.status_code == 200, response.text


def submit_verification(headers, result="consistent"):
    app.dependency_overrides[get_portfolio_fetcher] = lambda: FakePortfolioFetcher()
    app.dependency_overrides[get_gateway] = lambda: FakeGateway({
        "result": result,
        "reason": "The page describes the submitted profile." if result == "consistent" else "The page contradicts the submitted profile.",
    })
    response = client.post("/api/v1/verification/me", headers=headers, json={
        "processing_consent_accepted": True,
        "trust_notice_accepted": True,
        "portfolio_url": "https://example.org/product",
        "secp_entity_name": "Example Technologies (Private) Limited",
        "secp_registration_number": "0123456",
    })
    assert response.status_code == 201, response.text
    return response.json()


def test_admin_queue_is_admin_only_and_contains_signals_without_contact_details():
    user_headers = create_user("queue-investor@example.com", "investor")
    create_match_profile(user_headers)
    verification = submit_verification(user_headers)

    appealed_headers = create_user("appealed-investor@example.com", "investor")
    create_match_profile(appealed_headers)
    appealed_verification = submit_verification(appealed_headers, result="inconsistent")
    appeal = client.post("/api/v1/verification/me/appeals", headers=appealed_headers, json={
        "reason": "The linked page is for our older product name.",
        "added_evidence": "The reviewer can compare this with the current product page.",
    })
    assert appeal.status_code == 201, appeal.text

    assert client.get("/api/v1/admin/verification/review-queue", headers=user_headers).status_code == 403
    assert client.get("/api/v1/admin/verification/review-queue").status_code == 401

    admin_headers = create_admin()
    response = client.get("/api/v1/admin/verification/review-queue", headers=admin_headers)
    assert response.status_code == 200, response.text
    items = response.json()
    assert {item["status"] for item in items} >= {"pending_review", "appeal_pending"}
    item = next(item for item in items if item["verification_id"] == verification["id"])
    assert item["score"] == verification["score"]
    assert item["signals"]["secp_cross_check"] == "pending_manual_review"
    assert len(item["signal_details"]) == 5
    assert all({"signal_name", "score", "outcome", "input_snapshot", "reason"} <= signal.keys()
               for signal in item["signal_details"])
    assert item["appeal"] is None
    assert item["report_count"] == 0
    appealed_item = next(item for item in items if item["verification_id"] == appealed_verification["id"])
    assert appealed_item["appeal"]["added_evidence"] == "The reviewer can compare this with the current product page."
    assert not {"email", "full_name", "phone", "contact_email"}.intersection(item)


def test_admin_approves_appeal_records_reviewer_and_makes_status_visible():
    user_headers = create_user("appeal-investor@example.com", "investor")
    create_match_profile(user_headers)
    verification = submit_verification(user_headers, result="inconsistent")
    appeal = client.post("/api/v1/verification/me/appeals", headers=user_headers, json={
        "reason": "The linked page is for our older product name.",
        "added_evidence": "The reviewer can compare this with the current product page.",
    })
    assert appeal.status_code == 201, appeal.text
    admin_headers = create_admin("appeal-admin@example.com")
    queue = client.get("/api/v1/admin/verification/review-queue", headers=admin_headers)
    assert queue.status_code == 200, queue.text
    queued = next(item for item in queue.json() if item["verification_id"] == verification["id"])
    assert queued["status"] == "appeal_pending"
    assert queued["appeal"]["added_evidence"] == "The reviewer can compare this with the current product page."

    decision = client.post(
        f"/api/v1/admin/verification/{verification['id']}/decision",
        headers=admin_headers,
        json={"decision": "approve", "reason": "The appeal evidence resolves the profile concern."},
    )
    assert decision.status_code == 200, decision.text
    assert decision.json()["status"] == "verified"
    assert client.get("/api/v1/verification/me", headers=user_headers).json()["status"] == "verified"

    with TestSessionLocal() as session:
        saved_appeal = session.scalar(select(VerificationAppeal))
        saved_decision = session.scalar(
            select(VerificationDecision).where(VerificationDecision.decision == "verified")
        )
        admin = session.scalar(select(User).where(User.email == "appeal-admin@example.com"))
        assert saved_appeal.status == "approved"
        assert saved_appeal.reviewed_by == admin.id
        assert saved_appeal.reviewed_at is not None
        assert saved_appeal.decision_reason == "The appeal evidence resolves the profile concern."
        assert saved_decision.reviewer_user_id == admin.id
        assert saved_decision.reason == "The appeal evidence resolves the profile concern."
        assert saved_decision.created_at is not None
    second_appeal = client.post("/api/v1/verification/me/appeals", headers=user_headers, json={
        "reason": "I want to submit another appeal.",
        "added_evidence": "Here is more evidence for another review.",
    })
    assert second_appeal.status_code == 409


def test_admin_requires_nonblank_reason_and_rejects_forbidden_second_transition():
    user_headers = create_user("decision-investor@example.com", "investor")
    create_match_profile(user_headers)
    verification = submit_verification(user_headers)
    admin_headers = create_admin("decision-admin@example.com")

    no_token = client.post(
        f"/api/v1/admin/verification/{verification['id']}/decision",
        json={"decision": "approve", "reason": "The reviewer confirmed this profile."},
    )
    assert no_token.status_code == 401
    non_admin = client.post(
        f"/api/v1/admin/verification/{verification['id']}/decision",
        headers=user_headers,
        json={"decision": "approve", "reason": "The reviewer confirmed this profile."},
    )
    assert non_admin.status_code == 403

    missing_reason = client.post(
        f"/api/v1/admin/verification/{verification['id']}/decision",
        headers=admin_headers,
        json={"decision": "approve"},
    )
    assert missing_reason.status_code == 422
    empty_reason = client.post(
        f"/api/v1/admin/verification/{verification['id']}/decision",
        headers=admin_headers,
        json={"decision": "approve", "reason": ""},
    )
    assert empty_reason.status_code == 422
    whitespace_reason = client.post(
        f"/api/v1/admin/verification/{verification['id']}/decision",
        headers=admin_headers,
        json={"decision": "approve", "reason": "   "},
    )
    assert whitespace_reason.status_code == 422

    approved = client.post(
        f"/api/v1/admin/verification/{verification['id']}/decision",
        headers=admin_headers,
        json={"decision": "approve", "reason": "The reviewer confirmed the submitted identity evidence."},
    )
    assert approved.status_code == 200, approved.text
    assert approved.json()["reason"] == "The reviewer confirmed the submitted identity evidence."
    second_decision = client.post(
        f"/api/v1/admin/verification/{verification['id']}/decision",
        headers=admin_headers,
        json={"decision": "reject", "reason": "A second final decision is not allowed."},
    )
    assert second_decision.status_code == 409
    with TestSessionLocal() as session:
        reviewer = session.scalar(select(User).where(User.email == "decision-admin@example.com"))
        saved_decision = session.scalar(
            select(VerificationDecision).where(
                VerificationDecision.verification_id == verification["id"],
                VerificationDecision.decision == "verified",
            )
        )
        assert saved_decision.reviewer_user_id == reviewer.id
        assert saved_decision.reason == "The reviewer confirmed the submitted identity evidence."


def test_admin_rejection_is_final_and_records_reviewer_reason():
    user_headers = create_user("reject-investor@example.com", "investor")
    create_match_profile(user_headers)
    verification = submit_verification(user_headers)
    assert verification["band"] == "review"
    admin_headers = create_admin("reject-admin@example.com")

    decision = client.post(
        f"/api/v1/admin/verification/{verification['id']}/decision",
        headers=admin_headers,
        json={"decision": "reject", "reason": "No."},
    )

    assert decision.status_code == 200, decision.text
    assert decision.json()["status"] == "rejected"
    assert decision.json()["reason"] == "No."
    assert client.get("/api/v1/verification/me", headers=user_headers).json()["reason"] == "No."
    assert client.post("/api/v1/verification/me/appeals", headers=user_headers, json={
        "reason": "A reviewer should reconsider this decision.",
        "added_evidence": "Additional records are available for a review.",
    }).status_code == 409
    with TestSessionLocal() as session:
        reviewer = session.scalar(select(User).where(User.email == "reject-admin@example.com"))
        saved_decision = session.scalar(
            select(VerificationDecision).where(
                VerificationDecision.verification_id == verification["id"],
                VerificationDecision.decision == "rejected",
            )
        )
        assert saved_decision.reviewer_user_id == reviewer.id
        assert saved_decision.reason == "No."
        assert session.scalar(
            select(func.count(VerificationAppeal.id)).where(
                VerificationAppeal.verification_id == verification["id"]
            )
        ) == 0


def test_denied_appeal_is_final_and_cannot_be_appealed_again():
    user_headers = create_user("denied-appeal-investor@example.com", "investor")
    create_match_profile(user_headers)
    verification = submit_verification(user_headers, result="inconsistent")
    first_appeal = client.post("/api/v1/verification/me/appeals", headers=user_headers, json={
        "reason": "The product page has since been corrected.",
        "added_evidence": "The prior version is archived for review.",
    })
    assert first_appeal.status_code == 201, first_appeal.text
    admin_headers = create_admin("denied-appeal-admin@example.com")

    decision = client.post(
        f"/api/v1/admin/verification/{verification['id']}/decision",
        headers=admin_headers,
        json={"decision": "reject", "reason": "The submitted evidence does not resolve the mismatch."},
    )

    assert decision.status_code == 200, decision.text
    assert decision.json()["status"] == "rejected"
    assert decision.json()["reason"] == "The submitted evidence does not resolve the mismatch."
    assert client.get("/api/v1/verification/me", headers=user_headers).json()["status"] == "rejected"
    second_appeal = client.post("/api/v1/verification/me/appeals", headers=user_headers, json={
        "reason": "I want to submit another appeal.",
        "added_evidence": "Here is further evidence for another review.",
    })
    assert second_appeal.status_code == 409
    with TestSessionLocal() as session:
        saved_appeal = session.scalar(select(VerificationAppeal))
        reviewer = session.scalar(select(User).where(User.email == "denied-appeal-admin@example.com"))
        assert saved_appeal.status == "rejected"
        assert saved_appeal.reviewed_by == reviewer.id
        assert saved_appeal.reviewed_at is not None
        assert saved_appeal.decision_reason == "The submitted evidence does not resolve the mismatch."


def test_reported_profile_returns_to_queue_with_score_locked():
    target_headers = create_user("reported-investor@example.com", "investor")
    create_match_profile(target_headers)
    verification = submit_verification(target_headers)
    reporter_headers = create_user("reporter-founder@example.com", "founder")
    report = client.post(
        f"/api/v1/verification/profiles/{verification['user_id']}/reports",
        headers=reporter_headers,
        json={"reason": "The profile details need a human review."},
    )
    assert report.status_code == 201, report.text

    # Editing the profile after the report must not trigger a new score.
    create_match_profile(target_headers)
    admin_headers = create_admin("reported-admin@example.com")
    response = client.get("/api/v1/admin/verification/review-queue", headers=admin_headers)
    assert response.status_code == 200, response.text
    item = next(item for item in response.json() if item["verification_id"] == verification["id"])
    assert item["status"] == "pending_review"
    assert item["report_count"] == 1
    with TestSessionLocal() as session:
        saved = session.get(ProfileVerification, verification["id"])
        assert saved.rescore_locked is True
        assert saved.score == verification["score"]
        assert saved.signals == verification["signals"]
        assert session.scalar(
            select(func.count(VerificationSignal.id)).where(
                VerificationSignal.verification_id == verification["id"]
            )
        ) == 5
        assert session.scalar(
            select(func.count(ProfileReport.id)).where(ProfileReport.target_user_id == verification["user_id"])
        ) == 1
