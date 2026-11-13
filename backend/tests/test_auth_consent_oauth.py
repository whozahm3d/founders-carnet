from datetime import UTC, datetime

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _registration_payload(email: str) -> dict[str, object]:
    return {
        "email": email,
        "password": "SecurePass123!",
        "full_name": "Consent User",
        "consent_accepted": True,
    }


def test_registration_requires_explicit_consent_and_does_not_create_user():
    response = client.post(
        "/api/v1/auth/register/founder",
        json={
            **_registration_payload("no-consent@example.com"),
            "consent_accepted": False,
        },
    )

    assert response.status_code == 400
    assert (
        client.post(
            "/api/v1/auth/login",
            json={"email": "no-consent@example.com", "password": "SecurePass123!"},
        ).status_code
        == 401
    )


def test_registration_role_is_in_path_and_admin_cannot_be_selected():
    response = client.post(
        "/api/v1/auth/register/admin",
        json=_registration_payload("admin-choice@example.com"),
    )

    assert response.status_code == 422
    assert (
        client.post(
            "/api/v1/auth/login",
            json={"email": "admin-choice@example.com", "password": "SecurePass123!"},
        ).status_code
        == 401
    )


def test_consent_can_be_withdrawn_without_exposing_password_or_token():
    client.post(
        "/api/v1/auth/register/founder",
        json=_registration_payload("withdraw@example.com"),
    )
    login = client.post(
        "/api/v1/auth/login",
        json={"email": "withdraw@example.com", "password": "SecurePass123!"},
    )
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    response = client.post("/api/v1/users/me/consent/withdraw", headers=headers)

    assert response.status_code == 200
    assert response.json()["withdrawn"] is True
    assert "access_token" not in response.text
    assert "SecurePass123!" not in response.text


def test_deletion_request_disables_account_invalidates_token_and_clears_llm_cache(
    monkeypatch,
):
    import app.main as main_module

    cleared_scopes = []
    monkeypatch.setattr(
        main_module,
        "clear_structured_response_cache",
        cleared_scopes.append,
        raising=False,
    )
    client.post(
        "/api/v1/auth/register/founder",
        json=_registration_payload("delete-me@example.com"),
    )
    login = client.post(
        "/api/v1/auth/login",
        json={"email": "delete-me@example.com", "password": "SecurePass123!"},
    )
    token = login.json()["access_token"]

    response = client.post(
        "/api/v1/users/me/deletion-request",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 202
    assert len(cleared_scopes) == 1
    assert isinstance(cleared_scopes[0], int)
    scheduled = datetime.fromisoformat(response.json()["deletion_scheduled_for"])
    assert scheduled > datetime.now(UTC).replace(tzinfo=None)
    assert (
        client.get(
            "/api/v1/users/me", headers={"Authorization": f"Bearer {token}"}
        ).status_code
        == 401
    )
    assert (
        client.post(
            "/api/v1/auth/login",
            json={"email": "delete-me@example.com", "password": "SecurePass123!"},
        ).status_code
        == 401
    )


def test_fake_linkedin_provider_creates_identity_and_reuses_it():
    payload = {
        "authorization_code": "fake-linkedin-code",
        "consent_accepted": True,
    }
    first = client.post("/api/v1/auth/linkedin/talent", json=payload)
    second = client.post("/api/v1/auth/linkedin/talent", json=payload)

    assert first.status_code == 201, first.text
    assert second.status_code == 200, second.text
    assert first.json()["id"] == second.json()["id"]
    assert first.json()["role"] == "talent"
