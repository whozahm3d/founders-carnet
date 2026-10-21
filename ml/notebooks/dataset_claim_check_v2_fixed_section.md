# Dataset Claim Checks V2 - Bug-Fixed Section

**Run Timestamp**: 2026-10-18 16:13:26

## Summary of Fixed Sections

| Section | Target Dataset / Step | Status |
|---|---|---|
| S1 | Fixed Section | OK |
| S10 | Fixed Section | OK |
| S11 | Fixed Section | OK |
| S12 | Fixed Section | OK |
| S14 | Fixed Section | OK |
| S2 | Fixed Section | OK |
| S3 | Fixed Section | OK |
| S4 | Fixed Section | OK |
| S5 | Fixed Section | OK |
| S6 | Fixed Section | OK |
| S7 | Fixed Section | OK |
| S8 | Fixed Section | OK |
| S9 | Fixed Section | OK |
| Step 3 | Fixed Section | OK |
| Step 4 | Fixed Section | OK |

## Detailed Checks and Numeric Assertions

| Dataset | Claim | Operator | Threshold | Actual | Result |
|---|---|---|---|---|---|
| roman_urdu_parl_split_dataset | Validation rows | == | 20719 | 20719 | PASS |
| roman_urdu_parl_split_dataset | Test rows | == | 20741 | 20741 | PASS |
| roman_urdu_parl_split_dataset | Urdu column Arabic script share | >= | 80.0 | 76.8 | FAIL |
| roman_urdu_parl_split_dataset | Roman-Urdu Latin script share | >= | 70.0 | 80.23 | PASS |
| roman_urdu_parl_split_dataset | Pair-level overlap with val/test | <= | 50 | 0 | PASS |
| LinkedIn-Dataset-main | Physical rows | == | 3600 | 3600 | PASS |
| LinkedIn-Dataset-main | Column count | == | 39 | 39 | PASS |
| LinkedIn-Dataset-main | Max column missing rate | <= | 100.0 | 31.36 | PASS |
| Startup SuccessFail Dataset from Crunchbase | Non-blank rows count | >= | 500 | 66368 | PASS |
| Startup SuccessFail Dataset from Crunchbase | Strict tech share % | >= | 15.0 | 23.0 | PASS |
| StartUp Investments (Crunchbase) | Non-blank rows | == | 49438 | 49438 | PASS |
| StartUp Investments (Crunchbase) | Duplicates on non-blank rows | <= | 10 | 0 | PASS |
| StartUp Investments (Crunchbase) | Strict tech share % | >= | 15.0 | 23.53 | PASS |
| StartUp Investments (Crunchbase) | Positive funding share % | >= | 50.0 | 82.74 | PASS |
| How Companies Screen Resumes ATS Dataset (NLP+ML) | Non-blank rows count | >= | 500 | 6000 | PASS |
| How Companies Screen Resumes ATS Dataset (NLP+ML) | Strict tech share % | >= | 15.0 | 100.0 | PASS |
| How Companies Screen Resumes ATS Dataset (NLP+ML) | Median text chars (main text only) | >= | 100 | 5.0 | FAIL |
| Pakistan Startup Census | Physical rows | == | 553 | 553 | PASS |
| Pakistan Startup Census | All-NaN rows | == | 120 | 120 | PASS |
| Pakistan Startup Census | Non-blank rows count | == | 433 | 433 | PASS |
| Pakistan Startup Census | Duplicate startup names on non-blank | <= | 5 | 1 | PASS |
| Pakistan Startup Census | Tech share % | >= | 15.0 | 11.78 | FAIL |
| Pakistan's Job Market | Explicit title != company mapping | == | 1 | 1 | PASS |
| Pakistan's Job Market | JD text cut at 250 characters | == | 250 | p95=250.0, max=250 | INFO |
| Pakistan's Job Market | Triplet duplicates % | <= | 20.0 | 19.64 | PASS |
| Pakistan's Job Market | Strict tech share % | >= | 15.0 | 26.8 | PASS |
| Pakistan Job Market Dataset (Rozee.pk) | Column count | == | 12 | 12 | PASS |
| Pakistan Job Market Dataset (Rozee.pk) | Non-blank rows count | >= | 500 | 1034 | PASS |
| Pakistan Job Market Dataset (Rozee.pk) | Strict tech share % | >= | 15.0 | 8.41 | FAIL |
| Resume Dataset | Physical rows | == | 2484 | 2484 | PASS |
| Resume Dataset | Category count | == | 24 | 24 | PASS |
| Resume Dataset | IT category rows | == | 120 | 120 | PASS |
| Resume Dataset | Engineering category rows | == | 118 | 118 | PASS |
| Resume Dataset | PDF files count | == | 2484 | 2484 | PASS |
| resume_dataset_by_haider_maseeh | Total rows (9 cats) | == | 9000 | 9000 | PASS |
| resume_dataset_by_haider_maseeh | Tech rows (6 cats) | == | 6000 | 6000 | PASS |
| resume_dataset_by_haider_maseeh | Excluded rows (3 cats) | == | 3000 | 3000 | PASS |
| resume_dataset_by_haider_maseeh | Tech unique texts count | == | 4170 | 4170 | PASS |
| resume_dataset_by_haider_maseeh | Tech duplicate % | <= | 35.0 | 30.5 | PASS |
| roman-urdu-retrieval-queries | Urdu passages count | == | 1674 | 1674 | PASS |
| roman-urdu-retrieval-queries | Test queries count | == | 200 | 200 | PASS |
| hassan7272urdu-finance-qa | QA pairs count | == | 1510 | 1510 | PASS |
| hassan7272urdu-finance-qa | Question Arabic script % | >= | 80.0 | 32.9 | FAIL |
| hassan7272urdu-finance-qa | Answer Arabic script % | >= | 80.0 | 36.9 | FAIL |
| hassan7272urdu-finance-qa | Regulatory keywords share % | >= | 20.0 | 55.83 | PASS |
| hassan7272urdu-finance-qa | Answer median length | >= | 100 | 352.0 | PASS |
| hassan7272urdu-finance-qa | Duplicate questions count | <= | 10 | 3 | PASS |
| hassan7272urdu-finance-qa | Answers naming regulatory authorities % | >= | 10.0 | 19.34 | PASS |
| iteratecv-resume-tailoring | Strict tech share % | <= | 95.0 | 85.0 | PASS |
| Step 3 | Tech Resumes Pool | >= | 1000 | 6238 | PASS |
| Step 3 | Tech Jobs Pool | >= | 500 | 1877 | PASS |
| Step 3 | Pair Cross Product | >= | 500000 | 11708726 | PASS |

## Regression Table

| Bug ID | Bug Description | Verification Check | Status |
|---|---|---|---|
| 1 | Regex \\u escape sequence error | Plain Python code points in script_share helper | PASS |
| 2 | String threshold comparisons ('<=20.0%') | v2_check_num parses numbers as float | PASS |
| 3 | Parl val/test rows (16,219 vs 20,719) | Combined small+main CSVs; audit matches physical lines | PASS |
| 4 | LinkedIn opcode false positives ('Connections') | SafeRestrictedUnpickler loads (3600, 39) cleanly | PASS |
| 5 | Blank rows & float iteration error | drop_blank_rows isolates 120 blank rows (433 valid) | PASS |
| 6 | Job Market column mapping & series alignment | Explicit title='Job Name', assert != company, reset_index | PASS |
| 7 | Resume Dataset index out of bounds | Recursive CSV locator, 24 categories, guarded sample | PASS |
| 8 | Loose tech matcher false positives | Single compiled strict regex with word boundaries | PASS |
| 9 | Haider resumes categories | TECH_RESUME_CATEGORIES (6 cats) vs 3 excluded reported | PASS |
| 10 | Dynamic Scorecard derivation | Recomputed from run metrics and TEAM_DECISIONS dict | PASS |
| 11 | Retrieval baseline & Finance QA metrics | 1,674 passages, 200 queries, SBP/SECP/FBR mentions | PASS |