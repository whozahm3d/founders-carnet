---
name: report-code-sync
description: Use when writing or changing code, a schema, an API, a diagram, or a dataset step for The Founder's Carnet, and when the user asks whether the code matches the report. Checks the change against the project report and records any difference on purpose.
---

# Report and code sync

The supervisor wants the code, the diagrams and the report to say the same thing. This skill is how Claude checks that. It is written by the team, not copied from elsewhere.

## When to run it

- Before writing a new component, endpoint, table, prompt or pipeline step.
- After a change that touches a name, a field, a flow, or a rule that the report describes.
- When the user asks "does this match the report?".
- When a diagram, the data dictionary, or a feature description might now be out of date.

## Steps

1. **Name what the change touches.** List the report section, diagram, data dictionary table, or requirement it implements (for example a feature chapter, a figure number, a table name). If you cannot tell, ask the user. Do not guess a section number.
2. **Get the source text.** `main.tex` and the master document are not guaranteed to be in this repo. If they are not here, ask the user to paste the section or point to the file. Do not rely on memory of the report.
3. **Compare.** Check names, fields, data types, flow order, roles, and the rules in `CLAUDE.md`:
   - the client talks only to the FastAPI gateway
   - the LLM Gateway is the only path to Gemini
   - matching never calls a language model
   - trained model and prompted LLM call are kept separate
   - contact details show only after both sides accept
   - RAG answers cite sources and say so when unsupported
   - age and gender are never matching features
4. **Report the result in plain words.** Use a short table with four columns: item, what the report says, what the code does, and which one you suggest changing. If everything matches, say so and say what you compared.
5. **Do not decide silently.** If the code and report disagree, ask the user whether to change the code or the report. Hard-to-undo cases (schema, API contract, folder rename) need an explicit yes.
6. **Record it.** After the user decides, propose a dated entry for `docs/DECISIONS.md` using `docs/decision-entry-template.md`. Name the file and show the entry first. Add it only after the user agrees.
7. **List follow-ups.** Say which diagrams, data dictionary tables, or report sections now need a matching edit, and who owns that folder in `CLAUDE.md`. Do not edit the report or diagrams from here unless asked.

## Rules

- Say what you checked and what you did not.
- Do not claim the code matches until you have read the report text for that part.
- Do not call a prompted feature "trained" or "fine-tuned".
- A change that adds scope (new feature, new data source, new role) is flagged as scope, not treated as a sync fix. The project is three people over about six months.
