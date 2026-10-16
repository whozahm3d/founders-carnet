#!/usr/bin/env python3
"""Copy .claude/skills/* into .agents/skills/ so Codex and Antigravity can read them.

Why: Codex and Antigravity read skills from <repo>/.agents/skills/ and do not read
.claude/skills/. This script keeps .claude/skills/ as the one source.

What it does: copies every skill folder from .claude/skills/ to .agents/skills/.
What it never does: delete anything. A skill removed from .claude/skills/ stays
in .agents/skills/ until you delete that folder yourself. .agents/skills/ is in
.gitignore, so nothing here is committed.

Usage (from anywhere inside the repo):
    python scripts/sync_agent_skills.py
    python scripts/sync_agent_skills.py --dry-run
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dry-run", action="store_true", help="show what would be copied")
    args = parser.parse_args()

    root = repo_root()
    src = root / ".claude" / "skills"
    dst = root / ".agents" / "skills"

    if not src.is_dir():
        print(f"No skills folder at {src}", file=sys.stderr)
        return 1

    copied = 0
    for skill in sorted(p for p in src.iterdir() if p.is_dir()):
        if not (skill / "SKILL.md").is_file():
            print(f"skip {skill.name}: no SKILL.md")
            continue
        target = dst / skill.name
        print(f"{'would copy' if args.dry_run else 'copy'} {skill.name}")
        if not args.dry_run:
            # dirs_exist_ok overwrites files with the same name; it removes nothing.
            shutil.copytree(skill, target, dirs_exist_ok=True)
        copied += 1

    print(f"{copied} skill(s) {'found' if args.dry_run else 'copied'} to {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
