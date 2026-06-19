# Project adoption workflow

Use this when adding `.project_os/` to an existing project.

## Steps

1. Run `project_os.py init --root <project>` without `--apply` to preview.
2. Read the existing `PROJECT_STATE.md`, `AGENTS.md`, `DATA_ASSETS.md`, `RESULTS_INDEX.md`, `RUNS_INDEX.tsv`, and `DECISIONS.md` when present.
3. Run `project_os.py init --root <project> --apply` only after confirming the new files will not overwrite existing work.
4. Create one task representing the active workstream.
5. Add existing authoritative plans and root docs to that task's `context_manifest.jsonl`.
6. Set runtime pointers with `set-current-task` and, only when known, `current_run`.
7. Run `validate` and fix errors before using the harness as the continuation source.

## Existing project rule

For an existing scientific project, the harness should point to current plans instead of replacing them. If a project already has a planning hierarchy, encode that hierarchy in `.project_os/spec/project_rules.md` and task context manifests.
