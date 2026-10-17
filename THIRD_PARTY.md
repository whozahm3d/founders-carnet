# Third-party material

Everything under `.claude/skills/`, `.claude/commands/` and `.claude/agents/` (except what is listed as ours) was copied from the public repositories below. The first batch was copied on 15 October 2026 and the second batch (section "Added to install") was added on 16 October 2026. Licenses are listed per row. Copies of the licenses go in `third_party_licenses/`. Keep them if the repo is shared.

**How it was checked.** Every included folder in the first batch was scanned for risky patterns: downloads, pipe-to-shell, delete commands, `eval`/`exec`, obfuscation, install commands, and phrases that try to override instructions. Every flagged line was read. The one script that runs commands (`webapp-testing/scripts/with_server.py`) was read in part. Not every line of every file was read, so treat these like any other dependency. The second batch has **not** been scanned yet (see the notes under that section). Ali's own Claude Code installs it; follow the final list below.

## Included

| What | From | Commit | License |
| --- | --- | --- | --- |
| 11 process skills: `spec-driven-development`, `planning-and-task-breakdown`, `incremental-implementation`, `test-driven-development`, `code-review-and-quality`, `debugging-and-error-recovery`, `security-and-hardening`, `api-and-interface-design`, `documentation-and-adrs`, `frontend-ui-engineering`, `source-driven-development` | github.com/addyosmani/agent-skills | aeac41d4 | MIT |
| `git-workflow-and-versioning`, `shipping-and-launch`, `ci-cd-and-automation`, `performance-optimization`, `observability-and-instrumentation`, plus the upstream `references/` folder (7 checklist files, copied to `.claude/references/` so the `../../references/` links in these skills and the 11 above resolve). Two local edits in `git-workflow-and-versioning/SKILL.md`: the `git reset --hard HEAD` line is rewritten to tell the team instead, and a two-line note under the title says the `CLAUDE.md` git rules win | github.com/addyosmani/agent-skills | aeac41d4 (same commit as the row above, re-checked 17 October 2026) | MIT (`addyosmani-agent-skills-MIT.txt`, same file as the row above) |
| `web-design-guidelines` (live download removed; rules saved as `command.md`, byte-identical to upstream). `SKILL.md` edited to read the local file, with one added line saying the Figma prototypes win on copy and style where the rules clash with `frontend-design` | github.com/vercel-labs/agent-skills (`skills/web-design-guidelines`) and github.com/vercel-labs/web-interface-guidelines (`command.md`) | skill 063bee94; rules 434b7f91 (downloaded 2026-10-16 22:20 UTC, SHA-256 d246b026f4f29b5823a9cc857f9edf3d2507002e055e32040cadeaf3b38e0234) | Skill: MIT per the repo README, no LICENSE file. Rules: MIT, Copyright (c) 2025 Vercel Labs (`vercel-labs-web-interface-guidelines-MIT.txt`) |
| `ponytail`, `ponytail-review`, `ponytail-audit`, `ponytail-debt` (skills only; `ponytail-help`, `ponytail-gain` and every hook file left out). Two local edits: the `ponytail` and `ponytail-review` descriptions now say "Use only when the user asks for it" instead of starting on any coding task, "code review" or "review my PR" | github.com/DietrichGebert/ponytail | 6f1c2bf | MIT, Copyright (c) 2026 DietrichGebert (`ponytail-MIT.txt`) |
| `fastapi` | github.com/fastapi/fastapi (`.agents/skills/fastapi`) | 0b919816 | MIT |
| `vercel-react-best-practices`, `vercel-composition-patterns` (folders renamed to match each skill's `name`) | github.com/vercel-labs/agent-skills | 063bee94 | MIT (stated in the skill files; the repo has no root LICENSE file) |
| `supabase-postgres-best-practices` | github.com/supabase/agent-skills | c9be0e93 | MIT |
| `train-sentence-transformers`, `huggingface-datasets` | github.com/huggingface/skills | c3ff942b | Apache-2.0 |
| `webapp-testing` | github.com/anthropics/skills | dbd4588f | Apache-2.0 |
| `frontend-design`, `claude-api` (`claude-api` trimmed to `SKILL.md`, `curl/`, `python/`, `typescript/` and `shared/`; `csharp/`, `go/`, `java/`, `php/`, `ruby/`, `shared/preserved-thinking-migration/` and `shared/preserved-thinking-migration.md` left out) | github.com/anthropics/skills | dbd4588f | Apache-2.0 |
| `python-patterns`, `python-testing`, `verification-loop` | github.com/affaan-m/ECC | b92f181b | MIT |
| `/feature-dev` command and three read-only agents (`code-explorer`, `code-architect`, `code-reviewer`) | github.com/anthropics/claude-plugins-official (`plugins/feature-dev`) | 8f814f49 | Apache-2.0 |
| `humanizer` | Your claude.ai account (skill v2.9.0; same file as `humanizer.skill` in the Project) | not tracked | MIT (stated in the skill file) |
| `anti-ai-writing` | Your claude.ai account (plugin, github.com/avectats7/anti-ai-writing) | not tracked | MIT |
| `explore-data`, `statistical-analysis`, `validate-data`, `sql-queries` | Your claude.ai account (Anthropic `data` plugin) | not tracked | Apache-2.0 |

The last three rows were copied from the skills synced to your account on 15 October 2026, not cloned from GitHub, so there is no commit hash. Same scan as above, no flagged lines other than word lists.

Ours, not third-party: `.claude/settings.json`, `.claude/hooks/guard.py`, `.claude/skills/report-code-sync/`, `scripts/backup.py`, `scripts/backup_config.json`, `scripts/scan_for_keys.py`, `scripts/sync_agent_skills.py`, `.githooks/pre-commit`, `.github/` files, `docs/datasets.md`, `docs/decision-entry-template.md`, `env.example`, `CLAUDE.md`, `AGENTS.md`, `SETUP.md`.

Things to know:

- `webapp-testing` starts whatever server command you give it. It needs `pip install playwright` and a browser install before first use.
- `train-sentence-transformers` has a reference page that mentions a paid Hugging Face Jobs option and a `curl ... | bash` line to install their CLI. It is documentation only. `CLAUDE.md` already tells Claude to ask before paid services or installs.
- Anything that fetches web content (the `fastapi` skill links to its docs, `source-driven-development` tells Claude to read official docs) can pull in text you have not reviewed. Do not paste secrets into a session that is browsing.

## Final install list (decided 16 October 2026)

This is the list Ali's Claude Code installs. It replaces the "install note" wording in the tables below where they differ. Nothing outside this list is installed (`CLAUDE.md` still says to ask before adding anything).

**Install into the repo (committed, so all three get them)**

| What | From | Where it goes |
| --- | --- | --- |
| `frontend-design`, `claude-api` | anthropics/skills | `.claude/skills/<name>/` |
| `git-workflow-and-versioning` and the launch, CI/CD, performance and observability skills | addyosmani/agent-skills | `.claude/skills/<name>/`. Remove or rewrite every `git reset --hard` line first |
| `web-design-guidelines` | vercel-labs/agent-skills | `.claude/skills/web-design-guidelines/`. Copy the rules file in and remove the live download |
| `graphify` | Graphify-Labs/graphify | `uv tool install graphifyy`, then `graphify install --project`. After the first services exist. Steps below |
| ponytail (4 skills, skills only) | DietrichGebert/ponytail | `.claude/skills/<name>/`. Installed 17 October 2026. No hook files copied. The `ponytail` and `ponytail-review` descriptions are trimmed so they start only when asked. caveman and gstack: skipped (see "Not installing") |
| `DESIGN.md` | VoltAgent/awesome-design-md (MIT) | Project root. One brand only. **Which brand is not decided; discuss after most of the functionality is done. Do not install it before then.** Figma prototypes stay the UI source |

**Install per person, never commit**

| What | Why |
| --- | --- |
| `docx`, `pdf`, `pptx`, `xlsx` (anthropics/skills) | Anthropic license is all rights reserved |
| `code-review` plugin (claude-plugins-official) | Posts to GitHub pull requests; only when a person asks |
| my-claude-skills, awesome-claude-skills | No license file |
| rea (`npx rea-agents setup`) | MCP server |
| gsd-core, ECC (see `SETUP.md` sections 6 and 10) | Installer-based, hooks off |
| spec-kit (`specify-cli`) | Installed on each person's own laptop with `uv tool install specify-cli==<version pinned at install>`. Nothing is copied into the repo and it is not installed yet. Source read at 2b43eef (github.com/github/spec-kit), MIT, Copyright GitHub, Inc. `specify init` writes `.specify/` and agent commands, so it needs its own OK. Overlaps `spec-driven-development`: use one of the two per feature |

**Not installing:** codebase-memory-mcp, claude-swarm, screenshot-to-code, AgentForge-AIOrchestrator.

- caveman (read 17 October 2026 at d262ab3, Apache-2.0): skipped. Its own README says the core skill gives 3% fewer output tokens than a plain "Answer concisely." control, "inside the noise". Most of its other skills use the hosted Caveman Cloud gateway or rewrite `CLAUDE.md`-style files.
- gstack (read 17 October 2026 at 3e8b34d, MIT): skipped. It is not skills-only: each skill starts by running `~/.claude/skills/gstack/bin/gstack-skill-start` from a separate runtime install (`./setup`) and has a telemetry step. Its hooks and its workflows that commit, push, open pull requests, merge and deploy (`ship`, `land-and-deploy`) clash with `CLAUDE.md`.

**Read first, install only if Ali says yes:** career-ops, financial-services, replica-skill (section F). Claude Code reads each one, reports in a few lines, and waits.

**Reference only (not installed):** agents.md, awesome-free-llm-apis, and the tools in section E.

**After installing:** add a row for each new skill to the table in `CLAUDE.md`, fill in the commit and license columns here, copy each license into `third_party_licenses/`, and run `python scripts/sync_agent_skills.py` so Codex and Antigravity see the same skills (they read `.agents/skills/`, not `.claude/skills/`). The script also copies `.claude/references/` to `.agents/references/`, so the `../../references/` links in the skills resolve.

## Added to install (16 October 2026)

These were left out of the first batch. They are now on the install list for project design, context and token management, architecture, backend help, and multi-agent coding. Commit and license are filled in when each one is installed, because they were not read in depth when this list was written. Pin the commit at install time and copy the license into `third_party_licenses/`.

**Rules for every row below:** no hooks that run on their own, no autonomous deletes or edits, and `CLAUDE.md` still wins when a skill disagrees with it. Where a row says "hooks off" or "per person", follow that instead of copying files into the repo.

### A. Single skills from repos already used

| What | From | Skipped before because | Install note |
| --- | --- | --- | --- |
| `docx`, `pdf`, `pptx`, `xlsx` | github.com/anthropics/skills | Anthropic license says all rights reserved. | Install per person from the repo or claude.ai. **Do not commit the files.** |
| `frontend-design` | github.com/anthropics/skills | Could pull the UI away from the Figma prototypes. | Install. Figma prototypes stay the source for the UI. |
| `claude-api` | github.com/anthropics/skills | For Claude, and the project uses Gemini. | Install for LLM Gateway and prompt design reference only. |
| `code-review` plugin | github.com/anthropics/claude-plugins-official (`plugins/code-review`) | Posts comments on GitHub pull requests by itself and runs five parallel agents. | Install per person. Do not let it post to the repo without a person asking each time. |
| `git-workflow-and-versioning`, launch, CI/CD, performance, observability skills | github.com/addyosmani/agent-skills | `git-workflow-and-versioning` recommends `git reset --hard`, which `CLAUDE.md` blocks. | Install the folders. Remove or rewrite every `git reset --hard` line in `git-workflow-and-versioning` before use. |
| `web-design-guidelines` | github.com/vercel-labs/agent-skills | Downloads its rules from a live GitHub URL every time it runs. | Install, but copy the rules file into the skill folder and remove the live download. |

### B. Whole repos

| Name | Link | Role in the project | Install note |
| --- | --- | --- | --- |
| gsd-core | <https://github.com/open-gsd/gsd-core> | Context and task management for multiple agents | Installer-based, Node 24, do not copy by hand. `core` profile only, hooks off. See `SETUP.md` section 10. Version mismatch open (1.17.0 vs 1.12.0): pin one. |
| ECC (full plugin) | <https://github.com/affaan-m/ECC> | Agents, rules, backend and Python/TypeScript patterns | `npx ecc-universal@2.2.3 setup`, Global scope, **hooks off**, rules `common` + `python` (+ `typescript` for frontend). See `SETUP.md` section 6. |
| **graphify** | <https://github.com/Graphify-Labs/graphify> | Code graph for context and token savings | **Install now.** README read on 16 October 2026. Apache-2.0 / MIT. Installs as a `/graphify` skill. Steps in "Setup via Claude Code" below. Run it once the first services exist. |
| codebase-memory-mcp | <https://github.com/DeusData/codebase-memory-mcp> | Codebase memory for context and token savings | **Not installing.** README read: the installer is `curl ... \| bash`, edits agent config, adds Claude Code hooks, starts a background daemon and a file watcher. It conflicts with the hooks rule and overlaps graphify. |
| claude-swarm | <https://github.com/affaan-m/claude-swarm> | Multi-agent coding | **Not installing.** README read: standalone Python CLI that needs a paid `ANTHROPIC_API_KEY` and edits files through worker agents on its own. Claude Code subagents and worktrees cover the same need. |
| AgentForge-AIOrchestrator | <https://github.com/Pavan03062006/AgentForge-AIOrchestrator> | Multi-agent orchestration | **Not installing.** README read: standalone web app that needs a Supabase project, and it states no license, so it cannot go in the repo. |
| spec-kit | <https://github.com/github/spec-kit> | Spec-driven architecture workflow | **Install per person, not installed yet.** MIT. `uv tool install specify-cli==<version>` on each laptop; nothing is copied into the repo. Source read at 2b43eef. Has its own command-line workflow. Overlaps `spec-driven-development`, so use one of the two per feature. |
| agents.md | <https://github.com/agentsmd/agents.md> | `AGENTS.md` format spec | Format spec, no skill. Our `AGENTS.md` already follows it. Reference only. |
| awesome-design-md | <https://github.com/VoltAgent/awesome-design-md> | Design reference files for the frontend | **Install.** README read: nothing to install, you copy one brand's `DESIGN.md` into the project root. MIT. The UI still follows the Figma prototypes. |
| screenshot-to-code | <https://github.com/abi/screenshot-to-code> | Design-to-code | **Not installing.** README read: standalone web app (Poetry + pnpm) that needs an OpenAI, Anthropic or Gemini API key. Not usable from Claude Code. |
| awesome-free-llm-apis | <https://github.com/mnfst/awesome-free-llm-apis> | Options for the LLM Gateway | Reference list. Read, do not install. |
| **rea** (REA: Reverse Engineer Anything) | <https://github.com/morluto/rea> | Reverse engineering across binaries, applications and runtime behavior, for agents | **Install now.** MIT. Added on request. It is an MCP server: `npx rea-agents setup` (or `npm install --global rea-agents`). The repo's skill is under `.agents/skills`, and skills.sh lists it as `morluto/rea/reverse-engineer-anything`. Install per person. Steps in "Setup via Claude Code" below. |

### Setup via Claude Code (graphify and rea)

Each of the three of you runs these on your own machine, from the repo root. They are tools that install themselves, so nothing is copied by hand. Do not commit tool caches or their output unless a step says so.

**graphify** (Python 3.10+, `uv` recommended). Run it after the first services exist. The repo has no code to map yet.

1. `uv tool install graphifyy` (the package name has two y's; other `graphify*` packages are not affiliated). `pipx install graphifyy` also works.
2. `graphify install --project` writes `.claude/skills/graphify/SKILL.md` for this project only. Commit that folder so the others get the skill.
3. In Claude Code, run `/graphify .` to build the graph. Output goes to `graphify-out/` (`GRAPH_REPORT.md`, `graph.json`, `graph.html`). Add `graphify-out/` to `.gitignore` if it is large or regenerated.
4. Set `GRAPHIFY_QUERY_LOG_DISABLE=1` in your shell profile to stop it logging every query to `~/.cache/graphify-queries.log`.
5. **Do not run `graphify hook install`.** It adds git hooks that rebuild the graph on commit and checkout, which breaks the no-auto-run-hooks rule.
6. The README says `graphify install` also registers a Claude Code hook that fires before search and file-read calls and nudges the agent toward the graph. It only adds a hint, but it is an auto-running hook. Check `.claude/settings.json` after step 2 and remove it if you do not accept that.
7. Code is parsed locally. Docs, PDFs and images it indexes are sent to the model, so keep secrets and private files out of the folders you point it at.
8. Optional MCP mode: `uv tool install "graphifyy[mcp]"`. Not part of the default setup.

**rea** (Node.js and npm).

1. `npx rea-agents setup`, or `npm install --global rea-agents` for the `rea` CLI.
2. The skill is also listed on skills.sh as `morluto/rea/reverse-engineer-anything`. Its files live under `.agents/skills` in the repo.
3. It is an MCP server, so register it per person, not in the shared repo. Run `/mcp` in Claude Code to confirm it connected.
4. Setup details beyond these commands were not on the README page I read. If `npx rea-agents setup` asks to change your agent config or add hooks, read what it will do before accepting.

**Project context (not a tool).** Graphify maps code, not the report. The report's context goes in short markdown files under `docs/context/`, referenced from `CLAUDE.md` and `AGENTS.md`. Those files are written after the report edits are final.

### C. Conflict with the hooks rule: install only with hooks off

| Name | Link | Problem | Install note |
| --- | --- | --- | --- |
| ponytail | <https://github.com/DietrichGebert/ponytail> | Installs hooks that run on their own. | Installed 17 October 2026: 4 skills only, no hook files copied. The `ponytail` and `ponytail-review` descriptions are trimmed so they start only when asked. |
| caveman | <https://github.com/JuliusBrussee/caveman> | Very short replies and 26 auto-running hook files. | Skipped after reading it (see "Not installing"). Its own README calls the gain "inside the noise". |
| gstack | <https://github.com/garrytan/gstack> | Auto-running hooks and workflows that conflict with our rules. | Skipped after reading it (see "Not installing"). Not skills-only: it needs a runtime install and has hooks and deploy workflows. |

### D. No license file: install per person, never commit

| Name | Link |
| --- | --- |
| my-claude-skills | <https://github.com/mar-antaya/my-claude-skills> |
| awesome-claude-skills (864 skill folders) | <https://github.com/ComposioHQ/awesome-claude-skills> |

Without a license these cannot be redistributed. Each of the three of you installs them from the source repo. Do not put the files in this repo.

### E. Tools and platforms, not skill packs

Listed so nothing is dropped. These are applications or libraries, so they are **not** copied into `.claude/skills/`. Use them as tools or reading.

| Name | Link |
| --- | --- |
| firecrawl | <https://github.com/firecrawl/firecrawl> |
| opik | <https://github.com/comet-ml/opik> |
| openclaw | <https://github.com/openclaw/openclaw> |
| hermes-agent | <https://github.com/NousResearch/hermes-agent> |
| OmniRoute | <https://github.com/diegosouzapw/OmniRoute> |
| open-design | <https://github.com/nexu-io/open-design> |
| claude-agent-sdk-python | <https://github.com/anthropics/claude-agent-sdk-python> |
| claude-cookbooks | <https://github.com/anthropics/claude-cookbooks> |
| claude-code | <https://github.com/anthropics/claude-code> |

### F. Judged unrelated, now listed for a recheck

| Name | Link |
| --- | --- |
| career-ops | <https://github.com/career-ops-hq/career-ops> |
| financial-services | <https://github.com/anthropics/financial-services> |
| replica-skill | <https://github.com/Jakeschincariol/replica-skill> |

These were judged from names and folder layout, not read in depth. Read each one before installing.

## Skills and Codex or Antigravity

Codex reads skills from `<repo>/.agents/skills`. Antigravity reads workspace skills from `<project>/.agents/skills/`. Neither reads `.claude/skills`. `scripts/sync_agent_skills.py` copies `.claude/skills/*` into `.agents/skills/`, and also copies `.claude/references/` into `.agents/references/` because the skills link to `../../references/*.md` (copy only, never deletes). `.agents/skills/` is in `.gitignore`, so `.claude/skills/` stays the one source. Run the script after pulling.

## Left out, and why

**Still to be decided (not installed yet):** the `DESIGN.md` brand (after most functionality is done), and whether to install career-ops, financial-services and replica-skill (after Claude Code reads them). See also "Not in report" in `docs/context/coding-plan.md`.

**From your claude.ai account (about 1,000 skills in ~150 plugins), I took 6 and left the rest.** They are still available to you in claude.ai, Desktop and cloud sessions through your account. They are not in the repo, so teammates do not get them.

- `ali-ahmad`: your personal voice profile, with email samples and personal details. It should not go in a repo three people share. Copy it by hand if you want it.
- `probabl-skills` (ML pipeline skills): they run on `pixi` and `skore`, which clash with the `.venv` and `pip` rule in `CLAUDE.md`.
- `humanize-kit`: needs a saved voice profile to work.
- `superpowers`, `engineering`, `figma`, `huggingface-skills` (rest), `ml-pipeline`, `resume-tailoring`, `deep-research`: large, overlapping with skills already here, or tied to tools you have not set up, or no license file in the synced copy. Ask if you want any of them.
- Twilio, Unity, Zoom, Salesforce, AWS, Databricks, Shopify, SEO, sales and similar plugins: unrelated to this project.
- Harness tooling plugins (harness-architect, bc-harness, harnesskit, harness-init, harness-bootstrap, context-handoff): in the account only, not bundled.

**Added by me, not on your list:** `fastapi`, the two Vercel skills, `supabase-postgres-best-practices`, `train-sentence-transformers` and `huggingface-datasets`. Each is a good match for FastAPI, Next.js, Postgres with pgvector, and the FYP-2 re-ranker.

**Optional personal installs** (`SETUP.md` section 8, not bundled): claude-md-management, claude-code-setup, claude-context-optimizer.
