#!/usr/bin/env python3
"""PreToolUse hook: protect key files and save a backup copy before Claude changes a file.

Runs before Write, Edit, MultiEdit and NotebookEdit. Standard library only.

  * Protected files (settings, hooks, backup scripts, .env files, backups, .git):
    blocked with exit code 2. Edit these yourself in your editor.
  * Any other existing file: a backup copy is saved to .claude/backups/, then the
    user is asked to confirm the change.
  * A new file inside the repo: allowed.
  * Anything outside the repo: left to Claude Code's normal permission flow.

If this script itself fails, Claude Code carries on without it. The deny rules in
.claude/settings.json do not depend on this script.
"""
import json
import os
import sys
from pathlib import Path


def decide(decision, reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": decision,
        "permissionDecisionReason": reason}}))


def protected(rel):
    p = rel.as_posix().casefold()
    name = rel.name.casefold()
    if name == ".env" or (name.startswith(".env.") and not name.endswith((".example", ".sample", ".template"))):
        return True
    exact = {".claude/settings.json", ".claude/settings.local.json",
             "scripts/backup.py", "scripts/backup_config.json"}
    prefixes = (".claude/hooks/", ".claude/backups/", "_backup_mirror/", ".git/")
    return p in exact or p.startswith(prefixes)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    tool_input = data.get("tool_input") or {}
    target = tool_input.get("file_path") or tool_input.get("notebook_path")
    if not target:
        return 0
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or ".").resolve()
    path = Path(target)
    if not path.is_absolute():
        path = Path(data.get("cwd") or root) / path
    try:
        rel = path.resolve().relative_to(root)
    except (ValueError, OSError):
        return 0

    if protected(rel):
        print(f"Blocked: {rel.as_posix()} is a protected file. Ask the user to change it themselves.",
              file=sys.stderr)
        return 2

    if path.exists():
        saved = None
        try:
            sys.path.insert(0, str(root / "scripts"))
            import backup
            copy = backup.snapshot_file(path)
            saved = copy.relative_to(backup.ROOT).as_posix() if copy else None
        except Exception:
            pass
        note = f"A backup copy was saved to {saved}." if saved else "No backup copy could be saved."
        decide("ask", f"Changing existing file {rel.as_posix()}. {note}")
    else:
        decide("allow", f"New file {rel.as_posix()} inside the repo.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
