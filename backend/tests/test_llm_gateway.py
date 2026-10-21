import json
import logging
import sys
from types import ModuleType
from types import SimpleNamespace

import pytest
from google.genai.errors import ServerError

from app.services.compliance_assistant import GroundingValidation
from app.services.compliance_retrieval import RetrievedChunk
import app.services.llm_gateway as gateway_module
from app.services.llm_gateway import GeminiGateway


class FakeModels:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.calls = []

    def generate_content(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(text=next(self.responses))


class FakeClient:
    def __init__(self, responses):
        self.models = FakeModels(responses)
        self.closed = False

    def close(self):
        self.closed = True


def test_gateway_requests_structured_evidence_bound_answer_and_validation(caplog):
    client = FakeClient(
        [
            json.dumps({"answer": "The source says this.", "citation_chunk_ids": ["c1"]}),
            json.dumps({"is_supported": True, "unsupported_claims": []}),
        ]
    )
    gateway = GeminiGateway(api_key="test-key", model_name="configured-model", client=client)
    passage = RetrievedChunk(
        chunk=SimpleNamespace(
            chunk_id="c1",
            text="Source passage text.",
            section="4",
            page_number=12,
            document=SimpleNamespace(
                title="Sample Act",
                issuing_body="SECP",
                effective_date="2026-06-30",
                source_url="https://example.test/source",
            ),
        ),
        similarity=0.91,
    )

    with caplog.at_level(logging.INFO, logger="app.services.llm_gateway"):
        draft = gateway.generate_answer("Question?", [passage])
        validation = gateway.validate_answer("Question?", draft.answer, [passage])

    assert draft.answer == "The source says this."
    assert draft.citation_chunk_ids == ["c1"]
    assert isinstance(validation, GroundingValidation)
    assert validation.is_supported is True
    assert len(client.models.calls) == 2
    first_config = client.models.calls[0]["config"]
    assert first_config["response_mime_type"] == "application/json"
    assert "untrusted" in first_config["system_instruction"].lower()
    assert client.models.calls[0]["model"] == "configured-model"
    assert "Gemini generation completed" in caplog.text
    completed_records = [
        record for record in caplog.records
        if record.message.startswith("Gemini generation completed")
    ]
    assert len(completed_records) == 2
    assert completed_records[0].model == "configured-model"
    assert completed_records[0].passage_count == 1
    assert completed_records[0].approximate_prompt_chars > 0
    assert completed_records[0].elapsed_ms >= 0
    assert "model=configured-model" in completed_records[0].message
    assert "attempt_number=1" in completed_records[0].message
    assert "approximate_prompt_chars=" in completed_records[0].message
    assert "elapsed_ms=" in completed_records[0].message
    assert "Source passage text." not in caplog.text


def test_gateway_closes_its_client():
    client = FakeClient([])
    gateway = GeminiGateway(api_key="test-key", model_name="configured-model", client=client)

    gateway.close()

    assert client.closed is True


def test_gateway_configures_timeout_and_bounded_transient_retries(monkeypatch):
    captured = {}
    google_module = ModuleType("google")
    google_module.__path__ = []
    genai_module = ModuleType("google.genai")
    genai_module.Client = lambda **kwargs: captured.update(kwargs) or FakeClient([])
    types_module = ModuleType("google.genai.types")
    types_module.HttpOptions = lambda **kwargs: kwargs
    genai_module.types = types_module
    monkeypatch.setitem(sys.modules, "google", google_module)
    monkeypatch.setitem(sys.modules, "google.genai", genai_module)
    monkeypatch.setitem(sys.modules, "google.genai.types", types_module)

    GeminiGateway(api_key="test-key", model_name="configured-model")

    options = captured["http_options"]
    assert options["api_version"] == "v1"
    assert options["timeout"] == 60_000
    assert options["retry_options"] == {"attempts": 1}


def test_gateway_propagates_provider_errors_to_compliance_service():
    class FailingModels:
        def generate_content(self, **kwargs):
            raise RuntimeError("provider unavailable")

    client = SimpleNamespace(models=FailingModels())
    gateway = GeminiGateway(api_key="test-key", model_name="configured-model", client=client)

    with pytest.raises(RuntimeError, match="provider unavailable"):
        gateway.generate_answer("Question?", [])


def test_gateway_logs_and_propagates_timeout_without_prompt_contents(caplog):
    provider_error = ServerError(
        code=504,
        response_json={
            "error": {
                "message": "Deadline expired before operation could complete.",
                "status": "DEADLINE_EXCEEDED",
            }
        },
    )

    class TimeoutModels:
        def generate_content(self, **kwargs):
            raise provider_error

    client = SimpleNamespace(models=TimeoutModels())
    gateway = GeminiGateway(api_key="test-key", model_name="configured-model", client=client)
    passage = RetrievedChunk(
        chunk=SimpleNamespace(
            chunk_id="c1",
            text="Private evidence text.",
            section="1",
            page_number=1,
            document=SimpleNamespace(
                title="Sample Act",
                issuing_body="SECP",
                effective_date="2026-06-30",
            ),
        ),
        similarity=0.9,
    )

    with pytest.raises(ServerError, match="DEADLINE_EXCEEDED"):
        gateway.generate_answer("Private user question", [passage])

    assert "Gemini generation failed" in caplog.text
    assert "Private user question" not in caplog.text
    assert "Private evidence text." not in caplog.text
    failed_record = caplog.records[-1]
    assert failed_record.model == "configured-model"
    assert failed_record.passage_count == 1
    assert failed_record.approximate_prompt_chars > 0
    assert failed_record.elapsed_ms >= 0


def test_gateway_retries_504_once_and_logs_each_attempt(monkeypatch, caplog):
    timeout_error = ServerError(
        code=504,
        response_json={
            "error": {
                "message": "Deadline expired before operation could complete.",
                "status": "DEADLINE_EXCEEDED",
            }
        },
    )

    class RetryModels:
        def __init__(self):
            self.calls = []

        def generate_content(self, **kwargs):
            self.calls.append(kwargs)
            if len(self.calls) == 1:
                raise timeout_error
            return SimpleNamespace(
                text=json.dumps({"answer": "Supported.", "citation_chunk_ids": ["c1"]})
            )

    monkeypatch.setattr(gateway_module, "sleep", lambda seconds: None)
    client = SimpleNamespace(models=RetryModels())
    gateway = GeminiGateway(api_key="test-key", model_name="configured-model", client=client)
    passage = RetrievedChunk(
        chunk=SimpleNamespace(
            chunk_id="c1",
            text="Evidence.",
            section="1",
            page_number=1,
            document=SimpleNamespace(
                title="Sample Act",
                issuing_body="SECP",
                effective_date="2026-06-30",
            ),
        ),
        similarity=0.9,
    )

    with caplog.at_level(logging.INFO, logger="app.services.llm_gateway"):
        answer = gateway.generate_answer("Question?", [passage])

    assert answer.answer == "Supported."
    assert len(client.models.calls) == 2
    assert all(call["model"] == "configured-model" for call in client.models.calls)
    retry_record = next(
        record for record in caplog.records if record.message.startswith("Gemini retry scheduled")
    )
    success_record = next(
        record for record in caplog.records
        if record.message.startswith("Gemini generation completed")
    )
    assert retry_record.attempt_number == 1
    assert retry_record.failure_category == "provider_timeout"
    assert success_record.attempt_number == 2
    assert "attempt_number=1" in retry_record.message
    assert "model=configured-model" in retry_record.message


def test_gateway_uses_only_an_explicit_configured_fallback(monkeypatch, caplog):
    not_found = ServerError(
        code=404,
        response_json={"error": {"message": "model unavailable", "status": "NOT_FOUND"}},
    )

    class FallbackModels:
        def __init__(self):
            self.calls = []

        def generate_content(self, **kwargs):
            self.calls.append(kwargs)
            if len(self.calls) == 1:
                raise not_found
            return SimpleNamespace(text=json.dumps({"answer": "", "citation_chunk_ids": []}))

    monkeypatch.setattr(gateway_module, "sleep", lambda seconds: None)
    client = SimpleNamespace(models=FallbackModels())
    gateway = GeminiGateway(
        api_key="test-key",
        model_name="configured-model",
        fallback_model="configured-fallback",
        client=client,
    )

    with caplog.at_level(logging.INFO, logger="app.services.llm_gateway"):
        gateway.generate_answer("Question?", [])

    assert [call["model"] for call in client.models.calls] == [
        "configured-model",
        "configured-fallback",
    ]
    assert any(
        record.message.startswith("Gemini fallback selected") for record in caplog.records
    )


def test_gateway_uses_fallback_only_after_primary_retry_fails(monkeypatch, caplog):
    timeout_response = {
        "error": {"message": "deadline expired", "status": "DEADLINE_EXCEEDED"}
    }

    class RepeatedTimeoutModels:
        def __init__(self):
            self.calls = []

        def generate_content(self, **kwargs):
            self.calls.append(kwargs)
            if len(self.calls) <= 2:
                raise ServerError(code=504, response_json=timeout_response)
            return SimpleNamespace(text=json.dumps({"answer": "", "citation_chunk_ids": []}))

    monkeypatch.setattr(gateway_module, "sleep", lambda seconds: None)
    client = SimpleNamespace(models=RepeatedTimeoutModels())
    gateway = GeminiGateway(
        api_key="test-key",
        model_name="configured-model",
        fallback_model="configured-fallback",
        client=client,
    )

    with caplog.at_level(logging.INFO, logger="app.services.llm_gateway"):
        gateway.generate_answer("Question?", [])

    assert [call["model"] for call in client.models.calls] == [
        "configured-model",
        "configured-model",
        "configured-fallback",
    ]
    events = [record.message for record in caplog.records]
    assert events[0].startswith("Gemini retry scheduled")
    assert events[1].startswith("Gemini fallback selected")


def test_gateway_does_not_retry_quota_errors(monkeypatch):
    quota_error = ServerError(
        code=429,
        response_json={"error": {"message": "quota exceeded", "status": "RESOURCE_EXHAUSTED"}},
    )

    class QuotaModels:
        def __init__(self):
            self.calls = 0

        def generate_content(self, **kwargs):
            self.calls += 1
            raise quota_error

    monkeypatch.setattr(gateway_module, "sleep", lambda seconds: None)
    client = SimpleNamespace(models=QuotaModels())
    gateway = GeminiGateway(api_key="test-key", model_name="configured-model", client=client)

    with pytest.raises(ServerError):
        gateway.generate_answer("Question?", [])

    assert client.models.calls == 1


def test_gateway_minimal_diagnostic_uses_no_retrieved_evidence():
    client = FakeClient(["OK"])
    gateway = GeminiGateway(api_key="test-key", model_name="configured-model", client=client)

    gateway.diagnostic_ping()

    request = client.models.calls[0]
    assert request["contents"] == "Reply with exactly: OK"
    assert request["config"]["max_output_tokens"] == 8


def test_gateway_bounds_oversized_and_duplicate_evidence_context():
    client = FakeClient([json.dumps({"answer": "", "citation_chunk_ids": []})])
    gateway = GeminiGateway(api_key="test-key", model_name="configured-model", client=client)
    passages = []
    for index in range(12):
        passages.append(
            RetrievedChunk(
                chunk=SimpleNamespace(
                    chunk_id=f"chunk-{index}",
                    text=f"Passage {index}: " + ("relevant official text " * 90),
                    section=str(index),
                    page_number=index + 1,
                    document=SimpleNamespace(
                        title=f"Official source {index}",
                        issuing_body="SECP",
                        effective_date="2026-06-30",
                    ),
                ),
                similarity=1 - index / 20,
            )
        )
    passages.append(passages[0])

    gateway.generate_answer("What does the source say?", passages)

    payload = json.loads(client.models.calls[0]["contents"])
    assert len(payload["evidence"]) <= 5
    assert len({item["chunk_id"] for item in payload["evidence"]}) == len(payload["evidence"])
    assert sum(len(item["text"]) for item in payload["evidence"]) <= 6_000
    assert payload["evidence"][0]["chunk_id"] == "chunk-0"
