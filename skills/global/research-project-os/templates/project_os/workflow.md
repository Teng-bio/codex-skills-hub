# Project OS Workflow

Default phases:

```text
Intake -> Plan -> Research -> Run -> Evaluate -> Promote -> Archive -> Release
```

Rules:

- Read `PROJECT_STATE.md` and this workflow before substantive work.
- Resolve continuation from `runtime/current_task`, `runtime/current_branch`, and `runtime/current_run`.
- Load task context from `tasks/<task_id>/context_manifest.jsonl`.
- Put generated run outputs under `runs/<run_id>/` or the project-approved run directory.
- Register runs and results in `.project_os/indexes/` and root human indexes.
- Promote to `current/` only after explicit user approval.
- Update `PROJECT_STATE.md` or task `handoff.md` before stopping when project state changed.
