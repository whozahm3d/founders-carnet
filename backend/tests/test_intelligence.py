from fastapi.testclient import TestClient

from app.database import get_db
from app.feature_schemas import PitchTurnResult, ReadinessResult
from app.main import app
from app.models import Startup
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

    def generate_structured(self, *, response_schema, **kwargs):
        if response_schema is ReadinessResult:
            return ReadinessResult.model_validate({
                "dimensions": [
                    {"dimension": name, "score": 3, "reasoning": "Evidence supplied by the founder supports this score.",
                     "next_action": "Validate this with three target customers."}
                    for name in (
                        "problem_clarity", "market_definition", "differentiation",
                        "business_model_coherence", "traction", "team", "scalability",
                    )
                ]
            })
        self.pitch_call += 1
        if self.pitch_call == 1:
            return PitchTurnResult(finished=False, next_question="How will you acquire customers?")
        score = {"score": 4, "reasoning": "The founder gave a clear, specific response."}
        return PitchTurnResult(finished=True, clarity=score, confidence=score, content=score)


def setup_function():
    global fake_gateway
    fake_gateway = FakeGateway()
    app.dependency_overrides[get_encoder] = FakeEncoder
    app.dependency_overrides[get_gateway] = lambda: fake_gateway


def teardown_function():
    app.dependency_overrides.pop(get_encoder, None)
    app.dependency_overrides.pop(get_gateway, None)


def create_user(email, role):
    response = client.post("/api/v1/auth/register", json={
        "email": email, "password": "SecurePass123!", "full_name": role.title(), "role": role,
    })
    assert response.status_code == 201, response.text
    login = client.post("/api/v1/auth/login", json={"email": email, "password": "SecurePass123!"})
    assert login.status_code == 200, login.text
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def create_startup(headers):
    consent = client.put("/api/v1/founders/me/profile", headers=headers, json={"consent_accepted": True})
    assert consent.status_code == 200, consent.text
    response = client.post("/api/v1/founders/me/startups", headers=headers, json={
        "name": "Routewise", "description": "Tools for local retail delivery.", "sector": "logistics",
        "stage": "mvp", "location": "Lahore, Pakistan", "business_model": "Subscription",
        "traction_summary": "12 active pilot shops", "customer_count": 12,
        "skills": ["operations", "software"], "funding_need_min": 10000, "funding_need_max": 20000,
    })
    assert response.status_code == 201, response.text
    return response.json()


def test_matching_explanation_and_contact_require_both_acceptances():
    founder = create_user("founder-match@example.com", "founder")
    startup = create_startup(founder)
    mentor = create_user("mentor-match@example.com", "mentor")
    profile_payload = {
        "consent_accepted": True,
        "sector": "logistics", "stages": ["mvp"], "skills": ["operations", "software"],
        "availability": "open", "location": "Lahore, Pakistan", "summary": "Mentors logistics founders.",
        "is_open": True,
    }
    no_consent = client.put("/api/v1/matching/me/profile", headers=mentor,
                            json={**profile_payload, "consent_accepted": False})
    assert no_consent.status_code == 400
    saved = client.put("/api/v1/matching/me/profile", headers=mentor, json=profile_payload)
    assert saved.status_code == 200, saved.text
    assert saved.json()["consent_version"] == "ecosystem-profile-v1"

    matches = client.get(f"/api/v1/matching/startups/{startup['id']}", headers=founder)
    assert matches.status_code == 200, matches.text
    match = matches.json()[0]
    assert set(match["factors"]) == {"sector_fit", "stage_fit", "skill_overlap", "availability_fit", "ticket_fit"}
    assert match["semantic_similarity"] == 1
    assert match["score"] == 1
    assert match["contact_email"] is None

    accepted_by_mentor = client.post(f"/api/v1/matching/{match['id']}/accept", headers=mentor)
    assert accepted_by_mentor.status_code == 200
    assert accepted_by_mentor.json()["contact_email"] is None
    accepted_by_founder = client.post(f"/api/v1/matching/{match['id']}/accept", headers=founder)
    assert accepted_by_founder.json()["contact_email"] == "mentor-match@example.com"
    mentor_matches = client.get("/api/v1/matching/me", headers=mentor)
    assert mentor_matches.json()[0]["contact_email"] == "founder-match@example.com"


def test_closed_mentor_is_not_recommended():
    founder = create_user("founder-closed@example.com", "founder")
    startup = create_startup(founder)
    mentor = create_user("mentor-closed@example.com", "mentor")
    profile = client.put("/api/v1/matching/me/profile", headers=mentor, json={
        "consent_accepted": True,
        "sector": "logistics", "stages": ["mvp"], "availability": "closed",
        "location": "Lahore, Pakistan", "summary": "Currently unavailable.", "is_open": False,
    })
    assert profile.status_code == 200
    contradictory = client.put("/api/v1/matching/me/profile", headers=mentor, json={
        "consent_accepted": True,
        "sector": "logistics", "stages": ["mvp"], "availability": "closed",
        "location": "Lahore, Pakistan", "summary": "Currently unavailable.", "is_open": True,
    })
    assert contradictory.status_code == 422
    results = client.get(f"/api/v1/matching/startups/{startup['id']}", headers=founder)
    assert results.status_code == 200
    assert results.json() == []


def test_talent_profiles_can_match_with_founders():
    founder = create_user("founder-talent@example.com", "founder")
    startup = create_startup(founder)
    talent = create_user("talent-match@example.com", "talent")
    profile = client.put("/api/v1/matching/me/profile", headers=talent, json={
        "consent_accepted": True,
        "sector": "logistics", "stages": ["mvp"], "skills": ["software"],
        "availability": "open", "location": "Lahore, Pakistan", "summary": "Backend engineer for startups.",
    })
    assert profile.status_code == 200, profile.text
    results = client.get(f"/api/v1/matching/startups/{startup['id']}", headers=founder)
    assert results.status_code == 200
    assert results.json()[0]["candidate_role"] == "talent"
    assert results.json()[0]["contact_email"] is None


def test_investors_only_see_verified_startups_with_readiness():
    founder = create_user("founder-investor@example.com", "founder")
    startup = create_startup(founder)
    investor = create_user("investor-match@example.com", "investor")
    profile = client.put("/api/v1/matching/me/profile", headers=investor, json={
        "consent_accepted": True,
        "sector": "logistics", "stages": ["mvp"], "skills": ["operations"],
        "availability": "open", "location": "Lahore, Pakistan", "summary": "Early stage investor.",
        "ticket_min": 10000, "ticket_max": 25000,
    })
    assert profile.status_code == 200, profile.text
    endpoint = f"/api/v1/matching/startups/{startup['id']}"
    assert client.get(endpoint, headers=founder).json() == []

    readiness = client.post(f"/api/v1/startups/{startup['id']}/readiness", headers=founder)
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
        investor_acceptance = client.post(f"/api/v1/matching/{investor_match['id']}/accept", headers=investor)
        assert investor_acceptance.json()["contact_email"] == "founder-investor@example.com"
        assert client.get("/api/v1/matching/me", headers=investor).json()[0]["contact_email"] == "founder-investor@example.com"
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
    assert all(set(item) >= {"dimension", "score", "reasoning", "next_action"} for item in assessment["result"]["dimensions"])
    history = client.get(f"/api/v1/startups/{startup['id']}/readiness", headers=founder)
    assert history.status_code == 200
    assert history.json()[0]["id"] == assessment["id"]


def test_pitch_keeps_transcript_and_only_scores_when_finished():
    founder = create_user("founder-pitch@example.com", "founder")
    startup = create_startup(founder)
    started = client.post("/api/v1/pitch/sessions", headers=founder,
                          json={"startup_id": startup["id"], "persona": "seed investor"})
    assert started.status_code == 201, started.text
    session_id = started.json()["id"]
    assert started.json()["status"] == "active"
    assert started.json()["scores"] is None

    continuing = client.post(f"/api/v1/pitch/sessions/{session_id}/turns", headers=founder,
                             json={"answer": "We help local shops reduce delivery delays."})
    assert continuing.status_code == 200, continuing.text
    assert continuing.json()["status"] == "active"
    assert continuing.json()["scores"] is None

    finished = client.post(f"/api/v1/pitch/sessions/{session_id}/turns", headers=founder,
                           json={"answer": "We charge each shop a monthly subscription."})
    assert finished.status_code == 200, finished.text
    assert finished.json()["status"] == "completed"
    assert set(finished.json()["scores"]) == {"clarity", "confidence", "content"}
    assert len(finished.json()["turns"]) == 4
    history = client.get("/api/v1/pitch/history", headers=founder)
    assert history.json()[0]["id"] == session_id


def test_pitch_can_be_marked_incomplete_without_a_final_score():
    founder = create_user("founder-incomplete@example.com", "founder")
    startup = create_startup(founder)
    started = client.post("/api/v1/pitch/sessions", headers=founder,
                          json={"startup_id": startup["id"], "persona": "seed investor"})
    session_id = started.json()["id"]
    abandoned = client.post(f"/api/v1/pitch/sessions/{session_id}/abandon", headers=founder)
    assert abandoned.status_code == 200
    assert abandoned.json()["status"] == "incomplete"
    assert abandoned.json()["scores"] is None
    assert len(abandoned.json()["turns"]) == 1
