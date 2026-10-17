# Requirements

Source: report Chapter 4 (Functional Requirements, Non-Functional Requirements, Risk Analysis). IDs are stable and never renumbered, so they are not contiguous inside their groups. Cite them in code comments, tests, and pull requests.

31 functional requirements: 25 in FYP-1 only, 4 in FYP-2 only (FR-9, FR-11, FR-30, FR-31), 2 split (FR-7 and FR-13: basic version in FYP-1, trained re-ranker in FYP-2).

## Functional requirements

### Accounts and access
| ID | Requirement | Sem |
| --- | --- | --- |
| FR-17 | Users accept a consent notice and a trust note on hybrid verification before submitting profile data | 1 |
| FR-22 | Register with email and password or LinkedIn, pick one role | 1 |
| FR-23 | Signed token at login, per-role endpoint limits, session ends at logout | 1 |
| FR-27 | Review or withdraw consent for non-essential processing; request account deletion | 1 |

### Founder services and compliance
| ID | Requirement | Sem |
| --- | --- | --- |
| FR-1 | Founders create a profile and submit traction and business data | 1 |
| FR-2 | AI mentor feedback and a readiness score per dimension | 1 |
| FR-3 | Multi-turn investor pitch simulation scoring clarity, confidence, content | 1 |
| FR-4 | Competitor and market size summary from live web search, evidence apart from interpretation | 1 |
| FR-28 | Founders view pitch history with scores | 1 |
| FR-8 | Compliance answers from SECP, FBR, PSEB documents with dated citations, or "no supported answer" | 1 |

### Job board and talent
| ID | Requirement | Sem |
| --- | --- | --- |
| FR-5 | Talent uploads a CV and gets suggested edits | 1 |
| FR-6 | List startup jobs and internships | 1 |
| FR-24 | Verified founders publish, edit, close, delete listings and view applications | 1 |
| FR-25 | Talent saves a listing, applies, tracks status | 1 |

### Matching and discovery
| ID | Requirement | Sem |
| --- | --- | --- |
| FR-7 | Match founders with mentors and investors, talent with mentors and founders; contact only after both accept | 1 and 2 |
| FR-10 | Investors see only verified startups with a completed readiness assessment | 1 |
| FR-13 | Talent links a public GitHub profile; repo count, commit recency, language mix feed the re-ranker | 1 and 2 |
| FR-29 | Mentors mark themselves open or closed; closed mentors are left out of matches | 1 |

### Profile verification and administration
| ID | Requirement | Sem |
| --- | --- | --- |
| FR-12 | Mentor and investor profiles become verified and visible after LinkedIn OAuth or SECP cross-check | 1 |
| FR-14 | High score verifies at once, low score rejects with logged reason, middle goes to human review | 1 |
| FR-19 | Score each profile from collected signals; log score, signal values, band | 1 |
| FR-20 | Check a portfolio or product link loads real content matching the profile: consistent, inconsistent, insufficient | 1 |
| FR-15 | Users see profile status (auto-verified, auto-rejected, pending review, appeal pending, verified, rejected) and reason | 1 |
| FR-16 | Reported or blocked profiles go back to human review and are not re-scored | 1 |
| FR-21 | An auto-rejected user may appeal once with added evidence; reviewer decision is final and visible | 1 |
| FR-26 | Console shows escalated profiles and appeals with signals and score; records each decision and reason against the reviewer | 1 |

### Platform and ecosystem
| ID | Requirement | Sem |
| --- | --- | --- |
| FR-18 | Team-written usage guides reachable from every dashboard | 1 |
| FR-9 | English, Urdu, Roman Urdu in conversation, benchmarked per language | 2 |
| FR-11 | Startups pay a placement fee only when startup and candidate both confirm a hire; one-sided confirmation goes to a reviewer (billing is mocked) | 2 |
| FR-30 | List startup events run by others, with organizer and source link | 2 |
| FR-31 | Reviewed external resource links, attributed to original publishers | 2 |

## Non-functional requirements

| ID | Requirement |
| --- | --- |
| NFR-1 | 50 concurrent logged-in users without visible slowdown |
| NFR-2 | LLM request returns in about 8 seconds; free tier allows about 5 at once, the rest queue |
| NFR-3 | Match query returns ranked results in about 2 seconds on the seeded demo dataset |
| NFR-4 | Passwords stored only as salted hashes, never in logs or errors |
| NFR-5 | Every endpoint except registration, login, and public pages needs a valid token and is limited to the caller's role |
| NFR-6 | No API response shows another user's contact details before both sides accept |
| NFR-7 | Uploaded files checked for type and size, stored outside the served directory |
| NFR-8 | Credentials and API keys come from environment configuration, not the repository |
| NFR-9 | Personal data only through opt-in registration or linked accounts, after the FR-17 consent notice |
| NFR-10 | Deletion request disables the account at once and removes personal data within 30 days |
| NFR-11 | Pitch transcripts, compliance query logs, verification records kept only until the account is deleted |
| NFR-12 | Every compliance answer cites source passages with document title and effective date |
| NFR-13 | No supporting passage, or failed validation: say there is no grounded answer |
| NFR-14 | An answer quoting a fee or tax rate states the effective date of its source |
| NFR-15 | Readiness scores store reasoning, match results store factors, so explanations need no new model call |
| NFR-16 | A first-time user can submit a profile, get feedback, and request a match unaided |
| NFR-17 | Body text meets 4.5:1 contrast in light and dark themes (WCAG 2.1 AA) |
| NFR-18 | Layout uses CSS logical properties so right-to-left Urdu can be added in FYP-2 |
| NFR-19 | LLM calls go through one internal gateway; changing provider or tier is a configuration change |
| NFR-20 | Matching and retrieval use the same embedding pipeline and vector store |
| NFR-21 | API layer keeps no session state; matching and retrieval run as separate services |
| NFR-22 | Every schema change is a versioned migration; schema rebuilds from history on an empty database |
| NFR-23 | Linting and tests run on every pull request; a failing run blocks the merge |

## Risks worth remembering while coding

- R-1 (High): too few labeled pairs for the re-ranker. Fallback is a pilot result against the baseline.
- R-2, R-3: unsupported or outdated compliance answers. Cite and date every answer. Abstain when unsure.
- R-4: answers read as legal or tax advice. Never say whether a license applies to a case.
- R-5: free-tier LLM limits. Queue and keep provider in config.
- R-7: fake profiles. Claim only that rules raise the cost of casual fakery; doubtful profiles go to a reviewer.
- R-9 (High): Roman Urdu has no standard spelling. Benchmark first. FYP-1 is English only.
- R-10: no training data from scraping. Ever.
- R-15: fee model not legally reviewed. Claim no compliance.

Full list is R-1 to R-19 in the report.
