from types import SimpleNamespace

from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.dialects import postgresql

from app.database import get_db
from app.feature_models import ProfileVerification
from app.feature_schemas import PitchTurnResult, ReadinessResult
from app.main import app
from app.models import EcosystemProfile, Startup, User
from app.routes.intelligence import _matching_candidates_query
from app.services.feature_ai import get_encoder, get_gateway

client = TestClient(app)
fake_gateway = None


class FakeEncoder:
    model_name = "test-embedding-model"

    def encode(self, texts):
        return tuple((1.0, 0.0) for _ in texts)


class FakeGateway:
    def __init__(self):
        self.pitch_call = 0
        self.pitch_requests = []
        self.fail_pitch = False

    def generate_structured(self, *, response_schema, **kwargs):
        if response_schema is ReadinessResult:
            return ReadinessResult.model_validate(
                {
                    "dimensions": [
                        {
                            "dimension": name,
                            "score": 3,
                            "reasoning": "Evidence supplied by the founder supports this score.",
                            "next_action": "Validate this with three target customers.",
                        }
                        for name in (
                            "problem_clarity",
                            "market_definition",
                            "differentiation",
                            "business_model_coherence",
                            "traction",
                            "team",
                            "scalability",
                        )
                    ]
                }
            )
        self.pitch_requests.append(kwargs)
        if self.fail_pitch:
            raise RuntimeError("mock pitch provider failure")
        self.pitch_call += 1
        if self.pitch_call == 1:
            return PitchTurnResult(
                finished=False, next_question="How will you acquire customers?"
            )
        score = {
            "score": 4,
            "reasoning": "The founder gave a clear, specific response.",
        }
        return PitchTurnResult(
            finished=True, clarity=score, confidence=score, content=score
        )


def setup_function():
    global fake_gateway
    fake_gateway = FakeGateway()
    app.dependency_overrides[get_encoder] = FakeEncoder
    app.dependency_overrides[get_gateway] = lambda: fake_gateway


def teardown_function():
    app.dependency_overrides.pop(get_encoder, None)
    app.dependency_overrides.pop(get_gateway, None)


def create_user(email, role):
    response = client.post(
        f"/api/v1/auth/register/{role}",
        json={
            "email": email,
            "password": "SecurePass123!",
            "full_name": role.title(),
            "consent_accepted": True,
        },
    )
    assert response.status_code == 201, response.text
    login = client.post(
        "/api/v1/auth/login", json={"email": email, "password": "SecurePass123!"}
    )
    assert login.status_code == 200, login.text
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def mark_profile_verified(headers):
    user_id = client.get("/api/v1/users/me", headers=headers).json()["id"]
    db_generator = app.dependency_overrides[get_db]()
    db = next(db_generator)
    db.add(
        ProfileVerification(
            user_id=user_id,
            portfolio_url="https://example.org/portfolio",
            secp_entity_name="Example Technologies",
            secp_registration_number="123456",
            status="verified",
            score=0.9,
            band="high",
            signals={"secp_cross_check": "verified"},
            reason="Reviewer verified the SECP record.",
            threshold_version="profile-verification-test-v1",
            consent_version="profile-verification-consent-v1",
            trust_notice_version="profile-verification-trust-v1",
        )
    )
    db.commit()
    try:
        next(db_generator)
    except StopIteration:
        pass


def create_startup(headers):
    consent = client.put(
        "/api/v1/founders/me/profile", headers=headers, json={"consent_accepted": True}
    )
    assert consent.status_code == 200, consent.text
    response = client.post(
        "/api/v1/founders/me/startups",
        headers=headers,
        json={
            "name": "Routewise",
            "description": "Tools for local retail delivery.",
            "sector": "logistics",
            "stage": "mvp",
            "location": "Lahore, Pakistan",
            "business_model": "Subscription",
            "traction_summary": "12 active pilot shops",
            "customer_count": 12,
            "skills": ["operations", "software"],
            "funding_need_min": 10000,
            "funding_need_max": 20000,
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


def test_matching_explanation_and_contact_require_both_acceptances():
    founder = create_user("founder-match@example.com", "founder")
    startup = create_startup(founder)
    mentor = create_user("mentor-match@example.com", "mentor")
    profile_payload = {
        "consent_accepted": True,
        "sector": "logistics",
        "stages": ["mvp"],
        "skills": ["operations", "software"],
        "availability": "open",
        "location": "Lahore, Pakistan",
        "summary": "Mentors logistics founders.",
        "is_open": True,
    }
    no_consent = client.put(
        "/api/v1/matching/me/profile",
        headers=mentor,
        json={**profile_payload, "consent_accepted": False},
    )
    assert no_consent.status_code == 400
    saved = client.put(
        "/api/v1/matching/me/profile", headers=mentor, json=profile_payload
    )
    assert saved.status_code == 200, saved.text
    assert saved.json()["consent_version"] == "ecosystem-profile-v1"
    mark_profile_verified(mentor)

    matches = client.get(f"/api/v1/matching/startups/{startup['id']}", headers=founder)
    assert matches.status_code == 200, matches.text
    match = matches.json()[0]
    assert set(match["factors"]) == {
        "sector_fit",
        "stage_fit",
        "skill_overlap",
        "availability_fit",
        "ticket_fit",
    }
    assert match["semantic_similarity"] == 1
    assert match["score"] == 1
    assert match["request_status"] == "recommended"
    assert match["contact_email"] is None
    assert (
        client.get("/api/v1/matching/me", headers=mentor).json()[0]["contact_email"]
        is None
    )

    accepted_by_mentor = client.post(
        f"/api/v1/matching/{match['id']}/accept", headers=mentor
    )
    assert accepted_by_mentor.status_code == 200
    assert accepted_by_mentor.json()["request_status"] == "pending"
    assert accepted_by_mentor.json()["contact_email"] is None
    assert (
        client.get(
            f"/api/v1/matching/startups/{startup['id']}", headers=founder
        ).json()[0]["contact_email"]
        is None
    )
    assert (
        client.get("/api/v1/matching/me", headers=founder).json()[0]["contact_email"]
        is None
    )
    assert (
        client.get("/api/v1/matching/me", headers=mentor).json()[0]["contact_email"]
        is None
    )
    accepted_by_founder = client.post(
        f"/api/v1/matching/{match['id']}/accept", headers=founder
    )
    assert accepted_by_founder.json()["request_status"] == "accepted"
    assert accepted_by_founder.json()["contact_email"] == "mentor-match@example.com"
    refreshed_matches = client.get(
        f"/api/v1/matching/startups/{startup['id']}", headers=founder
    )
    assert refreshed_matches.json()[0]["contact_email"] == "mentor-match@example.com"
    mentor_matches = client.get("/api/v1/matching/me", headers=mentor)
    assert mentor_matches.json()[0]["contact_email"] == "founder-match@example.com"


def test_unverified_mentor_is_hidden_and_profile_edits_return_it_to_review():
    founder = create_user("founder-verification-gate@example.com", "founder")
    startup = create_startup(founder)
    mentor = create_user("mentor-verification-gate@example.com", "mentor")
    profile_payload = {
        "consent_accepted": True,
        "sector": "logistics",
        "stages": ["mvp"],
        "skills": ["operations"],
        "availability": "open",
        "location": "Lahore, Pakistan",
        "summary": "Mentor for logistics founders.",
    }
    assert (
        client.put(
            "/api/v1/matching/me/profile", headers=mentor, json=profile_payload
        ).status_code
        == 200
    )
    endpoint = f"/api/v1/matching/startups/{startup['id']}"
    assert client.get(endpoint, headers=founder).json() == []

    mark_profile_verified(mentor)
    assert client.get(endpoint, headers=founder).json()[0]["candidate_role"] == "mentor"

    profile_payload["summary"] = "Updated profile for logistics founders."
    updated = client.put(
        "/api/v1/matching/me/profile", headers=mentor, json=profile_payload
    )
    assert updated.status_code == 200
    status_response = client.get("/api/v1/verification/me", headers=mentor)
    assert status_response.json()["status"] == "pending_review"
    assert status_response.json()["rescore_locked"] is True
    assert client.get(endpoint, headers=founder).json() == []


def test_matching_request_can_be_accepted_to_reveal_contacts():
    founder = create_user("founder-request@example.com", "founder")
    startup = create_startup(founder)
    mentor = create_user("mentor-request@example.com", "mentor")
    profile = client.put(
        "/api/v1/matching/me/profile",
        headers=mentor,
        json={
            "consent_accepted": True,
            "sector": "logistics",
            "stages": ["mvp"],
            "skills": ["operations"],
            "availability": "open",
            "location": "Lahore, Pakistan",
            "summary": "Interested mentor.",
        },
    )
    assert profile.status_code == 200
    mark_profile_verified(mentor)
    matches = client.get(f"/api/v1/matching/startups/{startup['id']}", headers=founder)
    match_id = matches.json()[0]["id"]

    request = client.post(f"/api/v1/matching/{match_id}/request", headers=founder)
    assert request.status_code == 202, request.text
    assert request.json()["request_status"] == "pending"
    assert request.json()["founder_accepted"] is True
    assert request.json()["candidate_accepted"] is False
    assert request.json()["contact_email"] is None
    assert (
        client.post(f"/api/v1/matching/{match_id}/request", headers=founder).status_code
        == 409
    )

    accepted = client.post(f"/api/v1/matching/{match_id}/accept", headers=mentor)
    assert accepted.status_code == 200, accepted.text
    assert accepted.json()["request_status"] == "accepted"
    assert accepted.json()["contact_email"] == "founder-request@example.com"


def test_matching_recipient_can_decline_without_contact_reveal():
    founder = create_user("founder-decline@example.com", "founder")
    startup = create_startup(founder)
    mentor = create_user("mentor-decline@example.com", "mentor")
    outsider = create_user("outsider-decline@example.com", "talent")
    profile = client.put(
        "/api/v1/matching/me/profile",
        headers=mentor,
        json={
            "consent_accepted": True,
            "sector": "logistics",
            "stages": ["mvp"],
            "skills": ["operations"],
            "availability": "open",
            "location": "Lahore, Pakistan",
            "summary": "Not sure yet.",
        },
    )
    assert profile.status_code == 200
    mark_profile_verified(mentor)
    matches = client.get(f"/api/v1/matching/startups/{startup['id']}", headers=founder)
    match_id = matches.json()[0]["id"]

    assert (
        client.post(f"/api/v1/matching/{match_id}/request", headers=founder).status_code
        == 202
    )
    assert (
        client.post(
            f"/api/v1/matching/{match_id}/decline", headers=outsider
        ).status_code
        == 404
    )
    declined = client.post(f"/api/v1/matching/{match_id}/decline", headers=mentor)
    assert declined.status_code == 200, declined.text
    assert declined.json()["request_status"] == "declined"
    assert declined.json()["contact_email"] is None
    assert (
        client.post(f"/api/v1/matching/{match_id}/accept", headers=founder).status_code
        == 409
    )
    assert (
        client.post(f"/api/v1/matching/{match_id}/request", headers=founder).status_code
        == 409
    )


def test_closed_mentor_is_not_recommended():
    founder = create_user("founder-closed@example.com", "founder")
    startup = create_startup(founder)
    mentor = create_user("mentor-closed@example.com", "mentor")
    profile = client.put(
        "/api/v1/matching/me/profile",
        headers=mentor,
        json={
            "consent_accepted": True,
            "sector": "logistics",
            "stages": ["mvp"],
            "availability": "closed",
            "location": "Lahore, Pakistan",
            "summary": "Currently unavailable.",
            "is_open": False,
        },
    )
    assert profile.status_code == 200
    contradictory = client.put(
        "/api/v1/matching/me/profile",
        headers=mentor,
        json={
            "consent_accepted": True,
            "sector": "logistics",
            "stages": ["mvp"],
            "availability": "closed",
            "location": "Lahore, Pakistan",
            "summary": "Currently unavailable.",
            "is_open": True,
        },
    )
    assert contradictory.status_code == 422
    mark_profile_verified(mentor)
    results = client.get(f"/api/v1/matching/startups/{startup['id']}", headers=founder)
    assert results.status_code == 200
    assert results.json() == []


def test_talent_profiles_can_match_with_founders():
    founder = create_user("founder-talent@example.com", "founder")
    startup = create_startup(founder)
    talent = create_user("talent-match@example.com", "talent")
    profile = client.put(
        "/api/v1/matching/me/profile",
        headers=talent,
        json={
            "consent_accepted": True,
            "sector": "logistics",
            "stages": ["mvp"],
            "skills": ["software"],
            "availability": "open",
            "location": "Lahore, Pakistan",
            "summary": "Backend engineer for startups.",
        },
    )
    assert profile.status_code == 200, profile.text
    results = client.get(f"/api/v1/matching/startups/{startup['id']}", headers=founder)
    assert results.status_code == 200
    assert results.json()[0]["candidate_role"] == "talent"
    assert results.json()[0]["contact_email"] is None


def test_matching_limits_results_to_requested_top_k():
    founder = create_user("founder-top-k@example.com", "founder")
    startup = create_startup(founder)
    endpoint = f"/api/v1/matching/startups/{startup['id']}"

    for number in range(4):
        mentor = create_user(f"mentor-top-k-{number}@example.com", "mentor")
        response = client.put(
            "/api/v1/matching/me/profile",
            headers=mentor,
            json={
                "consent_accepted": True,
                "sector": "logistics",
                "stages": ["mvp"],
                "skills": ["operations"],
                "availability": "open",
                "location": "Lahore, Pakistan",
                "summary": f"Mentor profile {number}.",
            },
        )
        assert response.status_code == 200, response.text
        mark_profile_verified(mentor)

    default_results = client.get(endpoint, headers=founder)
    one_result = client.get(f"{endpoint}?top_k=1", headers=founder)
    invalid_limit = client.get(f"{endpoint}?top_k=4", headers=founder)

    assert default_results.status_code == 200
    assert len(default_results.json()) == 3
    assert one_result.status_code == 200
    assert len(one_result.json()) == 1
    assert invalid_limit.status_code == 422


def test_closed_mentor_does_not_consume_founder_match_page_limit():
    founder = create_user("founder-closed-page@example.com", "founder")
    startup = create_startup(founder)
    mentor_headers = []
    for number in range(2):
        mentor = create_user(f"mentor-closed-page-{number}@example.com", "mentor")
        saved = client.put(
            "/api/v1/matching/me/profile",
            headers=mentor,
            json={
                "consent_accepted": True,
                "sector": "logistics",
                "stages": ["mvp"],
                "skills": ["operations"],
                "availability": "open",
                "location": "Lahore, Pakistan",
                "summary": f"Mentor profile {number}.",
            },
        )
        assert saved.status_code == 200, saved.text
        mark_profile_verified(mentor)
        mentor_headers.append(mentor)

    matches = client.get(f"/api/v1/matching/startups/{startup['id']}", headers=founder)
    assert matches.status_code == 200
    closed_mentor_id = client.get("/api/v1/users/me", headers=mentor_headers[0]).json()[
        "id"
    ]
    db_generator = app.dependency_overrides[get_db]()
    db = next(db_generator)
    profile = db.scalar(
        select(EcosystemProfile).where(EcosystemProfile.user_id == closed_mentor_id)
    )
    profile.is_open = False
    db.commit()
    try:
        results = client.get("/api/v1/matching/me?limit=1", headers=founder)
    finally:
        try:
            next(db_generator)
        except StopIteration:
            pass

    assert results.status_code == 200
    assert len(results.json()) == 1
    assert results.json()[0]["candidate_user_id"] != closed_mentor_id


def test_inactive_candidate_is_not_returned_in_founder_match_list():
    founder = create_user("founder-inactive-match@example.com", "founder")
    startup = create_startup(founder)
    mentor = create_user("mentor-inactive-match@example.com", "mentor")
    saved = client.put(
        "/api/v1/matching/me/profile",
        headers=mentor,
        json={
            "consent_accepted": True,
            "sector": "logistics",
            "stages": ["mvp"],
            "skills": ["operations"],
            "availability": "open",
            "location": "Lahore, Pakistan",
            "summary": "Mentor profile.",
        },
    )
    assert saved.status_code == 200, saved.text
    mark_profile_verified(mentor)
    matches = client.get(f"/api/v1/matching/startups/{startup['id']}", headers=founder)
    assert len(matches.json()) == 1
    inactive_mentor_id = client.get("/api/v1/users/me", headers=mentor).json()["id"]

    db_generator = app.dependency_overrides[get_db]()
    db = next(db_generator)
    inactive_mentor = db.get(User, inactive_mentor_id)
    inactive_mentor.is_active = False
    db.commit()
    try:
        results = client.get("/api/v1/matching/me", headers=founder)
    finally:
        try:
            next(db_generator)
        except StopIteration:
            pass

    assert results.status_code == 200
    assert results.json() == []


def test_postgres_candidate_filters_are_applied_before_similarity_limit():
    statement = _matching_candidates_query(
        startup=SimpleNamespace(
            id=17,
            location="Lahore, Pakistan",
            is_verified=False,
        ),
        query_vector=[0.25, 0.75],
        embedding_model="test-embedding-model",
        readiness_exists=False,
        top_k=3,
        is_postgresql=True,
    )
    compiled = statement.compile(dialect=postgresql.dialect())
    sql = str(compiled).lower()

    assert "users.role in" in sql
    assert "profile_verifications.status in" in sql
    assert "lower(trim(ecosystem_profiles.location))" in sql
    assert "users.is_active is true" in sql
    assert (
        "users.role !=" in sql
    )  # Investors are excluded until verification and readiness.
    assert "vector_dims(ecosystem_profiles.embedding)" in sql
    assert (
        "ecosystem_profiles.embedding <=>" in sql
    )  # PostgreSQL cosine distance orders candidates.
    assert "users.hashed_password" not in sql
    assert "users.email" not in sql
    assert (
        sql.index("where ecosystem_profiles.is_open")
        < sql.index("order by")
        < sql.index("limit")
    )
    assert compiled.params["lower_1"] == "lahore, pakistan"


def test_investors_only_see_verified_startups_with_readiness():
    founder = create_user("founder-investor@example.com", "founder")
    startup = create_startup(founder)
    investor = create_user("investor-match@example.com", "investor")
    profile = client.put(
        "/api/v1/matching/me/profile",
        headers=investor,
        json={
            "consent_accepted": True,
            "sector": "logistics",
            "stages": ["mvp"],
            "skills": ["operations"],
            "availability": "open",
            "location": "Lahore, Pakistan",
            "summary": "Early stage investor.",
            "ticket_min": 10000,
            "ticket_max": 25000,
        },
    )
    assert profile.status_code == 200, profile.text
    mark_profile_verified(investor)
    endpoint = f"/api/v1/matching/startups/{startup['id']}"
    assert client.get(endpoint, headers=founder).json() == []

    readiness = client.post(
        f"/api/v1/startups/{startup['id']}/readiness", headers=founder
    )
    assert readiness.status_code == 201
    assert client.get(endpoint, headers=founder).json() == []

    db_generator = app.dependency_overrides[get_db]()
    db = next(db_generator)
    db.get(Startup, startup["id"]).is_verified = True
    db.commit()
    try:
        matches = client.get(endpoint, headers=founder)
        assert matches.status_code == 200
        assert matches.json()[0]["candidate_role"] == "investor"
        assert matches.json()[0]["contact_email"] is None
        investor_match = matches.json()[0]
        client.post(f"/api/v1/matching/{investor_match['id']}/accept", headers=founder)
        investor_acceptance = client.post(
            f"/api/v1/matching/{investor_match['id']}/accept", headers=investor
        )
        assert (
            investor_acceptance.json()["contact_email"]
            == "founder-investor@example.com"
        )
        assert (
            client.get("/api/v1/matching/me", headers=investor).json()[0][
                "contact_email"
            ]
            == "founder-investor@example.com"
        )
    finally:
        try:
            next(db_generator)
        except StopIteration:
            pass


def test_readiness_stores_all_seven_dimensions_and_history():
    founder = create_user("founder-ready@example.com", "founder")
    startup = create_startup(founder)
    result = client.post(f"/api/v1/startups/{startup['id']}/readiness", headers=founder)
    assert result.status_code == 201, result.text
    assessment = result.json()
    assert assessment["rubric_version"] == "readiness-v1"
    assert len(assessment["result"]["dimensions"]) == 7
    assert all(
        set(item) >= {"dimension", "score", "reasoning", "next_action"}
        for item in assessment["result"]["dimensions"]
    )
    history = client.get(f"/api/v1/startups/{startup['id']}/readiness", headers=founder)
    assert history.status_code == 200
    assert history.json()[0]["id"] == assessment["id"]


def test_pitch_keeps_transcript_and_only_scores_when_finished():
    founder = create_user("founder-pitch@example.com", "founder")
    startup = create_startup(founder)
    started = client.post(
        "/api/v1/pitch/sessions",
        headers=founder,
        json={"startup_id": startup["id"], "persona": "seed investor"},
    )
    assert started.status_code == 201, started.text
    session_id = started.json()["id"]
    assert started.json()["status"] == "active"
    assert started.json()["scores"] is None

    continuing = client.post(
        f"/api/v1/pitch/sessions/{session_id}/turns",
        headers=founder,
        json={"answer": "We help local shops reduce delivery delays."},
    )
    assert continuing.status_code == 200, continuing.text
    assert continuing.json()["status"] == "active"
    assert continuing.json()["scores"] is None

    finished = client.post(
        f"/api/v1/pitch/sessions/{session_id}/turns",
        headers=founder,
        json={"answer": "We charge each shop a monthly subscription."},
    )
    assert finished.status_code == 200, finished.text
    assert finished.json()["status"] == "completed"
    assert set(finished.json()["scores"]) == {"clarity", "confidence", "content"}
    assert len(finished.json()["turns"]) == 4
    rubric = fake_gateway.pitch_requests[-1]["system_instruction"]
    assert "fixed rubric" in rubric
    assert "Confidence means confidence conveyed by the writing" in rubric
    assert "not a funding prediction" in rubric
    history = client.get("/api/v1/pitch/history", headers=founder)
    assert history.json()[0]["id"] == session_id


def test_pitch_generation_failure_preserves_founder_answer():
    founder = create_user("founder-pitch-failure@example.com", "founder")
    startup = create_startup(founder)
    started = client.post(
        "/api/v1/pitch/sessions",
        headers=founder,
        json={"startup_id": startup["id"], "persona": "seed investor"},
    )
    session_id = started.json()["id"]
    fake_gateway.fail_pitch = True

    response = client.post(
        f"/api/v1/pitch/sessions/{session_id}/turns",
        headers=founder,
        json={"answer": "We have 12 pilot customers."},
    )

    assert response.status_code == 502
    history = client.get("/api/v1/pitch/history", headers=founder)
    saved = next(session for session in history.json() if session["id"] == session_id)
    assert saved["status"] == "active"
    assert saved["scores"] is None
    assert [turn["speaker"] for turn in saved["turns"]] == ["investor", "founder"]
    assert saved["turns"][-1]["content"] == "We have 12 pilot customers."


def test_pitch_can_be_marked_incomplete_without_a_final_score():
    founder = create_user("founder-incomplete@example.com", "founder")
    startup = create_startup(founder)
    started = client.post(
        "/api/v1/pitch/sessions",
        headers=founder,
        json={"startup_id": startup["id"], "persona": "seed investor"},
    )
    session_id = started.json()["id"]
    abandoned = client.post(
        f"/api/v1/pitch/sessions/{session_id}/abandon", headers=founder
    )
    assert abandoned.status_code == 200
    assert abandoned.json()["status"] == "incomplete"
    assert abandoned.json()["scores"] is None
    assert len(abandoned.json()["turns"]) == 1
