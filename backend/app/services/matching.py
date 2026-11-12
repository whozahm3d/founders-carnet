"""Deterministic FYP-1 matching factors; deliberately contains no LLM calls."""

from collections.abc import Sequence

from app.models import EcosystemProfile, Startup
from app.services.compliance_retrieval import cosine_similarity

# Proposal because the report names factors but does not give numeric weights.
MATCH_WEIGHTS = {
    "sector_fit": 0.25,
    "stage_fit": 0.20,
    "skill_overlap": 0.25,
    "availability_fit": 0.15,
    "ticket_fit": 0.15,
}
SEMANTIC_SIMILARITY_WEIGHT = 0.5


def startup_match_text(startup: Startup) -> str:
    return " ".join((startup.name, startup.description, startup.sector, startup.stage, startup.business_model,
                     startup.traction_summary, startup.location, " ".join(startup.skills or [])))


def profile_match_text(profile: EcosystemProfile) -> str:
    return " ".join((profile.sector, " ".join(profile.stages or []), " ".join(profile.skills or []),
                     profile.availability, profile.location, profile.summary))


def score_profile(startup: Startup, profile: EcosystemProfile) -> dict[str, float]:
    sector = float(startup.sector.strip().casefold() == profile.sector.strip().casefold())
    stage = float(startup.stage.casefold() in {value.casefold() for value in profile.stages})
    startup_skills = {value.strip().casefold() for value in startup.skills or [] if value.strip()}
    profile_skills = {value.strip().casefold() for value in profile.skills or [] if value.strip()}
    skill = len(startup_skills & profile_skills) / len(startup_skills | profile_skills) if (startup_skills | profile_skills) else 0.0
    availability = {"open": 1.0, "limited": 0.5, "closed": 0.0}[profile.availability]

    if profile.ticket_min is None and profile.ticket_max is None:
        ticket = 1.0
    elif startup.funding_need_min is None and startup.funding_need_max is None:
        ticket = 0.0
    else:
        startup_min = float(startup.funding_need_min or 0)
        startup_max = float(startup.funding_need_max or startup_min)
        profile_min = float(profile.ticket_min or 0)
        profile_max = float(profile.ticket_max if profile.ticket_max is not None else profile_min)
        ticket = float(max(startup_min, profile_min) <= min(startup_max, profile_max))

    return {
        "sector_fit": sector,
        "stage_fit": stage,
        "skill_overlap": round(skill, 6),
        "availability_fit": availability,
        "ticket_fit": ticket,
    }


def weighted_match_score(factors: dict[str, float]) -> float:
    return round(sum(factors[key] * weight for key, weight in MATCH_WEIGHTS.items()), 6)


def combined_match_score(similarity: float, factors: dict[str, float]) -> tuple[float, float]:
    """Blend cosine similarity with the hand-weighted compatibility factors."""
    normalized_similarity = max(0.0, min(1.0, float(similarity)))
    factor_score = weighted_match_score(factors)
    combined = (
        normalized_similarity * SEMANTIC_SIMILARITY_WEIGHT
        + factor_score * (1.0 - SEMANTIC_SIMILARITY_WEIGHT)
    )
    return normalized_similarity, round(combined, 6)


def rank_profiles(
    query_embedding: Sequence[float],
    candidates: Sequence[tuple[EcosystemProfile, Sequence[float]]],
) -> list[tuple[EcosystemProfile, float]]:
    ranked = [(profile, cosine_similarity(query_embedding, embedding)) for profile, embedding in candidates]
    ranked.sort(key=lambda item: (-item[1], item[0].user_id))
    return ranked
