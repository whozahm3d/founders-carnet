# Build order

Source: report Chapter 2 (Delivery Priority and Fallback Plan), Chapter 6 (Plan for FYP-2), and Chapter 5 (Development Methods).

## Foundations first

Authentication, role-based access, and user profiles. Every feature depends on them.

## Then, in this order

1. Compliance assistant with citations and abstention, and its evaluation.
2. Matching engine: baseline prototype in FYP-1, trained re-ranker in FYP-2 (labels depend on a partner).
3. Readiness score, then pitch simulator, then market research synthesis.
4. Resume optimizer and the job and internship board.
5. English, Urdu, and Roman Urdu benchmark (already planned for FYP-2).
6. Supporting classifiers on the FINAL datasets (resume role, startup outcome, follow-on funding). Offline work; not on the critical path. Dropped before anything above it.

If work falls behind, items lower in the list are dropped first.

## Scope decision for FYP-1 (2026-10-16)

All 12 FYP-1 features from the Chapter 4 table are attempted. Anything not finished by Nov 8 is reported in the Chapter 6 limitations and moves to FYP-2. The list above still decides what is dropped first. The per-feature plan, minimum slices and cut lines are in `coding-plan.md`.

## The FYP-1 checkpoint

The checkpoint is the end of FYP-1. If the compliance assistant cannot give cited answers and abstain correctly on a held-out question set by then, no lower item is extended in FYP-2 until it can.

If there are too few labeled pairs for the re-ranker, the matching result reported is the cosine baseline plus a hand-weighted feature score, stated as a pilot result.

## Sprint order

Foundations, the compliance assistant, matching, then the remaining prompted modules. Details are in the sprint plan.

## FYP-2 plan

| Phase | Work | Exit criterion |
| --- | --- | --- |
| 1 | Close the FYP-1 checkpoint: finish gold set, expand corpus, evaluate citations, recall, abstention | Correct citations and abstention on the held-out set |
| 2 | Matching: collect 150 to 300 labeled pairs, train re-ranker, compare with cosine baseline | NDCG@K and MRR against the baseline, or a stated pilot result |
| 3 | Prompted modules: readiness, pitch simulator, market research, resume optimizer, job board | Readiness score vs. 2 or 3 human reviewers on 10 to 15 ideas (Spearman) |
| 4 | Benchmark English, Urdu, Roman Urdu on 30 to 50 parallel descriptions per language, then add FR-9 | Results per language; fine-tuning only if a gap is found |
| 4b | Train and evaluate the three supporting classifiers (`docs/datasets.md`): clean and deduplicate first, then macro-F1 against a simple baseline | Results reported per classifier, or a stated pilot result |
| 5 | Mocked placement fee billing, events calendar, resource links, user manual | FR-11, FR-30, FR-31 demonstrated |
| 6 | Load test, usability walkthrough, in-university survey, founder and talent interviews | NFR-1, NFR-2, NFR-3, NFR-16 checked |

## Working rules

- No training on a dataset until its preprocessing items in `docs/datasets.md` are done (for example the Haider deduplication and the Success/Fail date filter).
- Start with the simplest thing we can evaluate and measure against a stated baseline.
- Requirements and design come before code, but parts are still built and revised inside a sprint.
- Code reaches `main` only through pull requests that run linting and tests (NFR-23).
- Testing plan: unit tests on scoring and ranking; integration tests on role-scoped access (no token, wrong role, before and after acceptance) and on no contact details before mutual acceptance; the compliance assistant on a hand-verified gold question set (citation correctness, retrieval recall, correct abstention).
