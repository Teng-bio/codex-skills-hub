---
name: project-state-maintainer
description: Maintain a canonical `PROJECT_STATE.md` in each project root so work can be resumed from the folder itself instead of reconstructing chat history. Use when creating or adopting a project, when starting work in a new repo or folder, when resuming prior work, when making meaningful changes or decisions, when handing work off, or when the user asks for a project summary, progress summary, current status, next steps, overall workflow, or a durable summary of the project's state. In Chinese, also trigger this skill when the user says things like `写一个项目状态文档`, `更新项目状态文档`, `总结项目状态`, `总结一个项目文档`, `记录当前项目进度`, `记录一下当前项目状态和下一步`, `整理项目当前进展`, `写一下这个项目现在做到哪`, or any similar request meaning “summarize or update the project's current state”.
---

# Project State Maintainer

Maintain one file per project root:

- `PROJECT_STATE.md`

This file is the durable project handoff, not the chat transcript.

## Core rule

When this skill is active:

1. Detect the project root.
2. Ensure `PROJECT_STATE.md` exists there.
3. Read `PROJECT_STATE.md` before substantive work.
4. Update `PROJECT_STATE.md` before finishing any turn that changes project understanding or project state.

Do not rely on chat history as the primary project memory if `PROJECT_STATE.md` exists.

## Root detection

Use this order:

1. Git root of the current working directory.
2. Current working directory if no git root exists.

Never write project state outside the detected root unless the user explicitly asks for another location.

## Managed files

Primary file:

- `PROJECT_STATE.md`

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

## When to update

Update `PROJECT_STATE.md` whenever any of these are true:

- code, config, data, docs, or project files changed
- a bug/root cause was identified
- a plan or architecture decision was made
- a task was completed, blocked, or re-scoped
- the user asked for a summary, progress, or handoff state

Do not skip updates just because the turn was short.

You may skip the update only when the turn produced no project-relevant change, no new conclusion, and no new next step.

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
2. Decide which sections changed.
3. Build one minimal JSON payload.
4. Call `update`.
5. Re-read the file only if you need to verify or reference it in the response.

Avoid repeatedly rewriting the file for each tiny thought; batch related updates into one write near the end of the turn.

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
4. create or patch `AGENTS.md` with the project-state rule
5. tell the user that this project now has a durable project-state file

## References

- `assets/AGENTS-project-state-snippet.md`
- `scripts/project_state.py`
