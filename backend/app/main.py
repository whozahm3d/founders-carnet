from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import update
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_roles
from app.models import User
from app.routes.compliance import router as compliance_router
from app.routes.founders import router as founders_router
from app.routes.intelligence import router as intelligence_router
from app.schemas import TokenResponse, UserLoginRequest, UserRead, UserRegisterRequest
from app.services.wiring import close_compliance_answer_service
from app.services.feature_ai import clear_feature_clients
from app.security import create_access_token, hash_password, verify_password


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        yield
    finally:
        close_compliance_answer_service()
        clear_feature_clients()


app = FastAPI(title="Founders Carnet API", lifespan=lifespan)
app.include_router(compliance_router)
app.include_router(founders_router)
app.include_router(intelligence_router)


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


@app.post("/api/v1/auth/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserRegisterRequest, db: Session = Depends(get_db)) -> User:
    """Register a user with explicit role assignment for the foundations slice.

    FR-22, FR-23, NFR-4, NFR-5, NFR-8.
    """
    normalized_email = payload.email.lower()
    existing = db.query(User).filter(User.email == normalized_email).first()
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    role = payload.role.lower()
    allowed_roles = {"founder", "talent", "mentor", "investor"}
    if role not in allowed_roles:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported role")

    user = User(
        email=normalized_email,
        full_name=payload.full_name.strip(),
        hashed_password=hash_password(payload.password),
        role=role,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/api/v1/auth/login", response_model=TokenResponse)
def login_user(payload: UserLoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
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
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response:
    """Invalidate every token issued before this logout (FR-23, NFR-5)."""
    db.execute(
        update(User)
        .where(User.id == current_user.id)
        .values(token_version=User.token_version + 1)
    )
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/api/v1/users/me", response_model=UserRead)
def read_current_user(current_user: User = Depends(get_current_user)) -> User:
    """Return the current authenticated user's profile.

    NFR-5: protected endpoints require a valid token and caller role.
    """
    return current_user


@app.get("/api/v1/admin/stats")
def admin_stats(current_user: User = Depends(require_roles("admin"))) -> dict[str, str]:
    """Admin-only endpoint for the first access-control slice.

    FR-23, NFR-5.
    """
    return {"status": "ok", "role": current_user.role}


@app.get("/")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
