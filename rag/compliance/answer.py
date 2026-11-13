"""Versioned structured output contract for compliance answers (FR-8, NFR-12)."""

from __future__ import annotations

from pydantic import AliasChoices, BaseModel, ConfigDict, Field

ANSWER_PROMPT_VERSION = "compliance-answer-v2"


class AnswerOutput(BaseModel):
    """The JSON contract returned by the LLM Gateway before evidence checks."""

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    answer: str = Field(default="", max_length=6000)
    citation_chunk_ids: list[str] = Field(
        default_factory=list,
        max_length=10,
        validation_alias=AliasChoices("citations", "citation_chunk_ids"),
        serialization_alias="citations",
    )
    abstain: bool = False
    abstain_reason: str | None = Field(default=None, max_length=300)

    @property
    def citations(self) -> list[str]:
        return self.citation_chunk_ids
