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
| `graphify` (skill folder: `SKILL.md` and `references/`; `.graphify_version` left out). Installed 2 November 2026 with `uv tool install graphifyy==0.9.100`, then `graphify install --project --platform agents` (skill-only; plain `--project` also edits `CLAUDE.md` and `.claude/settings.json`, so it was not used). One local edit: the `SKILL.md` description starts only when asked. Tool is personal (uv tool on Ali's machine), skill folder is in the repo. **Personal tool, not required by the FYP.** | github.com/Graphify-Labs/graphify | 32e5efe (PyPI `graphifyy` 0.9.100) | Apache-2.0 plus MIT, see `NOTICE` (`graphify-Apache-2.0.txt`, `graphify-MIT.txt`, `graphify-NOTICE.txt`) |

The last three rows were copied from the skills synced to your account on 15 October 2026, not cloned from GitHub, so there is no commit hash. Same scan as above, no flagged lines other than word lists.

Ours, not third-party: `.claude/settings.json`, `.claude/hooks/guard.py`, `.claude/skills/report-code-sync/`, `scripts/backup.py`, `scripts/backup_config.json`, `scripts/scan_for_keys.py`, `scripts/sync_agent_skills.py`, `.githooks/pre-commit`, `.github/` files, `docs/datasets.md`, `docs/decision-entry-template.md`, `env.example`, `CLAUDE.md`, `AGENTS.md`, `SETUP.md`.

Things to know:

- `webapp-testing` starts whatever server command you give it. It needs `pip install playwright` and a browser install before first use.
- `train-sentence-transformers` has a reference page that mentions a paid Hugging Face Jobs option and a `curl ... | bash` line to install their CLI. It is documentation only. `CLAUDE.md` already tells Claude to ask before paid services or installs.
- Anything that fetches web content (the `fastapi` skill links to its docs, `source-driven-development` tells Claude to read official docs) can pull in text you have not reviewed. Do not paste secrets into a session that is browsing.

## Install log, per-person tools (2 November 2026)

Tools installed on Ali's machine only. Nothing here is copied into the repo unless the "Where" column says so. Where a row says "installed" it supersedes any "not installed yet" wording further down this file.

**Everything in this table is a personal tool, not required by the FYP.** Where each lives (decided 3 November 2026): the normal Claude Code configuration (`~/.claude`) stays free of auto-running hooks and may hold hook-free tools (skills, MCP servers, plugins without hooks); every hook-based tool goes in the separate personal-tools profile (`CLAUDE_CONFIG_DIR=C:\Users\pakistan\.claude-hooks`), which is launched only outside this repository.

| What | Source | Version or commit | Licence | Date | Where | FYP status |
| --- | --- | --- | --- | --- | --- | --- |
| spec-kit (`specify` CLI) | github.com/github/spec-kit, PyPI `specify-cli` | 1.2.6 (tag v1.2.6, commit 9eacc24) | MIT, Copyright GitHub, Inc. | 2026-11-02 | personal (`uv tool install specify-cli==1.2.6`). `specify init` not run | personal tool, not required by the FYP |
| `docx`, `pdf`, `pptx`, `xlsx` skills | github.com/anthropics/skills, delivered through Ali's claude.ai account (`anthropic-skills:*`) | not tracked | Anthropic, all rights reserved | 2026-11-02 | personal, already available, nothing installed or copied. Never commit these files | personal tool, not required by the FYP |
| `code-review` plugin | github.com/anthropics/claude-plugins-official (`plugins/code-review`) | 1.0.1 (marketplace copy has no git commit) | Apache-2.0 | 2026-11-02 | personal (`claude plugin install code-review@claude-plugins-official --scope user`). No hooks, no MCP server. Posts to GitHub only with `--comment` | personal tool, not required by the FYP |
| my-claude-skills: `ci-cd-pipeline-builder`, `dependency-auditor`, `performance-profiler`, `pr-review-expert`, `skill-security-auditor`, `tech-debt-tracker` (all 6) | github.com/mar-antaya/my-claude-skills | a67d698 | **None (no LICENSE file)** | 2026-11-02 | personal only: copied to `~/.claude/skills/`. Never copy into the repo or `.claude/skills/`. Restored 2026-11-03: `ci-cd-pipeline-builder` and `performance-profiler` were deleted by mistake and re-copied from the clone at a67d698 (byte-identical) | personal tool, not required by the FYP |
| career-ops (standalone folder, not a plugin: the plugin form adds a `SessionStart` hook, so it was not used) | github.com/career-ops-hq/career-ops | 20b9fd3 (v1.38.0) | MIT, Copyright (c) 2026 Santiago Fernández de Valderrama | 2026-11-02 | personal: `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm install` in `~/claude-tools/career-ops`, Chromium not downloaded. Nothing in the repo. Needs the user's own AI key in a `.env` there | personal tool, not required by the FYP |
| replica-skill: `replica-recon`, `replica-diff`, `replica-test`, `replica-design`, `replica-build`, `replica-brand`, `replica-entrepreneur`, `replica-launch` (8 of 11; the last three added 2026-11-03) | github.com/Jakeschincariol/replica-skill | 77c9436 | MIT, Copyright (c) 2026 Jake Schincariol | 2026-11-02 | personal: copied to `~/.claude/skills/`. Not in the repo. The Figma prototypes and `DESIGN.md` win over `replica-design` and `replica-build` where they disagree. Not installed (all six read on 3 November 2026: no hooks, scripts offline; these three push a different stack or a live-shipping workflow): `replica-architect`, `replica-backend`, `replica-deploy`. Restored 2026-11-03: `replica-design` and `replica-build` were deleted by mistake and re-copied from the clone at 77c9436 (byte-identical). Placement decided 2026-11-03: `replica-design` and `replica-build` stay in the main config (`C:\Users\pakistan\.claude\skills\`) because they are hook-free. A redundant byte-identical copy, made earlier the same day, is in the personal-tools profile at `C:\Users\pakistan\.claude-hooks\skills\`; Ali may remove it. `replica-brand` points at `../replica-design/contrast.py`, which resolves in the main config | personal tool, not required by the FYP |
| financial-services | github.com/anthropics/financial-services | 6056506 | Apache-2.0 | 2026-11-02 | **read, not installed** (wrong domain, paid data connectors, scope excludes investment advice) | personal tool, not required by the FYP |
| ECC (`ecc-universal`, plugin `ecc@ecc`) | github.com/affaan-m/ECC | b38be6a (npm 2.2.3, current `latest`) | MIT, Copyright (c) 2026 Affaan Mustafa | 2026-11-03 read; approved 2026-11-03 | **approved 3 November 2026, nothing installed.** Used only through `claude --plugin-dir C:\Users\pakistan\claude-tools\ecc` (pinned clone, commit b38be6a) in the separate hooks profile, never in the main config or founders-carnet. Hooks stay disabled with `ECC_HOOKS_ENABLED=false` until Ali changes that. The plugin registers 27 hook entries across 8 events (an earlier note said 26 across 9; that was wrong); "off" only disables them, each still starts `node`, and the flag defaults to on if missing. `stop:format-typecheck` rewrites JS/TS files (`prettier` or `biome --write`) after a response. Rules `common` + `python` (16 files, copied 2026-11-03) live only in `C:\Users\pakistan\.claude-hooks\rules\ecc\`, not in the path `SETUP.md` section 6 gives. Brings 71 agents, 98 commands, 314 skills. `plugin.json` registers no MCP servers. Its `config-protection` and `gateguard` hooks share the Write/Edit matcher with `.claude/hooks/guard.py` if ever enabled. `SETUP.md` section 6 says "hooks off" removes them, which is not what the source shows | personal tool, not required by the FYP |
| caveman | github.com/JuliusBrussee/caveman | 4.0.1, commit 2e068f7 | Apache-2.0 (older MIT file kept; see `LICENSING.md`) | 2026-11-02 read; approved 2026-11-03 | **approved 3 November 2026, nothing installed.** Used only through `claude --plugin-dir C:\Users\pakistan\claude-tools\caveman` (pinned clone) in the separate hooks profile, never in the main config or founders-carnet. The Claude plugin registers 4 hook entries: SessionStart and SubagentStart (`caveman-activate.js`), UserPromptSubmit (`caveman-mode-tracker.js`), SessionEnd (`caveman-stats.js --record`). It writes under `$CLAUDE_CONFIG_DIR`; its user config is `%APPDATA%\caveman\config.json`. If active in the repo it conflicts with CLAUDE.md: terse replies against the plain-words rule, and `caveman-compress`, `-optimize` and `-setup` can rewrite instruction files. The CLI (not the plugin) sends usage telemetry by default. Do not use the `curl … \| bash` installer | personal tool, not required by the FYP |
| gstack | github.com/garrytan/gstack | commit 82db89a | MIT, Copyright (c) 2026 Garry Tan | 2026-11-03 | **read again, kept skipped.** All 62 skill files and the skill hooks hardcode `~/.claude/skills/gstack`, so a `CLAUDE_CONFIG_DIR` profile cannot isolate it. `setup` registers hooks in `settings.json` and needs Bun (not installed). `ship` and `land-and-deploy` commit, push, open PRs, merge and deploy; `redact_prepush_hook` writes a git hook; `gstack-team-init` writes `.claude/` and `CLAUDE.md` into a repo. A fake-HOME experiment in `claude-lab` is possible later and was not done | personal tool, not required by the FYP |
| codebase-memory-mcp | github.com/DeusData/codebase-memory-mcp | release v0.12.1 (published 2026-10-16); source read at commit 2921415 (also shows 0.12.1) | MIT, Copyright (c) 2025 DeusData | 2026-11-03 | **dropped by Ali on 3 November 2026; to be removed by hand (graphify is kept instead, they overlap).** Earlier the same day it was installed in reduced form (MCP only, hooks profile only): Release zip `codebase-memory-mcp-windows-amd64.zip` (48,508,123 bytes) verified: SHA-256 `4e4e0f16b45233af5c757a1fcbe3c3b16e9056375b1fbe2ce020b6de75dedcc0` matches the GitHub API digest and `checksums.txt`. Extracted to `C:\Users\pakistan\claude-tools\cbm\v0.12.1\extracted\` (exe unsigned, 333,716,480 bytes). `install.ps1` NOT run: it downloads `latest`, not v0.12.1, and installs hooks, agents, a PATH change and the daemon. Registered with `claude mcp add --scope user` only in the hooks profile (`C:\Users\pakistan\.claude-hooks\.claude.json`), `CBM_CACHE_DIR=C:\Users\pakistan\.claude-hooks\cbm-cache`, `watcher_enabled=false`, `auto_index` off. No Claude hooks installed. 17 MCP tools. Repository not indexed; never use `persistence: true` in founders-carnet. Overlaps graphify. The source read (HEAD) may differ from the release build. Sigstore bundle not verified (no `cosign`) | personal tool, not required by the FYP |
| claude-swarm | github.com/affaan-m/claude-swarm | 0.2.0, commit 9b1c556 | MIT, Copyright (c) 2026 Affaan Mustafa | 2026-11-03 | **read again, reference clone only, not installed.** Python CLI and library (not a skill; no `SKILL.md`). Needs a paid `ANTHROPIC_API_KEY` for real runs (`--demo` needs none). Its worker agents run with `permission_mode="acceptEdits"`. PyPI ownership of the name `claude-swarm` not checked. Clone: `C:\Users\pakistan\claude-tools\claude-swarm` | personal tool, not required by the FYP |
| screenshot-to-code | github.com/abi/screenshot-to-code | commit a813977 | MIT, Copyright (c) 2023 Abi Raja | 2026-11-03 | **read again, reference clone only, not installed.** Local web app (FastAPI + React + Playwright Chromium; Poetry and pnpm), not a skill. Needs one of `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, and `REPLICATE_API_KEY` is recommended; uploaded screenshots go to the chosen provider. Conflicts with "Figma prototypes win". Clone: `C:\Users\pakistan\claude-tools\screenshot-to-code` | personal tool, not required by the FYP |
| AgentForge-AIOrchestrator | github.com/Pavan03062006/AgentForge-AIOrchestrator | commit f19bcd6 | **none (no LICENSE file)** | 2026-11-03 | **read again, reference clone only, not installed.** FastAPI + Next.js web app on Supabase (needs a Supabase project, DB password in `backend/.env`, `OPENROUTER_API_KEY`, `NVIDIA_API_KEY`); schema disables RLS by design. Personal reference only, never in the repo. Clone: `C:\Users\pakistan\claude-tools\AgentForge-AIOrchestrator` | personal tool, not required by the FYP |
| gsd-core (`@opengsd/gsd-core`) | github.com/open-gsd/gsd-core | bfab824 (npm 1.19.0, current `latest`) | MIT, Copyright (c) 2026 Open GSD | 2026-11-02 | **read, dry-run done, skipped.** No hooks-off flag; a real `--claude --global` install registers about 25 managed hooks (update check, statusline, commit validator, graphify update, read/write guards) in `~/.claude/settings.json`. Node `>=24.0.0` is met (24.18.0). The open "1.17.0 vs 1.12.0" mismatch is stale: both are older than 1.19.0, so pin 1.19.0 if it is ever installed. `SETUP.md` section 10 still says v1.17.0 | personal tool, not required by the FYP |
| rea (`rea-agents`) | github.com/morluto/rea | 920d634 (npm 6.8.0) | MIT, bundles third-party tools under their own licences (`licenses/`) | 2026-11-02 | **read, not installed, waiting on you.** Needs Node ^24.22.1 (machine has 24.18.0). Would be user scope only: `mcpServers.rea` in `~/.claude.json`, launched with `npx -y rea-agents@6.8.0 mcp`. Plan: pin 6.8.0, `--skill=false`, `--tool-families session,artifact,application`, dry-run first | personal tool, not required by the FYP |
| claude-context-optimizer | github.com/egorfedorov/claude-context-optimizer | 1fb7a86 (v5.1.1) | MIT, Copyright (c) 2026 Egor Fedorov | 2026-11-02 read; 2026-11-03 approved | **approved 3 November 2026, nothing installed.** Used only through `claude --plugin-dir C:\Users\pakistan\claude-tools\claude-context-optimizer` (pinned clone, commit 1fb7a86) inside the separate hooks profile (`CLAUDE_CONFIG_DIR=C:\Users\pakistan\.claude-hooks`), never in the main config and never in founders-carnet. Registers six auto-running hooks (`PreToolUse` on Read, `PostToolUse`, `UserPromptSubmit`, `PreCompact`, `SessionStart`, `SessionEnd`). It reads the main profile's `~/.claude/projects` transcripts by path and writes to `C:\Users\pakistan\.claude-context-optimizer\`, so the profile does not fully isolate it | personal tool, not required by the FYP |
| claude-md-management, claude-code-setup | claude.ai account (synced), also in claude-plugins-official | not tracked | not tracked | 2026-11-02 | personal, already available, nothing installed | personal tool, not required by the FYP |
| awesome-claude-skills, 6 of 864: `changelog-generator`, `content-research-writer`, `domain-name-brainstormer`, `lead-research-assistant`, `meeting-insights-analyzer`, `tailored-resume-generator` | github.com/ComposioHQ/awesome-claude-skills | be2a406 | **Unclear.** README badge says Apache-2.0 but there is no LICENSE file | 2026-11-02 | personal only: copied to `~/.claude/skills/`. Never copy into the repo. Not installed (full list of the other 858 in `C:\Users\pakistan\claude-tools\awesome-skills-list.md`; waiting on Ali to pick): the 832 `composio-skills` connectors (they need Rube MCP, hosted by Composio, plus an OAuth connection per service, and the data transits Composio; corrected 2026-11-03, first written as "account and API key"), 10 duplicates of skills already in the claude.ai account, and `skill-share`, `developer-growth-analysis`, `video-downloader`, `file-organizer`, `invoice-organizer`, `langsmith-fetch`, `competitive-ads-extractor`, `image-enhancer`, `raffle-winner-picker`, `twitter-algorithm-optimizer` | personal tool, not required by the FYP |

## Final install list (decided 16 October 2026)

This is the list Ali's Claude Code installs. It replaces the "install note" wording in the tables below where they differ. Nothing outside this list is installed (`CLAUDE.md` still says to ask before adding anything). The per-person items in this section (the "Install per person, never commit" table) are personal tools, not required by the FYP.

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
| spec-kit (`specify-cli`) | Installed on each person's own laptop with `uv tool install specify-cli==<version pinned at install>`. Nothing is copied into the repo. Installed on Ali's machine on 2 November 2026 (1.2.6); `specify init` has not been run. Source read at 2b43eef (github.com/github/spec-kit), MIT, Copyright GitHub, Inc. `specify init` writes `.specify/` and agent commands, so it needs its own OK. Overlaps `spec-driven-development`: use one of the two per feature |

**Not installing:** claude-swarm, screenshot-to-code, AgentForge-AIOrchestrator (codebase-memory-mcp: approved in reduced form on 3 November 2026, then dropped the same day; see the install log). The three were re-read on 3 November 2026 and kept as reference clones in `C:\Users\pakistan\claude-tools\`; nothing installed.

- caveman (read 17 October 2026 at d262ab3, Apache-2.0): skipped. Its own README says the core skill gives 3% fewer output tokens than a plain "Answer concisely." control, "inside the noise". Most of its other skills use the hosted Caveman Cloud gateway or rewrite `CLAUDE.md`-style files. **Update 2026-11-03:** approved by Ali for the separate hooks profile only (pinned clone 2e068f7, v4.0.1); see the install log.
- gstack (read 17 October 2026 at 3e8b34d, MIT): skipped. It is not skills-only: each skill starts by running `~/.claude/skills/gstack/bin/gstack-skill-start` from a separate runtime install (`./setup`) and has a telemetry step. Its hooks and its workflows that commit, push, open pull requests, merge and deploy (`ship`, `land-and-deploy`) clash with `CLAUDE.md`. **Update 2026-11-03:** read again at 82db89a and kept skipped; see the install log.

**Read first, install only if Ali says yes:** career-ops, financial-services, replica-skill (section F). Claude Code reads each one, reports in a few lines, and waits.

**Reference only (not installed):** agents.md, awesome-free-llm-apis, and the tools in section E.

**After installing:** add a row for each new skill to the table in `CLAUDE.md`, fill in the commit and license columns here, copy each license into `third_party_licenses/`, and run `python scripts/sync_agent_skills.py` so Codex and Antigravity see the same skills (they read `.agents/skills/`, not `.claude/skills/`). The script also copies `.claude/references/` to `.agents/references/`, so the `../../references/` links in the skills resolve.

## Added to install (16 October 2026)

These were left out of the first batch. They are now on the install list for project design, context and token management, architecture, backend help, and multi-agent coding. Commit and license are filled in when each one is installed, because they were not read in depth when this list was written. Pin the commit at install time and copy the license into `third_party_licenses/`.

**Rules for every row below:** no hooks that run on their own, no autonomous deletes or edits, and `CLAUDE.md` still wins when a skill disagrees with it. Where a row says "hooks off" or "per person", follow that instead of copying files into the repo. Items in sections B to F below that Ali installed or cloned for himself are personal tools, not required by the FYP.

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
| **graphify** | <https://github.com/Graphify-Labs/graphify> | Code graph for context and token savings | **Installed 2 November 2026** (0.9.100, skill-only; repo not indexed). Apache-2.0 / MIT. Installs as a `/graphify` skill. Steps in "Setup via Claude Code" below. |
| codebase-memory-mcp | <https://github.com/DeusData/codebase-memory-mcp> | Codebase memory for context and token savings | **Not installing.** README read: the installer is `curl ... \| bash`, edits agent config, adds Claude Code hooks, starts a background daemon and a file watcher. It conflicts with the hooks rule and overlaps graphify. **Update 2026-11-03:** approved by Ali in a reduced form, then dropped the same day. See the install log. |
| claude-swarm | <https://github.com/affaan-m/claude-swarm> | Multi-agent coding | **Not installing.** README read: standalone Python CLI that needs a paid `ANTHROPIC_API_KEY` and edits files through worker agents on its own. Claude Code subagents and worktrees cover the same need. **Update 2026-11-03:** re-read at 9b1c556; Ali reconsidered it, then chose a reference clone only. Nothing installed. See the install log. |
| AgentForge-AIOrchestrator | <https://github.com/Pavan03062006/AgentForge-AIOrchestrator> | Multi-agent orchestration | **Not installing.** README read: standalone web app that needs a Supabase project, and it states no license, so it cannot go in the repo. **Update 2026-11-03:** re-read at f19bcd6; Ali reconsidered it, then chose a reference clone only. Nothing installed. See the install log. |
| spec-kit | <https://github.com/github/spec-kit> | Spec-driven architecture workflow | **Install per person.** Installed on Ali's machine on 2 November 2026 (1.2.6, `specify init` not run). MIT. `uv tool install specify-cli==<version>` on each laptop; nothing is copied into the repo. Source read at 2b43eef. Has its own command-line workflow. Overlaps `spec-driven-development`, so use one of the two per feature. |
| agents.md | <https://github.com/agentsmd/agents.md> | `AGENTS.md` format spec | Format spec, no skill. Our `AGENTS.md` already follows it. Reference only. |
| awesome-design-md | <https://github.com/VoltAgent/awesome-design-md> | Design reference files for the frontend | **Install.** README read: nothing to install, you copy one brand's `DESIGN.md` into the project root. MIT. The UI still follows the Figma prototypes. |
| screenshot-to-code | <https://github.com/abi/screenshot-to-code> | Design-to-code | **Not installing.** README read: standalone web app (Poetry + pnpm) that needs an OpenAI, Anthropic or Gemini API key. Not usable from Claude Code. **Update 2026-11-03:** re-read at a813977; Ali reconsidered it, then chose a reference clone only. Nothing installed. See the install log. |
| awesome-free-llm-apis | <https://github.com/mnfst/awesome-free-llm-apis> | Options for the LLM Gateway | Reference list. Read, do not install. |
| **rea** (REA: Reverse Engineer Anything) | <https://github.com/morluto/rea> | Reverse engineering across binaries, applications and runtime behavior, for agents | **Install now.** MIT. Added on request. It is an MCP server: `npx rea-agents setup` (or `npm install --global rea-agents`). The repo's skill is under `.agents/skills`, and skills.sh lists it as `morluto/rea/reverse-engineer-anything`. Install per person. Steps in "Setup via Claude Code" below. |

### Setup via Claude Code (graphify and rea)

Each of the three of you runs these on your own machine, from the repo root. They are tools that install themselves, so nothing is copied by hand. Do not commit tool caches or their output unless a step says so.

**graphify** (Python 3.10+, `uv` recommended). `backend/` and `frontend/` now have code. Do not index the repo until Ali says so.

1. `uv tool install graphifyy==0.9.100` (the package name has two y's; other `graphify*` packages are not affiliated). `pipx install graphifyy` also works.
2. `graphify install --project --platform agents` writes the skill only, to `.agents/skills/graphify/` (not committed). Copy `SKILL.md` and `references/` to `.claude/skills/graphify/` and trim the `SKILL.md` description so it starts only when asked. **Do not use plain `graphify install --project`**: it also appends a section to `CLAUDE.md` and writes a `PreToolUse` hook into `.claude/settings.json`.
3. In Claude Code, run `/graphify .` to build the graph. Output goes to `graphify-out/` (`GRAPH_REPORT.md`, `graph.json`, `graph.html`). Add `graphify-out/` to `.gitignore` if it is large or regenerated.
4. Set `GRAPHIFY_QUERY_LOG_DISABLE=1` in your shell profile to stop it logging every query to `~/.cache/graphify-queries.log`.
5. **Do not run `graphify hook install`.** It adds git hooks that rebuild the graph on commit and checkout, which breaks the no-auto-run-hooks rule.
6. After step 2, `git diff CLAUDE.md .claude/settings.json` must be empty. Never run `graphify claude install`: it registers an auto-running hook that fires before search and file-read calls.
7. Code is parsed locally. Docs, PDFs and images it indexes are sent to the model, so keep secrets and private files out of the folders you point it at. If `GEMINI_API_KEY` or `GOOGLE_API_KEY` is set in your shell, Gemini is used for that pass: unset them, or index with `--code-only`.
8. Optional MCP mode: `uv tool install "graphifyy[mcp]"`. Not part of the default setup.
9. `SKILL.md` lines 700 and 702 run `rm -f graphify-out/...`. The `rm` deny rule blocks them, so delete those temp files by hand.

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
| caveman | <https://github.com/JuliusBrussee/caveman> | Very short replies and auto-running hooks (the Claude plugin at 2e068f7 registers 4 hook entries). | Skipped 17 October; approved 3 November 2026 for the separate hooks profile only (see install log). Its own README calls the gain "inside the noise". |
| gstack | <https://github.com/garrytan/gstack> | Auto-running hooks and workflows that conflict with our rules. | Skipped after reading it (see "Not installing"); re-read 3 November 2026 and kept skipped. Not skills-only: it needs a runtime install and has hooks and deploy workflows. |

### D. No license file: install per person, never commit

| Name | Link | Status (2 November 2026) |
| --- | --- | --- |
| my-claude-skills | <https://github.com/mar-antaya/my-claude-skills> | Installed for Ali only: all 6 skills in `~/.claude/skills/` |
| awesome-claude-skills (864 skill folders) | <https://github.com/ComposioHQ/awesome-claude-skills> | Installed for Ali only: 6 of 864. The 832 Composio connectors were not installed |

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

**Still to be decided (not installed yet):** the `DESIGN.md` brand (after most functionality is done). Decided 2 November 2026: career-ops (Ali only, hook off) and 5 of 11 replica-skill skills (Ali only) installed; financial-services and gsd-core read and skipped; claude-context-optimizer and ECC approved on 3 November 2026 (pinned clones, separate hooks profile only); rea waiting on a Node upgrade. See the install log table above and `docs/build-log.md`. See also "Not in report" in `docs/context/coding-plan.md`.

**From your claude.ai account (about 1,000 skills in ~150 plugins), I took 6 and left the rest.** They are still available to you in claude.ai, Desktop and cloud sessions through your account. They are not in the repo, so teammates do not get them.

- `ali-ahmad`: your personal voice profile, with email samples and personal details. It should not go in a repo three people share. Copy it by hand if you want it.
- `probabl-skills` (ML pipeline skills): they run on `pixi` and `skore`, which clash with the `.venv` and `pip` rule in `CLAUDE.md`.
- `humanize-kit`: needs a saved voice profile to work.
- `superpowers`, `engineering`, `figma`, `huggingface-skills` (rest), `ml-pipeline`, `resume-tailoring`, `deep-research`: large, overlapping with skills already here, or tied to tools you have not set up, or no license file in the synced copy. Ask if you want any of them.
- Twilio, Unity, Zoom, Salesforce, AWS, Databricks, Shopify, SEO, sales and similar plugins: unrelated to this project.
- Harness tooling plugins (harness-architect, bc-harness, harnesskit, harness-init, harness-bootstrap, context-handoff): in the account only, not bundled.

**Added by me, not on your list:** `fastapi`, the two Vercel skills, `supabase-postgres-best-practices`, `train-sentence-transformers` and `huggingface-datasets`. Each is a good match for FastAPI, Next.js, Postgres with pgvector, and the FYP-2 re-ranker.

**Optional personal installs** (`SETUP.md` section 8, not bundled): claude-md-management, claude-code-setup, claude-context-optimizer.
