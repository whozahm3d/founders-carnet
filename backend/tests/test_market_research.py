import httpx
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.market_research_schemas import (
    CitedStatement,
    CompetitorFinding,
    MarketResearchInterpretation,
)
from app.services.feature_ai import get_gateway
from app.services.web_search import (
    FirecrawlSearch,
    FirecrawlSearchError,
    SearchEvidence,
    get_market_search,
)

client = TestClient(app)
fake_search = None
fake_gateway = None


class FakeSearch:
    def __init__(self, results):
        self.results = results
        self.queries = []

    def search(self, query):
        self.queries.append(query)
        return self.results


class FakeGateway:
    model_name = "test-gemini-model"

    def __init__(self):
        self.calls = []
        self.unknown_source = False
        self.fail = False

    def generate_structured(self, *, response_schema, **kwargs):
        self.calls.append(kwargs)
        if self.fail:
            raise RuntimeError("mock provider error")
        source_id = "S999" if self.unknown_source else "S1"
        return MarketResearchInterpretation(
            overview=CitedStatement(
                text="The market is developing.", source_ids=[source_id]
            ),
            market_size=CitedStatement(
                text="The source estimates market growth.", source_ids=[source_id]
            ),
            competitors=[
                CompetitorFinding(
                    name="Example competitor",
                    finding=CitedStatement(
                        text="It serves small businesses.", source_ids=[source_id]
                    ),
                )
            ],
            opportunities=[],
        )


def setup_function():
    global fake_search, fake_gateway
    fake_search = FakeSearch(
        [
            SearchEvidence(
                title="Pakistan logistics market report",
                url="https://example.org/logistics",
                content="Publicly available market evidence.",
                published_date="2026-01-01",
            )
        ]
    )
    fake_gateway = FakeGateway()
    app.dependency_overrides[get_gateway] = lambda: fake_gateway
    app.dependency_overrides[get_market_search] = lambda: fake_search


def teardown_function():
    app.dependency_overrides.pop(get_gateway, None)
    app.dependency_overrides.pop(get_market_search, None)


def founder_and_startup(email="market-research@example.com"):
    registration = client.post(
        "/api/v1/auth/register/founder",
        json={
            "email": email,
            "password": "SecurePass123!",
            "full_name": "Market Founder",
            "consent_accepted": True,
        },
    )
    assert registration.status_code == 201, registration.text
    login = client.post(
        "/api/v1/auth/login", json={"email": email, "password": "SecurePass123!"}
    )
    assert login.status_code == 200, login.text
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
    profile = client.put(
        "/api/v1/founders/me/profile", headers=headers, json={"consent_accepted": True}
    )
    assert profile.status_code == 200, profile.text
    startup_response = client.post(
        "/api/v1/founders/me/startups",
        headers=headers,
        json={
            "name": "Routewise",
            "description": "Delivery tools for local shops.",
            "sector": "logistics",
            "stage": "mvp",
            "location": "Lahore, Pakistan",
            "business_model": "subscription",
            "traction_summary": "Pilot stage",
            "customer_count": 12,
        },
    )
    assert startup_response.status_code == 201, startup_response.text
    return headers, startup_response.json()


def test_firecrawl_search_sends_bounded_web_search_and_parses_evidence():
    requests = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {
                    "web": [
                        {
                            "title": "Pakistan startup sector report",
                            "url": "https://example.org/report",
                            "description": "A public market overview.",
                            "markdown": "The report summarizes startup activity.",
                            "metadata": {"publishedTime": "2026-01-05"},
                        }
                    ]
                },
            },
        )

    client = httpx.Client(transport=httpx.MockTransport(handler))
    search = FirecrawlSearch(api_key="test-key", client=client)

    evidence = search.search("Pakistan logistics startup competitors")

    request = requests[0]
    assert request.url.path == "/v2/search"
    assert request.headers["authorization"] == "Bearer test-key"
    assert request.read()
    import json

    payload = json.loads(request.content)
    assert payload["query"] == "Pakistan logistics startup competitors"
    assert payload["country"] == "PK"
    assert payload["limit"] <= 5
    assert payload["highlights"] is True
    assert "scrapeOptions" not in payload
    assert "linkedin.com" in payload["excludeDomains"]
    assert len(evidence) == 1
    assert evidence[0].title == "Pakistan startup sector report"
    assert evidence[0].content == "The report summarizes startup activity."
    assert str(evidence[0].url) == "https://example.org/report"
    client.close()


def test_firecrawl_rejects_malformed_search_response():
    client = httpx.Client(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(200, json={"success": True, "data": {}})
        )
    )
    search = FirecrawlSearch(api_key="test-key", client=client)

    with pytest.raises(FirecrawlSearchError):
        search.search("market size")

    client.close()


def test_firecrawl_provider_failure_is_sanitized():
    client = httpx.Client(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(401, json={"error": "secret detail"})
        )
    )
    search = FirecrawlSearch(api_key="test-key", client=client)

    with pytest.raises(FirecrawlSearchError) as captured:
        search.search("market size")

    assert "secret detail" not in str(captured.value)
    assert "test-key" not in str(captured.value)
    client.close()


def test_market_research_keeps_evidence_separate_and_stores_history():
    headers, startup = founder_and_startup()

    response = client.post(
        "/api/v1/market-research",
        headers=headers,
        json={
            "startup_id": startup["id"],
            "question": "Who are our local delivery competitors?",
        },
    )

    assert response.status_code == 201, response.text
    report = response.json()
    assert report["status"] == "complete"
    assert report["evidence"][0]["source_id"] == "S1"
    assert report["evidence"][0]["title"] == "Pakistan logistics market report"
    assert report["interpretation"]["overview"]["text"] == "The market is developing."
    assert report["interpretation"]["overview"]["source_ids"] == ["S1"]
    assert report["model_name"] == "test-gemini-model"
    assert fake_search.queries[0].startswith("Pakistan logistics Routewise")
    sent = fake_gateway.calls[0]
    assert sent["payload"]["public_web_evidence"][0]["source_id"] == "S1"
    assert "only the supplied public web evidence" in sent["system_instruction"]

    history = client.get(
        f"/api/v1/startups/{startup['id']}/market-research", headers=headers
    )
    assert history.status_code == 200
    assert history.json()[0]["id"] == report["id"]
    assert history.json()[0]["evidence"] == report["evidence"]


def test_market_research_with_no_search_results_abstains_without_llm_call():
    headers, startup = founder_and_startup("market-empty@example.com")
    fake_search.results = []

    response = client.post(
        "/api/v1/market-research",
        headers=headers,
        json={
            "startup_id": startup["id"],
            "question": "What is the market size?",
        },
    )

    assert response.status_code == 201, response.text
    assert response.json()["status"] == "insufficient_evidence"
    assert response.json()["evidence"] == []
    assert response.json()["interpretation"] is None
    assert fake_gateway.calls == []


def test_market_research_rejects_unknown_citation_and_keeps_evidence_log():
    headers, startup = founder_and_startup("market-invalid-citation@example.com")
    fake_gateway.unknown_source = True

    response = client.post(
        "/api/v1/market-research",
        headers=headers,
        json={
            "startup_id": startup["id"],
            "question": "Who are our local delivery competitors?",
        },
    )

    assert response.status_code == 502
    history = client.get(
        f"/api/v1/startups/{startup['id']}/market-research", headers=headers
    )
    assert history.json()[0]["status"] == "generation_failed"
    assert history.json()[0]["evidence"][0]["source_id"] == "S1"


def test_market_research_failure_preserves_search_evidence_and_hides_provider_error():
    headers, startup = founder_and_startup("market-provider-failure@example.com")
    fake_gateway.fail = True

    response = client.post(
        "/api/v1/market-research",
        headers=headers,
        json={
            "startup_id": startup["id"],
            "question": "Who are our local delivery competitors?",
        },
    )

    assert response.status_code == 502
    assert "mock provider error" not in response.text
    history = client.get(
        f"/api/v1/startups/{startup['id']}/market-research", headers=headers
    )
    assert history.json()[0]["status"] == "generation_failed"
    assert history.json()[0]["evidence"]


def test_market_research_is_founder_only_and_startup_owned():
    _headers, startup = founder_and_startup("market-owner@example.com")
    other_headers, _ = founder_and_startup("market-other@example.com")

    response = client.post(
        "/api/v1/market-research",
        headers=other_headers,
        json={
            "startup_id": startup["id"],
            "question": "Who are our local delivery competitors?",
        },
    )

    assert response.status_code == 404
    assert fake_search.queries == []
