# research-project-os E2E coverage audit

Date: 2026-06-24

This document records the current disposable end-to-end smoke coverage for
`skills/local/research-project-os/scripts/project_os.py`.

## Scope

Primary smoke entry:

```bash
python3 skills/local/research-project-os/scripts/smoke_project_os_e2e.py
```

The smoke script creates only temporary harness projects and temporary external
asset roots. It must not touch real project paths or the default configured
external storage roots.

## Coverage summary

- CLI subcommands discovered from `project_os.py`: **80**
- Subcommands exercised by `smoke_project_os_e2e.py`: **80**
- Missing subcommand coverage: **0**
- Approval-gate negative paths covered:
  - `register-result`
  - `accept-result`
  - `promote-result`
  - `build-release`
  - `restore-journal`
  - `externalize-asset`
  - `adopt-external-asset`

## Covered command surface

Bootstrap / health / routing:

- `init`
- `new-project`
- `start`
- `status`
- `route`
- `explain-trigger`
- `doctor`
- `validate`
- `refresh-indexes`
- `restore-journal`
- `install-adapters`
- `build-adapters`

Branch and session runtime:

- `create-branch`
- `set-current-branch`
- `list-branches`
- `show-branch`
- `archive-branch`
- `create-session`
- `set-current-session`
- `list-sessions`
- `show-session`
- `set-session-focus`
- `pause-session`
- `resume-session`
- `close-session`
- `plan-session-cleanup`
- `plan-recovery`

Task and run provenance:

- `create-task`
- `set-current-task`
- `list-tasks`
- `show-task`
- `update-task`
- `update-task-stage`
- `close-task`
- `add-dependency`
- `remove-dependency`
- `add-context`
- `remove-context`
- `create-run`
- `set-current-run`
- `update-run`
- `close-run`
- `list-runs`
- `show-run`
- `add-run-input`
- `add-run-command`
- `add-run-output`
- `add-run-metric`
- `add-run-parameter`
- `capture-run-env`

Results and releases:

- `register-result`
- `accept-result`
- `promote-result`
- `supersede-result`
- `show-current`
- `list-results`
- `show-result`
- `build-release`
- `list-releases`
- `show-release`
- `validate-release`

Assets and portable externalization:

- `register-asset`
- `list-assets`
- `show-asset`
- `list-asset-locations`
- `update-asset`
- `checksum-asset`
- `plan-externalize-assets`
- `externalize-asset`
- `adopt-external-asset`
- `verify-external-assets`
- `refresh-assets`

Decisions, handoff, dashboards, hooks, migration:

- `record-decision`
- `list-decisions`
- `update-handoff`
- `summarize-state`
- `export-dashboard`
- `list-hooks`
- `dispatch-hooks`
- `migrate-branch-first`

## Explicit boundaries

- The smoke does not enable active/background hooks.
- Session cleanup and recovery remain report-only.
- Migration coverage is conservative dry-run coverage plus separate historical
  dogfood records; it does not mutate real legacy projects.
- Externalization uses explicit temporary primary/backup roots and checks that
  the resulting files are neither hard links nor symlinks.
- Symlinks are not treated as canonical recovery paths; canonical recovery is
  `asset_id + .project_os/indexes/asset_locations.tsv`.

## Re-audit command

The current 80/80 count was produced by comparing `sub.add_parser(...)`
definitions in `project_os.py` with `r.os("<subcommand>", ...)` calls in the
smoke script. Re-run after adding any CLI command and update this file before
release.
