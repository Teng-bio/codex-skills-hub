# Research Project OS Branch-First Schemas

> Status: superseded by `docs/RESEARCH_PROJECT_OS_COMPLETE_DEVELOPMENT_PLAN.md`
> Retained as historical context / detailed reference only. If it conflicts with the complete plan, follow the complete plan.


Date: 2026-06-23

This document defines the **target branch-first data model** for `research-project-os`.

It is a contract document for the next implementation batches. It does **not** require every field to exist in code yet, but new implementation work should converge to this schema rather than inventing ad hoc fields.

## 1. Path conventions

```text
Branch workspace     .project_os/branches/<branch_id>/
Task workspace       .project_os/branches/<branch_id>/tasks/<task_id>/
Run workspace        runs/<branch_id>/<run_id>/
Branch current       current/branches/<branch_id>/
Project current      current/project/
Release package      release/<release_id>/
```

Rules:

- Every task belongs to exactly one branch.
- Every formal run belongs to exactly one task and one branch.
- Every registered result belongs to exactly one run, task, and branch.
- Global indexes remain under `.project_os/indexes/`.

## 2. Common field rules

### IDs

Recommended ID forms:

```text
branch_id   = main | method_a | review_r2 | figure_rebuild
task_id     = 20260623_nmr_main_qc
run_id      = 20260623_153000__nmr_main_qc
result_id   = 20260623_153000__heatmap_v1
asset_id    = gse12345_raw_matrix
release_id  = 20260623_main_results_v1
```

### Timestamps

Use ISO 8601 with timezone:

```text
2026-06-23T15:30:00+08:00
```

### Status rule

Statuses should be enumerated strings, not booleans or free text.

### Paths

Paths should be project-root relative unless an external absolute path is unavoidable.

## 3. `branches.tsv`

Canonical location:

```text
.project_os/indexes/branches.tsv
```

Header:

```text
branch_id	status	parent_branch_id	title	branch_path	task_root	run_root	current_root	git_branch	created_at	closed_at	notes
```

Field meanings:

- `branch_id`: stable branch/workstream identifier
- `status`: `active | paused | completed | archived | abandoned`
- `parent_branch_id`: parent branch ID or empty
- `title`: short human label
- `branch_path`: usually `.project_os/branches/<branch_id>`
- `task_root`: usually `.project_os/branches/<branch_id>/tasks`
- `run_root`: usually `runs/<branch_id>`
- `current_root`: usually `current/branches/<branch_id>`
- `git_branch`: optional linked Git branch name
- `created_at`: branch creation time
- `closed_at`: branch close/archive time or empty
- `notes`: short notes

## 4. `branch.json`

Canonical location:

```text
.project_os/branches/<branch_id>/branch.json
```

Minimal target shape:

```json
{
  "branch_id": "main",
  "title": "Main analysis line",
  "status": "active",
  "parent_branch_id": "",
  "git_branch": null,
  "branch_path": ".project_os/branches/main",
  "task_root": ".project_os/branches/main/tasks",
  "run_root": "runs/main",
  "current_root": "current/branches/main",
  "created_at": "2026-06-23T00:00:00+08:00",
  "closed_at": null,
  "objective_file": "objective.md",
  "context_file": "context.md",
  "handoff_file": "handoff.md",
  "notes": ""
}
```

## 5. `tasks.tsv`

Canonical location:

```text
.project_os/indexes/tasks.tsv
```

Header:

```text
task_id	branch_id	status	kind	stage	title	task_path	parent_task_id	created_at	updated_at	owner	priority	notes
```

Allowed `status`:

```text
active, paused, blocked, completed, archived, superseded
```

Allowed `stage`:

```text
Intake, Plan, Research, Run, Evaluate, Promote, Archive, Release
```

Suggested `priority`:

```text
urgent, high, normal, low
```

## 6. `task.json`

Canonical location:

```text
.project_os/branches/<branch_id>/tasks/<task_id>/task.json
```

Minimal target shape:

```json
{
  "task_id": "20260623_nmr_main_qc",
  "title": "NMR main-line QC pass",
  "status": "active",
  "kind": "analysis",
  "stage": "Run",
  "branch_id": "main",
  "parent_task_id": null,
  "task_path": ".project_os/branches/main/tasks/20260623_nmr_main_qc",
  "created_at": "2026-06-23T15:30:00+08:00",
  "updated_at": "2026-06-23T15:30:00+08:00",
  "owner": "",
  "priority": "normal",
  "objective_file": "objective.md",
  "context_file": "context.md",
  "context_manifest": "context_manifest.jsonl",
  "handoff_file": "handoff.md",
  "notes": ""
}
```

## 7. `runs.tsv`

Canonical location:

```text
.project_os/indexes/runs.tsv
```

Header:

```text
run_id	branch_id	task_id	status	result_status	run_path	created_at	closed_at	code_ref	notes
```

Allowed `status`:

```text
active, completed, failed, pending_review, archived, superseded
```

Allowed `result_status`:

```text
draft, candidate, accepted, current, superseded, legacy, release
```

`code_ref` may contain a short commit hash or another project-specific code reference summary.

## 8. `RUN_MANIFEST.json`

Canonical location:

```text
runs/<branch_id>/<run_id>/RUN_MANIFEST.json
```

Minimal target shape:

```json
{
  "run_id": "20260623_153000__nmr_main_qc",
  "branch_id": "main",
  "task_id": "20260623_nmr_main_qc",
  "status": "active",
  "created_at": "2026-06-23T15:30:00+08:00",
  "closed_at": null,
  "code_ref": {
    "git_commit": null,
    "dirty": null,
    "git_available": null
  },
  "environment": {
    "python": null,
    "conda_env": null,
    "packages": {}
  },
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

### Structured child rows

Suggested `inputs[]` row:

```json
{
  "asset_id": "gse12345_raw_matrix",
  "kind": "matrix",
  "path": "data/raw/gse12345/matrix.tsv",
  "checksum": null,
  "notes": ""
}
```

Suggested `commands[]` row:

```json
{
  "command": "python script.py --input ...",
  "cwd": ".",
  "exit_code": null,
  "started_at": null,
  "finished_at": null
}
```

Suggested `outputs[]` row:

```json
{
  "path": "runs/main/20260623_153000__nmr_main_qc/output.tsv",
  "kind": "table",
  "title": "QC summary table",
  "notes": ""
}
```

## 9. `results.tsv`

Canonical location:

```text
.project_os/indexes/results.tsv
```

Header:

```text
result_id	branch_id	task_id	run_id	status	type	path	title	created_at	accepted_at	promoted_to	replaced_by	notes
```

Allowed `status`:

```text
draft, candidate, accepted, current, superseded, legacy, release
```

`promoted_to` should record the current-slot destination when relevant, for example:

```text
current/branches/main/heatmap_v1.png
current/project/summary_table.tsv
```

## 10. Task-local `run_links.tsv`

Canonical location:

```text
.project_os/branches/<branch_id>/tasks/<task_id>/run_links.tsv
```

Header:

```text
run_id	status	path	created_at	notes
```

## 11. Task-local `result_links.tsv`

Canonical location:

```text
.project_os/branches/<branch_id>/tasks/<task_id>/result_links.tsv
```

Header:

```text
result_id	status	path	run_id	created_at	notes
```

## 12. `assets.tsv`

Canonical location:

```text
.project_os/indexes/assets.tsv
```

Header:

```text
asset_id	kind	path	version	source_url	source_note	immutable	status	registered_at	checksum	notes
```

Recommended `status` values:

```text
active, deprecated, replaced, unavailable, provenance_unknown
```

`immutable` should be:

```text
true | false
```

## 13. `releases.tsv`

Canonical location:

```text
.project_os/indexes/releases.tsv
```

Header:

```text
release_id	status	path	created_at	source_branch_ids	source_result_ids	notes
```

Recommended `status`:

```text
draft, finalized, superseded, archived
```

## 14. Release package manifest

Canonical location:

```text
release/<release_id>/MANIFEST.tsv
```

Header:

```text
file_path	type	source_result_id	source_run_id	source_task_id	source_branch_id	checksum	notes
```

## 15. Resume invariants

A future agent should be able to resolve:

1. `current_branch` -> branch workspace
2. `current_task` -> branch-local task directory
3. `current_run` -> `runs/<branch_id>/<run_id>/RUN_MANIFEST.json`
4. project current outputs -> `current/project/`
5. branch current outputs -> `current/branches/<branch_id>/`
6. global state summaries -> root docs and `.project_os/indexes/*.tsv`
