"""Models for matching, readiness, and pitch practice (FR-2, FR-3, FR-7, FR-10, FR-28, FR-29)."""

from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, DateTime, Float, ForeignKey, Index, Integer, JSON, String, Text, UniqueConstraint, func
from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models import VECTOR_TYPE, Base


class TalentProfile(Base):
    """Talent-specific profile data, including an optional public GitHub link (FR-13)."""

    __tablename__ = "talent_profiles"
    __table_args__ = (UniqueConstraint("user_id", name="uq_talent_profiles_user"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    github_url: Mapped[str | None] = mapped_column(String(2048))
    consent_version: Mapped[str] = mapped_column(String(80), nullable=False)
    consented_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


class EcosystemProfile(Base):
    __tablename__ = "ecosystem_profiles"
    __table_args__ = (
        CheckConstraint("user_id > 0", name="ck_ecosystem_profiles_user_id"),
        Index("ix_ecosystem_profiles_open", "is_open"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    sector: Mapped[str] = mapped_column(String(100), nullable=False)
    stages: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    skills: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    availability: Mapped[str] = mapped_column(String(30), nullable=False)
    ticket_min: Mapped[float | None] = mapped_column(nullable=True)
    ticket_max: Mapped[float | None] = mapped_column(nullable=True)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    consent_version: Mapped[str] = mapped_column(String(50), nullable=False)
    consented_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    is_open: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    embedding: Mapped[list[float] | None] = mapped_column(VECTOR_TYPE)
    embedding_model: Mapped[str | None] = mapped_column(String(255))
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


class MatchRecord(Base):
    __tablename__ = "match_records"
    __table_args__ = (
        UniqueConstraint("startup_id", "candidate_user_id", name="uq_match_startup_candidate"),
        CheckConstraint("score >= 0 AND score <= 1", name="ck_match_records_score"),
        CheckConstraint(
            "request_status IN ('recommended', 'pending', 'accepted', 'declined')",
            name="ck_match_records_request_status",
        ),
        Index("ix_match_records_startup_id", "startup_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    startup_id: Mapped[int] = mapped_column(ForeignKey("startups.id", ondelete="CASCADE"), nullable=False)
    candidate_user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    factors: Mapped[dict[str, float]] = mapped_column(JSON, nullable=False)
    similarity: Mapped[float] = mapped_column(default=0.0, nullable=False)
    score: Mapped[float] = mapped_column(nullable=False)
    founder_accepted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    candidate_accepted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    request_status: Mapped[str] = mapped_column(
        String(20), default="recommended", server_default="recommended", nullable=False
    )
    requester_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


class ReadinessAssessment(Base):
    __tablename__ = "readiness_assessments"
    __table_args__ = (Index("ix_readiness_startup_created", "startup_id", "created_at"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    startup_id: Mapped[int] = mapped_column(ForeignKey("startups.id", ondelete="CASCADE"), nullable=False)
    rubric_version: Mapped[str] = mapped_column(String(50), nullable=False)
    result: Mapped[dict[str, object]] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)


class PitchSession(Base):
    __tablename__ = "pitch_sessions"
    __table_args__ = (Index("ix_pitch_sessions_user_created", "user_id", "created_at"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    startup_id: Mapped[int] = mapped_column(ForeignKey("startups.id", ondelete="CASCADE"), nullable=False)
    persona: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)
    scores: Mapped[dict[str, object] | None] = mapped_column(JSON)
    rubric_version: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime)


class PitchTurn(Base):
    __tablename__ = "pitch_turns"
    __table_args__ = (
        UniqueConstraint("session_id", "turn_number", name="uq_pitch_session_turn"),
        CheckConstraint("turn_number >= 1", name="ck_pitch_turns_turn_number"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("pitch_sessions.id", ondelete="CASCADE"), nullable=False)
    turn_number: Mapped[int] = mapped_column(Integer, nullable=False)
    speaker: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)


class MarketResearchReport(Base):
    __tablename__ = "market_research_reports"
    __table_args__ = (Index("ix_market_research_startup_created", "startup_id", "created_at"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    startup_id: Mapped[int] = mapped_column(ForeignKey("startups.id", ondelete="CASCADE"), nullable=False)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    interpretation: Mapped[dict[str, object] | None] = mapped_column(JSON)
    evidence: Mapped[list[dict[str, object]]] = mapped_column(JSON, nullable=False)
    prompt_version: Mapped[str] = mapped_column(String(80), nullable=False)
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)


class ResumeOptimization(Base):
    __tablename__ = "resume_optimizations"
    __table_args__ = (
        Index("ix_resume_optimizations_user_created", "user_id", "created_at"),
        UniqueConstraint("storage_key", name="uq_resume_optimizations_storage_key"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    storage_key: Mapped[str] = mapped_column(String(32), nullable=False)
    file_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    target_role: Mapped[str] = mapped_column(String(120), nullable=False)
    processing_consent_version: Mapped[str] = mapped_column(String(80), nullable=False)
    processing_consented_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    suggestions: Mapped[list[dict[str, object]] | None] = mapped_column(JSON)
    prompt_version: Mapped[str] = mapped_column(String(80), nullable=False)
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)


class JobListing(Base):
    __tablename__ = "job_listings"
    __table_args__ = (
        CheckConstraint("employment_type IN ('job', 'internship')", name="ck_job_listings_type"),
        CheckConstraint("status IN ('open', 'closed')", name="ck_job_listings_status"),
        Index("ix_job_listings_status_created", "status", "created_at"),
        Index("ix_job_listings_startup_id", "startup_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    startup_id: Mapped[int] = mapped_column(ForeignKey("startups.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    employment_type: Mapped[str] = mapped_column(String(20), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    is_remote: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="open", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


class JobSave(Base):
    __tablename__ = "job_saves"
    __table_args__ = (
        UniqueConstraint("job_id", "user_id", name="uq_job_saves_job_user"),
        Index("ix_job_saves_user_created", "user_id", "created_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("job_listings.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)


class JobApplication(Base):
    __tablename__ = "job_applications"
    __table_args__ = (
        UniqueConstraint("job_id", "candidate_user_id", name="uq_job_applications_job_candidate"),
        CheckConstraint(
            "status IN ('submitted', 'reviewing', 'shortlisted', 'rejected', 'withdrawn')",
            name="ck_job_applications_status",
        ),
        Index("ix_job_applications_job_created", "job_id", "created_at"),
        Index("ix_job_applications_candidate_created", "candidate_user_id", "created_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("job_listings.id", ondelete="CASCADE"), nullable=False)
    candidate_user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    cover_letter: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="submitted", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


class ProfileVerification(Base):
    """Scored and consented verification record for mentors and investors (FR-12, FR-14, FR-15, FR-19)."""

    __tablename__ = "profile_verifications"
    __table_args__ = (
        CheckConstraint("score >= 0 AND score <= 1", name="ck_profile_verifications_score"),
        CheckConstraint(
            "status IN ('pending_review', 'auto_verified', 'auto_rejected', 'appeal_pending', 'verified', 'rejected', 'blocked')",
            name="ck_profile_verifications_status",
        ),
        CheckConstraint("band IN ('high', 'review', 'low')", name="ck_profile_verifications_band"),
        UniqueConstraint("user_id", name="uq_profile_verifications_user"),
        Index("ix_profile_verifications_status_created", "status", "created_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    portfolio_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    secp_entity_name: Mapped[str] = mapped_column(String(255), nullable=False)
    secp_registration_number: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    band: Mapped[str] = mapped_column(String(20), nullable=False)
    signals: Mapped[dict[str, object]] = mapped_column(JSON, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    threshold_version: Mapped[str] = mapped_column(String(100), nullable=False)
    consent_version: Mapped[str] = mapped_column(String(80), nullable=False)
    consented_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    trust_notice_version: Mapped[str] = mapped_column(String(80), nullable=False)
    trust_notice_accepted_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    rescore_locked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


class VerificationSignal(Base):
    """Inputs and outcomes for each verification signal (FR-19, NFR-15)."""

    __tablename__ = "verification_signals"
    __table_args__ = (
        UniqueConstraint("verification_id", "signal_name", name="uq_verification_signals_case_name"),
        Index("ix_verification_signals_verification_id", "verification_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    verification_id: Mapped[int] = mapped_column(
        ForeignKey("profile_verifications.id", ondelete="CASCADE"), nullable=False
    )
    signal_name: Mapped[str] = mapped_column(String(80), nullable=False)
    input_snapshot: Mapped[dict[str, object]] = mapped_column(JSON, nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    outcome: Mapped[str] = mapped_column(String(80), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)


class VerificationAppeal(Base):
    """One evidence-bearing appeal per rejected verification (FR-21, NFR-11)."""

    __tablename__ = "verification_appeals"
    __table_args__ = (
        UniqueConstraint("verification_id", name="uq_verification_appeals_verification"),
        CheckConstraint("status IN ('pending', 'approved', 'rejected')", name="ck_verification_appeals_status"),
        Index("ix_verification_appeals_status_created", "status", "created_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    verification_id: Mapped[int] = mapped_column(
        ForeignKey("profile_verifications.id", ondelete="CASCADE"), nullable=False
    )
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    added_evidence: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    decision_reason: Mapped[str | None] = mapped_column(Text)
    reviewed_by: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)


class ProfileReport(Base):
    """A user report routes a profile to review and locks its score (FR-16)."""

    __tablename__ = "profile_reports"
    __table_args__ = (
        UniqueConstraint("reporter_user_id", "target_user_id", name="uq_profile_reports_reporter_target"),
        Index("ix_profile_reports_target_created", "target_user_id", "created_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    reporter_user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    target_user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    reason: Mapped[str] = mapped_column(String(1000), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)


class VerificationDecision(Base):
    """Append-only score and reviewer decision trail (FR-19, FR-26, NFR-11)."""

    __tablename__ = "verification_decisions"
    __table_args__ = (Index("ix_verification_decisions_profile_created", "verification_id", "created_at"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    verification_id: Mapped[int] = mapped_column(
        ForeignKey("profile_verifications.id", ondelete="CASCADE"), nullable=False
    )
    reviewer_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    decision: Mapped[str] = mapped_column(String(30), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    band: Mapped[str] = mapped_column(String(20), nullable=False)
    signals: Mapped[dict[str, object]] = mapped_column(JSON, nullable=False)
    threshold_version: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)


class LLMGatewayCallLog(Base):
    """Metadata-only record for one model attempt or structured-cache hit (NFR-2, NFR-19)."""

    __tablename__ = "llm_gateway_call_logs"
    __table_args__ = (
        CheckConstraint(
            "outcome IN ('success', 'failure', 'cache_hit')",
            name="ck_llm_gateway_call_logs_outcome",
        ),
        CheckConstraint("attempt_number >= 0", name="ck_llm_gateway_call_logs_attempt"),
        CheckConstraint("queue_position >= 0", name="ck_llm_gateway_call_logs_queue_position"),
        Index("ix_llm_gateway_call_logs_created_at", "created_at"),
        Index("ix_llm_gateway_call_logs_request_id", "request_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    request_id: Mapped[str] = mapped_column(String(36), nullable=False)
    operation: Mapped[str] = mapped_column(String(100), nullable=False)
    model_name: Mapped[str] = mapped_column(String(120), nullable=False)
    prompt_version: Mapped[str | None] = mapped_column(String(120))
    attempt_number: Mapped[int] = mapped_column(Integer, nullable=False)
    queue_position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    passage_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    approximate_prompt_chars: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    cache_hit: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    outcome: Mapped[str] = mapped_column(String(16), nullable=False)
    failure_category: Mapped[str | None] = mapped_column(String(80))
    elapsed_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
