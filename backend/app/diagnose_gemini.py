"""Run a short no-evidence Gemini diagnostic outside the compliance endpoint."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from time import perf_counter

import httpx

from app.config import get_settings
from app.services.llm_gateway import GeminiGateway, classify_provider_error


def main() -> int:
    settings = get_settings()
    print(f"configured_model={settings.gemini_model}")
    print(f"fallback_model={settings.gemini_fallback_model or 'not configured'}")
    print(f"request_timeout_ms={settings.gemini_request_timeout_ms}")
    try:
        sdk_version = version("google-genai")
    except PackageNotFoundError:
        sdk_version = "not installed"
    print(f"google_genai_sdk={sdk_version}")

    if settings.gemini_api_key is None:
        print("result=not_configured; GEMINI_API_KEY is missing")
        return 2

    gateway = GeminiGateway(
        api_key=settings.gemini_api_key.get_secret_value(),
        model_name=settings.gemini_model,
        fallback_model=settings.gemini_fallback_model,
        request_timeout_ms=settings.gemini_request_timeout_ms,
    )
    started_at = perf_counter()
    try:
        gateway.diagnostic_ping()
    except (httpx.HTTPError, RuntimeError, ValueError) as exc:
        status_code = getattr(exc, "code", None) or getattr(exc, "status_code", None)
        print(
            "result=failed "
            f"category={classify_provider_error(exc)} "
            f"error_type={type(exc).__name__} "
            f"status_code={status_code or 'unavailable'} "
            f"elapsed_ms={int((perf_counter() - started_at) * 1000)}"
        )
        return 1
    finally:
        gateway.close()

    print(f"result=success elapsed_ms={int((perf_counter() - started_at) * 1000)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
