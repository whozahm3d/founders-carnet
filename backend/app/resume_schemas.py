"""Resume optimization input and output contracts (FR-5, NFR-7)."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ResumeLineSuggestion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    line_number: int = Field(ge=1)
    before: str = Field(min_length=1, max_length=2000)
    after: str = Field(min_length=1, max_length=2000)
    reasoning: str = Field(min_length=1, max_length=500)


class ResumeOptimizationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    suggestions: list[ResumeLineSuggestion] = Field(max_length=30)


class ResumeOptimizationRead(BaseModel):
    id: int
    status: Literal["complete", "generation_failed"]
    target_role: str
    suggestions: list[ResumeLineSuggestion] | None
    prompt_version: str
    model_name: str
    created_at: datetime
