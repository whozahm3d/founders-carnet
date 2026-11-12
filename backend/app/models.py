from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    JSON,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from pgvector.sqlalchemy import VECTOR


VECTOR_TYPE = VECTOR().with_variant(JSON(), "sqlite")


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), default="founder", nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    token_version: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    deletion_requested_at: Mapped[datetime | None] = mapped_column(DateTime)
    deletion_scheduled_for: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)

    consent_records: Mapped[list[ConsentRecord]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    oauth_identities: Mapped[list[OAuthIdentity]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    compliance_queries: Mapped[list[ComplianceQuery]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    founder_profile: Mapped[FounderProfile | None] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )


class ConsentRecord(Base):
    """Auditable consent state for personal-data processing (FR-17, FR-27, NFR-9)."""

    __tablename__ = "consent_records"
    __table_args__ = (
        UniqueConstraint("user_id", "consent_type", name="uq_consent_records_user_type"),
        Index("ix_consent_records_user_type", "user_id", "consent_type"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    consent_type: Mapped[str] = mapped_column(String(80), nullable=False)
    consent_version: Mapped[str] = mapped_column(String(80), nullable=False)
    accepted_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    withdrawn_at: Mapped[datetime | None] = mapped_column(DateTime)
    source: Mapped[str] = mapped_column(String(30), nullable=False)

    user: Mapped[User] = relationship(back_populates="consent_records")


class OAuthIdentity(Base):
    """External identity mapping without storing provider access tokens (FR-22, NFR-4)."""

    __tablename__ = "oauth_identities"
    __table_args__ = (
        UniqueConstraint("provider", "provider_subject", name="uq_oauth_provider_subject"),
        UniqueConstraint("user_id", "provider", name="uq_oauth_user_provider"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    provider: Mapped[str] = mapped_column(String(40), nullable=False)
    provider_subject: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)

    user: Mapped[User] = relationship(back_populates="oauth_identities")


class FounderProfile(Base):
    """Founder-owned profile data submitted after explicit profile consent (FR-1, FR-17)."""

    __tablename__ = "founder_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    bio: Mapped[str | None] = mapped_column(Text)
    location: Mapped[str | None] = mapped_column(String(255))
    consent_version: Mapped[str] = mapped_column(String(50), nullable=False)
    consented_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user: Mapped[User] = relationship(back_populates="founder_profile")
    startups: Mapped[list[Startup]] = relationship(
        back_populates="founder_profile",
        cascade="all, delete-orphan",
    )


class Startup(Base):
    """A founder's business and traction record used by readiness and matching (FR-1)."""

    __tablename__ = "startups"
    __table_args__ = (
        CheckConstraint(
            "stage IN ('idea', 'mvp', 'growth', 'scaling')",
            name="ck_startups_stage",
        ),
        CheckConstraint("customer_count >= 0", name="ck_startups_customer_count"),
        CheckConstraint(
            "monthly_revenue IS NULL OR monthly_revenue >= 0",
            name="ck_startups_monthly_revenue",
        ),
        CheckConstraint(
            "funding_need_min IS NULL OR funding_need_min >= 0",
            name="ck_startups_funding_need_min",
        ),
        CheckConstraint(
            "funding_need_max IS NULL OR funding_need_max >= funding_need_min",
            name="ck_startups_funding_need_range",
        ),
        Index("ix_startups_founder_profile_id", "founder_profile_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    founder_profile_id: Mapped[int] = mapped_column(
        ForeignKey("founder_profiles.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    sector: Mapped[str] = mapped_column(String(100), nullable=False)
    stage: Mapped[str] = mapped_column(String(30), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    business_model: Mapped[str] = mapped_column(String(255), nullable=False)
    traction_summary: Mapped[str] = mapped_column(Text, nullable=False)
    customer_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    monthly_revenue: Mapped[float | None] = mapped_column(Numeric(14, 2))
    skills: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    funding_need_min: Mapped[float | None] = mapped_column(Numeric(14, 2))
    funding_need_max: Mapped[float | None] = mapped_column(Numeric(14, 2))
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    founder_profile: Mapped[FounderProfile] = relationship(back_populates="startups")


class ComplianceDocument(Base):
    __tablename__ = "compliance_documents"
    __table_args__ = (Index("ix_compliance_documents_active", "is_active"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    file_name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    issuing_body: Mapped[str] = mapped_column(String(100), nullable=False)
    document_type: Mapped[str] = mapped_column(String(50), nullable=False)
    source_url: Mapped[str] = mapped_column(Text, nullable=False)
    effective_date: Mapped[str | None] = mapped_column(String(32))
    consolidation_date: Mapped[str | None] = mapped_column(String(32))
    retrieved_at: Mapped[str | None] = mapped_column(String(32))
    content_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    scope_note: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    chunks: Mapped[list[ComplianceChunk]] = relationship(
        back_populates="document",
        cascade="all, delete-orphan",
    )


class ComplianceChunk(Base):
    __tablename__ = "compliance_chunks"
    __table_args__ = (
        UniqueConstraint("chunk_id", name="uq_compliance_chunks_chunk_id"),
        Index("ix_compliance_chunks_document_id", "document_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(
        ForeignKey("compliance_documents.id", ondelete="CASCADE"),
        nullable=False,
    )
    chunk_id: Mapped[str] = mapped_column(String(512), nullable=False)
    page_number: Mapped[int] = mapped_column(Integer, nullable=False)
    section: Mapped[str | None] = mapped_column(String(100))
    text: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list[float] | None] = mapped_column(VECTOR_TYPE)
    embedding_model: Mapped[str | None] = mapped_column(String(255))

    document: Mapped[ComplianceDocument] = relationship(back_populates="chunks")
    citations: Mapped[list[ComplianceCitation]] = relationship(back_populates="chunk")


class ComplianceQuery(Base):
    __tablename__ = "compliance_queries"
    __table_args__ = (
        CheckConstraint(
            "outcome IN ('answered', 'abstained', 'failed')",
            name="ck_compliance_queries_outcome",
        ),
        Index("ix_compliance_queries_user_id", "user_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer_text: Mapped[str | None] = mapped_column(Text)
    outcome: Mapped[str] = mapped_column(String(20), nullable=False)
    abstention_reason: Mapped[str | None] = mapped_column(String(100))
    passage_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    latency_ms: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    prompt_version: Mapped[str | None] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)

    user: Mapped[User] = relationship(back_populates="compliance_queries")
    citations: Mapped[list[ComplianceCitation]] = relationship(
        back_populates="query",
        cascade="all, delete-orphan",
    )


class ComplianceCitation(Base):
    __tablename__ = "compliance_citations"
    __table_args__ = (
        UniqueConstraint("query_id", "chunk_id", name="uq_compliance_citations_query_chunk"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    query_id: Mapped[int] = mapped_column(
        ForeignKey("compliance_queries.id", ondelete="CASCADE"),
        nullable=False,
    )
    chunk_id: Mapped[int] = mapped_column(
        ForeignKey("compliance_chunks.id", ondelete="CASCADE"),
        nullable=False,
    )
    rank: Mapped[int] = mapped_column(Integer, nullable=False)

    query: Mapped[ComplianceQuery] = relationship(back_populates="citations")
    chunk: Mapped[ComplianceChunk] = relationship(back_populates="citations")


# Import after Base and the existing models are defined so all tables register
# with the same metadata used by Alembic and SQLite tests.
from app.feature_models import (  # noqa: E402,F401
    EcosystemProfile,
    JobApplication,
    JobListing,
    JobSave,
    MarketResearchReport,
    MatchRecord,
    PitchSession,
    PitchTurn,
    ProfileReport,
    ProfileVerification,
    ReadinessAssessment,
    ResumeOptimization,
    VerificationAppeal,
    VerificationDecision,
    LLMGatewayCallLog,
    TalentProfile,
    VerificationSignal,
)
