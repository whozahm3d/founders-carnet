# Third-party material

Everything under `.claude/skills/`, `.claude/commands/` and `.claude/agents/` (except what is listed as ours) was copied from the public repositories below on 15 October 2026. The licenses are MIT or Apache-2.0. Copies are in `third_party_licenses/`. Keep them if the repo is shared.

**How it was checked.** Every included folder was scanned for risky patterns: downloads, pipe-to-shell, delete commands, `eval`/`exec`, obfuscation, install commands, and phrases that try to override instructions. Every flagged line was read. The one script that runs commands (`webapp-testing/scripts/with_server.py`) was read in part. Not every line of every file was read, so treat these like any other dependency.

## Included

| What | From | Commit | License |
|---|---|---|---|
| 11 process skills: `spec-driven-development`, `planning-and-task-breakdown`, `incremental-implementation`, `test-driven-development`, `code-review-and-quality`, `debugging-and-error-recovery`, `security-and-hardening`, `api-and-interface-design`, `documentation-and-adrs`, `frontend-ui-engineering`, `source-driven-development` | github.com/addyosmani/agent-skills | aeac41d4 | MIT |
| `fastapi` | github.com/fastapi/fastapi (`.agents/skills/fastapi`) | 0b919816 | MIT |
| `vercel-react-best-practices`, `vercel-composition-patterns` (folders renamed to match each skill's `name`) | github.com/vercel-labs/agent-skills | 063bee94 | MIT (stated in the skill files; the repo has no root LICENSE file) |
| `supabase-postgres-best-practices` | github.com/supabase/agent-skills | c9be0e93 | MIT |
| `train-sentence-transformers`, `huggingface-datasets` | github.com/huggingface/skills | c3ff942b | Apache-2.0 |
| `webapp-testing` | github.com/anthropics/skills | dbd4588f | Apache-2.0 |
| `python-patterns`, `python-testing`, `verification-loop` | github.com/affaan-m/ECC | b92f181b | MIT |
| `/feature-dev` command and three read-only agents (`code-explorer`, `code-architect`, `code-reviewer`) | github.com/anthropics/claude-plugins-official (`plugins/feature-dev`) | 8f814f49 | Apache-2.0 |

| `humanizer` | Your claude.ai account (skill v2.9.0; same file as `humanizer.skill` in the Project) | not tracked | MIT (stated in the skill file) |
| `anti-ai-writing` | Your claude.ai account (plugin, github.com/avectats7/anti-ai-writing) | not tracked | MIT |
| `explore-data`, `statistical-analysis`, `validate-data`, `sql-queries` | Your claude.ai account (Anthropic `data` plugin) | not tracked | Apache-2.0 |

The last three rows were copied from the skills synced to your account on 15 October 2026, not cloned from GitHub, so there is no commit hash. Same scan as above, no flagged lines other than word lists.

Ours, not third-party: `.claude/settings.json`, `.claude/hooks/guard.py`, `.claude/skills/report-code-sync/`, `scripts/backup.py`, `scripts/backup_config.json`, `scripts/scan_for_keys.py`, `.githooks/pre-commit`, `.github/` files, `docs/datasets.md`, `docs/decision-entry-template.md`, `env.example`, `CLAUDE.md`, `AGENTS.md`, `SETUP.md`.

Things to know:
- `webapp-testing` starts whatever server command you give it. It needs `pip install playwright` and a browser install before first use.
- `train-sentence-transformers` has a reference page that mentions a paid Hugging Face Jobs option and a `curl ... | bash` line to install their CLI. It is documentation only. `CLAUDE.md` already tells Claude to ask before paid services or installs.
- Anything that fetches web content (the `fastapi` skill links to its docs, `source-driven-development` tells Claude to read official docs) can pull in text you have not reviewed. Do not paste secrets into a session that is browsing.

## Left out, and why

**From your claude.ai account (about 1,000 skills in ~150 plugins), I took 6 and left the rest.** They are still available to you in claude.ai, Desktop and cloud sessions through your account. They are not in the repo, so teammates do not get them.
- `ali-ahmad`: your personal voice profile, with email samples and personal details. It should not go in a repo three people share. Copy it by hand if you want it.
- `docx`, `pdf`, `pptx`, `xlsx`: Anthropic's license says "all rights reserved", so I did not copy them into a repo.
- `probabl-skills` (ML pipeline skills): they run on `pixi` and `skore`, which clash with the `.venv` and `pip` rule in `CLAUDE.md`.
- `humanize-kit`: needs a saved voice profile to work.
- `superpowers`, `engineering`, `figma`, `huggingface-skills` (rest), `ml-pipeline`, `resume-tailoring`, `deep-research`, `frontend-design`: large, overlapping with skills already here, or tied to tools you have not set up, or no license file in the synced copy. Ask if you want any of them.
- Twilio, Unity, Zoom, Salesforce, AWS, Databricks, Shopify, SEO, sales and similar plugins: unrelated to this project.

**Added by me, not on your list:** `fastapi`, the two Vercel skills, `supabase-postgres-best-practices`, `train-sentence-transformers` and `huggingface-datasets`. Each is a good match for FastAPI, Next.js, Postgres with pgvector, and the FYP-2 re-ranker.

**Applications, platforms or libraries rather than skill packs:** firecrawl, opik, openclaw, hermes-agent, OmniRoute, open-design (each has thousands of files); claude-agent-sdk-python, claude-cookbooks, claude-code (the CLI's own repo; its plugins duplicate claude-plugins-official).

**No SKILL.md files found in the survey:** graphify, screenshot-to-code, codebase-memory-mcp (it installs a separate MCP server program), AgentForge-AIOrchestrator, agents.md (a format spec), claude-swarm, awesome-design-md (design reference files; your UI follows the Figma prototypes).

**Unrelated to this project (judged from names and folder layout, not read in depth):** career-ops (job search), financial-services (finance plugins), replica-skill (website cloning), rea (reverse engineering).

**Would work against your rules:**
- caveman: makes replies very short and has 26 hook files that run automatically. You need explanations you can repeat to your supervisor.
- ponytail and gstack: large sets of skills with hooks that run automatically. I did not review them in depth, so they are out rather than risked.
- GSD Core (`open-gsd/gsd-core`, v1.17.0, commit 7dadc90, MIT): an installer-based framework with 72 skills, about 60 agents and many auto-run hooks, needing Node 24. Its README says not to copy files by hand, so it is not bundled. `SETUP.md` section 10 has optional install steps.
- ECC (full install): the zip bundles only 3 of its skills. You asked for the full plugin, so `SETUP.md` section 6 has the install steps. It is not bundled because it is large and its hooks run on their own. If you install it, turn its hooks off.

**No license file, so they cannot be redistributed:** my-claude-skills, awesome-claude-skills (a list with 864 skill folders).

**Reference only:** awesome-free-llm-apis (a list of free LLM APIs, useful to read for the free-tier work), spec-kit (its own command-line workflow, overlaps `spec-driven-development`; ask if you want it).

**Skipped from repos I did use:**
- anthropics/skills: docx, pdf, pptx, xlsx and the rest are not needed for a coding repo and I did not check their license terms. `frontend-design` could pull the UI away from the Figma prototypes. `claude-api` is for Claude, and you use Gemini.
- claude-plugins-official: `code-review` posts comments on GitHub pull requests by itself and runs five parallel agents.
- addyosmani/agent-skills: `git-workflow-and-versioning` recommends `git reset --hard`, which your rules block. The other 11 skills (launch, CI/CD, performance, observability and similar) are not needed yet. Add them later by copying the folder.
- vercel-labs/agent-skills: `web-design-guidelines` downloads its rules from a live GitHub URL every time it runs.
