from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class SecpCheckResult:
    outcome: str
    score: float
    reason: str


class SecpChecker(Protocol):
    def check(self, entity_name: str, registration_number: str) -> SecpCheckResult:
        """Return a manual-review state for submitted SECP details."""


class ManualSecpChecker:
    """Fake boundary for the manual official-record check used in this slice."""

    def check(self, entity_name: str, registration_number: str) -> SecpCheckResult:
        del entity_name, registration_number
        return SecpCheckResult(
            outcome="pending_manual_review",
            score=0.5,
            reason="A reviewer must compare the submitted details with official SECP records.",
        )


secp_checker: SecpChecker = ManualSecpChecker()


def get_secp_checker() -> SecpChecker:
    return secp_checker
