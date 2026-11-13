"""Contracts for the market research search and evidence-grounded synthesis (FR-4)."""

from datetime import datetime
from typing import Literal

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field, model_validator


class MarketResearchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    startup_id: int
    question: str = Field(min_length=5, max_length=500)


class CitedStatement(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(min_length=1, max_length=1500)
    source_ids: list[str] = Field(min_length=1, max_length=5)

    @model_validator(mode="after")
    def unique_source_ids(self) -> "CitedStatement":
        if len(set(self.source_ids)) != len(self.source_ids):
            raise ValueError("source_ids must be unique")
        return self


class CompetitorFinding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=200)
    finding: CitedStatement


class MarketResearchInterpretation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    overview: CitedStatement
    market_size: CitedStatement | None = None
    competitors: list[CompetitorFinding] = Field(max_length=10)
    opportunities: list[CitedStatement] = Field(max_length=10)


class ResearchEvidenceRead(BaseModel):
    source_id: str
    title: str
    url: AnyHttpUrl
    content: str
    published_date: str | None


class MarketResearchRead(BaseModel):
    id: int
    startup_id: int
    question: str
    status: Literal["complete", "insufficient_evidence", "generation_failed"]
    interpretation: MarketResearchInterpretation | None
    evidence: list[ResearchEvidenceRead]
    prompt_version: str
    model_name: str
    created_at: datetime
