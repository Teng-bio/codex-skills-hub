# Run manifest schema

A formal run must have `RUN_MANIFEST.json`.

Minimal structure:

```json
{
  "run_id": "20260619_200000__task_slug",
  "task_id": "20260619_task",
  "status": "active",
  "created_at": "2026-06-19T20:00:00+08:00",
  "closed_at": null,
  "code_ref": {"git_commit": null, "dirty": null, "git_available": null},
  "environment": {"python": null, "conda_env": null, "packages": {}},
  "inputs": [],
  "parameters": {},
  "commands": [],
  "outputs": [],
  "metrics": {},
  "result_status": "draft",
  "promoted_to": [],
  "notes": ""
}
```

Run status values:

```text
active, completed, failed, pending_review, archived, superseded
```

Result status values attached to run outputs:

```text
draft, candidate, accepted, current, superseded, legacy, release
```
