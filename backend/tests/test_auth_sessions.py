from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient
from jose import jwt

from app.config import get_settings
from app.main import app

client = TestClient(app)


def _register_and_login(email: str = "founder@example.com") -> str:
    client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "SecurePass123!",
            "full_name": "A Founder",
            "role": "founder",
        },
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "SecurePass123!"},
    )
    assert response.status_code == 200, response.text
    return response.json()["access_token"]


def test_public_registration_cannot_create_an_admin():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "admin@example.com",
            "password": "SecurePass123!",
            "full_name": "Public Admin",
            "role": "admin",
        },
    )
    assert response.status_code == 400
    assert client.post(
        "/api/v1/auth/login",
        json={"email": "admin@example.com", "password": "SecurePass123!"},
    ).status_code == 401


def test_registration_validation_does_not_echo_the_submitted_password():
    password = "Pwd#X!"
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "short-password@example.com",
            "password": password,
            "full_name": "A Founder",
            "role": "founder",
        },
    )
    assert response.status_code == 422
    assert password not in response.text


def test_logout_invalidates_all_tokens_issued_before_logout():
    token = _register_and_login()
    second_token = client.post(
        "/api/v1/auth/login",
        json={"email": "founder@example.com", "password": "SecurePass123!"},
    ).json()["access_token"]

    logout = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert logout.status_code == 204

    for issued_token in (token, second_token):
        response = client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {issued_token}"},
        )
        assert response.status_code == 401


def test_expired_token_is_rejected():
    settings = get_settings()
    expired = jwt.encode(
        {
            "sub": "1",
            "role": "founder",
            "ver": 0,
            "exp": datetime.now(UTC) - timedelta(seconds=1),
        },
        settings.secret_key,
        algorithm=settings.algorithm,
    )
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {expired}"},
    )
    assert response.status_code == 401
