from fastapi.testclient import TestClient
from sqlalchemy import select

from app.database import get_db
from app.feature_models import VerificationSignal
from app.main import app
from app.services.feature_ai import get_encoder, get_gateway
from app.services.portfolio_verification import get_portfolio_fetcher
from app.services.secp_check import SecpCheckResult, get_secp_checker


client = TestClient(app)


class FakeEncoder:
    model_name = "test-encoder"

    def encode(self, texts):
        return [[0.1, 0.2, 0.3] for _ in texts]


class FakePortfolioFetcher:
    def fetch(self, _url):
        return "A product site with relevant company information."


class FakeGateway:
    def __init__(self):
        self.calls = 0

    def generate_structured(self, **_kwargs):
        from app.verification_schemas import PortfolioLinkAssessment

        self.calls += 1
        return PortfolioLinkAssessment(result="consistent", reason="The page matches the submitted profile.")


class VerifiedFakeSecpChecker:
    def check(self, _entity_name, _registration_number):
        return SecpCheckResult(
            outcome="verified",
            score=1.0,
            reason="The reviewer fake confirms the submitted SECP record.",
        )


class PendingFakeSecpChecker:
    def check(self, _entity_name, _registration_number):
        return SecpCheckResult(
            outcome="pending_manual_review",
            score=0.5,
            reason="A reviewer must check the official SECP record.",
        )


def setup_function():
    app.dependency_overrides[get_encoder] = FakeEncoder
    app.dependency_overrides[get_portfolio_fetcher] = lambda: FakePortfolioFetcher()


def teardown_function():
    app.dependency_overrides.clear()


def _register(email: str, role: str) -> dict[str, str]:
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
    login = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "SecurePass123!"},
    )
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def _matching_profile(headers: dict[str, str]) -> None:
    response = client.put(
        "/api/v1/matching/me/profile",
        headers=headers,
        json={
            "consent_accepted": True,
            "sector": "fintech",
            "stages": ["mvp"],
            "skills": ["strategy"],
            "availability": "open",
            "ticket_min": 0,
            "ticket_max": 100,
            "location": "Lahore",
            "summary": "A complete profile for a fintech professional.",
        },
    )
    assert response.status_code == 200, response.text


def test_talent_profile_stores_optional_github_link_and_requires_talent_role():
    talent = _register("talent-step4@example.com", "talent")
    saved = client.put(
        "/api/v1/talent/me/profile",
        headers=talent,
        json={"consent_accepted": True, "github_url": "https://github.com/example-user"},
    )

    assert saved.status_code == 200, saved.text
    assert saved.json()["github_url"] == "https://github.com/example-user"

    founder = _register("founder-step4@example.com", "founder")
    assert client.put(
        "/api/v1/talent/me/profile",
        headers=founder,
        json={"consent_accepted": True, "github_url": None},
    ).status_code == 403


def test_talent_verification_stores_all_five_signals_and_only_calls_gateway_for_link():
    gateway = FakeGateway()
    app.dependency_overrides[get_gateway] = lambda: gateway
    app.dependency_overrides[get_secp_checker] = lambda: PendingFakeSecpChecker()
    talent = _register("talent-verify-step4@example.com", "talent")
    _matching_profile(talent)
    github = client.put(
        "/api/v1/talent/me/profile",
        headers=talent,
        json={"consent_accepted": True, "github_url": "https://github.com/example-user"},
    )
    assert github.status_code == 200, github.text

    submitted = client.post(
        "/api/v1/verification/me",
        headers=talent,
        json={
            "processing_consent_accepted": True,
            "trust_notice_accepted": True,
            "portfolio_url": "https://example.org/product",
            "secp_entity_name": "Example Technologies (Private) Limited",
            "secp_registration_number": "0123456",
        },
    )

    assert submitted.status_code == 201, submitted.text
    body = submitted.json()
    assert set(body["signals"]) >= {
        "linkedin_oauth",
        "secp_cross_check",
        "profile_completeness",
        "github_for_talent",
        "portfolio_link",
    }
    assert body["signals"]["secp_cross_check"] == "pending_manual_review"
    assert body["status"] == "pending_review"
    assert gateway.calls == 1

    db_generator = app.dependency_overrides[get_db]()
    db = next(db_generator)
    try:
        verification_id = body["id"]
        rows = db.execute(
            select(VerificationSignal).where(VerificationSignal.verification_id == verification_id)
        ).scalars().all()
        assert {row.signal_name for row in rows} == {
            "linkedin_oauth",
            "secp_cross_check",
            "profile_completeness",
            "github_for_talent",
            "portfolio_link",
        }
    finally:
        db_generator.close()


def test_verified_secp_and_complete_signals_can_auto_verify():
    app.dependency_overrides[get_gateway] = lambda: FakeGateway()
    app.dependency_overrides[get_secp_checker] = lambda: VerifiedFakeSecpChecker()
    talent = _register("talent-auto-step4@example.com", "talent")
    _matching_profile(talent)
    client.put(
        "/api/v1/talent/me/profile",
        headers=talent,
        json={"consent_accepted": True, "github_url": "https://github.com/example-user"},
    )

    response = client.post(
        "/api/v1/verification/me",
        headers=talent,
        json={
            "processing_consent_accepted": True,
            "trust_notice_accepted": True,
            "portfolio_url": "https://example.org/product",
            "secp_entity_name": "Example Technologies (Private) Limited",
            "secp_registration_number": "0123456",
        },
    )

    assert response.status_code == 201, response.text
    assert response.json()["band"] == "high"
    assert response.json()["status"] == "auto_verified"
