# Scope and no-go list

Source: report Chapter 2 (Goals, Scope, Constraints) and Chapter 4 (Risks).

## What it is

An AI platform for the Pakistani startup ecosystem. It connects founders, startup job seekers (talent), mentors, and investors, plus an admin role. All five roles share one AI reasoning engine. It only makes introductions.

## Goals

1. One AI engine for five roles, with role-based access and mutual acceptance before contact details show.
2. A compliance assistant that answers only from official SECP, FBR, and PSEB documents, cites every answer, and declines when evidence is not enough.
3. Two-stage matching: pgvector retrieval, then a supervised re-ranker. Compared with a cosine-only baseline using NDCG@K and MRR.
4. Readiness scoring, pitch simulation, and market research synthesis as prompted modules, each with its own evaluation.
5. A curated board of startup jobs and internships, plus a resume and LinkedIn optimizer.
6. Hybrid profile verification: automated score for clear cases, human reviewer for unclear ones, every decision logged, one appeal.
7. A benchmark of retrieval and generation in English, Urdu, and Roman Urdu (FYP-2).
8. A small legal footprint.

## No-go list

Stop and flag it if a feature drifts toward any of these.

- No equity in any startup.
- No investment brokerage. The platform does not broker, hold, or mediate investment money. No payment flow between investor and startup. No fee tied to an investment outcome.
- No legal or tax advice. The compliance assistant informs. It never says whether a license or registration applies to someone's case.
- No scraping of individual personal profiles. Users register themselves.
- No open community forum, no team or project-management tools, no paid cohort training with human staff.
- We do not host events. The calendar only lists events run by others.
- The readiness score is not a probability. The platform does not predict funding.
- Gender or location weighting in matching was considered and rejected. Fairness needs its own metrics and ethical review first. Age and gender are never matching features.
- A State Bank foreign exchange and offshore structures corpus was rejected as too risky.
- No data without consent. Personal data comes only from self-registration, consented pilot data, manual authoring, or synthetic data. Never from scraping social media, messaging apps, or public profiles (PECA 2016, R-10).

## Open legal item

No lawyer or SECP has reviewed the fee model (R-15). We claim no regulatory compliance. Legal review is required before any launch. Billing is mocked in FYP-2.

## Constraints

- Three people, two semesters, no designer, tester, or ops person. Ali leads AI and ML, Shahzeb the frontend, Taha the backend. Each feature must be small enough to build and explain.
- No paid infrastructure. Vercel (frontend), Railway or Render (backend and workers), free Gemini tier.
- Gemini 2.5 or lower. Higher models were unreliable under free-tier load.
- No public dataset pairs Pakistani founders with mentors or investors. No incubator partnership yet (R-16).
- FYP-1 is English only. Urdu and Roman Urdu come in FYP-2.
- RAG and multilingual NLP are new to the team. Start with a baseline, try advanced work only when the baseline is stable.

## FYP-1 and FYP-2 split

FYP-1: SRS and design documents, interactive prototypes, code for main flows, a compliance assistant prototype with citations and abstention, a hybrid matching prototype (cosine baseline plus feature weights).

FYP-2: re-ranker training and testing, the Urdu and Roman Urdu benchmark, a larger compliance corpus, placement fee billing (mocked), events calendar, resource links, user manual.
