"""Models for matching, readiness, and pitch practice (FR-2, FR-3, FR-7, FR-10, FR-28, FR-29)."""

from datetime import datetime

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
