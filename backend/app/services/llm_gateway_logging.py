"""Persist sanitized metadata for model attempts without storing prompt data."""

from typing import Any

from app.database import SessionLocal
from app.feature_models import LLMGatewayCallLog


def write_gateway_call_log(event: dict[str, Any]) -> None:
    with SessionLocal() as session:
        session.add(LLMGatewayCallLog(**event))
        session.commit()
