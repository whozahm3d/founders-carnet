import io

import pytest
from fastapi.testclient import TestClient
from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject

from app.config import _REPOSITORY_ROOT, get_settings
from app.main import app
from app.services.feature_ai import get_gateway
from app.services.resume_optimizer import _private_storage_root


def synthetic_pdf(text="Built API endpoints for retail clients."):
    writer = PdfWriter()
    page = writer.add_blank_page(width=300, height=400)
    font = DictionaryObject(
        {
            NameObject("/Type"): NameObject("/Font"),
            NameObject("/Subtype"): NameObject("/Type1"),
            NameObject("/BaseFont"): NameObject("/Helvetica"),
        }
    )
    font_ref = writer._add_object(font)
    page[NameObject("/Resources")] = DictionaryObject(
        {
            NameObject("/Font"): DictionaryObject({NameObject("/F1"): font_ref}),
        }
    )
    content_stream = DecodedStreamObject()
    content_stream.set_data(f"BT /F1 12 Tf 40 350 Td ({text}) Tj ET".encode("ascii"))
    page[NameObject("/Contents")] = writer._add_object(content_stream)
    buffer = io.BytesIO()
    writer.write(buffer)
    return buffer.getvalue()


client = TestClient(app)
fake_gateway = None


class FakeGateway:
    model_name = "test-model"

    def __init__(self):
        self.fail = False
        self.invalid_line = False

    def generate_structured(self, *, response_schema, **kwargs):
        if self.fail:
            raise RuntimeError("mock provider failure")
        return response_schema.model_validate(
            {
                "suggestions": [
                    {
                        "line_number": 1,
                        "before": (
                            "A line not present in the resume."
                            if self.invalid_line
                            else "Built API endpoints for retail clients."
                        ),
                        "after": "Built API endpoints serving retail clients.",
                        "reasoning": "Uses a concise action verb while preserving the original claim.",
                    }
                ]
            }
        )


def setup_function():
    global fake_gateway
    fake_gateway = FakeGateway()
    app.dependency_overrides[get_gateway] = lambda: fake_gateway


def teardown_function():
    app.dependency_overrides.pop(get_gateway, None)


def create_talent(email="resume-talent@example.com"):
    registered = client.post(
        "/api/v1/auth/register/talent",
        json={
            "email": email,
            "password": "SecurePass123!",
            "full_name": "Resume Talent",
            "consent_accepted": True,
        },
    )
    assert registered.status_code == 201, registered.text
    login = client.post(
        "/api/v1/auth/login", json={"email": email, "password": "SecurePass123!"}
    )
    assert login.status_code == 200, login.text
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def pdf_headers(headers, consent="true"):
    return {
        **headers,
        "Content-Type": "application/pdf",
        "X-Resume-Processing-Consent": consent,
    }


def test_resume_optimizer_stores_private_pdf_and_returns_validated_line_edits(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(get_settings(), "resume_storage_dir", tmp_path)
    headers = create_talent()
    response = client.post(
        "/api/v1/resumes/optimize?target_role=Backend%20Engineer",
        headers=pdf_headers(headers),
        content=synthetic_pdf(),
    )

    assert response.status_code == 201, response.text
    report = response.json()
    assert report["status"] == "complete"
    assert (
        report["suggestions"][0]["before"] == "Built API endpoints for retail clients."
    )
    assert (
        report["suggestions"][0]["after"]
        == "Built API endpoints serving retail clients."
    )
    stored_files = list(tmp_path.glob("*.pdf"))
    assert len(stored_files) == 1
    assert stored_files[0].read_bytes().startswith(b"%PDF-")
    assert str(tmp_path) not in response.text

    history = client.get("/api/v1/resumes/history", headers=headers)
    assert history.status_code == 200
    assert history.json()[0]["id"] == report["id"]

    deleted = client.delete(f"/api/v1/resumes/{report['id']}", headers=headers)
    assert deleted.status_code == 204
    assert list(tmp_path.glob("*.pdf")) == []
    assert client.get("/api/v1/resumes/history", headers=headers).json() == []


def test_resume_upload_requires_processing_consent():
    headers = create_talent()
    response = client.post(
        "/api/v1/resumes/optimize?target_role=Backend%20Engineer",
        headers=pdf_headers(headers, consent="false"),
        content=b"%PDF-1.7\nsynthetic test document",
    )
    assert response.status_code == 403


def test_resume_upload_rejects_wrong_mime_or_pdf_signature():
    headers = create_talent()
    wrong_mime = client.post(
        "/api/v1/resumes/optimize?target_role=Backend%20Engineer",
        headers={
            **headers,
            "Content-Type": "text/plain",
            "X-Resume-Processing-Consent": "true",
        },
        content=b"not a pdf",
    )
    bad_signature = client.post(
        "/api/v1/resumes/optimize?target_role=Backend%20Engineer",
        headers=pdf_headers(headers),
        content=b"not a pdf",
    )
    assert wrong_mime.status_code == 415
    assert bad_signature.status_code == 415


def test_resume_rejects_empty_text_and_oversized_upload(tmp_path, monkeypatch):
    monkeypatch.setattr(get_settings(), "resume_storage_dir", tmp_path)
    headers = create_talent()
    scanned = client.post(
        "/api/v1/resumes/optimize?target_role=Backend%20Engineer",
        headers=pdf_headers(headers),
        content=synthetic_pdf(text=""),
    )
    oversized = client.post(
        "/api/v1/resumes/optimize?target_role=Backend%20Engineer",
        headers=pdf_headers(headers),
        content=b"%PDF-1.7" + b"x" * (5 * 1024 * 1024),
    )
    assert scanned.status_code == 422
    assert oversized.status_code == 413
    assert list(tmp_path.glob("*.pdf")) == []


def test_resume_generation_failure_is_logged_without_returning_fake_suggestions(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(get_settings(), "resume_storage_dir", tmp_path)
    fake_gateway.fail = True
    headers = create_talent()
    response = client.post(
        "/api/v1/resumes/optimize?target_role=Backend%20Engineer",
        headers=pdf_headers(headers),
        content=synthetic_pdf(),
    )
    assert response.status_code == 502
    assert "mock provider failure" not in response.text
    history = client.get("/api/v1/resumes/history", headers=headers)
    assert history.json()[0]["status"] == "generation_failed"
    assert history.json()[0]["suggestions"] is None


def test_resume_rejects_model_edits_that_do_not_match_source_lines(
    tmp_path, monkeypatch, caplog
):
    monkeypatch.setattr(get_settings(), "resume_storage_dir", tmp_path)
    fake_gateway.invalid_line = True
    headers = create_talent("resume-invalid-edit@example.com")

    response = client.post(
        "/api/v1/resumes/optimize?target_role=Backend%20Engineer",
        headers=pdf_headers(headers),
        content=synthetic_pdf(),
    )

    assert response.status_code == 502
    assert "Built API endpoints for retail clients." not in caplog.text
    assert "A line not present in the resume" not in caplog.text
    history = client.get("/api/v1/resumes/history", headers=headers)
    assert history.json()[0]["status"] == "generation_failed"
    assert history.json()[0]["suggestions"] is None


def test_resume_history_and_delete_are_scoped_to_owner(tmp_path, monkeypatch):
    monkeypatch.setattr(get_settings(), "resume_storage_dir", tmp_path)
    owner_headers = create_talent("resume-owner@example.com")
    other_headers = create_talent("resume-other@example.com")
    response = client.post(
        "/api/v1/resumes/optimize?target_role=Backend%20Engineer",
        headers=pdf_headers(owner_headers),
        content=synthetic_pdf(),
    )
    resume_id = response.json()["id"]
    stored_before = list(tmp_path.glob("*.pdf"))

    assert client.get("/api/v1/resumes/history", headers=other_headers).json() == []
    assert (
        client.delete(f"/api/v1/resumes/{resume_id}", headers=other_headers).status_code
        == 404
    )
    assert list(tmp_path.glob("*.pdf")) == stored_before


def test_resume_storage_rejects_served_and_unignored_repo_paths(monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(
        settings, "resume_storage_dir", _REPOSITORY_ROOT / "backend" / "app"
    )
    with pytest.raises(RuntimeError):
        _private_storage_root()


def test_resume_upload_openapi_documents_raw_pdf_body():
    operation = client.get("/openapi.json").json()["paths"]["/api/v1/resumes/optimize"][
        "post"
    ]
    request_body = operation["requestBody"]
    assert request_body["content"]["application/pdf"]["schema"] == {
        "type": "string",
        "format": "binary",
    }
