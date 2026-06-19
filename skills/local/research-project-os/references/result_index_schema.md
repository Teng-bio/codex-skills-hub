# Result index schema

`.project_os/indexes/results.tsv` and task `result_links.tsv` use this minimal schema:

```text
result_id	task_id	run_id	status	type	path	title	created_at	accepted_at	replaced_by	notes
```

Allowed result statuses:

```text
draft, candidate, accepted, current, superseded, legacy, release
```

Rules:

- Register generated outputs as `draft` or `candidate` first.
- `accepted` or `current` requires explicit user approval.
- Root `RESULTS_INDEX.md` is the human-facing result entry point and should summarize accepted/candidate/legacy outputs.
- `current/` should contain promoted pointers/copies only, never independent ad-hoc versions.
