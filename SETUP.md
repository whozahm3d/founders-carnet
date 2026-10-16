# Setup

Do sections 1 and 2 first. Sections 5 to 10 are separate. Do section 9 before your first push.

## 1. Install

1. This zip is already merged with your repo files (README, folder READMEs, `docs/DECISIONS.md`). Unzip it into the root of your `founders-carnet` folder and merge when Windows asks. `CLAUDE.md` is the only file of yours it replaces.
2. `.gitignore` already has the new lines, under the heading "Added for the Claude Code setup". Check them before your first `git add`. Do not paste anything.
3. In PowerShell, run `python --version`. If it fails but `py --version` works, open `.claude/settings.json` in your editor and change `"command": "python"` to `"command": "py"` in both hooks. Claude cannot edit this file.
4. Restart Claude Code from the repo folder.

## 2. Test it (two minutes)

1. Start a session. A folder called `_backup_mirror/` should appear.
2. Ask: "Add the line test to the end of README.md". You should get a confirmation prompt that mentions a backup copy, and a copy should appear under `.claude/backups/`.
   - If the edit just happens with no prompt, tell me. A user report says some Claude Code versions do not enforce confirmation prompts, and I could not test on Windows. The deny rules below still hold, and we would add a stricter hook.
3. Ask: "Delete README.md". It should be refused.
4. Run `python scripts/backup.py list`.
5. If Claude Code reports a settings problem, run `/doctor`.

## 3. Everyday commands

```
python scripts/backup.py mirror               copy important folders to _backup_mirror/ (also runs at session start)
python scripts/backup.py zip                  zip into ..\founders-carnet-backups\ (outside the repo)
python scripts/backup.py zip --include-data   same, plus data/, datasets/, models/ (files over 500 MB skipped)
python scripts/backup.py list                 show what exists
python scripts/backup.py restore docs\x.md    bring back a deleted file or folder
python scripts/backup.py restore docs\x.md --from snapshot   the copy from just before Claude's last edit
python scripts/backup.py restore docs\x.md --force           overwrite the current file (it is saved first)
```

Restore never overwrites a file you still have unless you pass `--force`. Without it, the copy is saved next to the file as `x.md.restored-<time>`.

## 4. What protects you, and what does not

**Blocks Claude cannot be talked out of** (deny rules in `.claude/settings.json`): `rm`, `rmdir`, `del`, `Remove-Item`; `git push`, `reset`, `clean`, `restore`, `rebase`, `checkout --`, `branch -D`, `stash drop`; reading or editing `.env` files; editing the settings, hooks, backup script and backup folders.

**Asks you first** (ask rules): `git commit`, and any `pip install`, `python -m pip install` or `npm install`.

**Extra layer** (hook): before Claude changes an existing file, a copy goes to `.claude/backups/` and you are asked to confirm. New files inside the repo are allowed. If Python is missing the hook silently does nothing, so do the test above.

**Limits:**
- Deny rules block the commands listed. They cannot stop every way of deleting a file, such as a Python one-liner. Git is the real backup, so commit and push often.
- The mirror lives inside the repo folder, so deleting the whole folder deletes it. The zip is outside. Copy a zip to Drive or a USB stick now and then.
- `.env` files are never backed up because they hold secrets. Keep your own copy.
- Only folders listed in `scripts/backup_config.json` are mirrored. Backup folders are cleared after 30 days.
- The blocks apply to Claude Code only. Gemini in Antigravity does not use `.claude/settings.json`. See section 7 for `AGENTS.md`.
- To change a protected file (settings, hooks, backup script), edit it yourself.

## 5. Python

The report names Python 3.11, Node 24 and PostgreSQL 16 (the Node 20 to 24 change is logged in `docs/DECISIONS.md`, 2026-10-15 and 2026-10-16). FastAPI and sentence-transformers both support 3.11, so all three of you should use it. `CLAUDE.md` has the Python rules Claude follows.

**Check your version** (PowerShell):

```
python --version
```

If it is not 3.11.x, install 3.11 from python.org and tick "Add python.exe to PATH". If `python` is not found but `py` works, use `py -3.11` in place of `python` below.

**Create a virtual environment**, one per folder that has Python code. Example for the backend:

```
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

If PowerShell refuses to run the activate script, run this once and try again:

```
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

**Install packages from a file** so all three of you get the same versions:

```
pip install -r requirements.txt
```

When a new package is needed, Claude will ask first, say why, and add it to `requirements.txt` with a pinned version. You run the install yourself, or approve it when Claude Code asks.

**Run the tests:**

```
pip install pytest
pytest
```

**Lint** (`ruff` is a default I picked, since the report asks for linting but names no tool. Change it if the team prefers another):

```
pip install ruff
ruff check .
```

`.venv/`, `__pycache__/` and similar are in `.gitignore`, so they stay out of git.

## 6. ECC (optional, installed on your machine, not in the repo)

ECC is Affaan Mustafa's plugin of agents, skills and commands. It installs into your own Claude Code, so it applies to every project, not only this repo. Each teammate who wants it must install it.

ECC's own guide says to pick one install method, not several. Do not mix them. Do sections 1 and 2 first, so you know the safety setup works before ECC is added.

**What you need:** Node.js 24 (the project version; ECC itself only needs 18 or newer), Git, and Claude Code 2.1 or newer. Check in PowerShell:

```
node --version
git --version
claude --version
```

### Step 1. Install the plugin (hooks off)

Run this in PowerShell, from any folder:

```
npx ecc-universal@2.2.3 setup
```

When the wizard asks:
- **Scope:** choose Global user. Do not choose project, because that would write into this repo's settings, which are protected.
- **Hooks:** choose **off**. ECC's hooks run on their own, which goes against the rule that Claude changes nothing until told. You keep the skills, agents and commands.

Start a new Claude Code session and run `/plugin list`. `ecc@ecc` should show as enabled.

If you prefer the commands from ECC's README, they also work. Run these inside Claude Code:

```
/plugin marketplace add https://github.com/affaan-m/ECC
/plugin install ecc@ecc
```

That install turns hooks on by default. Run the `setup` wizard above afterwards and choose hooks **off**. The wizard manages the same plugin, so this is not a second install.

### Step 2. Copy the rules

Rules are not part of the plugin, so they are copied by hand. ECC recommends the `common` folder plus one folder for your language. Backend, RAG and ML people use `python`. Frontend people use `typescript`.

Clone ECC to a folder **outside** the repo, for example your Downloads folder, not inside `founders-carnet`:

```
cd $HOME\Downloads
git clone https://github.com/affaan-m/ECC.git
cd ECC
New-Item -ItemType Directory -Force "$HOME\.claude\rules\ecc"
Copy-Item -Recurse -Force "rules\common" "$HOME\.claude\rules\ecc\"
Copy-Item -Recurse -Force "rules\python" "$HOME\.claude\rules\ecc\"
```

Frontend people add this line as well:

```
Copy-Item -Recurse -Force "rules\typescript" "$HOME\.claude\rules\ecc\"
```

On Mac or Linux the original `mkdir -p` and `cp -R` lines from ECC's README work as written.

You can delete the cloned `ECC` folder afterwards.

### Step 3. Check that your safety rules still win

Open Claude Code in the repo folder and repeat tests 2 and 3 from section 2. The edit should still ask first, and "Delete README.md" should still be refused. I have not tested ECC together with this setup. If either test fails, run `/plugin disable ecc@ecc` and tell me.

### Things to know

- **ECC's workflow rules say to commit and push.** `CLAUDE.md` says Claude does not. The deny rules block `git push` and the commit rule asks first, so the safety rules win. If Claude seems confused by the two, tell it to follow `CLAUDE.md`.
- **It is large.** ECC's own manifest lists 71 agents, 311 skills and 97 command shortcuts. Their descriptions share Claude's context with your project skills. If Claude gets slow or loses track of things, run `/plugin disable ecc@ecc`.
- **Rule files load into every session.** They are the heaviest part. If sessions feel crowded, remove the `typescript` folder first.
- **To update or change the hook profile later,** run `npx ecc-universal@2.2.3 setup` again.
- **To remove it,** run `/plugin uninstall ecc@ecc` and delete `$HOME\.claude\rules\ecc`.
- The plugin id `ecc@ecc` and version 2.2.3 match ECC's own manifest at the commit I checked. I did not run the install.

## 7. Other agents (AGENTS.md)

`AGENTS.md` in the repo root tells Gemini in Antigravity, Codex and similar agents to read `CLAUDE.md`, and repeats the key safety rules. `GEMINI.md` is a short pointer to `AGENTS.md` for Antigravity. Antigravity reads `AGENTS.md` (IDE 1.20.5 and later) or `GEMINI.md`; which one wins when both exist is not documented, so both say the same thing. If the agent skips them, start the session with: "Read AGENTS.md and CLAUDE.md first." These agents ignore `.claude/settings.json`, so for them the rules are instructions only, not blocks.

Codex and Antigravity read skills from `.agents/skills/`, not `.claude/skills/`. After cloning or pulling, run `python scripts/sync_agent_skills.py`. It copies the skills across and never deletes. See section 11.

## 8. Optional personal plugins (not in the repo)

Plugins install per person, so they cannot travel with the repo. These three are from the plugin directory in your Claude account. In Claude Code, run `/plugin`, search for the name, and install it. I did not run these installs, so the menu wording may differ.

| Plugin | What it does | Notes |
|---|---|---|
| `claude-md-management` | Suggests cleanups to `CLAUDE.md` (`claude-md-improver`) and can add lessons from a session (`/revise-claude-md`) | Only changes `CLAUDE.md` when you run it. Read its suggestion before accepting. Do not let it touch the safety section. |
| `claude-code-setup` | Looks at the repo and recommends Claude Code settings, hooks and skills (`claude-automation-recommender`) | Advice only. Do not apply a recommendation that loosens `.claude/settings.json`. |
| `claude-context-optimizer` (v4.12.1, MIT) | Shows what is using up Claude's context | It ships hooks that run automatically, which goes against the "nothing runs until told" rule. Install it only if sessions feel slow, and turn it off when you are done. |

After installing any plugin, repeat tests 2 and 3 from section 2.

## 9. Team files in this zip

These are new files. None of them replaces anything from the scaffold zip (`docs/DECISIONS.md` is not touched).

| File | What to do |
|---|---|
| `.env.example` | Done: the file is in the repo. It lists the settings the stack needs, with no values. Everyone copies it to `.env` and fills in their own keys. |
| `.github/CODEOWNERS` | All three handles are filled in (@whozahm3d, @ShahzebMalik32, @tahanawaz27-jpg). Turn on "Require review from Code Owners" in the `protect-main` ruleset once all three have accepted access to the repo. Not before, or no pull request can be approved. |
| `.github/pull_request_template.md` | Appears automatically on new pull requests. |
| `.github/workflows/ci.yml` | Runs the key scan, then ruff and pytest for `backend`, `rag` and `ml`, and lint, test and build for `frontend`. Each part skips itself while its folder is empty. I could not run it on GitHub. Look at the first run in the Actions tab and tell me what fails. |
| `scripts/scan_for_keys.py` | Finds API keys and tracked `.env` files. Run `python scripts/scan_for_keys.py` any time. It is a simple pattern check, so use gitleaks if you want a stronger one. |
| `.githooks/pre-commit` | Runs that scan before each commit. Turn it on once per clone: `git config core.hooksPath .githooks`. |
| `docs/datasets.md` | The list of datasets, one entry each. Fill an entry before using a dataset. |
| `docs/pending-report-changes.md` | Things the code has changed that the report does not say yet (now: the Chapter 6 rows and stale items), with a draft `DECISIONS.md` entry. |
| `docs/decision-entry-template.md` | The format for new entries in `docs/DECISIONS.md`. |
| `.claude/skills/report-code-sync/` | A skill we wrote. It makes Claude compare a change with the report, show the differences, and propose a `DECISIONS.md` entry. It asks you to paste the report section if `main.tex` is not in the repo. |

The scan was tested on a throwaway repo (it flagged a fake key and a tracked `.env`, and passed a clean tree). The pre-commit hook and CI file were not run.

## 10. GSD Core (optional, installed on your machine, not in the repo)

GSD Core (`open-gsd/gsd-core`, v1.17.0, MIT) is a planning framework for AI coding agents. It runs a loop of discuss, plan, execute, verify and ship, one phase at a time, and keeps its state in a `.planning/` folder. Its README says to use its installer and not to copy its files by hand, so I did not put it in the zip. It cannot be bundled the way the skills were.

**What it brings:** 72 skills, about 60 agents and a set of hooks that run automatically. The installer's help text says the full install adds about 12,000 tokens of descriptions to every session. The `core` profile adds about 700.

**Why it is optional and not default:**
- **Its hooks run on their own.** That goes against the "nothing runs until told" rule. One of them starts a background update check at the start of each session.
- **It plans, edits and commits on its own.** In this repo the deny rules block `git push` and the commit rule asks first, so those rules still win. The installer also writes into `settings.json`. In this repo that file is protected from Claude, but you run the installer yourself in a terminal, so nothing stops it. With `--local` it would mix its hooks into our `.claude/settings.json`. Use `--global`, not `--local`.
- **It overlaps `/feature-dev` and `spec-driven-development`.** Two planning workflows in one session pull in different directions. Pick one per task.
- **It needs Node.js 24 or newer** (`package.json`, `engines`). The project now uses Node 24 too, so this is no longer a conflict. Everyone on the team should be on 24.

**How we use it (decided with Ali: the middle path):**
- Install only the `core` profile. Add more later if you miss something.
- Use it for planning and verification: discuss, plan, verify. Do not use its autonomous run mode, which writes whole phases of code without you reading them. The team must be able to explain every line to the supervisor.
- One workflow per task: GSD or `/feature-dev`, not both.
- One person (Ali) installs it first, on a throwaway copy of the repo. The others install it after the section 2 tests pass.

**Install steps** (do sections 1 and 2 first):

1. Preview without installing anything:
   ```
   npx @opengsd/gsd-core@latest --claude --global --profile=core --dry-run
   ```
2. If the preview looks fine, run the same line without `--dry-run`. `core` is the smallest profile.
3. Open Claude Code in the repo and repeat tests 2 and 3 from section 2. The edit should still ask first, and "Delete README.md" should still be refused. If either fails, remove GSD:
   ```
   npx @opengsd/gsd-core@latest --claude --global --uninstall
   ```
4. **`.planning/` is not committed (draft rule, Ali to confirm).** It is already in `.gitignore`. Do this before the first GSD command, in this order:
   - Check that `.planning/` is in `.gitignore` (section 1 added it).
   - Then run `/gsd-new-project` and answer **No** or set `commit_docs: false` if it asks. GSD's default is to commit `.planning/` on its own, but its docs say an ignored `.planning/` switches that off. Check with `git status` that `.planning/` does not appear.
   - If `.planning/` ever got committed before it was ignored, adding it to `.gitignore` later does not remove it. Tell me before running any git command to fix that.
   - Anything from `.planning/` that the team needs goes into `docs/DECISIONS.md` or the report by hand, in plain words. `.planning/config.json` can hold search API keys in plain text, which is another reason it stays out of git.

I read the repo's file list, README, `package.json` and the installer's option list. I did not run the installer, and I did not read all 27 hooks line by line. The flags above come from the installer's own help text, not from a test.

## 11. Skills install and keeping tools in step (added 2026-10-16)

The approved install list is in `THIRD_PARTY.md` under "Final install list". Ali runs it in his own Claude Code with the prompt in `INSTALL_PROMPT.md` (kept outside the repo). It installs nothing outside the list.

For Taha and Shahzeb on Codex or Antigravity:

1. Pull the latest `main`.
2. Run `python scripts/sync_agent_skills.py`. It copies `.claude/skills/*` to `.agents/skills/`. It never deletes, and `.agents/skills/` is gitignored.
3. Run it again after every pull that changes `.claude/skills/`.

Per-person installs (docx, pdf, pptx, xlsx, the code-review plugin, rea, and the no-license repos) are never committed. See the table in `THIRD_PARTY.md`.

`rag/data/` (the 11 corpus documents) is committed, so a clone has them. `rag/corpus_manifest.md` has the SHA-256 hashes to check against.
