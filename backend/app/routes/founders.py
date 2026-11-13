"""Founder profile and startup endpoints (FR-1, FR-17, NFR-5, NFR-9)."""

from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_roles
from app.models import FounderProfile, Startup, User
from app.schemas import (
    FounderProfileRead,
    FounderProfileWrite,
    StartupCreate,
    StartupRead,
    StartupUpdate,
)

router = APIRouter(prefix="/api/v1/founders/me", tags=["founders"])
FounderDep = Annotated[User, Depends(require_roles("founder"))]
SessionDep = Annotated[Session, Depends(get_db)]
PROFILE_CONSENT_VERSION = "founder-profile-v1"
_REQUIRED_STARTUP_FIELDS = {
    "name",
    "description",
    "sector",
    "stage",
    "location",
    "business_model",
    "traction_summary",
    "customer_count",
    "skills",
}


@router.put("/profile", response_model=FounderProfileRead)
def save_founder_profile(
    payload: FounderProfileWrite,
    current_user: FounderDep,
    session: SessionDep,
) -> FounderProfile:
    """Create or update the caller's founder profile after explicit consent."""
    if not payload.consent_accepted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile data requires explicit processing consent",
        )

    profile = session.scalar(
        select(FounderProfile).where(FounderProfile.user_id == current_user.id)
    )
    if profile is None:
        profile = FounderProfile(
            user_id=current_user.id,
            bio=payload.bio,
            location=payload.location,
            consent_version=PROFILE_CONSENT_VERSION,
            consented_at=datetime.now(UTC).replace(tzinfo=None),
        )
        session.add(profile)
    else:
        profile.bio = payload.bio
        profile.location = payload.location
        profile.consent_version = PROFILE_CONSENT_VERSION
        profile.consented_at = datetime.now(UTC).replace(tzinfo=None)

    session.commit()
    session.refresh(profile)
    return profile


@router.get("/profile", response_model=FounderProfileRead)
def read_founder_profile(
    current_user: FounderDep,
    session: SessionDep,
) -> FounderProfile:
    profile = session.scalar(
        select(FounderProfile).where(FounderProfile.user_id == current_user.id)
    )
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Founder profile not found"
        )
    return profile


@router.post(
    "/startups",
    response_model=StartupRead,
    status_code=status.HTTP_201_CREATED,
)
def create_startup(
    payload: StartupCreate,
    current_user: FounderDep,
    session: SessionDep,
) -> Startup:
    profile = session.scalar(
        select(FounderProfile).where(FounderProfile.user_id == current_user.id)
    )
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Create a consented founder profile before adding startup data",
        )
    if (
        payload.funding_need_min is not None
        and payload.funding_need_max is not None
        and payload.funding_need_min > payload.funding_need_max
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="funding_need_max must be at least funding_need_min",
        )

    startup_values = payload.model_dump()
    startup_values["skills"] = _normalize_skills(payload.skills)
    startup = Startup(founder_profile_id=profile.id, **startup_values)
    session.add(startup)
    session.commit()
    session.refresh(startup)
    return startup


@router.get("/startups", response_model=list[StartupRead])
def list_startups(
    current_user: FounderDep,
    session: SessionDep,
) -> list[Startup]:
    profile = session.scalar(
        select(FounderProfile).where(FounderProfile.user_id == current_user.id)
    )
    if profile is None:
        return []
    return list(
        session.scalars(
            select(Startup)
            .where(Startup.founder_profile_id == profile.id)
            .order_by(Startup.id)
        ).all()
    )


@router.patch("/startups/{startup_id}", response_model=StartupRead)
def update_startup(
    startup_id: int,
    payload: StartupUpdate,
    current_user: FounderDep,
    session: SessionDep,
) -> Startup:
    profile = session.scalar(
        select(FounderProfile).where(FounderProfile.user_id == current_user.id)
    )
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Startup not found"
        )
    startup = session.scalar(
        select(Startup).where(
            Startup.id == startup_id,
            Startup.founder_profile_id == profile.id,
        )
    )
    if startup is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Startup not found"
        )

    changes = payload.model_dump(exclude_unset=True)
    if any(
        field in _REQUIRED_STARTUP_FIELDS and value is None
        for field, value in changes.items()
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Required startup fields cannot be cleared",
        )
    minimum = changes.get("funding_need_min", startup.funding_need_min)
    maximum = changes.get("funding_need_max", startup.funding_need_max)
    if minimum is not None and maximum is not None and minimum > maximum:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="funding_need_max must be at least funding_need_min",
        )
    if "skills" in changes and changes["skills"] is not None:
        changes["skills"] = _normalize_skills(changes["skills"])
    for field, value in changes.items():
        setattr(startup, field, value)

    session.commit()
    session.refresh(startup)
    return startup


def _normalize_skills(skills: list[str]) -> list[str]:
    return list(dict.fromkeys(skill.strip() for skill in skills if skill.strip()))
