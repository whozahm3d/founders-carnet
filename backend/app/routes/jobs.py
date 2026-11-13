"""Startup job listings and talent applications (FR-6, FR-24, FR-25, NFR-5)."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_roles
from app.job_schemas import (
    FounderJobApplicationRead,
    JobApplicationCreate,
    JobApplicationStatusUpdate,
    JobListingCreate,
    JobListingPatch,
    JobListingRead,
    TalentJobApplicationRead,
)
from app.models import (
    FounderProfile,
    JobApplication,
    JobListing,
    JobSave,
    Startup,
    User,
)

router = APIRouter(prefix="/api/v1", tags=["jobs"])
FounderDep = Annotated[User, Depends(require_roles("founder"))]
TalentDep = Annotated[User, Depends(require_roles("talent"))]
SessionDep = Annotated[Session, Depends(get_db)]


def _owned_verified_startup(session: Session, startup_id: int, user_id: int) -> Startup:
    startup = session.scalar(
        select(Startup)
        .join(FounderProfile, Startup.founder_profile_id == FounderProfile.id)
        .where(
            Startup.id == startup_id,
            FounderProfile.user_id == user_id,
            Startup.is_verified.is_(True),
        )
    )
    if startup is None:
        raise HTTPException(status_code=404, detail="Verified startup not found")
    return startup


def _owned_listing(session: Session, job_id: int, user_id: int) -> JobListing:
    listing = session.scalar(
        select(JobListing)
        .join(Startup, JobListing.startup_id == Startup.id)
        .join(FounderProfile, Startup.founder_profile_id == FounderProfile.id)
        .where(
            JobListing.id == job_id,
            FounderProfile.user_id == user_id,
            Startup.is_verified.is_(True),
        )
    )
    if listing is None:
        raise HTTPException(status_code=404, detail="Job listing not found")
    return listing


def _listing_read(session: Session, listing: JobListing) -> JobListingRead:
    startup_name = session.scalar(
        select(Startup.name).where(Startup.id == listing.startup_id)
    )
    return JobListingRead(
        id=listing.id,
        startup_id=listing.startup_id,
        startup_name=startup_name,
        title=listing.title,
        description=listing.description,
        employment_type=listing.employment_type,
        location=listing.location,
        is_remote=listing.is_remote,
        status=listing.status,
        created_at=listing.created_at,
        updated_at=listing.updated_at,
    )


@router.post(
    "/startups/{startup_id}/jobs",
    response_model=JobListingRead,
    status_code=status.HTTP_201_CREATED,
)
def create_listing(
    startup_id: int,
    payload: JobListingCreate,
    current_user: FounderDep,
    session: SessionDep,
) -> JobListingRead:
    startup = _owned_verified_startup(session, startup_id, current_user.id)
    listing = JobListing(startup_id=startup.id, **payload.model_dump())
    session.add(listing)
    session.commit()
    session.refresh(listing)
    return _listing_read(session, listing)


@router.get("/startups/{startup_id}/jobs", response_model=list[JobListingRead])
def list_founder_listings(
    startup_id: int,
    current_user: FounderDep,
    session: SessionDep,
) -> list[JobListingRead]:
    _owned_verified_startup(session, startup_id, current_user.id)
    listings = session.scalars(
        select(JobListing)
        .where(JobListing.startup_id == startup_id)
        .order_by(JobListing.created_at.desc(), JobListing.id.desc())
    ).all()
    return [_listing_read(session, listing) for listing in listings]


@router.get("/jobs", response_model=list[JobListingRead])
def browse_listings(
    current_user: TalentDep,
    session: SessionDep,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> list[JobListingRead]:
    listings = session.scalars(
        select(JobListing)
        .join(Startup, JobListing.startup_id == Startup.id)
        .where(JobListing.status == "open", Startup.is_verified.is_(True))
        .order_by(JobListing.created_at.desc(), JobListing.id.desc())
        .limit(limit)
        .offset(offset)
    ).all()
    return [_listing_read(session, listing) for listing in listings]


@router.patch("/jobs/{job_id}", response_model=JobListingRead)
def update_listing(
    job_id: int,
    payload: JobListingPatch,
    current_user: FounderDep,
    session: SessionDep,
) -> JobListingRead:
    listing = _owned_listing(session, job_id, current_user.id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(listing, field, value)
    session.commit()
    session.refresh(listing)
    return _listing_read(session, listing)


@router.delete("/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_listing(
    job_id: int, current_user: FounderDep, session: SessionDep
) -> Response:
    listing = _owned_listing(session, job_id, current_user.id)
    session.delete(listing)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/jobs/{job_id}/save", status_code=status.HTTP_200_OK)
def save_listing(
    job_id: int, current_user: TalentDep, session: SessionDep
) -> dict[str, int | bool]:
    listing = session.scalar(
        select(JobListing)
        .join(Startup, Startup.id == JobListing.startup_id)
        .where(
            JobListing.id == job_id,
            Startup.is_verified.is_(True),
        )
    )
    if listing is None or listing.status != "open":
        raise HTTPException(status_code=404, detail="Open job listing not found")
    existing = session.scalar(
        select(JobSave).where(
            JobSave.job_id == job_id, JobSave.user_id == current_user.id
        )
    )
    if existing is None:
        session.add(JobSave(job_id=job_id, user_id=current_user.id))
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            existing = session.scalar(
                select(JobSave).where(
                    JobSave.job_id == job_id, JobSave.user_id == current_user.id
                )
            )
            if existing is None:
                raise
    return {"job_id": job_id, "saved": True}


@router.delete("/jobs/{job_id}/save", status_code=status.HTTP_204_NO_CONTENT)
def unsave_listing(
    job_id: int, current_user: TalentDep, session: SessionDep
) -> Response:
    saved = session.scalar(
        select(JobSave).where(
            JobSave.job_id == job_id, JobSave.user_id == current_user.id
        )
    )
    if saved is not None:
        session.delete(saved)
        session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/jobs/saved", response_model=list[JobListingRead])
def saved_listings(
    current_user: TalentDep, session: SessionDep
) -> list[JobListingRead]:
    listings = session.scalars(
        select(JobListing)
        .join(JobSave, JobSave.job_id == JobListing.id)
        .join(Startup, Startup.id == JobListing.startup_id)
        .where(JobSave.user_id == current_user.id, Startup.is_verified.is_(True))
        .order_by(JobSave.created_at.desc(), JobSave.id.desc())
    ).all()
    return [_listing_read(session, listing) for listing in listings]


@router.post(
    "/jobs/{job_id}/applications",
    response_model=TalentJobApplicationRead,
    status_code=status.HTTP_201_CREATED,
)
def apply_to_listing(
    job_id: int,
    payload: JobApplicationCreate,
    current_user: TalentDep,
    session: SessionDep,
) -> TalentJobApplicationRead:
    listing = session.scalar(
        select(JobListing)
        .join(Startup, Startup.id == JobListing.startup_id)
        .where(
            JobListing.id == job_id,
            JobListing.status == "open",
            Startup.is_verified.is_(True),
        )
    )
    if listing is None:
        raise HTTPException(
            status_code=409, detail="Job listing is closed or unavailable"
        )
    application = JobApplication(
        job_id=job_id,
        candidate_user_id=current_user.id,
        cover_letter=payload.cover_letter,
    )
    session.add(application)
    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        duplicate = session.scalar(
            select(JobApplication.id).where(
                JobApplication.job_id == job_id,
                JobApplication.candidate_user_id == current_user.id,
            )
        )
        if duplicate is not None:
            raise HTTPException(
                status_code=409, detail="Already applied to this listing"
            ) from exc
        raise
    session.refresh(application)
    startup_name = session.scalar(
        select(Startup.name).where(Startup.id == listing.startup_id)
    )
    return TalentJobApplicationRead(
        id=application.id,
        job_id=job_id,
        job_title=listing.title,
        startup_id=listing.startup_id,
        startup_name=startup_name,
        status=application.status,
        cover_letter=application.cover_letter,
        created_at=application.created_at,
        updated_at=application.updated_at,
    )


@router.get("/jobs/applications/me", response_model=list[TalentJobApplicationRead])
def my_applications(
    current_user: TalentDep, session: SessionDep
) -> list[TalentJobApplicationRead]:
    rows = session.execute(
        select(JobApplication, JobListing, Startup)
        .join(JobListing, JobApplication.job_id == JobListing.id)
        .join(Startup, JobListing.startup_id == Startup.id)
        .where(JobApplication.candidate_user_id == current_user.id)
        .order_by(JobApplication.created_at.desc(), JobApplication.id.desc())
    ).all()
    return [
        TalentJobApplicationRead(
            id=application.id,
            job_id=listing.id,
            job_title=listing.title,
            startup_id=startup.id,
            startup_name=startup.name,
            status=application.status,
            cover_letter=application.cover_letter,
            created_at=application.created_at,
            updated_at=application.updated_at,
        )
        for application, listing, startup in rows
    ]


@router.get(
    "/startups/{startup_id}/job-applications",
    response_model=list[FounderJobApplicationRead],
)
def founder_applications(
    startup_id: int,
    current_user: FounderDep,
    session: SessionDep,
) -> list[FounderJobApplicationRead]:
    _owned_verified_startup(session, startup_id, current_user.id)
    rows = session.execute(
        select(JobApplication, User)
        .join(JobListing, JobApplication.job_id == JobListing.id)
        .join(User, User.id == JobApplication.candidate_user_id)
        .where(JobListing.startup_id == startup_id)
        .order_by(JobApplication.created_at.desc(), JobApplication.id.desc())
    ).all()
    return [
        FounderJobApplicationRead(
            id=application.id,
            job_id=application.job_id,
            candidate_user_id=candidate.id,
            candidate_full_name=candidate.full_name,
            candidate_email=candidate.email,
            status=application.status,
            cover_letter=application.cover_letter,
            created_at=application.created_at,
            updated_at=application.updated_at,
        )
        for application, candidate in rows
    ]


@router.patch(
    "/job-applications/{application_id}", response_model=FounderJobApplicationRead
)
def update_application_status(
    application_id: int,
    payload: JobApplicationStatusUpdate,
    current_user: FounderDep,
    session: SessionDep,
) -> FounderJobApplicationRead:
    row = session.execute(
        select(JobApplication, User, Startup)
        .join(User, User.id == JobApplication.candidate_user_id)
        .join(JobListing, JobListing.id == JobApplication.job_id)
        .join(Startup, Startup.id == JobListing.startup_id)
        .join(FounderProfile, FounderProfile.id == Startup.founder_profile_id)
        .where(
            JobApplication.id == application_id,
            FounderProfile.user_id == current_user.id,
            Startup.is_verified.is_(True),
        )
    ).first()
    if row is None:
        raise HTTPException(status_code=404, detail="Job application not found")
    application, candidate, _startup = row
    application.status = payload.status
    session.commit()
    session.refresh(application)
    return FounderJobApplicationRead(
        id=application.id,
        job_id=application.job_id,
        candidate_user_id=candidate.id,
        candidate_full_name=candidate.full_name,
        candidate_email=candidate.email,
        status=application.status,
        cover_letter=application.cover_letter,
        created_at=application.created_at,
        updated_at=application.updated_at,
    )
