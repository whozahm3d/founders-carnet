import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.feature_ai import get_encoder, get_gateway
from app.services.portfolio_verification import get_portfolio_fetcher

client = TestClient(app)


class FakeEncoder:
    model_name = "test-encoder"

    def encode(self, texts):
        return [[0.1, 0.2, 0.3] for _ in texts]


def setup_function():
    app.dependency_overrides[get_encoder] = FakeEncoder


def teardown_function():
    app.dependency_overrides.pop(get_encoder, None)


class FakePortfolioFetcher:
    def fetch(self, _url):
        return "A product site for the fintech company described in the profile."


class FakeGateway:
    def __init__(self, result):
        self.result = result
        self.calls = 0

    def generate_structured(self, **_kwargs):
        from app.verification_schemas import PortfolioLinkAssessment

        self.calls += 1
        return PortfolioLinkAssessment.model_validate(self.result)


def create_user(email, role):
    created = client.post(
        f"/api/v1/auth/register/{role}",
        json={
            "email": email,
            "password": "SecurePass123!",
            "full_name": role.title(),
            "consent_accepted": True,
        },
    )
    assert created.status_code == 201, created.text
    token = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": "SecurePass123!",
        },
    )
    return {"Authorization": f"Bearer {token.json()['access_token']}"}


def create_match_profile(headers):
    response = client.put(
        "/api/v1/matching/me/profile",
        headers=headers,
        json={
            "consent_accepted": True,
            "sector": "fintech",
            "stages": ["mvp"],
            "skills": ["strategy"],
            "availability": "open",
            "location": "Lahore",
            "summary": "Mentor in fintech product strategy with startup experience.",
        },
    )
    assert response.status_code == 200, response.text


def submit_verification(headers):
    return client.post(
        "/api/v1/verification/me",
        headers=headers,
        json={
            "processing_consent_accepted": True,
            "trust_notice_accepted": True,
            "portfolio_url": "https://example.org/product",
            "secp_entity_name": "Example Technologies (Private) Limited",
            "secp_registration_number": "0123456",
        },
    )


def install_verification_fakes(portfolio_result):
    app.dependency_overrides[get_portfolio_fetcher] = lambda: FakePortfolioFetcher()
    app.dependency_overrides[get_gateway] = lambda: FakeGateway(portfolio_result)


def test_profile_flow_scores_saves_status_and_requires_manual_secp_review():
    install_verification_fakes(
        {
            "result": "consistent",
            "reason": "The page describes the stated fintech product.",
        }
    )
    headers = create_user("verify-investor@example.com", "investor")
    create_match_profile(headers)

    submitted = submit_verification(headers)
    assert submitted.status_code == 201, submitted.text
    body = submitted.json()
    assert body["band"] == "review"
    assert body["status"] == "pending_review"
    assert body["score"] == 0.6964
    assert body["signals"]["secp_cross_check"] == "pending_manual_review"
    assert body["signals"]["portfolio_link"] == "consistent"

    history = client.get("/api/v1/verification/me", headers=headers)
    assert history.status_code == 200
    assert history.json()["id"] == body["id"]

    appeal = client.post(
        "/api/v1/verification/me/appeals",
        headers=headers,
        json={
            "reason": "The registration number belongs to our parent company.",
            "added_evidence": "The official registration certificate is available to the reviewer.",
        },
    )
    assert appeal.status_code == 409


def test_auto_rejected_profile_can_appeal_once_and_report_locks_rescoring():
    install_verification_fakes(
        {"result": "inconsistent", "reason": "The page describes a different business."}
    )
    headers = create_user("verify-mentor@example.com", "mentor")
    create_match_profile(headers)
    submitted = submit_verification(headers)
    assert submitted.status_code == 201, submitted.text
    assert submitted.json()["status"] == "auto_rejected"

    appeal = client.post(
        "/api/v1/verification/me/appeals",
        headers=headers,
        json={
            "reason": "The linked page is for our older product name.",
            "added_evidence": "The reviewer can compare this with the current product page.",
        },
    )
    assert appeal.status_code == 201, appeal.text
    assert appeal.json()["status"] == "appeal_pending"
    assert (
        client.post(
            "/api/v1/verification/me/appeals",
            headers=headers,
            json={
                "reason": "Second appeal",
                "added_evidence": "Additional evidence",
            },
        ).status_code
        == 409
    )

    reporter = create_user("verify-reporter@example.com", "talent")
    reported = client.post(
        f"/api/v1/verification/profiles/{client.get('/api/v1/verification/me', headers=headers).json()['user_id']}/reports",
        headers=reporter,
        json={"reason": "Please review this profile evidence."},
    )
    assert reported.status_code == 201, reported.text
    assert reported.json()["status"] == "received"
    assert (
        client.get("/api/v1/verification/me", headers=headers).json()["status"]
        == "pending_review"
    )
    assert (
        client.post(
            "/api/v1/verification/me",
            headers=headers,
            json={
                "processing_consent_accepted": True,
                "trust_notice_accepted": True,
                "portfolio_url": "https://example.org/product",
                "secp_entity_name": "Example Technologies (Private) Limited",
                "secp_registration_number": "0123456",
            },
        ).status_code
        == 409
    )


def test_verification_requires_role_consent_profile_and_https_portfolio():
    install_verification_fakes(
        {"result": "consistent", "reason": "Relevant product details are present."}
    )
    founder = create_user("verify-founder@example.com", "founder")
    assert submit_verification(founder).status_code == 403

    investor = create_user("verify-consent@example.com", "investor")
    create_match_profile(investor)
    no_consent = client.post(
        "/api/v1/verification/me",
        headers=investor,
        json={
            "processing_consent_accepted": False,
            "trust_notice_accepted": True,
            "portfolio_url": "https://example.org/product",
            "secp_entity_name": "Example Technologies",
            "secp_registration_number": "123",
        },
    )
    assert no_consent.status_code == 400
    http_url = client.post(
        "/api/v1/verification/me",
        headers=investor,
        json={
            "processing_consent_accepted": True,
            "trust_notice_accepted": True,
            "portfolio_url": "http://example.org/product",
            "secp_entity_name": "Example Technologies",
            "secp_registration_number": "123",
        },
    )
    assert http_url.status_code == 422
    private_host = client.post(
        "/api/v1/verification/me",
        headers=investor,
        json={
            "processing_consent_accepted": True,
            "trust_notice_accepted": True,
            "portfolio_url": "https://127.0.0.1/admin",
            "secp_entity_name": "Example Technologies",
            "secp_registration_number": "123",
        },
    )
    assert private_host.status_code == 422


def test_portfolio_provider_failure_does_not_create_a_successful_verification():
    class FailedFetcher:
        def fetch(self, _url):
            raise RuntimeError("provider unavailable")

    app.dependency_overrides[get_portfolio_fetcher] = lambda: FailedFetcher()
    headers = create_user("verify-failed@example.com", "mentor")
    create_match_profile(headers)
    result = submit_verification(headers)
    assert result.status_code == 503
    assert client.get("/api/v1/verification/me", headers=headers).status_code == 404


def test_empty_portfolio_page_is_insufficient_and_does_not_claim_a_match():
    fetcher = FakePortfolioFetcher()
    fetcher.fetch = lambda _url: ""
    gateway = FakeGateway(
        {"result": "consistent", "reason": "Unused when page has no content."}
    )
    app.dependency_overrides[get_portfolio_fetcher] = lambda: fetcher
    app.dependency_overrides[get_gateway] = lambda: gateway
    headers = create_user("verify-empty-page@example.com", "investor")
    create_match_profile(headers)

    result = submit_verification(headers)
    assert result.status_code == 201, result.text
    assert result.json()["signals"]["portfolio_link"] == "insufficient"
    assert result.json()["status"] == "pending_review"
    assert gateway.calls == 0


def test_thresholds_must_be_ordered():
    from pydantic import ValidationError

    from app.config import Settings

    with pytest.raises(ValidationError):
        Settings(
            _env_file=None,
            verification_low_threshold=0.9,
            verification_high_threshold=0.8,
        )
