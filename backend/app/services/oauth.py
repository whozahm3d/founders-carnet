from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class OAuthProfile:
    provider_subject: str
    email: str
    full_name: str


class LinkedInProvider(Protocol):
    def authenticate(self, authorization_code: str) -> OAuthProfile:
        """Exchange a provider authorization code for a minimal identity."""


class FakeLinkedInProvider:
    """Deterministic provider for tests and local development only."""

    def authenticate(self, authorization_code: str) -> OAuthProfile:
        if authorization_code != "fake-linkedin-code":
            raise ValueError("LinkedIn authentication failed")
        return OAuthProfile(
            provider_subject="fake-linkedin-subject-1",
            email="fake-linkedin-user@example.com",
            full_name="Fake LinkedIn User",
        )


linkedin_provider: LinkedInProvider = FakeLinkedInProvider()
