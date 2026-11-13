"""Deterministic scoring for collected profile verification signals (FR-14, FR-19)."""

from dataclasses import dataclass

from app.config import Settings
from app.feature_models import EcosystemProfile
from app.services.secp_check import SecpCheckResult
from app.verification_schemas import PortfolioVerdict, VerificationScoringResult


@dataclass(frozen=True)
class SignalValue:
    score: float
    outcome: str
    input_snapshot: dict[str, object]
    reason: str


def score_profile_verification(
    profile: EcosystemProfile,
    *,
    role: str,
    linkedin_connected: bool,
    secp_result: SecpCheckResult,
    github_url: str | None,
    portfolio_result: PortfolioVerdict,
    portfolio_reason: str,
    settings: Settings,
) -> VerificationScoringResult:
    required_values = (
        profile.sector,
        profile.stages,
        profile.availability,
        profile.location,
        profile.summary,
        profile.skills,
        profile.ticket_min is not None and profile.ticket_max is not None,
    )
    completeness = round(
        sum(bool(value) for value in required_values) / len(required_values), 4
    )
    github_score = 1.0 if role != "talent" or github_url else 0.0
    portfolio_score = {"consistent": 1.0, "insufficient": 0.5, "inconsistent": 0.0}[
        portfolio_result
    ]
    signal_values = {
        "linkedin_oauth": SignalValue(
            score=1.0 if linkedin_connected else 0.0,
            outcome="connected" if linkedin_connected else "not_connected",
            input_snapshot={
                "provider": "linkedin",
                "identity_present": linkedin_connected,
            },
            reason="A LinkedIn OAuth identity is linked."
            if linkedin_connected
            else "No LinkedIn OAuth identity is linked.",
        ),
        "secp_cross_check": SignalValue(
            score=secp_result.score,
            outcome=secp_result.outcome,
            input_snapshot={
                "entity_name": "submitted",
                "registration_number": "submitted",
            },
            reason=secp_result.reason,
        ),
        "profile_completeness": SignalValue(
            score=completeness,
            outcome="complete" if completeness == 1.0 else "incomplete",
            input_snapshot={
                "required_fields_present": round(completeness * len(required_values))
            },
            reason="All required matching profile fields are present."
            if completeness == 1.0
            else "One or more required matching profile fields are incomplete.",
        ),
        "github_for_talent": SignalValue(
            score=github_score,
            outcome="not_applicable"
            if role != "talent"
            else "provided"
            if github_url
            else "not_provided",
            input_snapshot={"github_url_present": bool(github_url), "role": role},
            reason=(
                "GitHub is not a required signal for this role."
                if role != "talent"
                else "A GitHub link is present."
                if github_url
                else "No GitHub link was provided."
            ),
        ),
        "portfolio_link": SignalValue(
            score=portfolio_score,
            outcome=portfolio_result,
            input_snapshot={"portfolio_result": portfolio_result},
            reason=portfolio_reason,
        ),
    }
    score = round(
        settings.verification_linkedin_weight * signal_values["linkedin_oauth"].score
        + settings.verification_secp_weight * signal_values["secp_cross_check"].score
        + settings.verification_completeness_weight
        * signal_values["profile_completeness"].score
        + settings.verification_github_weight * signal_values["github_for_talent"].score
        + settings.verification_portfolio_weight
        * signal_values["portfolio_link"].score,
        4,
    )
    band = (
        "high"
        if score >= settings.verification_high_threshold
        else "low"
        if score <= settings.verification_low_threshold
        else "review"
    )

    # The SECP cross-check is a manual reviewer step; profile completeness or a link alone
    # must not establish a legal entity's identity.
    status = (
        "auto_rejected"
        if band == "low"
        else "auto_verified"
        if band == "high" and secp_result.outcome == "verified"
        else "pending_review"
    )
    if band == "low":
        reason = (
            "The collected signals are below the verification threshold. "
            + "; ".join(value.reason for value in signal_values.values())
        )
    elif band == "high":
        reason = "The signals score highly. " + (
            "The SECP check is recorded as verified."
            if status == "auto_verified"
            else "A manual SECP cross-check is still required."
        )
    else:
        reason = "The collected signals need human review. " + "; ".join(
            value.reason for value in signal_values.values()
        )

    threshold_version = (
        f"{settings.verification_rule_version}:weights=linkedin:{settings.verification_linkedin_weight:.2f},"
        f"secp:{settings.verification_secp_weight:.2f},completeness:{settings.verification_completeness_weight:.2f},"
        f"github:{settings.verification_github_weight:.2f},portfolio:{settings.verification_portfolio_weight:.2f}:"
        f"high={settings.verification_high_threshold:.3f}:"
        f"low={settings.verification_low_threshold:.3f}"
    )
    return VerificationScoringResult(
        score=score,
        band=band,
        status=status,
        signals={name: value.outcome for name, value in signal_values.items()},
        reason=reason,
        threshold_version=threshold_version,
    )
