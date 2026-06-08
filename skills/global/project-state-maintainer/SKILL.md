---
name: project-state-maintainer
description: Maintain a thin canonical `PROJECT_STATE.md` plus optional md/tsv/json companion docs so work can be resumed from the project folder instead of chat history. Use when creating/adopting/resuming a project, making meaningful changes or decisions, handing work off, summarizing status/progress/next steps, or when project docs risk becoming too large and need splitting into `RESULTS_INDEX.md`, `DECISIONS.md`, `DATA_ASSETS.md`, or run/result registries. In Chinese, also trigger when the user says `写一个项目状态文档`, `更新项目状态文档`, `总结项目状态`, `记录当前项目进度`, `整理项目当前进展`, `项目文档太大`, `拆分项目文档`, or similar.
---

# Project State Maintainer

Maintain a **thin state file** per project root:

- `PROJECT_STATE.md`

This file is the durable project handoff, not the chat transcript and not a full history ledger.

When detail would make `PROJECT_STATE.md` bulky, split it into md/tsv/json companion docs and leave only a concise pointer in `PROJECT_STATE.md`.

## Core rule

When this skill is active:

1. Detect the project root.
2. Ensure `PROJECT_STATE.md` exists there.
3. Read `PROJECT_STATE.md` before substantive work.
4. Read companion docs only when needed for the task.
5. Update the most specific companion doc first when detail belongs there.
6. Update `PROJECT_STATE.md` before finishing any turn that changes project understanding or project state.

Do not rely on chat history as the primary project memory if `PROJECT_STATE.md` exists.
Do not bloat `PROJECT_STATE.md` with raw logs, full run histories, or long rationales.

## Root detection

Use this order:

1. Git root of the current working directory.
2. Current working directory if no git root exists.

Never write project state outside the detected root unless the user explicitly asks for another location.

## Managed files

Primary file:

- `PROJECT_STATE.md`

Recommended companion files, created only when useful:

- `RESULTS_INDEX.md`: current accepted/candidate/legacy result entry points.
- `DECISIONS.md`: decision log with context, decision, rationale, consequences, and status.
- `DATA_ASSETS.md`: data sources, paths, versions, ownership/copying rules, and caveats.
- `RUNS_INDEX.tsv`: run registry, normally maintained with `project-flow-guard`.
- `runs/*/RUN_MANIFEST.json`: run-level structured metadata, normally maintained with `project-flow-guard`.

Canonical source formats are limited to:

- Markdown (`.md`) for human-readable summaries and rationale.
- TSV (`.tsv`) for searchable registries.
- JSON (`.json`) for structured run/script metadata.

SQLite/HTML may be generated later for query or display, but must not be treated as the canonical project-state source unless the user explicitly changes this policy.

Companion file on first adoption of a project:

- `AGENTS.md`

On first adoption, if the project root does not have an `AGENTS.md`, create one using the snippet in `assets/AGENTS-project-state-snippet.md`.

If `AGENTS.md` already exists, preserve existing content and append a short `PROJECT_STATE` policy only if the file does not already contain an equivalent rule.

## What belongs in `PROJECT_STATE.md`

Keep the file concise and decision-oriented. The canonical sections are:

1. `Project Summary`
2. `Current Goal`
3. `Current Status`
4. `Key Paths`
5. `Decisions`
6. `Recent Changes`
7. `Open Problems`
8. `Next Step`
9. `Resume Prompt`

Rules:

- Write for the next agent or future you.
- Prefer short bullets over long prose.
- Record decisions and current reality, not raw chat.
- Update `Recent Changes`, `Current Status`, and `Next Step` on every meaningful turn.
- Keep `Resume Prompt` to 1-3 sentences that tell the next agent exactly how to continue.
- Keep detailed evidence in companion docs/reports and link to it.
- If a section is growing into a history log, summarize it and move detail to `docs/project_history.md`, `DECISIONS.md`, `RESULTS_INDEX.md`, `DATA_ASSETS.md`, or domain reports.

## Companion doc routing

Use the narrowest doc that answers the question:

| User/agent question | Preferred doc |
|---|---|
| What is the project and what is next? | `PROJECT_STATE.md` |
| Which result is current/accepted/candidate/legacy? | `RESULTS_INDEX.md` |
| Why did we choose or abandon a plan? | `DECISIONS.md` |
| Where did data come from and which paths are authoritative? | `DATA_ASSETS.md` |
| What happened in a generated analysis run? | `RUNS_INDEX.tsv` + `RUN_MANIFEST.json` |

Suggested `DECISIONS.md` entry:

```markdown
## YYYY-MM-DD: short decision title

Status: proposed | accepted | superseded | rejected

Context:
- ...

Decision:
- ...

Rationale:
- ...

Consequences:
- ...
```

Suggested `RESULTS_INDEX.md` entry:

```markdown
## Current result group

- Status: accepted | candidate | legacy
- Main files: `path/to/file.tsv`, `path/to/report.md`
- Source run: `runs/<run_id>/RUN_MANIFEST.json`
- Notes: concise caveats only
```

## When to update

Update `PROJECT_STATE.md` whenever any of these are true:

- code, config, data, docs, or project files changed
- a bug/root cause was identified
- a plan or architecture decision was made
- a task was completed, blocked, or re-scoped
- the user asked for a summary, progress, or handoff state

Do not skip updates just because the turn was short.

You may skip the update only when the turn produced no project-relevant change, no new conclusion, and no new next step.

Update companion docs when the detail would otherwise crowd `PROJECT_STATE.md`:

- Update `RESULTS_INDEX.md` when accepted/current/candidate/legacy result entry points change.
- Update `DECISIONS.md` when a method, threshold, reference, architecture, scope, or data-inclusion decision changes.
- Update `DATA_ASSETS.md` when data source paths, versions, checksums, ownership/copying rules, or external-data caveats change.
- Let `project-flow-guard` update `RUNS_INDEX.tsv` and `RUN_MANIFEST.json` for formal generated runs; reference those files from `PROJECT_STATE.md`.

## Update workflow

Use the bundled script instead of hand-editing whenever possible.

### Create or normalize the file

```bash
python3 scripts/project_state.py ensure --project-root <root>
```

### Read current structured state

```bash
python3 scripts/project_state.py show --project-root <root>
```

### Update structured state

```bash
python3 scripts/project_state.py update --project-root <root> --json '<json>'
```

`--json` accepts a partial object. Only provided sections are updated.

## Preferred update strategy

1. Call `show` or read the current file.
2. Decide whether detail belongs in `PROJECT_STATE.md` or a companion doc.
3. Update the companion doc first if needed.
4. Build one minimal JSON payload for `PROJECT_STATE.md`.
5. Call `update`.
6. Re-read the file only if you need to verify or reference it in the response.

Avoid repeatedly rewriting the file for each tiny thought; batch related updates into one write near the end of the turn.
When companion docs are absent, create only the minimal file that is useful for the current task; do not scaffold every optional doc automatically.

## JSON shape for updates

Use these keys:

```json
{
  "project_summary": "string",
  "current_goal": "string",
  "current_status": ["bullet", "bullet"],
  "key_paths": ["path", "path"],
  "decisions": ["decision", "decision"],
  "recent_changes": ["change", "change"],
  "open_problems": ["problem", "problem"],
  "next_step": ["step", "step"],
  "resume_prompt": "string"
}
```

Guidelines:

- String fields should be compact paragraphs or 1-3 sentences.
- List fields should be flat lists of short bullets.
- `key_paths` should prefer project-relative paths when clear.

## Quality bar

Bad state file:

- vague
- chatty
- missing concrete next step
- duplicates raw conversation

Good state file:

- explains what the project is
- explains what is happening right now
- names the important files
- captures key decisions
- gives the next agent an immediate continuation point

## First adoption checklist

When using this skill in a project for the first time:

1. detect root
2. create `PROJECT_STATE.md`
3. seed it with the current project understanding
4. create companion docs only if the project already needs them
5. create or patch `AGENTS.md` with the project-state rule
6. tell the user that this project now has a durable project-state file

## References

- `assets/AGENTS-project-state-snippet.md`
- `scripts/project_state.py`
