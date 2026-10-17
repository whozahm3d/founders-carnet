**The Founder's Carnet**

**AI-Native Startup Ecosystem Platform for Pakistan**

*Master Project Document — Merged Draft*

Ali Ahmad · Shahzeb Imran · Taha Nawaz
Department of Artificial Intelligence & Data Science, FAST NUCES, Lahore

*Final Project Proposal — Supervisor Confirmed*

---

## Project Brief (FAST-NUCES cover-page fields)

**FYP Type:** Development

**Brief Description:** An AI-native platform connecting Pakistani startup founders, startup-specific talent (job/internship seekers), mentors, and investors on one shared AI reasoning engine — readiness scoring, pitch practice, market research synthesis, resume/profile optimization, ecosystem matching via a trained re-ranking model, and a compliance RAG assistant grounded in SECP/FBR/PSEB sources.

**UN SDGs targeted:**
- **SDG 8 — Decent Work and Economic Growth:** a dedicated, curated pathway into startup employment and internships for job-seekers currently unserved by general job boards.
- **SDG 9 — Industry, Innovation and Infrastructure:** AI-native infrastructure supporting early-stage venture creation and founder-investor-mentor connectivity in Pakistan's startup ecosystem.
- **SDG 5 / SDG 10 — Gender Equality / Reduced Inequalities:** deliberate outreach to women-led founders and women in tech during anchor-partner recruitment (Section 8), addressing a documented ~1% women-led-business gap the government's own Ignite-backed WISE Lab initiative was created to address.

**Algorithms and knowledge used from Core Courses:**
- Artificial Intelligence / Machine Learning — embedding-based semantic matching, supervised ranking (re-ranker training), contrastive/triplet fine-tuning
- Natural Language Processing — retrieval-augmented generation, multilingual embeddings, prompt engineering
- Database Systems — relational schema design, pgvector similarity search
- Software Engineering — requirements engineering, modular service architecture, iterative development
- Web Technologies — REST API design, frontend/backend integration
- Information Security — authentication (JWT/OAuth), role-based access control, data privacy handling

**Group Members:** Ali Ahmad, Shahzeb Imran, Taha Nawaz

---

## Table of Contents

1. Executive Summary
   - 1.1 Why "The Founder's Carnet"
2. Problem Statement
   - 2.1 Objectives
3. Literature / Research Foundation
4. Competitive Analysis
5. Gap Analysis & Differentiation
6. Proposed Solution & Scope
   - 6.1 Phase 1 — Potential FYP
   - 6.2 Explicitly Out of Scope
   - 6.3 Constraints
7. Business Model & Monetization
   - 7.1 Business Opportunity
   - 7.2 If this becomes a real company after the FYP
8. Stakeholders Description
   - 8.1 Stakeholders Summary
   - 8.2 Key High-Level Goals and Problems of Stakeholders
9. Datasets
10. Project Pipeline & Workflow
11. System Architecture
12. Core AI Reasoning Engine — the shared pattern
13. Feature-by-Feature Deep Dive
14. Tech Stack
15. User Workflows
16. Requirements
    - 16.1 List of Features
    - 16.2 Functional Requirements
    - 16.3 Non-Functional Requirements
17. Evaluation Plan
18. Legal, Regulatory & Ethical Considerations
19. Risks & Limitations
20. Go-to-Market / Trust & Adoption Strategy
21. Research Questions
22. Timeline / Milestones
23. Phase 2 — Potential Business (expected steps if pursued beyond the FYP)
24. Conclusion
25. References
26. Appendix

---

# 1. Executive Summary

The Founder's Carnet is an AI-native platform connecting three groups underserved by Pakistan's existing startup infrastructure: early-stage founders, job- and internship-seekers who specifically want to work at startups, and the mentors and investors who support them — treated as distinct stakeholder types throughout this document (Section 8), not one merged role. The platform runs on one shared AI reasoning engine — not five disconnected AI features — applied consistently across founder mentorship, startup readiness scoring, pitch practice, market research synthesis, resume/profile optimization, and ecosystem matching.

Pakistan already has physical accelerators (NIC, Plan9, i2i, LUMS CFE), at least four directly-audited digital competitors or close analogs (InnoCollab.pk, PakStartups.org, PakLaunch, StartupNetwork.pk — Section 4.1), and a live founder–investor matchmaking platform in i2i's Investor Founder Discovery Platform (IFDP, Section 4.4), so this is not a claim to a new category. The contribution is integration, localization, and a defensible technical core: a trainable hybrid matching/re-ranking model (the project's primary machine-learning artifact), retrieval-augmented generation for compliance guidance, and consistent multilingual support across English, Urdu, and Roman Urdu — none of which any audited competitor currently does together.

The project is scoped to be legally uncomplicated by design: no equity is ever taken, no investment transaction is brokered on-platform, and no feature that amounts to running a licensed financial intermediary or physical accelerator is included. Monetization comes from subscriptions (talent, mentors, investors) and a cash placement fee (startups, only when they hire through the platform) — never from a cut of investment.

## 1.1 Why "The Founder's Carnet"

The name is meant to describe an actual mechanism in the system, not decorate it. Section 2 establishes the core problem: Pakistan's startup-support system is real but relationship-gated — who you know, who already vouches for you, who's already in the room. A founder outside that circle has no way to build a track record a stranger (an investor, a mentor, an employer) could trust without a personal introduction first.

A *carnet* is the precise word for the mechanism that solves that specific problem. Beyond its everyday sense of a small record booklet, a carnet is, concretely, an internationally recognized document — the ATA Carnet — that lets something cross a border and be trusted by a stranger (a customs official who has never seen it before) without needing a prior relationship or repeated re-verification each time. That is the actual claim this project is making about what it adds to Pakistan's startup ecosystem: not a new category, but a way for a founder's standing to cross the boundary between "unknown to this investor" and "trusted enough to talk to," without needing a personal introduction to make that crossing possible.

This is also literal, not just thematic — nearly everything that differentiates this platform from what's already out there (Section 5) is, mechanically, building or checking some part of that crossing:

- The **compliance assistant** never answers from memory; every answer retrieves and cites a specific source passage, so the answer is checkable, not just asserted (Section 13.6).
- The **matching engine** logs the structured features behind every match, so "why was I matched with this person" has a real, stored answer rather than an explanation invented after the fact (Section 13.5).
- The **profile verification process** — automated where the signals are clear, human where they're not — logs every decision with a reason, and grants the "Verified" badge that lets a profile cross from unseen to trusted — building an actual reviewable history instead of a silent, unexplained gate (Section 13.8).
- The **competitive analysis itself** is kept as a dated evidence log (Appendix A), because partway through building this document, an earlier claim about a competitor turned out to be stale — the fix was to start dating and re-verifying claims rather than asserting them once and leaving them.
- The **readiness score** is a dimension-by-dimension record of where a founder stands and what's missing, not a single opaque number — the specific content that gets checked at the crossing.

The name describes a discipline the project already had to learn the hard way during its own drafting, not an aspiration invented for branding. "Founder's" centers who it's for: the founder's own credential, built to earn trust with investors, mentors, and employers — visible and understandable to the founder, not a private judgment handed down at them. The same logic extends to talent (a checkable record of skills and activity that lets them cross into a startup's hiring pipeline) and to mentors and investors (a verified, reviewed standing that lets them cross into a founder's trust) — everyone on the platform is building something that can be checked at the boundary, not asking to be taken on faith.

# 2. Problem Statement

Pakistan's startup-support system is real but structurally narrow. It is gated by competitive cohort admissions and run on fixed multi-month program cycles most applicants never reach. Plan9 alone reports 195+ graduated startups across 14 incubation cycles (https://plan9.pitb.gov.pk/node/1176, accessed October 13, 2026; the alumni listing shows Cycles 1 to 14 and the page reports 195+ graduated startups, while the introductory text on the same page still gives 160 startups in 10 cycles, and earlier articles show 170+, so the figure is dated). Founders outside that gate — by timing or a rejected application — have no structured way to get feedback on traction, validate a market, practice a pitch, or find vetted mentors and investors.

A parallel, largely separate gap exists on the talent side. People who specifically want to work at a startup — as an employee, intern, or early hire — have no dedicated pathway. General job boards (Rozee.pk, Indeed, Glassdoor) are not curated for startups (a search on 13 October 2026 returned only about 20 companies and 3 open jobs across the three), and the one platform positioned as startup-focused (InnoCollab.pk) labels a section "Talent" that, on direct audit, serves founders promoting their own ventures — not candidates seeking employment at someone else's startup.

The problem The Founder's Carnet addresses is therefore two-sided and specific: access to startup guidance, capital connections, and startup-specific employment in Pakistan is gated by competitive cohort admissions, not by genuine need or merit. Platforms addressing parts of this gap exist — most directly i2i's Investor Founder Discovery Platform, which connects founders and investors through a curated directory (Section 4.4) — but no audited platform serves the founder, talent, and mentor/investor sides together from one integrated, AI-native product with a regulatory compliance layer.

**Regulatory corroboration of this problem statement.** SECP's own position paper, *Holistic Framework for Building a Supportive Start-up Ecosystem in Pakistan* (30 October 2024), states that varying start-up definitions used by SECP, SBP, FBR, STZA and SMEDA create a fragmented regulatory environment in which "start-ups may face difficulties in navigating different regulatory frameworks"; that there is "limited access to experienced mentors and advisors to guide start-ups through growth stages"; and that entrepreneurs "are often unaware of available resources, funding options, government policies, and international markets." The same paper records that the majority of tech hubs and labs are concentrated in Islamabad, Lahore and Karachi, which "limits access to resources for entrepreneurs in tier 2 and tier 3 cities." These are the regulator's own findings, not this project's inference.

## 2.1 Objectives

1. Design and build an AI-native platform connecting five distinct stakeholder types — founders/startups, talent, mentors, investors, and admin/moderation — on one shared reasoning engine, rather than as disconnected single-purpose tools.
2. Train and evaluate a hybrid semantic + structured-feature re-ranking model for founder-mentor, founder-investor, and startup-talent matching, benchmarked against a cosine-similarity-only baseline (NDCG@K, MRR).
3. Build a retrieval-augmented compliance assistant grounded exclusively in official SECP/FBR/PSEB sources, with mandatory source citation and a no-guessing fallback when no confident grounded answer exists.
4. Deliver AI-assisted founder readiness scoring, investor pitch simulation, market research synthesis, and resume/LinkedIn optimization as prompted (not trained) LLM features, each validated against a defined evaluation approach (Section 17).
5. Support English, Urdu, and Roman Urdu in AI-generated conversational output, with per-language quality benchmarked rather than assumed equal (Section 13.7).
6. Keep the platform's legal and business-model footprint deliberately narrow — no equity taken, no investment brokered on-platform, no scraping of individual personal profiles — so the system's regulatory exposure stays comparable to a job board or professional directory, not a licensed financial intermediary (Section 18).
7. Demonstrate the above as a working, deployable prototype within a three-person, six-month build (Section 22), with a documented fallback order (Section 22) if scope needs to compress.

# 3. Literature / Research Foundation

This section grounds the technical design in established research rather than treating "AI" as an unstructured feature list. It is a scaffold; the team will expand it with a formal search of IEEE Xplore, ACM Digital Library, and Google Scholar during the literature-review phase, particularly for 2023–2026 work on LLM-based decision support and startup/SME analytics.

**Retrieval-Augmented Generation.** Lewis et al. (2020) introduced RAG, combining a parametric language model with a non-parametric retrieval index so generated text is grounded in retrieved documents rather than the model's internal parameters alone. This directly informs the compliance assistant's design: rather than letting the LLM answer registration or tax questions from memory (real hallucination risk), answers are grounded in a retrieval index built from official SECP, FBR, and PSEB documentation, with citations to source. RAG is the standard technique for mitigating hallucination in knowledge-intensive, low-error-tolerance domains, which is why it is used here instead of an unconstrained chat interface.

**Sentence Embeddings for Semantic Matching.** Reimers and Gurevych (2019) proposed Sentence-BERT, using siamese and triplet network structures to derive sentence embeddings comparable by cosine similarity. This underpins the matching service: founder, mentor, investor, and talent profiles are embedded into a shared vector space, candidates are retrieved by similarity search, and a lightweight trainable re-ranker layers in structured filters (sector, stage, availability) and, once enough exists, observed accept/decline outcomes.

**AI-Assisted Decision Support for Small and Growing Businesses.** Applied research and industry analysis consistently show AI decision-support tools deliver the clearest early ROI for resource-constrained businesses in narrow, well-defined tasks — sales/traction analysis, structured recommendation — rather than open-ended automation. This motivates scoping each The Founder's Carnet AI feature (readiness scoring, pitch feedback, market synthesis) around one specific, bounded decision rather than a general-purpose "business assistant."

**Learning-to-Rank.** The matching engine's core research framing: given a query entity and a candidate set, learn a scoring function that ranks relevant candidates above irrelevant ones, using pairwise or graded relevance judgments as training signal and NDCG@K / MRR as evaluation metrics. This is what separates the matching engine from "an LLM that suggests people" — it is a trained, benchmarked model with a baseline comparison.

# 4. Competitive Analysis

The team conducted direct, hands-on audits — creating accounts and inspecting live product screens — for four platforms structurally closest to The Founder's Carnet: InnoCollab.pk, PakStartups.org, PakLaunch, and StartupNetwork.pk. Pitch Pakistan was in the September 2026 audit set but was removed from the report on 13 October 2026 (it is not an investor or venture platform, and its site was unreachable on that date). One platform from the original ecosystem scan, Startup.pk, remains unaudited (public web presence only) and is flagged accordingly in Section 4.2 rather than blended in as if equally verified.

## 4.1 Directly audited (hands-on account walkthroughs)

| Platform | What it offers | Confirmed limitation |
|---|---|---|
| **InnoCollab.pk** | AI pitch practice, AI market research, AI pitch-deck generator, AI co-founder matching, mentor booking, investor discovery (as described on the public page), gamified pitch streaks/leaderboards, cofounder compatibility quiz | The bundled "Talent/Entrepreneur" *role* is founder self-promotion (submit an idea, connect with investors/mentors/team) — confirmed by direct audit, not a candidate-facing job pathway. **Re-verified September 2026:** a separate "Meet Our Talented Innovators" directory complicates a one-line summary of this — individual profiles tagged by skill (digital marketing, SEO, content writing, data analytics, Java/C++) with a "Sign up to Connect" action, closer to a genuine skills directory than founder self-promotion. Both exist on the platform simultaneously; neither is a startup-specific job/internship board with real listings (detail in Appendix A). No government compliance content. English only. No real-world events, only in-app messaging. |
| **PakStartups.org** | Startup directory (verified by funding stage), co-founder matchmaking engine, Ecosystem Directory (incubators/accelerators/VCs/government programs), a Knowledge Vault with incorporation guides and SAFE templates, events calendar, active Reddit and Discord communities | No AI anywhere on the platform — no scoring, matching AI, or generation. **Re-verified August–September 2026** (direct account walkthrough, Appendix A): the Startup Directory is genuinely populated, not empty — 100+ real listings confirmed by direct visit, including full detail pages with named founders (e.g., Artbazaar.pk, founders Fatima, Ahsan, and Abdul Rafay). This corrects an earlier snapshot of the same platform that found several features unpopulated; the platform has clearly been built out since. The site's own stated figures — 100+ verified startups, 14,000+ members in its r/PakStartups Reddit community — are confirmed by direct visit. However, the Ecosystem Directory ("0 of 0 organizations"), the Events calendar (one listed event, zero RSVPs), and the Knowledge Vault's "Learning Guides" subsection ("0 guides," featured guide marked "Coming Soon") were all confirmed still empty or near-empty on the same September 2026 visit — the build-out reached the Startup Directory specifically, not the platform as a whole. **Not yet independently re-confirmed:** whether the separate Find Co-Founder matching tool is similarly populated with real (rather than curated/example) listings — protocol in Appendix B. |
| **PakLaunch** | A large, active diaspora network — founded in San Francisco (April 2020) by Aly Fahd as a single WhatsApp group; states 400K+ members as of August 2025 (the site's own pages show inconsistent figures — 300K–500K members and $80–130M+ facilitated funding depending on which page is checked; cite as a range with this caveat, never a single hard number). **Directly audited September 2026** (registered account, Appendix A): a real, active member community — genuine founder posts soliciting investment and co-founders, real regional meetups (Toronto, Hong Kong, Singapore, Riyadh) organized by named members, an embedded AI assistant ("Halo"), a real job board, LMS-style learning resources (Product Management, Design Thinking, and similar short courses), and a named testimonial from Asif Awan of Indus Valley Capital (already a Wave 2 outreach target, Section 20) confirming real fundraising outcomes attributed to the community. | In the team's September 2026 test, Halo declined SECP/FBR/SBP regulatory questions when asked directly — corroborates the compliance-assistant gap (Section 5) rather than undermining it — but Halo's own in-chat membership pricing ($50/$500/$1,000 tiers) does not match the platform's live pricing page ($300/$1,000/$3,000 tiers), a concrete real-world example of the ungrounded-answer failure mode Section 13.6 is built to avoid. The job board has real postings, but they are general-professional (Video Editor, Real Estate Analyst, AWS Consultant) and stale (~7–9 months old at audit time) — not curated for startup-specific or entry-level roles. Forum/group content is real but only lightly moderated: includes members openly soliciting trading capital and promoting personal investment platforms inside discussion groups, exactly the kind of unmoderated financial solicitation this project's scope (Section 6.2, Section 18.1) deliberately stays away from. Not an AI-native, open self-registration platform — its strength is human network and live events, not algorithmic matching or scoring. |
| **StartupNetwork.pk** | A classifieds-style directory, job board, and events aggregator explicitly positioning itself around startups, investors, and job seekers. | **Directly audited September 2026** (registered account, Appendix A): the startup directory is real and populated — 37 listings confirmed by direct visit, mixing tech startups with traditional SMBs (an IP law firm, a clothing manufacturer, a resort). Registration offers exactly two roles, Startup or Investor — **no talent/job-seeker registration path exists at all**, despite the platform's own "job seekers" positioning. The Events tab and the Jobs tab both return "There are no listings matching your search" despite full filter UIs (vacancy type, qualification, salary, date range). This replaces an earlier, less precise claim that the whole site returned no listings — the directory itself is real; the job-board and events functionality are the parts that are empty. No AI anywhere on the platform. |

## 4.2 Broader ecosystem scan — preliminary, pending hands-on confirmation

One platform from the original ecosystem scan remains unaudited. **Basis: public web presence only — not yet independently confirmed by the team registering and using the platform.** Kept clearly separate from Section 4.1 so the two evidence qualities are never blended. (PakLaunch and StartupNetwork.pk were also identified in this scan but have since been directly audited with registered accounts — see Section 4.1.)

| Platform | What it actually is | Relevant gap for The Founder's Carnet |
|---|---|---|
| **Startup.pk** | Primarily a media/content platform (news, funding roundups, founder guides), reaching a stated 800+ founders/investors/ecosystem players. Announces a paid tier, **Startup.pk Pro** (Rs. 1,999/month), described as offering weekly investor-intelligence reports, real-time funding/grant alerts, and "warm, matched intros to angels and VCs." As of 13 October 2026 the public page shows it as a waitlist, not a launched product. | The closest thing to a paid, investor-matching competitor found in this scan. But matching appears human-facilitated ("warm intros"), not AI-scored, and there's no public evidence of a talent/job board, a founder readiness score, or an interactive compliance assistant — its regulatory content (e.g., SECP/SBP explainer articles) is the same static-article model as PakStartups' Knowledge Vault. |

*A fifth name surfaced during the original research pass, "Pakistan Startup Connect," but direct investigation found it isn't a comparable product at all — it's the Pakistani government's registration portal for the Pakistan Startup Fund (a matching-grant program under the Ministry of IT), where VC funds register as grant partners. It's dropped from this comparison as a mismatch rather than forced into a table it doesn't belong in.*

## 4.3 Known from general market/public information (not newly audited)

| Platform | What it offers | Confirmed limitation |
|---|---|---|
| **NIC / Plan9 / i2i / LUMS CFE** (physical accelerators) | Human mentorship, cohort programs, investor introductions; Plan9 alone reports 195+ graduated startups across 14 cycles (Section 2) | Cohort-gated through competitive admissions, fixed multi-month cycles, no AI/data layer, no talent/employment side. |
| **VC4A** | Global mentor marketplace with AI "Smart Matching" | Not Pakistan-specific; not bundled with readiness scoring, pitch practice, or a talent board. |
| **1Mby1M** | Global virtual accelerator marketing an "AI Mentor" in 57 languages, no equity taken | Validates the AI-mentor concept globally but has no Pakistani regulatory grounding, no PKR context, no local investor network. |
| **Rozee.pk / Indeed / Glassdoor / Wellfound** | General or globally-generic job boards; Wellfound carries some startup listings | None curated specifically for the Pakistani startup ecosystem. |
| **Internee.pk** | Pakistan-specific virtual internship platform with structured tasks and mock interviews | Builds skills via simulated tasks; does not connect candidates to live hiring needs at real startups; no founder-facing product. |
| **ReadyScore / ValidatorAI-type tools** | Standalone AI startup readiness/fundability scoring | Global, generic, not localized, not bundled with anything else. |

## 4.4 i2i Investor Founder Discovery Platform (IFDP) — the closest existing system

**Added October 2026.** IFDP was not in the original competitive scan and is the single closest existing system to this project. It was publicly browsable at `https://ifdp.invest2innovate.com` on 3 October 2026 (the site did not load on 13 October 2026), funded under i2i's Visa Foundation-backed "i2i Ecosystem" project (a USD 500,000 commitment announced 12 January 2024) and reported launched in October 2024.

**Organizational status — material to how this entry should be read.** In April 2026, i2i's founder Kalsoom Lakhani announced that Invest2Innovate, the organization she founded in 2011, is closing after fifteen years of supporting Pakistan's startup ecosystem. The same announcement states explicitly that **i2i Ventures, the separate venture capital fund, is not closing** — only the ecosystem-support organization that operates IFDP. The platform was accessible on 3 October 2026 but did not load on 13 October 2026, so this document does not claim it is permanently offline; what is uncertain is its continued maintenance and the fate of the national-portal proposal below, whose intended operator is winding down. This should be stated as uncertainty, not as a competitor's demise: the platform was live when checked, its data was real, and a successor or acquirer is possible.

**What does not change.** i2i's published research — the Pakistan Startup Ecosystem Report and the Deal Flow Tracker figures cited in Section 25 — remains valid and citable. A publisher ceasing operations does not retract its published work.

| Platform | What it actually is | Relevant gap for The Founder's Carnet |
|---|---|---|
| **IFDP** (Invest2Innovate) | An approval-gated directory of startups, founders, and investors. Registration is open to all three profile types; profiles publish only after i2i approval. Its own stated flow is: submit a request → "Get Verified & Go Live — Once approved, your profile goes live" → "Curated Matchmaking — If you opt in, we'll connect you with relevant startups, founders, or investors." Startup listings carry structured fields (founding year, team size with gender split, funding raised and type, last round date, instruments, valuation, lead investor, stage, competitors, sectors, regions). Discovery is taxonomy filtering. | **Two-sided only** — no talent/jobs side and no mentor profile type. **No compliance or regulatory features.** **No AI matching, ranking, or search** — the i2i policy brief that proposes scaling IFDP nationally describes its AI modules as *planned*, and none are observable on the live platform. Verification method is not described beyond a statement that it "ensures that all community members are genuine." No user counts are published. |

**Evidence discipline applied to this entry.** i2i's policy brief *Closing the Funding Gap for Startups in Pakistan* (June 2025) describes IFDP as having "soft-KYC verification, curated startup and investor profiles, and warm-introduction tools." Of these, the public pages describe curated matchmaking; the staff-mediated introduction step was observed only in the team's logged-in session (screenshots retained) and is reported here as observed, not independently verifiable by a reader. The brief's headline description of IFDP is copied from i2i's own platform marketing copy, and the brief itself was co-developed by i2i and supported by Visa Foundation, which also funds IFDP — so its description of IFDP is not an independent assessment. This document therefore records what the live platform demonstrably does, and marks the remainder as claimed rather than verified.

**What IFDP does better than this project will.** i2i holds the Deal Flow Tracker funding dataset, an established ecosystem brand, and real investor relationships. This project has none of those and should not pretend otherwise.

**Related public-sector activity.** The Pakistan Startup Fund, run by MoITT and executed by Ignite, operates its own portal at `startupconnect.pk` with equity-free co-investment grants and investor matchmaking. It is unconnected to i2i and is the more relevant public-sector comparator — more so now, given i2i's announced closure.

**The national-portal proposal is effectively dormant.** The i2i policy brief proposed that MoITT establish a Digital National Startup–Investor Matchmaking Portal by scaling IFDP, with Ignite providing policy mandate and seed funding and i2i operating it. No announcement, funding, or memorandum of understanding was found, so it was only ever a recommendation; with its proposed operator closing, it is unlikely to proceed in that form. This document does not treat it as a live competitive threat, and does not treat its absence as permanent either.

---

# 5. Gap Analysis & Differentiation

Cross-referencing the problem statement against the audited landscape leaves four confirmed, evidence-backed gaps:

1. **A genuine startup-employment pathway.** Confirmed absent from InnoCollab.pk (whose bundled "Talent/Entrepreneur" role is founder self-promotion — though a separate skills-tagged directory on the same platform means this can't be summarized in one line without a caveat, Section 4.1) and from StartupNetwork.pk (registration offers no talent/job-seeker role at all, and its own Jobs tab returns zero results despite a full filter UI, Section 4.1). PakLaunch has a real, working job board — the closest actual threat to this gap of anything directly audited — but its listings are general-professional and stale (~7–9 months old at audit time), not curated for startup-specific or entry-level roles (Section 4.1). PakStartups.org's overlap here remains an open, specifically-scoped question: its Startup Directory is confirmed populated (Section 4.1), but whether its separate "Find Co-Founder" tool functions as genuine talent/employment matching, or is comparatively sparse, is being tested directly with real registered test profiles (Appendix B) rather than assumed either way.
2. **An interactive, cited compliance assistant** grounded in SECP/FBR/PSEB sources. PakStartups.org has a static Knowledge Vault — and its "Learning Guides" subsection specifically returns zero results at present (Appendix A), a step below even "static but complete" — and Startup.pk's regulatory content (Section 4.2) is the same static-article model. PakLaunch's embedded AI assistant, Halo, corroborates this gap directly rather than closing it: when the team asked about SECP/FBR/SBP rules in September 2026, it stated it had no knowledge of them rather than guessing (Section 4.1; a dated observation, not a standing claim about the product). No audited or scanned platform offers a grounded, query-able Q&A interface for compliance questions.
3. **English, Urdu, and Roman Urdu accessibility** in AI-generated content — every audited or scanned platform, including IFDP, is English-only.
4. **Integration on one shared AI reasoning engine**, rather than separate products for separate audiences — and, specifically versus PakStartups.org, an AI layer at all: its directory, matching, and listing features are static/manual with no scoring, matching AI, or generation anywhere on the platform.

The founder-mentorship and investor-matching features individually already exist elsewhere (most notably InnoCollab.pk); the directory/community model already exists elsewhere (most notably PakStartups.org, whose Startup Directory is confirmed populated with 100+ real listings and whose community channels report 14,000+ members, concentrated in its r/PakStartups Reddit community specifically). Neither is claimed as novel in isolation — the differentiation rests on the four points above, combined, plus a research-grade evaluated matching engine (Section 13) that none of these platforms have published evidence of.

**The closest funded competitor on the investor side specifically is Startup.pk Pro** (Section 4.2), a paid subscription offering "warm, matched intros to angels and VCs." It's worth naming directly rather than ignoring: it signals that others see a market for matching/intelligence tools (it is still a waitlist, so it is not evidence of willingness to pay), while still leaving the AI-scored, trained-model differentiation intact — Startup.pk Pro's matching is described as human-facilitated, not algorithmic.

**Claims The Founder's Carnet will not make:** "first AI startup platform in Pakistan," "first platform connecting founders and investors in Pakistan" (IFDP is live and predates this project — Section 4.4), "no Pakistani platform has AI," "our AI predicts which startups get funded," "our matching guarantees successful mentorship or investment."

**Claims The Founder's Carnet will make:** an integrated AI decision-support workflow across founder, talent, mentor, and investor use cases; a hybrid semantic + structured-feature re-ranking model as the primary ML contribution; regulatory information grounded in an indexed, cited corpus; explicit English/Urdu/Roman Urdu evaluation rather than an assumed capability.

# 6. Proposed Solution & Scope

## 6.1 Phase 1 — Potential FYP (in scope, built and demonstrated)

What follows is scoped as the FYP deliverable — realistic for a three-person student team to build and demonstrate within the project timeline. Phase 2 (Section 23), by contrast, is what's expected if the team decides to take The Founder's Carnet beyond the FYP as a real business.

- Founder profiles with AI mentor feedback and an AI-generated readiness/fundability score
- AI-simulated investor pitch practice with scoring and feedback
- AI market research synthesis (competitor scan and rough sizing, clearly labelled as synthesis, not syndicated data)
- Talent profiles with an AI resume and LinkedIn/X profile optimizer
- A curated, startup-specific job/internship board
- Mentor and investor discovery via embedding-based matching + trained re-ranker, with identity revealed only on mutual acceptance
- A RAG-based compliance assistant grounded in SECP, FBR, and PSEB documentation
- English, Urdu, and Roman Urdu support in AI-generated conversational output, benchmarked rather than assumed
- **Curated external resource links** — SAFE templates, incorporation checklists, and founder guides, linked out to their original trusted sources (SECP, PSEB, YC's public SAFE) rather than authored or re-hosted by The Founder's Carnet. Deliberately a short curated list, not a content library — reproducing static guides in-house would undercut the exact differentiation claimed against PakStartups' Knowledge Vault in Section 5, and re-hosting others' documents raises copyright questions this project doesn't need to take on.
- **Ecosystem events calendar** — cross-lists real events already run by others: the anchor-partner institution (Section 20), and known ecosystem players (NIC, Plan9, PakLaunch's UNconference, PSEB/Ignite programs). The Founder's Carnet does not organize, host, or staff any event itself — that's Phase 2 territory (Section 23) for the same operational-capacity reason paid cohort training is.
- **Hybrid profile review** — every founder, talent, mentor, and investor profile is scored automatically at registration. Clear cases are verified or rejected immediately, and ambiguous cases and appeals from rejected users are reviewed by a person. A profile becomes visible to others only after it is verified, automatically or by a reviewer. Full detail in Section 13.8.
- **In-platform usage guides** — short, team-authored "how this works" pages for each user type (what a readiness score means, how matching works, what "Verified" means), distinct from the curated external resource links above, which are ecosystem knowledge rather than platform documentation.

## 6.2 Explicitly Out of Scope

- Taking equity in any startup, in any form, at any stage
- Brokering, executing, holding funds for, or managing/mediating any investment transaction or legal action between investors and startups — any resulting meeting or deal happens off-platform, through normal channels, with the Carnet's role ending at the introduction
- An open community forum or discussion board
- Team/project-management tooling
- Paid, human-staffed cohort training programs
- Organizing, hosting, or staffing events — the events calendar (Section 6.1) only surfaces events run by others
- Negotiated third-party vendor perks/discounts ("deals" program)
- Scraping of individual persons' personal profile data — mentors, investors, and talent register directly instead
- Legal or tax advice of any kind; the compliance assistant is informational and cites sources, never certifies correctness
- Predicting funding outcomes with certainty; the readiness score is explicitly not a funding probability
- General small/medium business financing and operations support (bank-style credit, cash-flow management, succession planning) for traditional businesses outside the venture-growth model — a distinct market with different investor types and regulatory context (Section 8), deliberately left to a separate product rather than stretched to fit here

## 6.3 Constraints

- **Team size:** three students (Ali Ahmad — AI/ML and system design, Shahzeb Imran — frontend, Taha Nawaz — backend), with no dedicated designer, QA, or DevOps role.
- **Timeline:** two semesters, approximately eight months end-to-end (Section 22), including validation interviews, build, evaluation, and defense preparation.
- **Budget:** no paid infrastructure — free/low-cost tiers only (Vercel, Railway/Render, university-provided GPU access for model fine-tuning), and no real payment-gateway integration during the FYP (Section 23) since the team has no incorporated legal entity to hold a merchant account.
- **Data availability:** no existing Pakistani startup-ecosystem dataset at any credible scale; every labeled dataset (matching relevance labels, multilingual benchmark/fine-tuning triples) must be built from self-registration, consented pilot data, manual authorship, or LLM-assisted synthetic generation (Sections 9, 13.7) — never scraped.
- **Regulatory:** the platform must stay outside SECP's broker-dealer/financial-intermediary licensing territory (the specific mechanism SECP has used to test crowdfunding-adjacent activity is the Regulatory Sandbox Guidelines, 2019 — not a standalone "Equity-Based Crowdfunding Regulations," a name that does not check out against SECP's own published regulations) and comply with PECA's data-collection rules (Section 18) — this rules out equity-taking, on-platform deal brokering, and any scraping of individual personal profiles, and shapes the business model, data sourcing rules, and feature scope throughout this document.
- **Team expertise:** none of the three team members has prior hands-on experience with RAG pipelines, contrastive/triplet embedding fine-tuning, or production-scale multilingual NLP — these are learned during the build (background technical grounding, not a formal literature review) before implementation, which is reflected in the conservative, staged approach to the multilingual and matching-engine work (baseline first, fine-tuning only as a validated stretch goal).

# 7. Business Model & Monetization

The Founder's Carnet does not monetize the side that has no money (founders) or attempt to monetize investment outcomes (regulatory landmine). It monetizes access to tools and successful hiring outcomes instead.

![Business model — who pays, who doesn't, and what stays off-platform](diagrams/business_model.png)

| Side | Model | Why |
|---|---|---|
| **Founders** | Free | Founders are the supply side of the whole ecosystem and the primary source of the interaction data the matching engine needs. Charging them suppresses the exact usage that makes the rest of the platform valuable. |
| **Talent (job/internship-seekers)** | Freemium subscription — free basic profile + job board access; paid tier unlocks the AI resume/LinkedIn optimizer, unlimited pitch-adjacent career tools, and priority visibility to startups | Talent has some ability to pay for a career tool (comparable to LinkedIn Premium, Rezi, Teal), and the AI optimizer is a clear, demonstrable value-add they'll pay for directly. |
| **Mentors** | Flat subscription for dealflow access and mentorship-matching tools | A flat fee for access and tooling — never a fee contingent on a specific outcome — keeps this a straightforward software subscription. |
| **Investors** | Flat subscription for dealflow access and investment-matching tools | A flat fee for access and tooling — never a fee contingent on a specific investment outcome — keeps this a software subscription, not a security or brokerage arrangement, avoiding broker-dealer or financial-intermediary classification under SECP's securities framework (Section 18.1). |
| **Startups (talent-hiring side only)** | Cash placement fee, charged to the startup only when it successfully hires a candidate sourced through the Carnet's job/internship board | Standard, well-precedented recruiting revenue model (the same mechanism Wellfound, LinkedIn Recruiter, and traditional recruiters use). No equity, no investment link, no licensing complexity. |

**On investor–startup deals specifically:** the Carnet's role stops at a mutually-accepted introduction. Any resulting meeting, negotiation, term sheet, or closed investment happens **off-platform**, through the parties' own channels — The Founder's Carnet does not track, verify, mediate, or take any fee tied to whether a deal closes. This is a deliberate design choice, not an oversight: a platform that takes a cut of a deal it cannot see or verify creates both an unenforceable business promise and a real regulatory exposure (see Section 15). Earlier drafts of this project considered a success-fee-on-investment model; it was dropped for exactly this reason.

## 7.1 Business Opportunity

Pakistan's startup ecosystem has real, growing activity (physical accelerators, an active angel/VC community, a stated government push via PSEB/Ignite) but no integrated digital layer connecting its three sides — founders, startup-specific talent, and the mentors and investors who support them — on one product. The closest local competitors are single-purpose: InnoCollab.pk covers founder-facing AI tools but has no genuine talent/employment pathway; PakStartups.org has a populated directory and community but no AI layer at all (Section 4). The opportunity is not a new market category — it's the specific, evidence-backed integration gap identified in Section 5, monetized through recruiting-style placement fees and career/dealflow subscriptions rather than investment-linked revenue, which keeps the business model outside licensed-intermediary territory (Section 18.1) while still being a well-precedented model (the same mechanism Wellfound and LinkedIn Recruiter already use).

## 7.2 If this becomes a real company after the FYP

The FYP proves the product and the core ML contribution; it does not need to prove the company. If the team chooses to continue The Founder's Carnet past graduation, the realistic sequence is:

1. **Incorporate** as a private limited company via SECP once the team is ready to accept real subscription payments and enter into real terms of service (a legal step, not a technical one — the FYP prototype does not need this).
2. **Get a targeted legal review** of the subscription and placement-fee model specifically — confirming neither structure inadvertently triggers investment-intermediary or brokerage classification — before turning on real billing.
3. **Convert the anchor-partner relationship** (Section 20) from a pilot data-sharing arrangement into the Carnet's first paying B2B relationship: license the readiness-scoring, pitch-simulation, and matching tools to that incubator as their internal cohort infrastructure, rather than trying to acquire three sides of a marketplace cold.
4. **Turn on real payment rails** (JazzCash/Easypaisa) for the talent, mentor, and investor subscriptions, replacing the FYP's mocked paywall.
5. **Only then**, with real usage and a real dataset, consider the aggregated ecosystem intelligence product (Section 23) as a second revenue line sold to VCs, corporates, and government bodies (PSEB/Ignite) — this requires meaningfully more usage than an FYP will produce and should not be presented as an FYP deliverable.

Everything in Phase 2 (Section 23) is sequenced against this path — each item is deferred for a specific business, legal, or resource reason, not because it lacks value.


# 8. Stakeholders Description

The platform is built around five distinct stakeholder types, not three — mentors and investors are separate user types with separate profiles, separate matching logic, and separate (if similarly structured) subscriptions, and the admin/moderation role is a fifth, internal stakeholder with its own dedicated console (Section 11.1, Section 13.8), not a footnote to the other four.

## 8.1 Stakeholders Summary

| Stakeholder | Who they are | Role on the platform |
|---|---|---|
| **Founders / Startups** | Early-stage Pakistani founders outside, or not yet part of, the existing cohort-based accelerator system — explicitly including founders past idea-stage: registered, revenue-generating businesses at MVP, Growth, or Scaling stage (Section 9's `stage` field), not just first-time idea validation. | Free users; the platform's supply side. Submit a profile, receive AI readiness scoring/mentor feedback/pitch practice, request mentor and investor matches, optionally post job/internship listings. |
| **Talent** | University CS/business students and early-career professionals specifically seeking startup employment or internships — unserved by both general job boards and InnoCollab.pk's founder-oriented "Talent" section. | Freemium subscribers. Submit a CV/profile, receive AI resume/LinkedIn optimization, browse the curated job/internship board, optionally request mentor matches for career guidance. |
| **Mentors** | Industry professionals and university faculty (a low-friction initial pool given the team's own institutional access) offering expertise/time rather than capital. | Flat-subscription users. Matched to founders and talent by the ranking service on expertise fit (Section 13.5); identity shared only on mutual acceptance. |
| **Investors** | Pakistan-based angels/VCs already engaged through NIC, Plan9, i2i, or VC4A's existing Pakistan-based investor pool, offering capital rather than time/expertise. | Flat-subscription users. Browse startups with a verified profile and a completed readiness assessment (FR-10); matched to founders; identity shared only on mutual acceptance; any resulting investment happens off-platform (Section 18.1). |
| **Admin** | The project team, acting as platform moderators/reviewers — an internal stakeholder, not an external platform user. | Oversees the hybrid profile verification system (Section 13.8): monitors auto-verify/auto-reject thresholds, personally reviews only the ambiguous cases escalated to human review and appeals from rejected users, handles reported/blocked profile re-review, monitors regulatory-corpus freshness. |

Mentors and investors are kept structurally separate deliberately: they have different profile fields (expertise/availability vs. investment thesis/stage), different matching signals feeding the re-ranker (Section 13.5), and — while both pay a flat subscription — different underlying reasons the flat-fee structure matters (for investors specifically, it's what keeps the platform out of broker-dealer/financial-intermediary licensing territory under SECP's framework; Section 18.1). Treating them as one merged "Mentor/Investor" role earlier in this project's drafting undersold that distinction — it's corrected throughout the document now (Sections 7, 11.1, 15).

## 8.2 Key High-Level Goals and Problems of Stakeholders

**Founders / Startups**
- *Goals:* get structured, honest feedback on investment/hiring readiness; practice pitching before it counts; find mentors and investors without needing a pre-existing personal connection.
- *Problems today:* gated by competitive cohort admissions; no structured feedback loop for founders outside that gate; no way to build a trustable track record with a stranger investor or mentor without a personal introduction first (Section 1.1).

**Talent**
- *Goals:* find genuine startup-specific employment or internships; present their experience compellingly for startup roles specifically.
- *Problems today:* general job boards (Rozee.pk, Indeed, Glassdoor) aren't curated for startups; the one platform positioned as startup-focused (InnoCollab.pk) labels a section "Talent" that actually serves founders promoting their own ventures, not candidates.

**Mentors**
- *Goals:* find founders genuinely worth their time efficiently, without relying entirely on an existing personal network.
- *Problems today:* mentorship access is currently relationship-gated the same way founder access to capital is (Section 1.1, Section 2) — there's no structured way to see a founder's actual readiness before committing time to them.

**Investors**
- *Goals:* find vetted founders with a completed readiness assessment efficiently, without wading through unvetted dealflow or relying solely on warm intros.
- *Problems today:* the same network-dependency problem as mentors, compounded by the fact that no local platform combines AI-scored readiness with genuine matching (Startup.pk Pro's "warm intros" are human-facilitated, not algorithmic — Section 4.2).

**Admin**
- *Goals:* keep fake, bot-generated, or low-effort profiles off the platform without over-promising an automated solution that isn't achievable yet.
- *Problems today:* at FYP scale, there simply aren't enough confirmed fraud/fake-profile examples to safely train a fully automated legitimacy classifier (Section 13.8) — most profiles are resolved automatically via an authored signal-scoring rule, but review stays human-in-the-loop specifically for the ambiguous minority, which is a real, ongoing operational cost the design accounts for rather than hides.

Precise market-sizing figures for this specific bundled segment are not independently available and will not be asserted with false precision. Founder- and talent-validation interviews (Section 17) are the primary source of demand evidence, not an invented TAM figure.

**A specific underserved subgroup worth naming:** roughly 1% of Pakistani businesses are women-led, a well-documented gap the government's own Ignite-backed WISE Lab initiative was created to address. The Founder's Carnet makes no algorithmic changes on the basis of gender — see Section 19 for why building demographic weighting into the ranking model itself is deliberately out of scope — but this is a concrete, low-cost thing to act on operationally: prioritizing outreach to women-led founders and women in tech during anchor-partner recruitment (Section 20) is a market-awareness decision, not a model change.

**What The Founder's Carnet is not for, deliberately:** general small/medium business financing and operations support — a retail shop or family manufacturing business seeking bank-style credit, cash-flow management, or succession planning is a different market with different investor types (banks and microfinance, not angels/VCs), a different regulatory context, and a readiness rubric that wouldn't mean the same thing for both audiences. the Carnet's readiness scoring (Section 13.1) is calibrated around venture-style growth ambition specifically; stretching it to cover traditional SME financing would make it incoherent for both audiences rather than useful for either. This is a deliberate scope boundary, not an oversight — general SME support is a distinct enough market that it deserves its own product, not a bolt-on to this one.

# 9. Datasets

Every dataset below is either self-registered, publicly sourced with attribution, or built through direct human annotation — none is scraped from individuals' personal profiles, in line with PECA.

| Dataset | Source | Target size (pilot) | Purpose |
|---|---|---|---|
| Startup profiles | Self-registration | 50–150 | Idea/stage/sector representation for readiness scoring and matching |
| Mentor profiles | Self-registration + anchor-partner referral | 30–75 | Founder–mentor matching |
| Investor profiles | Self-registration + anchor-partner referral | 20–50 | Founder–investor matching |
| Talent profiles | Self-registration | 75–200 | Startup–talent matching |
| Startup jobs/internships | Founder-submitted, curated | 50–150 | Talent retrieval/ranking |
| **Human relevance labels** | Pairwise/1–5 ratings, sourced primarily through the anchor-partner incubator's real cohort (Section 20) | 150–300 realistic initial target; 1,000+ is the long-run goal, not the FYP target | Re-ranker training/evaluation — this is the load-bearing dataset for the whole ML contribution and the one most dependent on the anchor-partner relationship actually landing |
| Regulatory document corpus | Official SECP/FBR/PSEB sources only, whitelisted — verified current entry points for all three plus PECA, SBP, BOI, and PBS are maintained in the companion Resources, Literature & Dataset Reference document, Section 9.1 | Fixed and profiled 4 October 2026: 11 documents (Section 13.6) | RAG grounding for the compliance assistant |
| Market evidence corpus | Curated, traceable public sources | As needed per synthesis query | Evidence-backed market synthesis |
| Multilingual benchmark set | Team-authored + LLM-assisted parallel English/Urdu/Roman Urdu profile and query pairs | 30–50 examples per language | Baseline benchmark (committed deliverable) — measures how much matching and RAG quality degrades per language before assuming equal performance, rather than after (Section 13.7) |
| Multilingual fine-tuning triples (stretch) | Consented pilot-user profiles + manually authored/LLM-assisted synthetic profiles, labeled (anchor, positive, negative) by the team — sourcing locked to Section 13.7's rules, never scraped | Go/no-go threshold set and checked at the Month 4 checkpoint (Section 13.7); attempted only if met | Contrastive/triplet fine-tuning of the multilingual embedding model — a second, stretch-goal trained artifact, contingent on legitimately-sourced labeled data actually materializing |
| Readiness-score calibration set | Team- and mentor-authored sample startup ideas, independently rated by 2–3 human reviewers | 20–30 | Correlation check between the LLM-scored rubric and human judgment |

**External datasets, profiled 3 October 2026 (none trains the deployed re-ranker).** Five are kept: the Roman-Urdu-Parl Hugging Face split (6,374,678 Urdu and Roman Urdu pairs, multilingual benchmark source); the LinkedIn-Dataset of Ayoobi et al. (3,600 profiles, research use only, aggregate use only); two Crunchbase schema proxies on Kaggle (Startup Success/Fail, 66,368 rows; StartUp Investments, 54,294 rows with 4,855 duplicate rows); and the Kaggle Resume-Job Matching Dataset (150,493 resume-vacancy pairs, 86.1% rejected, Russian market, practice data only). Two were screened and excluded: Resume Dataset PDF (image-only files) and an ATS resume-screening dataset (short texts consistent with synthetic generation). None states a licence except the LinkedIn README, so all are used for internal profiling and schema design only, never redistributed, and names, birth dates, age, gender and contact fields are excluded. Full profiles are in `Chapter3_Source_Register_v2.md`, Section E.

**Why this table matters more than it looks:** the single largest execution risk in this entire project is the human relevance-label dataset. Everything downstream — the re-ranker, its evaluation, the academic claim that this is "more than an API wrapper" — depends on it existing at a credible scale. That is why Section 14 (anchor-partner strategy) is not a marketing nicety; it is the actual mechanism by which this dataset gets built at all, and the realistic 150–300 target above (rather than the 1,000+ aspirational figure) reflects what a 3-person team can plausibly source in a 6-month window through one real institutional relationship. The multilingual fine-tuning triples carry the same discipline for the same reason, at a smaller scale — Section 13.7 locks down exactly which sources are and are not legitimate for that dataset, because the temptation to shortcut data collection is highest on the smallest, most tedious dataset.

# 10. Project Pipeline & Workflow

This section describes how a request actually moves through the system, end to end, across every layer — not just what each AI feature does in isolation.

## 10.1 Live request pipeline (user-facing)

![Live request pipeline, step by step](diagrams/live_pipeline.png)

1. **Client (Next.js/React)** — user submits a form or message (idea text, CV upload, pitch transcript, a match request, a compliance question).
2. **API Gateway (FastAPI)** — authenticates the request (JWT), validates the payload against a Pydantic schema, and applies role-based authorization (e.g., only a founder can submit a startup idea; only an accepted match can reveal contact info).
3. **Task router** — determines which internal service the request belongs to: LLM Orchestration (open-ended generation: mentor feedback, market synthesis, pitch feedback, resume/LinkedIn optimization), Matching & Ranking Service (candidate retrieval), or RAG Compliance Service (grounded Q&A).
4. **Service execution:**
   - *LLM Orchestration* loads the relevant prompt template, injects structured context pulled from the database, and calls the LLM Gateway.
   - *Matching & Ranking* embeds the query profile (if not already embedded), retrieves top-K candidates via pgvector cosine similarity, computes structured compatibility features, and scores candidates with the trained re-ranker.
   - *RAG Compliance* embeds the question, retrieves the top-N relevant chunks from the indexed regulatory corpus, and passes only those chunks plus the question to the LLM Gateway with a "ground your answer only in the provided text" instruction.
5. **LLM Gateway** — the single choke point for every external model call: selects the provider/model, enforces token budgets and rate limits, logs the model/prompt version, and validates the output against the expected structured schema before it returns.
6. **Evidence & metadata persistence** — every AI output (a score, a match, a generated answer) is stored with its model/version identifier and, where applicable, its retrieved evidence or feature contributions — this is what lets the frontend show "why this match" without re-generating an explanation from scratch, and what makes the results auditable for evaluation later.
7. **Response formatting & return** — the API returns a structured JSON payload (not raw LLM text); the client renders it into the appropriate UI (a score breakdown, a ranked match list with explanation chips, a cited answer card).

## 10.2 Background / offline pipeline

Independent of any single user request, a set of scheduled and batch processes keep the system's intelligence current:

![Background/offline pipeline: ingestion, annotation, and re-ranker training](diagrams/offline_pipeline.png)

- **Document ingestion (Celery/cron):** whitelisted SECP/FBR/PSEB pages are periodically fetched, parsed (preserving headings/sections), chunked, embedded, and re-indexed into pgvector, with source URL and retrieval timestamp recorded on every chunk.
- **Firm-level data seeding (Playwright):** public, firm-level pages (VC portfolio pages, published partner/alumni lists) are scraped on a schedule to seed the initial investor/mentor directory — never individual personal profiles.
- **Annotation collection:** the human relevance-judgment dataset (Section 9) is collected through a small internal annotation tool, not live user traffic, and stored separately from production interaction data to avoid leakage between training and evaluation.
- **Re-ranker training (batch, not real-time):** on a fixed cadence (not per-request), the matching re-ranker is retrained on the accumulated labeled pairs, evaluated against the cosine-similarity baseline on a held-out split, and only promoted to production if it doesn't regress.
- **Embedding regeneration:** whenever a profile is edited, or the embedding model itself changes, affected embeddings are regenerated in the background rather than blocking the user's request.

## 10.3 Why this two-pipeline separation matters

Splitting the "live request" path from the "background intelligence-building" path is what makes the matching model's evaluation meaningful: the re-ranker is trained and validated offline, on a held-out set, before it ever touches a live request — so a demo match is never the first time that model version has been tested. It also keeps user-facing latency low, since embedding regeneration and document re-indexing never happen synchronously inside a request.

# 11. System Architecture

![System architecture — frontend, backend services, AI/ML layer, and data layer](diagrams/architecture.png)

## 11.1 Frontend design

Built in **Next.js/React**, organized around role-specific experiences rather than one generic dashboard, because a founder, a job-seeker, and an investor need almost entirely different information on their home screen.

- **Founder experience:** onboarding/profile creation → readiness dashboard (dimension-level score breakdown with concrete gap callouts, not just a number) → pitch-practice interface (a turn-by-turn chat-style UI with a visible rubric and post-session written feedback) → market-research report view (clearly separating "evidence found" from "model interpretation," per Section 13.3) → match feed with explanation chips ("strong sector fit, high skill overlap, compatible stage") → mutual-acceptance request flow → optional job/internship posting.
- **Talent experience:** profile creation with CV/LinkedIn text import → resume/LinkedIn optimizer (a before/after diff-style editor, not just a wall of suggestions) → job/internship board with filters (sector, stage, remote/on-site, city) → match feed for mentor guidance.
- **Mentor experience:** expertise/availability profile setup → ranked founder and talent feed (matched on expertise fit, Section 13.5) → match request accept/decline → (post-acceptance) contact details revealed.
- **Investor experience:** investment thesis/stage profile setup → ranked founder feed, limited to verified startups with a completed readiness assessment (FR-10) → match request accept/decline → (post-acceptance) contact details revealed.
- **Admin console:** the hybrid verification queue (Section 13.8) — ambiguous cases and appeals escalated for human approve/reject, reported-profile re-review, job-listing review, regulatory-corpus freshness status.
- **Help & usage guides:** short, team-authored "how this works" pages available from every dashboard — what a readiness score means, how matching and the "Verified" badge work, how to use the pitch simulator — plus the visible profile-review status (pending/verified/rejected) described in Section 13.8, so a user is never left guessing why they can't see something yet.
- **Design constraints specific to Pakistan's user base:** mobile-responsive by default (low/mid-tier smartphone usage is common), compressed assets and lazy-loaded content (data-cost sensitivity, patchy connectivity), and plain-language UI copy in English by default with Urdu/Roman Urdu available in AI-generated content — the UI chrome itself stays simple rather than requiring full interface translation, which is a separate and much larger effort than translating AI outputs.

## 11.2 Backend design

Built in **Python + FastAPI**, structured as modular internal services behind one API gateway rather than a single monolith, so the matching model, the RAG pipeline, and ordinary CRUD logic can be tested, evaluated, and replaced independently.

- **Auth service:** registration, login, JWT issuance, role assignment (founder / talent / mentor / investor / admin).
- **Profile service:** CRUD for all four user types' structured profiles, including the free-text-to-structured-attribute normalization step (Section 13 — Resume/LinkedIn Optimizer and Profile Normalization).
- **Startup Intelligence service:** readiness scoring, pitch-practice session management, market-research synthesis requests.
- **Matching & Ranking service:** embedding generation calls, candidate retrieval, re-ranker inference, mutual-acceptance state machine.
- **RAG Compliance service:** document ingestion pipeline, retrieval, grounded-generation orchestration.
- **LLM Gateway service:** the single internal interface every other service calls for any LLM completion — never called directly by the frontend, and never called ad hoc by another service.
- **Admin/Moderation service:** the human-in-the-loop profile review queue (Section 13.8) — approve/reject with logged reason, appeal decisions, verification status changes, reported-profile re-review, content takedown.
- **Database:** **PostgreSQL** as the system of record for all relational data, with the **pgvector** extension storing embeddings in the same database rather than standing up a separate vector store — simpler operationally, and sufficient at the FYP's data scale.

![Simplified database schema — key entities and relationships](diagrams/db_schema.png)

*Simplified for readability — shown are the entities that matter for understanding the system, not a complete column-level schema; join tables and minor lookup entities are omitted.*

- **Background jobs:** **Celery** (with Redis as the broker) handles the offline pipeline described in Section 10.2 — document ingestion, embedding regeneration, scheduled scraping, and batch re-ranker training.

## 11.3 AI/ML design

This is the layer that answers "what is actually trained here, versus what is just a well-grounded LLM call" — a distinction the document keeps explicit throughout, because conflating the two is the fastest way to lose credibility in front of a panel.

- **Embeddings:** a multilingual sentence-embedding model from the sentence-transformers family (candidates: LaBSE, paraphrase-multilingual-mpnet-base-v2, multilingual-e5), chosen and validated specifically against the multilingual baseline benchmark (Section 13.7) rather than assumed to work out of the box — Roman Urdu embedding quality is a genuinely open research problem, not a solved one, and the model choice is made after testing, not before. Used off-the-shelf, pretrained, in Phase 1 by default; contrastive/triplet fine-tuning on the team's own labeled data is a scoped stretch goal (Section 13.7), attempted only if a labeled-triple threshold is met by a fixed checkpoint — not committed as a guaranteed deliverable.
- **Matching re-ranker — the core trained model in this system, guaranteed regardless of how other stretch goals land.** A lightweight, supervised ranking model (logistic regression or a gradient-boosted ranker, chosen by validation performance rather than complexity for its own sake) combining embedding similarity with structured compatibility features (sector fit, stage fit, skill overlap, geography, availability, ticket range where relevant). Trained on the human relevance-judgment dataset (Section 9), evaluated against a cosine-similarity-only baseline using NDCG@K and MRR on a held-out split. If the multilingual fine-tuning stretch goal (above) is also completed, it becomes a second trained artifact in the system — both are labeled explicitly as trained, everything else in this layer stays labeled prompted, so the distinction never blurs regardless of how many stretch goals land.
- **LLM Gateway:** a provider-agnostic abstraction, designed to sit in front of any provider's API without other services needing to know which one is behind it. Centralizes prompt templates (so a prompt is versioned and changed in one place, not scattered across services), enforces per-request token budgets and rate limits, validates that structured-output calls actually return valid schema-conforming JSON, logs model/provider/version on every call for evaluation traceability, and keeps a fallback-to-older-model retry path for when the primary model is unavailable. **Current provider (2026-09-10, see DECISIONS.md): Gemini 2.5 and below, via Google AI Studio's free tier.** This is a cost-driven choice for the FYP build, not a permanent architectural commitment, the gateway's provider-agnostic design means swapping to Claude, OpenAI, or a paid Gemini tier later is a configuration change, not a rework. If paid API access becomes necessary, the department has indicated it can help arrange this.
- **RAG pipeline:** ingestion (whitelist official sources only) → section-aware chunking (not arbitrary character windows) → embedding → pgvector retrieval → optional lexical re-ranking of retrieved passages → generation constrained to only the retrieved evidence → citation/source-metadata attachment → a validation pass checking that the answer doesn't make claims the retrieved passages don't support.
- **Everything else in this system is a prompted LLM call, not a trained model** — readiness scoring (a structured rubric prompt), pitch feedback (persona-driven multi-turn prompting against a fixed rubric), market-research synthesis (evidence-first prompting over retrieved sources), the resume/LinkedIn optimizer (prompted rewriting grounded in the parsed CV and, optionally, a target role), and the portfolio/product link consistency check in profile verification (Section 13.8, evidence-first prompting over one fetched page, the same retrieval-grounded pattern as market research synthesis). Stating this distinction explicitly in the proposal is what lets the team credibly answer "why isn't this just an LLM wrapper" — because it isn't hiding the fact that most features *are* LLM calls; it's being precise about which one isn't.

## 11.4 Integration — how the layers actually talk to each other

- The **frontend never calls an LLM provider or the matching/RAG services directly** — every request goes through the FastAPI gateway, which is also where API keys live server-side, never exposed to the client.
- The **backend is the only caller of the LLM Gateway**; the Matching service and RAG service are internal APIs consumed only by the backend's orchestration layer, not exposed publicly.
- **Auth propagates via JWT** issued at login and validated by gateway middleware on every request; role claims in the token are what gate investor visibility of verified startups with a completed readiness assessment and what enforce the mutual-acceptance contact-reveal rule.
- **AI outputs are never re-generated for display** — because every output is persisted with its evidence/feature metadata at generation time (Section 10.1, step 6), the frontend requesting "why was I matched with this mentor" is a database read, not a new LLM call, which keeps explanation-display fast and consistent between page loads.
- **Deployment integration:** Docker Compose runs all services plus Postgres and Redis together for local development; GitHub Actions runs lint/test on every pull request and builds/deploys on merge to main; the frontend deploys to Vercel and the backend/workers to Railway or Render; provider API keys and other secrets are injected via environment configuration, never committed to the repository or shipped to the client bundle.


# 12. Core AI Reasoning Engine — the shared pattern

The technical thesis of this project is that one reasoning pattern — **structured input in, structured decision out** — is reused across every AI-driven surface, rather than five unrelated AI features bolted together. Every surface follows the same three stages:

1. **Normalize** — raw user input (traction data, a CV, a pitch transcript, a stated need) is parsed into a structured schema.
2. **Reason** — the structured input goes to either the LLM Orchestration layer with a task-specific prompt template (open-ended feedback/generation), or the Matching/Ranking service (candidate retrieval and scoring).
3. **Ground & Return** — output is grounded wherever correctness matters (compliance answers via RAG with citations; matches via real stored profile data and logged feature contributions) and returned as a structured, displayable result — never raw, unstructured LLM text.

![Core AI reasoning engine: Normalize, Reason, Ground & Return, applied across every feature](diagrams/reasoning_pattern.png)

| Input | Output | Which stage carries the real ML contribution |
|---|---|---|
| Startup traction data | AI mentor feedback + readiness score | Prompted (rubric-grounded) |
| Startup idea / sector | AI market research synthesis | Prompted (evidence-grounded) |
| Pitch transcript | Investor role-play critique and score | Prompted (rubric-grounded) |
| CV / LinkedIn text | Resume & profile optimization suggestions | Prompted (extraction-grounded) |
| Founder/talent stated need | Ranked mentor, investor, or job matches | **Trained** (embedding + re-ranker) |
| Compliance question | Cited regulatory answer | Prompted (retrieval-grounded) |

# 13. Feature-by-Feature Deep Dive

## 13.1 Startup Readiness Score

**Problem it solves:** founders have no structured way to know where their idea is weak before pitching it to a real mentor or investor, and an unstructured "is this fundable?" question has no honest answer at FYP scale.

**Design:** the score is deliberately *not* a funding probability — there is no dataset connecting Pakistani founder submissions to actual funding outcomes, and claiming otherwise would be indefensible in a viva. Instead, it is an interpretable rubric across seven dimensions: problem clarity, market definition, differentiation, business-model coherence, traction, team, and scalability. Each dimension is scored 1–5 with a written justification, not just a number.

**Pipeline:** founder submits structured startup data → Normalize stage extracts/validates the seven-dimension inputs → a single well-engineered prompt implementing the rubric is sent through the LLM Gateway → the model returns a structured JSON object (per-dimension score + justification + suggested next action) → validated against the expected schema → persisted with model/version metadata → rendered as a gap-breakdown dashboard, not a bare number.

**What's trained vs. prompted:** entirely prompted. No custom model is trained for this feature — the "training" that matters here is prompt engineering plus calibration.

**Validation before full build:** before this feature is built into the product, a calibration spike runs first — 10–15 sample startup ideas (mix of strong and weak) scored by the LLM rubric and independently by 2–3 human reviewers (a professor, a senior, or the team acting as separate raters), checking Spearman correlation between the two. If the LLM scores don't track human judgment, the rubric gets redesigned before any UI is built around it.

**Evaluation:** correlation with expert ratings on a held-out sample; qualitative review of disagreements, not just the correlation number.

## 13.2 AI Pitch Simulator

**Problem it solves:** founders outside a cohort program get zero practice pitching to a skeptical, probing audience before it matters.

**Design:** the system role-plays a configurable investor persona (sector-aware, stage-aware) and conducts a multi-turn conversation — asking follow-up questions the way a real investor would, not just receiving a monologue. Session history is retained so a founder can track improvement across attempts.

**Pipeline:** founder starts a session with startup context loaded → LLM Orchestration maintains conversation state and generates persona-consistent follow-up questions against a fixed rubric (clarity, market understanding, defensibility of numbers, handling of pushback) → after the session, a structured feedback summary is generated, scored per rubric dimension → session and scores persisted for history/trend view.

**What's trained vs. prompted:** prompted, persona- and rubric-driven. No model is trained specifically for this feature.

**Evaluation:** qualitative review by real founders and mentors (from the validation-interview pool, Section 17) on whether the questions asked and feedback given match what a human mentor would actually flag — relevance rate and perceived usefulness, not just "does it sound plausible."

## 13.3 AI Market Research Synthesis

**Problem it solves:** founders need a rough competitive/market picture and have no easy, trustworthy way to get one without either paying for a report or letting an LLM invent numbers.

**Design:** explicitly evidence-first, not "generate a market report" on demand. The system distinguishes discovered evidence from model interpretation at all times, and when it cannot verify a market-size claim, it says the estimate is unavailable rather than presenting an invented number as fact.

**Pipeline:** founder submits idea/sector → live web search retrieves candidate sources → sources are stored with metadata (title, URL, retrieval date) → LLM Orchestration synthesizes only from retrieved evidence, with a hard instruction not to state unsupported quantitative claims → citations are attached inline → output is rendered with evidence clearly separated from interpretation.

**What's trained vs. prompted:** prompted, evidence-grounded generation over live search results — the same RAG discipline as the compliance assistant, applied to open web sources instead of a fixed regulatory corpus.

**Evaluation:** citation correctness and unsupported-claim rate on a manually reviewed test set of queries.

## 13.4 Resume & LinkedIn/X Profile Optimizer

**Problem it solves:** talent users, especially those newer to the job market, don't know how to present their experience compellingly for startup roles specifically (which value scrappiness and demonstrated ownership differently than large-company resumes do).

**Design:** a prompted rewriting assistant, grounded in the user's actual parsed CV/profile text and, optionally, a target role's description — not a generic "improve my resume" black box. This is also where the platform's CV-parsing/skill-extraction step (needed anyway for matching) gets direct product value, rather than existing purely as backend plumbing.

**Pipeline:** talent user uploads/pastes CV or LinkedIn/X text → Normalize stage extracts structured skills, experience, and preference attributes (the same extraction the matching engine consumes) → LLM Orchestration generates specific line-level rewrite suggestions, shown as a before/after diff rather than a wall of generic advice → user accepts/edits/rejects suggestions inline.

**What's trained vs. prompted:** entirely prompted. This is explicitly *not* a trained model — it's worth stating this plainly in the proposal, because it's the clearest example in the whole system of the trained-vs-prompted distinction: the extraction and rewriting are LLM calls with good prompting and real user data as grounding, not a research artifact.

**Evaluation:** qualitative user feedback (does the suggested rewrite genuinely read better, does it introduce factual errors about the person's actual experience) rather than a formal metric — this is a product-quality feature, not a research claim.

**Test inputs (decided 4 October 2026):** no suitable external resume dataset survived screening (one was image-only, one consistent with synthetic generation), so the optimizer is tested on the team's own resumes and on resumes shared with consent.

## 13.5 Ecosystem Matching & Re-Ranking Engine — the primary ML contribution

**Problem it solves:** founders, mentors, investors, and talent all need to find relevant counterparts, and simple keyword or popularity-based matching produces poor, unexplainable results at any real scale.

**Design:** a two-stage hybrid ranker, described in full architectural detail in Section 11.3. Stage one (candidate generation) prioritizes recall using embedding similarity plus hard filters (sector, stage, geography). Stage two (re-ranking) is the actual trained model, combining semantic similarity with structured compatibility features. This is the one component in the entire system that is genuinely trained, evaluated against a baseline, and where "why was I matched with this person" has a real, loggable answer (feature contributions), not a post-hoc LLM-invented explanation.

![Two-stage matching and re-ranking engine](diagrams/matching_engine.png)

**Pipeline:** profile created/updated → embedding generated (background job) → on a match request, top-K candidates retrieved via pgvector cosine similarity → structured features computed (sector_fit, stage_fit, skill_overlap, geography_fit, availability_fit, ticket_fit where relevant) → re-ranker scores and orders candidates → top results returned with the dominant match factors surfaced in the UI → request-to-connect flow gated by mutual acceptance before any contact info is revealed.

**Mentor expertise taxonomy — explicitly broader than fundraising.** A founder's needs change once they're past idea-stage (Section 8): a registered, revenue-generating startup often needs help with financial management, operations, or hiring/HR at least as much as pitch coaching. The mentor expertise tags feeding `sector_fit` are deliberately not fundraising-only — they include operational categories (financial management, operations, HR/team-building) alongside the usual product/growth/fundraising tags, so a founder past validation stage matches on what they actually need next, not just "startup mentor" generically. This is a data-modeling change to an existing feature, not a new subsystem — it costs a tag taxonomy update, nothing structural.

**A modest additional signal for talent matching specifically:** for candidates who link a public GitHub profile, basic API-level metadata — public repository count, commit recency, primary language mix — is pulled in as one more structured feature (`technical_activity_signal`), the same way sector or stage fit already are. This is deliberately scoped to metadata the GitHub API returns directly, not deep static-analysis of code quality or "structural complexity," which is a much larger research problem and not something this re-ranker attempts.

**What's trained vs. prompted:** trained. Explicitly not an LLM call — this is a supervised ranking model (logistic regression or a lightweight gradient-boosted ranker, chosen by validation performance) trained on the human relevance-judgment dataset described in Section 9.

**Evaluation:** NDCG@K and MRR against a cosine-similarity-only baseline on a held-out split of the labeled pairs; request-to-accept rate tracked in a pilot group as a secondary, real-world signal.

**Cold start:** for new users with no interaction history yet, ranking relies on semantic profile content and hard constraints alone; accept/decline signals are folded in as additional features only once enough real interactions exist — this is treated as a documented limitation, not silently assumed away.

## 13.6 Compliance Assistant (Regulatory RAG)

**Problem it solves:** founders need to know how to register a company, register for tax, and understand PSEB-related requirements, and generic LLM answers on this topic carry real hallucination risk with real consequences.

**Design:** answers only from an indexed, whitelisted corpus of official government sources (SECP, FBR, PSEB) — never from the model's general training knowledge. Every answer carries a source citation, a document date/version where available, and an explicit non-advisory disclaimer.

**Pipeline:** described fully in Section 10.2 (ingestion) and 11.3 (retrieval/generation). At query time: question embedded → top-N relevant chunks retrieved → LLM Gateway generates an answer constrained to only the retrieved text → citations attached → a validation check confirms the answer doesn't assert anything the retrieved passages don't support → if no confident grounded answer exists, the system says so rather than guessing.

**Corpus (fixed 4 October 2026):** Income Tax Ordinance 2001 (FBR consolidation amended up to 30 June 2026) and the Finance Act 2026; Companies Act 2017 (Parts I and IV and sections 462–473 only); SECP's Seventh Schedule with fees in effect from 20 April 2026; SECP Regulatory Sandbox Guidelines 2019 (eligibility, application and testing process only, with no advice on whether a product needs a licence); SECP's startup position paper (2024); FBR's 2018 VOSS circular, Register for Income Tax page, Registration of Individual on Iris guide (2019) and Iris FAQs (registration and e-enrolment answers only); and the PSEB Industry Facilitation page (registration documents, fees and renewal only, never tax). Every file was profiled for page count, version, text layer and SHA-256 hash, and web pages are kept as dated snapshots.

**Answer rules that follow from the corpus:** tax answers come only from the Ordinance and the Finance Act. Company NTN answers cite the 2018 VOSS circular with its date and note that FBR's web page still directs companies to a facilitation counter. Fee answers cite the Seventh Schedule and its effective date, because the schedule raises several fees by 10% each April; from about 20 April 2027 the assistant warns that a newer increase may apply.

**What's trained vs. prompted:** prompted, retrieval-grounded generation. The retrieval index itself (embeddings + chunking) is built via the same sentence-embedding model as the matching engine, but no model is *trained* specifically for this feature.

**Evaluation:** citation correctness and retrieval recall on a manually verified test question set; freshness auditing when source documents change. The test set includes questions that probe the known conflicts and date dependencies above, and out-of-scope questions the assistant should decline.

## 13.7 Multilingual Support (English, Urdu, Roman Urdu)

**Problem it solves:** every audited competitor is English-only, but a meaningful share of Pakistani founders and talent are more comfortable expressing ideas, pitches, and questions in Urdu or Roman Urdu.

**Design and honest framing:** this is treated as an evaluated research dimension, not a marketing claim — and for good reason. Roman Urdu has no standard orthography and frequent English code-switching, and current research confirms this remains a genuinely open, underexplored problem for multilingual language models generally (not a solved, off-the-shelf capability). The project does not assume equal performance across the three languages; it measures it.

![Multilingual baseline benchmark, Month 4 go/no-go checkpoint, and the conditional fine-tuning stretch goal](diagrams/multilingual_finetuning.png)

**Pipeline / validation approach — Step 1: baseline benchmark (committed).** Before the matching pipeline is built around an assumed multilingual capability, this benchmark runs first — roughly 30–50 short profile/idea descriptions per language, expressing the same underlying meaning in English, Urdu script, and Roman Urdu, embedded with an off-the-shelf pretrained multilingual model (candidates: LaBSE, paraphrase-multilingual-mpnet-base-v2, multilingual-e5 — final pick after checking each one's actual Urdu-language coverage, not assumed) and checked by cosine similarity: do same-meaning cross-language pairs cluster together, and do genuinely different ideas stay apart? The same benchmark approach (retrieval relevance, answer faithfulness, citation correctness via RAGAS) is then applied per language for the RAG and matching pipelines specifically, rather than claimed as a blanket capability. This step is guaranteed regardless of what follows — it requires no special data collection beyond what the team writes itself, and produces a real, quantified finding either way (Roman Urdu underperforming the other two would itself be a legitimate, reportable result, not a failure).

**Step 2: fine-tuning (stretch goal, contingent on data).** If the baseline shows a meaningful gap — most likely in Roman Urdu, given its lack of standard orthography and frequent English code-switching — the follow-up is to fine-tune the chosen embedding model on the team's own labeled data, rather than only reporting the gap. This uses **contrastive/triplet learning**, the standard technique behind the sentence-transformers ecosystem: the model is trained on triples of (anchor profile, a genuinely good match, a genuinely bad match) so that embeddings of real matches move closer together and non-matches move further apart. A single university-provided GPU is sufficient for this — fine-tuning a sentence-embedding model on a dataset of hundreds-to-low-thousands of triples is realistically an hours-to-a-day job, so **compute is not the constraint here; labeled data is.** A held-out test set is set aside before any training happens, so the before/after comparison stays honest.

**Data sourcing rules for the fine-tuning triples (locked, no exceptions).** Only the following are used to build (anchor, positive, negative) triples:

1. **Publicly available structured datasets** already being sourced for the project (Section 9).
2. **Consented pilot-user data** — real founders/mentors/talent (classmates, FAST incubator contacts, early pilot users) who explicitly agree, via a short written consent statement, that their profile data can be used for training/evaluation.
3. **Manually authored profiles** — the team writes realistic founder/mentor/talent profiles across all three languages and manually assigns match/no-match labels.
4. **LLM-assisted synthetic generation** — an LLM helps generate realistic profile variations faster, clearly labeled as synthetic, with match/no-match labels still assigned by the team, not the LLM.

**Explicitly excluded, no exceptions:** scraping or collecting data from WhatsApp, Facebook, Instagram, Reddit, or any public profiles/comment sections without direct, explicit consent. This is not a data-quality preference — WhatsApp content is private communication between people who never consented to being training data (a PECA concern); Facebook/Instagram scraping directly contradicts this project's own locked scope decision of self-registration only (Section 6.2, Section 18.2) and breaches platform Terms of Service regardless of Pakistani law; Reddit restricted bulk scraping under its 2023 API terms, and even where technically accessible, none of these sources produce the labeled (anchor, positive, negative) pairs the task actually needs — unlabeled scraped text does not solve the data problem even before the legal/ethical issues are considered.

**Execution guardrails:**

- **Consent, in writing.** Pilot-user consent is a short written statement, not a verbal "sure" — what's collected, that it's used for training/evaluation, that it's anonymized before use. Whether FAST requires any formal ethics sign-off for collecting data from real people at this scale is confirmed with the supervisor rather than assumed.
- **A minimum triple threshold, set in advance.** Fine-tuning is only attempted if a pre-agreed minimum triple count per language is met — a dataset too small to fine-tune on meaningfully risks overfitting or showing no real improvement over baseline, which would undercut the research story rather than strengthen it. The exact number is set once real collection rates are known, not guessed upfront.
- **Labeling consistency.** At least a subset of triples is independently double-labeled by two team members, with agreement checked — a defensible answer to "who decided this was a good match" beats a single person's unverified judgment call.
- **A hard checkpoint, not an open-ended stretch goal.** By the end of Month 4 (Section 22), the team reviews how much legitimately-sourced labeled data actually exists and makes an explicit go/no-go call on fine-tuning, rather than letting it drift into crunch time. If the threshold isn't met, the baseline-only story ships cleanly.
- **Storage and anonymization.** Consented pilot data is anonymized/pseudonymized before use in training and given a defined storage location — not left in a shared folder in raw form.

**What's trained vs. prompted:** the embedding model is pre-trained and off-the-shelf by default (not trained from scratch by the team); fine-tuning it on the team's own labeled data (Step 2, above) is a genuine but conditional trained artifact — attempted only if the data threshold is met, and reported as a stretch goal, not promised as committed. Language handling elsewhere (generation, normalization) is prompted, with conservative Roman Urdu normalization to avoid altering names, technical terms, or intended meaning.

**Evaluation:** a benchmark measuring retrieval relevance, answer faithfulness, and citation correctness independently for English, Urdu, and Roman Urdu, on the off-the-shelf baseline model — with results reported honestly even if Roman Urdu underperforms, rather than an assumed-equal claim. If fine-tuning is attempted, the same benchmark is re-run on the fine-tuned model and directly compared against the baseline, per language — that comparison, not the fact that fine-tuning happened, is the actual research output.

## 13.8 Trust & Verification: Hybrid Automated + Human-in-the-Loop Profile Review

**Problem it solves:** fake, low-effort, or bot-generated profiles degrade match quality and, if they slip through, undermine every trust claim The Founder's Carnet makes to founders, mentors, and investors. Fully manual review of every profile also doesn't scale a three-person team's time well, and this is still a data problem in the other direction: at FYP scale, there simply aren't enough confirmed fraud/fake-profile examples to safely train a full legitimacy classifier — an automated gate that decides everything on its own would be guessing, not detecting.

**Design:** every profile is scored automatically at submission time on a small set of signals already collected elsewhere in the system — LinkedIn OAuth verification (pass/fail), SECP registration ID cross-check where applicable (pass/fail, FR-12), profile completeness, for talent the optional GitHub activity signal (FR-13), and for founders and investors the optional portfolio/product link signal described below (FR-20). This produces an **authored, rule-based score for most signals — not a trained model**, with one deliberately-flagged prompted exception (below). The distinction matters and is kept explicit the same way trained-vs-prompted is kept explicit elsewhere (Section 11.3): nothing here is learned from labeled data, because a confirmed fraud/genuine dataset doesn't exist yet to learn from safely. The team sets and documents the weights and thresholds through reasoning about the signals, not through training.

- **High score → auto-verified instantly.** "Verified" badge granted with no human step in the loop.
- **Low score → auto-rejected instantly.** Reason logged and visible to the user, same as a human rejection would show. The user can appeal once with additional evidence, and the appeal goes to human review (below).
- **Ambiguous middle band → escalated to human review** (Admin/Moderation service, Section 11.2) — the same review queue from earlier drafts of this design, now handling only the cases the authored rule can't confidently resolve, plus appeals from auto-rejected users, not every profile.

This keeps the human-in-the-loop role from the original design intact rather than removing it — Section 8's Admin stakeholder still exists and still matters — it's just scoped down to the minority of ambiguous cases, which is a more realistic use of a three-person team's time than reviewing every single profile by hand.

**A fifth signal, specific to founders and investors — personal portfolio and product links (optional).** Founders seeking investment typically have *something* publicly visible by that point — a live product, a landing page, a demo, or at minimum a build-in-public presence for earlier-stage teams — and investors typically have a public track record of their own (a personal site, an AngelList/Wellfound or Crunchbase investor profile, a firm page). Both may optionally provide these links during profile creation, which become one more input to the same automated score above, not a separate pipeline:

- **Authored check (rule-based):** does the link resolve, and is there substantive content behind it (not a blank or parked page)? Pass/fail, treated the same as the OAuth/SECP checks.
- **Prompted check (LLM-based):** the fetched page content is compared against what the person already entered in their profile (sector, stage, and traction description for founders; thesis and stage focus for investors), and the LLM returns a structured label — *consistent*, *inconsistent*, or *not enough content to judge* — rather than a free-text opinion. This is the one prompted LLM sub-component inside an otherwise authored, rule-based scoring system, and it's flagged as such explicitly (see "What's trained vs. prompted vs. authored" below) rather than left to blend invisibly into "the algorithm."

**Where this does and doesn't apply — kept consistent with FR-12's own boundary.** LinkedIn is explicitly excluded from direct link-fetching: LinkedIn's own Terms of Service prohibit automated access to profile pages regardless of whether the profile is public or the owner consents, so only the fields already returned through the OAuth handshake (name, headline, current role) are used, matched against what the person typed into the form — never a raw fetch of a linkedin.com URL. For other public profile sources (e.g., AngelList/Wellfound, Crunchbase, Product Hunt), an official API is used where one exists, rather than direct scraping; personal websites and product/build-in-public pages are fetched directly, since the person supplied that link themselves and controls that content.

**Optional, not mandatory.** A founder in the earliest building stage may not have anything public yet, and that's a legitimate state, not a red flag — not providing a link simply means one fewer signal feeding the score, which naturally pushes an otherwise-thin profile toward the ambiguous band and a human look, rather than penalizing it outright.

![Hybrid profile verification pipeline: automated signal scoring with human escalation for ambiguous cases](diagrams/profile_review_pipeline.png)

**Pipeline:**

1. User registers and submits a profile, completing the LinkedIn OAuth handshake or SECP ID cross-check where applicable (FR-12).
2. The system computes an automated signal score from the collected verification signals.
3. Score above the auto-verify threshold → "Verified" badge granted immediately, visible to other users.
4. Score below the auto-reject threshold → rejected immediately, reason logged, visible to the user, who may submit one appeal with additional evidence; the appeal enters the human review queue described in step 5.
5. Score in the ambiguous middle band → enters the human review queue (Admin/Moderation service); reviewer approves or rejects with a short logged reason, same mechanism as before. The same queue handles appeals, and the reviewer's decision on an appeal is final.
6. The user can see their own status at any time — auto-verified, auto-rejected, pending human review (including a pending appeal), or reviewed — rather than silence while waiting.
7. A profile that's later reported or blocked (Section 19) re-enters human review specifically (not automatic re-scoring), since a report is itself a signal the automated score never had.

**Execution guardrails, mirroring the same staged-rollout discipline used for the multilingual fine-tuning checkpoint (Section 13.7):**

- **Start conservative.** A narrow auto-verify band and a narrow auto-reject band, with a deliberately wide ambiguous/human-review band at launch — biasing errors toward sending more borderline cases to a human, not fewer, rather than optimizing for less manual work too early. The bands are only tightened later, once real behavior has been observed.
- **Every decision is logged the same way, auto or human.** The exact signal values and score that produced an auto-decision are stored alongside it, so "why was I auto-verified or auto-rejected" has a real, inspectable answer — consistent with this document's "checkable, not asserted" theme (Section 1.1).
- **Thresholds are documented and revisited manually**, not retrained — there's no training loop here to accidentally drift on its own.

**Consent and framing shown to the user:** registration explicitly states that profiles are checked — automatically where the signals are clear, by a person where they're not — and why; this is framed to users as a trust signal ("most profiles are verified instantly on strong signals; anything unclear gets a real second look"), not just a delay. Full notice text in Section 18.4–18.5.

**What's trained vs. prompted vs. authored:** none of this is a trained model. Most of it — the OAuth, SECP, completeness, and GitHub checks — is authored, rule-based logic, a third category kept as explicit as the other two used elsewhere in this document. The one exception is the portfolio/product link consistency check above, which is a **prompted LLM call** (grounded in retrieved page content, the same pattern as market research synthesis in Section 13.3) feeding into the otherwise-authored score as a single structured input — flagged explicitly here rather than left to blend into "the algorithm." Human judgment is retained specifically for the cases the combined score can't confidently resolve. **Phase 2 (Potential Business, Section 23):** if enough consented decision data accumulates post-graduation — both auto-decisions and human decisions, each already logged with its signals — a genuinely trained legitimacy-scoring model becomes a realistic next step, replacing the authored rule with a learned one. Still explicitly conditional on real usage first, not promised as an FYP deliverable, for the same reason the matching re-ranker's training data had to be sourced through an anchor partner rather than assumed to exist.

**Evaluation (Phase 1):** the proportion of profiles auto-verified vs. auto-rejected vs. escalated to human review (expected to skew heavily toward escalation at launch, narrowing as thresholds are tuned on observed behavior); review turnaround time for the escalated subset; qualitative spot-checks of both the automated decisions and the human ones, rather than a formal precision/recall metric, since confirmed ground truth on fraud is still too thin at this scale to compute one honestly.

# 14. Tech Stack

![Tech stack by layer, from frontend to deployment](diagrams/tech_stack.png)

| Layer | Choice | Why |
|---|---|---|
| Frontend | React / Next.js (TypeScript) on Node.js 24 | Standard, well-documented, team has existing familiarity |
| Backend | Python + FastAPI | Async-friendly, strong typing via Pydantic, natural fit for an AI-heavy backend |
| Database | PostgreSQL + pgvector | Relational data and embeddings in one store — avoids standing up a separate vector database at this scale |
| LLM reasoning | Gemini 2.5 and below (Google AI Studio free tier) currently, behind an internal gateway | Free-tier access at no cost for the FYP build; provider-agnostic gateway design means swapping to Claude/OpenAI or a paid tier later is a configuration change, not a rework |
| Matching / ranking | sentence-transformers (embeddings) + scikit-learn or a gradient-boosting library (re-ranker) | Lightweight, appropriate to the realistic data scale — not a full neural cross-encoder that would overfit on a few hundred labeled pairs |
| Retrieval (RAG) | Chunking + embedding pipeline over indexed SECP/FBR/PSEB documents, stored in pgvector | Reuses the same embedding infrastructure as matching |
| Background jobs | Celery + Redis | Handles ingestion, embedding regeneration, scheduled scraping, batch re-ranker training |
| Scraping (firm-level, public data only) | Playwright | Seeds the initial investor/mentor directory from public portfolio/partner pages |
| Containerization | Docker Compose | Justified by the genuinely multi-service architecture — matching, RAG, and LLM orchestration as independent, testable services |
| Deployment | Vercel (frontend), Railway or Render (backend + workers) | Free/low-cost tiers sufficient for FYP-scale demo traffic |
| CI/CD | GitHub Actions | Lint/test on pull request, build/deploy on merge to main |

# 15. User Workflows

## 15.1 Founder

![Founder journey, from registration to being investor-visible](diagrams/founder_journey.png)

1. Register and create a startup profile (traction, ask, sector, team).
2. Receive an AI-generated readiness score with a dimension-level gap breakdown — available immediately, independent of review status, since it doesn't expose the founder to anyone else.
3. Use AI mentor feedback and pitch practice to address identified gaps.
4. Once verified (auto or human, Section 13.8) and with a completed readiness assessment, become visible to registered investors and request mentor matches. The score itself is shown as information and is not used as a cutoff. The founder can see their own verification status at any time rather than waiting in silence.
5. Optionally post a job/internship listing, visible on the talent board.

## 15.2 Talent

![Talent journey, from profile creation to applying](diagrams/talent_journey.png)

1. Register and create a profile; upload or paste a CV and LinkedIn/X profile text — optionally linking a public GitHub profile, which feeds the modest technical-activity signal described in Section 13.5. Profile is scored and, if ambiguous, enters human review (Section 13.8) at this point.
2. Receive AI-generated resume and profile optimization suggestions — available immediately, independent of review status, since it doesn't expose the user to anyone else.
3. Once verified (auto or human), browse the curated startup job/internship board.
4. Apply directly to listings.
5. Optionally request a mentor match for career guidance.

## 15.3 Mentor

![Mentor journey, from verification to introduction](diagrams/mentor_journey.png)

1. Self-register with expertise/sector focus and availability, completing a LinkedIn OAuth handshake or SECP registration ID cross-check (FR-12) as one signal feeding into automated verification, escalated to human review only if ambiguous (Section 13.8), which gates the "Verified" badge and visibility.
2. Matched to founders and talent by the ranking service on expertise fit, including the operational mentorship categories beyond fundraising described in Section 13.5.
3. Send or receive a match request; the other party accepts or declines — identity is shared only on acceptance.
4. Provide mentorship guidance off-platform — the Carnet's role ends at the introduction.

## 15.4 Investor

![Investor journey, from verification to introduction](diagrams/investor_journey.png)

1. Self-register with investment thesis and stage focus, completing a LinkedIn OAuth handshake or SECP registration ID cross-check (FR-12) as one signal feeding into automated verification, escalated to human review only if ambiguous (Section 13.8), which gates the "Verified" badge and visibility to founders.
2. Browse startups with a verified profile and a completed readiness assessment (FR-10); matched to founders by the ranking service.
3. Send a match request; the founder accepts or declines — identity is shared only on acceptance.
4. Any resulting meeting or investment happens off-platform, through normal channels — the Carnet's role ends at the introduction (Section 18.1).

## 15.5 Compliance query (any founder)

![Compliance query workflow, including the no-guessing fallback](diagrams/compliance_journey.png)

1. Ask a question about business registration, tax registration, or PSEB requirements, in English, Urdu, or Roman Urdu.
2. System retrieves relevant passages from the indexed official-source corpus.
3. A grounded answer is generated, with source citations and document date/version shown.
4. If no confident grounded answer exists, the system says so explicitly rather than guessing.


# 16. Requirements

## 16.1 List of Features

- Founder readiness/fundability scoring with dimension-level gap breakdown
- AI-simulated investor pitch practice with multi-turn conversation and scored feedback
- AI market research synthesis, evidence-first and citation-backed
- Talent resume and LinkedIn/X profile optimization (before/after diff)
- Curated, startup-specific job/internship board
- Embedding-based ecosystem matching with a trained re-ranker (founder–mentor, founder–investor, startup–talent), mutual-acceptance contact reveal
- RAG-based compliance assistant grounded in SECP/FBR/PSEB documentation, with mandatory citations
- English, Urdu, and Roman Urdu support in AI-generated conversational output, benchmarked per language
- Human-in-the-loop profile review and "Verified" badge for all five stakeholder types
- Curated external resource links (SAFE templates, incorporation checklists)
- Ecosystem events calendar (cross-listed, not self-hosted)
- In-platform usage guides for each stakeholder type

## 16.2 Functional Requirements

| ID | Requirement | Module |
|---|---|---|
| FR-1 | Founders can create a profile and submit structured traction/business data. | Founder |
| FR-2 | System generates AI mentor feedback and a dimension-level readiness score from submitted founder data. | Founder / Core Engine |
| FR-3 | System simulates a multi-turn investor pitch session, scoring clarity, market understanding, defensibility of numbers, and handling of pushback, with session history retained. | Founder / Core Engine |
| FR-4 | System generates a market research summary (competitors, rough sizing) using live web search, clearly separating evidence from interpretation. | Founder / Core Engine |
| FR-5 | Talent users can upload/enter a CV and LinkedIn/X profile text and receive AI-generated optimization suggestions. | Talent |
| FR-6 | System displays a curated, filterable list of startup jobs/internships. | Talent |
| FR-7 | System matches founders/talent to mentors and investors using embedding similarity plus a trained re-ranker; contact identity revealed only after mutual acceptance. | Matching Service |
| FR-8 | System answers founder compliance questions using retrieval-grounded generation over indexed SECP/FBR/PSEB documents, with source citations. | Compliance Service |
| FR-9 | System supports English, Urdu, and Roman Urdu in AI-generated conversational responses, with per-language quality benchmarked. | Core Engine |
| FR-10 | System limits investor visibility to startup profiles that are verified and have a completed readiness assessment. The readiness score is shown as information and is not used as a cutoff. | Investor Discovery |
| FR-11 | Startups are charged a placement fee only upon confirmed hire of a candidate sourced through the job board; no fee is charged for browsing, posting, or unsuccessful searches. | Billing |
| FR-12 | Mentor and investor profiles complete a LinkedIn OAuth handshake or SECP registration ID cross-check before receiving a "Verified" badge and becoming visible to founders. | Auth / Trust |
| FR-13 | Talent profiles may optionally link a public GitHub profile; if linked, basic API-level metadata (repo count, commit recency, language mix) is included as one structured feature in the re-ranker. | Matching Service |
| FR-14 | Every new profile (founder, talent, mentor, investor) is scored automatically against a defined signal threshold at submission; profiles clearing the auto-verify threshold become visible immediately, profiles at or below the auto-reject threshold are rejected immediately, and profiles in the ambiguous band are held in a human review queue until a reviewer approves or rejects them; all rejections (auto or human) carry a logged reason visible to the user, and an auto-rejected user may appeal once (FR-21). | Admin / Trust |
| FR-15 | Users can view their own profile's review status at any time (auto-verified / auto-rejected / pending human review / appeal pending / verified / rejected, with reason). | Admin / Trust |
| FR-16 | Reported or blocked profiles (Section 19) re-enter human review specifically (not automatic re-scoring), rather than a separate undefined moderation path. | Admin / Trust |
| FR-17 | At registration, before any profile data is submitted, users are shown a consent and data notice (Section 18.4) and a short trust note explaining hybrid verification (Section 18.5), and must actively accept before proceeding. | Auth / Trust |
| FR-18 | Team-authored usage guides ("how this works" pages) are accessible from every dashboard for all user types. | Frontend |
| FR-19 | The system computes an automated verification score from collected signals (LinkedIn OAuth pass/fail, SECP ID cross-check pass/fail where applicable, profile completeness, and GitHub activity for talent per FR-13); the score, the signal values behind it, and the threshold band it fell into are logged for every profile, whether the outcome was auto-decided or human-decided. | Admin / Trust |
| FR-20 | Founder and investor profiles may optionally provide a personal portfolio/profile link and, for founders, a product or public build-in-public link; if provided, the system checks the link resolves with substantive content (authored signal) and runs a prompted LLM consistency check against the profile's own claims (consistent / inconsistent / insufficient content), both feeding into the verification score (FR-19). LinkedIn URLs are never fetched directly — only OAuth-returned fields are used (FR-12). | Admin / Trust |
| FR-21 | A user whose profile is auto-rejected may submit one appeal with additional evidence; the appeal enters the human review queue, and the reviewer's decision, with a logged reason, is final and visible to the user. | Admin / Trust |

## 16.3 Non-Functional Requirements

| Category | Requirement |
|---|---|
| Performance | AI mentor/readiness responses return within acceptable interactive latency (target: under ~8 seconds for a typical LLM call); matching queries return within ~2 seconds at demo scale. |
| Security | Passwords hashed and salted; authenticated API endpoints (JWT); investor/mentor contact details never exposed until an explicit mutual-accept event; uploaded files validated and scanned. |
| Scalability | Stateless API layer with separated matching/RAG services should scale horizontally without redesign, though the FYP demo targets a small seeded dataset, not production load. |
| Usability | Core flows (submit profile → get feedback → request a match) completable without external instructions. |
| Data Privacy | Personal data collected via opt-in self-registration only, never scraped, and only after explicit consent (FR-17); firm-level/business data sourced from published public sources with attribution; users can request deletion of their data on demand, not just in principle (see also Section 19). |
| Reliability of AI output | RAG compliance answers must cite retrieved passages; the system must clearly flag when it cannot find a grounded answer rather than guessing. |
| Explainability | Match and score outputs persist feature contributions or retrieved evidence so explanations can be displayed without re-generation. |

# 17. Evaluation Plan

Deliberately trimmed from an earlier, far more ambitious version of this plan — which called for 11 formal experiments, a 1,000+-label dataset, full bias/fairness audits, and three-way model comparisons across every module. That version would be a strong basis for a research lab's multi-year agenda; it is not buildable by three people in six months alongside a full-stack product. What follows is the realistic core, with everything else explicitly marked as stretch.

| Feature | Evaluation approach | Priority |
|---|---|---|
| Matching / re-ranking engine | Trained re-ranker vs. cosine-similarity baseline, NDCG@K and MRR on a held-out split of the labeled pairs; request-to-accept rate in a pilot group as a secondary real-world signal. | **Core** — this is the primary ML claim in the whole project and must not be cut. |
| Compliance RAG | Citation correctness and groundedness on a manually verified test question set. | **Core** |
| Readiness score | Correlation (Spearman) between LLM-rubric scores and human expert ratings on a held-out sample; qualitative review of disagreements. | **Core** |
| Multilingual (English/Urdu/Roman Urdu) — baseline | Retrieval relevance, answer faithfulness, and citation correctness benchmarked per language, on the off-the-shelf embedding model, scoped to the matching and RAG pipelines specifically — not every module across all three languages. | **Deferred to FYP-2** — not attempted in FYP-1 (see DECISIONS.md, 2026-09-10). English-only for the RAG build this semester, given the team's limited hands-on RAG experience (Section 6.3) and the genuinely open nature of Roman Urdu normalization (Section 13.7). Revisit as a committed, narrowly-scoped benchmark once the FYP-1 build is stable. |
| Multilingual — fine-tuned vs. baseline comparison | Same benchmark re-run on a model fine-tuned (contrastive/triplet) on the team's own labeled data (Section 13.7); reported as a before/after comparison per language. | **Stretch** — attempted only if the Month 4 go/no-go data-threshold check (Section 13.7, Section 22) is met. |
| Pitch simulation | Qualitative review by real founders/mentors: does AI feedback match what a human mentor would flag. | Secondary |
| Market synthesis | Citation correctness and unsupported-claim rate on a test set. | Secondary |
| Resume/LinkedIn optimizer | Qualitative user feedback on suggestion quality and factual accuracy. | Secondary, product-quality claim, not a research claim |
| Bias/fairness audit across ranking | Deferred to Phase 2/future work unless time allows — noted as a limitation, not silently ignored. | Stretch |
| Full 3-way model comparison (logistic vs. gradient-boosted vs. neural re-ranker) | One re-ranker architecture is chosen and justified upfront based on the realistic label-count scale; comparison against a fancier architecture is future work. | Stretch |

**Overall product-problem-fit validation:** structured interviews with 10–15 early-stage founders and 10–15 startup job/internship seekers, conducted early in the build, to validate which bundled feature matters most and catch any mismatch between the assumed and actual problem before too much has been built around an assumption.

**FYP-1 execution note (2026-09-10):** the matching engine keeps its status above as the project's primary ML contribution, that does not change. What changes is build order for FYP-1 specifically: the compliance RAG assistant is the one component actually built and tested for this semester's Implementation and Test Cases chapter, since it carries no anchor-partner data dependency and is fully testable now, while the matching engine's training data remains gated on the anchor-partner relationship (Section 9, Section 20) landing. The matching engine's own build and evaluation move to FYP-2. See DECISIONS.md for the dated record of this call, and note this reverses the fallback order in Section 22, which still lists the matching engine ahead of RAG.

# 18. Legal, Regulatory & Ethical Considerations

## 18.1 Securities / brokerage regulation

Facilitating actual investment deals — holding funds, structuring securities, or taking equity as an intermediary — is a licensed activity in Pakistan requiring broker-dealer or financial-intermediary status under SECP's securities framework. **Regulatory naming correction:** an earlier draft of this document cited this as governed by "SECP's Equity-Based Crowdfunding Regulations, 2019" — that name does not check out against any regulation SECP has actually published. The specific mechanism SECP has used to let a fintech-adjacent product test crowdfunding-type activity is the **Regulatory Sandbox Guidelines, 2019**, under which SECP has granted one crowdfunding platform time-boxed approval to operate under direct regulatory supervision, including formal due diligence on issuers. This project deliberately avoids that classification entirely: no transaction, fee-on-investment, or security is ever executed, tracked, or mediated on-platform, and the Carnet's involvement in any investor–startup relationship ends at a mutually-accepted introduction. The Carnet never enters the Sandbox and doesn't need to, precisely because an introduction-only service that never touches funds or securities does not meet the threshold for broker-dealer or financial-intermediary classification in the first place — a stronger, more specific claim than "we're not a crowdfunding platform." This is why the earlier equity-based / deal-close-fee version of the business model was replaced with flat subscriptions and a talent-hiring placement fee (Section 7) — the platform's regulatory footprint is comparable to a job board or professional directory, not a financial intermediary.

## 18.2 Data protection

Individual personal data (mentors, investors, talent) is collected exclusively via opt-in self-registration, never scraping, in line with Pakistan's Prevention of Electronic Crimes Act (PECA). Only publicly published, firm-level/commercial data (e.g., a VC firm's own portfolio page) is considered for automated sourcing.

## 18.3 Ethical considerations

- **Algorithmic fairness:** readiness-scoring and matching models make judgments about real people's startups and careers; known limitations are documented and scores are presented as a decision-support signal, never as objective truth.
- **Informed consent:** founders and job-seekers participating in validation interviews are informed of the research purpose and give consent before any data is used, even informally.
- **Transparency of AI-generated content:** users are told when they're interacting with an AI system (mentor feedback, pitch practice) rather than a human.
- **No legal or tax advice:** the compliance assistant is informational, cited, and versioned — never certified as legally correct, and never involved in managing or advising on any actual legal action between users.

## 18.4 Consent & Data Notice (shown at registration)

Required reading and active acceptance before any profile data is submitted (FR-17), for every user type. Draft text — legal review recommended before real-world use, same as any other user-facing legal text, but included here in full rather than as a placeholder so the actual commitment is visible and checkable, not just referenced:

> **What we collect and why.** We collect the profile information you provide (startup details, CV/LinkedIn text, expertise or investment focus), plus basic technical data needed to run the platform (login activity, uploaded file metadata). If you link a GitHub profile, we read basic public metadata only (repository count, commit recency, language mix) — never private repository content. If you provide a personal portfolio link or, for founders, a product/build-in-public link, we fetch that page to confirm it's real and consistent with what you've told us — this is shown as its own note right where you enter the link, separate from this general notice, and is used for verification only, never shared or repurposed. We never fetch your LinkedIn page directly — only the information LinkedIn itself returns through the secure login you approve. We use this to power matching, readiness scoring, and the other features described in this platform, and — only with your separate, explicit agreement below — to help us review profiles for authenticity.
>
> **What we don't do.** We never sell your data. We never scrape your personal profile from elsewhere without your registering it yourself. Mentor and investor contact details are never shared with a founder until you've both agreed to connect.
>
> **Your controls.** You can request a copy of your data or its deletion at any time from your account settings; deletion requests are honored, not just accepted in principle.
>
> **Review consent (separate, optional checkbox):** "I consent to my profile review decision and the signals behind it being stored, in anonymized form, to help The Founder's Carnet improve how it detects fake or low-effort profiles in the future." Declining this box does not block registration — it only means your review data isn't used for that future improvement work (Section 23).

**Contextual consent note (shown directly on the portfolio/product link field, not just in the notice above):** "This link is optional. If you provide it, we'll check that it's reachable and consistent with your profile — used only for verification, never shared publicly or with other users beyond your profile itself. Skipping this is fine; it just means one fewer signal toward instant verification." Shown at the point of entry rather than left to a general notice the person may not remember by the time they reach this field — the same "checkable, not asserted" discipline this document applies elsewhere (Section 1.1).

## 18.5 Trust Note (shown at registration)

Shorter, plainer, and shown alongside the consent notice above — this is the "why" in human terms, not the legal text:

> Every profile on The Founder's Carnet is checked before it goes live. Strong, clear signals — like a verified LinkedIn account or a matched SECP registration — get you verified instantly. If something about your profile needs a closer look, a real person checks it before it goes live, rather than an automated filter making the final call on unclear cases. We built it this way on purpose: genuine founders and genuine investors are exactly who this platform is for, and we'd rather take a moment on the unclear cases than let bots and low-effort spam profiles crowd out real people.

# 19. Risks & Limitations

| Risk / Limitation | Impact | Mitigation |
|---|---|---|
| Cold start — empty mentor and investor pools at demo time | Weak, unconvincing live demonstration | Seed early with real mentors from faculty/industry contacts and real founders from validation interviews. This risk is real even for established platforms: PakStartups.org's Startup Directory is now well-populated (100+ real listings, confirmed by direct visit, August 2026), but reaching that took sustained real-world growth effort — an earlier snapshot of the same platform found several features with no listings at all, which is exactly the "reads as broken, not just empty" failure mode The Founder's Carnet needs to avoid at its own launch (see Appendix A for both findings, dated). |
| Sparse Pakistani-specific matching data | Underpowered re-ranker training | Human-annotated relevance dataset via the anchor-partner incubator (Section 20); realistic 150–300 label target rather than an aspirational 1,000+; document dataset construction and any inter-rater agreement achieved. |
| LLM dependency reads as "just an API wrapper" | Weak perceived ML contribution | Trained re-ranker is the explicit primary ML artifact; every other feature is labeled prompted, not trained, so the distinction is stated rather than implied. |
| Hallucinated market research or compliance answers | Founders shown false information | Evidence-first synthesis and RAG grounding with mandatory citations; explicit "no confident answer found" fallback instead of guessing. |
| Regulatory/legal risk in compliance answers | Guidance mistaken for legal/tax advice | Positioned as an informational retrieval assistant with visible disclaimer, source dates, and versioning — never legal certainty. |
| Roman Urdu variability | Inconsistent multilingual performance | Treated as an evaluated, benchmarked feature — validated with a baseline benchmark before the pipeline is built around an assumed capability; fine-tuning to close a measured gap is an explicit stretch goal, not a promise, gated by a Month 4 data-threshold checkpoint (Section 13.7). |
| Temptation to source multilingual/matching training data via scraping (social media, messaging apps, forums) under deadline pressure | Legal exposure (PECA), platform Terms of Service breach, and direct contradiction of the platform's own self-registration-only stance (Section 6.2, 18.2) — the kind of finding that turns a data-quality question into an ethics one in front of a panel | Data sourcing for every labeled dataset, including the multilingual fine-tuning triples, is locked to self-registration, consented pilot data, manual authorship, and LLM-assisted synthetic generation only — with the exclusion list stated explicitly rather than left to individual judgment under time pressure (Section 13.7). |
| Investor fit is more than semantic similarity | Poor match quality if similarity is the only signal | Hard constraints plus structured features (stage, ticket size, thesis, geography) combined with semantic similarity in the re-ranker. |
| Competitive overlap with InnoCollab.pk / PakStartups.org / PakLaunch / StartupNetwork.pk | Panel questions the project's novelty | Explicit, evidence-based differentiation (Section 5) citing four direct, hands-on product audits (Section 4.1) and one remaining clearly-labeled preliminary scan entry, Startup.pk (Section 4.2), rather than assumed gaps. |
| Fake or low-quality profiles | Misleading matches, spam | No longer left abstract: hybrid verification (Section 13.8) auto-verifies or auto-rejects on strong signals (LinkedIn OAuth handshake or SECP company-registration ID cross-check, FR-12, plus completeness) and escalates ambiguous cases and appeals from rejected users to human review; reported or blocked profiles re-enter human review specifically rather than a separate undefined flow. |
| Data privacy — sensitive CVs, pitch decks, investor information | Confidentiality risk | Data minimization, role-based access, encrypted secrets, explicit consent, deletion controls. |
| Overall scope vs. three-person, six-month capacity | Missed deliverables | Tiered feature list, realistic (not aspirational) dataset and evaluation targets throughout this document, and the fallback build order in Section 22. |
| Features considered and deliberately excluded, not merely deferred | Scope drift if reconsidered later without the original reasoning | Two items were evaluated and rejected outright rather than pushed to Phase 2 (Section 23): (1) expanding the compliance RAG corpus to cover SBP foreign-exchange rules and offshore holding-company structuring ("Delaware flips") — this is complex cross-border tax/corporate law, a materially different risk category from citing SECP/FBR registration steps, and doesn't get safer with more time, only riskier with more usage; (2) building gender- or location-based weighting directly into the matching model's scoring function — a real algorithmic-fairness question that needs dedicated ethical review before being built at all, not a coefficient to add casually. Recorded here so the reasoning isn't lost if either idea resurfaces later. |

# 20. Go-to-Market / Trust & Adoption Strategy

The trust mechanics already covered above (verification, moderation, mutual acceptance, cited evidence) answer *how the platform stays trustworthy once people are on it*. They don't answer the harder question: why would the *first* investor or founder ever join a platform with no one else on it yet.

**Anchor-partner approach:** rather than attempting to cold-acquire three sides of a marketplace simultaneously, the team pursues one real institutional partner during the FYP. This is not a "nice to have" GTM idea; it is the actual mechanism that makes Section 9's human relevance-judgment dataset achievable at all. A partnership provides:

- Instant credibility ("validated with an active incubator's cohort," not "we hope people show up")
- A realistic path to the annotated matching dataset the re-ranker depends on
- A believable, specific answer to a supervisor's or panel's "how do you get anyone to trust and join this" question

**Wave 1 — government-backed and university-based (first outreach priority):**

- **NIC (National Incubation Center) network**, under Ignite / the Ministry of IT & Telecom — nine centers nationally (Islamabad, Lahore, Karachi, Peshawar, Quetta, Rawalpindi, Faisalabad, Hyderabad, Sialkot). **Correction, verified September 2026:** an earlier draft of this document described NIC Lahore as co-located with LUMS's Center for Entrepreneurship — that is no longer accurate. LUMS hosted a National Incubation Center Lahore (NICL) in partnership with Ignite for several years, but that arrangement ended December 19, 2023; the National Incubation Center Lahore operating today is a separate organization, run by a NetSol Technologies–led consortium at Vogue Tower, with no current LUMS affiliation. NIC Lahore is therefore approached as a fully independent Wave 1 target on its own merits, not as a geographically convenient extension of the LUMS relationship.
- **Plan9** — Punjab Information Technology Board's own Lahore-based accelerator, already the team's primary reference point for cohort-capacity comparisons (Section 2).
- **Ignite (National Technology Fund)** itself — the umbrella body funding the NIC network and the WISE Lab initiative referenced for women-led founder outreach (Section 8).
- **University-based options** — LUMS Center for Entrepreneurship and NUST Technology Incubation Center. The team's placement office is separately attempting an introduction to NIC or LUMS on the team's behalf (in progress — Section 22); FAST-NUCES's own entrepreneurship/ORIC-equivalent channels were checked directly and don't run this kind of incubator matchmaking themselves, so direct outreach remains the team's primary path regardless of how the placement-office introduction lands.

**Wave 1 outreach update, dated September 17, 2026:** the team's first Wave 1 conversation — with Minahil Zia at LUMS Centre for Entrepreneurship — did not result in an anchor-partner relationship at this stage. The team was not able to fully deliver the planned pitch; feedback included that the idea read as vague and that the team lacked demonstrable entrepreneurial background, alongside an offer of bot/test accounts for FYP demonstration purposes and a stated conditional willingness to introduce the team to her own team and to founders once a working prototype or proper, market-fit product exists. Full record kept separately (LUMS_CfE_Meeting_Record_2026-09-17.md; decision logged in DECISIONS.md). Per supervisor guidance, this is not being treated as a closed door: the team is deferring further incubator outreach until the platform is more pitch-ready, and in the interim is running an in-university survey across all project aspects and approaching FAST-NUCES faculty for mentorship. This affects Wave 1/Wave 2 outreach pacing specifically, not the Section 22 build timeline.

**Wave 2 — private accelerators, VC firms, and angel networks (pursued once a first-wave conversation is underway, not before):**

- **Private accelerators:** Invest2Innovate (i2i), Katalyst Labs, Epiphany, Demo, Telenor Velocity, Jazz Xlr8.
- **VC firms:** Sarmayacar, Indus Valley Capital, Fatima Gobi Ventures, i2i Ventures, Zayn Capital, 47 Ventures, Lakson Investments Venture Capital, TPL e-Ventures.
- **Angel networks:** Pakistani Angels, TIE Islamabad, Pakistan Business Angel Network (PBAN).
- **Individual founders and investors**, approached directly as a supplementary channel alongside the institutional outreach above — not a replacement for it. This includes publicly visible figures from Pakistan's startup media, most notably Shark Tank Pakistan's Season 1 panel (Aleem Dar, Rabeel Warraich, Junaid Iqbal of Salt Ventures, Faisal Aftab of Zayn Capital — already a Wave 2 target independently — and Kalsoom Lakhani), as well as founders who pitched on the show. The founders are arguably the stronger near-term fit: their fundraising journeys are already public and self-articulated, making them well-suited to the validation interviews in Appendix C, not just individual-investor outreach.

**On response rates for individual outreach:** these are not something the team controls or can predict, and no single contact is treated as a required outcome. The deliverable here is the outreach effort itself — working through the institutional, university, and individual channels available given the team's own capacity, network, and references — not a guaranteed reply from any specific person. A non-response simply moves the team to the next name on the list, the same way a "no-go" is handled at the Month 4 multilingual checkpoint (Section 13.7): a decided, documented path either way, not a stalled one.

**The specific pitch to Wave 1 organizations:** beyond general credibility and dataset access (above), the concrete ask is an exchange, not a one-way favor. If the partner organization is running, or planning, an investor-facing event, The Founder's Carnet offers to provide a curated shortlist of registered, readiness-scored startups from the platform for that event's pitch slots. This is framed carefully as **curation, not endorsement** — the platform is surfacing candidates it has structured data on, not vouching for their investment readiness or outcomes, consistent with the introduction-only boundary this document holds everywhere else (Section 7, Section 18.1).

This is deliberately scoped as outreach the team can start immediately (a conversation with one institution), not a dependency that blocks the build — the toy/synthetic pipeline validation described in Section 9 and the multilingual baseline benchmark and fine-tuning data collection in Section 13.7 proceed in parallel regardless of how the partnership conversation goes.

# 21. Research Questions

1. Does a hybrid semantic + structured-feature re-ranker measurably outperform a semantic-similarity-only baseline for founder-mentor, founder-investor, and startup-talent matching, given a realistically small (150–300 label) Pakistani-specific dataset?
2. Does retrieval-augmented generation, grounded in a whitelisted official-source corpus, measurably reduce unsupported/hallucinated claims in regulatory guidance compared to unconstrained LLM generation?
3. Does an LLM-scored, rubric-based readiness assessment correlate meaningfully with human expert judgment, without being presented as a funding-outcome predictor?
4. Does retrieval and generation quality differ meaningfully across English, Urdu, and Roman Urdu for the matching and compliance-assistant pipelines, and if so, where specifically does it degrade? *(Conditional follow-up, stretch scope: if a meaningful gap is found, does contrastive fine-tuning on a small, legitimately-sourced labeled dataset measurably close it, relative to the off-the-shelf baseline?)*

# 22. Timeline / Milestones

Two semesters, approximately eight months. Ownership and per-person work division are deliberately not assigned here — that's a team-internal decision made separately from this document.

| Phase | Milestones |
|---|---|
| Month 1 | Supervisor sign-off; founder/talent validation interviews (10–15 each); anchor-partner outreach begins; finalize requirements; architecture design. |
| Month 2 | Core schema + auth; founder & talent profile CRUD; initial LLM orchestration (mentor feedback). |
| Month 3 | Readiness score; pitch-practice MVP; embedding pipeline stood up; multilingual baseline benchmark run (English/Urdu/Roman Urdu, off-the-shelf model) and results reported; consented pilot-data collection and manual/synthetic triple authoring begins in parallel, under the locked sourcing rules (Section 13.7). |
| Month 4 | Matching service (baseline cosine similarity); mid-year evaluation/demo; **go/no-go checkpoint for multilingual fine-tuning** — labeled triple count reviewed against the pre-agreed threshold (Section 13.7); decision made and locked, not revisited under later time pressure. |
| Month 5 | RAG compliance assistant; document ingestion pipeline for SECP/FBR/PSEB sources. |
| Month 6 | Job/internship board; resume/LinkedIn optimizer; investor discovery limited to verified startups with a completed readiness assessment. |
| Month 7 | Re-ranker training on accumulated/anchor-partner-sourced interaction data; **if Month 4 checkpoint was a go:** contrastive fine-tuning of the multilingual embedding model and fine-tuned-vs-baseline benchmark comparison; **if no-go:** baseline multilingual results finalized as-is; UI polish; seeding real demo data. |
| Month 8 | Evaluation against success metrics; documentation finalization; final defense preparation. |

**Fallback order if behind schedule (FYP-1, updated 2026-10-01):** authentication, role-based access, and profiles are built first because every feature depends on them. After that: (1) compliance RAG and its evaluation, (2) matching/re-ranking engine (prototyped in FYP-1 with the cosine-similarity baseline; training and evaluation moved to FYP-2 given the anchor-partner data dependency, Section 9), (3) readiness score, (4) pitch simulator and market research synthesis, (5) resume/LinkedIn optimizer and talent/job layer, (6) secondary polish, (7) the English/Urdu/Roman Urdu benchmark (already deferred to FYP-2). The FYP-1 checkpoint is the end of the semester: if the compliance assistant does not return cited answers and abstain correctly on a held-out question set by then, nothing lower on the list is extended until it does. Compliance RAG leads for FYP-1 specifically because it has no external data dependency and is fully testable now; the matching engine remains the project's primary ML contribution overall and returns to the top of this order once anchor-partner data is available.

# 23. Phase 2 — Potential Business (expected steps if pursued beyond the FYP)

Everything here is framed deliberately: Phase 1 (Section 6.1) is what's realistic to demonstrate as the FYP. This section is not a wishlist — it's what's actually expected to happen, in roughly this order, if the team chooses to take The Founder's Carnet beyond the FYP as a real business. Every item below is deferred for a specific, named reason — legal, financial, or resource-based — not because it lacks value. Listing the constraint alongside each item is what shows a panel the team understands *why* something is out of scope for Phase 1, not just that it is.

| Phase 2 item | What it adds | Why it's a Phase 2 — Potential Business step, specifically |
|---|---|---|
| Real payment gateway integration (JazzCash/Easypaisa) | Live billing for subscriptions and placement fees, replacing the FYP's mocked paywall UI | Requires a registered business bank account and a merchant agreement — both require the company to actually be incorporated first. An FYP prototype run by three students without a registered entity cannot legally hold a merchant account; the demo uses a mocked paywall for exactly this reason. |
| Milestone tracker with recurring AI check-ins | Recreates YC's weekly-accountability mechanic; strengthens subscription retention | Retention features only make sense once there's a live, paying user base generating the behavior to check in on. Building it against zero real usage data would be building a feature with no way to validate it works. |
| Cofounder matching | Reuses the existing matching engine for a new relationship type | Cofounder matching implicitly touches equity-split expectations between matched parties — the same category of sensitivity that caused the team to remove the equity-based business model. Reusing the matching engine here is technically trivial; the product/legal framing around it (what happens when two matched people need to agree on equity) is not, and is deliberately kept separate from the FYP's no-equity boundary. |
| Deeper regional language support beyond Urdu/Roman Urdu | Broader accessibility | Each additional language requires its own benchmarking and preprocessing work — as demonstrated by the nontrivial effort required just to validate Roman Urdu (Section 13.7). Claiming broader coverage without the same rigor would repeat the exact mistake this document was rewritten to avoid: an unverified multilingual claim. |
| Video pitch upload with speech-to-text extraction | Lets founders submit a spoken pitch instead of typing one, feeding the transcript into the existing pitch-feedback pipeline | Real, buildable infrastructure — a video storage layer, a third-party speech-to-text API, and added privacy/consent handling for video data — but it's additional infrastructure on top of an already tight six-month build, not a cheap add-on. Belongs after the core matching and RAG contributions are solid, not competing with them for the team's time. |
| Roman Urdu support beyond the feasibility-spike outcome (Section 13.7) | Full transliteration/normalization coverage if the spike shows today's embeddings genuinely aren't enough | Deliberately conditional: whether this is needed at all depends on what the spike finds. Building a dedicated normalization layer regardless of the spike result would be solving a problem that might not exist, at the cost of time the matching and RAG contributions need more. |
| Open community/discussion forum | Peer support and engagement beyond the core matching flows | Directly observed during competitive audit, and reconfirmed on follow-up review (Appendix A): PakStartups.org's Startup Directory needed sustained real-world effort to reach its current 100+ real listings — an earlier snapshot of the same platform found several features with no listings at all, illustrating exactly how easily an unseeded community feature reads as broken rather than quiet. Pakistani founders have also already consolidated around existing channels (PakStartups' own r/PakStartups Reddit community, 14,000+ members; an active "Startup Pakistan" LinkedIn presence with 600K+ followers; PakLaunch's 400K+-member diaspora network, Section 4.1) — PakLaunch's own forum activity, confirmed by direct audit, shows real founders already posting fundraising asks and organizing real regional meetups there, which only strengthens the point. A new, unseeded The Founder's Carnet forum has no credible path to displacing them within an FYP timeline, and arguably not without a real, funded growth effort afterward either. |
| Paid, human-staffed biannual cohort training | A plausible premium offering layered on top of the AI tools | This is a real operating business function — hiring staff, scheduling, curriculum, contracts — not a software feature. It requires the company to exist as a legal entity with actual operating capital, which is a post-incorporation, post-FYP concern by definition. |
| Any equity-based or investment-outcome-linked monetization | Would more closely mirror how YC itself makes money | Requires SECP crowdfunding-platform or investment-advisor licensing, dedicated legal counsel, and capital reserves neither the FYP nor an early-stage post-graduation company realistically has. This is not "later in Phase 2" — it is out of scope indefinitely unless the company pursues a completely separate, dedicated regulated business line, which is a Series-A-or-later conversation, not a near-term roadmap item. |
| Aggregated ecosystem intelligence product (sold to VCs, corporates, PSEB/Ignite) | A second, higher-margin revenue line built on top of accumulated matching/market data | Requires meaningfully more real usage and data volume than an FYP or even an early post-graduation product will have generated. Positioned honestly as a plausible long-run direction (Section 7.2), not a near-term deliverable. |
| ML-based legitimacy/fraud scoring for new profiles | Replaces the Phase 1 authored, rule-based signal score (Section 13.8) with a genuinely trained model, further reducing the volume of cases escalated to human review | Needs a real training signal that doesn't exist yet: enough consented, logged decisions — both auto-decided and human-decided — accumulated over real usage. Attempting this during the FYP would mean training on too few confirmed fake-profile examples to produce anything better than noise — the same "not enough labeled data" problem already worked through for the matching re-ranker (Section 9), sharper here because fraud is rarer than match quality. The Phase 1 rule-based score (not a trained model) plus human review for ambiguous cases stays the mechanism through Phase 1 for this reason. |

# 24. Conclusion

The Founder's Carnet is scoped as an honest, buildable answer to a specific, evidence-backed gap: Pakistani founders outside the narrow physical accelerator system, and job-seekers who specifically want to work at startups, currently have no integrated, AI-native platform serving them. Every individual AI capability here has a real precedent elsewhere; the contribution is combining them onto one reasoning engine, grounding them in Pakistani regulatory reality, making them accessible in the languages founders actually use, and being explicit — throughout, not just in a limitations appendix — about what is legally, financially, and practically out of scope for a student-built prototype. The primary research contribution is the trained hybrid matching/re-ranking model, evaluated against a real baseline on a realistically-sized, honestly-sourced dataset; the primary product contribution is the integration itself.

# 25. References

This section is the full compiled bibliography, merged in from the companion Resources, Literature & Dataset Reference document per its own stated purpose ("compiled for... Section 25 (References) expansion"). Every entry carries the same type tag used in the companion document — **[Peer-reviewed]**, **[Preprint]**, **[Official/Government]**, or **[Community/Industry data]** — so academic literature, government sources, and practitioner/community data are never blended together. A sample of these citations (arXiv IDs, DOIs, and specific factual claims — including the Journal of Pakistan Administration's 22,549-RLCO figure and the SECP regulatory naming correction below; the RLCO expansion itself was found to be incorrect in a second verification pass and is corrected at that entry) were independently re-verified via live search in September 2026 as part of this merge; the remainder carry forward the companion document's own verification pass, dated the same session it was compiled. One correction was found and applied during this merge: "An Automatic Pitch Deck Analyzer" is dated 2024 per ACM's own conference listing (CODS-COMAD '24), not 2025 as an earlier draft had it.

**Fourth update, 13 October 2026.** A nine-claim evidence register was resolved (`claim_evidence_register.md`). Changes: (1) Pitch Pakistan was removed from the report entirely, including its comparison row, bibliography entry and Appendix A rows, and the audited-platform count is now four (InnoCollab.pk, PakStartups.org, PakLaunch, StartupNetwork.pk) out of seven platforms reviewed. (2) The Plan9 source now points to `plan9.pitb.gov.pk/node/1176`, accessed 13 October 2026, with a note that the page's introductory text still says 160 startups in 10 cycles. (3) The IFDP link was kept, but the entry now says the site was open on 3 October 2026 and did not load on 13 October 2026, and describes IFDP as curated matchmaking per its public pages. (4) Halo's lack of SECP/FBR/SBP knowledge is scoped to the team's September 2026 test. (5) Startup.pk Pro is described as a waitlist. (6) StartupBlink is cited from the official page (`ref:startupblink2026`, 13 October 2026). (7) The SHA-256 of the April 2026 Seventh Schedule was added to `profile_report.md` (fee Rs 6,655 from 20 April 2026, up 10% from Rs 6,050). Confirmed and unchanged: ITO s.154A rate of 0.25% to tax year 2029, the two different startup definitions, Clause 133 omitted by the Finance Act 2021, and the Companies Act ss.462 to 473 titles. Do not cite the GAE law-firm article, the AI-generated Companies Act summary, or the AI-generated PSEB FAQ PDF. Claims 1 to 6 (login-gated or hands-on observations) are still being re-checked by Ali and may change wording.

**Third update, 4 October 2026.** The regulatory corpus and external datasets were downloaded and profiled, and the Chapter 3 bibliography was completed. Corrections: the Ordinance corpus copy is now FBR's consolidation amended up to 30 June 2026 (839 pp.); Companies Act fees are cited from the Seventh Schedule with fees in effect from 20 April 2026 (the 10 November 2025 version is superseded); the Roman-Urdu-Parl split loads 6,374,678 pairs. Sources cited in Chapter 3 that were missing from this list are added under "Chapter 3 additions" below. Evidence: `Chapter3_Source_Register_v2.md`, Section E.

**Second verification pass, October 2026.** The companion Resources document was re-verified end to end against primary texts rather than search summaries. Over 60 corrections were applied, including three serious errors that had propagated into this document: (1) the citation "Income Tax Ordinance 2001, Second Schedule §143" was wrong in both the section number and the instrument — §143 governs non-resident shipping — and has been replaced with the correct §154A position below; (2) the expansion "Registration Letters of Company Operations" for RLCO did not appear in the source paper and was removed; (3) the role attributed to PEAR (structured-feature fusion) was wrong, and Grbovic & Cheng (KDD '18) has been added as the correct Stage 2 precedent. Further corrections to venue, authorship, and metric names are marked inline at the affected entries. The full change log, with per-source evidence grading, is held in `Chapter3_Source_Register_v2.md`.

### Matching & Re-Ranking Engine

Yu, X., Zhang, J., & Yu, Z. (2024). ConFit: Improving Resume-Job Matching using Data Augmentation and Contrastive Learning. [Peer-reviewed] *RecSys '24*, 601–611. https://doi.org/10.1145/3640457.3688108 *(corrected October 2026: peer-reviewed at ACM RecSys 2024, previously listed as a preprint)*

Yu, X., et al. (2025). ConFit v2: Improving Resume-Job Matching with Hypothetical Resume Embedding and Runner-Up Hard-Negative Mining. [Peer-reviewed] *Findings of ACL 2025*. https://aclanthology.org/2025.findings-acl.661/ *(corrected October 2026: now peer-reviewed, previously listed as a preprint)*

Pei, C., Zhang, Y., Zhang, Y., Sun, F., Lin, X., Sun, H., Wu, J., Jiang, P., & Ou, W. (2019). Personalized Re-ranking for Recommendation. [Peer-reviewed] *RecSys 2019*. https://arxiv.org/abs/1904.06813

Grbovic, M., & Cheng, H. (2018). Real-time Personalization using Embeddings for Search Ranking at Airbnb. [Peer-reviewed] *KDD '18*, 311–320. https://doi.org/10.1145/3219819.3219885 *(Added October 2026 as the correct precedent for the Stage 2 design: learned embeddings used as similarity features alongside structured features in a gradient-boosted ranker, in a two-sided marketplace.)*

Burges, C. J. C. (2010). From RankNet to LambdaRank to LambdaMART: An Overview. Microsoft Research Technical Report MSR-TR-2010-82.

Ke, G., et al. (2017). LightGBM: A Highly Efficient Gradient Boosting Decision Tree. [Peer-reviewed] *NIPS 2017*, 3146–3154.

Li, Y., Zhu, J., Liu, W., Su, L., Cai, G., Zhang, Q., Tang, R., Xiao, X., & He, X. (2022). PEAR: Personalized Re-ranking with Contextualized Transformer for Recommendation. [Peer-reviewed] *Companion Proceedings of the Web Conference 2022*, 62–66. https://doi.org/10.1145/3487553.3524208 *(Role corrected October 2026: PEAR models mutual influences among items in a list together with user history — listwise context modelling, not the fusion of structured features with embeddings. It is cited here only to note that listwise re-ranking models exist and require substantially more training data than this project has.)*

Thakur, N., Reimers, N., Rücklé, A., Srivastava, A., & Gurevych, I. (2021). BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models. [Peer-reviewed] *NeurIPS 2021 Datasets & Benchmarks Track*. https://arxiv.org/abs/2104.08663

Abdollahpouri, H., & Burke, R. (2019). Multi-stakeholder Recommendation and its Connection to Multi-sided Fairness. [Peer-reviewed, RMSE workshop at RecSys 2019] https://arxiv.org/abs/1907.13158 *(the paper's running multi-stakeholder example is Uber Eats — consumers, restaurants, and delivery partners — not Uber; Airbnb is used for the multi-provider exposure case)*

Covington, P., Adams, J., & Sargin, E. (2016). Deep Neural Networks for YouTube Recommendations. [Peer-reviewed] *RecSys 2016*. https://dl.acm.org/doi/10.1145/2959100.2959190

Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. [Peer-reviewed] *Proceedings of EMNLP-IJCNLP 2019*, 3982–3992. https://arxiv.org/abs/1908.10084

Karpukhin, V., Oğuz, B., Min, S., Lewis, P., Wu, L., Edunov, S., Chen, D., & Yih, W. (2020). Dense Passage Retrieval for Open-Domain Question Answering. [Peer-reviewed] *EMNLP 2020*. https://arxiv.org/abs/2004.04906

Qin, C., et al. (2023, revised 2025). A Comprehensive Survey of Artificial Intelligence Techniques for Talent Analytics. [Preprint] https://arxiv.org/abs/2307.03195 *(scope note, October 2026: this surveys AI for talent analytics across talent management, organization management, and labour market analysis; person-job fit is one subsection, not the paper's focus)*

Guo, W., Liu, X., Wang, S., Kazi, M., Wang, Z., Fu, Z., Jia, J., Zhang, L., Gao, H., & Long, B. (2021). Deep Natural Language Processing for LinkedIn Search. [Preprint, industry] https://arxiv.org/abs/2108.13300

Ayoobi, N., Shahriar, S., & Mukherjee, A. (2023). The Looming Threat of Fake and LLM-generated LinkedIn Profiles: Challenges and Opportunities for Detection and Prevention. [Peer-reviewed] *HT '23: Proceedings of the 34th ACM Conference on Hypertext and Social Media*, Article 38, 1–10. https://doi.org/10.1145/3603163.3609064 *(establishes that profile section structure is discriminative for detecting fake and LLM-generated profiles, reaching 96.33% accuracy with BERT on manually created fakes — the basis for this project's rule-based profile-completeness heuristics, Section 13.8.)*

Gulati, A., Agarwal, V., Sharma, A., & Kumar, R. (2025). Weak Links in LinkedIn: Enhancing Fake Profile Detection in the Age of LLMs. [Peer-reviewed] *ASONAM 2025*, Springer Lecture Notes in Computer Science, vol. 16323. https://doi.org/10.1007/978-3-032-13821-7_31 *(must be read alongside Ayoobi et al. above: this paper reports that detectors performing at roughly F1 96% on manually created fake profiles fall to roughly F1 68% against LLM-generated profiles, with a false accept rate of 42–52%. This project therefore treats rule-based profile heuristics as raising the cost of casual fakery rather than defending against a determined LLM-assisted attacker, which is why human review is retained for mentor onboarding — Section 13.8.)*

Dai, H., et al. (2015). Scraping and Clustering Techniques for the Characterization of LinkedIn Profiles. [Low-tier venue: ITCS 2015 / AIRCC] https://arxiv.org/abs/1505.00989 — historical methodology note only, superseded by the two entries above; this project's self-registration-only, no-scraping stance (Sections 6.2, 18.2) is a deliberate contrast to this paper's approach.

### RAG & Compliance Assistant

Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W., Rocktäschel, T., Riedel, S., & Kiela, D. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. [Peer-reviewed] *Advances in Neural Information Processing Systems*, 33, 9459–9474. https://arxiv.org/abs/2005.11401

Kim, J., Hur, M., & Min, M. (2025). From RAG to QA-RAG: Integrating Generative AI for Pharmaceutical Regulatory Compliance Process. [Peer-reviewed] *SAC '25: Proceedings of the 40th ACM/SIGAPP Symposium on Applied Computing*, 1293–1295. https://doi.org/10.1145/3672608.3707749 *(corrected October 2026: the venue year was 2025, not 2024, and the published paper has three authors; the 2024 arXiv preprint has two. It is a three-page short paper and carries the domain-analogy role, not evaluation claims.)*

Magesh, V., Surani, F., Dahl, M., Suzgun, M., Manning, C. D., & Ho, D. E. (2025). Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools. [Peer-reviewed] *Journal of Empirical Legal Studies*, 22(2), 216–242. https://doi.org/10.1111/jels.12413 *(a preregistered empirical evaluation finding that leading commercial AI legal research tools hallucinate between 17% and 33% of the time — the strongest available justification for this project's mandatory-citation and abstention design.)*

Joren, H., Zhang, J., Ferng, C.-S., Juan, D.-C., Taly, A., & Rashtchian, C. (2025). Sufficient Context: A New Lens on Retrieval Augmented Generation Systems. [Peer-reviewed] *ICLR 2025*. https://arxiv.org/abs/2411.06037

Peng, X., Choubey, P. K., Xiong, C., & Wu, C.-S. (2025). Unanswerability Evaluation for Retrieval Augmented Generation. [Peer-reviewed] *ACL 2025*. https://arxiv.org/abs/2412.12300

Niu, C., et al. (2024). RAGTruth: A Hallucination Corpus for Developing Trustworthy Retrieval-Augmented Language Models. [Peer-reviewed] *ACL 2024*, 10862–10878. https://doi.org/10.18653/v1/2024.acl-long.585

Asai, A., Wu, Z., Wang, Y., Sil, A., & Hajishirzi, H. (2024). Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection. [Peer-reviewed] *ICLR 2024*. https://arxiv.org/abs/2310.11511

Rajpurkar, P., Jia, R., & Liang, P. (2018). Know What You Don't Know: Unanswerable Questions for SQuAD. [Peer-reviewed] *ACL 2018*. https://arxiv.org/abs/1806.03822

Kamath, A., Jia, R., & Liang, P. (2020). Selective Question Answering under Domain Shift. [Peer-reviewed] *ACL 2020*. https://arxiv.org/abs/2006.09462

Cormack, G., Clarke, C., & Büttcher, S. (2009). Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods. [Peer-reviewed] *SIGIR 2009*. https://dl.acm.org/doi/10.1145/1571941.1572114

### RAG / LLM Evaluation Methodology

Es, S., James, J., Espinosa-Anke, L., & Schockaert, S. (2024). RAGAS: Automated Evaluation of Retrieval Augmented Generation. [Peer-reviewed] *EACL 2024 System Demonstrations*. https://aclanthology.org/2024.eacl-demo.16/ *(metric-name correction, October 2026: the published paper's three metrics are Faithfulness, Answer Relevance, and **Context Relevance** — how much of the retrieved context is needed to answer. "Context Precision" is a later metric in the ragas library and does not appear in the paper; earlier drafts of this document conflated the two.)*

Yu, H., et al. (2024). Evaluation of Retrieval-Augmented Generation: A Survey. [Preprint] https://arxiv.org/html/2405.07437v2

Liu, Y., et al. (2023). G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment. [Peer-reviewed] *EMNLP 2023*. https://arxiv.org/abs/2303.16634

Kwiatkowski, T., et al. (2019). Natural Questions: A Benchmark for Question Answering Research. [Peer-reviewed] *TACL*. https://aclanthology.org/Q19-1026/

Yang, Z., et al. (2018). HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering. [Peer-reviewed] *EMNLP 2018*. https://arxiv.org/abs/1809.09600

Bajaj, P., Nguyen, T., et al. (2016). MS MARCO: A Human Generated Machine Reading Comprehension Dataset. [Preprint] https://arxiv.org/abs/1611.09268

### Multilingual — Urdu / Roman Urdu

Alam, M., & Hussain, S. (2022). Roman-Urdu-Parl: Roman-Urdu and Urdu Parallel Corpus for Urdu Language Understanding. [Peer-reviewed] *ACM TALLIP*, 21(1). https://doi.org/10.1145/3464424 *(title corrected October 2026. The paper reports 6,365,808 sentence pairs; the publicly available split is smaller, so any figure stated in this project should be the row count actually loaded.)*

KICS, UET Lahore. (2024). Benchmarking the Performance of Pre-trained LLMs across Urdu NLP Tasks. [Preprint] https://arxiv.org/abs/2405.15453

Tahir, M. A., Shams, S., Hussain, S., & Butt, A. M. (2026). Instruction-Tuned Urdu LLMs: Efficient Adaptation of Llama Models and Evaluation Resources for Urdu. [Peer-reviewed] *LREC 2026*. https://aclanthology.org/2026.lrec-1.832/ *(title and authorship corrected October 2026; the earlier entry gave the title as "UrduLLaMA: Instruction-Tuned Urdu LLMs" and attributed it to KICS/CLE as an institution.)*

Tahir, M. A., Shams, S., Fiaz, L., Adeeba, F., & Hussain, S. (2025). Benchmarking the Performance of Pre-trained LLMs across Urdu NLP Tasks. [Peer-reviewed] *CHiPSAL 2025*. https://aclanthology.org/2025.chipsal-1.3/ *(published, not a preprint as previously listed.)*

Enevoldsen, K., et al. (2025). MMTEB: Massive Multilingual Text Embedding Benchmark. [Peer-reviewed] *ICLR 2025*. https://arxiv.org/abs/2502.13595 *(the largest multilingual embedding benchmark, covering 250+ languages. Its only Roman Urdu task is sentiment classification; it contains no Roman Urdu semantic-similarity or retrieval task, which is the evidence base for this project treating Roman Urdu retrieval as an open problem rather than a solved capability.)*

Muneer, I., Fatima, G., Khan, M. S., Nawab, R. M. A., & Saeed, A. (2023). Developing a Large Benchmark Corpus for Urdu Semantic Word Similarity. [Peer-reviewed] *ACM TALLIP*, 22(3), Article 83. https://doi.org/10.1145/3566124 *(the best off-the-shelf multilingual transformer tested, LaBSE, reached a Pearson correlation of 0.57 on Urdu-script word pairs — the realistic expectation anchor for this project's multilingual baseline, Section 13.7.)*

Fatima, G., Nawab, R. M. A., Khan, M. S., & Saeed, A. (2021). Developing a Cross-lingual Semantic Word Similarity Corpus for English–Urdu Language Pair. [Peer-reviewed] *ACM TALLIP*, 21(2), Article 25. https://doi.org/10.1145/3472618

### Startup Readiness Scoring & Pitch Feedback

Yin, X., & Luo, J. (2018). How Do Accelerators Select Startups? Shifting Decision Criteria Across Stages. [Peer-reviewed] *IEEE Transactions on Engineering Management*, 65, 574–589. https://doi.org/10.1109/TEM.2018.2791501 *(full citation added October 2026.)*

Beyhan, B., & Fındık, D. (2022). Selection of Sustainability Startups for Acceleration: How Prior Access to Financing and Team Features Influence Accelerators' Selection Decisions. [Peer-reviewed, open access] *Sustainability*, 14(4), 2125. https://doi.org/10.3390/su14042125 — 7,358 social and 2,671 environmental sustainability startups; prior equity funding and philanthropic support strongly affect selection. *(Authors and DOI verified 4 October 2026, replacing an unconfirmed placeholder.)*

(2024). An Automatic Pitch Deck Analyzer. [Peer-reviewed] *ACM CODS-COMAD '24*. https://dl.acm.org/doi/10.1145/3703323.3703710 — a DistilBERT model fine-tuned on 123 pitches reached ~76% accuracy; cited as a cautionary result supporting the trained-vs-prompted distinction (Section 11.3). (Date corrected September 2026: ACM's own conference listing dates this CODS-COMAD '24, not 2025 as an earlier draft had it.)

### Entrepreneurial Ecosystem Theory

Isenberg, D. (2010, June). How to Start an Entrepreneurial Revolution. [Practitioner/foundational] *Harvard Business Review*. https://hbr.org/2010/06/the-big-idea-how-to-start-an-entrepreneurial-revolution

Isenberg, D. (2010, July). How to Start an Entrepreneurial Revolution in Six Months. [Practitioner] *Harvard Business Review*. https://hbr.org/2010/07/how-to-start-an-entrepreneuria

Stam, E., & van de Ven, A. (2021). Entrepreneurial Ecosystem Elements. [Peer-reviewed] *Small Business Economics*, 56(2), 809–832. https://doi.org/10.1007/s11187-019-00270-6 *(corrected October 2026: the co-author was previously omitted and the year was given as 2019; the DOI was issued in 2019 but the paper was published in 2021. The paper presents its own ten-element model, not an operationalization of Isenberg's six domains.)*

Wurth, B., Stam, E., & Spigel, B. (2022). Toward an Entrepreneurial Ecosystem Research Program. [Peer-reviewed] *Entrepreneurship Theory and Practice*, 46(3), 729–778. https://doi.org/10.1177/1042258721998948

Spigel, B. (2017). The Relational Organization of Entrepreneurial Ecosystems. [Peer-reviewed] *Entrepreneurship Theory and Practice*, 41(1), 49–72. https://doi.org/10.1111/etap.12167

Acs, Z. J., Stam, E., Audretsch, D. B., & O'Connor, A. (2017). The lineages of the entrepreneurial ecosystem approach. [Peer-reviewed] *Small Business Economics*, 49(1), 1–10. https://doi.org/10.1007/s11187-017-9864-8

Awan, J. T. (2025). Ecosystem for Business Startup in Punjab: Issues, Challenges, and Way Forward. [Peer-reviewed, Pakistan-specific] *Journal of Pakistan Administration*, 46(2), 41–71. https://journal.nspp.gov.pk/index.php/jpa/article/download/109/106/239 (the 22,549 figure is correct; **correction, October 2026:** RLCO stands for "Registrations, Licenses, Certificates, and Other documents" per the paper itself, p. 48 — the earlier expansion "Registration Letters of Company Operations" did not appear in the paper and has been removed. Note also that the paper's introductory claims about limited early-stage financing and low female participation cite SECP 2024, i2i 2024 and Ignite 2023 rather than being the author's own findings; the author's own findings are limited finance, digital literacy barriers, regulatory complexity, and awareness gaps.)

### Multi-Sided Platform Economics

Rysman, M. (2009). The Economics of Two-Sided Markets. [Peer-reviewed] *Journal of Economic Perspectives*, 23(3), 125–143. *(upgraded October 2026 from a set of lecture slides to the peer-reviewed journal article.)*

Caillaud, B., & Jullien, B. (2003). Chicken and egg: competition among intermediation service providers. [Peer-reviewed] *RAND Journal of Economics*, 34(2), 309–328. *(states the chicken-and-egg problem for intermediation platforms directly, and describes the standard response as "divide-and-conquer" pricing — subsidising participation on one side and recovering the loss on the other, which is the published basis for this project's founders-free business model, Section 7. Their model is two-sided with competing intermediaries; this project is three-sided, which compounds rather than resolves the problem.)*

Rochet, J.-C., & Tirole, J. (2003). Platform Competition in Two-Sided Markets. [Peer-reviewed] *Journal of the European Economic Association*, 1(4), 990–1029. https://doi.org/10.1162/154247603322493212

Schein, A. I., Popescul, A., Ungar, L. H., & Pennock, D. M. (2002). Methods and Metrics for Cold-Start Recommendations. [Peer-reviewed] *SIGIR '02*, 253–260. https://doi.org/10.1145/564376.564421 *(addresses the new-item cold start directly; its footnote 1 states the new-user problem is symmetric where user attribute data is available, which is the case here. Also relevant to this project's evaluation design: the paper finds simple heuristic baselines rivalling trained models, and recommends reporting heuristic predictors alongside machine-learning results for perspective.)*

Two-Sided Markets, Pricing, and Network Effects. [Academic chapter, Northwestern] https://faculty.wcas.northwestern.edu/apa522/Two-Sided-Market-and-Network-Effects.pdf

### Datasets

Kaggle: Startup Success/Fail Dataset from Crunchbase. [Community/Industry data, schema proxy only] https://www.kaggle.com/datasets/yanmaksi/big-startup-secsees-fail-dataset-from-crunchbase

Kaggle: StartUp Investments (Crunchbase). [Community/Industry data, schema proxy only] https://www.kaggle.com/datasets/arindam235/startup-investments-crunchbase

darysha. Resume-Job Matching Dataset. [Community/Industry data, practice data only] https://www.kaggle.com/datasets/darysha/hse-hackathon — 150,493 parsed resume-vacancy pairs, profiled 3 October 2026. *(Replaces the earlier generic "Kaggle resume/job-matching datasets" entry. Screened and excluded: Hadi K P, Resume Dataset PDF, https://www.kaggle.com/datasets/hadikp/resume-data-pdf, image-only; Amay Mishra, How Companies Screen Resumes: ATS Dataset (NLP+ML), consistent with synthetic generation.)*

Mavkif. Roman-Urdu-Parl-split. [Community/Industry data] https://huggingface.co/datasets/Mavkif/Roman-Urdu-Parl-split — 6,374,678 pairs loaded on 3 October 2026.

Invest2Innovate. *Pakistan Startup Ecosystem Report 2024* (4th edition, launched 12 December 2024). [Community/Industry data] https://invest2innovate.com — startup funding peaked at USD 355 million in 2022, fell to USD 74 million in 2023, and reached approximately USD 37 million to November 2024; i2i's Q4 2024 Deal Flow Update gives USD 42.5 million for the full calendar year 2024. Fintech accounted for USD 30.5 million of the USD 37 million. Women comprise 39% of the startup workforce and have received 18.75% of startup funding since 2015. *(Replaces the Kaggle "Pakistan Startup Census" below, which is superseded for all current-state figures.)*

StartupBlink. *Innovators Business Environment Index 2026*. [Community/Industry data] — Pakistan ranks 100th globally and 2nd in South Asia, with pillar scores of Business Incentives 29.995 (#108), Market Perception 23.476 (#109), and Ease of Operating Business 48.845 (#97). **This is a different index from the Global Startup Ecosystem Index, in which Pakistan ranks 67th; the two must not be conflated.**

Usmani, Z. Pakistan Startup Census. [Community/Industry data] https://www.kaggle.com/datasets/zusmani/pakistan-startup-census — a 2021 personal compilation, not an official census. **Superseded (October 2026) by the i2i Pakistan Startup Ecosystem Report above for any current-state figure.** Retained only as a record of a dropped source.

LinkedIn-Dataset (GitHub). [Community/Industry data] https://github.com/navid-aub/LinkedIn-Dataset — companion paper: https://arxiv.org/abs/2307.11864 — 3,600 profiles; labels 0 (legitimate), 1 (fake), 10 and 11 (ChatGPT-generated from legitimate and from fake profile statistics) per the README, which restricts use to research.

### Pakistan Startup Ecosystem Market Data (non-academic, market-synthesis grounding only)

StartupBlink — Pakistan Startup Ecosystem (Global Startup Ecosystem Index). [Community/Industry data] https://www.startupblink.com/startup-ecosystem/pakistan — Pakistan ranks 67th globally and 2nd in South Asia in 2026, with 1,127 startups mapped. Ranking trajectory: 76th (2023), 71st (2024), 72nd (2025), 67th (2026).

Invest2Innovate (i2i). [Community/Industry data] https://invest2innovate.com

Ignite National Technology Fund. [Official/Government-affiliated] https://ignite.org.pk

### Government & Regulatory Sources

Securities and Exchange Commission of Pakistan (SECP). Regulatory Sandbox Guidelines, 2019. https://www.secp.gov.pk/regulatory-sandbox/ (corrected September 2026 — an earlier draft cited this as "Equity-Based Crowdfunding Regulations, 2019," a name that does not check out against any regulation SECP has published; re-confirmed against SECP's own site, a 2021 Lexology legal analysis, and two Pakistani law-firm writeups on SECP's fintech sandbox)

Securities and Exchange Commission of Pakistan (SECP). Companies Act 2017 (updated 18 August 2022). https://www.secp.gov.pk/companies-act-2017/ — corpus scope: Parts I and IV and sections 462–473.

Securities and Exchange Commission of Pakistan (SECP). Seventh Schedule of the Companies Act 2017, table of fees w.e.f. 20 April 2026. [Official/Government] https://www.secp.gov.pk/document/seventh-schedule-updated-till-20-04-2023-2/?wpdmdl=47657 — incorporation fee for nominal capital up to Rs. 100,000: Rs. 6,655 electronic, Rs. 12,100 physical; fees rise 10% each year under S.R.O. 500(I)/2023.

Federal Board of Revenue (IT Wing). Virtual One Stop Shop (VOSS) for Company Registration, C. No. 1(62)/SS(BDT-IT)/2017, 27 March 2018. [Official/Government] https://download1.fbr.gov.pk/Docs/20194121643945673VirtualOneStopShop(VOSS)forCompanyRegistration.pdf

Federal Board of Revenue. Register for Income Tax (web page, accessed 4 October 2026); Registration of Individual on Iris (25 May 2019); Iris FAQs. [Official/Government] https://www.fbr.gov.pk/categ/register-income-tax/51147/30846/%2071150 · https://download1.fbr.gov.pk/Docs/2019527755039915Registrationofindividualoniris.pdf · https://e.fbr.gov.pk/SOP/IRIS/Iris_FAQs.pdf

Federal Board of Revenue (FBR), Government of Pakistan. https://www.fbr.gov.pk — taxpayer registration and filing via the IRIS portal, https://iris.fbr.gov.pk

Pakistan Software Export Board (PSEB). https://techdestination.com — registration/member portal at https://portal.techdestination.com (verified September 2026; note the board's current public portal is techdestination.com, not pseb.org.pk)

Prevention of Electronic Crimes Act (PECA), 2016, Act No. XL of 2016, National Assembly of Pakistan. https://pakistancode.gov.pk

Ministry of Information Technology & Telecommunication (MoITT), Government of Pakistan. Digital Pakistan Policy, 2018. https://moitt.gov.pk

State Bank of Pakistan (SBP). https://www.sbp.org.pk (central bank / payments and forex regulator; referenced for completeness — outside this project's committed compliance-assistant scope, Section 19)

Board of Investment (BOI), Government of Pakistan. https://invest.gov.pk — general investment facilitation.

**Income Tax Ordinance, 2001** (FBR consolidation amended up to 30 June 2026, 839 pp., https://download1.fbr.gov.pk/Docs/2026724177725705IncomeTaxOrdinanace2001.pdf; replaces the 20 February 2026 copy) and **The Finance Act, 2026** (Gazette of Pakistan Extraordinary, 26 June 2026; effective 1 July 2026). [Official/Government]
*Correction, October 2026:* an earlier draft cited "Income Tax Ordinance 2001, Second Schedule §143 (PSEB startup tax exemption)". **That reference was wrong in two respects and has been removed.** Section 143 is "Non-resident ship owner or charterer", and it is a section of the Ordinance rather than a clause of the Second Schedule. The correct position, verified against the primary text, is: clause (133) of Part I of the Second Schedule (the IT/ITeS export exemption) was **omitted by the Finance Act, 2021**, and its own sunset had been 30 June 2025; the IT and ITeS definitions it carried moved to **section 2**; section 100D is the builders-and-developers regime, not an IT provision; and the operative mechanism is **section 154A, "Export of Services"**, under which the authorised dealer deducts at realisation of foreign exchange proceeds, at **0.25% for exporters registered with and certified by PSEB and 1% otherwise** (Division IVA, Part III, First Schedule — the Finance Act 2026 substituted "2029" for "2026", extending the concessionary rate through tax year 2029). Under section 154A(2) the deduction is a **final tax** only if the return is filed, withholding statements are filed where required, and sales tax returns are filed where required — with an express proviso disapplying that last condition for PSEB-registered IT exporters. A separate and distinct rate applies under **section 153** to domestic IT and ITeS payments (4%, per the Finance Act 2025).

**Securities and Exchange Commission of Pakistan.** *Position Paper: Holistic Framework for Building a Supportive Start-up Ecosystem in Pakistan*, 30 October 2024. [Official/Government] https://www.secp.gov.pk/document/rsb-position-paper/

**Pakistan Software Export Board.** *PSEB Annual Report, January–December 2025*. [Official/Government] — 9,400 registered companies, 1,400 registered call centres, 16,300 registered freelancers; USD 3.8 billion ICT exports in FY 2024-25.

**Pakistan Software Export Board.** Industry Facilitation (registration requirements, documents, fees). [Official/Government] https://techdestination.com/industry-facilitation/ — last modified 19 August 2026; indexed for registration only, never for tax.

Pakistan Bureau of Statistics (PBS). https://www.pbs.gov.pk

### Chapter 3 additions (4 October 2026)

Gokhan, T., Wang, K., Gurevych, I., & Briscoe, T. (2024). RIRAG: Regulatory Information Retrieval and Answer Generation. [Preprint] arXiv 2409.05677. Shared task: Shared Task RIRAG-2025, *Proceedings of the 1st Regulatory NLP Workshop (RegNLP 2025)*, ACL Anthology 2025.regnlp-1.1.

Bertaglia, T., Gui, H., Goanta, C., & Spanakis, G. (2026). Traceable by Design: An LLM Pipeline and Dashboard for EU Regulatory Consultation Analysis. [Preprint] arXiv 2605.30995v2.

Pipitone, N., & Houir Alami, G. (2024). LegalBench-RAG: A Benchmark for Retrieval-Augmented Generation in the Legal Domain. [Preprint] arXiv 2408.10343v1 — cited for task framing and the CUAD replication-cost estimate only.

Hendrycks, D., Burns, C., Chen, A., & Ball, S. (2021). CUAD: An Expert-Annotated NLP Dataset for Legal Contract Review. [Preprint] arXiv 2103.06268.

Khan, M., Asif, A., Khan, M. A., Latif, S., & Fatima, M. (2026). ROMEVA: Geometry-Preserving Vocabulary Expansion for Roman Urdu Language Models. [Preprint] arXiv 2606.22478v1.

Ahmed, A., Guo, L., Huang, D., Unar, S., & Nazar, M. (2026). Confidence-aware Semi-supervised Siamese Graph Networks for Semantic Text Similarity in Low-resource Urdu. [Peer-reviewed] *Scientific Reports*, 16, 27747. https://doi.org/10.1038/s41598-026-50399-0

van Aken, P., Jung, M. M., Liebregts, W., & Onal Ertugrul, I. (2023). Deciphering Entrepreneurial Pitches: A Multimodal Deep Learning Approach to Predict Probability of Investment. [Peer-reviewed] *ICMI '23*, 144–152. https://doi.org/10.1145/3577190.3614146

Giuggioli, G., Pellegrini, M. M., & Giannone, G. (2025). Artificial Intelligence as an Enabler for Entrepreneurial Finance: A Practical Guide to AI-Driven Video Pitch Evaluation for Entrepreneurs and Investors. [Peer-reviewed] *Management Decision*, 63(10), 3477–3500. https://doi.org/10.1108/MD-10-2023-1926

Kaminski, J. C., & Hopp, C. (2020). Predicting Outcomes in Crowdfunding Campaigns with Textual, Visual, and Linguistic Signals. [Peer-reviewed] *Small Business Economics*, 55(3), 627–649. https://doi.org/10.1007/s11187-019-00218-w

Khan, M. I., & Hussain, J. G. (2026). Informal Venture Capital in Emerging Economies: A Case of Pakistan. [Peer-reviewed] *Venture Capital*, 28(2–3), 359–378. https://doi.org/10.1080/13691066.2024.2433284

Jullien, B., Pavan, A., & Rysman, M. (2021). Two-sided markets, pricing, and network effects. In K. Ho, A. Hortaçsu, & A. Lizzeri (Eds.), *Handbook of Industrial Organization* (Vol. 4, Ch. 7, pp. 485–592). Elsevier. https://doi.org/10.1016/bs.hesind.2021.11.007

Burke, R. (2017). Multisided Fairness for Recommendation. [Workshop, FAT/ML 2017] arXiv 1707.00093v2.

Biswas, A., Patro, G. K., Ganguly, N., Gummadi, K. P., & Chakraborty, A. (2021). Toward Fair Recommendation in Two-sided Platforms. [Peer-reviewed] *ACM Transactions on the Web*, 16(2), Article 8.

### Platforms Audited & Other

Y Combinator. Program structure, standard deal terms, and Demo Day documentation. https://www.ycombinator.com

PakStartups — Where Pakistan's Founders Build Together. https://www.pakstartups.org/ (platform audit conducted by the project team, original audit and September 2026 re-verification)

InnoCollab.pk. Platform audit conducted directly by the project team, original audit and September 2026 re-verification.

PakLaunch. https://www.paklaunch.com (platform audit conducted directly by the project team, September 2026)

StartupNetwork.pk. https://startupnetwork.pk (platform audit conducted directly by the project team, September 2026)


National Incubation Center (NIC) network, Plan9 (Punjab Information Technology Board), and Invest2Innovate (i2i) — public program information.

*Note: this list intentionally does not include invented or unverified citations. The companion Resources, Literature & Dataset Reference document carries the full role/annotation for each citation above (why it's cited, what it defends against a panel question), plus Appendix A's quick-reference table and Appendix B's MOU template — this section is the formal bibliography; that document is the working literature-review tool.*

# 26. Appendix

## A. Competitive Audit Evidence Log

Direct-visit findings, dated, supporting Sections 4–5 and 19 — based on the team actually registering accounts and using each platform, not on saved screenshot files (none were retained as separate evidence artifacts; the specific observations below are recorded from those walkthroughs instead). Kept as a dated log rather than a single static claim, because — as this project already learned firsthand — a competitor's live product changes, and a claim that's true on one visit can go stale by the next.

| Date | Feature checked | Finding | Basis |
|---|---|---|---|
| Original audit (pre-August 2026) | PakStartups.org: Find Co-Founder, Ecosystem Directory, Events | Zero listings in all three | Direct account registration and walkthrough |
| August 2026 (re-verification) | PakStartups.org: Startup Directory | Populated, 100+ real listings with named founders, funding-stage tags, category tags, and city — e.g., Artbazaar.pk (founders Fatima, Ahsan, Abdul Rafay), NovenPay, AD Livestock Farm, vcarpool, LowPrice.pk | Direct site visit — directory grid view and an individual listing page (https://www.pakstartups.org/startups/artbazaarpk) |
| August 2026 (re-verification) | PakStartups.org homepage stated figures | "100+ Verified Startups" and "14,000+" members confirmed as the platform's own stated numbers, and consistent with the populated directory actually observed — not an unverified marketing claim taken at face value | Direct fetch of the pakstartups.org homepage |
| August 2026 (re-verification) | PakStartups.org: 14,000+ figure attribution | Corrected: attributed by the platform itself to its r/PakStartups Reddit community specifically, not Discord as an earlier draft of this document stated | Direct fetch of the pakstartups.org homepage |
| September 2026 (re-verification) | PakStartups.org: Ecosystem Directory | Still empty — "Showing 0 of 0 organizations," "No organizations found" across all region/category filters | Direct site visit, screenshot retained |
| September 2026 (re-verification) | PakStartups.org: Events calendar | Real but very thin — one listed event ("Training Work Shop For Rural Region," organized by Muhammad Ali Anjum), zero RSVPs shown | Direct site visit, screenshot retained |
| September 2026 (re-verification) | PakStartups.org: Knowledge Vault → Learning Guides subsection | Empty — "Showing 0 guides," "No guides found" across all filters; the featured "Ultimate Guide to Series A Funding" is marked "Coming Soon," not published | Direct site visit, screenshot retained |
| **Not yet re-verified** | PakStartups.org: Find Co-Founder tool specifically | Open — the three "Active Co-Founder Openings" visible on the homepage may be real user submissions or curated marketing examples; this has not been distinguished by a real registered test account | Protocol below (Appendix B) |
| Original audit (pre-August 2026) | InnoCollab.pk: "Talent/Entrepreneur" role | Founder self-promotion, not a candidate-facing job/employment section (detail below) | Direct account registration and walkthrough |
| September 2026 (re-verification) | InnoCollab.pk: "Meet Our Talented Innovators" directory | A separate page from the Talent/Entrepreneur role above — individual profiles tagged by skill (digital marketing, SEO, content writing, data analytics, Java/C++) with a "Sign up to Connect" action, closer to a genuine skills directory than founder self-promotion (detail below) | Direct site visit, screenshot retained |
| Original audit (pre-August 2026) | PakStartups.org: Knowledge Vault | Static content library, not interactive or cited (detail below) | Direct account walkthrough |
| September 2026 (new audit) | PakLaunch: registered account, Activity Feed | Real, active community — named founders posting fundraising asks (e.g., Usman Ghani, Founder/CEO of ADMA Family, seeking strategic partners and early-stage investors) and organizing real regional meetups (Toronto, Hong Kong, Singapore, Riyadh) | Direct account registration and walkthrough, screenshots retained |
| September 2026 (new audit) | PakLaunch: Halo AI assistant | Correctly declines SECP/FBR/SBP regulatory questions ("I don't have that information in my knowledge base") — but its in-chat membership pricing (Student $50/yr, Annual $500/yr, Executive $1,000/yr) does not match the live pricing page (Navigator $300/yr, Explorer $1,000/yr, Pioneer $3,000/yr) | Direct chat session, screenshots retained |
| September 2026 (new audit) | PakLaunch: job board | Real postings exist but are general-professional (Video Editor, Real Estate Analyst, AWS & Snowflake Consultant) and stale — most dated 6–9 months old at audit time | Direct site visit, screenshot retained |
| September 2026 (new audit) | PakLaunch: community/funding stats | Inconsistent across the site's own pages — 400K+/$120M+ on one page, 500K+/$130M+ on another; a third page states "As of August 2025, Paklaunch has grown to a 400K+ strong global community," the most specific dated figure found | Direct site visits, screenshots retained |
| September 2026 (new audit) | PakLaunch: forum/group moderation | Real but only lightly moderated — a "Stocks, Commodities and Cryptocurrency Trading" group includes members soliciting trading capital directly ("If anyone want to invest with me... I have expertise in this work and need capital") and promoting personal investment platforms; some posted moderation rules exist but don't prevent this | Direct site visit, screenshot retained |
| September 2026 (new audit) | StartupNetwork.pk: registered account, Startup directory | Real and populated — "Showing 37 results," mixing tech startups (AI & Automation, Tech & Software) with traditional SMBs (IP law firm, clothing manufacturer, resort) | Direct account registration and walkthrough, screenshot retained |
| September 2026 (new audit) | StartupNetwork.pk: registration options | Exactly two roles offered — Startup or Investor. No talent/job-seeker registration path exists | Direct account registration, screenshot retained |
| September 2026 (new audit) | StartupNetwork.pk: Events and Jobs tabs | Both return "There are no listings matching your search" despite full filter UIs (date range, vacancy type, qualification, salary, region) | Direct site visit, screenshots retained |

**InnoCollab.pk "Talent/Entrepreneur" role, in specific terms:** the bundled role lists founders and entrepreneurs promoting their own ventures — seeking co-founders, feedback, or capital — rather than candidates seeking employment at someone else's startup. The wider platform was also confirmed, during the same walkthrough, to have no government/regulatory compliance content, to be English-only, and to hold events only as in-app messaging rather than real-world listings. **Update, September 2026:** a separate page, "Meet Our Talented Innovators," was found during a follow-up visit and complicates this finding — it lists individual profiles tagged by skill (e.g., "digital Marketing," "Web Designer," "Guest Posting, SEO, content writing," "Data analytics, java, c++") with a "Sign up to Connect" action per profile. This reads closer to a genuine skills/talent directory than founder self-promotion. Both pages exist on the platform simultaneously and serve different purposes; neither functions as a startup-specific job/internship board with real, employer-posted openings, which is the specific gap claimed in Section 5.

**PakStartups.org Knowledge Vault, in specific terms:** a library of incorporation guides and SAFE (Simple Agreement for Future Equity) templates, structured into four subsections (Learning Guides, Operational Toolkit, Market Intelligence, Resource Directory). It isn't interactive or query-able, and its content isn't cited to specific regulatory sources the way the Carnet's compliance assistant (Section 13.6) is designed to be. **Update, September 2026:** the Learning Guides subsection specifically was found empty on direct visit — "0 guides," "No guides found" — with its featured Series A guide marked "Coming Soon" rather than published. The original characterization of the Vault as "genuinely informative as a reference" should be read as applying to whichever subsections are actually populated, not the Vault as a whole; this hasn't been checked subsection-by-subsection beyond Learning Guides.

**PakLaunch, in specific terms:** a real, actively-used diaspora community, not a static marketing site — the Activity Feed shows named individuals posting genuine fundraising asks and organizing real, dated meetups across multiple cities. Its AI assistant (Halo) is scoped narrowly and honestly (it declines regulatory questions rather than guessing), which is a point in its favor and a useful, citable example when defending why this project's own compliance assistant is grounded in retrieval rather than left to answer from a general model. Two things temper how strong a competitor it is on this project's specific dimensions: its job board is real but not startup/entry-level-curated, and its own site displays inconsistent membership/funding figures depending on which page is checked — both worth naming plainly rather than smoothing over.

**StartupNetwork.pk, in specific terms:** functions as a genuine classifieds-style business directory — the 37-listing Startup tab is real, not placeholder content — but its claimed three-sided positioning ("startups, investors, and job seekers") is not backed by the actual registration flow, which has no talent-side role at all, and its Jobs and Events tabs are both functionally empty despite built-out filter UIs. This is a more precise, corrected version of an earlier finding that described the platform's listings generally as empty — the empty result was specific to Events, and (as of this direct account audit) is also true of Jobs.


*Screenshots for every finding above dated September 2026 were captured and retained during this audit round, addressing the earlier note in this log about evidence being written-notes-only.*

## B. PakStartups.org "Find Co-Founder" Verification Protocol

Replaces an earlier placeholder ("the team will register to confirm") with an actual test plan. The goal is narrow and specific: determine whether Find Co-Founder functions as genuine talent/employment-relevant matching, or is comparatively unpopulated compared to the now-confirmed Startup Directory — not to reverse-engineer the platform's internal logic, which cannot be verified from outside and is not asserted here. One relevant, already-confirmed detail motivating this protocol: PakStartups' own registration flow for Find Co-Founder includes Freelancer and Student role options alongside Founder/Co-Founder — which is what raised the original overlap question in Section 5.

| Test profile | Registered persona | What it checks |
|---|---|---|
| Profile A | Founder seeking a full-time technical co-founder | Baseline — does the tool return any real, non-example candidate matches at all for a standard founder use case |
| Profile B | Independent freelancer available for project-based work | Whether the tool meaningfully distinguishes short-term/contract-seeking users from co-founder-seeking users, or returns the same results regardless |
| Profile C | Student seeking an internship or entry-level role | Whether a talent-side, employment-oriented use case is served at all — the specific gap this document claims (Section 5) |

**Method:** register one real account per persona, using the platform's actual signup flow, and record — in writing, with the date, and via screenshot if at all possible this time — what each account sees in Find Co-Founder: real candidate profiles, empty results, or example/placeholder content. No claim is made about *why* the tool behaves as observed (e.g., no assumption about internal filters or verification logic); only *what is directly observed* is recorded, consistent with this document's standard elsewhere.

**Outcome and how it's used:** if Find Co-Founder returns real, distinct results per persona, Section 5's differentiation claim is narrowed accordingly (competitive overlap acknowledged, differentiation rests more heavily on the other three points in that section). If it returns sparse or example-only results even for a real registered account, the existing claim stands and is updated from "pending confirmation" to "confirmed" with dated evidence.

## C. Founder & Talent Validation Interview Guide (draft)
- What is the single hardest part of getting your startup ready for investors right now?
- Have you tried to find a mentor or investor before? What happened?
- If an AI tool gave you feedback on your pitch/traction, would you trust it? What would make you trust it more?
- (Talent) What's stopped you from finding a startup job/internship so far?
- (Talent) Would you use a startup-specific job board over LinkedIn/Rozee? Why or why not?

## D. Glossary

| Term | Meaning |
|---|---|
| SECP | Securities and Exchange Commission of Pakistan — regulates company registration and capital markets. |
| FBR | Federal Board of Revenue — Pakistan's tax authority. |
| PSEB | Pakistan Software Export Board — supports and registers IT/software businesses. |
| SAFE | Simple Agreement for Future Equity — a standardized early-stage fundraising instrument popularized by YC. |
| RAG | Retrieval-Augmented Generation — grounding an LLM's output in retrieved source documents. |
| Embedding | A numeric vector representation of text used to measure semantic similarity. |
| Re-ranker | A model that re-orders an initial set of retrieved candidates using additional signals. |
| PECA | Prevention of Electronic Crimes Act — Pakistan's law governing electronic data and cybercrime, relevant to personal-data handling. |
