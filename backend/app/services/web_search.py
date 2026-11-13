"""Bounded public-web search through Firecrawl (FR-4)."""

from __future__ import annotations

import logging
from time import perf_counter
from typing import Any

import httpx
from fastapi import HTTPException, status
from pydantic import AnyHttpUrl, BaseModel, Field

from app.config import get_settings

FIRECRAWL_SEARCH_URL = "https://api.firecrawl.dev/v2/search"
FIRECRAWL_MAX_RESULTS = 5
FIRECRAWL_MAX_CONTENT_CHARS = 3_000
FIRECRAWL_REQUEST_TIMEOUT_MS = 25_000
FIRECRAWL_HTTP_TIMEOUT_SECONDS = 30.0
EXCLUDED_PROFILE_DOMAINS = [
    "linkedin.com",
    "facebook.com",
    "instagram.com",
    "x.com",
    "twitter.com",
]

logger = logging.getLogger(__name__)


class SearchEvidence(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    url: AnyHttpUrl
    content: str = Field(min_length=1, max_length=FIRECRAWL_MAX_CONTENT_CHARS)
    published_date: str | None = Field(default=None, max_length=80)


class FirecrawlSearchError(RuntimeError):
    """Provider or response failure without credential or payload details."""


class FirecrawlSearch:
    def __init__(
        self,
        *,
        api_key: str,
        request_timeout_ms: int = FIRECRAWL_REQUEST_TIMEOUT_MS,
        client: httpx.Client | None = None,
    ) -> None:
        if not api_key:
            raise ValueError("Firecrawl API key is not configured")
        if not 5_000 <= request_timeout_ms <= 55_000:
            raise ValueError(
                "Firecrawl request timeout must be between 5000 and 55000 ms"
            )
        self._api_key = api_key
        self._request_timeout_ms = request_timeout_ms
        self._client = client

    def search(self, query: str) -> list[SearchEvidence]:
        payload = {
            "query": query,
            "limit": FIRECRAWL_MAX_RESULTS,
            "sources": [{"type": "web"}],
            "country": "PK",
            "safe": True,
            "timeout": self._request_timeout_ms,
            "highlights": True,
            "excludeDomains": EXCLUDED_PROFILE_DOMAINS,
        }
        request_started = perf_counter()
        client = self._client or httpx.Client(timeout=FIRECRAWL_HTTP_TIMEOUT_SECONDS)
        owns_client = self._client is None
        try:
            response = client.post(
                FIRECRAWL_SEARCH_URL,
                headers={
                    "Authorization": f"Bearer {self._api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            response.raise_for_status()
            body = response.json()
            results = self._parse_results(body)
        except (httpx.HTTPError, ValueError, TypeError, KeyError) as exc:
            logger.exception(
                "Firecrawl search failed status_code=%s elapsed_ms=%d",
                getattr(getattr(exc, "response", None), "status_code", "unavailable"),  # noqa: TRY401
                int((perf_counter() - request_started) * 1000),
            )
            raise FirecrawlSearchError(
                "Public web search is temporarily unavailable"
            ) from exc
        finally:
            if owns_client:
                client.close()

        logger.info(
            "Firecrawl search completed result_count=%d elapsed_ms=%d",
            len(results),
            int((perf_counter() - request_started) * 1000),
        )
        return results

    @staticmethod
    def _parse_results(body: Any) -> list[SearchEvidence]:
        if not isinstance(body, dict) or body.get("success") is not True:
            raise ValueError("Invalid Firecrawl response")
        data = body.get("data")
        web_results = data.get("web") if isinstance(data, dict) else None
        if not isinstance(web_results, list):
            raise TypeError("Invalid Firecrawl results")

        evidence: list[SearchEvidence] = []
        seen_urls: set[str] = set()
        for item in web_results:
            if not isinstance(item, dict):
                continue
            url = item.get("url")
            title = item.get("title")
            if not isinstance(url, str) or not isinstance(title, str):
                continue
            normalized_url = url.strip()
            if not normalized_url or normalized_url.casefold() in seen_urls:
                continue
            metadata = item.get("metadata")
            metadata = metadata if isinstance(metadata, dict) else {}
            content = item.get("markdown") or item.get("description")
            if not isinstance(content, str) or not content.strip():
                continue
            content = content.strip()[:FIRECRAWL_MAX_CONTENT_CHARS]
            try:
                source = SearchEvidence(
                    title=title.strip()[:300],
                    url=normalized_url,
                    content=content,
                    published_date=metadata.get("publishedTime") or item.get("date"),
                )
            except (ValueError, TypeError):
                continue
            evidence.append(source)
            seen_urls.add(normalized_url.casefold())
            if len(evidence) >= FIRECRAWL_MAX_RESULTS:
                break
        return evidence


def get_market_search() -> FirecrawlSearch:
    settings = get_settings()
    if settings.firecrawl_api_key is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Market research search is not configured",
        )
    return FirecrawlSearch(
        api_key=settings.firecrawl_api_key.get_secret_value(),
        request_timeout_ms=settings.firecrawl_request_timeout_ms,
    )
