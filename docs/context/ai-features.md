# Trained model or prompted LLM call

Source: report Chapter 5 (System Overview, Goals and Guidelines), Risk Analysis (R-8), Chapter 6.

Keep these separate in code, comments, and docs. Do not call a prompted feature "trained" or "fine-tuned".

## The one trained model

| Feature | Detail |
| --- | --- |
| Matching re-ranker (FYP-2) | Logistic regression or a gradient-boosted ranker on structured features. Trained on 150 to 300 labeled pairs. Compared with the cosine baseline using NDCG@K and MRR. Goes live only if it shows no regression. |

FYP-1 does not train it. FYP-1 ranks by cosine similarity plus feature weights across five factors: sector fit, stage fit, skill overlap, availability fit, and ticket fit.

If there are too few labeled pairs, the reported result is the cosine baseline plus a hand-weighted feature score, stated as a pilot result (R-1).

Matching never calls a language model. It uses embeddings (sentence-transformers), pgvector similarity search, and the re-ranker.

A cross-encoder or neural listwise re-ranker was rejected: too expensive, and likely to overfit on 150 to 300 pairs.

## Prompted LLM calls (Gemini, through the LLM Gateway only)

| Feature | Notes |
| --- | --- |
| Readiness assessment (FR-2) | Seven dimensions, each score stores its reasoning and the rubric version |
| Pitch simulator (FR-3) | Multi-turn investor conversation, scored against a fixed rubric |
| Market research synthesis (FR-4) | Live web sources; evidence kept apart from interpretation |
| Resume and profile suggestions (FR-5) | Line-level before and after |
| Compliance answers (FR-8) | Generated only from retrieved passages, with citations and abstention |
| Portfolio link check (FR-20) | Returns consistent, inconsistent, or insufficient |

## Authored rules, not models

Four of the five verification signals are rules the team wrote: LinkedIn OAuth, SECP cross-check, profile completeness, GitHub activity. Only the portfolio link check is a prompted call. Thresholds are configuration values.

## Pattern every AI feature follows

1. Normalize the input into a schema.
2. Reason (prompted template or ranking step).
3. Ground and return a structured result with evidence. Never return raw LLM text. When evidence is missing, say so.

## Explanations are stored, not regenerated

Readiness scores store their reasoning. Match results store their factors. "Why was I matched" is a database read (NFR-15).

## Things we decided not to do

- No fine-tuning on the regulatory corpus. It changes (a fee schedule was replaced during the project), and a fine-tuned model cannot cite a passage.
- No answering from model memory without retrieval. Commercial legal research tools hallucinated 17 to 33% of the time.
- Embedding fine-tuning waits until a benchmark finds a gap and there is enough labeled data. BM25 with reciprocal rank fusion only if it improves retrieval on the gold question set.
- No accuracy claim for any model. None has been trained or evaluated yet.
