# Task Plan: Full Core Research Project Harness Roadmap

> Status: superseded by `docs/RESEARCH_PROJECT_OS_COMPLETE_DEVELOPMENT_PLAN.md`
> Retained as historical context / detailed reference only. If it conflicts with the complete plan, follow the complete plan.

## Canonical execution note

Do not execute this roadmap directly. Use `docs/RESEARCH_PROJECT_OS_COMPLETE_DEVELOPMENT_PLAN.md` as the active P0/P1/P2 development plan; this file is retained to show prior planning context.


## Goal
Build a reusable repository-local research/project harness that can reliably manage long-running scientific or analysis projects. The harness should support project continuation, branch/workstream control, task context, run provenance, result promotion, release packaging, data/decision records, and future extension layers. Skills are the current entry points; plugins, hooks, dashboards, and subskills are deferred layers, not discarded features.

## Current Product Principle

Core first, extensions later:

```text
Priority 1: core project-control loop must work end-to-end.
Priority 2: release/data/decision/handoff capabilities complete the scientific workflow.
Priority 3: plugin/hooks/dashboard/subskills/adapters are added after core semantics are stable.
```

Deferred does **not** mean removed. Every core design decision should preserve extension points for later plugin packaging, hooks, dashboards, subskills, and cross-agent adapters.

## Current Phase
Superseded. Active execution has moved to `docs/RESEARCH_PROJECT_OS_COMPLETE_DEVELOPMENT_PLAN.md`, starting with P0.1 schema freeze and project identity/event journal helpers.

## Historical note: 2026-06-24 externalization follow-up

- Portable externalization is now part of the active implementation track under the complete development plan.
- Current near-term execution order:
  1. keep externalization report-first and approval-gated
  2. adopt real pilot projects into `.project_os/` with dry-run first
  3. run non-destructive externalization planning on real projects
  4. report old absolute-path / symlink / missing-copy repair points without auto-rewriting them

## Historical note: 2026-06-24 disposable E2E baseline

- `skills/local/research-project-os/scripts/smoke_project_os_e2e.py` is now the release/dogfood smoke for this harness.
- `docs/RESEARCH_PROJECT_OS_E2E_COVERAGE.md` records the current coverage audit.
- Current audit result: all 80 public `project_os.py` subcommands are covered by the disposable smoke, including approval-gate negative paths and no-hardlink/no-symlink externalization checks.

## Architecture Layers

| Layer | Purpose | Current/Planned Artifacts |
|---|---|---|
| L0 Contract/schema layer | Defines stable project facts and file contracts | `references/*.md`, `.project_os/spec/*.md`, TSV/JSON schemas |
| L1 Core harness engine | Deterministic CLI operations on project files | `scripts/project_os.py`, small wrapper scripts |
| L2 Project files | Durable project memory and human entry points | `.project_os/`, `PROJECT_STATE.md`, `RUNS_INDEX.tsv`, `RESULTS_INDEX.md`, `DATA_ASSETS.md`, `DECISIONS.md` |
| L3 Agent entry layer | Natural-language use by Codex/agents | `research-project-os`, `project-skeleton`, future subskills |
| L4 Distribution/automation layer | Install, enforce, visualize, integrate | future plugin packaging, hooks, dashboards, adapters |

## Filesystem Topology Decision

Adopt a **branch-first physical workspace architecture**.

Reference:

- `docs/RESEARCH_PROJECT_OS_BRANCH_FIRST_ARCHITECTURE.md`

Rules:

1. Each branch/workstream gets a physical workspace:
   - `.project_os/branches/<branch_id>/`
2. Each formal run uses a branch-aware default path:
   - `runs/<branch_id>/<run_id>/`
3. Branch-local tasks live under the branch workspace:
   - `.project_os/branches/<branch_id>/tasks/<task_id>/`
4. Global indexes remain mandatory:
   - `.project_os/indexes/*.tsv`
5. Project-level root docs remain the human entry points:
   - `PROJECT_STATE.md`, `RESULTS_INDEX.md`, `DATA_ASSETS.md`, `RUNS_INDEX.tsv`, `DECISIONS.md`
6. Branch-first layout is the target for new projects; older flat layouts may need migration support later.

## Phase 0: Scope reset and state alignment

### Objective
Make the project plan reflect the full core harness scope and explicitly defer, not delete, plugin/hooks/dashboard/subskill layers.

### Steps
1. Update `PROJECT_STATE.md` with the corrected scope decision.
2. Replace `task_plan.md` with this full-core roadmap.
3. Add scope findings to `findings.md`.
4. Add session progress to `progress.md`.
5. Keep unrelated mirror-sync updates separate from harness planning commits.
6. Commit planning/state update after user approval.

### Acceptance
- Plan states that branch/workstream and run lifecycle are core.
- Plan states that hooks/plugin/dashboard/subskills are deferred extension layers, not removed.
- Project state points future agents to this roadmap.

### Status
- **in_progress**

---

## Phase 1: Core contract and schema freeze

### Objective
Define stable file contracts before expanding commands. This prevents future plugin/hooks/dashboard/subskills from depending on unstable ad hoc fields.

### Files
- `skills/local/research-project-os/references/harness_contract.md`
- `skills/local/research-project-os/references/task_schema.md`
- `skills/local/research-project-os/references/run_manifest_schema.md`
- `skills/local/research-project-os/references/result_index_schema.md`
- `skills/local/research-project-os/references/data_asset_schema.md`
- New: `skills/local/research-project-os/references/branch_schema.md`
- New: `skills/local/research-project-os/references/lifecycle_events.md`
- New: `docs/RESEARCH_PROJECT_OS_BRANCH_FIRST_ARCHITECTURE.md`
- `skills/local/research-project-os/templates/project_os/spec/*.md`

### Steps
1. Inventory existing schemas in references and template spec files.
2. Define stable IDs:
   - `project_id`
   - `branch_id`
   - `task_id`
   - `run_id`
   - `result_id`
   - `asset_id`
   - `release_id`
3. Define required branch fields:
   - `branch_id`
   - `status`
   - `parent_branch_id`
   - `title`
   - `created_at`
   - `closed_at`
   - `objective`
   - `notes`
4. Define task-to-branch relation:
   - every task has `branch_id`
   - task may have `parent_task_id`
   - task stage records workflow position
5. Define run-to-task/branch relation:
   - every run has `task_id`
   - run inherits or records `branch_id`
   - run status transitions are explicit
6. Define result-to-run/task/branch relation:
   - every result has `run_id`, `task_id`, `branch_id`
   - accepted/current states are separate from candidate registration
7. Define release-to-result relation:
   - release packages accepted/current results only unless explicitly overridden
8. Define lifecycle event names for later hooks without implementing hooks now:
   - `project.initialized`
   - `branch.created`
   - `branch.changed`
   - `task.created`
   - `task.changed`
   - `run.created`
   - `run.closed`
   - `result.registered`
   - `result.promoted`
   - `release.created`
   - `state.updated`
9. Decide JSON/TSV canonical fields and keep backward compatibility notes.
10. Freeze the branch-first path contract:
   - `.project_os/branches/<branch_id>/`
   - `.project_os/branches/<branch_id>/tasks/<task_id>/`
   - `runs/<branch_id>/<run_id>/`
   - `current/branches/<branch_id>/`
   - `current/project/`
11. Update template `.project_os/spec/*.md` with the same contracts.
12. Record migration expectations for earlier flat layouts without implementing destructive migration.

### Acceptance
- Schema references and template specs agree.
- All future commands can target stable IDs and lifecycle events.
- Hooks/dashboard/plugin can later observe stable events without changing core files.

### Status
- **pending**

---

## Phase 2: Branch/workstream management

### Objective
Make branch/workstream a first-class harness object with a **physical workspace per branch** so multi-direction scientific work does not become a flat list of runs.

### Files
- `skills/local/research-project-os/scripts/project_os.py`
- `skills/local/research-project-os/references/branch_schema.md`
- `docs/RESEARCH_PROJECT_OS_BRANCH_FIRST_ARCHITECTURE.md`
- `skills/local/research-project-os/templates/project_os/indexes/.gitkeep`
- `.project_os/indexes/branches.tsv` template behavior
- `.project_os/branches/<branch_id>/` template behavior
- `skills/local/research-project-os/SKILL.md`

### New/updated CLI commands
- `create-branch`
- `set-current-branch`
- `list-branches`
- `show-branch`
- `archive-branch`
- `refresh-indexes` updates branches
- `doctor` reports branch pointer health

### Steps
1. Add `branches.tsv` read/write helpers if missing.
2. Add branch row creation function.
3. Add branch workspace creation function for:
   - `.project_os/branches/<branch_id>/branch.json`
   - `objective.md`
   - `context.md`
   - `handoff.md`
   - `decisions.md`
   - `research/`
   - `notes/`
   - `tasks/`
4. Ensure a default `main` branch workspace is created during `new-project` and `init`.
5. Add `create-branch --title ... --branch-id ... --parent-branch-id ...`.
6. Add `set-current-branch --branch-id ...`.
7. Add `list-branches` with human and `--json` output.
8. Add `show-branch --branch-id ...`.
9. Add `archive-branch --branch-id ... --notes ...` without deleting tasks/runs/results or branch workspace files.
10. Update task creation so branch-local task path becomes:
    - `.project_os/branches/<branch_id>/tasks/<task_id>/`
11. Update run creation so default run path becomes:
    - `runs/<branch_id>/<run_id>/`
12. Update result registration so each result records branch and can later promote into:
    - `current/branches/<branch_id>/`
13. Update `doctor` to detect missing current branch, missing branch rows, missing branch workspaces, and tasks/runs pointing to unknown branches.
14. Update `SKILL.md` with branch workspace rules.
15. Update README/routing docs with branch-first examples.

### Acceptance
- A project can hold multiple workstreams without mixing runs/results.
- Current branch can be resolved from files.
- Each branch has an inspectable physical workspace.
- Branch archive never deletes history.
- Future hooks can attach to `branch.created` and `branch.changed` events.

### Status
- **pending**

---

## Phase 3: Task and context management upgrade

### Objective
Make tasks reliable units of work with explicit context manifests, stages, handoff, and branch linkage.

### Files
- `scripts/project_os.py`
- `references/task_schema.md`
- `references/context_manifest_schema.md`
- `templates/project_os/tasks/example_task/*`
- `templates/project_os/workflow.md`

### New/updated CLI commands
- `create-task` refine branch defaults
- `set-current-task`
- `list-tasks`
- `show-task`
- `update-task-stage`
- `close-task`
- `add-context`
- `remove-context`
- `update-handoff`

### Steps
1. Review current `task.json` schema.
2. Add optional fields for priority, owner, branch, stage, and status transitions if not present.
3. Implement `list-tasks --status --branch-id --json`.
4. Implement `show-task --task-id` to print objective, branch, stage, and context manifest summary.
5. Implement `update-task-stage --task-id --stage Intake|Plan|Research|Run|Evaluate|Promote|Archive|Release`.
6. Implement `close-task --task-id --status completed|blocked|archived --notes ...`.
7. Implement `add-context --task-id --type ... --path ... --purpose ... --required true|false`.
8. Implement `remove-context --task-id --path ...` using safe non-destructive manifest editing.
9. Implement `update-handoff --task-id --message ...` or stdin input.
10. Ensure `start` resolves current branch first, then loads only the current branch task manifest plus required root files.
11. Ensure `doctor` reports missing required context files.
12. Update workflow docs so tasks are the unit of continuation.

### Acceptance
- A future agent can resume from current task without reading the whole repo.
- Task stage is explicit and machine-readable.
- Context manifest is editable through CLI, not by fragile manual edits only.
- Future dashboards can render task status from stable task/index fields.

### Status
- **pending**

---

## Phase 4: Run lifecycle control

### Objective
Make run control complete enough for real analysis provenance: create, update, attach commands/inputs/outputs/metrics, close, index, and resume current run.

### Files
- `scripts/project_os.py`
- `references/run_manifest_schema.md`
- `templates/project_os/spec/run_provenance.md`
- root `RUNS_INDEX.tsv` behavior

### New/updated CLI commands
- `create-run`
- `set-current-run`
- `show-run`
- `list-runs`
- `update-run`
- `add-run-input`
- `add-run-command`
- `add-run-output`
- `add-run-metric`
- `close-run`

### Steps
1. Review existing `RUN_MANIFEST.json` structure.
2. Add `branch_id` to run manifest if not already written.
3. Add `set-current-run --run-id ...`.
4. Add `show-run --run-id ...` with status, task, branch, outputs, metrics.
5. Add `list-runs --task-id --branch-id --status --json`.
6. Add `update-run --run-id --status ... --notes ...` for safe metadata updates.
7. Add `add-run-input --run-id --path ... --kind ... --checksum optional`.
8. Add `add-run-command --run-id --command ... --cwd ... --exit-code optional`.
9. Add `add-run-output --run-id --path ... --kind ... --title ...`.
10. Add `add-run-metric --run-id --name ... --value ... --unit optional`.
11. Refine `close-run` so status transition is explicit and `closed_at` is written.
12. Ensure `refresh-indexes` rebuilds `.project_os/indexes/runs.tsv` and root `RUNS_INDEX.tsv`.
13. Ensure `doctor` detects active current run, closed current run, missing run manifest, malformed manifest, and orphan run rows.
14. Preserve future hook event points: `run.created`, `run.updated`, `run.closed`.

### Acceptance
- Every formal run can be traced to task, branch, inputs, commands, outputs, and metrics.
- Default formal runs live under `runs/<branch_id>/<run_id>/`.
- Current run can be resumed or cleared intentionally.
- Closing a run updates indexes without promoting results automatically.
- Future hooks can enforce run-close checks without changing command semantics.

### Status
- **pending**

---

## Phase 5: Result lifecycle control

### Objective
Make results first-class objects with clear statuses and safe promotion rules.

### Files
- `scripts/project_os.py`
- `references/result_index_schema.md`
- `templates/project_os/spec/result_curation.md`
- root `RESULTS_INDEX.md`
- `current/`

### New/updated CLI commands
- `register-result`
- `list-results`
- `show-result`
- `accept-result`
- `promote-result`
- `supersede-result`
- `show-current`

### Steps
1. Review existing result schema and statuses.
2. Add `branch_id` to result rows if not already present.
3. Ensure `register-result` links result to run/task/branch.
4. Add `list-results --task-id --branch-id --status --json`.
5. Add `show-result --result-id ...`.
6. Add `accept-result --result-id ... --notes ...` to mark accepted without copying to `current/`.
7. Refine `promote-result --result-id --to current/... --apply`:
   - dry-run by default;
   - explicit `--apply` required;
   - explicit `--replace` required if target exists;
   - record `accepted_at` or `promoted_at`.
8. Add `supersede-result --result-id --by-result-id ... --notes ...`.
9. Add `show-current` to summarize current accepted files.
10. Update `RESULTS_INDEX.md` generation/update rules.
11. Ensure promotion records source run/task/branch.
12. Ensure branch-level promotion target can be `current/branches/<branch_id>/` and project-level promotion target can be `current/project/`.
12. Preserve future hook event points: `result.registered`, `result.accepted`, `result.promoted`, `result.superseded`.

### Acceptance
- Candidate, accepted, current, superseded, and legacy are distinct.
- Users can find current results without browsing run folders.
- Promotion is safe and explicit.
- Future release packaging can consume accepted/current results directly.

### Status
- **pending**

---

## Phase 6: Data asset management

### Objective
Track input data, references, external resources, and immutable/mutable assets so run provenance is meaningful.

### Files
- `scripts/project_os.py`
- `references/data_asset_schema.md`
- root `DATA_ASSETS.md`
- `.project_os/indexes/assets.tsv`

### New/updated CLI commands
- `register-asset`
- `list-assets`
- `show-asset`
- `update-asset`
- `checksum-asset`
- `refresh-assets`

### Steps
1. Review asset schema.
2. Define required fields: `asset_id`, `kind`, `path`, `version`, `source_url`, `source_note`, `immutable`, `status`, `registered_at`, `checksum`, `notes`.
3. Implement `register-asset --path ... --kind ... --source-url ... --version ...`.
4. Implement `list-assets --kind --status --json`.
5. Implement `show-asset --asset-id ...`.
6. Implement `update-asset --asset-id ...` for status/version/notes.
7. Implement `checksum-asset --asset-id ...` or `--path ...`.
8. Implement `refresh-assets` to align `.project_os/indexes/assets.tsv` and `DATA_ASSETS.md` summaries.
9. Allow `create-run` or `add-run-input` to reference registered `asset_id`.
10. Preserve future hook event point: `asset.registered`, `asset.updated`.

### Acceptance
- Runs can reference stable data assets instead of ad hoc paths only.
- Data provenance is visible from root docs and machine-readable indexes.
- Asset checksums are available when practical but not forced for every exploratory file.

### Status
- **pending**

---

## Phase 7: Decision and handoff management

### Objective
Make project decisions and stopping points durable without bloating `PROJECT_STATE.md`.

### Files
- `scripts/project_os.py`
- root `DECISIONS.md`
- task `decisions.md`
- task `handoff.md`
- `PROJECT_STATE.md`

### New/updated CLI commands
- `record-decision`
- `list-decisions`
- `update-handoff`
- `summarize-state`

### Steps
1. Define decision entry format: date, status, context, decision, rationale, consequences, links.
2. Implement `record-decision --scope project|task --task-id optional --title ... --status proposed|accepted|superseded|rejected`.
3. Support stdin/multiline body for detailed decisions.
4. Implement `list-decisions --scope --status --json`.
5. Expand `update-handoff` to update task handoff and optionally root `PROJECT_STATE.md` next step.
6. Implement `summarize-state` to print current project, branch, task, run, and current results.
7. Ensure `PROJECT_STATE.md` remains thin and points to details.
8. Preserve future hook event point: `decision.recorded`, `handoff.updated`, `state.updated`.

### Acceptance
- Important decisions are searchable and not lost in chat.
- Future agents can stop and resume cleanly.
- `PROJECT_STATE.md` does not become a raw log.

### Status
- **pending**

---

## Phase 8: Release packaging

### Objective
Turn accepted/current results into reproducible, shareable release folders.

### Files
- `scripts/project_os.py`
- `references/release_packaging.md` or existing template spec
- `templates/project_os/spec/release_packaging.md`
- root `release/`

### New CLI commands
- `build-release`
- `list-releases`
- `show-release`
- `validate-release`

### Steps
1. Define release schema: `release_id`, created time, source results, source runs, files, checksums, notes.
2. Implement `build-release --release-id ... --result-id ... --to release/<id> --apply`.
3. Dry-run by default; require `--apply` to copy/write release files.
4. Generate `MANIFEST.tsv` listing files, source result IDs, source run IDs, checksums, and notes.
5. Generate `CHECKSUMS.tsv` or checksum columns in manifest.
6. Generate release `README.md` with purpose, included results, provenance, environment notes, and caveats.
7. Implement `list-releases`.
8. Implement `show-release --release-id ...`.
9. Implement `validate-release --release-id ...` to check manifest paths and checksums.
10. Preserve future hook event point: `release.created`, `release.validated`.

### Acceptance
- Accepted results can be packaged without manual folder archaeology.
- Release package is reproducible and provenance-linked.
- Release packaging does not replace or delete underlying runs/results.

### Status
- **pending**

---

## Phase 9: Index, doctor, and validation improvements

### Objective
Make the harness self-diagnosing enough that users can repair partial adoption or inconsistent state.

### Files
- `scripts/project_os.py`
- `references/harness_contract.md`
- `README.md`

### Commands
- `status`
- `doctor`
- `validate`
- `refresh-indexes`
- new optional: `repair-plan`

### Steps
1. Standardize command output with optional `--json` for core read commands.
2. Expand `status` to summarize project, branch, task, run, result, release.
3. Expand `doctor` to report:
   - missing `.project_os/`
   - missing root docs
   - invalid current branch/task/run
   - tasks without branches
   - runs without tasks/branches
   - results without runs
   - assets missing paths
   - releases missing manifests
4. Add fix suggestions for each doctor finding.
5. Keep actual repairs explicit; do not auto-modify unless command name and `--apply` make it clear.
6. Expand `validate` for strict machine checks.
7. Add `repair-plan` if useful: prints proposed fixes without applying.
8. Ensure `refresh-indexes` rebuilds task, branch, run, result, asset, and release indexes.

### Acceptance
- Users can understand why a project is unhealthy.
- Repair remains deliberate and transparent.
- Future hooks can call `doctor`/`validate` later without adding new semantics.

### Status
- **pending**

---

## Phase 10: Agent entry and natural-language routing update

### Objective
Keep the user-facing interface simple while the core harness becomes more capable.

### Files
- `skills/local/research-project-os/SKILL.md`
- `skills/local/project-skeleton/SKILL.md`
- `README.md`
- `docs/SKILL_ROUTING_MATRIX.md`

### Steps
1. Update `research-project-os` description to include branch/workstream, run lifecycle, result promotion, release packaging, and data assets.
2. Keep `project-skeleton` short and focused on bootstrap/resume.
3. Add natural trigger examples:
   - `项目骨架` -> detect bootstrap/resume
   - `开工` -> start/resume
   - `新建一个分析分支` -> create branch
   - `切到这个分支` -> set current branch
   - `开始一次正式运行` -> create run
   - `关闭这个run` -> close run
   - `记录这个结果` -> register result
   - `设为当前结果` -> promote result with approval
   - `打包release` -> build release
   - `登记这个数据源` -> register asset
4. Ensure skill instructions always prefer dry-run before risky writes.
5. Ensure promotion/release operations require explicit user approval.
6. Keep `SKILL.md` concise; detailed rules stay in references.

### Acceptance
- User can operate the harness through short natural phrases.
- Skill text remains a router, not a giant manual.
- Future subskills can split by trigger category without rewriting the core CLI.

### Status
- **pending**

---

## Phase 11: Plugin packaging plan, deferred but interface-ready

### Objective
Prepare the core harness to become a plugin later without doing plugin packaging now.

### Future files
- `plugins/research-project-os/.codex-plugin/plugin.json`
- `plugins/research-project-os/skills/`
- `plugins/research-project-os/assets/`
- `plugins/research-project-os/hooks/` later, disabled by default

### Steps now
1. Avoid hard-coded absolute paths in skill references/scripts.
2. Keep templates and scripts self-contained under the skill directory.
3. Keep CLI commands stable and documented.
4. Maintain a clear version/changelog note for breaking schema changes.
5. Keep future plugin manifest requirements in a reference note, not active packaging.

### Later implementation steps
1. Scaffold plugin manifest.
2. Bundle skills, references, scripts, and templates.
3. Add local marketplace entry.
4. Install locally and verify skill availability.
5. Document install/uninstall and versioning.

### Acceptance for now
- No plugin package is required for core harness use.
- Nothing in the core design blocks plugin packaging later.

### Status
- **deferred / interface reserved**

---

## Phase 12: Hooks plan, deferred but interface-ready

### Objective
Do not require hooks for current operation, but design core commands so future hooks can enforce rules cleanly.

### Future hook candidates
- `SessionStart`: remind/load project state.
- `PreToolUse`: warn before risky shell/file operations in a harness project.
- `PostToolUse`: suggest registering outputs after formal runs.
- `Stop`: remind to update handoff/state.
- `PermissionRequest`: require extra confirmation for promote/release/destructive operations.

### Steps now
1. Define lifecycle event names in `references/lifecycle_events.md`.
2. Ensure commands support dry-run and machine-readable output where useful.
3. Ensure commands are idempotent or fail safely.
4. Ensure promote/release/destructive operations are explicit and auditable.
5. Do not add active hooks yet.

### Later implementation steps
1. Add optional `hooks/hooks.json` in plugin or project config.
2. Start with non-destructive reminder hooks only.
3. Add enforcement hooks only after user trusts the project hook layer.
4. Keep hooks disabled or absent by default in plugin packaging unless explicitly documented.

### Acceptance for now
- Core harness works without hooks.
- Future hooks can call existing CLI commands instead of inventing new logic.

### Status
- **deferred / interface reserved**

---

## Phase 13: Dashboard/export plan, deferred but interface-ready

### Objective
Allow future visual dashboards without making generated files the source of truth.

### Future outputs
- `.project_os/exports/task_graph.html`
- `.project_os/exports/run_graph.html`
- `.project_os/exports/result_dashboard.html`
- optional `.json` export bundle

### Steps now
1. Keep canonical data in Markdown/TSV/JSON.
2. Add `--json` output to list/show commands where practical.
3. Keep indexes normalized enough for later export.
4. Avoid storing dashboard-only state.

### Later implementation steps
1. Add `export-dashboard` command.
2. Generate task/run/result graph files from indexes.
3. Add static HTML reports.
4. Optionally add SQLite export as generated view only.

### Acceptance for now
- Dashboard can be added later from existing indexes.
- Generated views are never canonical state.

### Status
- **deferred / interface reserved**

---

## Phase 14: Subskill split plan, deferred but interface-ready

### Objective
Keep one router skill for now, but allow future split if trigger categories become stable.

### Candidate future subskills
- `project-os-branch`
- `project-os-task`
- `project-os-run`
- `project-os-result`
- `project-os-data`
- `project-os-release`

### Steps now
1. Keep command groups clean in `project_os.py`.
2. Keep references separated by domain.
3. Avoid duplicating schema text inside `SKILL.md`.
4. Use natural trigger examples to identify stable future boundaries.

### Later implementation steps
1. Split only if main router becomes too large or routing becomes ambiguous.
2. Each subskill calls the same CLI.
3. Subskills must not fork schemas or create competing conventions.

### Acceptance for now
- Single router remains usable.
- Future subskills can be added without changing the project file contract.

### Status
- **deferred / interface reserved**

---

## Immediate Implementation Order

### Batch A: Contract and branch foundation
1. Add `branch_schema.md`.
2. Add `lifecycle_events.md`.
3. Add `docs/RESEARCH_PROJECT_OS_BRANCH_FIRST_ARCHITECTURE.md`.
4. Update schema references to include branch-first path relations.
5. Add default branch workspace behavior to init/new-project if incomplete.
6. Implement branch commands and branch workspace creation.
7. Update task/run/result rows to carry branch information consistently.

### Batch B: Run and task control
8. Add task list/show/stage/close/context/handoff commands.
9. Add run list/show/set-current/update/add-input/add-command/add-output/add-metric commands.
10. Expand run manifest and run index behavior with `runs/<branch_id>/<run_id>/`.
11. Expand status/doctor around branch-task-run relationships.

### Batch C: Result and asset control
11. Add result list/show/accept/supersede/show-current commands.
12. Refine promote-result safety behavior.
13. Add asset register/list/show/update/checksum commands.
14. Link assets into run inputs.

### Batch D: Release and state
15. Implement build-release.
16. Implement release manifest/checksum/README generation.
17. Add decision and handoff commands.
18. Add project summary/status command improvements.

### Batch E: Agent routing and docs
19. Update `research-project-os` skill description and body.
20. Update `project-skeleton` examples if needed.
21. Update README and routing docs.
22. Sync registry and validate skill metadata.
23. Commit in small batches, keeping unrelated global mirror updates separate.

### Batch F: Deferred interface readiness
24. Keep plugin packaging notes updated.
25. Keep hook lifecycle event names stable.
26. Keep dashboard export assumptions stable.
27. Keep subskill boundaries documented but unimplemented until needed.

## Non-goals for Current Core Phase

- Do not implement active hooks yet.
- Do not package as plugin yet.
- Do not build editable/rich dashboard UI yet; only generated dashboard/export views are allowed.
- Do not split subskills yet.
- Do not add destructive cleanup commands.
- Do not replace project-specific scientific plans.

## Success Criteria

The core harness is successful when a project can:

1. Initialize or adopt `.project_os/`.
2. Resolve current branch, task, and run.
3. Manage multiple workstreams without mixing provenance.
4. Represent each branch as both a global index row and a physical workspace.
5. Create and close formal runs with structured provenance.
6. Register, accept, promote, supersede, and find results.
7. Track data assets used by runs.
8. Record key decisions and handoff notes.
9. Build a release package from accepted/current results.
10. Let a future session continue from files instead of chat memory.
11. Leave stable extension points for plugin, hooks, dashboards, and subskills.

## Implementation Status Update — 2026-06-23

- Batch A is implemented for the branch-first foundation.
- Batch B is substantially implemented: core run create/list/show/close/update plus appenders for input/command/output/metric are available; task stage/close/context helpers are available.
- Batch C is substantially implemented: result register/promote/list/show plus accept/supersede/show-current are available; asset register/list/show/update/checksum/refresh and run input asset references are available.
- Batch D is substantially implemented: decision/handoff commands, summarize-state, release build/list/show/validate, and initial flat -> branch-first migration are available.
- Integrity hardening now includes advisory lock, `doctor --repair-plan`, derived-view drift checks, task dependency DAG checks, result replacement DAG checks, and event reference checks.
- Next implementation frontier: real-project migration/adoption dogfooding and remaining P2 extensions; run parameter/package capture and major code splitting are now implemented in later status updates.

## Implementation Status Update — 2026-06-23 task/run split

- P1.11 splitting continued: task lifecycle and run provenance commands now live in `skills/local/research-project-os/scripts/_task_run.py`.
- `_result_release.py` now reuses `_task_run.py` run/task path helpers instead of keeping a second simplified resolver.
- Full task/run/result/release smoke passed with validate 0 errors / 0 warnings and doctor `ok=true`.
- Next implementation frontier: split asset helper/commands into `_assets.py`, then optionally split decision/handoff, while keeping `project_os.py` as the stable CLI facade.

## Implementation Status Update — 2026-06-23 asset split

- P1.11 splitting continued: asset registry/checksum/usage commands and helpers now live in `skills/local/research-project-os/scripts/_assets.py`.
- `_task_run.py` now reuses `_assets.py` for asset lookup and usage writes instead of carrying duplicate helper logic.
- Asset split smoke passed with release validation true, validate 0 errors / 0 warnings, doctor `ok=true`, and route `登记数据` -> `register_asset`.
- Next implementation frontier after asset split was decision/handoff extraction; that split is now recorded in the following update.

## Implementation Status Update — 2026-06-23 decision/handoff split

- P1.11 splitting continued: decision journal, handoff, and state summary commands now live in `skills/local/research-project-os/scripts/_decision_handoff.py`.
- `project_os.py` remains the stable CLI facade; `record-decision`, `list-decisions`, `update-handoff`, and `summarize-state` keep the same public command names and arguments.
- Decision/handoff smoke passed with release validation true, validate 0 errors / 0 warnings, doctor `ok=true`, route `记录决策` -> `record_decision`, and route `更新交接` -> `update_handoff`.
- Final validation after the split passed: `python3 -m py_compile` on the CLI/modules; `python3 scripts/validate_skills.py` returned 70 skills / 0 errors / 11 existing warnings; `python3 scripts/sync_skills.py --dry-run` returned total 679 / ok 592 / skip 65 / update 20 / write 2.
- Next implementation frontier after decision/handoff split was project/bootstrap/branch/adapters extraction; that split is now recorded below.

## Implementation Status Update — 2026-06-23 project/branch split

- P1.11 splitting continued: project bootstrap, adapter installation, status/start, refresh-indexes, and branch commands now live in `skills/local/research-project-os/scripts/_project_branch.py`.
- `project_os.py` remains the stable CLI facade; `init`, `new-project`, `install-adapters`, `build-adapters`, `status`, `start`, `refresh-indexes`, `create-branch`, `set-current-branch`, `list-branches`, `show-branch`, and `archive-branch` keep the same public command names and arguments.
- Bootstrap/branch/adapter smoke passed with validate 0 errors / 0 warnings and doctor `ok=true`.
- Route/export smoke still passed after the split, including `route 开工`, `route 新建分支`, generated dashboard JSON/HTML/SQLite, validate 0 errors / 0 warnings, and doctor `ok=true`.
- Migration smoke still passed after the split for old flat task/run/result adoption with path rewrite, validate 0 errors / 0 warnings, and doctor `ok=true`.
- Next implementation frontier after project/branch split was migration extraction with richer conflict reports; that split is now recorded below.

## Implementation Status Update — 2026-06-23 migration split

- P1.11 splitting continued: flat -> branch-first adoption and migration logic now lives in `skills/local/research-project-os/scripts/_migration.py`.
- `project_os.py` remains the stable CLI facade; `migrate-branch-first` keeps the same public command name and arguments.
- Dry-run migration diagnostics now expose a structured summary, conflict list, warning list, and `safe_to_apply` boolean before any apply operation.
- Synthetic normal migration smoke passed with `safe_to_apply=true`, apply, validate 0 errors / 0 warnings, and doctor `ok=true`.
- Synthetic conflict migration smoke correctly reported blocking conflicts and missing path warnings with `safe_to_apply=false`.
- Next implementation frontier after migration split was validate/doctor facade cleanup; that split is now recorded below.

## Implementation Status Update — 2026-06-23 health split

- P1.11 splitting continued: `validate` and `doctor` command bodies now live in `skills/local/research-project-os/scripts/_health.py`.
- `_integrity.py` remains the shared helper layer for integrity checks and repair-plan generation.
- `project_os.py` remains the stable CLI facade; `validate` and `doctor` keep the same public command names and arguments.
- Temporary health smoke passed with validate 0 errors / 0 warnings, doctor `ok=true`, and `doctor --repair-plan` producing no repairs on a clean project.
- Final validation after the split passed: `python3 -m py_compile` on the CLI/modules; `python3 scripts/validate_skills.py` returned 70 skills / 0 errors / 11 existing warnings; `python3 scripts/sync_skills.py --dry-run` returned total 679 / ok 592 / skip 65 / update 20 / write 2.
- Next implementation frontier: dogfood `migrate-branch-first` on one real legacy project; continue improving diagnostics from real adoption evidence before active hooks/plugin work.

## Implementation Status Update — 2026-06-23 current/result view enhancement

- Result lifecycle display now has derived current views for `all`, `project`, and `branch` scopes.
- `show-current --audit` reports basic promotion-audit categories without changing canonical state.
- Generated `RESULTS_INDEX.md` now includes a `Current views` section before the status-grouped result list.
- Current/result smoke passed with project current count 1, branch current count 1, audit ok, validate 0 errors / 0 warnings, and doctor `ok=true`.
- Promotion audit has also been connected to validate/doctor warnings and repair-plan guidance.
- Negative smokes passed for missing current targets and duplicate current targets.
- Next implementation frontier remains real-project migration/adoption dogfooding; if no project path is available, continue with P1 consistency hardening or graph/dashboard polish.

## Implementation Status Update — 2026-06-23 dashboard graph export

- Generated dashboard/export now includes a derived graph payload.
- `.project_os/exports/dashboard.json` contains `graph.nodes`, `graph.edges`, and relation/kind counts.
- `.project_os/exports/dashboard.html` renders graph summary plus node/edge tables.
- `.project_os/exports/dashboard.sqlite` contains generated `graph_nodes` and `graph_edges` tables when `--sqlite` is used.
- Graph nodes cover project, branch, task, run, result, current target, asset, and release objects; edges cover ownership/provenance/promotion/asset/release relationships.
- Dashboard graph smoke passed with required nodes/edges and validate 0 errors / 0 warnings.
- Richer visual UI remains deferred; the generated graph data contract is now present for later dashboards.

## Implementation Status Update — 2026-06-23 journal snapshot audit

- P1.10 consistency hardening now includes journal/current snapshot coverage checks.
- `validate` / `doctor` report event references that no longer resolve to canonical branch/task/run/result/asset/release rows.
- `validate` / `doctor` report non-legacy snapshot rows that lack lifecycle event coverage.
- Rows older than a `project.adopted` event are tolerated as legacy/adopted state to avoid false positives during migration.
- Missing coverage is a warning and `doctor --repair-plan` points to `summarize-state` / provenance review; it does not synthesize or edit lifecycle events.
- Smoke passed for both a clean lifecycle and a negative manually inserted row without journal coverage.

## Implementation Status Update — 2026-06-24 run lifecycle provenance

- P1.2 run lifecycle enhancement now includes run package capture and detailed close-run summaries.
- `capture-run-env --pip-freeze --freeze-file docs/pip-freeze.txt` writes a run-local freeze file and records `environment.package_capture` in `RUN_MANIFEST.json`.
- `close-run` writes a detailed generated `RUN_SUMMARY.md` with identity, counts, parameters, inputs, commands, outputs, metrics, promoted targets, environment, package sample, and notes.
- Run lifecycle smoke passed with freeze file present, manifest metadata present, summary sections present, validate 0 errors / 0 warnings, and doctor `ok=true`.
- Next implementation frontier remains real-project adoption/migration dogfooding before active hooks/plugin work.

## Implementation Status Update — 2026-06-24 manual hooks dispatcher

- P2.1 now has a manual/report-only hooks foundation: `list-hooks` and `dispatch-hooks` are available through `project_os.py`.
- The dispatcher reads `.project_os/journals/events.jsonl` and can emit `session_summary`, `reminder`, `opt_in_maintenance`, and report-only placeholder `guard` reports.
- `dispatch-hooks --write-report` writes generated reports under `.project_os/exports/hooks/`; these reports are non-canonical derived views.
- Short-trigger routes for `hook状态`, `hooks状态`, `列出hooks`, `hook报告`, `hook提醒`, and `派发hook` now resolve to hooks CLI plans.
- Active automatic hooks remain a non-goal for the current phase; no hook handler auto-executes commands, writes canonical state, or bypasses promotion/release approval gates.
- Next implementation frontier remains real-project migration/adoption dogfooding and small consistency hardening before plugin packaging or active automatic hooks.

## Implementation Status Update — 2026-06-24 hooks dashboard/doctor advisory

- P2.1/P2.4 consistency hardening now exposes manual hooks status in generated dashboard outputs.
- `export-dashboard` JSON includes a `hooks` payload with config, event source, event counts, report counts, allowed kinds, and active-dispatcher advisory flags.
- Generated HTML renders Hooks status and Allowed hook kinds sections; SQLite exports `hooks_status` and `hooks_allowed_kinds` tables.
- `validate` and `doctor --repair-plan` now surface hooks config drift such as accidental active dispatcher config, unknown allowed kinds, or missing event source as warning/advisory items.
- Active automatic hooks remain deferred; these checks do not execute hook suggestions, do not write canonical state, and do not bypass approval gates.
- Next frontier remains additional real-project migration/adoption dogfooding or similarly small consistency hardening before plugin packaging or active automatic hooks.

## Implementation Status Update — 2026-06-24 real migration dogfood

- Real-project migration dogfood was run on `/tmp` copies of `/home/teng/pingtai_final_20260430`, not on the original project.
- The real sample covered old flat `.project_os/tasks/`, missing `project.json`, missing event journal, missing branch workspace, old index headers, and a flat run under `runs/<run_id>/`.
- Dry-run, copy-mode apply, move-mode apply, repeated target-exists diagnostics, and `--replace` dry-run all behaved as intended; copied/moved projects validated with 0 errors / 0 warnings and `start` resumed the expected branch/task.
- Migration output now mirrors `summary`, `conflicts`, `warnings`, and `safe_to_apply` at the top level of both dry-run and apply payloads for easier review and scripting.
- `doctor --repair-plan` now gives concrete `install-adapters --platforms codex|claude --apply` suggestions for missing adapter blocks.
- Next frontier remains more real legacy samples, especially real multi-branch old data and heavily hand-edited manifests; active hooks/plugin packaging remain deferred.

## Implementation Status Update — 2026-06-24 restore-journal hardening

- Added a minimal `restore-journal` command for initialized harnesses whose `.project_os/journals/events.jsonl` file is missing.
- The command is dry-run by default; `--apply --approved` creates only the missing journal and appends `journal.restored`. It does not overwrite existing journals or synthesize historical lifecycle coverage.
- `doctor --repair-plan` now points missing default event-source cases to approval-gated `restore-journal --apply --approved`; non-default `hooks.event_source` drift still routes to config review.
- Short-trigger route `恢复事件日志` plans `restore-journal` and requires `--approved` when `--apply` is requested.
- Manual hook reminders understand `journal.restored` and suggest validation/review commands without executing them.
- Targeted smoke and final non-destructive validation passed; active hooks, plugin packaging, and full crash replay remain deferred.

## Implementation Status Update — 2026-06-24 report-only recovery planner

- P2.3 now has a safe foundation slice: `plan-recovery` is exposed through `project_os.py` and implemented in `_recovery.py`.
- The planner reports stale advisory lock candidates, atomic-write tmp leftovers, malformed event journal lines, missing harness paths, runtime pointer drift, manifest/index drift, and stale generated views.
- `plan-recovery --write-report` writes only `.project_os/exports/recovery/recovery_plan_<timestamp>.json`; it does not replay events, roll back operations, delete tmp files, remove locks, or rewrite canonical state.
- Short-trigger routes `恢复计划`, `恢复检查`, and `崩溃恢复检查` now plan `plan-recovery` commands while preserving report-only safety notes.
- `doctor --repair-plan` surfaces recovery candidates as warning-level advisory and suggests `plan-recovery --write-report`; clean projects remain `ok=true`.
- Generated dashboard exports now include a recovery summary in JSON/HTML and SQLite tables `recovery_status` and `recovery_summary`.
- Full WAL replay/rollback and automatic lock/tmp cleanup remain deferred and require a separate explicit design.

## Implementation Status Update — 2026-06-24 dashboard current-result/promotion-audit view

- P2.4 dashboard/export now exposes current-result and promotion-audit derived views.
- `dashboard.json` includes `current_results` with all/project/branch current views, branch counts, and audit summary.
- `dashboard.html` renders Current results and promotion audit sections.
- `dashboard.sqlite` includes `current_results_status`, `current_results`, `current_result_branch_counts`, and `promotion_audit`.
- These are generated inspection views only. Canonical result state remains `.project_os/indexes/results.tsv`, result/task/run manifests, and `current/` targets; promotion and repair still require approval-gated CLI commands.

## Implementation Status Update — 2026-06-24 current-result short-trigger route

- Short-trigger routing now includes a dedicated read-only current-result inspection intent.
- `当前结果` / `查看当前结果` route to `show-current --scope <all|project|branch> --audit` and can narrow to branch scope when `--branch-id` is provided.
- This route is explicitly distinct from `设为当前结果` / `替换当前结果`, which remain approval-gated promotion flows.
- No canonical state is written: no result promotion, no `current/` repair, and no `results.tsv` rewrite.

## Implementation Status Update — 2026-06-24 summarize-state current-result/session focus alignment

- `summarize-state` now reports session-aware runtime focus through a `runtime_focus` payload, while preserving top-level `current_branch` / `current_task` / `current_run` compatibility fields.
- `summarize-state` now includes a read-only `current_results` derived summary with all/project/current-branch counts, project/current-branch rows, `audit_ok`, and promotion-audit warning counts.
- The current-result summary reuses the same helper layer as `show-current --audit` and dashboard exports, avoiding a second interpretation of current result state.
- No canonical state is written: no result promotion, no `current/` repair, no result manifest change, and no `results.tsv` rewrite.

## Implementation Status Update — 2026-06-24 status run/result summary hardening

- `status` now reports session-aware runtime focus through a `runtime_focus` payload, while preserving top-level `current_branch` / `current_task` / `current_run` compatibility fields.
- `status.runs_summary` includes active/open run counts, current run row, current branch/task active run counts, and a last-run row derived from `.project_os/indexes/runs.tsv`.
- `status.results_summary` includes candidate/accepted/current counts, latest candidate rows, project/current-branch current rows, `audit_ok`, and promotion-audit warning counts derived from `.project_os/indexes/results.tsv` and `current/` targets.
- No canonical state is written: no index refresh, no journal append, no result promotion, no `current/` repair, no run/result manifest change, and no `results.tsv` rewrite.

## Implementation Status Update — 2026-06-24 direct promotion/release approval gate

- Direct `promote-result --apply` now requires `--approved`; dry-run promotion remains available without approval.
- Direct `build-release --apply` now requires `--approved`; dry-run release packaging remains available without approval.
- The short-trigger router now emits executable promotion/release planned commands containing both `--apply` and `--approved` when the route was explicitly approved.
- This aligns direct CLI behavior with the documented rule that current promotion and release packaging are approval-gated write paths.

## Implementation Status Update — 2026-06-24 restore-journal direct approval gate

- Direct `restore-journal --apply` now requires `--approved`; dry-run journal restoration remains available without approval.
- The short-trigger router now emits executable `restore-journal` planned commands containing both `--apply` and `--approved` when `恢复事件日志` was explicitly approved.
- `doctor --repair-plan` and `plan-recovery` now suggest `restore-journal --apply --approved` for missing default journal recovery.
- This aligns direct CLI behavior with the documented rule that writing canonical event-source state is approval-gated.
