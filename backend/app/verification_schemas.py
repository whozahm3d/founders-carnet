"""Request/response contracts for profile verification (FR-12, FR-14, FR-15, FR-16, FR-19, FR-20, FR-21)."""

from datetime import datetime
from ipaddress import ip_address
from typing import Literal

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field, field_validator

PortfolioVerdict = Literal["consistent", "inconsistent", "insufficient"]
ProfileVerificationStatus = Literal[
    "pending_review",
    "auto_verified",
    "auto_rejected",
    "appeal_pending",
    "verified",
    "rejected",
    "blocked",
]


class ProfileVerificationWrite(BaseModel):
    model_config = ConfigDict(extra="forbid")

    processing_consent_accepted: bool
    trust_notice_accepted: bool
    portfolio_url: AnyHttpUrl = Field(max_length=2048)
    secp_entity_name: str = Field(min_length=2, max_length=255)
    secp_registration_number: str = Field(min_length=1, max_length=100)

    @field_validator("portfolio_url")
    @classmethod
    def require_https_portfolio(cls, value: AnyHttpUrl) -> AnyHttpUrl:
        if value.scheme != "https":
            raise ValueError("Portfolio URL must use HTTPS")
        if value.username or value.password:
            raise ValueError("Portfolio URL cannot contain credentials")
        host = value.host.casefold().rstrip(".")
        if host in {"localhost", "localhost.localdomain"} or host.endswith(
            (".localhost", ".local", ".internal")
        ):
            raise ValueError("Portfolio URL must use a public hostname")
        try:
            address = ip_address(host)
        except ValueError:
            address = None
        if address is not None and not address.is_global:
            raise ValueError("Portfolio URL must use a public hostname")
        return value

    @field_validator("secp_entity_name", "secp_registration_number")
    @classmethod
    def strip_required_secp_values(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("SECP entity details cannot be blank")
        return normalized


class PortfolioLinkAssessment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    result: PortfolioVerdict
    reason: str = Field(min_length=1, max_length=500)


class ProfileVerificationRead(BaseModel):
    id: int
    user_id: int
    portfolio_url: str
    secp_entity_name: str
    secp_registration_number: str
    status: ProfileVerificationStatus
    score: float
    band: Literal["high", "review", "low"]
    signals: dict[str, object]
    reason: str
    threshold_version: str
    appeal_used: bool
    rescore_locked: bool
    created_at: datetime
    updated_at: datetime | None


class VerificationAppealWrite(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reason: str = Field(min_length=10, max_length=1000)
    added_evidence: str = Field(min_length=10, max_length=5000)

    @field_validator("reason", "added_evidence")
    @classmethod
    def strip_appeal_values(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("Appeal fields cannot be blank")
        return normalized


class ProfileReportWrite(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reason: str = Field(min_length=10, max_length=1000)

    @field_validator("reason")
    @classmethod
    def strip_report_reason(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("Report reason cannot be blank")
        return normalized


class ProfileReportRead(BaseModel):
    id: int
    status: Literal["received"] = "received"


class AdminAppealRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    reason: str
    added_evidence: str
    status: Literal["pending", "approved", "rejected"]
    decision_reason: str | None
    created_at: datetime


class AdminVerificationSignalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    signal_name: str
    score: float
    outcome: str
    input_snapshot: dict[str, object]
    reason: str


class AdminVerificationQueueItem(BaseModel):
    verification_id: int
    user_id: int
    user_role: str
    status: ProfileVerificationStatus
    score: float
    band: Literal["high", "review", "low"]
    signals: dict[str, object]
    signal_details: list[AdminVerificationSignalRead]
    reason: str
    threshold_version: str
    appeal: AdminAppealRead | None
    report_count: int
    created_at: datetime


class AdminVerificationDecisionWrite(BaseModel):
    model_config = ConfigDict(extra="forbid")

    decision: Literal["approve", "reject"]
    reason: str = Field(min_length=1, max_length=1000)

    @field_validator("reason")
    @classmethod
    def strip_decision_reason(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("Decision reason cannot be blank")
        return normalized


class VerificationScoringResult(BaseModel):
    score: float = Field(ge=0, le=1)
    band: Literal["high", "review", "low"]
    status: ProfileVerificationStatus
    signals: dict[str, object]
    reason: str
    threshold_version: str
