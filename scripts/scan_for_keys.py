"""Look for API keys and other credentials in files that git tracks.

Standard library only. Exit code 0 means nothing found, 1 means something was found.

    python scripts/scan_for_keys.py            check every file git tracks
    python scripts/scan_for_keys.py --staged   check only files staged for commit

This is a simple pattern check, not a full scanner. It catches common key formats and
tracked .env files. A tool such as gitleaks is stronger if the team wants more.
To allow a line that looks like a key but is not, add  key-scan: ignore  to that line.
"""
import re
import subprocess
import sys
from pathlib import Path

# Folders with third-party text that may contain example keys.
SKIP_PREFIXES = (".claude/skills/", "third_party_licenses/", "_backup_mirror/", ".claude/backups/")
SKIP_NAMES = {"scan_for_keys.py"}
SKIP_SUFFIXES = (".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".pt", ".pth", ".safetensors", ".onnx", ".ckpt", ".ico", ".woff", ".woff2")
MAX_BYTES = 2_000_000

PATTERNS = [
    ("Google API key", re.compile(r"AIza[0-9A-Za-z_\-]{35}")),
    ("OpenAI-style key", re.compile(r"\bsk-[A-Za-z0-9_\-]{20,}")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{40,}")),
    ("AWS access key id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Private key block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----")),
    (
        "Hard-coded credential assignment",
        re.compile(r"(?i)(?:api[_-]?key|secret|token|password|passwd)\s*[:=]\s*['\"][^'\"\s]{16,}['\"]"),
    ),
]


def tracked_files(staged):
    cmd = ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"] if staged else ["git", "ls-files"]
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    return [line for line in out.splitlines() if line]


def is_env_file(path):
    name = Path(path).name
    return (name == ".env" or name.startswith(".env.")) and name != ".env.example"


def main():
    staged = "--staged" in sys.argv
    try:
        files = tracked_files(staged)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Could not run git here. Run this from inside the repository.")
        return 2

    problems = []
    for path in files:
        if is_env_file(path):
            problems.append((path, 0, "A .env file is tracked by git"))
            continue
        if path.startswith(SKIP_PREFIXES) or Path(path).name in SKIP_NAMES or path.lower().endswith(SKIP_SUFFIXES):
            continue
        p = Path(path)
        try:
            if not p.is_file() or p.stat().st_size > MAX_BYTES:
                continue
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for number, line in enumerate(text.splitlines(), start=1):
            if "key-scan: ignore" in line:
                continue
            for label, pattern in PATTERNS:
                if pattern.search(line):
                    problems.append((path, number, label))
                    break

    if problems:
        print("Possible keys found. Do not commit these. Remove them and rotate the key if it was real.")
        for path, number, label in problems:
            where = f"{path}:{number}" if number else path
            print(f"  {where}  {label}")
        return 1
    print(f"No keys found in {len(files)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
