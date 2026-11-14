## Updates, 14 Nov 2026 (these override anything below)

- Styling is CSS Modules. Ignore Tailwind option A and the choice step in prompt F1.
- `/design/` means DESIGN.md at the repo root and `frontend/design_reference/`. Ignore stitch-v1, stitch-v2 and rename_map. `frontend/design_reference/INDEX.md` maps each route to its reference folder.
- Agents never commit. Ali commits after each step.
- No AI marks, badges or labels anywhere in the UI. The "Language-model label" rule in section 6 and test FT-06 no longer apply.
- The gradient page background stays as designed. Revisit only if Playwright screenshots show a white band.
- Order of work: Task 2 foundation first (tokens, fonts, Logo, icons, TopNav and MenuOverlay, ui components, /styleguide), then the audit, then one screen at a time.

# The Founder's Carnet: Frontend Implementation Guide

Nov 11, 2026 · @Ali

This guide covers the frontend part of the implementation chapter (template Chapter 7, your Chapter 6) and gives prompts that turn your Stitch prototypes into the real Next.js app.

## 0. Read first: the frontend already exists

Updated 11 November 2026 after reading github.com/whozahm3d/founders-carnet. I read the code and the build log. I did not run the app. Everything below that says "create" now means "change what is there".

| Area | What the repo has | Gap |
| --- | --- | --- |
| Stack | Next.js 16.4.2, React 19.3, TypeScript, ESLint | The report says Tailwind CSS and shadcn/ui. The app uses CSS Modules. Neither Tailwind nor a test runner is installed |
| Pages built | Login, register, founder dashboard, profile, readiness, pitch practice, session feedback, matches, plus the talent, mentor, investor and admin dashboards and the talent job board. All were built by Shahzeb with Antigravity from the 12 wireframes in docs/context/wireframes, not from Stitch | They follow the wireframes, so they will differ from the new Stitch prototypes |
| Placeholders | Talent profile, resume and matches; mentor profile and requests; investor profile, founders and requests all render PlaceholderPage | Real screens needed. The report promises them in D3 |
| Data | Every page except login and register shows hard-coded sample data. The API is called only for authentication (AuthContext and lib/auth.ts). Mock mode is on unless NEXT\_PUBLIC\_USE\_MOCK is set to false | The backend routes for profile, matching, readiness, pitch and compliance are not wired to any screen |
| Session | Token and user in localStorage; logged-out users go to /login; other roles' routes redirect to the user's own dashboard | The code has a TODO to move the token to an httpOnly cookie |
| Components | Badge, Button, Card, ConsentBox, EmptyState, Input, MatchCard, ProgressBar, Spinner, StatCard, plus Sidebar, PageHeader and DashboardLayout | No select, table, tabs, modal, drawer or toast |
| Design source | The 12 wireframe PNGs. DESIGN.md and the Stitch exports are not in the repo | CLAUDE.md says the Figma prototypes and DESIGN.md win. Change that line to name the Stitch exports |
| Checks | The build log records `npm run build` passing with 24 static routes | No frontend tests |

**Three decisions for you before any prompt runs**

1. **Styling.** The report says Tailwind and shadcn/ui, and the Stitch exports are Tailwind markup, so Tailwind is the cheaper path for the rebuilt screens. Adopting it means a DECISIONS entry (it changes the stack and needs an install approval), and the old CSS Modules stay until each page is rebuilt. Keeping CSS Modules means a DECISIONS entry and a change to the report's software list. Pick one and record it. Prompt F1 asks the agent to show both and wait.
2. **Where the design files live.** Add `design/` at the repo root with `DESIGN.md`, `stitch/` and the rename map. Do not make `/design/requirements.md`: point the agent to docs/context/requirements.md, which already exists.
3. **Mock mode.** It is on by default. Anyone who runs the app without reading the README sees fake data and believes it is live. Make the default off once the first screen is wired, and say on the screen when it is on.

**Rules the agents must follow here (from CLAUDE.md).** Plan first and wait for your yes. Never commit, push, delete or move files. Back up an existing file before editing it with `python scripts/backup.py snapshot <path>`. Ask before installing packages. Use PowerShell commands. Add a docs/build-log.md entry per finished screen, and a DECISIONS entry plus a pending-report row when a screen differs from the report's GUI section.

## 1. What the report chapter must say about the frontend

The frontend goes in subsection 6.1.3 of your implementation chapter (template Chapter 7). template.tex wants what you built, the platform, and the procedure, not code. Each figure needs a caption that describes the picture for a screen reader.

| Report part | Write | Evidence |
| --- | --- | --- |
| Platform | Next.js 16, React 19, TypeScript, Vercel hosting, pinned versions in package.json. Styling: the report says Tailwind and shadcn/ui and the repo uses CSS Modules, so write whichever you decide in Section 0 | package.json |
| Design system | The tokens from DESIGN.md: ink, paper, accent colour, type scale, spacing, one icon set, the canonical logo | Token file |
| Screens built | One short paragraph per role (founder, talent, mentor, investor, admin) and the shared screens, with a screenshot of the running app, not the Stitch export | Screenshots with captions |
| AI screen pattern | The five states: queued, loading, success, abstain, failure, and how each maps to the API response | A state figure |
| Navigation | The flow per role, matching the navigation figures already in the GUI section | Route list |
| What runs on mocks | A plain statement of which screens still use fixtures instead of the live API | Your task list |
| Frontend tests | Test cases TC-11 and TC-12 from the playbook (Section 19.3), plus the checks in Section 5 below | Test output |

One trap: the GUI section of main.tex promises ten more screens in D3 and a data dictionary. Build those screens before you claim them in the chapter. The list is in Section 3 below.

Show screenshots of the running app. A Stitch export is a prototype, and a panel will ask the difference.

## 2. What to give the coding agents from your prototypes

The code.html files are the best input you have, but they are throwaway Tailwind CDN pages with hard-coded sample data. The agent should read them as a visual spec and rebuild each screen as real components. It should not copy them.

Put these in the repository before the first prompt:

1. `/design/stitch/<P-code>/code.html` and `screen.png` for every screen you will build, renamed with the P-codes from the rename map (P10, P11 and so on). Do not give the agent all 85 folders. Give it the primary screens first, then each screen's states, mobile version, drawers and modals as you reach them.
2. `/design/DESIGN.md`, after the fixes listed in the earlier prototype review: the YAML colours corrected, one token vocabulary, one icon set, no `background-attachment: fixed`.
3. `/design/rename_map.csv`, so the agent knows that P10.m is the mobile version of P10 and that anything marked z is parked and must be ignored.
4. `/design/requirements.md`: copy only the FR and NFR lines for the user-facing features from main.tex (FR-1 to FR-31 and the NFRs on response time, consent and abstention). The agent should not read the whole report.
5. The API contract: `/backend/openapi.json` once the backend exports it. Until then, the endpoint table in the playbook (Section 11.1).

What the agent must change when it converts a prototype:

- Replace the Tailwind CDN script with a real Tailwind config built from the DESIGN.md tokens.
- Replace hard-coded names, numbers and dates with typed fixtures first, then API calls.
- Replace repeated markup with shared components: nav, page header, card, table, drawer, modal, form field, status chip, and the AI response panel.
- Keep the visual result. If a conversion changes spacing, type or colour, that is a bug.

## 3. Screen build order, routes and requirements

Build in this order. The first group needs no AI and no live data, and it carries most of the report's GUI promises. Requirement IDs come from main.tex. Routes are suggestions.

| Order | P-code | Screen | Route | Requirement |
| --- | --- | --- | --- | --- |
| 1 | P01, P02 | Sign in, application submitted | /login, /register | FR-22, FR-17, FR-23 |
| 1 | P00 | Landing | / | Public page |
| 2 | P10 | Founder dashboard | /founder | FR-1, FR-28 |
| 2 | P11 | Startup profile | /founder/profile | FR-1, FR-15 |
| 2 | P20, P21, P22 | Talent dashboard, job board, application tracker | /talent, /jobs, /applications | FR-6, FR-25 |
| 2 | P30, P40, P41, P50 | Mentor, investor, portfolio, admin console | /mentor, /investor, /admin | FR-29, FR-10, FR-26 |
| 2 | P60 | Mutual reveal | /introductions/\[id\] | FR-7 |
| 2 | P61, P62, P63 | Settings and consent, usage guides, consent protocol | /settings, /help | FR-27, FR-18 |
| 3 | P18, P19 | Job listings, applicants | /founder/jobs | FR-24 |
| 3 | P17 | Matches | /founder/matches | FR-7 |
| 4 | P13 | Compliance assistant (drawer) | any dashboard | FR-8 |
| 4 | P12, P14, P15, P16 | Readiness, market research, pitch practice, session feedback | /founder/readiness and so on | FR-2, FR-4, FR-3, FR-28 |
| 4 | P23 | Resume optimizer | /talent/resume | FR-5 |

**Screens main.tex promises that do not exist in your prototypes.** The GUI section says ten screens are added in D3. These have no prototype yet, so write the prototype first (Stitch), then build:

- Talent, mentor and investor profile screens
- Mentor requests screen
- Appeal form for a rejected profile (FR-21)

Check the exact list of ten against the GUI section of main.tex, since I could not recover it from the text. If you cut any of them, change the sentence in main.tex too.

## 4. Prompts F1 to F7, copy-paste

Merge the shared context into your existing AGENTS.md and CLAUDE.md, then run the prompts in order, one at a time. Review the diff and run the build after each one.

### Shared frontend context

```text
Project: The Founder's Carnet, an introduction-only startup ecosystem platform for Pakistan. Roles: founder, talent, mentor, investor, admin.
Frontend: /frontend, Next.js 16 (App Router), React 19, TypeScript, Node 24. Existing pages and components must be changed in place, never duplicated. Styling follows the decision recorded in docs/DECISIONS.md.
Read CLAUDE.md first. Its safety rules win over this prompt: plan first and wait for my yes, never commit, push, delete or move files, back up an existing file before editing it (python scripts/backup.py snapshot <path>), ask before installing any package, use PowerShell commands.
Design source of truth: /design/DESIGN.md and the Stitch exports in /design/stitch/<P-code>/ (code.html and screen.png). /design/rename_map.csv explains the codes: P10 is a primary screen, P10.m its mobile version, P10.s1 a state, P10.d1 a drawer, P10.x1 a modal. Ignore anything marked z.
Requirements: docs/context/requirements.md. Cite FR and NFR IDs in code comments.
Rules:
- Treat code.html as a visual spec. Rebuild it as typed React components. Never paste the Tailwind CDN script or inline style blocks.
- Colours, fonts, spacing, radius and icons come only from the tokens in DESIGN.md. Do not add colours or fonts.
- Use the canonical logo SVG from DESIGN.md exactly.
- Repeated markup becomes a shared component. Reuse the existing ones in src/components before adding any.
- Introduction only: no equity, no money handling, no compliance advice, no funding probability. Contact details stay hidden until both sides accept.
- Every AI output is visibly marked as written by a language model. The pitch counterpart is labelled a simulation.
- Sample data lives in typed fixtures in /src/fixtures, behind one API client that switches between fixtures and the real API. Say on screen when fixtures are in use.
- Accessible by default: labels, focus states, contrast, keyboard use, alt text.
- Show a short plan, wait for my yes, implement, then run the build and lint and report the real output. Do not claim a screen matches the prototype until you have compared it with screen.png at the same width.
- Add a docs/build-log.md entry per finished screen. If a screen differs from the report, add a DECISIONS entry with the reason and a row in docs/pending-report-changes.md.
```

### F1: project setup and design tokens

```text
Do not create a new project: /frontend already exists (Next.js 16, CSS Modules, components in src/components/ui and src/components/layout). Read /design/DESIGN.md, src/app/globals.css and the existing components. Then show me two options with their cost and wait for my choice: (A) add Tailwind, map the DESIGN.md tokens in its config and globals.css, and keep the existing CSS Modules working until each page is rebuilt; (B) keep CSS Modules and define the tokens as CSS custom properties in globals.css. Tell me which packages option A needs to install and why.
After I choose, apply the tokens: colours, type scale, fonts (load only the weights used), spacing, radius, shadows, the page background and the icon set. Add the logo component using the canonical SVG. Reuse and restyle the existing components (Badge, Button, Card, ConsentBox, EmptyState, Input, MatchCard, ProgressBar, Spinner, StatCard, Sidebar, PageHeader, DashboardLayout). Add only what is missing: select, table, tabs, modal, drawer, toast. Add one /styleguide page that renders every component in every state so we can compare it with the prototypes. Do not rebuild any product screen yet.
```

### F2: app shell, navigation and role routing

```text
Review the existing shell: DashboardLayout, Sidebar, PageHeader, AuthContext and src/lib/navigation.ts. The role route guards already work (a logged-out user goes to /login, another role's routes redirect to the user's own dashboard). Keep them, and change them only if the new prototypes require it, and ask first. Update the top bar, the mobile menu overlay and the navigation for each role from the new prototypes (P10, P20, P30, P40, P50 and their mobile versions). Add the shared pages P61 (settings and consent), P62 (usage guides) and P63 (consent protocol) if they do not exist. Keep the session mock behind the API client switch. Show the plan and wait for my yes before editing any file.
```

### F3: convert one screen (reuse this prompt for every screen)

```text
If the page already exists, edit it and never create a second one. Convert the prototype screen <P-CODE> (/design/stitch/<P-CODE>/code.html, screenshot screen.png) into a real page at <ROUTE>, for the role <ROLE>. Reuse the existing components, and add a new shared component only if two or more screens need it. Move all sample content into /src/fixtures/<name>.ts with TypeScript types that match the API contract for this screen (requirements: <FR-IDs>). Also build its mobile layout from <P-CODE>.m and any states, drawers or modals listed in /design/rename_map.csv under this code. Compare the result with screen.png at 1280 px and 390 px and list any difference you could not remove. Do not change the design.
```

Run F3 for the screens in the order of Section 3: auth, dashboards, profiles, job board and tracker, mutual reveal, job listings, matches.

### F4: auth, consent and account screens

```text
Review the existing login and register pages and the ConsentBox against P01 and P02, and change them in place. The backend registers a user with email, password and one role (founder, talent, mentor or investor; admin is never offered) and issues a token at login. Consent is stored with the founder profile and the ecosystem profile, not at registration, although FR-17 says consent comes before profile data. Do not change the backend. Build the form so the consent box must be ticked before submit, show the server's error messages, and add a status screen for the verification status and its reason (FR-15) using fixtures, because the backend has no verification endpoint yet. Add the consent and account-deletion controls from P61 (FR-27), also on fixtures. Write every gap you find to docs/api_gaps.md as a contract change request for the backend (method, path, request, response, the screen and requirement that needs it).
```

### F5: the AI response panel with five states

```text
Build one reusable AI response panel component that every AI screen uses, with five states: queued (shows 'High demand, you are number N' and a cancel button), loading (skeleton, about 8 seconds), success (structured output, the time it was generated, and a visible mark that a language model wrote it), abstain (the no-grounded-answer message and its reason), failure (message, retry button, the previous result kept). The component takes the API response type and renders the right state. Then use it in the compliance assistant drawer (P13, with citation expansion and the dated source list), readiness (P12), market research (P14, with evidence kept apart from interpretation and a partial-results notice), pitch practice (P15, P16, with the simulation label and transcript modal) and the resume optimizer (P23). Add a /dev/states page where every AI screen can be forced into each of the five states with a query parameter.
```

Backend note: today only the compliance route returns a result shaped for this panel (outcome answered or abstained, answer, message, abstention reason, citations with title, issuing body, source link, section, page, effective date, consolidation date and retrieval date). No route returns a queued state yet, because the gateway queues inside the process, so build the queued state from the component and test it with a fixture. Readiness and pitch endpoints exist. Market research and the resume optimizer have no endpoint yet.

### F6: screens that have no prototype yet

```text
I will put a new Stitch export for each of these in /design/stitch/. Several already exist as PlaceholderPage routes (talent profile, resume and matches, mentor profile and requests, investor profile, founders and requests): replace the placeholder, and do not add a second page. Build them in the same way as F3: talent profile, mentor profile, investor profile, mentor requests (accept or decline, with contact details revealed only after both sides accept), and the appeal form for a rejected profile (FR-21: one appeal, evidence text, the reviewer's final decision and reason). If an export is missing, stop and tell me which one.
```

### F7: polish, accessibility and report screenshots

```text
Run a pass over all built pages: keyboard navigation, focus order, visible focus, colour contrast against the tokens, alt text, form labels, and reduced-motion support. Fix the problems. Ask before installing Playwright, which is not in package.json. Then write a Playwright script that opens every page at 1280 px and 390 px with fixtures, in every AI state, and saves screenshots to /report/screens/<P-code>-<state>-<width>.png. List any page that fails to load. Do not alter the design to pass a check without telling me.
```

Ask the agent to include a plain-English description of each screenshot in the file name list, so you can reuse it as the figure caption description the template requires.

## 5. Frontend test cases and metrics for the report

These use the template's test case table. Keep the status at Not executed until you run the test, and put numbers in the metrics table only from tests you ran.

| ID | Test | How to run | Requirement |
| --- | --- | --- | --- |
| FT-01 | Each role lands on its own dashboard, and typing another role's URL redirects away | Playwright, one test per role | FR-23 |
| FT-02 | Registration cannot be submitted until the consent box is ticked | Playwright | FR-17 |
| FT-03 | Admin is not offered as a role at registration | Component test | FR-22 |
| FT-04 | Contact details are not rendered anywhere until both sides have accepted | Component test on the match and mutual reveal screens | FR-7 |
| FT-05 | The AI panel renders each of the five states from its fixture | Component test, five cases | Playbook 11.2 |
| FT-06 | Every AI output shows the mark that a language model wrote it | Component test | Use case text |
| FT-07 | An abstained compliance answer shows the reason and no citation list | Component test | NFR-13 |
| FT-08 | A successful compliance answer shows each citation with its source and date | Component test | NFR-12 |
| FT-09 | Every page loads at 390 px with no horizontal scroll | Playwright | Usability |
| FT-10 | Build, lint and type check pass with no errors | CI | Maintainability |

Two things belong in the chapter even though they are not test cases. First, the accessibility pass from F7, reported as the list of problems found and fixed. Second, the screenshot set, used as the report's GUI figures.

Metrics for the template table: number of test cases (10 if you keep this list), how many passed and failed, and defect density, which is failed times 100 divided by executed. Check each requirement ID against main.tex before you write it down. I confirmed FR-7, FR-17, FR-22, FR-23, NFR-12 and NFR-13 exist, but not every wording.

Test tooling: package.json has no test runner. The only check recorded so far is `npm run build`, which the build log says passes. FT-01 to FT-09 need Vitest with Testing Library and Playwright. Ask before the agent installs them, and write the decision in the build log.

## 6. Rules and known prototype problems

These came out of the earlier prototype audit. Fix them in code, since the agent will otherwise copy them.

- **Fonts.** Some screens fell back to Inter because two token vocabularies existed, and weight 600 was not loaded. Load only the weights the tokens use.
- **Colours.** Some screens leaked lavender from the old YAML tokens. The Tailwind config must contain only the DESIGN.md palette.
- **Background.** The `fixed` gradient made screenshots show a white top. Use a normal scroll background.
- **Logo.** A few screens do not use the canonical logo. Use one logo component everywhere.
- **Duplicate and parked screens.** Do not build anything marked z in the rename map.
- **Language-model label.** The report says AI output is marked as written by a language model. Your DESIGN.md says no AI-generated badges. Resolve it in favour of the report, with a small plain text mark, not a badge.
- **Claims on screen.** No screen may promise compliance advice, a funding probability, equity, or payment handling. Check every sentence that the prototypes invented, especially in market research, where sample figures can look like real data. Label sample numbers as sample data in the fixtures.
- **Matches must not call a language model.** Matching is similarity plus a re-ranker. Do not put a generated explanation on a match unless it comes from the stored factors (NFR-15).

If a prompt asks the agent to change the design, the agent is wrong. Design changes happen in Stitch and DESIGN.md first, then in code.

## 7. When frontend code already exists and new prototypes replace the old ones

Shahzeb built the current pages with Antigravity from the 12 wireframes in docs/context/wireframes (see the 2026-10-18 build-log entries), not from Stitch. Use this section to bring them in line with the new Stitch prototypes. The new prototypes decide what each screen should look like. The existing code decides nothing except what is worth keeping. The OpenAPI file from the backend decides what the data looks like.

### 7.1 Set up the folders and the precedence rule

1. Put the new exports in `/design/stitch-v2/<P-code>/` (code.html and screen.png), with an updated `/design/rename_map_v2.csv`. Move the old exports to `/design/stitch-v1/` and do not delete them.
2. Write this at the top of `/design/README.md` and in AGENTS.md:

```text
Precedence: (1) /design/stitch-v2 decides layout and content of each screen. (2) /design/DESIGN.md decides colours, type, spacing, icons and the logo. (3) /backend/openapi.json decides field names, types, states and errors. Anything in /design/stitch-v1 is obsolete and is never used as a reference. If two of these sources disagree, do not choose silently: write the conflict in /docs/frontend_conflicts.md and continue with the higher-precedence source.
```

3. Work on a new git branch, so the existing working pages stay safe on the main branch.

### 7.2 Prompt F8: audit first, change nothing

```text
Do not change any code in this task. Audit the existing frontend in /frontend against the new prototypes in /design/stitch-v2 and write /docs/frontend_audit.md.
For every screen in /design/rename_map_v2.csv (ignore anything marked z) give one row: P-code, screen name, route, and a status from this list: matches, partly matches, missing, or wrong role. For partly matches, list each difference (layout, content, states, mobile, drawer or modal missing, hard-coded data, wrong tokens). For each existing page with no prototype, list it as 'no prototype' and say whether it looks like working logic worth keeping. Also list every shared component and whether it is reused or duplicated, every place where a colour, font, icon or logo is hard-coded instead of coming from the tokens, and every place that uses fake data or a direct fetch instead of the API client.
End with a ranked list of what to fix first and a count of screens per status. Quote file paths. Do not guess: if you cannot tell, say so.
```

Read the audit yourself before the next step. If a screen is marked as matching and it plainly is not, reject the audit and run it again with that screen named.

### 7.3 Prompt F9: reconcile the code with the new prototypes

```text
Using /docs/frontend_audit.md, bring /frontend in line with /design/stitch-v2, one screen at a time, in the order of the ranked list, stopping after each one so I can review it and commit it myself. Keep working logic (auth, forms, state, routing) and move it into the shared components. Rebuild layout and content from the prototype. Pull every colour, font, spacing, icon and the logo from the tokens in /design/DESIGN.md only, and remove hard-coded values. Build the mobile version and every state, drawer and modal listed for the screen in the rename map. Never delete or move a page. If a page has no prototype, leave it where it is and list it in /docs/frontend_audit.md. Back up each existing file before editing it. After each screen, compare it with its screen.png at 1280 px and 390 px and list the differences you could not remove. Stop and ask before you change the router structure or the auth logic.
```

### 7.4 Prompt F10: sync the frontend with the backend

```text
Save the OpenAPI schema from the running backend (GET /openapi.json) as /backend/openapi.json (a new file, so ask me first). Generate a typed API client in /frontend/src/api from it, asking before you install a generator such as openapi-typescript, and make it the only place that calls the backend. Today only src/context/AuthContext.tsx and src/lib/auth.ts call it. Replace every fixture and direct fetch with it. For each screen, compare what the screen needs with what the endpoints return and write /docs/api_gaps.md with three lists: (a) mismatches the frontend should fix by changing field names, types or mapping; (b) data or endpoints the screen needs that the backend does not provide, each written as a contract change request for the backend (method, path, request, response, the screen and requirement that needs it); (c) endpoints the backend has that no screen uses. Do not invent endpoints and do not edit the backend. Fix list (a) in the frontend. Map API responses to the five AI states: 202 with a job id is queued, 200 is success, 200 with abstain true is abstain, 5xx or a timeout is failure. Show the backend's error message on forms. Keep the one-variable switch between fixtures and the real API. Add contract tests that fail when a response no longer matches the generated types.
```

Send list (b) of `api_gaps.md` to the backend agent as a prompt of its own: one change request at a time, then regenerate `openapi.json`, then rerun F10. The OpenAPI file is the only agreement between the two sides, so neither side should edit the other.

### 7.5 Prompt F11: verify against the new prototypes

```text
Run the app against the real backend in docker-compose. For every screen in /design/rename_map_v2.csv, log in as the right role, open the page at 1280 px and 390 px, and save screenshots to /report/screens-v2/. Produce /docs/frontend_verification.md with one row per screen: loads with real data (yes or no), matches the prototype (yes, partly, no, with the difference), every state reachable, errors from the backend shown. List every screen that still uses fixtures. Do not mark a screen done unless you opened it.
```

### 7.6 What to check yourself

- Open three screens from the audit that it marked as matching and compare them with the prototype by eye.
- Check that no screen gained a feature from the old code that the new prototype dropped. If the old code has working logic for something the new prototype removed, decide whether it stays.
- Check that `api_gaps.md` list (b) is short. A long list means the prototypes assume data the backend does not have, so tell your supervisor which screens depend on it, and do not hide the gap with fake data.
- Whatever is still on fixtures at the end goes in the report's "what runs on mocks" line.
