"""Job board request and response contracts (FR-6, FR-24, FR-25)."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


EmploymentType = Literal["job", "internship"]
ApplicationStatus = Literal["submitted", "reviewing", "shortlisted", "rejected", "withdrawn"]


def _reject_whitespace_only(value: str) -> str:
    if not value.strip():
        raise ValueError("Field cannot contain only whitespace")
    return value


class JobListingCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=10, max_length=20_000)
    employment_type: EmploymentType
    location: str = Field(min_length=2, max_length=255)
    is_remote: bool = False

    @field_validator("title", "description", "location")
    @classmethod
    def require_nonblank_text(cls, value: str) -> str:
        return _reject_whitespace_only(value)


class JobListingPatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default=None, min_length=3, max_length=200)
    description: str | None = Field(default=None, min_length=10, max_length=20_000)
    employment_type: EmploymentType | None = None
    location: str | None = Field(default=None, min_length=2, max_length=255)
    is_remote: bool | None = None
    status: Literal["open", "closed"] | None = None

    @field_validator("title", "description", "location")
    @classmethod
    def require_nonblank_text(cls, value: str) -> str:
        return _reject_whitespace_only(value)

    @model_validator(mode="after")
    def require_update_values(self) -> "JobListingPatch":
        if not self.model_fields_set:
            raise ValueError("At least one listing field must be provided")
        if any(getattr(self, field) is None for field in self.model_fields_set):
            raise ValueError("Listing fields cannot be set to null")
        return self


class JobListingRead(BaseModel):
    id: int
    startup_id: int
    startup_name: str
    title: str
    description: str
    employment_type: EmploymentType
    location: str
    is_remote: bool
    status: Literal["open", "closed"]
    created_at: datetime
    updated_at: datetime | None


class JobApplicationCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    cover_letter: str | None = Field(default=None, max_length=5_000)


class JobApplicationStatusUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["reviewing", "shortlisted", "rejected"]


class TalentJobApplicationRead(BaseModel):
    id: int
    job_id: int
    job_title: str
    startup_id: int
    startup_name: str
    status: ApplicationStatus
    cover_letter: str | None
    created_at: datetime
    updated_at: datetime | None


class FounderJobApplicationRead(BaseModel):
    id: int
    job_id: int
    candidate_user_id: int
    candidate_full_name: str
    candidate_email: str
    status: ApplicationStatus
    cover_letter: str | None
    created_at: datetime
    updated_at: datetime | None
