import httpx
import pytest

from app.services.portfolio_verification import (
    PORTFOLIO_CONTENT_LIMIT,
    FirecrawlPortfolioFetcher,
    PortfolioFetchError,
)


def test_portfolio_fetch_uses_configured_provider_and_caps_extracted_content():
    observed = {}

    def handler(request):
        observed["url"] = str(request.url)
        observed["authorization"] = request.headers["Authorization"]
        observed["payload"] = request.read()
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {"markdown": "x" * (PORTFOLIO_CONTENT_LIMIT + 100)},
            },
        )

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        fetcher = FirecrawlPortfolioFetcher(
            api_key="test-key", timeout_ms=1000, client=client
        )
        content = fetcher.fetch("https://example.org/product")

    assert observed["url"] == "https://api.firecrawl.dev/v2/scrape"
    assert observed["authorization"] == "Bearer test-key"
    assert len(content) == PORTFOLIO_CONTENT_LIMIT
    assert b"onlyMainContent" in observed["payload"]


def test_portfolio_fetch_errors_are_sanitized():
    def handler(_request):
        return httpx.Response(503, text="provider response containing private details")

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        fetcher = FirecrawlPortfolioFetcher(
            api_key="test-key", timeout_ms=1000, client=client
        )
        with pytest.raises(PortfolioFetchError) as error:
            fetcher.fetch("https://example.org/private")

    assert str(error.value) == "Portfolio check is temporarily unavailable"
    assert "private" not in str(error.value)
