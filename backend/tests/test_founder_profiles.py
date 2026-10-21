from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def _founder_token(email: str = "founder@example.com") -> str:
    registered = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "SecurePass123!",
            "full_name": "A Founder",
            "role": "founder",
        },
    )
    assert registered.status_code == 201, registered.text
    login = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "SecurePass123!"},
    )
    assert login.status_code == 200, login.text
    return login.json()["access_token"]


def test_founder_can_save_consented_profile_and_startup_traction():
    token = _founder_token()
    headers = {"Authorization": f"Bearer {token}"}

    profile = client.put(
        "/api/v1/founders/me/profile",
        headers=headers,
        json={
            "bio": "Building a logistics platform for local retailers.",
            "location": "Lahore, Pakistan",
            "consent_accepted": True,
        },
    )
    assert profile.status_code == 200, profile.text
    assert profile.json()["consent_version"]
    assert profile.json()["bio"].startswith("Building")

    startup = client.post(
        "/api/v1/founders/me/startups",
        headers=headers,
        json={
            "name": "Routewise",
            "description": "Inventory and delivery tools for neighborhood shops.",
            "sector": "logistics technology",
            "stage": "mvp",
            "location": "Lahore, Pakistan",
            "business_model": "Monthly subscription",
            "traction_summary": "12 pilot stores and 3 months of repeat usage.",
            "customer_count": 12,
            "monthly_revenue": 45000,
            "skills": ["operations", "backend engineering"],
        },
    )
    assert startup.status_code == 201, startup.text
    startup_data = startup.json()
    assert startup_data["name"] == "Routewise"
    assert startup_data["customer_count"] == 12
    assert startup_data["is_verified"] is False

    listed = client.get("/api/v1/founders/me/startups", headers=headers)
    assert listed.status_code == 200
    assert [item["id"] for item in listed.json()] == [startup_data["id"]]


def test_founder_profile_requires_explicit_consent():
    token = _founder_token()
    response = client.put(
        "/api/v1/founders/me/profile",
        headers={"Authorization": f"Bearer {token}"},
        json={"bio": "A profile without consent", "location": "Lahore", "consent_accepted": False},
    )
    assert response.status_code == 400


def test_non_founder_cannot_write_founder_profile():
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "mentor@example.com",
            "password": "SecurePass123!",
            "full_name": "A Mentor",
            "role": "mentor",
        },
    )
    login = client.post(
        "/api/v1/auth/login",
        json={"email": "mentor@example.com", "password": "SecurePass123!"},
    )
    token = login.json()["access_token"]

    response = client.put(
        "/api/v1/founders/me/profile",
        headers={"Authorization": f"Bearer {token}"},
        json={"bio": "Not a founder", "location": "Lahore", "consent_accepted": True},
    )
    assert response.status_code == 403
