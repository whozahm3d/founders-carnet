"""Typed request and model-output schemas for Features 2 to 4."""

from datetime import datetime
from typing import Literal

from pydantic import (
    AnyHttpUrl,
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)


class TalentProfileWrite(BaseModel):
    model_config = ConfigDict(extra="forbid")

    consent_accepted: bool
    github_url: AnyHttpUrl | None = None

    @field_validator("github_url")
    @classmethod
    def require_public_github_url(cls, value: AnyHttpUrl | None) -> AnyHttpUrl | None:
        if value is None:
            return None
        if value.scheme != "https" or value.username or value.password:
            raise ValueError("GitHub URL must use HTTPS without credentials")
        host = value.host.casefold().rstrip(".")
        if host != "github.com" and not host.endswith(".github.com"):
            raise ValueError("GitHub URL must use github.com")
        return value


class TalentProfileRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    github_url: str | None
    consent_version: str
    consented_at: datetime


class EcosystemProfileWrite(BaseModel):
    consent_accepted: bool
    sector: str = Field(min_length=1, max_length=100)
    stages: list[str] = Field(min_length=1, max_length=4)
    skills: list[str] = Field(default_factory=list, max_length=50)
    availability: Literal["open", "limited", "closed"]
    ticket_min: float | None = Field(default=None, ge=0)
    ticket_max: float | None = Field(default=None, ge=0)
    location: str = Field(min_length=1, max_length=255)
    summary: str = Field(min_length=1, max_length=3000)
    is_open: bool = True

    @model_validator(mode="after")
    def validate_profile_state(self) -> "EcosystemProfileWrite":
        if self.availability == "closed" and self.is_open:
            raise ValueError("A closed profile must set is_open to false")
        if (
            self.ticket_min is not None
            and self.ticket_max is not None
            and self.ticket_min > self.ticket_max
        ):
            raise ValueError("ticket_max must be at least ticket_min")
        return self


class EcosystemProfileRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    sector: str
    stages: list[str]
    skills: list[str]
    availability: Literal["open", "limited", "closed"]
    ticket_min: float | None
    ticket_max: float | None
    location: str
    summary: str
    is_open: bool
    consent_version: str
    consented_at: datetime


class MatchRead(BaseModel):
    id: int
    startup_id: int
    startup_name: str
    candidate_user_id: int
    candidate_role: str
    sector: str
    location: str
    semantic_similarity: float
    score: float
    factors: dict[str, float]
    founder_accepted: bool
    candidate_accepted: bool
    mutual_acceptance: bool
    request_status: Literal["recommended", "pending", "accepted", "declined"]
    contact_email: str | None


class DimensionResult(BaseModel):
    dimension: Literal[
        "problem_clarity",
        "market_definition",
        "differentiation",
        "business_model_coherence",
        "traction",
        "team",
        "scalability",
    ]
    score: int = Field(ge=1, le=5)
    reasoning: str = Field(min_length=1, max_length=1200)
    next_action: str = Field(min_length=1, max_length=500)


class ReadinessResult(BaseModel):
    dimensions: list[DimensionResult] = Field(min_length=7, max_length=7)
    rubric_version: Literal["readiness-v1"] = "readiness-v1"

    @model_validator(mode="after")
    def require_all_dimensions_once(self) -> "ReadinessResult":
        expected = {
            "problem_clarity",
            "market_definition",
            "differentiation",
            "business_model_coherence",
            "traction",
            "team",
            "scalability",
        }
        actual = [item.dimension for item in self.dimensions]
        if set(actual) != expected or len(actual) != len(set(actual)):
            raise ValueError("All seven readiness dimensions must appear exactly once")
        return self


class ReadinessRead(BaseModel):
    id: int
    startup_id: int
    rubric_version: str
    result: ReadinessResult
    created_at: datetime


class ReadinessScore(BaseModel):
    score: int = Field(ge=1, le=5)
    reasoning: str = Field(min_length=1, max_length=1200)


class PitchTurnResult(BaseModel):
    next_question: str | None = Field(default=None, max_length=1000)
    finished: bool
    clarity: ReadinessScore | None = None
    confidence: ReadinessScore | None = None
    content: ReadinessScore | None = None

    @model_validator(mode="after")
    def match_completion_fields(self) -> "PitchTurnResult":
        scores = (self.clarity, self.confidence, self.content)
        if self.finished and (
            self.next_question is not None or any(score is None for score in scores)
        ):
            raise ValueError(
                "A finished pitch must contain the three scores and no next question"
            )
        if not self.finished and (
            not self.next_question or any(score is not None for score in scores)
        ):
            raise ValueError(
                "An unfinished pitch needs a follow-up question and no scores"
            )
        return self


class PitchStart(BaseModel):
    startup_id: int
    persona: str = Field(min_length=1, max_length=100)


class PitchAnswer(BaseModel):
    answer: str = Field(min_length=1, max_length=5000)


class PitchTurnRead(BaseModel):
    turn_number: int
    speaker: str
    content: str


class PitchSessionRead(BaseModel):
    id: int
    startup_id: int
    persona: str
    status: Literal["active", "incomplete", "completed"]
    scores: dict[str, object] | None
    rubric_version: str
    created_at: datetime
    completed_at: datetime | None
    turns: list[PitchTurnRead]
