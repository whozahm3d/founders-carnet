# Datasets

Record every dataset here before it is used. `CLAUDE.md` says no dataset is used unless it is listed. For each one, say what the supervisor will ask: what it contains, why it was chosen, and which user input it serves.

Rules that apply to all of them (see the data rules in `CLAUDE.md`):

- External datasets are for profiling and schema design only. None of them trains the deployed re-ranker.
- Age and gender are never matching features.
- Do not store names, birth dates, or contact fields from external datasets.
- Do not redistribute a dataset. Raw data stays out of git.
- No data without consent.

## Entry format

Copy this block for each dataset.

```
### Dataset name

- **Source and link:**
- **License or terms:**
- **Date downloaded and version:**
- **What it contains:** (rows, columns, what one row is)
- **Why we chose it:**
- **User input it serves:** (for example: founder profile, job seeker profile, mentor profile, startup description)
- **How we use it:** (profiling, schema design, test input, and so on)
- **Fields we keep, fields we drop:**
- **Personal data present?** (yes or no, and what we do about it)
- **Where the raw file lives:** (a path outside git, for example `data/`)
- **Report section it supports:**
- **Owner:**
- **Known problems:**
```

## Datasets in use

None yet.
