---
name: web-design-guidelines
description: Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "check my site against best practices".
metadata:
  author: vercel
  version: "1.0.0"
  argument-hint: <file-or-pattern>
---

# Web Interface Guidelines

Review files for compliance with Web Interface Guidelines.

## How It Works

1. Read the rules in `command.md` in this folder
2. Read the specified files (or prompt user for files/pattern)
3. Check against all rules in `command.md`
4. Output findings in the terse `file:line` format

## Guidelines Source

The rules are saved in `command.md` next to this file. Do not fetch them from the web.
`$ARGUMENTS` in `command.md` means the files or pattern the user gave.

`command.md` is a pinned copy of vercel-labs/web-interface-guidelines at commit 434b7f91
(downloaded 2026-10-16, SHA-256 d246b026f4f29b5823a9cc857f9edf3d2507002e055e32040cadeaf3b38e0234).
A person updates it by downloading a newer commit and recording the new hash in `THIRD_PARTY.md`.

Where a rule clashes with `frontend-design` on copy or style (for example Title Case or `&` for "and"),
the Figma prototypes win.

## Usage

When a user provides a file or pattern argument:
1. Read `command.md` in this folder
2. Read the specified files
3. Apply all rules in `command.md`
4. Output findings using the format specified in `command.md`

If no files specified, ask the user which files to review.
