# Registry schemas and templates

## `.project_flow/RUNS.tsv`

```text
run_id	branch_id	parent_run_id	task	intent	status	run_path	created_at	closed_at	note
```

Statuses: `active`, `completed`, `failed`, `pending_review`, `closed`.

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

States: `draft`, `candidate`, `accepted`, `release`, `archived`.

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

## `RUN_MANIFEST.md`

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
