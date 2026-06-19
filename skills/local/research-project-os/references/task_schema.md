# Task schema

Task directories live under `.project_os/tasks/<task_id>/`.

Required files:

```text
task.json
objective.md
context.md
context_manifest.jsonl
decisions.md
run_links.tsv
result_links.tsv
handoff.md
research/
```

Required `task.json` fields:

```json
{
  "task_id": "20260619_example_task",
  "title": "Example task",
  "status": "active",
  "kind": "analysis",
  "parent_task_id": null,
  "branch_id": "main",
  "created_at": "2026-06-19T20:00:00+08:00",
  "updated_at": "2026-06-19T20:00:00+08:00",
  "owner": "",
  "stage": "Intake",
  "objective_file": "objective.md",
  "context_manifest": "context_manifest.jsonl",
  "notes": ""
}
```

Allowed status values:

```text
active, paused, blocked, completed, archived, superseded
```
