#!/usr/bin/env python3
"""Backup helper for the Founder's Carnet repo.

Standard library only. Works on Windows, macOS and Linux.
Run it from anywhere:  python scripts/backup.py <command>

  mirror                 Copy the important folders into _backup_mirror/.
                         Nothing is ever deleted from the mirror, so a file you
                         delete by accident is still there. Older versions of
                         changed files are kept in _backup_mirror/.history/.
  zip [--include-data]   Make a timestamped zip in ../<repo>-backups/ (outside the
                         repo). --include-data also adds data/ datasets/ models/.
  snapshot <file>        Save one file to .claude/backups/<time>/ (the hook uses this).
  list                   Show what is backed up.
  restore <path> [--from mirror|snapshot|zip] [--force]
                         Restore a file or folder. Without --force an existing file
                         is never overwritten: the copy is saved next to it as
                         <name>.restored-<time>.

.env files are never copied (they hold secrets). Keep your own copy of them.
"""
import argparse
import json
import shutil
import sys
import tempfile
import zipfile
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = Path(__file__).resolve().parent / "backup_config.json"
DEFAULTS = {
    "important": ["docs", "rag", "ml", "backend", "frontend", "scripts", ".claude",
                  "CLAUDE.md", "README.md"],
    "data_dirs": ["data", "datasets", "models"],
    "exclude_dirs": ["node_modules", ".venv", "venv", "__pycache__", ".next", "dist",
                     "build", ".git", ".pytest_cache", ".mypy_cache", ".ruff_cache",
                     ".idea", ".vscode"],
    "exclude_prefixes": [".claude/backups", "_backup_mirror"],
    "max_file_mb": 20,
    "data_max_file_mb": 500,
    "snapshot_max_mb": 50,
    "keep_days": 30,
    "keep_zips": 10,
    "mirror_dir": "_backup_mirror",
    "zip_dir": None,
}


def load_config():
    cfg = dict(DEFAULTS)
    try:
        cfg.update(json.loads(CONFIG_PATH.read_text(encoding="utf-8")))
    except (OSError, ValueError):
        pass
    return cfg


def tag(micro=False):
    return datetime.now().strftime("%Y%m%d-%H%M%S" + ("-%f" if micro else ""))


def rel_of(path):
    try:
        return Path(path).resolve().relative_to(ROOT)
    except (ValueError, OSError):
        return None


def is_secret(name):
    n = name.lower()
    if n == ".env":
        return True
    return n.startswith(".env.") and not n.endswith((".example", ".sample", ".template"))


def prefix_excluded(rel, cfg):
    posix = rel.as_posix()
    return any(posix == p or posix.startswith(p + "/") for p in cfg["exclude_prefixes"])


def iter_files(cfg, tops, max_mb):
    limit = max_mb * 1024 * 1024
    for top in tops:
        p = ROOT / top
        if not p.exists():
            continue
        candidates = [p] if p.is_file() else None
        if candidates is None:
            candidates = []
            for dp, dirs, files in _walk(p, cfg):
                candidates.extend(Path(dp) / f for f in files)
        for f in candidates:
            try:
                if f.is_symlink() or is_secret(f.name):
                    continue
                if f.stat().st_size > limit:
                    continue
                rel = f.relative_to(ROOT)
                if prefix_excluded(rel, cfg):
                    continue
            except (OSError, ValueError):
                continue
            yield f


def _walk(top, cfg):
    import os
    for dp, dirs, files in os.walk(top):
        rel = Path(dp).relative_to(ROOT)
        dirs[:] = [d for d in dirs
                   if d not in cfg["exclude_dirs"]
                   and not prefix_excluded(rel / d, cfg)]
        yield dp, dirs, files


def copy_file(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def same(src, dst):
    a, b = src.stat(), dst.stat()
    return a.st_size == b.st_size and abs(a.st_mtime - b.st_mtime) < 2


def prune_old(folder, keep_days):
    """Remove dated sub-folders of our own backup folders once they are old enough."""
    folder = Path(folder)
    if not folder.is_dir() or rel_of(folder) is None:
        return 0
    cutoff = datetime.now() - timedelta(days=keep_days)
    removed = 0
    for child in folder.iterdir():
        try:
            if child.is_dir() and datetime.fromtimestamp(child.stat().st_mtime) < cutoff:
                shutil.rmtree(child)
                removed += 1
        except OSError:
            pass
    return removed


def snapshot_file(path):
    """Copy one existing file into .claude/backups/<time>/. Returns the copy or None."""
    cfg = load_config()
    p = Path(path)
    rel = rel_of(p)
    if rel is None or not p.is_file() or is_secret(p.name):
        return None
    if prefix_excluded(rel, cfg) or p.stat().st_size > cfg["snapshot_max_mb"] * 1024 * 1024:
        return None
    dst = ROOT / ".claude" / "backups" / tag(micro=True) / rel
    copy_file(p, dst)
    return dst


def cmd_mirror(args):
    cfg = load_config()
    mirror = ROOT / cfg["mirror_dir"]
    stamp, copied, archived = tag(), 0, 0
    for src in iter_files(cfg, cfg["important"], cfg["max_file_mb"]):
        rel = src.relative_to(ROOT)
        dst = mirror / rel
        if dst.exists():
            if same(src, dst):
                continue
            copy_file(dst, mirror / ".history" / stamp / rel)
            archived += 1
        copy_file(src, dst)
        copied += 1
    prune_old(mirror / ".history", cfg["keep_days"])
    prune_old(ROOT / ".claude" / "backups", cfg["keep_days"])
    if not args.quiet:
        print(f"mirror: {copied} file(s) copied, {archived} older version(s) kept in history")
    return 0


def zip_dir_of(cfg):
    return Path(cfg["zip_dir"]) if cfg["zip_dir"] else ROOT.parent / f"{ROOT.name}-backups"


def cmd_zip(args):
    cfg = load_config()
    out_dir = zip_dir_of(cfg)
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{ROOT.name}-{tag()}.zip"
    n = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        groups = [(cfg["important"], cfg["max_file_mb"])]
        if args.include_data:
            groups.append((cfg["data_dirs"], cfg["data_max_file_mb"]))
        for tops, mb in groups:
            for f in iter_files(cfg, tops, mb):
                z.write(f, f.relative_to(ROOT).as_posix())
                n += 1
    old = sorted(out_dir.glob(f"{ROOT.name}-*.zip"))
    for stale in old[:-cfg["keep_zips"]]:
        stale.unlink()
    print(f"zip: {n} file(s), {out.stat().st_size // 1024} KB -> {out}")
    return 0


def cmd_snapshot(args):
    dst = snapshot_file(args.file)
    if dst is not None and not args.quiet:
        print(f"snapshot: {dst.relative_to(ROOT).as_posix()}")
    return 0


def cmd_list(args):
    cfg = load_config()
    mirror = ROOT / cfg["mirror_dir"]
    files = [f for f in mirror.rglob("*") if f.is_file() and ".history" not in f.parts] if mirror.is_dir() else []
    hist = sorted((mirror / ".history").glob("*")) if (mirror / ".history").is_dir() else []
    snaps = sorted((ROOT / ".claude" / "backups").glob("*")) if (ROOT / ".claude" / "backups").is_dir() else []
    zips = sorted(zip_dir_of(cfg).glob(f"{ROOT.name}-*.zip")) if zip_dir_of(cfg).is_dir() else []
    print(f"mirror   : {len(files)} file(s) in {cfg['mirror_dir']}/, {len(hist)} history set(s)")
    print(f"snapshots: {len(snaps)} in .claude/backups/ (newest: {snaps[-1].name if snaps else 'none'})")
    print(f"zips     : {len(zips)} in {zip_dir_of(cfg)} (newest: {zips[-1].name if zips else 'none'})")
    return 0


def find_source(rel, how, cfg):
    if how == "mirror":
        src = ROOT / cfg["mirror_dir"] / rel
        return src if src.exists() else None
    if how == "snapshot":
        base = ROOT / ".claude" / "backups"
        for d in sorted(base.glob("*"), reverse=True) if base.is_dir() else []:
            if (d / rel).is_file():
                return d / rel
        return None
    if how == "zip":
        out_dir = zip_dir_of(cfg)
        for zp in sorted(out_dir.glob(f"{ROOT.name}-*.zip"), reverse=True) if out_dir.is_dir() else []:
            with zipfile.ZipFile(zp) as z:
                names = [n for n in z.namelist() if n == rel.as_posix() or n.startswith(rel.as_posix() + "/")]
                if names:
                    tmp = Path(tempfile.mkdtemp(prefix="carnet-restore-"))
                    z.extractall(tmp, names)
                    return tmp / rel
        return None
    return None


def cmd_restore(args):
    cfg = load_config()
    target = Path(args.path)
    if not target.is_absolute():
        target = ROOT / target
    rel = rel_of(target)
    if rel is None:
        print("restore: that path is outside the repo", file=sys.stderr)
        return 1
    src = find_source(rel, args.source, cfg)
    if src is None:
        print(f"restore: nothing found for {rel.as_posix()} in {args.source}", file=sys.stderr)
        return 1
    dst = target
    if target.exists():
        if args.force:
            if target.is_file():
                snapshot_file(target)
        else:
            dst = target.with_name(f"{target.name}.restored-{tag()}")
    if src.is_dir():
        shutil.copytree(src, dst, dirs_exist_ok=True)
    else:
        copy_file(src, dst)
    print(f"restore: {rel.as_posix()} -> {dst.relative_to(ROOT).as_posix()} (from {args.source})")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Backup helper for the Founder's Carnet repo.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("mirror"); m.add_argument("--quiet", action="store_true"); m.set_defaults(fn=cmd_mirror)
    z = sub.add_parser("zip"); z.add_argument("--include-data", action="store_true"); z.set_defaults(fn=cmd_zip)
    s = sub.add_parser("snapshot"); s.add_argument("file"); s.add_argument("--quiet", action="store_true"); s.set_defaults(fn=cmd_snapshot)
    l = sub.add_parser("list"); l.set_defaults(fn=cmd_list)
    r = sub.add_parser("restore"); r.add_argument("path")
    r.add_argument("--from", dest="source", choices=["mirror", "snapshot", "zip"], default="mirror")
    r.add_argument("--force", action="store_true"); r.set_defaults(fn=cmd_restore)
    args = ap.parse_args(argv)
    try:
        return args.fn(args)
    except Exception as exc:  # never crash a session start because of a backup problem
        print(f"backup error: {exc}", file=sys.stderr)
        return 0 if getattr(args, "quiet", False) else 1


if __name__ == "__main__":
    sys.exit(main())
