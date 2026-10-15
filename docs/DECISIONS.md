# Decisions log

Dated entries, newest first. Each entry has the context, what was tried, what was found, what was decided, and why. Add an entry every time the code or the report is changed so the two agree.

## 2026-10-15: Move from Node 20 to Node 24

**Context:** Node.js version used in the frontend, CI, and all development machines.

**What we tried:** Installed Node 24 on the frontend, CI, and all three machines to meet GSD Core's requirement of Node 24 or newer.

**What we found:** Node 20 reached end of life on 2026-04-30. GSD Core declares `engines.node >= 24.0.0` in its package.json. Not yet verified: a full `npm run build` of the Next.js app on Node 24 (there is no frontend code yet).

**Decision:** The report still says Node 20 and must be updated to Node 24 wherever it names the Node version.

**Why:** Node 20 is end-of-life and the planning tool requires Node 24 as a minimum.

**Follow-ups:** Update main.tex and the master document to name Node 24 in the stack and tools text, any technology table, and deployment diagram. No team member needs to act separately.

## 2026-10-15: Python 3.11 only, in every folder

**Context:** Python version used in backend, RAG, and ML folders, each with its own `.venv`.

**What we tried:** Installed Python 3.11.9 (the last 3.11 release with a Windows installer) on all three machines. Python 3.14 was removed from the lead machine.

**What we found:** Each folder uses Python 3.11 in its own virtual environment. One version avoids "works on my machine" differences between three laptops, and CI uses the same version.

**Decision:** The report must name Python 3.11 wherever it names a Python version (stack and tools text, any technology table, the ML and RAG environment description).

**Why:** A single version prevents environmental drift across the team.

**Follow-ups:** Update main.tex and the master document. No team member needs to act separately.

## 2026-10-15: GSD Core's `.planning/` folder stays out of git

**Context:** GSD Core (planning tool) keeps its plans, roadmap, and state in the `.planning/` folder.

**What we tried:** GSD Core's default is to commit those files on its own. Its config.json can hold API keys in plain text, and each person's `.planning/` copy changes constantly.

**What we found:** Committing `.planning/` would cause merge conflicts between three people and expose secrets. We added `.planning/` to `.gitignore` and turned off GSD's `commit_docs` setting.

**Decision:** Decisions the team needs to track go into `docs/DECISIONS.md` and the report by hand. No report change is needed.

**Why:** Avoids merge conflicts on personal state and reduces the risk of committing secrets.

**Follow-ups:** Revisit this decision if more than one person starts using GSD for shared planning across the team.
