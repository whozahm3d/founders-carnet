"""Admin review queue and final verification decisions (FR-16, FR-21, FR-26)."""

from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_roles
from app.feature_models import (
    ProfileReport,
    ProfileVerification,
    VerificationAppeal,
    VerificationDecision,
    VerificationSignal,
)
from app.models import User
from app.verification_schemas import (
    AdminAppealRead,
    AdminVerificationDecisionWrite,
    AdminVerificationQueueItem,
    AdminVerificationSignalRead,
    ProfileVerificationRead,
)


router = APIRouter(prefix="/api/v1/admin/verification", tags=["admin verification"])
SessionDep = Annotated[Session, Depends(get_db)]
AdminUser = Annotated[User, Depends(require_roles("admin"))]


@router.get("/review-queue", response_model=list[AdminVerificationQueueItem])
def read_review_queue(_: AdminUser, session: SessionDep) -> list[AdminVerificationQueueItem]:
    rows = session.execute(
        select(ProfileVerification, User.role)
        .join(User, User.id == ProfileVerification.user_id)
        .where(ProfileVerification.status.in_(("pending_review", "appeal_pending")))
        .order_by(ProfileVerification.created_at.asc(), ProfileVerification.id.asc())
    ).all()
    items = []
    for verification, user_role in rows:
        appeal = session.scalar(
            select(VerificationAppeal).where(VerificationAppeal.verification_id == verification.id)
        )
        signal_rows = session.scalars(
            select(VerificationSignal)
            .where(VerificationSignal.verification_id == verification.id)
            .order_by(VerificationSignal.id.asc())
        ).all()
        report_count = session.scalar(
            select(func.count(ProfileReport.id)).where(ProfileReport.target_user_id == verification.user_id)
        ) or 0
        items.append(
            AdminVerificationQueueItem(
                verification_id=verification.id,
                user_id=verification.user_id,
                user_role=user_role,
                status=verification.status,
                score=verification.score,
                band=verification.band,
                signals=verification.signals,
                signal_details=[
                    AdminVerificationSignalRead.model_validate(signal) for signal in signal_rows
                ],
                reason=verification.reason,
                threshold_version=verification.threshold_version,
                appeal=AdminAppealRead.model_validate(appeal) if appeal else None,
                report_count=report_count,
                created_at=verification.created_at,
            )
        )
    return items


@router.post("/{verification_id}/decision", response_model=ProfileVerificationRead)
def decide_verification(
    verification_id: int,
    payload: AdminVerificationDecisionWrite,
    reviewer: AdminUser,
    session: SessionDep,
) -> ProfileVerificationRead:
    verification = session.get(ProfileVerification, verification_id)
    if verification is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Verification case not found")
    if verification.status not in {"pending_review", "appeal_pending"}:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This verification case has a final decision")

    final_status = "verified" if payload.decision == "approve" else "rejected"
    appeal = session.scalar(
        select(VerificationAppeal).where(VerificationAppeal.verification_id == verification.id)
    )
    if appeal is not None and appeal.status == "pending":
        appeal.status = "approved" if payload.decision == "approve" else "rejected"
        appeal.decision_reason = payload.reason
        appeal.reviewed_by = reviewer.id
        appeal.reviewed_at = datetime.now(timezone.utc).replace(tzinfo=None)

    verification.status = final_status
    verification.reason = payload.reason
    session.add(
        VerificationDecision(
            verification_id=verification.id,
            reviewer_user_id=reviewer.id,
            decision=final_status,
            reason=payload.reason,
            score=verification.score,
            band=verification.band,
            signals=verification.signals,
            threshold_version=verification.threshold_version,
        )
    )
    session.commit()
    session.refresh(verification)

    appeal_exists = session.scalar(
        select(VerificationAppeal.id).where(VerificationAppeal.verification_id == verification.id)
    ) is not None
    return ProfileVerificationRead(
        id=verification.id,
        user_id=verification.user_id,
        portfolio_url=verification.portfolio_url,
        secp_entity_name=verification.secp_entity_name,
        secp_registration_number=verification.secp_registration_number,
        status=verification.status,
        score=verification.score,
        band=verification.band,
        signals=verification.signals,
        reason=verification.reason,
        threshold_version=verification.threshold_version,
        appeal_used=appeal_exists,
        rescore_locked=verification.rescore_locked,
        created_at=verification.created_at,
        updated_at=verification.updated_at,
    )
