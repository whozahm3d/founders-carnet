# The Founder's Carnet: AI, RAG and Model Training Playbook

Nov 9, 2026 · @Ali

Updated 11 November 2026 after reading the repository. Section 20 lists what already exists and what changes in earlier sections. Where Section 20 and an earlier section disagree, Section 20 wins. Section 18 was rewritten against the repository.

## 1. Purpose and how to use this playbook

This playbook decides, for every AI feature in main.tex, which model or method we use, why, how we test it, and how we build it in the 2 to 4 weeks before D3.

It answers the first two D2 comments directly: no model has been trained, and the re-ranker has no dataset. Every section follows the same order, so you can find the same kind of answer anywhere.

1. **Decision:** what we use.
2. **Why:** the alternatives we rejected and the reason.
3. **Method:** how it works, step by step.
4. **Evaluation:** how we measure it, against what baseline.
5. **Build steps:** what to do first, with tools.
6. **Impact:** what it changes for the user and the report.

How to read the labels:

- **Fixed** means main.tex already commits to it. Changing it means editing earlier chapters.
- **Proposed** means my recommendation. Confirm it or replace it.
- Any number marked as a target is a proposal for a pass rule we set before testing. Nothing in this file is a result.

Two cautions about using this for the report. First, rewrite everything in your own words before it goes into the chapter, because the Turnitin AI report must stay at 20% or less. Second, the report describes algorithms and procedure, not code (template, Chapter 7).

## 2. Where we stand

main.tex describes a full AI design, but no model has been trained or evaluated, and the corpus is collected but not yet processed. The goal of the next 2 to 4 weeks is to turn the design into measured results.

### What main.tex already fixes

| Area | Fixed commitment in main.tex |
| --- | --- |
| Compliance assistant | Answers only from 11 official documents (SECP, FBR, PSEB and the Finance Act 2026). Cites source and effective date. Abstains when evidence is missing. |
| Matching | Two stages: pgvector retrieval with hard filters on sector, stage and geography, then a re-ranker. FYP-1 uses feature weights. The trained re-ranker is the only trained model in the platform. |
| Evaluation | Re-ranker: NDCG@K and MRR against a cosine-only baseline, with two members labeling independently and agreement reported. Assistant: hand-written gold question set, measuring citation correctness, retrieval recall and correct abstention, with RAGAS as support. |
| Readiness score | Prompted module, 7 dimensions, score 1 to 5 with reason and next action. Compared with human ratings by Spearman correlation on 10 to 15 ideas. Not a funding probability. |
| Classifiers | Resume role, startup outcome, follow-on funding. Offline studies, macro F1 against a simple baseline. Never shown to users as a probability. |
| Multilingual | English, Urdu and Roman Urdu benchmark with off-the-shelf models such as LaBSE and multilingual-e5. Planned for FYP-2. |
| Infrastructure | PostgreSQL with pgvector, sentence-transformers, scikit-learn, Celery and Redis, one LLM gateway, Gemini free tier. Training on Colab. |

### What the D2 feedback requires

1. **Train something and decide the model.** The panel wants to see which model, why, and the plan before final implementation. Each later section has a decision record for this.
2. **Re-ranker data.** If no real data exists, generate synthetic data and use it for training only. If real data never arrives, ship the synthetic-trained model. Section 5 makes this safe by keeping a hand-labeled evaluation set separate.
3. **Figma prototypes.** Already handled by the frontend plan, not part of this file.

### Constraints that shape every choice

- **Time:** 2 to 4 weeks to D3.
- **People:** two builders, who are also the only two labelers (Ali and Shahzeb).
- **Compute:** Colab free tier, Kaggle GPUs, and a local GPU machine. This is enough for embeddings, LightGBM and a DistilBERT fine-tune, and not enough to train large models.
- **Language model access:** Gemini free tier, with a possible move to OpenRouter free models. The report currently says Gemini 2.5 or lower and five concurrent requests (NFR-2). If the provider changes, the gateway makes it a configuration edit (NFR-19), but the report text and results must name the model actually used.
- **Data:** no public labeled matching data exists. PECA 2016 rules out scraping personal data. Allowed sources are self-registration, consented pilot data, manual writing and synthetic data (R-10).

## 3. Build order and timeline

Build the compliance assistant first, then the re-ranker, then the prompted modules, then the classifiers, because that is the order main.tex fixes (Constraints, Section 2.6) and because each later step gets cheaper once the gateway and embeddings exist.

The plan below assumes four weeks. If you only have two, stop after step 2 and describe steps 3 and 4 as designed and started, not measured.

### Week 1: foundations and RAG corpus

1. Fix the LLM gateway: one function that takes a prompt version and a model id, returns JSON, caches every response on disk, and logs model id, prompt version and latency.
2. Convert the 11 corpus documents to text, record the SHA-256 hash and dates of each, and chunk by legal section.
3. Embed the chunks, load them into pgvector, and build the first retrieval call.
4. Start the gold question set: write 40 questions this week, split between you.

### Week 2: RAG evaluation and synthetic data

1. Finish the gold set to about 80 questions and freeze a test split.
2. Run the retrieval comparison (dense, BM25, hybrid) on the dev split, then confirm on the test split.
3. Build the generation, validator and abstention steps and run the no-retrieval baseline.
4. In parallel, generate synthetic profiles and start hand-labeling the 100 evaluation pairs.

### Week 3: re-ranker and prompted modules

1. Judge synthetic pairs, build features, train the three candidate rankers, and evaluate on the hand-labeled pairs.
2. Write the rubric prompts for readiness and pitch, collect the 10 to 15 sample ideas, and get human scores.
3. Hook the working endpoints to the frontend, replacing mock JSON.

### Week 4: classifiers, write-up, buffer

1. Train the TF-IDF plus logistic regression baselines for the three classifiers. Try DistilBERT only if time remains.
2. Collect every result table into one results folder and write the implementation chapter.
3. Update the abstract, executive summary and conclusions so none of them still say no model has been trained.
4. Leave at least three days for the Turnitin reports, which depend on the library.

### Suggested split

| Work | Lead | Second |
| --- | --- | --- |
| Gateway, corpus processing, retrieval | Shahzeb | Ali |
| Gold set, validator, abstention | Ali | Shahzeb |
| Synthetic data and re-ranker | Shahzeb | Ali |
| Hand-labeling of evaluation pairs | Both, independently |  |
| Prompted modules and classifiers | Ali | Shahzeb |
| API contracts and frontend hookup | Taha (backend), Ali (frontend) |  |

Adjust this to your real availability. The one fixed rule is that both of you label the evaluation pairs independently, because that is what main.tex promises.

## 4. RAG compliance assistant

The assistant retrieves passages from the indexed official documents, writes an answer from those passages alone, checks the answer, and abstains if it cannot be supported. We measure it against an assistant that answers freely, because that comparison is Research Question 2 in main.tex.

### 4.1 Decisions

| Decision | Choice | Status |
| --- | --- | --- |
| Architecture | Retrieval-augmented generation with a validation step and abstention | Fixed |
| Chunking | By legal section, with the heading path attached to each chunk | Proposed |
| Embedding model | Pick by bake-off on the gold set. Candidates: multilingual-e5-base, bge-m3, and a small English model as a floor | Proposed |
| Vector store | pgvector in the existing PostgreSQL (NFR-20) | Fixed |
| Retrieval | Dense, BM25, and hybrid with reciprocal rank fusion. Keep hybrid only if it wins on the gold set | Fixed in principle, Proposed in detail |
| Generator | Gemini through the gateway (or the OpenRouter model that replaces it), temperature 0, JSON output | Fixed |
| Conflict handling | Show both sources with dates, never pick silently | Proposed |

### 4.2 Why these choices

- **RAG, not fine-tuning.** The corpus changes (fees rise 10% a year, a tax exemption ended on 30 June 2025), and a fine-tuned model cannot cite a passage. Retrieval lets us re-index when a document changes.
- **RAG, not a free-answering model.** Magesh et al. found commercial legal tools hallucinated 17 to 33% of the time. We expect a free model to do worse on Pakistani regulation, and the baseline run in 4.5 tests that.
- **Section-based chunks.** Fixed-size chunks split a legal clause across two pieces and drop the section number we need for the citation. Section chunks keep the citation intact.
- **Embedding bake-off, not a guess.** multilingual-e5 is named in main.tex for the multilingual benchmark. bge-m3 is a stronger multilingual candidate but larger. One model must serve both matching and retrieval (NFR-20), so we choose with data from our own gold set.
- **pgvector, not a separate vector database.** One store to keep consistent. At a few thousand chunks, exact search is fast enough, so an approximate index is optional.
- **Hybrid only if it earns its place.** Legal text has exact terms (section numbers, defined words) that BM25 matches well. The Cormack et al. fusion constant of 60 is the default.

### 4.3 Method

**Indexing**

1. Convert each document to clean text. Record title, issuer, effective date, consolidation date, retrieval date and SHA-256 hash, as the database design already stores.
2. Split by section. If a section is longer than about 500 tokens, split by subsection and repeat the section title at the start of each piece. Never split inside a numbered clause.
3. Attach metadata to every chunk: document id, section number, heading path, effective date.
4. Embed and store. If you use multilingual-e5, add the `query:` and `passage:` prefixes the model expects. Skipping them quietly lowers quality.
5. Index only what main.tex scopes in: Parts I and IV and sections 462 to 473 of the Companies Act, founder-relevant tax provisions, and the PSEB page for registration procedure only. The two documents whose text could not be extracted stay out.

**Answering**

1. Embed the question and retrieve the top 5 to 8 chunks (dense, or hybrid if it wins).
2. If the best score is below a threshold chosen on the dev split, abstain without calling the model.
3. Send only the retrieved chunks to the model. The prompt forbids outside knowledge and requires JSON with `answer`, `citations` (chunk ids), `abstain` and `abstain_reason`.
4. Run the checks in 4.4. If any check fails, abstain.
5. Return the answer with each cited chunk's document title, section and effective date, and the informational note.

**Conflicting sources.** Two cases already exist in main.tex: the PSEB page against the Ordinance on a tax exemption, and two FBR sources on company registration. Proposed rule: statute outranks circular, and circular outranks web page. If retrieved passages disagree, the answer states both with their dates and says they conflict. The PSEB conflict is limited by scope, since main.tex indexes that page for registration procedure only. Confirm this rule with your supervisor before you build it.

### 4.4 The checks that make abstention real

- **Citation check (rule):** every cited chunk id must be in the retrieved set.
- **Number check (rule):** every rupee amount, percentage, date and section number in the answer must appear in a cited chunk. This catches the most dangerous errors cheaply, with no model call.
- **Support check (model):** a second call splits the answer into claims and asks whether each is supported by its cited chunk. Treat this as a helper, not as ground truth, since main.tex already warns that a model judging a model repeats its mistakes.
- **Scope check:** questions asking whether a license or registration is required in a particular case get the procedure-only response from the abstain use case.

### 4.5 Evaluation

**Gold set.** About 80 questions written from the corpus by both of you: roughly 55 answerable, including date-sensitive and conflicting-source questions, and roughly 25 that should be refused. For the refused ones, use the six categories in Peng et al. (open the paper for the exact list). Each answerable question records the chunk or chunks that support it, which is what makes recall measurable.

Split into 30 dev questions for tuning and 50 test questions that nobody looks at until the final run. Without that wall, we tune on the exam and the numbers mean nothing.

**Systems compared on the test split**

| System | Purpose |
| --- | --- |
| Same model, no retrieval | Answers freely. This is the Research Question 2 baseline |
| Dense retrieval only | Retrieval baseline |
| BM25 only | Retrieval baseline |
| Hybrid (reciprocal rank fusion) | Kept only if it beats dense |
| Full pipeline (retrieval, generation, checks, abstention) | The system we describe |

**Metrics**

| Metric | What it tells us |
| --- | --- |
| Recall@5 and MRR | Whether retrieval finds the supporting section |
| Citation correctness | Whether the cited chunk really supports the claim (manual on all test answers, since n is small) |
| Unsupported-claim rate | Share of answers with a claim no source supports. Mark spans by the RAGTruth types |
| Abstention precision and recall | Refuses what it should, answers what it should |
| Date correctness | Right rate or fee for the right effective date |
| Latency | Checked against NFR-2 (about 8 seconds) |

With 50 test questions, one question moves a rate by 2 points. Report counts next to percentages and give a Wilson confidence interval. Do not claim a difference you cannot show.

**Pass rules to fix now (proposed targets, change them before you run, not after):** the full pipeline has a lower unsupported-claim rate than the no-retrieval baseline, and it abstains correctly on most of the refused questions. If it does not, report that plainly and name the failure causes.

### 4.6 Build steps

1. Write `ingest.py`: text extraction, section splitting, metadata, hashing. Use PyMuPDF or pdfplumber for the PDFs. Check the section splits by hand on the Companies Act first, since legal numbering breaks naive rules.
2. Write `embed.py`: batch embedding on Colab or Kaggle, saved to disk, then loaded into pgvector.
3. Write `retrieve.py` with dense, BM25 (`rank_bm25`) and fusion as three functions with one shared output format.
4. Write `answer.py`: prompt template (versioned), JSON parsing, the four checks, abstention.
5. Write `eval_rag.py`: reads the gold file, runs each system, writes one CSV of per-question results. The report tables come from this CSV, never from memory.
6. Expose one endpoint, `POST /compliance/ask`, returning the fields listed in Section 11.

### 4.7 Impact

For users, a founder gets a cited, dated answer or an honest refusal, never a confident guess. For the report, this is the only component with a complete evaluation story by D3: baseline, ablation, and a clear pass rule. For the panel, it answers the "why not ChatGPT" question with a measured comparison instead of an argument.

## 5. Matching re-ranker

We train a gradient-boosted ranker (LightGBM, LambdaMART objective) on synthetic profile pairs, and judge it only on pairs two of us labeled by hand. That separation is what stops the model from proving itself right.

Two decisions apply, and both stay in docs/DECISIONS.md. The 19 October entry says the re-ranker trains on the team's own labeled pairs. The new entry, following the evaluators' feedback, adds the synthetic route for when real labels are short or never arrive. Write the new entry before generating any synthetic data. See 20.2 and 20.4.

### 5.1 Decisions

| Decision | Choice | Status |
| --- | --- | --- |
| Stages | Stage 1: pgvector cosine retrieval with hard filters. Stage 2: re-ranker | Fixed |
| Re-ranker model | LightGBM with the lambdarank objective | Fixed in principle (GBDT in main.tex), Proposed in detail |
| Training data | Synthetic profiles and LLM-judged labels, with a rule override for filter violations | Proposed, follows D2 feedback |
| Decision log (both entries stay) | 19 Oct: the re-ranker trains on the team's own 150 to 300 labeled pairs. 11 Nov (new, from the evaluators' feedback): when real labels are short or never arrive, train on synthetic pairs, test only on hand-labeled pairs, and use real pairs as they come in. The new entry adds to the 19 Oct one and does not delete it | 19 Oct: in docs/DECISIONS.md. 11 Nov: to be written (draft in 20.4) |
| Evaluation data | About 100 pairs labeled by Ali and Shahzeb independently, never used in training | Proposed |
| Baselines | Cosine only, and the hand-weighted five-factor score from FYP-1 | Fixed |
| Metrics | NDCG@5, NDCG@10, MRR | Fixed |

### 5.2 Why these choices

- **Gradient boosting, not a neural re-ranker or cross-encoder.** The features are a handful of structured values, the data is a few thousand synthetic pairs, and we have no large interaction logs. Burges and Ke et al. show boosted trees optimize ranking metrics directly. Trees also train in seconds on a CPU and give feature importances, so each match can show its factors (NFR-15).
- **Lambdarank, not plain classification.** Matching is about order, not about a yes or no per pair. The lambdarank objective optimizes ordering within each startup's candidate list.
- **Synthetic data, with a human-labeled test.** Synthetic training data is the only route the D2 comment leaves us if no real data appears. Its weakness is circularity: if the labels come from the same logic as the features, the model relearns that logic. The hand-labeled test set breaks the circle, because humans, not the formula, define "good" there.
- **Judge model differs from generator model.** A model tends to rate its own writing highly. Use one model to write profiles and a different one to judge pairs.
- **A model bake-off, not a single bet.** We train three rankers and keep the simplest one that wins: logistic regression on the same features, LightGBM pointwise, and LightGBM lambdarank. If the linear model ties, it wins, because it is simpler to defend.

### 5.3 Method

**Step 1: generate synthetic profiles**

1. Sample the structured attributes first from your own distributions, not from the language model: sector, stage, city, skills, ticket range, availability. Use the Pakistan Startup Census schema and cities as a guide. This keeps the set varied. If you ask a model to invent everything, it repeats the same few profiles.
2. Then ask the model to write the free-text bio or thesis for each sampled attribute set.
3. Target size: about 200 startups, 60 mentors, 60 investors, 120 talent profiles. Adjust to what the API allows.
4. Make every profile obviously synthetic in storage. No real names, no real companies.

**Step 2: build candidate lists.** For each startup, run stage 1 to get the top 15 candidates after hard filters. Each startup and its 15 candidates form one ranking group.

**Step 3: label with a judge.** Give the judge model one startup and its candidates in a single call, and ask for a 0 to 3 relevance grade per candidate with a one-line reason, using a written rubric. Listwise calls keep the cost near 200 to 400 calls instead of thousands, which matters on the free tier. The judge sees raw profile text only, never our feature values. Pairs that break a hard filter get 0 by rule. Run each list twice and average, and drop lists where the two runs disagree badly.

**Step 4: compute features** for every pair:

- cosine similarity of the profile embeddings
- sector match (exact, related, none)
- stage compatibility (the investor's stated stages include the startup's stage)
- skill overlap (Jaccard)
- availability (mentor open or closed)
- ticket fit (startup ask against investor range)
- pair type (founder to mentor, founder to investor, talent to mentor, talent to founder), plus the GitHub signals for talent pairs from FR-13: repository count, commit recency and language mix

**Step 5: split by startup, never by pair.** All pairs from one startup stay in the same fold. Splitting by pair leaks information, because the same startup would appear in training and testing.

**Step 6: train and select.** Use grouped cross-validation on the training startups to compare the three rankers and tune a few settings (trees, depth, learning rate). Keep early stopping on a validation fold.

**Step 7: evaluate once** on the hand-labeled test pairs.

### 5.4 The hand-labeled evaluation set

1. Pick 25 startups and 8 to 10 candidates each, mixing high-cosine, low-cosine and random candidates so the set is not already biased toward our formula.
2. Ali and Shahzeb grade each pair 0 to 3 separately, with the same written rubric used by the judge, and without seeing any model's score.
3. Report agreement with a weighted Cohen's kappa. Then resolve disagreements by discussion and keep both the raw and the final labels.
4. Lock the file. It is never used for training or tuning.
5. Add a small slice of real data if you can: 10 to 20 consenting people (university mentors, classmates who agree to a startup role). This is the only part of the test that is not synthetic, so label it clearly.

### 5.5 Evaluation

| System | Role |
| --- | --- |
| Cosine only | Stage 1 baseline |
| Hand-weighted five factors | FYP-1 baseline |
| Logistic regression on features | Simple learned baseline |
| LightGBM pointwise | Learned, not rank-aware |
| LightGBM lambdarank | Proposed re-ranker |

Report NDCG@5, NDCG@10 and MRR with a paired bootstrap over startups for the confidence interval. Also run a feature ablation (remove one feature at a time) and report feature importance. If you cannot beat the hand-weighted score, say so.

**What the result can and cannot claim.** A win means the model ranks synthetic profiles the way humans graded them. It does not show how the model behaves on real Pakistani founders, mentors and investors. State this sentence in the report. That honesty is what makes the synthetic approach defensible.

**Decision rule (set now):** ship the learned model only if it beats the hand-weighted baseline on the hand-labeled test with an interval that does not cross zero. Otherwise ship the hand-weighted score and report the learned model as a pilot, which is the fallback main.tex already names under R-1.

### 5.6 Build steps

1. `gen_profiles.py`: attribute sampler plus the bio-writing prompt, with caching.
2. `build_groups.py`: stage 1 retrieval and the ranking groups.
3. `judge_pairs.py`: the listwise judge prompt and the two-run averaging.
4. `features.py`: the one place features are computed. Matching in production must call this same function, or training and serving will drift apart.
5. `train_ranker.py`: grouped CV, three models, saved model and metrics.
6. `eval_ranker.py`: hand-labeled test, bootstrap, ablation, tables.
7. Store `retrieval_score`, `rerank_score` and `match_factors` in the existing match result table.

### 5.7 Impact

For users, matches arrive with a plain list of reasons, and never with contact details until both accept. For the report, this answers D2 points 1 and 2 together: a named model, a justified choice, a data plan that survives having no real data, and an evaluation that does not grade itself.

## 6. Prompted modules

Readiness scoring, pitch simulation, market research and the resume optimizer are prompted language model calls, not trained models. main.tex says so in several places, and it is the honest framing (R-8). Each gets a fixed output schema, a versioned prompt, and its own small test, because there is no training data to measure them with.

### 6.1 Decisions that apply to all four

- **Fixed JSON schema per module,** validated on return. A malformed response is retried once, then shown as a failure with the previous result kept (use cases in Chapter 4).
- **Prompts and rubrics are versioned like code,** and each stored result records the prompt version and model id (NFR-15, database design).
- **Temperature 0 for scoring,** a little higher only for the pitch persona.
- **Every output is labeled** as written by a language model, and the pitch counterpart as a simulation.
- **No claim of accuracy beyond what the small tests below show.**

### 6.2 Readiness score

**Decision:** one rubric prompt returning, for each of the 7 dimensions (problem clarity, market definition, differentiation, business model coherence, traction, team, scalability), a 1 to 5 score, a reason that quotes the profile, a gap and a next action.

**Why a rubric:** Yin and Luo support judging against clear criteria, and G-Eval-style scoring is the method main.tex names. A rubric with written anchors for each score level (what a 1, 3 and 5 look like) is far more consistent than an open question.

**Tests, in order of importance**

1. **Repeatability.** Run each of 10 to 15 sample ideas three times. Report the spread of each dimension score. If scores swing by 2 points between identical runs, the module is not usable and the report must say so.
2. **Sensitivity.** Take a strong idea and remove the traction data, then remove the team section. The matching dimension score should fall. This tests that the score responds to content, and it needs no human labels.
3. **Agreement with humans.** Two reviewers score the same ideas on the same rubric. Report Spearman correlation per dimension and overall, with the interval. With 10 to 15 ideas the interval is wide, and the report should say so rather than quote one number. Use at least one reviewer who is not on the team, such as a mentor or the supervisor, because we wrote the rubric.
4. **Grounding.** Check that every reason quotes something actually present in the profile.

**Sample ideas:** write them by hand, covering weak to strong, across sectors. Do not use real founders' ideas without permission.

### 6.3 Pitch simulator

**Decision:** a multi-turn chat where the model plays one of three investor personas, asks follow-ups that reference the founder's last answer, and at the end scores four dimensions (clarity, market understanding, defensibility of numbers, handling of pushback) against a fixed rubric (FR-3).

**How it works:** a system prompt holds the persona, the startup profile, and the rubric. Each turn sends the transcript so far. The final call returns scores, the three weakest questions and the change from earlier sessions.

**Tests:** run 8 to 10 scripted sessions with deliberately strong, weak and evasive answers. Check three things: follow-ups refer to what was said, the persona stays in character, and weak answers score lower than strong ones. Have a second person rate question relevance on a 1 to 5 scale. Treat this as a usability check, not a validation.

### 6.4 Market research synthesis

**Decision:** live web search feeds a two-part output. The Evidence part holds findings with source, link and retrieval date. The Interpretation part is the model's reading, which may not introduce a number that is absent from Evidence (FR-4).

**Why this split:** a model asked for a market size will invent one. Forcing every figure to carry a source makes invention visible.

**Tests:** run 10 queries. For each figure in Evidence, fetch the source page and check by string search that the figure appears there. Report the share of figures supported. Separately check that Interpretation introduced no new numbers. If a figure cannot be sourced, the module shows "No sourced figure found".

### 6.5 Resume and profile optimizer

**Decision:** the model returns line-level suggestions next to the original text, never a rewritten document that replaces the original (FR-5).

**Main risk:** the model adds experience the candidate never had. Treat this as the key failure.

**Tests:** main.tex already says there is no suitable test set, so use tens of cases from the team's own resumes, with each owner's permission. Check automatically that suggested text introduces no new employers, degrees, tools or numbers (a diff against the original with a word list of entities), then have each owner rate usefulness from 1 to 5. Do not use the Resume Dataset files as evidence of quality for this module, because they are for the role classifier.

### 6.6 Impact

These four are what users see most, and they are the easiest to dismiss as "just prompts". The repeatability, sensitivity and sourcing tests are what turn them into defended modules. Be explicit in the report that they are prompted, and report the test results as small pilot checks.

## 7. Profile verification scoring

Verification is a rule-based score over five signals, with three bands and a human in the middle. It is not a trained detector, and main.tex says it only raises the cost of casual fakes.

### 7.1 Decisions

| Item | Choice |
| --- | --- |
| Signals | LinkedIn OAuth, SECP check, profile completeness, GitHub activity (talent), portfolio link consistency |
| Prompted part | Only the link consistency check. The other four are rules we write |
| Bands | High auto-verifies, low auto-rejects with a logged reason, middle goes to a reviewer |
| Thresholds | Configuration values with a version number, stored with every decision |
| Appeal | One per profile, decided by a person, final |

### 7.2 Why rules, not a model

We have no confirmed fake profiles to train on (main.tex says so). Gulati et al. found detectors drop from about 96% F1 on hand-made fakes to about 68% on language-model fakes, so even a trained detector would not give strong protection. Rules are explainable, and every rejection must show a reason (FR-14, FR-15).

### 7.3 Method

1. Each signal produces a value between 0 and 1, or "missing".
2. The score is a weighted sum over the signals that are present, with the weights in configuration. If LinkedIn is unavailable (R-6), the score uses the remaining signals and more profiles fall in the middle band.
3. The link check fetches the public page, extracts its text, and asks the model whether it matches the profile. The answer is consistent, inconsistent or insufficient (FR-20). The system never fetches LinkedIn addresses.
4. The score, the signal values, the band and the threshold version are logged (FR-19).

### 7.4 Evaluation

Be careful here. With no real fakes, anything we measure tests our own rules, not real-world detection.

- **Unit tests:** hand-written profiles with known signal values must land in the expected band.
- **Injected cases:** write about 30 synthetic profiles with deliberate defects (empty fields, mismatched link, no verifiable identity) and 30 complete ones. Report how many land in each band. This is a test that the rules work as written, and the report must call it that.
- **Band distribution:** on the synthetic re-ranker profiles, report what share go to human review. This tells us whether the middle band is manageable by two reviewers.
- **Link check:** 15 to 20 profiles with matching and non-matching links, reporting the confusion between the three outcomes.

Threshold values come from a dev set and then stay fixed for the test set.

### 7.5 Impact

This keeps the admin workload bounded and every decision explainable. For the report, the claim stays narrow: rule signals make casual fakes harder, and humans decide the unclear cases.

## 8. Supporting classifiers

Three small classifiers are offline studies on public data. They exist to show that we can train and evaluate supervised models, and they never produce a user-facing probability of success, failure or funding (main.tex, Section 3.3.3). Do them last, because they do not feed any feature.

Repository check: the supervisor approved these classifiers on 21 October as offline FYP-2 studies, and none has been trained. Treat this section as optional and lowest priority for the D3 window. See 20.2.

### 8.1 Decisions

| Classifier | Data | Label | Metric |
| --- | --- | --- | --- |
| Resume role | Resume Dataset (Maseeh), six technical categories | Role category | Macro F1 |
| Startup outcome | Startup Success/Fail (Crunchbase) | Closed or not closed | Macro F1 |
| Follow-on funding | StartUp Investments (Crunchbase) | Raised a follow-on round or not | Macro F1 |

Models: start with TF-IDF plus logistic regression for the text task and gradient boosting or logistic regression for the tabular ones. Try DistilBERT on the resume task only if time remains. A strong simple baseline is the point: if DistilBERT cannot beat TF-IDF, that is a valid finding.

### 8.2 Method and leakage controls

These datasets break easily. Most of the work is cleaning, not modeling.

- **Resume role:** remove duplicate texts before splitting, because 30.5% of the technical texts repeat. Split after deduplication, otherwise the same resume sits in train and test and the score is inflated.
- **Startup outcome:** drop every field recorded after the outcome. Clean the impossible dates. Prefer a split by founding date if dates are usable, so we do not test on the past using the future.
- **Follow-on funding:** the label is whether a later round exists, so any total-funding field that already includes later rounds leaks the answer. Keep only features known at or before the first round. About 24.7% of the funding total is missing, so decide on one missing-value rule and state it.
- **Baselines:** majority class and a one-feature rule, alongside the real models.
- **Splits:** fixed random seed, stratified, saved to disk. For small classes use cross-validation and report the mean and spread.

### 8.3 Evaluation

Report macro F1, the per-class table and a confusion matrix for each classifier, next to its baseline. Say clearly that Crunchbase data is global and the resume data is international, so results say nothing about Pakistani startups or resumes (main.tex, Chapter 6).

### 8.4 Impact

The impact is on the project's credibility more than on users: it shows a clean supervised pipeline with leakage handled. Do not let these results leak into the product as a prediction.

## 9. Multilingual benchmark

This is FYP-2 work in main.tex, so for D3 the goal is a small first run and a clear design, not a full result. The reason to run something now is that the embedding model you pick in Section 4 also decides how Urdu and Roman Urdu will behave later.

### 9.1 Decisions

- **Models compared:** LaBSE and multilingual-e5 (both named in main.tex), plus bge-m3 if it is in the Section 4 bake-off.
- **Data:** short parallel descriptions in English, Urdu script and Roman Urdu. Roman-Urdu-Parl gives general parallel text. For startup and regulatory wording, write 30 to 50 parallel descriptions yourselves.
- **Question asked:** do same-meaning pairs stay close across the three forms, and does retrieval of a regulatory passage still work when the question is in Urdu or Roman Urdu?

### 9.2 Method

1. Build the parallel set. For each of 30 to 50 descriptions, write the English, the Urdu and a Roman Urdu version. Roman Urdu has no standard spelling, so write two spelling variants for a subset to test sensitivity.
2. Embed all versions with each model.
3. Cross-lingual match: for each Urdu or Roman Urdu text, check whether its English counterpart is the nearest neighbor among all English texts. Report top-1 and top-5 accuracy.
4. Retrieval check: translate 15 to 20 gold questions into Urdu and Roman Urdu and measure recall@5 against the same chunks.

### 9.3 Evaluation and honesty

Report results per language and per model, with counts. main.tex already says we should not assume strong Roman Urdu results, so a weak Roman Urdu result is a finding, not a failure. Fine-tuning is optional, only if the benchmark shows a gap and enough labeled data exists. The Urdu answer generation itself stays out of FYP-1 (FR-9 is FYP-2).

### 9.4 Impact

It keeps the multilingual claim honest and tells you early whether the embedding choice will hold when Urdu is added.

## 10. Shared evaluation rules, gateway and reproducibility

Every result in the report must be reproducible from files you can show the panel. These rules apply to every section above.

### 10.1 Model and method register

This one table answers the D2 question "which model, why, and what is the plan" at a glance.

| Component | Method | Chosen over | Baseline | Metric | Data |
| --- | --- | --- | --- | --- | --- |
| Compliance retrieval | Hybrid or dense retrieval, chosen on the gold set | Fine-tuning, free answering | Dense only, BM25 only, no retrieval | Recall@5, MRR | 11 documents, gold set |
| Compliance answer | Grounded generation with checks and abstention | Free answering | Same model without retrieval | Unsupported-claim rate, abstention precision and recall | Gold test split |
| Re-ranker | LightGBM lambdarank | Cross-encoder, neural re-rankers | Cosine only, hand-weighted | NDCG@5, NDCG@10, MRR | Synthetic training, hand-labeled test |
| Readiness | Rubric prompt | Open-ended prompt | Repeat-run spread | Spearman, repeatability, sensitivity | 10 to 15 ideas |
| Pitch simulator | Persona prompt with rubric | None | Scripted answers | Relevance rating, ordering of strong against weak | 8 to 10 sessions |
| Market research | Evidence plus interpretation | Single free summary | None | Share of sourced figures supported | 10 queries |
| Resume optimizer | Line-level suggestions | Full rewrite | None | Fabrication check, usefulness rating | Team resumes |
| Verification | Weighted rule score | Trained detector | Hand-written profiles | Band results on injected cases | Synthetic profiles |
| Classifiers | TF-IDF with logistic regression, then DistilBERT if time | Large models | Majority class | Macro F1 | Maseeh, Crunchbase sets |
| Multilingual | Off-the-shelf multilingual encoders | Fine-tuning first | English-only model | Top-1 and top-5, recall@5 | 30 to 50 parallel descriptions |

### 10.2 Rules for fair testing

1. **Freeze the test set first.** Write and lock gold questions and hand-labeled pairs before you tune anything. Tune on dev only. Run the test split once per final system.
2. **Never split by row when rows share a source.** Split by startup, by resume text after deduplication, or by founding date.
3. **Record what is synthetic.** Every table that touches synthetic data says so in its caption.
4. **Report counts, intervals and failures,** not only the best number. A clear negative result is acceptable. A hidden one is not.
5. **Two labelers, independent, then agreement.** Report kappa before resolving disagreements.
6. **One results folder.** Every script writes a CSV there. Report tables are produced from the CSVs.

### 10.3 The language model gateway

main.tex says every model call goes through one gateway (NFR-19). Build that first, since every module depends on it.

- **Inputs:** prompt version, model id, messages, JSON schema, temperature.
- **Cache on disk,** keyed by the full input. A repeated call during evaluation returns the stored answer, which saves free-tier quota and makes reruns identical.
- **Log** model id, prompt version, tokens, latency and outcome (this supports NFR-15 and the stored-assessment design).
- **Queue** requests to respect the five-at-a-time limit (NFR-2), with the queued state visible to the user.
- **Retry** once on malformed JSON, then fail visibly.

**If you move to OpenRouter free models:** pin one exact model id per experiment, record it with every result, and check the current rate and daily limits before planning the synthetic judge runs. Free models can be changed or removed without notice, so run the final evaluation of each module in a short window on the same model, and cache the outputs. main.tex and the abstract currently name Gemini, so update them to whatever you actually used. Do not mix models inside one comparison table unless the model is the thing being compared.

### 10.4 Reproducibility checklist

- Fixed random seeds, saved split files, and the corpus SHA-256 hashes already in main.tex.
- Versioned prompts and rubrics in the repository.
- Package versions in the repository.
- A short README per component with the exact command that produces its results CSV.
- Colab and Kaggle notebooks exported to the repository, not left only in the browser.

## 11. Connecting the AI features to the frontend and API

Every AI feature returns typed JSON through a FastAPI endpoint behind the gateway, and every response has the same state fields, so one frontend pattern serves all of them. The names below are proposals for Taha and Ali to agree on, and they must match the screens.

### 11.1 Endpoints and response fields

These paths are the planned design. The paths that exist in the repository today are in 20.3.

| Feature | Endpoint | Key response fields |
| --- | --- | --- |
| Compliance assistant | `POST /compliance/ask` | `answer`, `citations` (chunk id, document title, section, effective date, link), `abstain`, `abstain_reason`, `corpus_version`, `latency_ms` |
| Matches | `POST /matches/query` | per candidate: `rank`, `retrieval_score`, `rerank_score`, `factors` (sector, stage, skills, availability, ticket fit), `contact_locked` |
| Readiness | `POST /readiness/assess` | `dimensions` (name, score 1 to 5, reason, gap, next action), `overall`, `rubric_version`, `created_at` |
| Pitch | `POST /pitch/sessions`, `.../turn`, `.../end` | persona, next question, then final scores, weakest questions, change from earlier sessions |
| Market research | `POST /research/run` | `evidence` (finding, source, link, retrieved on), `interpretation`, `competitors`, `sources_unreached` |
| Resume optimizer | `POST /resume/suggest` | per suggestion: original text, suggested text, reason |
| Verification | internal call on profile submit | score, band, signals, threshold version, reason |

Every AI response also carries `model_id` and `prompt_version`, which the frontend can ignore and the database must store.

### 11.2 The five states

| State | How the API signals it | What the screen shows |
| --- | --- | --- |
| Queued | `202` with a job id and queue position | "High demand, you are number N" with cancel |
| Loading | request in progress | Generating, about 8 seconds |
| Success | `200` with data | Structured output with the AI-generated label and time |
| Abstain | `200` with `abstain: true` and a reason | The no-grounded-answer or procedures-only message |
| Failure | `5xx` or model error | Failure message, retry, previous result kept |

Abstain is a successful response, not an error. That distinction matters for the logs and for the abstention metric.

### 11.3 Working in parallel

1. Write the response schemas first, as shared type definitions used by both sides.
2. The frontend builds against mock JSON that already contains abstain, queued and failure cases.
3. As each module passes its test, swap its mock for the real endpoint. Do not swap one that has not been evaluated.
4. Keep sample numbers on screens clearly marked as samples, and never show a metric on a screen that the models have not produced.

## 12. Risks and impact

The three most likely ways this plan fails are time, a weak result that you are tempted to hide, and the language model provider changing under you.

| Risk | Likelihood | What to do | Impact if it happens |
| --- | --- | --- | --- |
| Gold set written late or tuned on | High | Freeze the test split in week 2 and tune on dev only | Numbers are inflated and the panel can tell |
| Synthetic labels teach the model our own formula | High | Hand-labeled test, judge differs from generator, rule override only for hard filters | The re-ranker result proves nothing |
| Free-tier quota or model change mid-evaluation | High | Gateway cache, pinned model id, listwise judge calls, run finals in one window | Results cannot be reproduced or compared |
| Re-ranker does not beat hand-weighted score | Medium | Decision rule set now. Ship the hand-weighted score and report the pilot | A negative result, which is acceptable if reported plainly |
| Section splitting breaks legal clauses | Medium | Check splits by hand on the Companies Act before embedding everything | Wrong citations, false recall |
| Conflicting sources produce a wrong confident answer | Medium | Precedence rule, show both with dates, conflict questions in the gold set | A cited but wrong answer, the worst failure for this product |
| Synthetic profiles look too alike | Medium | Sample attributes in code, write only the text with the model | A model that fits a narrow set |
| Labelers disagree heavily | Medium | Shared written rubric, calibration on 10 pairs first, report kappa | Noisy test set and wide intervals |
| Small samples tempt over-claiming | High | Report counts and intervals, and use cautious wording | Panel questions every claim |
| Time runs out before step 4 | Medium | Cut classifiers and multilingual first, keep RAG and re-ranker | Report says designed, not measured, for the cut items |
| Report text still says no model was trained | Medium | Search main.tex for every such sentence in the final pass | Contradiction the supervisor already flagged |
| AI-written report text raises the Turnitin AI score | Medium | Write results sections yourselves from your CSVs, and check early | Submission may be rejected above 20% |

### What changes if it works

- The assistant gives users cited, dated answers or a clear refusal.
- Matches carry explanations and hide contacts until both accept.
- The report moves from "designed" to "measured" for the two components the panel cared about.

## 13. Questions a panel may ask

Short answers you can say aloud. Each is consistent with main.tex and with the evaluation plan above. Replace any answer that stops being true once you have real results.

**Why not just use ChatGPT or Gemini directly for compliance questions?** Because a free model has no source and no date, and Pakistani rules change. We measure the difference: the same model with no retrieval is our baseline, and we compare unsupported-claim rates.

**Why RAG and not fine-tuning?** The documents change every year, and a fine-tuned model cannot point to the passage that supports its answer. With retrieval we re-index, and every answer cites a section and an effective date.

**How do you know it does not hallucinate?** We do not claim zero. We measure the unsupported-claim rate on a held-out set, check every number against the cited text by rule, and abstain when a check fails.

**What happens when two official sources disagree?** They do disagree in places, for example two FBR sources on company registration. The assistant shows both with their dates and says they conflict, instead of choosing one silently.

**Why LightGBM and not a neural re-ranker?** We have a few structured features and a few thousand synthetic pairs, no interaction logs. Boosted trees fit that, train on a CPU in seconds, and show which factors drove each match. We also compare against a linear model and a hand-weighted score, and keep the simplest winner.

**Is training on synthetic data legitimate?** It is a stated limit, not a hidden one. No public matching data exists and personal data cannot be scraped. We train on synthetic pairs, but judge only on pairs two of us labeled by hand, so the model cannot grade itself. Results are described as performance on synthetic profiles.

**How do you know the re-ranker works on real people?** We do not yet. We add a small slice of real consenting profiles to the test, label it separately, and plan a partner pilot in FYP-2 to collect real labels.

**Why only about 80 gold questions?** It is what two people can write and check carefully in the time. We say so, report counts with intervals, and do not claim small differences.

**Is the readiness score just a prompt?** Yes, and the report says so. We test it for repeatability, for sensitivity (removing traction should lower the score), and for agreement with human reviewers. It is never a funding probability.

**What if the language model provider changes or the free tier ends?** All calls go through one gateway, so changing provider is a configuration edit. We record the model id with every result and cache outputs, so earlier results stay reproducible.

**Why pgvector and not a vector database?** One store holds profiles and embeddings, and a match query can filter on columns and search vectors together. At our size, exact search is enough.

**What is new compared with existing platforms?** We do not claim to be first. The difference is a startup job path, a cited and abstaining compliance assistant, a separate mentor role, and matching we actually evaluate.

**What about Urdu and Roman Urdu?** The first version is English only. We run a small benchmark first, because Roman Urdu has no standard spelling and we cannot assume it works.

**How do you stop the model from inventing facts in the resume suggestions?** Suggestions appear next to the original, and an automatic diff checks that no new employer, degree, tool or number appears. The owner then rates usefulness.

**What do the classifiers add?** They show a clean supervised pipeline with leakage controls. They are offline studies on global data and never shown to users as a prediction.

## 14. How results map into the D3 report

Your new implementation chapter (the template's Chapter 7, numbered Chapter 6 in your report) takes its results from the results folder, and several earlier chapters must change so they do not contradict it.

### 14.1 Implementation chapter outline

The template asks for algorithmic and procedural detail, not code, and allows the chapter to describe the prototype in FYP-1. Test case tables are marked FYP-II, so check with your supervisor whether a small metrics table is expected now.

| Report section | Content from this playbook |
| --- | --- |
| Prototype overview | Stack, gateway, how components connect (Sections 10 and 11) |
| Compliance assistant | Corpus processing, chunking, retrieval comparison, generation, checks, abstention, results (Section 4) |
| Matching and re-ranker | Synthetic data, features, model selection, hand-labeled test, results (Section 5) |
| Prompted modules | Rubrics, schemas, small test results (Section 6) |
| Verification scoring | Signals, bands, injected-case test (Section 7) |
| Supporting classifiers | Cleaning, leakage controls, macro F1 (Section 8) |
| Frontend implementation | The five-state pattern and screens, with hand-built screenshots |
| Test metrics | The metrics actually collected so far |

### 14.2 Existing text that must change

Search main.tex for each of these.

1. **Abstract and Executive Summary:** both say no models have been trained or evaluated. Rewrite after the first results exist.
2. **Chapter 6 Findings and Challenges:** both repeat that no model is trained. Replace with real results and real limits.
3. **Objectives status table:** update the Delivered and Remaining columns.
4. **GUI section:** it promises ten screens "in D3" and a data dictionary "in the next deliverable". Both are commitments.
5. **Language model naming:** if you move away from Gemini, update every mention.
6. **Plan for FYP-2 and the new Conclusion chapter:** D3 requires a mandatory plan. Change phases that you completed into results.
7. **Re-ranker claims:** main.tex says labels come from self-registration or a partner pilot. Add the synthetic route and say what it can and cannot show.
8. **Chapter 3 wording:** it says external datasets train no re-ranker. That stays true, since the synthetic data is ours, but say so once in the implementation chapter.

### 14.3 Turnitin

Both the plagiarism and AI reports must be 20% or less. Do not paste text from this playbook or from any model into the chapter. Write the implementation and results sections yourselves, from your own CSVs and notes. Email the draft to the library early, since they generate the plagiarism report and you may need a second round.

## 15. Open decisions and next actions

Six decisions are still yours, and the first three block the most work.

### Decisions to make

- [ ] **Language model provider.** Stay on the Gemini free tier, or move to OpenRouter free models? Check current limits and pick one before week 1 ends, since the synthetic judge runs depend on it.
- [ ] **Embedding model.** Run the bake-off in Section 4 and fix one model for both retrieval and matching.
- [ ] **Conflict rule.** Confirm with your supervisor that statute outranks circular and circular outranks web page, and that conflicts are shown, not resolved silently.
- [ ] **Evaluation labelers.** You two are the only labelers. Decide whether to ask the supervisor or a mentor to score the readiness test ideas, since you wrote the rubric.
- [ ] **Scope cut.** Decide now what you drop if time runs short. This playbook suggests cutting the multilingual benchmark first, then the classifiers.
- [ ] **Chapter numbering and Turnitin scope.** Confirm the renumbered chapters and the Turnitin rules with your supervisor in writing.

### Next actions, in order

- [ ] Build the language model gateway with caching and logging.
- [ ] Convert and hash the 11 corpus documents, then check the section splits by hand.
- [ ] Write the first 40 gold questions, half each.
- [ ] Run the first dense retrieval and look at what it misses.
- [ ] Write the attribute sampler for synthetic profiles.

When the first results exist, come back and I will help turn them into the report chapter.

## 16. Gaps found in the audit

The first draft of this playbook left out the items below, which main.tex or D3 requires. Each is short, and none changes the plan above.

### 16.1 Privacy of data sent to language models

- **What goes out:** profiles, CVs, pitch answers and web page text are sent to a third-party model. Free tiers and free models may keep or reuse inputs, so read the current terms of whichever provider you use before sending anything real.
- **Rule:** never send emails, phone numbers or other contact details to a model. Redact them before the call. This supports NFR-6 and NFR-9.
- **Consent text:** the FR-17 notice must say that profile content is processed by an external language model.
- **Evaluation data:** run every experiment on synthetic profiles, your own resumes with permission, or consented pilot data. Never use another person's CV without consent.
- **The gateway cache:** the disk cache in Section 10.3 stores prompts, which can hold personal data. Use it for evaluation runs only. In production, either skip the cache or purge it on account deletion, so NFR-10 (data removed within thirty days) and NFR-11 (logs kept only until deletion) stay true. Prompt and response logs count as personal data.

### 16.2 Prompt injection and untrusted text

CVs, profile fields, linked pages, searched web pages and even corpus documents are text written by someone else, and they can contain instructions aimed at the model.

1. Keep instructions in the system message and wrap untrusted text in clearly marked delimiters. Tell the model that text inside them is data.
2. Never let model output trigger an action. It only returns validated JSON for a person or a rule to use.
3. The rule checks in Section 4.4 (citation and number checks) also limit what an injected instruction can do.
4. Add a small test: put 10 injected instructions (for example, a CV line telling the model to give a top score, or a web page telling it to cite nothing) into test inputs and count how many change the output. Report the count.

### 16.3 Corpus freshness and background jobs

- **Ingestion:** main.tex has Celery and cron jobs pulling whitelisted SECP, FBR and PSEB pages through Firecrawl. Save each page as a dated snapshot with its hash.
- **Updates (R-3):** re-check every document before the demonstration. If a document changed, bump `corpus_version`, re-chunk, re-embed, and rerun the gold set. A changed corpus can change old results.
- **Embeddings:** regenerate them when a profile is edited or the embedding model changes. If you change the embedding model after the bake-off, the stored vectors and the re-ranker features must both be rebuilt.

### 16.4 Performance numbers from the requirements

main.tex sets targets that these tests can check cheaply now, with the full load test left for FYP-2.

| Requirement | Target | What to measure now |
| --- | --- | --- |
| NFR-2 | A model request in about 8 seconds, with about 5 at once | Median and 95th percentile latency over 50 requests per AI endpoint, and what happens when 8 are sent at once |
| NFR-3 | A match query in about 2 seconds on the seeded data | Median and 95th percentile over 50 queries |
| NFR-1 | 50 concurrent users | Left to the FYP-2 load test (Phase 6) |

### 16.5 Error analysis

Numbers alone do not convince a panel. After each evaluation, read every wrong answer or wrong ranking and give it one cause: retrieval missed it, the chunk split a clause, the model ignored the evidence, a check was too strict, or the gold label was wrong. Report the counts. This also shows you whether to fix retrieval, chunking or the prompt next.

### 16.6 What this playbook updates in the FYP-2 plan

D3 requires a plan for FYP-2. The plan table in main.tex lists six phases. After D3, change them like this.

- **Phase 1 (assistant):** move the gold set, the corpus and the first evaluation to done. Keep the larger corpus and a re-run on new documents.
- **Phase 2 (matching):** record the synthetic training and hand-labeled test as done. Keep real labels from a partner pilot as the main open item.
- **Phase 3 (prompted modules):** record which small tests you finished.
- **Phase 4 (benchmark and classifiers):** mark what you ran, and leave only what you cut.
- **Phases 5 and 6:** unchanged.

### 16.7 Required for D3 but outside this playbook

- Rebuilding the Figma or prototype screens by hand and the ten missing screens.
- The data dictionary for the 41 tables.
- The renumbered chapters, and the Turnitin plagiarism and AI reports.
- The test case design section and the user manual, which the template marks FYP-II.

## 17. Everything else D3 needs

Section 16.7 listed work outside the AI side. This section covers it too, so the playbook is a full D3 checklist. Items marked "confirm" depend on your supervisor.

### 17.1 D2 feedback tracker

| D2 feedback | Where it is handled | Done when |
| --- | --- | --- |
| No model trained, decide which model and how | Sections 4, 5, 8 and the register in 10.1 | At least the assistant and the re-ranker have results CSVs and a report section |
| Re-ranker dataset, use synthetic data | Section 5 | Synthetic set, hand-labeled test and the decision rule are all written down and run |
| Figma prototypes look AI-generated | 17.2 below | Every screen rebuilt by hand and re-screenshotted |

### 17.2 Frontend screens

main.tex says ten screens are "added in D3" and four requirements have no screen. Together with redoing the twelve existing ones, that is the full list.

| Screen | Requirement | AI states needed |
| --- | --- | --- |
| Appeal form | FR-21 | None |
| Compliance assistant panel | FR-8 | All five (Section 11.2) and both abstain messages |
| Talent profile | FR-5, FR-13 | None |
| Resume optimizer | FR-5 | All five |
| Talent matches | FR-7 | Success, empty, locked contact |
| Mentor profile | FR-29 | None |
| Mentor requests | FR-7 | None |
| Investor profile | FR-12 | None |
| Investor founders list | FR-10 | None |
| Investor requests | FR-7 | None |
| Market research | FR-4 | All five and partial results |
| Usage guides | FR-18 | None |
| Job listing management | FR-24 | None |
| Consent and account deletion | FR-27 | None |

Also: redo the five navigation flow figures so they include the new screens, rebuild the twelve existing screens by hand, and make every number on a screen a clearly marked sample. Keep the screenshots in the same tagged format main.tex already uses, naming the use case or requirement each covers.

### 17.3 Data dictionary

The GUI chapter says the data dictionary for the 41 tables and 264 attributes comes in the next deliverable, so D3 is that deliverable.

1. Build the schema from your migrations on an empty database.
2. Query the database catalog (`information_schema.columns` plus the foreign key constraints) and export one CSV row per attribute: table, attribute, data type, key or referenced table, nullable, and a description.
3. Write the descriptions by hand. A generated description adds nothing and will read as generic.
4. Check the counts. main.tex calls 41 tables and 264 attributes planning figures. If the real schema differs, update every mention (abstract, assumptions and Chapter 4).
5. Turn the CSV into a long table in the report, grouped by the five modules.

### 17.4 Chapter renumbering

The template skips Chapters 5, 8 and 9 for development projects, so your Implementation chapter is 6 and Conclusions is 7, while D3 says Chapter 7 and Chapter 10. Confirm this with your supervisor in writing.

1. Search main.tex for hard-coded chapter numbers ("Chapter 3", "Chapter 5", "Chapter 6" and so on) in the introduction, executive summary, chapter conclusions and risk text.
2. After inserting the new chapter, every later number moves. Prefer `\ref` to a chapter label so it cannot go stale.
3. Update the outline paragraph at the end of Chapter 1, which summarizes each chapter in one line.
4. Recompile twice so the table of contents, figure and table lists settle.

### 17.5 Test cases and metrics (confirm)

The template marks test case design FYP-II, but a short start is cheap and uses work you are already doing.

- **Starter test cases,** in the template table format, for four use cases that map to this playbook: ask a compliance question, abstain when no answer exists, request a match and keep contact details locked until acceptance (NFR-6), and verify a profile automatically.
- **Test metrics table:** number of test cases, passed, failed, defect density (failed times 100 over executed), and a traceability matrix that links each requirement to at least one test. Fill only what you really ran.
- **Rule:** put numbers in the table only from executed tests. A planned test is listed as not executed.

### 17.6 User manual

The template marks it FYP-II, so leave it out of D3. Do not describe a feature in it that has not been built.

### 17.7 Turnitin and submission

1. Finish the text first. Sending a draft that later changes means getting new reports.
2. Remove every leftover template instruction paragraph and sample table. They are common text and raise the match.
3. Email the report to librarylhr@nu.edu.pk and ask which file format they want.
4. Get both the plagiarism and the AI report. Each must be 20% or less.
5. If one is above 20%, find the highlighted passages. Usual causes are long tables copied from sources, quoted regulations, definitions and acronym lists, and text that reads as machine-written. Rewrite those in your own words, then resubmit.
6. Ask the FYP coordinator for the Report Submission Instructions document and check naming, upload channel and any page limit. I have not seen that document.
7. Update the report date on the title page and in the anti-plagiarism declaration, which still read 21 October 2026.

### 17.8 Final consistency pass

Before the last compile, search main.tex for these.

| Search for | Reason |
| --- | --- |
| "no model", "not trained", "not been trained" | Contradicts your new results |
| "D3", "next deliverable", "added in" | Promises that must now be kept or removed |
| "Gemini" | Update if the provider changed |
| "41 tables", "264", "31 functional", "23 non-functional", "17 features" | Counts must still match the real system |
| "FYP-1" and "FYP-2" next to a feature | Moved items must be in the right semester |
| Figure and table labels | Every figure has the mandatory description line and no broken reference |
| Duplicate paragraph in Section 1.1 | The purpose paragraph appears twice in the current main.tex, remove one |

Compile with no undefined references and no missing images before you send anything to the library.

## 18. Starting implementation with coding agents (written against your repository)

These prompts assume the repository as it stands on 11 November 2026: a backend with auth, founder profiles, compliance, matching, readiness and pitch endpoints, a working LLM gateway, a RAG ingestion pipeline, and a frontend with 24 routes. Section 20 lists what exists. The prompts extend that code. They do not start over.

Your AGENTS.md and CLAUDE.md already set rules that every prompt must respect, so the prompts do not repeat them. The ones that shape how you prompt:

- The agent plans first and waits for your yes before anything bigger than a small fix.
- The agent never commits, pushes, deletes or moves files. You commit on a branch and open a pull request.
- Before changing an existing file, the agent names it, says what changes, and backs it up with `python scripts/backup.py snapshot <path>`.
- The agent asks before installing a package, adding a migration or a new table, or changing an API contract.
- Python 3.11 in a `.venv` per folder, pinned versions in requirements.txt, commands for Windows PowerShell.
- Each finished piece gets an entry in `docs/build-log.md`. Anything that differs from the report also gets a dated entry in `docs/DECISIONS.md` and a row in `docs/pending-report-changes.md`.
- Cite FR and NFR IDs from `docs/context/requirements.md`, not from the data dictionary, which uses an older numbering.

### 18.1 Lines to add to CLAUDE.md or AGENTS.md (only what is missing)

```text
Evaluation rules (rag/, ml/, backend/): fixed random seeds; saved split files; every result is written to a CSV with a README giving the exact command that produced it; no accuracy figure appears in any document until that CSV exists. Extend existing modules instead of creating parallel ones. Before writing an AI module, read docs/context/ai-features.md and the matching file in backend/app/services/.
Re-ranker data: do not generate or train on synthetic pairs until docs/DECISIONS.md contains the entry that approves it. Generated data lives in ml/, every row is marked synthetic: true, and it is listed in docs/datasets.md.
The supporting classifiers are FYP-2 offline studies. Do not start them unless I ask.
```

### 18.2 Prompt 1: extend the LLM gateway

```text
Read backend/app/services/llm_gateway.py and backend/tests/test_llm_gateway.py first. The gateway already has a five-slot semaphore (NFR-2), retries, a fallback model and logging. Do not rewrite it. Show me a plan and wait for my yes.
Then add, as separate small changes:
(a) An on-disk cache keyed by a hash of the full input (model id, prompt version, messages, response schema, temperature), switched on by config, so repeated evaluation runs cost no quota and give identical outputs.
(b) A persisted call log with model id, prompt version, token counts, latency, outcome and whether it was a cache hit (NFR-15, NFR-19). This needs a new Alembic migration, so show me the table design and wait for approval before creating it.
(c) The queue position, exposed to the caller, so a route can return a queued state and a position instead of blocking.
(d) A small registry of versioned prompts under backend/app/prompts/, so every module names its prompt version in one place.
Extend tests/test_llm_gateway.py with a fake provider: cache hit returns identical output and makes no provider call, six simultaneous calls run five and queue one, the call is logged. Do not call the real API in tests. Back up each existing file before editing. Run pytest from backend/ and report the real output. Add a build-log entry. Do not commit.
```

### 18.3 Prompt 2: gold set, retrieval comparison and end-to-end evaluation

```text
Read rag/, backend/app/services/compliance_retrieval.py, compliance_assistant.py, docs/context/corpus.md and rag/corpus_manifest.md. Already built: section-aware chunking, a provisional default embedding model (paraphrase-multilingual-mpnet-base-v2), dense top-5 retrieval, answer generation with an LLM grounding validator, abstention reasons, citations and a query log. Not built: a gold set, an evaluation harness, BM25 or hybrid retrieval, and any model comparison.
Show a plan and wait for my yes, then build in rag/evaluation/:
1) A gold question file format (rag/evaluation/gold_questions.jsonl): id, question, answerable true or false, the supporting section references, a category tag for out-of-scope questions, and a dev or test split. Build the loader and a ten-question starter file. I will write the real questions by hand. Do not generate gold answers.
2) A retrieval harness that compares dense (current), BM25 and hybrid with reciprocal rank fusion, for each embedding model in config: the current default, multilingual-e5-base and bge-m3. Compute Recall@5 and MRR on the dev split and write results/retrieval.csv. Tell me before installing anything and pin the versions.
3) An end-to-end run of ComplianceAnswerService over the gold set that measures citation correctness, unsupported-claim rate, and abstention precision and recall, with a no-retrieval baseline using the same model. Use the gateway cache.
4) A rule-based check in the answer service, in addition to the existing LLM validator: every number and date in the answer must appear in a cited chunk, otherwise abstain. Add tests.
Verify corpus file hashes against the manifest before indexing. Never index a superseded version. Make no accuracy claim until a results CSV exists, and say what was and was not run. If the default embedding model changes, add the DECISIONS entry and the pending-report row. Do not commit.
```

### 18.4 Prompt 3: the two prompted features that do not exist yet

```text
Read backend/app/routes/intelligence.py, backend/app/services/feature_ai.py, feature_schemas.py and feature_models.py. Readiness and pitch practice already follow the pattern: typed schema, gateway call, structured output saved with its prompt version. Build market research (FR-4) and the resume optimizer (FR-5) the same way. Show a plan and wait for my yes.
Market research: a query returns a competitor and market summary from live public web sources through Firecrawl, with evidence kept apart from interpretation, every source listed with its link and retrieval date, and a status of queued, running, complete or failed. Public pages only. Never scrape personal profiles (PECA 2016). Ask before adding the Firecrawl dependency or any key.
Resume optimizer: upload with type and size checks, stored outside the served folder (NFR-7), line-level before and after suggestions, and a check that no suggestion adds a claim that is not in the original. No external resume dataset.
Do not create tables or migrations without showing me the design first. Tests use a fake gateway. Cite FR and NFR IDs in code comments. Add build-log entries. Do not commit.
```

### 18.5 Prompt 4: synthetic re-ranker data (run last, after the DECISIONS entry exists)

The repo's 19 October decision says the re-ranker trains only on the team's own labeled pairs. D2 feedback allows synthetic data. Write the new DECISIONS entry first (a draft is in 20.4), then run this.

```text
Generate synthetic training data for the matching re-ranker under ml/ranker/. Use the real fields: startups (sector, stage, skills, location, funding need min and max, description) from backend/app/models.py, and ecosystem profiles (sector, stages, skills, availability, ticket min and max, location, summary) from backend/app/feature_models.py. The five factors are the ones in backend/app/services/matching.py: sector_fit, stage_fit, skill_overlap, availability_fit, ticket_fit.
Task A: write a generator script that produces about 300 synthetic startups and 600 synthetic counterparts for Pakistani tech startups, varied across sectors and stages, with some hard-filter violations on purpose. Every row has synthetic: true. No real people or companies.
Task B: a labeling script that asks a model to rate 20 candidates per startup from 0 to 4 with a one-line reason, through the gateway, using a different model from the one that wrote the profiles. Filter violations are forced to 0 by code, not by the model.
Save the prompts, model ids, seeds and the output files. Add the entry to docs/datasets.md. Then list five ways these labels are circular or biased.
Ask before installing anything. Do not commit.
```

The labels are for training only. The test set is the pairs that you and Shahzeb label by hand.

### 18.6 Prompt 5: hand-labeled test set and the re-ranker (run last)

Manual step first: you and Shahzeb each label about 100 candidate pairs independently, before looking at any model output, and save them to ml/ranker/handlabeled/. The report's own plan (risk R-1) is 150 to 300 labeled pairs, otherwise a stated pilot result against the baseline.

```text
Under ml/ranker/, train a LightGBM model with the lambdarank objective on the synthetic pairs. Features: the five factors from backend/app/services/matching.py plus the semantic similarity. Split by startup, never by pair, with a saved split file and seed, and a test that no startup appears in both train and test. Baselines: cosine similarity alone, and the existing weighted score (MATCH_WEIGHTS blended 0.5 with semantic similarity). Report NDCG@5, NDCG@10, MRR, Precision@K and Recall@K on the synthetic test split and on the hand-labeled set, which is never used for training, to ml/ranker/results/ranker.csv. Label every result a pilot unless 150 or more real labeled pairs were used. Export feature importances so each match can show its factors.
Anything that ships goes through backend/ as a service behind an interface, never as a notebook. Keep rerank_score empty until the model passes: it goes live only if it shows no regression against the baseline. If the match table has no column for the re-rank score, ask before adding one.
Ask before installing lightgbm and pin the version. Do not commit.
```

### 18.7 Order and checks

1. Prompts 1 and 2 first. The compliance assistant is the FYP-1 checkpoint in your build order, and no lower item is extended until it gives cited answers and abstains correctly on a held-out set.
2. Prompt 3 next, in the order the coding plan gives: readiness and pitch exist, then market research, then the resume optimizer.
3. Prompts 4 and 5 last, because they need the manual labeling. Draft the generation script earlier if you like, but run it only after the gateway cache exists and you know your daily quota.
4. Reserve at least four to five days at the end for Prompt 5. If you run out of time, report a stated pilot result against the baseline, and make no accuracy claim.
5. After each prompt: run pytest yourself from `.venv`, open the results CSV, and reject any number you cannot reproduce with the README command. Then commit on a branch and open a pull request. The CI workflow has never run on GitHub, so do not claim that it checks anything until a test branch confirms it.
6. Never paste real personal data or API keys into any tool. The repo's key scan runs in CI, but it is no excuse.

## 19. The implementation chapter, written to template.tex

The chapter is not only about models. template.tex asks you to elaborate whatever you have implemented so far, with the algorithms, platform and APIs, so it must cover the whole system: frontend, backend, database, and the AI components. This section extends 14.1, which covered only the AI parts.

### 19.1 Numbering and what the template requires

- The template's Chapter 7 (Implementation and Test Cases) is Chapter 6 in your report, because main.tex has no Proposed Approach chapter for a development project. The Conclusions chapter becomes Chapter 7. Confirm this with your supervisor, as already noted.
- Template rules for this chapter: a paragraph of introduction and a paragraph of conclusion; algorithmic and procedural detail, not programming code; for FYP-1 the chapter may describe the prototype.
- Three sections: Implementation, Test case design and description, Test Metrics. The template marks the test case section as added in FYP-II, so the Implementation section carries most of D3. Ask your supervisor whether a short starter test section is expected now. 17.5 recommends one.
- Every figure needs a caption that describes the picture for a screen reader (the template calls this mandatory). Code goes in the appendix only, and the chapter text must be written by you, not pasted from any model (Turnitin AI report 20% or less).

### 19.2 Section outline

| Report section | What to write | Evidence to collect |
| --- | --- | --- |
| 6.1 Implementation: platform and environment | Stack (Next.js, Tailwind, shadcn/ui, FastAPI, PostgreSQL 16 with pgvector, Celery), free-tier hosting, repository layout, pinned versions, what is mocked and what is live | Repository tree, package versions |
| 6.1.1 Backend and API | API gateway and the six services as built, role-based access, LinkedIn OAuth sign-in, the consent and mutual-reveal state machine (contact hidden until both sides accept), background queue, endpoint table | Endpoint list, state diagram |
| 6.1.2 Database | Tables actually created and migrated, pgvector columns, data dictionary (the GUI section promised it in D3) | Schema export |
| 6.1.3 Frontend | Design system tokens, screens built per role (use the P-list from the prototype work), the five-state pattern for AI screens, mobile layouts, what runs on mocks | Screenshots with captions |
| 6.1.4 LLM gateway | Cache, logging, queue of five (NFR-2), provider swap by configuration (NFR-19) | Gateway tests output |
| 6.1.5 Compliance assistant | Section 4 of this playbook: processing, retrieval comparison, grounded generation, validators, abstention (NFR-13) | rag\_retrieval.csv, rag\_answers.csv |
| 6.1.6 Matching and re-ranker | Section 5: cosine stage with hard filters, features, LightGBM, synthetic training, hand-labeled test. Written last, as results arrive | ranker.csv |
| 6.1.7 Prompted modules | Section 6: readiness, pitch simulator, market research, resume optimizer, with rubrics and schemas | Small test tables |
| 6.1.8 Verification and classifiers | Sections 7 and 8, each in half a page | Injected-case results, macro F1 |
| 6.1.9 Not yet implemented | A plain list of what is only designed (for example the multilingual benchmark, if not started). This feeds the Conclusion's FYP-2 plan | Your own task list |
| 6.2 Test case design and description | Shared attributes of the test cases, then the table(s) in the template format (19.3) | Test run output |
| 6.3 Test metrics | The template's metric table, filled only from executed tests (19.4) | Test counts |

For each algorithm, write the procedure as numbered steps in plain English (input, steps, output), and give the reasoning for the choice and the rejected alternative once. Do not paste code, prompts or model output into the chapter.

### 19.3 Test cases: two kinds, kept apart

- **Pass or fail tests** (backend, frontend, security). These use the template's test case table.
- **Model evaluations** (Recall@5, MRR, NDCG, abstention rates). These are measurements, not pass or fail. Report them in the implementation subsection of that component, or in a results table, and do not count them in the test-case metrics.

Starter set, using only requirements that main.tex actually states. Status stays "Not executed" until you run it.

| ID | Component | Test | Requirement |
| --- | --- | --- | --- |
| TC-01 | Auth | A user signs in and is routed to the dashboard of their own role only | Role-based access |
| TC-02 | Gateway | A repeated identical request returns the cached answer and makes no provider call | NFR-19 |
| TC-03 | Gateway | Six simultaneous requests: five run, one waits and shows a queue position | NFR-2 |
| TC-04 | Compliance | A question with no supporting passage returns abstain true with a reason | NFR-13 |
| TC-05 | Compliance | Every non-abstaining answer carries at least one citation with a date | NFR-12 |
| TC-06 | Matching | Candidates in the wrong sector, stage or geography never appear in the results | Hard filters |
| TC-07 | Matching | Contact details stay hidden until both sides accept | NFR-6 |
| TC-08 | Matching | Each match response lists its factors | NFR-15 |
| TC-09 | Re-ranker | No startup appears in both the training and the test split | Method |
| TC-10 | Verification | A deliberately incomplete profile lands in a lower band than a complete one | Verification rules |
| TC-11 | Frontend | An AI screen renders all five states: queued, loading, success, abstain, failure | Playbook 11.2 |
| TC-12 | Frontend | AI output is marked as written by a language model | Use case text |

Check each requirement ID against main.tex before you write it into a test case.

### 19.4 Test metrics

Use the template's table: number of test cases, passed, failed, defect density (failed times 100 divided by executed), test case effectiveness, and a traceability matrix. Fill it only from tests you ran. Test case effectiveness needs a count of defects found, so leave that row as FYP-II if you have not logged defects. The traceability matrix can be built now: one row per requirement from the starter set, one column for the test that covers it.

### 19.5 Order of writing

1. Write 6.1.1 to 6.1.4 first. They need no model results.
2. Write 6.1.5 and 6.1.7 as each component produces its results file.
3. Write 6.1.6 last, with the re-ranker.
4. Write 6.2 and 6.3 after you run the tests, then the chapter introduction and conclusion paragraphs.
5. Then update the Conclusions chapter (new Chapter 7) and the list in 14.2.

## 20. What the repository already contains, and what changes

Read from github.com/whozahm3d/founders-carnet (latest commit: merge of pull request 17) and the data dictionary approved on 5 October. I read the code and the docs. I did not run the tests, the app or the migrations, so "works" below means the code exists, not that it was run.

### 20.1 Status by component

| Component | In the repo | Not there yet |
| --- | --- | --- |
| Auth (FR-22, FR-23) | register, login, logout, current user; roles; token version; sanitized validation errors; 8 tests | LinkedIn sign-in; a consent record table (consent is stored inside the founder and ecosystem profile rows); account deletion; withdrawal of consent |
| Founder data (FR-1) | profile and startups: create, read, update; consent version stored | readiness gating of investor visibility (FR-10) |
| Compliance assistant (FR-8) | corpus indexer; section-aware chunking; provisional embedding default (paraphrase-multilingual-mpnet-base-v2); dense top-5 retrieval; answer generation; LLM grounding validator; abstention with reasons; citation fields with dates; query log; about 20 tests | gold question set; evaluation harness; BM25 and hybrid retrieval; embedding comparison; rule-based number and date check |
| LLM gateway (NFR-2, NFR-19) | Gemini client; five-slot semaphore; retry; fallback model; logging through the logger; prompt version strings; 11 tests | disk cache; persisted call log; queue position visible to callers; one prompt registry |
| Matching (FR-7) | ecosystem profiles; five factor weights (0.25, 0.20, 0.25, 0.15, 0.15) blended 0.5 with semantic similarity; factors stored; accept by both sides; contact email only after mutual acceptance; no model call | I could not confirm that candidate search uses pgvector with hard filters. The matching code imports a Python cosine function. Check this against the report, which says pgvector with filters. No re-rank score column |
| Readiness (FR-2), pitch (FR-3, FR-28) | endpoints, schemas, tables; four-area pitch rubric; history | calibration against human reviewers (FYP-2) |
| Not started | verification scoring, admin review and appeals (only a stats endpoint exists), jobs and applications, resume optimizer, market research, consent management, usage guides, Redis and Celery (only an environment variable; compose has the database only), API container, supporting classifiers (ml/ holds preprocessing and dataset profiling only), re-ranker, multilingual benchmark |  |
| Frontend | Next.js 16 and React 19, 24 routes for five roles, auth pages, founder screens built from the wireframes, responsive layout, route guards, a mock mode (on unless NEXT\_PUBLIC\_USE\_MOCK is false) | Tailwind and shadcn/ui (the report says both; the app uses CSS Modules); a typed API client; tests; httpOnly cookie instead of localStorage; placeholders for most talent, mentor, investor and admin pages |
| Tests and CI | about 56 backend test functions in 12 files, 11 in rag/ | frontend tests; CI has never run on GitHub (your own pending-changes table says so) |

### 20.2 Where the repository and the earlier sections disagree

| Earlier section | I wrote | The repository says | What to do |
| --- | --- | --- | --- |
| 3, timeline | 2 to 4 weeks of build | Coding plan: feature freeze about 6 November, report due 11 November | Confirm the real D3 date with your supervisor today. If it is 11 November, the plan in Section 3 is too long |
| 4.1, embeddings | bake-off of e5, bge-m3 and an English floor | The backend default is paraphrase-multilingual-mpnet-base-v2, marked provisional until evaluated | Add the current default as the incumbent in the bake-off |
| 4.1, retrieval | dense, BM25, hybrid | Only dense exists | Build the other two in Prompt 2 and keep hybrid only if it wins |
| 4.5, gold set | about 80 questions | The coding plan says 20 to 22 hand-verified questions. The report gives no number | Start at the committed number, grow it if time allows, and state the real count in the report |
| 5, re-ranker data | synthetic pairs and LLM labels | DECISIONS 19 October: the re-ranker trains only on the team's own 150 to 300 labeled pairs | Write a new DECISIONS entry and a pending-changes row first (draft in 20.4) |
| 8, classifiers | in the 2 to 4 week plan | Approved on 21 October as offline FYP-2 studies. Rules: deduplicate before splitting, 1990 to 2015 filter for Success/Fail, drop funding and post-outcome columns, macro-F1 against a simple baseline. None is trained | Mark as optional, lowest priority. Drop the DistilBERT idea, which is not in the repo plan |
| 10.3, gateway | build it first | It exists | Extend it (Prompt 1) |
| 10.3, provider | OpenRouter free models as an option | Gemini 2.5 or below, model ids in configuration, fallback inside the gateway | Moving provider needs a DECISIONS entry and an update to main.tex |
| 11.1, endpoints | planned paths such as /compliance/ask | Real paths are under /api/v1 (see 20.3) | Use the real ones |
| 11.2, queued state | 202 with a job id | The gateway queues inside the process. No route returns a queued response yet | Prompt 1 exposes the queue position, then a route can use it |
| 6.3, pitch rubric | four areas | Four areas (clarity, market understanding, defensibility of numbers, handling pushback). coding-plan.md still says three | Matches. Fix coding-plan.md |
| Report, database | PostgreSQL 16 | compose.yaml uses pgvector/pgvector:pg17 | Change one of them and log it |
| Data dictionary | 41 tables | 12 tables exist, with different names (users, founder\_profiles, startups, compliance\_documents and so on) and integer ids, not uuid | See 20.5 |

### 20.3 Endpoints that exist today

| Method and path | Purpose |
| --- | --- |
| POST /api/v1/auth/register, /login, /logout | Account and session |
| GET /api/v1/users/me, GET /api/v1/admin/stats | Current user, admin statistics |
| PUT, GET /api/v1/founders/me/profile | Founder profile with consent |
| POST, GET /api/v1/founders/me/startups, PATCH .../startups/{id} | Startups |
| POST /api/v1/compliance/questions | Compliance answer |
| PUT /api/v1/matching/me/profile | Mentor or investor ecosystem profile |
| GET /api/v1/matching/startups/{startup\_id}, GET /api/v1/matching/me | Matches for a startup, matches for me |
| POST /api/v1/matching/{match\_id}/accept | Accept a match |
| POST, GET /api/v1/startups/{startup\_id}/readiness | Readiness assessment |
| POST /api/v1/pitch/sessions, .../{id}/turns, .../{id}/abandon, GET /api/v1/pitch/history | Pitch practice |

The compliance response carries query\_id, outcome (answered or abstained), answer, message, abstention\_reason, citations (chunk id, document title, issuing body, source URL, section, page number, effective date, consolidation date, retrieved date) and an informational notice. A match carries the five factors, the semantic similarity, the score, both sides' acceptance, and the contact email only after mutual acceptance.

Not there yet: verification, admin review and appeals, jobs, resume, market research, consent withdrawal and deletion. Their requirement IDs are in the backend guide.

### 20.4 Draft DECISIONS entry for the synthetic re-ranker data

Write this in docs/DECISIONS.md in your own words, check the facts, and add the matching row to docs/pending-report-changes.md. Do not paste it unchanged.

```text
## 2026-11-11: Re-ranker trains on synthetic pairs, tested on hand-labeled pairs

Context: The 2026-10-19 entry says the re-ranker trains only on our own 150 to 300 labeled pairs. The D2 feedback says to train on synthetic data if no real data arrives, and to use it fully if real data never comes.
What we found: We found no public labeled dataset for Pakistani founder-mentor or investor matching, and no partner has supplied labels.
Decision: Train the re-ranker on synthetic startup and counterpart profiles with model-judged labels (filter violations forced to zero by code). Evaluate on about 100 pairs labeled independently by two team members, never used for training. Report every result as a pilot unless 150 or more real labeled pairs were used. The cosine baseline and the weighted score stay as baselines.
Relation to the 2026-10-19 entry: it stays in the log and is not deleted. It still governs real labels. This entry adds the synthetic route and says how the two are used together.\nWhy: It answers the D2 comment without claiming accuracy that synthetic data cannot support.
Follow-ups: docs/datasets.md entry for the synthetic data; main.tex re-ranker wording (Chapter 3, Chapter 5, Chapter 6); CLAUDE.md and docs/context/ai-features.md.
```

### 20.5 The data dictionary and the real schema

The approved dictionary has 41 tables. Four are tagged FYP-2 (subscription, event\_listing, resource\_link, placement\_fee\_event), which leaves 37 for FYP-1. The code has 12 tables with simpler names and integer ids. That is allowed: CLAUDE.md calls the 41-table schema a design baseline and says to update the dictionary and ER diagrams when the real schema differs.

- The report's data dictionary section must describe what you actually built, or say plainly which tables are designed but not built. Do not put 41 tables in the implementation chapter if 12 exist.
- Pick one of two routes and log it: change the code toward the dictionary (large, and unlikely to fit the time), or regenerate the dictionary and ER figures from the real models and mark the rest as designed.
- The dictionary's own open items still apply: FR numbers FR-22 to FR-26 are assumptions, FR-1 to FR-6 use an older numbering, and the pitch table still lists five areas in the .tex file.
- Missing for the verification story: verification\_case, verification\_signal, review\_decision, appeal, report\_flag and audit\_log. They are the largest gap between the report and the code.
