from fastapi.testclient import TestClient

from app.database import get_db
from app.main import app
from app.models import Startup


client = TestClient(app)


def create_user(email, role):
    registered = client.post(f"/api/v1/auth/register/{role}", json={
        "email": email,
        "password": "SecurePass123!",
        "full_name": role.title(),
        "consent_accepted": True,
    })
    assert registered.status_code == 201, registered.text
    login = client.post("/api/v1/auth/login", json={"email": email, "password": "SecurePass123!"})
    assert login.status_code == 200, login.text
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def create_startup(founder_headers, name="Job Board Startup"):
    profile = client.put(
        "/api/v1/founders/me/profile",
        headers=founder_headers,
        json={"consent_accepted": True},
    )
    assert profile.status_code == 200, profile.text
    created = client.post("/api/v1/founders/me/startups", headers=founder_headers, json={
        "name": name,
        "description": "Tools for local delivery businesses.",
        "sector": "logistics",
        "stage": "mvp",
        "location": "Lahore, Pakistan",
        "business_model": "subscription",
        "traction_summary": "Pilot users",
        "customer_count": 12,
    })
    assert created.status_code == 201, created.text
    return created.json()


def set_startup_verified(startup_id):
    db_generator = app.dependency_overrides[get_db]()
    db = next(db_generator)
    startup = db.get(Startup, startup_id)
    startup.is_verified = True
    db.commit()
    try:
        next(db_generator)
    except StopIteration:
        pass


def test_verified_founder_and_talent_complete_listing_application_flow():
    founder = create_user("jobs-founder@example.com", "founder")
    startup = create_startup(founder)
    set_startup_verified(startup["id"])
    talent = create_user("jobs-talent@example.com", "talent")

    created = client.post(f"/api/v1/startups/{startup['id']}/jobs", headers=founder, json={
        "title": "Backend Engineer Intern",
        "description": "Help improve our delivery platform API.",
        "employment_type": "internship",
        "location": "Lahore, Pakistan",
        "is_remote": False,
    })
    assert created.status_code == 201, created.text
    job = created.json()
    assert job["status"] == "open"
    assert job["startup_name"] == "Job Board Startup"

    browse = client.get("/api/v1/jobs", headers=talent)
    assert browse.status_code == 200
    assert browse.json()[0]["id"] == job["id"]
    saved = client.post(f"/api/v1/jobs/{job['id']}/save", headers=talent)
    assert saved.status_code == 200
    assert client.post(f"/api/v1/jobs/{job['id']}/save", headers=talent).status_code == 200
    assert client.get("/api/v1/jobs/saved", headers=talent).json()[0]["id"] == job["id"]

    application = client.post(f"/api/v1/jobs/{job['id']}/applications", headers=talent, json={
        "cover_letter": "I have built Python APIs and would like to contribute.",
    })
    assert application.status_code == 201, application.text
    assert application.json()["status"] == "submitted"
    assert client.post(
        f"/api/v1/jobs/{job['id']}/applications", headers=talent, json={"cover_letter": "Duplicate"}
    ).status_code == 409

    applications = client.get(f"/api/v1/startups/{startup['id']}/job-applications", headers=founder)
    assert applications.status_code == 200
    assert applications.json()[0]["candidate_email"] == "jobs-talent@example.com"
    assert client.get(
        f"/api/v1/startups/{startup['id']}/job-applications", headers=talent
    ).status_code == 403
    status_update = client.patch(
        f"/api/v1/job-applications/{application.json()['id']}",
        headers=founder,
        json={"status": "reviewing"},
    )
    assert status_update.status_code == 200
    candidate_history = client.get("/api/v1/jobs/applications/me", headers=talent)
    assert candidate_history.json()[0]["status"] == "reviewing"

    closed = client.patch(f"/api/v1/jobs/{job['id']}", headers=founder, json={"status": "closed"})
    assert closed.status_code == 200
    assert client.get("/api/v1/jobs", headers=talent).json() == []
    assert client.get("/api/v1/jobs/saved", headers=talent).json()[0]["status"] == "closed"
    assert client.post(f"/api/v1/jobs/{job['id']}/applications", headers=talent, json={}).status_code == 409

    deleted = client.delete(f"/api/v1/jobs/{job['id']}", headers=founder)
    assert deleted.status_code == 204
    assert client.get("/api/v1/jobs/saved", headers=talent).json() == []
    assert client.get("/api/v1/jobs/applications/me", headers=talent).json() == []


def test_unverified_or_non_owner_founder_cannot_manage_job_listings():
    founder = create_user("jobs-unverified@example.com", "founder")
    startup = create_startup(founder)
    talent = create_user("jobs-unverified-talent@example.com", "talent")

    unverified_publish = client.post(f"/api/v1/startups/{startup['id']}/jobs", headers=founder, json={
        "title": "Developer",
        "description": "Help us build.",
        "employment_type": "job",
        "location": "Lahore",
    })
    assert unverified_publish.status_code == 404

    set_startup_verified(startup["id"])
    created = client.post(f"/api/v1/startups/{startup['id']}/jobs", headers=founder, json={
        "title": "Developer",
        "description": "Help us build.",
        "employment_type": "job",
        "location": "Lahore",
    })
    assert created.status_code == 201
    other_founder = create_user("jobs-other-owner@example.com", "founder")
    assert client.delete(f"/api/v1/jobs/{created.json()['id']}", headers=other_founder).status_code == 404
    assert client.patch(
        f"/api/v1/jobs/{created.json()['id']}",
        headers=other_founder,
        json={"status": "closed"},
    ).status_code == 404
    assert client.get(
        f"/api/v1/startups/{startup['id']}/job-applications", headers=other_founder
    ).status_code == 404
    assert client.post(
        f"/api/v1/jobs/{created.json()['id']}/applications", headers=founder, json={}
    ).status_code == 403
    assert client.get("/api/v1/jobs", headers=founder).status_code == 403
    assert client.get("/api/v1/jobs", headers=talent).json()[0]["id"] == created.json()["id"]


def test_open_listing_cannot_be_saved_after_startup_loses_verification():
    founder = create_user("jobs-verification-revoked-founder@example.com", "founder")
    startup = create_startup(founder)
    set_startup_verified(startup["id"])
    talent = create_user("jobs-verification-revoked-talent@example.com", "talent")
    created = client.post(f"/api/v1/startups/{startup['id']}/jobs", headers=founder, json={
        "title": "Backend Engineer",
        "description": "Help improve our delivery platform API.",
        "employment_type": "job",
        "location": "Lahore, Pakistan",
    })
    assert created.status_code == 201, created.text

    db_generator = app.dependency_overrides[get_db]()
    db = next(db_generator)
    db.get(Startup, startup["id"]).is_verified = False
    db.commit()
    try:
        saved = client.post(f"/api/v1/jobs/{created.json()['id']}/save", headers=talent)
    finally:
        try:
            next(db_generator)
        except StopIteration:
            pass

    assert saved.status_code == 404


def test_job_listing_rejects_whitespace_only_required_fields_on_create_and_patch():
    founder = create_user("jobs-blank-fields-founder@example.com", "founder")
    startup = create_startup(founder)
    set_startup_verified(startup["id"])
    valid_listing = {
        "title": "Backend Engineer",
        "description": "Help improve our delivery platform API.",
        "employment_type": "job",
        "location": "Lahore, Pakistan",
    }

    for field in ("title", "description", "location"):
        invalid_create = {**valid_listing, field: "   "}
        created = client.post(
            f"/api/v1/startups/{startup['id']}/jobs", headers=founder, json=invalid_create
        )
        assert created.status_code == 422, f"{field} was accepted on create"

    created = client.post(
        f"/api/v1/startups/{startup['id']}/jobs", headers=founder, json=valid_listing
    )
    assert created.status_code == 201, created.text
    for field in ("title", "description", "location"):
        updated = client.patch(
            f"/api/v1/jobs/{created.json()['id']}", headers=founder, json={field: "   "}
        )
        assert updated.status_code == 422, f"{field} was accepted on patch"
