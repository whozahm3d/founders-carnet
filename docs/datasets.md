# Datasets

Record every dataset here before it is used. `CLAUDE.md` says no dataset is used unless it is listed. For each one, say what the supervisor will ask: what it contains, why it was chosen, and which user input it serves.

Rules that apply to all of them (see the data rules in `CLAUDE.md`):

- External datasets are for profiling, schema design, and aggregate baselines only. None of them trains the deployed re-ranker.
- Age and gender are never matching features.
- Do not store names, birth dates, or contact fields from external datasets.
- Do not redistribute a dataset. Raw data stays out of git.
- No data without consent.

## Selection rules

- **Tech niche:** The platform focuses on tech startups and technical talent only. General sector datasets are filtered to tech where possible.
- **Pakistan first:** Local Pakistani datasets are prioritized where available. Foreign datasets serve only as structure or method proxies.
- **Aggregates only:** External datasets are used for profiling, schema design, and aggregate baseline comparisons only. Deployed matching models do not train on external data.
- **No personal data:** Never store, print, or expose individual names, contact fields, or personal identifiers from external datasets.
- **Licence recorded as stated:** Licences are recorded strictly as stated on the dataset repository page or card metadata (or "No License Provided" / "Not stated").
- **Conservative title matcher:** The title matcher uses word boundaries and avoids loose substring matching; because it misses specific tool/framework titles like "Php", "Laravel", "Java", or "React", reported tech shares are "at least".
- **Category-list filter:** Crunchbase datasets use the category-list filter, which matches broad technology terms across pipe-separated categories.
- **Status labels:** The `status` column in `ml/notebooks/dataset_fit_scores_v2.csv` was set by hand to match the final decisions in this file and in `docs/DECISIONS.md` (2026-10-18). Notebook-assigned labels differed for five datasets. This file and `DECISIONS.md` are authoritative.

## Filters used

- **Crunchbase category-list tech terms (lowercase, matched on "|"-split categories):** software, saas, artificial intelligence, machine learning, analytics, big data, enterprise software, internet, mobile, apps, web development, cloud computing, cyber security, fintech, e-commerce, computer vision, data, developer tools, information technology. This filter is broad.
- **Title matcher (job titles and resume job_title; word-boundary, case-insensitive):** software (engineer, developer, architect), developer, programmer, frontend, backend, fullstack, full-stack, web developer, mobile developer, android, ios, data scientist, data analyst, data engineer, machine learning, ml engineer, ai engineer, artificial intelligence, deep learning, devops, cloud (engineer, architect), cybersecurity, qa (engineer, tester, analyst), quality assurance, database administrator, dba, sysadmin, system administrator, network engineer, information technology, it (specialist, manager, officer, support, engineer, consultant), tech lead, cto. It misses titles such as "Php", "Laravel", "Java", "React", so shares are "at least".
- **haider tech categories:** Java Developers, Web Developer, SQL Developers, Network and Systems Administrators, Datawarehousing/ETL, Business Intelligence. Excluded: Business Analyst, Project Manager, Recruiter.
- **LinkedIn Intro keyword list (informational only):** software, engineer, developer, data, machine learning, artificial intelligence, cloud, devops, backend, frontend, full stack, programmer, analytics, cyber security, saas, startup, tech, computer science, information technology.
- **Finance QA keywords:** secp, fbr, tax, company, registration, bank, zakat, license, return, filing (generic words included, so shares are indicative). Authority terms: sbp, secp, fbr, state bank, federal board of revenue, securities and exchange.

## Datasets in use

### FINAL

#### Roman-Urdu-Parl split

- **Status:** FINAL
- **Reason:** Only large parallel Urdu and Roman Urdu text found; clean train/test split with zero pair overlap.
- **Counts:** Train 6,365,808; validation 20,719; test 20,741; total 6,407,268; 2 columns ("Urdu text", "Roman-Urdu text").
- **Licence as stated:** Apache 2.0 in the card metadata of the Mavkif split repository (the original dataset's licence was not checked)
- **Requirement served:** R5 multilingual benchmark
- **Tech filter:** Kept whole (general language domain)
- **Limitations:** Butt et al. (arXiv:2503.21530) describe the source sentences as "collected from various informal online sources", not startup or regulatory text; validation and test (41,460 pairs) sit on top of the original count of 6,365,808 that the split card states.
- **Description:**
  (1) Parallel Urdu and Roman Urdu text pairs created by Mavkif on Hugging Face based on the paper by Alam and Hussain (ACM TALLIP 2022).
  (2) Used for requirement R5 as parallel text benchmark and language representation for Urdu and Roman Urdu.
  (3) Chosen as the only large parallel Urdu and Roman Urdu corpus available with zero pair-level split overlap.
  (4) Sentences come from general informal online sources rather than startup or regulatory text, and the Apache 2.0 licence is stated on the split repository only.

#### Pakistan Startup Census

- **Status:** FINAL
- **Reason:** Only structured public census dedicated specifically to Pakistani startups.
- **Counts:** 433 usable rows (553 physical rows, 120 blank rows); 7 columns (Name, Location, Tagline, Category, Website, Founded, Description); duplicate names on usable rows: 1.
- **Licence as stated:** "No License Provided" (research use only)
- **Requirement served:** R3 startup discovery
- **Tech filter:** Strict tech share at least 11.78%
- **Limitations:** 2021 static snapshot; research use only; licence not provided; duplicate names on usable rows (1); a listing page says 434.
- **Description:**
  (1) Directory of Pakistani startups created by Zeeshan-ul-hassan Usmani on Open Data Pakistan (CHISEL at LUMS) in April 2021.
  (2) Used for requirement R3 startup discovery directory schema design and location distribution profiling.
  (3) Chosen as the only structured public census dedicated specifically to Pakistani startups.
  (4) A 2021 static snapshot with no licence provided, containing 120 blank rows and 1 duplicate name.

#### Pakistan's Job Market

- **Status:** FINAL
- **Reason:** Primary source for real Pakistani employer job postings, titles, and city distributions.
- **Counts:** 6,680 rows, 9 columns (2019-12-18 to 2021-03-15; Lahore 2,046, Islamabad 1,921, Karachi 1,700); duplicates on title+company+date 19.64%.
- **Licence as stated:** ODbL on Open Data Pakistan copy; Kaggle shows "Data files (c) Original Authors" (cite Open Data Pakistan copy; attribution required).
- **Requirement served:** R2 matching and job board (job-description side of resume-JD tests)
- **Tech filter:** Strict tech share at least 26.8%
- **Limitations:** Job description text is cut at 250 characters; historical data from 2019 to 2021; 19.64% duplicates on title+company+date.
- **Description:**
  (1) Pakistani job postings dataset uploaded by Zeeshan-ul-hassan Usmani on Kaggle and Open Data Pakistan.
  (2) Used for requirement R2 matching and job board for the job description side of resume-JD tests.
  (3) Chosen as primary source for real Pakistani employer job titles and city distributions (Lahore, Islamabad, Karachi).
  (4) Job description text is cut at 250 characters and historical postings end in March 2021.

#### Startup Success/Fail (Crunchbase)

- **Status:** FINAL
- **Reason:** Closest public shape of startup operating outcomes, survival statuses, and sector classifications.
- **Counts:** 66,368 rows, 14 columns.
- **Licence as stated:** Not stated (Kaggle)
- **Requirement served:** R4 readiness proxies
- **Tech filter:** Category-list tech filter yields 28,695 tech rows (45.4% of rows with a category); status inside tech: operating 23,211, acquired 2,834, closed 2,221, ipo 429.
- **Limitations:** Impossible founded_at dates (1015 to 2914) requiring filtering to 1990-2015 before time features; global rather than Pakistani startups; licence not stated.
- **Description:**
  (1) Crunchbase startup outcomes dataset uploaded to Kaggle by Yan Maksi.
  (2) Used for requirement R4 readiness proxies and schema proxy for startup operating status and milestone fields.
  (3) Chosen as the closest public shape of startup operating outcomes and survival statuses.
  (4) Global data rather than Pakistan-specific, with extreme outlier dates (1015 to 2914) requiring 1990-2015 filtering.

#### StartUp Investments (Crunchbase)

- **Status:** FINAL
- **Reason:** Adds granular round-level funding columns, investment amounts, and investor stage categories.
- **Counts:** 54,294 raw rows, 39 columns; 4,856 blank rows, 49,438 usable rows, 0 duplicates on usable rows (earlier 4,855 duplicates were blank rows).
- **Licence as stated:** Not stated (Kaggle)
- **Requirement served:** R4 readiness proxies
- **Tech filter:** Category-list tech filter yields 20,542 tech rows (45.2% of rows with a category).
- **Limitations:** 4,856 blank rows; impossible date outliers (as early as year 0001); funding_total_usd missing for ~24.7% of rows; global coverage.
- **Description:**
  (1) Crunchbase funding rounds dataset uploaded to Kaggle by Arindam Banerji.
  (2) Used for requirement R4 readiness proxies and schema proxy for startup funding rounds and investment stages.
  (3) Chosen for its granular round-level funding columns and investor stage categories.
  (4) Contains 4,856 blank rows, uncleaned dates reaching year 0001, and missing funding values.

#### Resume Dataset (snehaanbhawal)

- **Status:** FINAL
- **Reason:** Public CC0 parsed multi-category CVs with clean text extracts across structured technical roles.
- **Counts:** 2,484 rows locally (the Kaggle card says 2,485 files), 4 columns (ID, Resume_str, Resume_html, Category), 24 categories; Information-Technology 120, Engineering 118.
- **Licence as stated:** CC0 (Kaggle)
- **Requirement served:** R1 resume optimizer inputs (IT slice)
- **Tech filter:** Information-Technology (120) and Engineering (118) categories; CSV text used only.
- **Limitations:** Scraped from LiveCareer examples; international English formatting rather than Pakistani conventions; use CSV text only (PDFs counted, never opened).
- **Description:**
  (1) Resume dataset scraped from LiveCareer examples and published on Kaggle by Snehaan Bhawal under CC0.
  (2) Used for requirement R1 resume optimizer inputs using the Information-Technology (120) and Engineering (118) slices.
  (3) Chosen for public CC0 licensing and clean text extracts across structured professional categories.
  (4) Examples reflect international templates rather than Pakistani resume conventions; PDFs remain unopened.

#### Resume Dataset (haider)

- **Status:** FINAL
- **Reason:** High volume of technical developer and system administrator resume texts for skills extraction.
- **Counts:** 9,000 rows (9 categories x 1,000), columns category, job_title, Text; tech categories have 6,000 rows, 4,170 unique texts, 30.5% duplicates; median text 11,168 characters.
- **Licence as stated:** CC BY-NC-SA 4.0 (Kaggle)
- **Requirement served:** R1 resume optimizer inputs
- **Tech filter:** 6 tech categories (Java Developers, Web Developer, SQL Developers, Network and Systems Administrators, Datawarehousing/ETL, Business Intelligence); 3 excluded (Business Analyst, Project Manager, Recruiter); unique texts only.
- **Limitations:** Provenance unclear (sourced only from "publicly accessible sources"); non-commercial licence; 30.5% duplicate text rate; non-Pakistani origin.
- **Description:**
  (1) Dataset of 9,000 resumes across nine job categories published on Kaggle by Haider Maseeh under CC BY-NC-SA 4.0.
  (2) Used for requirement R1 resume optimizer inputs for skills extraction and technical resume structure.
  (3) Chosen for high volume of long-form developer and administrator resume texts.
  (4) Unnamed provenance, non-commercial licence restriction, and 30.5% text duplication in tech categories.

---

### REFERENCE ONLY

#### LinkedIn-Dataset (Ayoobi et al.)

- **Status:** REFERENCE ONLY
- **Reason:** Reference for how profile structures differ between legitimate, fake, and AI-generated profiles.
- **Counts:** 3,600 profiles x 39 columns (pickle). Labels: 0 legitimate 1,800; 1 fake 600; 10 ChatGPT-generated 600; 11 ChatGPT-generated 600.
- **Licence as stated:** Research use only (stated in README; no LICENSE file)
- **Requirement served:** R3 startup discovery / R4 readiness proxies (profile verification structure reference)
- **Tech filter:** Intro column tech keyword match 661 rows (18.4%, informational only; no filtering applied).
- **Limitations:** No Pakistani profiles; research only restriction; Full Name column present (never accessed or stored); aggregate structure reference only.
- **Description:**
  (1) Synthetic and authentic LinkedIn profile dataset created by Ayoobi, Shahriar, and Mukherjee (HT 2023).
  (2) Used for requirement R4 readiness proxies and profile verification as an aggregate structure reference only.
  (3) Chosen as the only benchmark analyzing structural differences between legitimate, fake, and LLM-generated profiles.
  (4) Contains no Pakistani profiles, includes PII fields that must remain unread, and is restricted to research use.

#### ATS Dataset (NLP+ML)

- **Status:** REFERENCE ONLY
- **Reason:** Synthetic smoke test; never training or accuracy claims.
- **Counts:** 6,000 rows, 17 columns, 0 duplicates; six job roles, all tech; resume_text median 377 characters, job_description median 131 characters.
- **Licence as stated:** Not stated (Kaggle)
- **Requirement served:** R1 resume optimizer inputs / R2 matching (synthetic smoke test)
- **Tech filter:** All six job roles are technical.
- **Limitations:** Highly uniform distributions and short text lengths consistent with synthetic generation; synthetic smoke test; never training or accuracy claims.
- **Description:**
  (1) Resume screening dataset uploaded to Kaggle by Amay Mishra containing 6,000 paired records.
  (2) Used for requirements R1 and R2 strictly as a synthetic smoke test; never training or accuracy claims.
  (3) Chosen to test parser resilience on structured tabular fields without exposing real candidate data.
  (4) Texts are abnormally short and uniform, consistent with synthetic data generation.

#### IterateCV (abhaykanjoor/iteratecv-resume-tailoring)

- **Status:** REFERENCE ONLY
- **Reason:** Negative control to detect and audit LLM hallucination and fabrication patterns in tailored resume outputs.
- **Counts:** 600 rows (480 train / 60 dev / 60 test). Built from cnamuangtoun/resume-job-description-fit with GPT-4o mini tailored outputs.
- **Licence as stated:** MIT (Hugging Face)
- **Requirement served:** R1 resume optimizer inputs (negative control for fabrication audit)
- **Tech filter:** 100% tech share under loose keyword matching was likely caused by short tokens such as 'it' and 'ai'; the strict-matcher rerun on IterateCV did not complete.
- **Limitations:** Generated with GPT-4o mini; fabrication step crashed in fixed run; never training or evaluation data.
- **Description:**
  (1) Resume tailoring dataset published on Hugging Face by user abhaykanjoor for the IterateCV project, using GPT-4o mini adaptations under MIT licence.
  (2) Used for requirement R1 resume optimizer inputs strictly as a negative control for detecting AI fabrication.
  (3) Chosen because it explicitly captures LLM-generated modifications between original and tailored resumes.
  (4) Model outputs contain synthetic artifacts and it must never be used for training or positive evaluation.

#### Mavkif/roman-urdu-msmarco-dataset

- **Status:** REFERENCE ONLY
- **Reason:** Large Roman Urdu retrieval corpus (MS MARCO translated into Urdu, then transliterated into Roman Urdu) for exploratory retrieval benchmarking in FYP-2.
- **Counts:** Paper evaluates 6,980 queries (BM25 MRR@10 0.0846; fine-tuned mT5 reranker 0.1903); its Urdu translation has over 8.8 million passages. Local files: collection TSV 2,976.9 MB, train queries 37.8 MB, dev.small queries 0.3 MB.
- **Licence as stated:** Not stated (the paper states none; the repository has no README or licence file)
- **Requirement served:** R5 multilingual benchmark (FYP-2 retrieval reference)
- **Tech filter:** None (general search queries)
- **Limitations:** Two machine steps (IndicTrans2 translation into Urdu, then a fine-tuned m2m100 transliteration into Roman Urdu), and the paper attributes its lower Roman Urdu scores to transliteration noise; no local relevance labels; script-share values were not printed in the fixed run.
- **Description:**
  (1) Roman Urdu version of MS MARCO described by Butt, Varanasi and Neumann (LowResNLP 2025) and hosted by Mavkif on Hugging Face.
  (2) Used for requirement R5 as an exploratory reference for Roman Urdu information retrieval in FYP-2.
  (3) Chosen for its sheer volume of transliterated queries and passages mapped from a standard IR benchmark.
  (4) Two machine steps add noise, local relevance labels are absent, and no licence is stated.

#### roman-urdu-retrieval-queries

- **Status:** REFERENCE ONLY
- **Reason:** Structured multi-script retrieval queries (Urdu script, English, Roman Urdu) for IR pipeline harness calibration in FYP-2.
- **Counts:** 300 queries (100 dev, 200 test), 3,674 passages (1,674 Urdu, 2,000 English); author reports bge-m3 Recall@5 99.0% on Urdu script and 40.0% on Roman Urdu.
- **Licence as stated:** Queries CC BY 4.0, corpus CC BY-SA 4.0 (Wikipedia)
- **Requirement served:** R5 multilingual benchmark (FYP-2 harness calibration)
- **Tech filter:** None (Wikipedia knowledge domain)
- **Limitations:** Questions and Roman Urdu spellings generated by GPT-4o without native-speaker validation; general domain; harness calibration only.
- **Description:**
  (1) Multi-script retrieval dataset published on Hugging Face by user masoodd with Wikipedia corpus passages.
  (2) Used for requirement R5 multilingual benchmark for calibrating cross-script retrieval evaluation harnesses in FYP-2.
  (3) Chosen for aligned query variations across Urdu script, English, and three Roman Urdu spelling styles.
  (4) Transliterations were generated by GPT-4o rather than validated by native Pakistani speakers.

#### hassan7272/urdu-finance-qa

- **Status:** REFERENCE ONLY
- **Reason:** Informal reference for Pakistani financial vocabulary, phrasing, and question styles.
- **Counts:** 1,510 rows (JSON array); question_ur Arabic script share 32.9% with embedded English; answer median length 352 characters.
- **Licence as stated:** CC BY 4.0 stated by author
- **Requirement served:** Compliance Q&A assistant (question-style reference only)
- **Tech filter:** None applied (finance domain). Separate measure: 19.34% of rows name SBP, SECP or FBR.
- **Limitations:** Every viewed row has source = synthetic; consumer and Islamic finance rather than startup corporate regulation; answers are unverified and never ground truth.
- **Description:**
  (1) Financial QA dataset generated by Muhammad Hassan Shahbaz on Hugging Face as part of the FinGuard project.
  (2) Used for compliance assistant design as an informal reference for Urdu financial phrasing and question styles.
  (3) Chosen as one of the few public QA sets mentioning Pakistani financial institutions like SBP and FBR.
  (4) Answers are synthetic and unverified; the compliance assistant relies exclusively on official corpus documents.

#### Pakistan Job Market Dataset (Rozee.pk) 2024

- **Status:** REFERENCE ONLY
- **Reason:** Supplementary reference for contemporary Pakistani job listings, salary bands, and active hiring windows.
- **Counts:** 1,034 usable rows, 12 columns (Gender and Age excluded); Apply Before 2024-12-11 to 2025-03-14.
- **Licence as stated:** Apache 2.0 (Kaggle)
- **Requirement served:** R2 matching and job board (supplementary modern reference)
- **Tech filter:** Strict tech title share at least 8.41%.
- **Limitations:** Contains no job description text; small sample size (1,034 rows); gender and age columns excluded.
- **Description:**
  (1) Scraped job postings from Rozee.pk published on Kaggle by Syeda Zainish Fatima and Syed Wajdan Zeerak under Apache 2.0.
  (2) Used for requirement R2 matching and job board as a supplementary reference for contemporary Pakistani job listings.
  (3) Chosen for its recent 2024-2025 collection timeframe and explicit Pakistani city locations.
  (4) Lacks full job description text and contains non-merit fields (gender, age) that are strictly excluded.

#### linkedin-fake-profiles-gpt4turbo-gulati (Gulati et al.)

- **Status:** REFERENCE ONLY
- **Reason:** Companion data of the paper we cite on LLM-generated fake profiles; used only to understand how GPT-4 Turbo profiles differ from legitimate ones.
- **Counts (from the repository README, not yet profiled locally):** `cleaned_profiles.csv` 3,600 profiles (1,800 legitimate, 600 manually created fake, 1,200 GPT-3.5 generated); `generated_profiles_NEW.csv` 600 GPT-4 Turbo profiles. The README lists no columns and no labels for the second file. Local row and column counts to be added after profiling.
- **Licence as stated:** Not stated (repository README has no licence and no data-use terms)
- **Requirement served:** R4 readiness proxies (profile verification structure reference)
- **Tech filter:** None applied
- **Limitations:** No licence; the README does not say whether the legitimate profiles are real people's data or how they were anonymised, so treat all rows as possibly personal and never read or store individual profile text; no Pakistani profiles stated; `cleaned_profiles.csv` has the same size and label split as the LinkedIn-Dataset (Ayoobi et al.) and may overlap it (not checked); GPT-4 Turbo profiles come from few-shot prompts modelled on two legitimate examples; aggregate structure reference only.
- **Description:**
  (1) Data released with "Weak Links in LinkedIn: Enhancing Fake Profile Detection in the Age of LLMs" by Gulati, Kumar, Agarwal and Sharma (repository apoorva106/linkedin_fake_profile_detection on GitHub).
  (2) Used for requirement R4 readiness proxies and profile verification as an aggregate structure reference only.
  (3) Chosen because it is the only public set that adds GPT-4 Turbo generated profiles to the legitimate, fake and GPT-3.5 groups.
  (4) No licence is stated, personal-data status of the legitimate profiles is unknown, and it may overlap the LinkedIn-Dataset above.

---

### DROPPED

#### hafiz-hassaan-saeed Parallel Urdu-Roman Urdu Corpus

- **Status:** DROPPED
- **Reason:** 18.0% toxic content rate, high profanity, unvetted web-scraped social text, no author documentation.
- **Counts:** 72,771 rows.
- **Licence as stated:** Unstated / empty card metadata
- **Requirement served:** None (dropped from R5)
- **Tech filter:** None
- **Limitations:** High toxicity and vulgarity make it unacceptable for platform language representation.
- **Description:**
  (1) Parallel Urdu and Roman Urdu text collection uploaded to Hugging Face by Hafiz Hassaan Saeed.
  (2) Dropped from project requirements and evaluated as unfit for platform language representations.
  (3) Evaluated as a potential parallel text source before finding Roman-Urdu-Parl split.
  (4) Suffers from an 18.0% toxic content rate, high profanity, and an empty dataset card.

#### Khubaib01 RUEmoCorp

- **Status:** DROPPED
- **Reason:** Has labels; reason = no emotion feature in the project, and some person names remain in rows.
- **Counts:** 28,000 annotated plus 134,053 model-labelled (Hub lists 162,055 rows across both subsets).
- **Licence as stated:** Licence shown as CC BY 4.0 in metadata and Apache 2.0 in text.
- **Requirement served:** None (dropped)
- **Tech filter:** None
- **Limitations:** No emotion feature in the project, and some person names remain in rows.
- **Description:**
  (1) Roman Urdu emotion corpus uploaded to Hugging Face by Khubaib01 (28,000 annotated plus 134,053 model-labelled).
  (2) Dropped from project requirements as the project contains no emotion feature.
  (3) Screened as a potential resource for emotional tone analysis.
  (4) Has labels, but no emotion feature in the project, and some person names remain in rows.

#### Inferencelab RomanUrdu-NLP-Sentiment-Corpus

- **Status:** DROPPED
- **Reason:** Has labels; reason = no sentiment feature in the project, and some person names remain in rows.
- **Counts:** 134,052 rows.
- **Licence as stated:** Unstated (Hugging Face)
- **Requirement served:** None (dropped)
- **Tech filter:** None
- **Limitations:** No sentiment feature in the project, and some person names remain in rows.
- **Description:**
  (1) Roman Urdu social media dataset uploaded to Hugging Face by InferenceLab containing 134,052 rows.
  (2) Dropped from project requirements as the project contains no sentiment feature.
  (3) Screened as a candidate for understanding Roman Urdu sentiment in community reviews.
  (4) Has labels, but no sentiment feature in the project, and some person names remain in rows.

#### abdullaharoon/Urdu-Multi-Domain-Benchmark

- **Status:** DROPPED
- **Reason:** 26 sub-datasets with conflicting individual licences; four domains require rebuild scripts; offensive content present; cite the paper only.
- **Counts:** 130,872 rows.
- **Licence as stated:** Per-domain licences (each domain keeps its source licence); the authors' own contributions are CC BY-NC 4.0 per Zenodo; doi 10.5281/zenodo.23053495
- **Requirement served:** None (dropped; cite paper only)
- **Tech filter:** None
- **Limitations:** Fragmented licensing, rebuild requirements, and offensive content across uncurated domains.
- **Description:**
  (1) Multi-domain Urdu benchmark published on Hugging Face and Zenodo by Muhammad Abdullah Haroon and Maryam Bashir (FAST-NUCES Lahore), version 1.1, September 2026.
  (2) Dropped from project requirements; cited strictly as academic background literature.
  (3) Evaluated as a potential multi-domain evaluation benchmark for Urdu understanding.
  (4) Complex multi-licence fragmentation, executable rebuild scripts, and offensive text instances.

---

### EXCLUDED EARLIER

#### Resume-Job Matching (HSE hackathon)

- **Status:** EXCLUDED EARLIER
- **Reason:** Russian-language text; heavy domain and geographical mismatch with Pakistani startup ecosystem.
- **Counts:** 150,493 pairs (65,714 resumes, 43,756 vacancies); 86.1% rejected, 13.9% invited.
- **Licence as stated:** Not stated (Kaggle)
- **Requirement served:** None (excluded)
- **Tech filter:** None
- **Limitations:** Non-English, non-Urdu (Russian language only) with geographic mismatch.
- **Description:**
  (1) Russian resume-vacancy invitation dataset from an HSE hackathon uploaded to Kaggle by Daria Shataeva.
  (2) Excluded earlier from all requirements due to complete language and geographic divergence.
  (3) Initially inspected as a large-scale public baseline of resume-to-job pairing decisions.
  (4) Written entirely in Russian with 86.1% rejection skew and severe domain mismatch.

#### Resume Dataset PDF

- **Status:** EXCLUDED EARLIER
- **Reason:** 0 of 30 sampled files had text.
- **Counts:** 8,905 PDF files (0 of 30 sampled had text).
- **Licence as stated:** Not stated (Kaggle)
- **Requirement served:** None (excluded)
- **Tech filter:** None
- **Limitations:** 0 of 30 sampled files had text; image-only scans with no text layer.
- **Description:**
  (1) Collection of 8,905 PDF resume files uploaded to Kaggle by Hadi KP.
  (2) Excluded earlier from R1 resume optimizer testing due to lack of extractable text.
  (3) Profiled as potential raw PDF inputs for resume parsing and text extraction testing.
  (4) 0 of 30 sampled files had text; image-only scans with no text layer.

#### Maaz Urdu to Roman Urdu

- **Status:** EXCLUDED EARLIER
- **Reason:** No licence listed, partly AI-generated, skipped by the team.
- **Counts:** 4,860 pairs.
- **Licence as stated:** No licence listed.
- **Requirement served:** None (excluded)
- **Tech filter:** None
- **Limitations:** No licence listed, partly AI-generated, skipped by the team.
- **Description:**
  (1) Urdu to Roman Urdu translation dataset of 4,860 pairs uploaded to Hugging Face by user Maaz-x14.
  (2) Excluded earlier from multilingual language representation requirements.
  (3) Evaluated briefly as a parallel transliteration alternative before Roman-Urdu-Parl split.
  (4) No licence listed, partly AI-generated, skipped by the team.

#### Rankistan and awesome-pakistani

- **Status:** EXCLUDED EARLIER
- **Reason:** Named personal profiles and GitHub-versus-LinkedIn source leakage.
- **Counts:** Rankistan: leaderboard capped at 1,000 (about 34,854 candidate accounts searched on 2026-10-13 per its README); awesome-pakistani: 58 public profiles (51 developers, 6 organisations, 1 community; last updated 2026-08-06).
- **Licence as stated:** Rankistan: MIT (code only); awesome-pakistani: MIT.
- **Requirement served:** None (excluded)
- **Tech filter:** None
- **Limitations:** Named personal profiles and GitHub-versus-LinkedIn source leakage.
- **Description:**
  (1) GitHub developer profile lists: Rankistan (user sudo-ali-dev, MIT code only) and awesome-pakistani (user usman2x, MIT).
  (2) Excluded earlier from candidate profile indexing to prevent unconsented personal data exposure.
  (3) Explored as candidate sources for Pakistani developer skills and profile benchmarking.
  (4) Named personal profiles and GitHub-versus-LinkedIn source leakage.

#### Pakistani Startups Hub

- **Status:** EXCLUDED EARLIER
- **Reason:** Self-described demo build with composite quotes.
- **Counts:** Header counts conflict (2,220 companies and 218 investors versus 100 and 15 shown).
- **Licence as stated:** No reuse terms seen.
- **Requirement served:** None (excluded)
- **Tech filter:** None
- **Limitations:** Self-described demo build with composite quotes; header counts conflict (2,220 companies and 218 investors versus 100 and 15 shown).
- **Description:**
  (1) Directory listing of Pakistani startups compiled as a demonstration portal.
  (2) Excluded earlier from R3 startup discovery due to synthetic placeholder content.
  (3) Examined as a potential supplementary directory of local Pakistani startups.
  (4) Self-described demo build with composite quotes; header counts conflict (2,220 companies and 218 investors versus 100 and 15 shown).

#### ERUPD (arXiv 2412.17562)

- **Status:** EXCLUDED EARLIER
- **Reason:** 75,146 sentence pairs per the paper; no data release or licence seen.
- **Counts:** 75,146 sentence pairs per the paper.
- **Licence as stated:** No data release or licence seen.
- **Requirement served:** None (excluded; do not cite for data)
- **Tech filter:** None
- **Limitations:** 75,146 sentence pairs per the paper; no data release or licence seen; unverified participant consent (the abstract says part of the data comes from personal messaging groups).
- **Description:**
  (1) English-Roman Urdu translation dataset (75,146 pairs per paper) from arXiv preprint 2412.17562 by Furqan, Khaja and Habeeb (Hyderabad, India).
  (2) Excluded from project data pipelines because no data release or licence was seen.
  (3) Reviewed in literature for state-of-the-art Roman Urdu translation architectures.
  (4) 75,146 sentence pairs per the paper; no data release or licence seen; unverified participant consent.
