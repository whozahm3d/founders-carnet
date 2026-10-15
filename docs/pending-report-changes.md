# Pending report changes

Changes the code or tooling has already made that the report (`main.tex`), the master document and the diagrams do not yet reflect. Fix each one in the report later, add the `docs/DECISIONS.md` entry, then delete the row here.

| Date | What changed | Report says | Now | Where to fix | DECISIONS entry |
|---|---|---|---|---|---|
| 2026-10-15 | Node.js version | Node 20 | Node 24 | Every place the report names the Node version (stack and tools text, any technology table or deployment diagram) | Not yet added |

## Draft DECISIONS entry for the Node change

Copy this into `docs/DECISIONS.md` using the format in `docs/decision-entry-template.md`, and check the wording against the template.

> **2026-10-15: Move from Node 20 to Node 24.**
> Node 20 has passed its end-of-life date, and the GSD Core planning tool needs Node 24 or newer. The frontend, CI and all three machines use Node 24. The report still says Node 20 and must be updated. Not yet verified: a full `npm run build` of the Next.js app on Node 24 (there is no frontend code yet).

## Draft DECISIONS entry for `.planning/` (not a report change)

> **2026-10-15: GSD Core's `.planning/` folder stays out of git.**
> GSD Core keeps its plans, roadmap and state in `.planning/`. Each person's copy changes constantly and would conflict between three people, its default is to commit those files on its own, and `config.json` can hold API keys in plain text. So `.planning/` is in `.gitignore` and GSD's `commit_docs` is off. Decisions the team needs go into `docs/DECISIONS.md` and the report by hand. Revisit if more than one person starts using GSD for shared planning.

Before finalising, confirm the Node 20 end-of-life date from nodejs.org. It is stated here from memory.
