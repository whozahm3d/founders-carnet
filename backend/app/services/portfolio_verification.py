"""Fetch only user-submitted portfolio pages through the configured Firecrawl service (FR-20)."""

from __future__ import annotations

import logging

import httpx
from fastapi import HTTPException, status

from app.config import get_settings

FIRECRAWL_SCRAPE_URL = "https://api.firecrawl.dev/v2/scrape"
PORTFOLIO_CONTENT_LIMIT = 10_000
logger = logging.getLogger(__name__)


class PortfolioFetchError(RuntimeError):
    """Portfolio content could not be obtained from the configured provider."""


class FirecrawlPortfolioFetcher:
    def __init__(
        self, *, api_key: str, timeout_ms: int, client: httpx.Client | None = None
    ) -> None:
        self._api_key = api_key
        self._timeout_ms = timeout_ms
        self._client = client

    def fetch(self, url: str) -> str:
        client = self._client or httpx.Client(timeout=self._timeout_ms / 1000)
        owns_client = self._client is None
        try:
            response = client.post(
                FIRECRAWL_SCRAPE_URL,
                headers={"Authorization": f"Bearer {self._api_key}"},
                json={"url": url, "formats": ["markdown"], "onlyMainContent": True},
            )
            response.raise_for_status()
            body = response.json()
            if isinstance(body, dict) and body.get("success") is False:
                return ""
            if not isinstance(body, dict) or body.get("success") is not True:
                raise ValueError("Invalid portfolio content response")
            data = body.get("data") if isinstance(body, dict) else None
            markdown = data.get("markdown") if isinstance(data, dict) else None
            if markdown is None:
                return ""
            if not isinstance(markdown, str):
                raise TypeError("Invalid portfolio content response")
            return markdown[:PORTFOLIO_CONTENT_LIMIT]
        except (httpx.HTTPError, ValueError, TypeError, AttributeError) as exc:
            # Avoid logging a user-supplied URL or provider response body.
            logger.warning(
                "Portfolio page fetch failed error_type=%s", type(exc).__name__
            )
            raise PortfolioFetchError(
                "Portfolio check is temporarily unavailable"
            ) from exc
        finally:
            if owns_client:
                client.close()


def get_portfolio_fetcher() -> FirecrawlPortfolioFetcher:
    settings = get_settings()
    if settings.firecrawl_api_key is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Profile verification is not configured",
        )
    return FirecrawlPortfolioFetcher(
        api_key=settings.firecrawl_api_key.get_secret_value(),
        timeout_ms=settings.firecrawl_request_timeout_ms,
    )
