# Security Policy

The Founder's Carnet is a Final Year Project (FAST NUCES Lahore) and is under active development. It is not a production service, and security fixes are made on a best-effort basis by the student team.

## Supported Versions

There are no tagged releases yet. Only the latest commit on the `main` branch is supported.

| Version             | Supported          |
| ------------------- | ------------------ |
| `main` (latest)     | :white_check_mark: |
| Older commits, forks | :x:               |

## Reporting a Vulnerability

Please do not open a public issue for a security problem.

1. Use **GitHub private vulnerability reporting**: the repository's *Security* tab, then *Report a vulnerability*.
2. Or email the maintainers at `<add a contact email here>` with the subject "Security: Founder's Carnet".

Please include the affected component (backend, frontend or `rag/`), the steps to reproduce, and the impact you expect.

**What to expect**
- We acknowledge a report within 7 days.
- We send a status update at least every 14 days until it is resolved.
- If the report is accepted, we fix it on `main` and credit you if you want (the fix is not guaranteed to have a fixed date).
- If it is declined, we explain why.

## Scope

In scope: authentication and sessions (JWT, token versioning, role checks), access to contact details before mutual acceptance, prompt injection against the LLM gateway or the compliance assistant, and exposed secrets or personal data.

Out of scope: denial of service on free-tier hosting, vulnerabilities in third-party services (Gemini, hosting providers), and issues that need access to a maintainer's own machine.

## Secrets and Data

Never commit `.env` files, API keys or real user data. If you find a leaked secret in the history, report it privately so we can rotate it.
