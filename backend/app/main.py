from __future__ import annotations

import secrets
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import update
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_roles
from app.models import ConsentRecord, OAuthIdentity, User
from app.routes.admin_verification import router as admin_verification_router
from app.routes.compliance import router as compliance_router
from app.routes.founders import router as founders_router
from app.routes.intelligence import router as intelligence_router
from app.routes.jobs import router as jobs_router
from app.routes.market_research import router as market_research_router
from app.routes.resumes import router as resumes_router
from app.routes.verification import router as verification_router
from app.schemas import (
    ConsentStatusRead,
    DeletionRequestRead,
    LinkedInSignInRequest,
    TokenResponse,
    UserLoginRequest,
    UserRead,
    UserRegisterRequest,
    UserRole,
)
from app.security import create_access_token, hash_password, verify_password
from app.services.feature_ai import clear_feature_clients
from app.services.llm_cache import clear_structured_response_cache
from app.services.oauth import linkedin_provider
from app.services.wiring import close_compliance_answer_service


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        yield
    finally:
        close_compliance_answer_service()
        clear_feature_clients()


app = FastAPI(title="Founders Carnet API", lifespan=lifespan)
app.include_router(compliance_router)
app.include_router(admin_verification_router)
app.include_router(founders_router)
app.include_router(intelligence_router)
app.include_router(jobs_router)
app.include_router(market_research_router)
app.include_router(resumes_router)
app.include_router(verification_router)


@app.exception_handler(RequestValidationError)
async def sanitized_validation_error(
    _: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Never echo request values such as passwords in validation responses (NFR-4)."""
    errors = [
        {
            "loc": error.get("loc"),
            "msg": error.get("msg"),
            "type": error.get("type"),
        }
        for error in exc.errors()
    ]
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": errors})


REGISTRATION_CONSENT_TYPE = "non_essential_processing"
REGISTRATION_CONSENT_VERSION = "registration-v1"
PUBLIC_ROLES = ("founder", "talent", "mentor", "investor")


def _require_consent(accepted: bool) -> None:
    if not accepted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Consent is required before registration",
        )


def _record_consent(db: Session, user_id: int, source: str) -> ConsentRecord:
    record = ConsentRecord(
        user_id=user_id,
        consent_type=REGISTRATION_CONSENT_TYPE,
        consent_version=REGISTRATION_CONSENT_VERSION,
        source=source,
    )
    db.add(record)
    return record


@app.post("/api/v1/auth/register/{role}", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(role: UserRole, payload: UserRegisterRequest, db: Session = Depends(get_db)) -> User:
    """Register a public role with explicit consent; admin is never public.

    FR-17, FR-22, FR-23, NFR-4, NFR-5, NFR-8, NFR-9.
    """
    _require_consent(payload.consent_accepted)
    normalized_email = payload.email.lower()
    existing = db.query(User).filter(User.email == normalized_email).first()
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    user = User(
        email=normalized_email,
        full_name=payload.full_name.strip(),
        hashed_password=hash_password(payload.password),
        role=role,
        is_active=True,
    )
    db.add(user)
    db.flush()
    _record_consent(db, user.id, "password_registration")
    db.commit()
    db.refresh(user)
    return user


@app.post("/api/v1/auth/linkedin/{role}", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def linkedin_sign_in(
    role: UserRole,
    payload: LinkedInSignInRequest,
    response: Response,
    db: Session = Depends(get_db),
) -> User:
    """Sign in through the provider boundary using the local fake provider (FR-17, FR-22)."""
    _require_consent(payload.consent_accepted)
    try:
        identity_data = linkedin_provider.authenticate(payload.authorization_code)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="LinkedIn authentication failed") from exc

    identity = (
        db.query(OAuthIdentity)
        .filter(
            OAuthIdentity.provider == "linkedin",
            OAuthIdentity.provider_subject == identity_data.provider_subject,
        )
        .first()
    )
    if identity is not None:
        if not identity.user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Account is disabled")
        response.status_code = status.HTTP_200_OK
        return identity.user

    existing = db.query(User).filter(User.email == identity_data.email.lower()).first()
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    user = User(
        email=identity_data.email.lower(),
        full_name=identity_data.full_name,
        hashed_password=hash_password(secrets.token_urlsafe(32)),
        role=role,
        is_active=True,
    )
    db.add(user)
    db.flush()
    db.add(
        OAuthIdentity(
            user_id=user.id,
            provider="linkedin",
            provider_subject=identity_data.provider_subject,
        )
    )
    _record_consent(db, user.id, "linkedin_registration")
    db.commit()
    db.refresh(user)
    return user


@app.post("/api/v1/auth/login", response_model=TokenResponse)
def login_user(payload: UserLoginRequest, db: Annotated[Session, Depends(get_db)]) -> TokenResponse:
    """Sign in and issue a JWT for role-scoped access.

    FR-23, NFR-4, NFR-5.
    """
    normalized_email = payload.email.lower()
    user = db.query(User).filter(User.email == normalized_email).first()
    if user is None or not user.is_active or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(
        subject=str(user.id),
        role=user.role,
        token_version=user.token_version,
    )
    return TokenResponse(access_token=token)


@app.post("/api/v1/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout_user(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> Response:
    """Invalidate every token issued before this logout (FR-23, NFR-5)."""
    db.execute(
        update(User)
        .where(User.id == current_user.id)
        .values(token_version=User.token_version + 1)
    )
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/api/v1/users/me/consent/withdraw", response_model=ConsentStatusRead)
def withdraw_consent(
    current_user: User = Depends(require_roles(*PUBLIC_ROLES)),
    db: Session = Depends(get_db),
) -> ConsentStatusRead:
    """Withdraw non-essential processing consent and preserve the audit record (FR-27, NFR-9)."""
    record = (
        db.query(ConsentRecord)
        .filter(
            ConsentRecord.user_id == current_user.id,
            ConsentRecord.consent_type == REGISTRATION_CONSENT_TYPE,
        )
        .one()
    )
    if record.withdrawn_at is None:
        record.withdrawn_at = datetime.utcnow()
        db.commit()
        db.refresh(record)
    return ConsentStatusRead(
        consent_type=record.consent_type,
        consent_version=record.consent_version,
        withdrawn=record.withdrawn_at is not None,
        withdrawn_at=record.withdrawn_at,
    )


@app.post("/api/v1/users/me/deletion-request", response_model=DeletionRequestRead, status_code=status.HTTP_202_ACCEPTED)
def request_account_deletion(
    current_user: User = Depends(require_roles(*PUBLIC_ROLES)),
    db: Session = Depends(get_db),
) -> DeletionRequestRead:
    """Disable the account now and schedule the 30-day purge for step 9 (FR-27, NFR-11)."""
    requested_at = datetime.utcnow()
    scheduled_for = requested_at + timedelta(days=30)
    clear_structured_response_cache(current_user.id)
    current_user.deletion_requested_at = requested_at
    current_user.deletion_scheduled_for = scheduled_for
    current_user.is_active = False
    current_user.token_version += 1
    db.commit()
    return DeletionRequestRead(
        requested_at=requested_at,
        deletion_scheduled_for=scheduled_for,
        account_disabled=True,
    )


@app.get("/api/v1/users/me", response_model=UserRead)
def read_current_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    """Return the current authenticated user's profile.

    NFR-5: protected endpoints require a valid token and caller role.
    """
    return current_user


@app.get("/api/v1/admin/stats")
def admin_stats(current_user: Annotated[User, Depends(require_roles("admin"))]) -> dict[str, str]:
    """Admin-only endpoint for the first access-control slice.

    FR-23, NFR-5.
    """
    return {"status": "ok", "role": current_user.role}


@app.get("/")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
