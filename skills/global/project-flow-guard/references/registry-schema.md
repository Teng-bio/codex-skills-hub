# Registry schemas and templates

## `.project_flow/RUNS.tsv`

```text
run_id	branch_id	parent_run_id	task	intent	status	run_path	created_at	closed_at	note
```

Core CLI statuses: `active`, `completed`, `failed`, `pending_review`, `closed`.

Project-facing states such as `candidate`, `accepted`, `superseded`, `archived`, and `legacy` may be recorded in registry notes, `FILE_REGISTRY.tsv`, `RESULTS_INDEX.md`, or `RUN_MANIFEST.json` when they describe scientific/result acceptance rather than process state.

## Root `RUNS_INDEX.tsv` (optional)

Use when humans need a concise project-level run index outside `.project_flow/`.

```text
run_id	date	workstream	status	task	main_outputs	promoted_to	superseded_by	manifest	note
```

Keep it short. It is an index, not a full run report.

## `.project_flow/BRANCHES.tsv`

```text
branch_id	parent_baseline	status	branch_path	created_at	description
```

Statuses: `active`, `paused`, `closed`.

## `.project_flow/BASELINES.tsv`

```text
baseline_id	source	status	baseline_path	created_at	description
```

Statuses: `sealed`, `superseded`.

## `.project_flow/FILE_REGISTRY.tsv`

```text
canonical_path	source_path	source_run_id	branch_id	state	checksum	size_bytes	updated_at	note
```

States: `draft`, `candidate`, `accepted`, `release`, `archived`, `legacy`, `superseded`.

## `.project_flow/PROMOTIONS.tsv`

```text
promoted_at	source_path	canonical_path	source_run_id	branch_id	action	previous_canonical_path	reason
```

Actions: `promote_to_branch_current`, `promote_to_project_current`, `release`.

## `.project_flow/CHANGELOG.tsv`

For source edits:

```text
timestamp	session_id	intent	changed_paths	tests	status	note
```

## `RUN_MANIFEST.json`

Canonical structured run manifest.

```json
{
  "run_id": "<run_id>",
  "intent": "artifact_run",
  "task": "short task",
  "branch_id": "",
  "parent_run_id": "",
  "status": "active",
  "created_at": "YYYY-MM-DDTHH:MM:SS",
  "closed_at": "",
  "inputs": [],
  "commands": [],
  "outputs": [],
  "decisions": [],
  "notes": "",
  "promoted_to": [],
  "superseded_by": ""
}
```

## `RUN_MANIFEST.md` (optional)

Human summary. If both files exist, JSON is canonical for structured fields.

```markdown
# Run Manifest: <run_id>

- intent:
- task:
- branch_id:
- parent_run_id:
- status:
- created_at:

## Inputs

| role | path | checksum/status | note |
|---|---|---|---|

## Commands

```text
command here
```

## Outputs

| path | role | state | note |
|---|---|---|---|

## Decisions / notes
```

## `BASELINE.md`

```markdown
# Baseline: <baseline_id>

- created_at:
- source:
- reason:

## Accepted/current files

See `MANIFEST.tsv`.
```
