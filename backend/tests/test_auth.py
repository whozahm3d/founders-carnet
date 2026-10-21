from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_and_login_founder():
    payload = {
        "email": "founder@example.com",
        "password": "SecurePass123!",
        "full_name": "Ali Founder",
        "role": "founder",
    }

    register_response = client.post("/api/v1/auth/register", json=payload)
    assert register_response.status_code == 201, register_response.text
    data = register_response.json()
    assert data["email"] == payload["email"]
    assert data["role"] == "founder"

    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": payload["email"], "password": payload["password"]},
    )
    assert login_response.status_code == 200, login_response.text
    token = login_response.json()["access_token"]
    assert token


def test_protected_me_endpoint_requires_token():
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401


def test_admin_route_rejects_non_admin_role():
    register = client.post(
        "/api/v1/auth/register",
        json={
            "email": "mentor@example.com",
            "password": "SecurePass123!",
            "full_name": "Mentor User",
            "role": "mentor",
        },
    )
    assert register.status_code == 201

    login = client.post(
        "/api/v1/auth/login",
        json={"email": "mentor@example.com", "password": "SecurePass123!"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    response = client.get(
        "/api/v1/admin/stats",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403


def test_expired_or_invalid_token_is_rejected():
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer not-a-valid-token"},
    )
    assert response.status_code == 401
