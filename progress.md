# Progress Log

## Session: 2026-05-25

### Phase 1: Planning documents
- **Status:** complete
- Actions taken:
  - Reverted earlier unconfirmed `nature-skills` draft changes.
  - Created `docs/BIOINFO_WRITING_REFACTOR_PLAN.md`.
  - Created `docs/SKILL_ROUTING_MATRIX.md`.
- Files created/modified:
  - `docs/BIOINFO_WRITING_REFACTOR_PLAN.md`
  - `docs/SKILL_ROUTING_MATRIX.md`

### Phase 2: Evidence orchestrator skill
- **Status:** complete
- Actions taken:
  - Initialized file-based planning for this refactor.
  - Created `skills/local/bioinfo-evidence-orchestrator/SKILL.md`.
  - Created `skills/local/bioinfo-evidence-orchestrator/references/evidence-pack-template.md`.
  - Ran validation with `python3 scripts/validate_skills.py`: 0 errors, 11 pre-existing credential-word warnings in existing mirrored skills.
  - Ran `python3 scripts/sync_skills.py --dry-run`: only registry writes expected.
  - Ran `python3 scripts/sync_skills.py --apply`: refreshed `registry/SKILL_INVENTORY.tsv` and `registry/skills.json`.
- Files created/modified:
  - `task_plan.md`
  - `findings.md`
  - `progress.md`
  - `skills/local/bioinfo-evidence-orchestrator/SKILL.md`
  - `skills/local/bioinfo-evidence-orchestrator/references/evidence-pack-template.md`

## Test Results

| Test | Input | Expected | Actual | Status |
|---|---|---|---|---|
| `nature-skills` cleanup | `git status --short` | clean | clean before Phase 2 | ✓ |
| skill validation | `python3 scripts/validate_skills.py` | 0 errors | 0 errors, existing warnings only | ✓ |
| registry entry | grep `bioinfo-evidence-orchestrator` registry | skill appears | local skill appears with 2 files | ✓ |

## Error Log

| Timestamp | Error | Attempt | Resolution |
|---|---|---:|---|
| 2026-05-25 | Unconfirmed draft skill files were created in `nature-skills` | 1 | Backed up and reverted before continuing |
| 2026-05-25 | `python scripts/validate_skills.py` failed: `python` command not found | 1 | Used `python3 scripts/validate_skills.py` |

### Phase 3: Bio manuscript writing router
- **Status:** complete
- Actions taken:
  - Created `skills/local/bio-paper-writing/SKILL.md`.
  - Created references:
    - `skills/local/bio-paper-writing/references/evidence-pack-input.md`
    - `skills/local/bio-paper-writing/references/article-types.md`
    - `skills/local/bio-paper-writing/references/section-workflows.md`
  - Preserved the hard boundary: writing consumes evidence and does not run analysis.

### Phase 4: Specialized bio writing skills
- **Status:** complete
- Actions taken:
  - Created `skills/local/bio-results-writing/` for Results prose from figures/tables/evidence packs.
  - Created `skills/local/bio-methods-writing/` for reproducible Methods from workflow provenance.
  - Created `skills/local/bio-polishing/` for bioinformatics manuscript polishing, translation, terminology, and overclaim checks.
  - Created `skills/local/bio-reviewer-response/` for bioinformatics reviewer responses covering batch effects, FDR, external validation, data leakage, reproducibility, and availability concerns.
  - Created `skills/local/bio-data-code-availability/` for GEO/SRA/ENA/BioProject/BioSample/PRIDE/GitHub/Zenodo-style availability wording and repository action checklists.
  - Created `skills/local/bio-paper2ppt/` for Chinese bioinformatics journal-club/group-meeting PPT planning and deck creation guidance.

### Phase 5: Validation and registry sync
- **Status:** complete
- Actions taken:
  - Ran `python3 scripts/validate_skills.py`: 0 errors, 11 pre-existing warnings in existing mirrored skills.
  - Ran `python3 scripts/sync_skills.py --dry-run`.
  - Ran `python3 scripts/sync_skills.py --apply` to refresh `registry/SKILL_INVENTORY.tsv` and `registry/skills.json`.
  - Re-ran `python3 scripts/validate_skills.py`: 0 errors.
  - Checked registry entries for `bio-paper-writing`, `bio-results-writing`, `bio-methods-writing`, `bio-polishing`, `bio-reviewer-response`, `bio-data-code-availability`, and `bio-paper2ppt`.

### Auto-routing enhancement
- **Status:** complete
- Actions taken:
  - Created `skills/local/bio-research-auto-router/` to catch vague Chinese/English bioinformatics and manuscript prompts.
  - Added `references/vague-prompt-map.md` with natural prompt examples and target routes.
  - Updated routing docs so users do not need to name specific skills.

## Session: 2026-06-23 — Harness-first roadmap planning

### Planning update
- **Status:** complete
- Actions taken:
  - Reframed the current work from "writing a skill" to building a reusable repository-local research/project harness.
  - Replaced the old active `task_plan.md` with a harness roadmap covering fresh-session trigger tests, CLI hardening, state/index stabilization, release packaging, dogfooding, subskill split decision, plugin packaging, and optional automation/dashboard work.
  - Added harness roadmap findings to `findings.md`.
  - Updated `PROJECT_STATE.md` separately to record the harness-first goal.

### Validation context
- Current known validation baseline: 70 skills, 0 errors, 11 existing mirrored-skill warnings.
- Current known sync context: `scripts/sync_skills.py --dry-run` reports unrelated global mirror updates pending; keep separate from harness commits.

## Session: 2026-06-23 — Full core harness roadmap reset

### Scope correction
- **Status:** complete
- Actions taken:
  - Corrected the roadmap from lean-only MVP to full core harness scope.
  - Marked branch/workstream management and run lifecycle control as core requirements.
  - Kept plugin packaging, hooks, dashboards, and subskills as deferred but explicitly reserved extension layers.
  - Rewrote `task_plan.md` with phases for schema, branch, task, run, result, asset, decision/handoff, release, indexing, agent routing, and deferred extension interfaces.

## Session: 2026-06-23 — Branch-first physical workspace decision

### Architecture update
- **Status:** complete
- Actions taken:
  - Added `docs/RESEARCH_PROJECT_OS_BRANCH_FIRST_ARCHITECTURE.md` as the formal branch-first filesystem design.
  - Updated `task_plan.md` so branch management now means both global branch indexes and physical branch workspaces under `.project_os/branches/<branch_id>/`.
  - Updated the roadmap so formal run paths default to `runs/<branch_id>/<run_id>/` and branch-level current outputs can live under `current/branches/<branch_id>/`.
  - Recorded the branch-first design rationale in `findings.md`.

## Session: 2026-06-23 — Branch-first schema formalization

### Schema update
- **Status:** complete
- Actions taken:
  - Added `docs/RESEARCH_PROJECT_OS_BRANCH_FIRST_SCHEMAS.md` as the formal TSV/JSON schema contract for branch-first layout.
  - Added `skills/local/research-project-os/references/branch_schema.md`.
  - Added `skills/local/research-project-os/references/lifecycle_events.md`.
  - Updated branch-aware references for task, run, result, asset, context manifest, harness contract, and workflow phases.
  - Updated `skills/local/research-project-os/SKILL.md` and `README.md` to reflect branch-first physical workspaces and branch-aware run paths.

### Validation
- `python3 scripts/validate_skills.py`: 70 skills, 0 errors, 11 existing mirrored-skill warnings.
- `python3 scripts/sync_skills.py --dry-run`: still shows unrelated global mirror updates pending; keep separate from harness schema work.
## Session: 2026-06-23 — Complete harness development plan merge

### Planning consolidation
- **Status:** complete
- Actions taken:
  - Added `docs/RESEARCH_PROJECT_OS_COMPLETE_DEVELOPMENT_PLAN.md` as the canonical merged development document.
  - Merged the earlier harness implementation plan, branch-first architecture, branch-first schemas, full-core `task_plan.md`, Codex/Claude adapter scope, hook deferral policy, and lessons from `addyosmani/agent-skills`.
  - Defined P0 as the immediate implementation scope: schema/constants freeze, branch-first init, branch commands, branch-local tasks, branch-aware runs/results, indexes/doctor/validate, skill routing, Codex/Claude adapters, and smoke adoption.
  - Reaffirmed that plugin packaging, active hooks, dashboards, and subskills are deferred but interface-reserved.
## Session: 2026-06-23 — Short trigger router formalization

### Routing layer
- **Status:** complete
- Actions taken:
  - Added `skills/local/research-project-os/references/short_trigger_router.md`.
  - Defined the routing chain: short phrase -> intent -> state check -> CLI action -> verification.
  - Covered bootstrap/resume, branch, task, run, result, data asset, decision, and release trigger groups.
  - Updated `research-project-os/SKILL.md` and `project-skeleton/SKILL.md` to route compact phrases through the new reference instead of treating them as loose keywords.
  - Updated the complete development plan P0.8 to make the short trigger router a formal P0 module.

## Session: 2026-06-23 — Review adoption into complete harness plan

### Documentation update
- **Status:** complete
- Actions taken:
  - Updated `docs/RESEARCH_PROJECT_OS_COMPLETE_DEVELOPMENT_PLAN.md` with adopted recommendations from `docs/RESEARCH_PROJECT_OS_PLAN_REVIEW.md` and `docs/RESEARCH_PROJECT_OS_REVIEW.md`.
  - Added explicit contracts for project-wide unique task/run/result IDs, `.project_os/indexes/*.tsv` as canonical registries, `.project_os/project.json`, and `.project_os/journals/events.jsonl`.
  - Clarified runtime pointer recovery, config semantics, promotion source-of-truth, result type vocabulary, and flat-to-branch migration mapping.
  - Reordered P0 to schema freeze -> init -> branch -> task+run -> doctor/validate -> result -> short router -> adapters -> smoke adoption.
  - Added P1 hardening items for integrity rules, asset usage impact, task DAG dependencies, structured repair plans, consistency hardening, migration implementation, and `project_os.py` split boundaries.
  - Marked older harness/branch/schema docs and `task_plan.md` as superseded by the complete plan.

## Session: 2026-06-23 — P0 branch-first CLI implementation slice

### Code implementation
- **Status:** complete for the first P0 vertical slice
- Actions taken:
  - Rewrote `skills/local/research-project-os/scripts/project_os.py` around the branch-first contract.
  - Added schema headers for `branches.tsv`, `tasks.tsv`, `runs.tsv`, `results.tsv`, `assets.tsv`, `asset_usage.tsv`, and `releases.tsv`.
  - Added `.project_os/project.json` initialization and `.project_os/journals/events.jsonl` append-only lifecycle journal support.
  - Implemented branch-first init/new-project layout: `.project_os/branches/main/`, `runs/main/`, `current/branches/main/`, and `current/project/`.
  - Added branch commands: `create-branch`, `set-current-branch`, `list-branches`, `show-branch`, and `archive-branch`.
  - Moved task creation to `.project_os/branches/<branch_id>/tasks/<task_id>/` and run creation to `runs/<branch_id>/<run_id>/`.
  - Added branch-aware list/show commands for tasks, runs, and results, plus `set-current-run`.
  - Updated result registration/promotion to carry branch/task/run provenance and promote only under `current/`.
  - Added Claude adapter generation via `CLAUDE.md` while preserving the Codex `AGENTS.md` adapter.
  - Updated template workflow/spec files to branch-first wording and added template `branch_model.md` / `event_journal.md`.

### Verification
- `python3 -m py_compile skills/local/research-project-os/scripts/project_os.py`: passed.
- P0 full temporary-project smoke passed: new-project -> create branch -> create task -> create run -> register result -> dry-run promotion -> apply promotion -> refresh-indexes -> start -> doctor -> validate.
- Smoke evidence: current promoted file existed, event journal had 9 events, doctor `ok=true`, validate `errors=0`, and method_a had 1 task / 1 run / 1 result.
- `python3 scripts/validate_skills.py`: 70 skills, 0 errors, 11 pre-existing warnings.
- `python3 scripts/sync_skills.py --dry-run`: still reports unrelated global mirror updates and registry writes; not applied.

## Session: 2026-06-23 — Asset/decision/release core command expansion

### Code implementation
- **Status:** complete for this P1/P0-adjacent batch
- Actions taken:
  - Extended `skills/local/research-project-os/scripts/project_os.py` with data asset commands: `register-asset`, `list-assets`, `show-asset`, `update-asset`, `checksum-asset`, and `refresh-assets`.
  - Added run provenance append commands: `add-run-input`, `add-run-command`, `add-run-output`, and `add-run-metric`; run inputs can now reference registered `asset_id` values and refresh `.project_os/indexes/asset_usage.tsv`.
  - Added generated `DATA_ASSETS.md` refresh from canonical `assets.tsv` plus asset usage rows.
  - Added decision and handoff commands: `record-decision`, `list-decisions`, `update-handoff`, and `summarize-state`.
  - Added release packaging commands: dry-run/apply `build-release`, `list-releases`, `show-release`, and `validate-release`; release packages include `README.md`, `MANIFEST.tsv`, `CHECKSUMS.tsv`, and copied artifacts.
  - Extended `doctor` / `validate` to cover asset status/checksum drift, asset usage references, and release package existence/headers.
  - Updated `research-project-os` skill docs, schema references, templates, README, and the complete development plan status section.

### Verification
- `python3 -m py_compile skills/local/research-project-os/scripts/project_os.py`: passed.
- Temporary-project smoke passed through new-project -> branch -> task -> run -> register asset -> add run provenance -> accepted result -> dry-run release -> applied release -> validate release -> decision -> handoff -> refresh-indexes -> validate -> doctor.
- Smoke result: `validate` returned 0 errors / 0 warnings, `doctor` returned `ok=true`.

### Follow-up expansion in same session
- Added result lifecycle helpers: `accept-result`, `supersede-result`, and `show-current`.
- Added task/context helpers: `update-task-stage`, `close-task`, `add-context`, and `remove-context`.
- Added `update-run` for status/result-status/notes updates.
- Added guarded `migrate-branch-first` dry-run/apply command for flat `.project_os/tasks/<task_id>/` and `runs/<run_id>/` layouts.
- Ran an additional migration smoke after patching legacy task defaults; validation passed with 0 errors / 0 warnings.

## Session: 2026-06-23 — Integrity / repair-plan hardening

### Code implementation
- **Status:** complete for this hardening batch
- Actions taken:
  - Added `.project_os/runtime/lock` advisory locking for state-changing CLI commands.
  - Added `doctor --repair-plan` with non-executing repair suggestions.
  - Added derived-view drift checks for `RUNS_INDEX.tsv`, `RESULTS_INDEX.md`, and `DATA_ASSETS.md`.
  - Added integrity checks for inactive branch active work, result replacement cycles, task dependency DAGs, current results owned by inactive tasks, cross-branch promotion audit warnings, and lifecycle event references.
  - Added `update-task`, `add-dependency`, and `remove-dependency`.
  - Enhanced run environment snapshots and made `close-run` write `RUN_SUMMARY.md`.
  - Added `references/integrity_rules.md` and synchronized skill/reference/template docs.

### Verification
- `python3 -m py_compile skills/local/research-project-os/scripts/project_os.py`: passed.
- Mini smoke for task dependencies, task metadata update, run close summary, and validate passed with 0 errors / 0 warnings.

## Session: 2026-06-23 — Migration index upgrade and run parameter/env capture

### Code implementation
- **Status:** complete for this batch
- Actions taken:
  - Added `add-run-parameter` for structured key=value run parameters.
  - Added `capture-run-env` with Python/platform/venv metadata and optional `--pip-freeze` package capture.
  - Extended `migrate-branch-first` dry-run/apply to detect and upgrade old `tasks.tsv`, `runs.tsv`, and `results.tsv` headers.
  - Migration now patches missing branch-aware result fields such as `branch_id`, `promoted_to`, and `replaced_by` where possible.
  - Updated skill and reference docs for the new commands.

### Verification
- `python3 -m py_compile skills/local/research-project-os/scripts/project_os.py`: passed.
- Smoke verified old index header upgrade dry-run/apply plus `add-run-parameter` and `capture-run-env`.
- Expected warning remained for an intentionally missing old result path; no validation errors.

## Session: 2026-06-23 — CLI-backed short trigger router

### Code implementation
- **Status:** complete for non-executing route planning
- Actions taken:
  - Added `project_os.py route` and alias `explain-trigger`.
  - Implemented compact phrase recognition for bootstrap/resume, branch, task, run, result, asset, decision, and release intent groups.
  - Route output now includes current harness state, missing required fields, safety gates, planned deterministic CLI commands, verification commands, notes, and `ready`.
  - Preserved the key safety boundary: the router plans commands only and does not directly mutate project files.
  - Updated `short_trigger_router.md`, `research-project-os/SKILL.md`, `project-skeleton/SKILL.md`, README, and the complete development plan to expose the route planning surface.

### Verification
- `python3 -m py_compile skills/local/research-project-os/scripts/project_os.py`: passed.
- Temporary-project smoke covered `route` before init, after init, branch/task/run/result planning, and promotion dry-run planning.
- The same smoke finished with `validate` returning 0 errors / 0 warnings and `doctor --repair-plan` returning `ok=true`.

## Session: 2026-06-23 — Router split and dashboard export

## Session: 2026-06-24 — Portable externalization slice and pilot inspection

### Code implementation
- **Status:** complete for this batch
- Actions taken:
  - Added portable external-asset commands to `research-project-os`: `list-asset-locations`, `plan-externalize-assets`, `externalize-asset`, and `verify-external-assets`.
  - Extended the harness contract with `.project_os/indexes/asset_locations.tsv` and `.project_os/config.yaml` `external_assets`.
  - Updated router/docs/templates/views/health/export integration so external asset locations are visible through short-trigger routing, `DATA_ASSETS.md`, `doctor`, `validate`, `integrity`, and dashboard exports.
  - Enforced the portability rule in implementation and docs: no hard links, no inode/device dependence, symlink not canonical, canonical recovery via `asset_id + asset_locations.tsv`.
  - Hardened `_assets.py` after smoke testing so CLI-supplied external roots are preserved in `storage_root` metadata and later `refresh-assets` sync does not clobber richer primary-location notes created by `externalize-asset`.

### Verification
- `python3 -m py_compile skills/local/research-project-os/scripts/*.py`: passed before and after the `_assets.py` follow-up fix.
- Temporary-project smoke 1 passed:
  - `new-project --apply`
  - `create-task`
  - `create-run`
  - `add-run-input`
  - `add-context`
  - `plan-externalize-assets --threshold 1M --write-report`
  - `externalize-asset` dry-run and `--apply --approved`
  - `verify-external-assets --checksum`
  - `list-asset-locations`
  - `doctor`
  - `validate`
- Temporary-project smoke 2 confirmed the follow-up metadata fix:
  - `asset_locations.tsv` primary/backup `storage_root` values retained CLI-supplied roots
  - `refresh-assets` preserved the richer primary-location note instead of rewriting it to a generic derived note

### Pilot inspection
- **Status:** non-destructive read-only inspection complete
- Actions taken:
  - Confirmed the real pilot target file exists:
    - `/media/teng/HP_P900/bgcdetecttion/typeiipks/target_all_faa.renamed_for_Chen2022_HMMER.faa` (~9.1G)
  - Confirmed `/home/teng/BGCdetection/target_BGC_mining/typeII_pks` does not yet contain `.project_os/workflow.md`.
  - Ran `new-project` dry-run only on the real project to preview adoption scaffolding without modifying files.
  - Counted FAA reference pressure in the real project:
    - 49 basename hits for `target_all_faa.renamed_for_Chen2022_HMMER.faa`
    - 8 exact hits for the old in-project absolute FAA path
    - 1 broken symlink pointing to the missing in-project FAA copy
- Interpretation:
  - The real project is a good externalization pilot, but it needs harness adoption first.
  - Existing symlink usage confirms that symlink compatibility may still be useful locally, but must remain optional and non-canonical.

### Code implementation
- **Status:** complete for this batch
- Actions taken:
  - Started P1.11 module splitting by extracting the short-trigger router implementation into `skills/local/research-project-os/scripts/_router.py`.
  - Kept `project_os.py route` and `explain-trigger` as the public CLI surface through a thin wrapper.
  - Added `export-dashboard` with dry-run/apply behavior.
  - `export-dashboard --apply` writes generated `.project_os/exports/dashboard.json` and `.project_os/exports/dashboard.html`.
  - `export-dashboard --sqlite --apply` also writes `.project_os/exports/dashboard.sqlite`.
  - Dashboard/export policy remains strict: generated views are derived from canonical indexes, runtime pointers, and event journal; they are not source of truth.

### Verification
- `python3 -m py_compile skills/local/research-project-os/scripts/project_os.py skills/local/research-project-os/scripts/_router.py`: passed.
- Temporary-project smoke is pending in the next validation batch.

## Session: 2026-06-23 — Export split and migration adoption hardening

### Code implementation
- **Status:** complete for this batch
- Actions taken:
  - Continued P1.11 module splitting by extracting dashboard/export generation into `skills/local/research-project-os/scripts/_export.py`.
  - Kept `project_os.py export-dashboard` as the stable public CLI wrapper.
  - Hardened `migrate-branch-first` dry-run output to report task link-table repairs and run-manifest field repairs.
  - Added migration normalization for old `run_links.tsv` / `result_links.tsv` headers, missing run manifest fields, and result `branch_id` / `task_id` / `run_id` backfill.
  - Added migrated path rewriting so flat `runs/<run_id>/...` artifact references become `runs/<branch_id>/<run_id>/...` in `results.tsv`, task link tables, and run manifests.
  - Updated project adoption documentation, README, canonical plan, PROJECT_STATE, and findings.

### Verification
- `python3 -m py_compile skills/local/research-project-os/scripts/project_os.py skills/local/research-project-os/scripts/_router.py skills/local/research-project-os/scripts/_export.py`: passed.
- Core smoke passed through new-project -> branch -> task -> run -> parameter/env -> result -> accept -> promote -> close-run -> export-dashboard SQLite -> validate -> doctor; validate returned 0 errors / 0 warnings and doctor `ok=true`.
- Migration smoke passed for legacy flat `.project_os/tasks/<task_id>/`, `runs/<run_id>/`, old task link headers, sparse run manifest, and old `results.tsv`; migration rewrote result path to `runs/main/<run_id>/...`; validate returned 0 errors / 0 warnings.

## Session: 2026-06-23 — Schema/constants module split

### Code implementation
- **Status:** complete for this split
- Actions taken:
  - Extracted shared schema constants, allowed statuses, index headers, required fields, root defaults, adapter blocks, and project templates from `project_os.py` into `skills/local/research-project-os/scripts/_schema.py`.
  - Kept `project_os.py` as the public CLI facade using a thin import, so command names and behavior remain unchanged.

### Verification
- `python3 -m py_compile skills/local/research-project-os/scripts/project_os.py skills/local/research-project-os/scripts/_router.py skills/local/research-project-os/scripts/_export.py skills/local/research-project-os/scripts/_schema.py`: passed.
- Core smoke after the split passed through new-project -> branch -> task -> run -> result -> accept -> promote -> export-dashboard SQLite -> route -> validate -> doctor; validate returned 0 errors / 0 warnings.
- Migration smoke after the split passed for legacy flat task/run/result adoption with path rewrite; validate returned 0 errors / 0 warnings.

## Session: 2026-06-23 — Paths and project IO module split

### Code implementation
- **Status:** complete for this split
- Actions taken:
  - Extracted project-local path helpers into `skills/local/research-project-os/scripts/_paths.py`.
  - Extracted shared JSON/TSV/JSONL IO, event journal helpers, runtime pointer helpers, advisory lock, and common utility functions into `skills/local/research-project-os/scripts/_project_io.py`.
  - Initially attempted `_io.py`, but Python resolved that name to the built-in `_io` module; renamed to `_project_io.py` to avoid import shadowing.
  - Kept all public CLI command names and behavior under `project_os.py`.

### Verification
- `python3 -m py_compile skills/local/research-project-os/scripts/project_os.py skills/local/research-project-os/scripts/_schema.py skills/local/research-project-os/scripts/_paths.py skills/local/research-project-os/scripts/_project_io.py skills/local/research-project-os/scripts/_router.py skills/local/research-project-os/scripts/_export.py`: passed.
- Core smoke passed through new-project -> branch -> task -> run -> asset -> run provenance -> result -> accept -> promote -> release -> validate-release --record -> close-run -> export-dashboard SQLite -> route -> validate -> doctor; validate returned 0 errors / 0 warnings and doctor `ok=true`.
- Migration smoke passed for legacy flat task/run/result adoption with dry-run repair reporting and path rewrite; validate returned 0 errors / 0 warnings.

## Session: 2026-06-23 — Integrity and derived views split

### Code implementation
- **Status:** complete for this split
- Actions taken:
  - Extracted validate/doctor helper functions, dependency/replacement DAG checks, derived-view drift checks, event reference checks, and repair-plan construction into `skills/local/research-project-os/scripts/_integrity.py`.
  - Extracted `RESULTS_INDEX.md` and `DATA_ASSETS.md` generated-text helpers into `skills/local/research-project-os/scripts/_views.py`.
  - Kept `project_os.py validate`, `doctor`, and `refresh-indexes` as stable public CLI commands.
  - Fixed the first split boundary by moving derived-view generation out of the main file so `_integrity.py` no longer depends on main-file functions.

### Verification
- `python3 -m py_compile skills/local/research-project-os/scripts/project_os.py skills/local/research-project-os/scripts/_schema.py skills/local/research-project-os/scripts/_paths.py skills/local/research-project-os/scripts/_project_io.py skills/local/research-project-os/scripts/_views.py skills/local/research-project-os/scripts/_integrity.py skills/local/research-project-os/scripts/_router.py skills/local/research-project-os/scripts/_export.py`: passed.
- Core smoke passed through new-project -> branch -> task -> run -> asset -> run provenance -> result -> accept -> promote -> release -> validate-release --record -> close-run -> export-dashboard SQLite -> validate -> doctor; validate returned 0 errors / 0 warnings and doctor `ok=true`.
- Migration smoke passed for legacy flat task/run/result adoption with path rewrite; validate returned 0 errors / 0 warnings.

## Session: 2026-06-23 — Hooks contract reservation

### Code/documentation implementation
- **Status:** complete for this batch
- Actions taken:
  - Added `skills/local/research-project-os/references/hooks_contract.md` to define the deferred hook boundary.
  - Added template `.project_os/spec/hooks.md` and expanded template `.project_os/config.yaml` with a default-disabled `hooks:` block.
  - Updated `_schema.py` so new `new-project` / `init` scaffolds include the same hooks contract files/config.
  - Updated `workflow.md`, `event_journal.md`, `harness_contract.md`, `lifecycle_events.md`, `SKILL.md`, README, and the canonical development plan to state that hooks may observe `events.jsonl` and call the CLI, but must not write canonical state directly.
  - Kept active hook dispatching explicitly out of scope for P0/P1.

### Verification
- `python3 -m py_compile` for `project_os.py`, `_schema.py`, `_paths.py`, `_project_io.py`, `_views.py`, `_integrity.py`, `_router.py`, and `_export.py`: passed.
- Temporary scaffold smoke confirmed `new-project --apply` creates `.project_os/spec/hooks.md`, expands the default-disabled `hooks:` config block, and still passes `validate` / `doctor`.
- `python3 scripts/validate_skills.py`: passed with 70 skills, 0 errors, and the same 11 existing credential-word warnings.
- `python3 scripts/sync_skills.py --dry-run`: completed; summary `total 679, ok 592, skip 65, update 20, write 2`. These are dry-run mirror/registry actions only and were not applied.

## Session: 2026-06-23 — Result/release command module split

### Code implementation
- **Status:** complete for this split
- Actions taken:
  - Extracted result lifecycle commands from `project_os.py` into `skills/local/research-project-os/scripts/_result_release.py`:
    - `register-result`
    - `accept-result`
    - `promote-result`
    - `supersede-result`
    - `show-current`
    - `list-results`
    - `show-result`
  - Extracted release packaging commands into the same cohesive module:
    - `build-release`
    - `list-releases`
    - `show-release`
    - `validate-release`
  - Kept `project_os.py` as the stable argparse/CLI facade and command dispatch entry.
  - Preserved the canonical-state boundary: results remain in `.project_os/indexes/results.tsv` plus run manifests/current outputs; releases remain under `release/<release_id>/` plus `.project_os/indexes/releases.tsv`; no new state store was introduced.

### Verification
- `python3 -m py_compile` for `project_os.py`, `_result_release.py`, `_schema.py`, `_paths.py`, `_project_io.py`, `_views.py`, `_integrity.py`, `_router.py`, and `_export.py`: passed.
- Result/release smoke passed through new-project -> branch -> task -> run -> register-result -> accept-result -> dry-run promote -> apply promote -> show-current -> build-release -> show-result -> show-release -> validate-release --record -> validate -> doctor.
- Smoke result: release valid, validate 0 errors / 0 warnings, doctor `ok=true`.

## Session: 2026-06-23 — Task/run command module split

### Code implementation
- **Status:** complete for this split
- Actions taken:
  - Extracted task lifecycle and run provenance commands from `project_os.py` into `skills/local/research-project-os/scripts/_task_run.py`.
  - `_task_run.py` now owns task path resolution, branch-local task creation, task update/stage/close/dependency/context helpers, run creation/current/list/show/update/close, run provenance appenders, parameter capture, environment capture, and task/run index refresh.
  - Kept `project_os.py` as the stable argparse/CLI facade; public command names and arguments remain unchanged.
  - Updated `_result_release.py` to import `task_dir` and `find_run_manifest` from `_task_run.py`, removing duplicated result/run path resolution rules.
  - Left the remaining duplicated asset helper boundary visible for the next split; the next clean target is `_assets.py` so `add-run-input` and asset commands share one helper implementation.

### Verification
- `python3 -m py_compile` for `project_os.py`, `_task_run.py`, `_result_release.py`, `_schema.py`, `_paths.py`, `_project_io.py`, `_views.py`, `_integrity.py`, `_router.py`, and `_export.py`: passed.
- Full task/run/result/release smoke passed through new-project -> branch -> task -> update/stage/dependency/context -> asset -> run -> run input/command/output/metric/parameter/env -> update-run -> close-run -> register-result -> accept-result -> dry-run promote -> apply promote -> build-release -> validate-release --record -> refresh-indexes -> validate -> doctor -> route -> export-dashboard SQLite.
- Smoke result: `validate` returned 0 errors / 0 warnings, `doctor` returned `ok=true`, release validation returned `valid=true`.

## Session: 2026-06-23 — Asset command/helper module split

### Code implementation
- **Status:** complete for this split
- Actions taken:
  - Added `skills/local/research-project-os/scripts/_assets.py` for asset registry commands and shared asset helpers.
  - Moved asset helpers and commands out of `project_os.py`: `register-asset`, `list-assets`, `show-asset`, `update-asset`, `checksum-asset`, and `refresh-assets` now live in `_assets.py`.
  - Updated `_task_run.py` to reuse `_assets.py` helpers for asset lookup, URL detection, usage row creation, and asset usage upsert.
  - Preserved `project_os.py` as the public CLI facade; all asset command names and arguments remain unchanged.
  - Avoided a module-level cycle by making `_assets.py` perform a local import of `_task_run.add_run_input` only inside `command_register_asset` when `--run-id` is used.

### Verification
- `python3 -m py_compile` for `project_os.py`, `_assets.py`, `_task_run.py`, `_result_release.py`, `_schema.py`, `_paths.py`, `_project_io.py`, `_views.py`, `_integrity.py`, `_router.py`, and `_export.py`: passed.
- Asset split smoke passed through new-project -> branch -> task -> run -> register-asset with `--run-id` -> show/checksum/update/refresh asset -> run input/output using asset -> result -> accept -> promote -> release -> validate-release --record -> refresh-indexes -> validate -> doctor -> route -> export-dashboard SQLite.
- Smoke result: release valid, `validate` returned 0 errors / 0 warnings, `doctor` returned `ok=true`, and short-trigger route for `登记数据` resolved to `register_asset`.

## Session: 2026-06-23 — Decision/handoff command module split

### Code implementation
- **Status:** complete for this split
- Actions taken:
  - Added `skills/local/research-project-os/scripts/_decision_handoff.py` for decision journal, handoff update, and state summary commands.
  - Moved `record-decision`, `list-decisions`, `update-handoff`, and `summarize-state` out of `project_os.py`.
  - Kept `project_os.py` as the stable argparse/CLI facade; public command names and arguments remain unchanged.
  - Implemented a local branch-index refresh helper inside `_decision_handoff.py` for `summarize-state`, avoiding a dependency back into the CLI facade.
  - Updated `docs/RESEARCH_PROJECT_OS_COMPLETE_DEVELOPMENT_PLAN.md`, `PROJECT_STATE.md`, `task_plan.md`, and `findings.md` to record the completed split.

### Verification
- `python3 -m py_compile` for `project_os.py`, `_decision_handoff.py`, `_assets.py`, `_task_run.py`, `_result_release.py`, `_schema.py`, `_paths.py`, `_project_io.py`, `_views.py`, `_integrity.py`, `_router.py`, and `_export.py`: passed.
- Decision/handoff smoke passed through new-project -> branch -> task -> run -> asset -> record project/branch/task decisions -> list decisions -> update project/branch/task handoff -> summarize-state -> route decision/handoff triggers -> result -> accept -> promote -> release -> validate-release --record -> refresh-indexes -> validate -> doctor.
- Smoke result: 3 decisions recorded, task-scope decision filtering returned 1 row, route `记录决策` resolved to `record_decision`, route `更新交接` resolved to `update_handoff`, release validation returned `valid=true`, `validate` returned 0 errors / 0 warnings, and `doctor` returned `ok=true`.
- Final repository checks after the split:
  - `python3 scripts/validate_skills.py`: 70 skills, 0 errors, 11 existing mirrored/global credential-word warnings.
  - `python3 scripts/sync_skills.py --dry-run`: summary `total 679, ok 592, skip 65, update 20, write 2`; dry-run only, no mirror/registry writes applied.

## Session: 2026-06-23 — Project/bootstrap/branch command module split

### Code implementation
- **Status:** complete for this split
- Actions taken:
  - Added `skills/local/research-project-os/scripts/_project_branch.py` for project bootstrap, adapter installation, status/start, refresh-indexes, and branch commands.
  - Moved `init`, `new-project`, `install-adapters` / `build-adapters`, `status`, `start`, `refresh-indexes`, `create-branch`, `set-current-branch`, `list-branches`, `show-branch`, and `archive-branch` implementation out of `project_os.py`.
  - Kept `project_os.py` as the stable public CLI facade and argparse dispatch entry.
  - Reduced `project_os.py` to remaining facade/wrapper logic plus migration, validate, and doctor command bodies.
  - Updated `docs/RESEARCH_PROJECT_OS_COMPLETE_DEVELOPMENT_PLAN.md`, `PROJECT_STATE.md`, `task_plan.md`, and `findings.md` to record the split.

### Verification
- `python3 -m py_compile` for `project_os.py`, `_project_branch.py`, `_decision_handoff.py`, `_assets.py`, `_task_run.py`, `_result_release.py`, `_schema.py`, `_paths.py`, `_project_io.py`, `_views.py`, `_integrity.py`, `_router.py`, and `_export.py`: passed.
- Bootstrap/branch/adapter smoke passed through new-project -> status -> start -> list-branches -> create-branch -> show-branch -> set-current-branch -> install-adapters -> refresh-indexes -> validate -> doctor.
- Route/export smoke after the split passed through new-project -> route `开工` -> route `新建分支` -> task -> run -> result -> export-dashboard SQLite -> validate -> doctor.
- Migration smoke after the split passed for legacy flat task/run/result adoption with old headers and path rewrite; validate returned 0 errors / 0 warnings and doctor `ok=true`.

## Session: 2026-06-23 — Migration command module split and conflict diagnostics

### Code implementation
- **Status:** complete for this split and diagnostics batch
- Actions taken:
  - Added `skills/local/research-project-os/scripts/_migration.py` for flat-layout adoption and migration logic.
  - Moved `migrate-branch-first` and migration helper functions out of `project_os.py`.
  - Kept `project_os.py` as the stable public CLI facade; `migrate-branch-first` keeps the same public command name and arguments.
  - Enhanced dry-run migration diagnostics with a structured `diagnostics` payload containing summary counts, conflicts, warnings, and `safe_to_apply`.
  - Added pre-apply conflict detection for existing branch-first targets, task/run ID conflicts, duplicate mapping situations, malformed run manifests, missing result paths, missing asset paths, unmapped flat result paths, and asset paths that cannot be safely rewritten.
  - Updated migration/adoption documentation so users can inspect dry-run diagnostics before choosing copy/move/replace or manual repair.

### Verification
- Normal migration smoke passed with dry-run actions, `safe_to_apply=true`, apply, validate 0 errors / 0 warnings, and doctor `ok=true`.
- Conflict migration smoke correctly reported blocking conflicts including target/task/run conflicts and missing result/asset paths; `safe_to_apply=false`.
- Final checks after state-doc update passed:
  - `python3 -m py_compile` for `project_os.py` and all split modules.
  - `python3 scripts/validate_skills.py`: 70 skills, 0 errors, 11 existing mirrored/global credential-word warnings.
  - `python3 scripts/sync_skills.py --dry-run`: summary `total 679, ok 592, skip 65, update 20, write 2`; dry-run only, no mirror/registry writes applied.

## Session: 2026-06-23 — Validate/doctor health command module split

### Code implementation
- **Status:** complete for this split
- Actions taken:
  - Added `skills/local/research-project-os/scripts/_health.py` for `validate` and `doctor` command bodies.
  - Kept `_integrity.py` as the reusable helper layer for header checks, context manifest checks, graph/integrity checks, derived-view drift checks, event reference checks, and repair-plan construction.
  - Updated `project_os.py` to import `command_validate` and `command_doctor` from `_health.py` while preserving the public commands `project_os.py validate` and `project_os.py doctor`.
  - Kept argparse and CLI dispatch centralized in `project_os.py`.

### Verification
- `python3 -m py_compile` for `project_os.py`, `_health.py`, and all split modules: passed.
- Temporary health smoke passed through new-project -> branch -> task -> run -> result -> validate -> doctor -> doctor --repair-plan.
- Smoke result: validate returned 0 errors / 0 warnings, doctor returned `ok=true`, and repair plan returned 0 suggested fixes.
- `python3 scripts/validate_skills.py`: 70 skills, 0 errors, 11 existing mirrored/global credential-word warnings.
- `python3 scripts/sync_skills.py --dry-run`: summary `total 679, ok 592, skip 65, update 20, write 2`; dry-run only, no mirror/registry writes applied.

## Session: 2026-06-23 — Current/result derived view enhancement

### Code/documentation implementation
- **Status:** complete for this increment
- Actions taken:
  - Added current-result derived view helpers to `skills/local/research-project-os/scripts/_views.py`.
  - Enhanced `show-current` with `--scope all|project|branch` and `--audit` while preserving old `--branch-id` and `--project-only` behavior.
  - Added promotion audit output for missing current targets, duplicate current targets, cross-branch promotions, and legacy unscoped `status=current` rows.
  - Updated generated `RESULTS_INDEX.md` to include a `Current views` section with project-level and branch-level current results.
  - Updated result schema reference and template result-curation spec to document the new derived view behavior.

### Verification
- Current/result smoke passed through new-project -> branch -> task -> run -> two results -> accept -> promote to branch current and project current -> `show-current --scope all|branch|project --audit` -> validate -> doctor.
- Smoke result: all current count 2, project current count 1, branch `method_a` current count 1, promotion audit `ok=true`, validate 0 errors / 0 warnings, doctor `ok=true`.
- `python3 -m py_compile` for the CLI/modules: passed.
- `python3 scripts/validate_skills.py`: 70 skills, 0 errors, 11 existing mirrored/global credential-word warnings.
- `python3 scripts/sync_skills.py --dry-run`: summary `total 679, ok 592, skip 65, update 20, write 2`; dry-run only, no mirror/registry writes applied.

## Session: 2026-06-23 — Promotion audit health-check integration

### Code implementation
- **Status:** complete for this hardening increment
- Actions taken:
  - Reused `_views.promotion_audit()` inside `_integrity.add_integrity_checks()`.
  - Added validate/doctor warnings for missing current targets, duplicate current targets, and unscoped `status=current` rows.
  - Added repair-plan routing so current-target drift points users to `show-current --scope all --audit`.

### Verification
- Negative smoke for a deleted promoted current file passed: `show-current --audit` reported `ok=false`, `validate` reported a missing current target warning, and `doctor --repair-plan` suggested `show-current --scope all --audit`.
- Negative smoke for a duplicate promoted target passed: `validate` reported duplicate current target warnings.
- Final checks passed:
  - `python3 -m py_compile` for the CLI/modules.
  - `python3 scripts/validate_skills.py`: 70 skills, 0 errors, 11 existing mirrored/global credential-word warnings.
  - `python3 scripts/sync_skills.py --dry-run`: summary `total 679, ok 592, skip 65, update 20, write 2`; dry-run only, no mirror/registry writes applied.

## Session: 2026-06-23 — Dashboard graph export enhancement

### Code/documentation implementation
- **Status:** complete for generated graph inspection
- Actions taken:
  - Enhanced `skills/local/research-project-os/scripts/_export.py` with `build_graph()`.
  - `dashboard_payload()` now includes a derived `graph` object with `nodes`, `edges`, counts by node kind, counts by edge relation, and a policy note.
  - Dashboard HTML now renders graph summary, graph node table, and graph edge table.
  - Dashboard SQLite export now writes generated `graph_nodes` and `graph_edges` tables.
  - Graph nodes currently cover project, branch, task, run, result, current target, asset, and release entities.
  - Graph edges currently cover branch ownership, task/run/result provenance, result promotion, asset usage/result links, replacement, and release inclusion.
  - Guarded against blank IDs creating meaningless graph nodes; asset nodes expose their asset kind as `type`.

### Verification
- `python3 -m py_compile skills/local/research-project-os/scripts/*.py`: passed.
- Dashboard graph smoke passed through new-project -> branch -> task -> run -> asset usage -> result -> accept -> promote -> release -> `export-dashboard --apply --sqlite`.
- Smoke verified required graph nodes for project/branch/task/run/result/current-target/asset/release, required provenance edges, asset `type=data`, and SQLite `graph_nodes` / `graph_edges` row counts.
- Smoke result: `validate` returned 0 errors / 0 warnings; generated graph had 10 nodes and 13 edges in the test project.
- Next implementation frontier remains real-project migration/adoption dogfooding; richer dashboard UI remains deferred because the generated JSON/HTML/SQLite graph view is now available for inspection.

## Session: 2026-06-23 — Journal/current snapshot audit

### Code/documentation implementation
- **Status:** complete for P1 consistency audit
- Actions taken:
  - Enhanced `skills/local/research-project-os/scripts/_integrity.py` with journal/current snapshot coverage checks.
  - `validate` / `doctor` now warn when lifecycle events reference missing branch/task/run/result/asset/release objects.
  - `validate` / `doctor` now warn when non-legacy branch/task/run/result/asset/release snapshot rows lack event coverage in `events.jsonl`.
  - Added `project.adopted` tolerance so migrated/adopted rows created before adoption do not cause noisy missing-creation-event warnings.
  - Updated `doctor --repair-plan` guidance for journal coverage gaps to point to `summarize-state` and manual provenance review instead of auto-editing events.
  - Updated integrity reference/template and the complete development plan to record that P1 journal/snapshot audit is implemented while full WAL replay remains deferred.

### Verification
- `python3 -m py_compile skills/local/research-project-os/scripts/*.py`: passed.
- Clean journal smoke passed through new-project -> branch -> task -> run -> asset -> result -> accept -> release -> validate/doctor with 0 errors / 0 warnings.
- Negative smoke manually inserted a future-dated task row without a lifecycle event; `validate` reported `journal snapshot missing event coverage: task manual_task`, and `doctor --repair-plan` suggested `summarize-state` / review.
- Legacy adoption smoke passed for a flat task/run/result project migrated with `migrate-branch-first --apply`; `validate` returned 0 errors / 0 warnings, confirming `project.adopted` tolerance avoids false event-coverage warnings for adopted historical rows.
- Final repository checks passed: `git diff --check`; `python3 scripts/validate_skills.py` returned 70 skills / 0 errors / 11 existing warnings; `python3 scripts/sync_skills.py --dry-run` returned total 679 / ok 592 / skip 65 / update 20 / write 2.

## Session: 2026-06-24 — Run lifecycle package capture and detailed summary

### Code/documentation implementation
- **Status:** complete for P1 run lifecycle provenance enhancement
- Actions taken:
  - Added `capture-run-env --freeze-file`, defaulting to `docs/pip-freeze.txt` relative to the run directory.
  - `capture-run-env --pip-freeze` now writes the raw freeze output to the run-local freeze file and records `environment.package_capture` metadata in `RUN_MANIFEST.json`.
  - `package_capture` records method, parsed package count, raw line count, unparsed count/examples, freeze file path, and captured timestamp.
  - Replaced the short close-run summary with a detailed `RUN_SUMMARY.md` covering identity, counts, parameters, inputs, commands, outputs, metrics, promoted targets, environment, package sample, and notes.
  - Updated the complete development plan, run manifest schema reference, project template run provenance spec, and `research-project-os/SKILL.md` command example.

### Verification
- `python3 -m py_compile skills/local/research-project-os/scripts/*.py`: passed.
- Temporary run lifecycle smoke passed through new-project -> branch -> task -> run -> add parameter -> add command -> add output -> add metric -> `capture-run-env --pip-freeze --freeze-file docs/pip-freeze.txt` -> close-run.
- Smoke verified `runs/<branch_id>/<run_id>/docs/pip-freeze.txt`, `RUN_MANIFEST.json.environment.package_capture.freeze_file`, and detailed `RUN_SUMMARY.md` sections.
- Smoke result: validate returned 0 errors / 0 warnings and doctor returned `ok=true`.

## Session: 2026-06-24 — Real legacy harness adoption dogfood

### Code/documentation implementation
- **Status:** complete for this migration/adoption hardening increment
- Actions taken:
  - Ran non-destructive dogfood on `/home/teng/pingtai_final_20260430`, an older flat `.project_os` harness.
  - Found that `migrate-branch-first` failed before planning when the old harness lacked a branch-first target branch (`Missing target branch: main`).
  - Enhanced `_migration.py` so `migrate-branch-first` plans and applies missing scaffold repairs for older harnesses: `.project_os/project.json`, `.project_os/journals/events.jsonl`, `.project_os/branches/<branch_id>/`, branch current/run directories, missing index files, and full branch-aware index headers.
  - Dry-run diagnostics now include `scaffold_repairs` and `branch_repairs` summary counts.
  - Fixed journal snapshot time comparison for legacy timezone-naive timestamps by normalizing parsed times to a timezone-aware value.
  - Updated `project_adoption.md` and the complete development plan to document scaffold adoption behavior.

### Verification
- Real project dry-run on `/home/teng/pingtai_final_20260430` now succeeds with `safe_to_apply=true`, reporting scaffold/branch/index/task/run repair actions instead of failing on a missing branch.
- Real project copy migration smoke passed by copying `/home/teng/pingtai_final_20260430` to `/tmp`, running `migrate-branch-first --apply --mode copy`, then `validate`, `doctor`, and `start`.
- Smoke result on the copied real project: apply actions 15, validate 0 errors / 0 warnings, doctor `ok=true`, and `start` resolved branch `main` plus task `20260619_nmr_gcf_poc`.
- Synthetic old flat harness smoke also passed for a minimal legacy project missing project/journal/branch scaffolding: dry-run showed scaffold and branch repairs, apply succeeded, validate 0 errors / 0 warnings, doctor `ok=true`, and start resolved the migrated task.

## Session: 2026-06-24 — Partial migration scaffold dogfood

### Code/documentation implementation
- **Status:** complete for this adoption hardening increment
- Actions taken:
  - Searched local project folders for additional `.project_os` real-project samples; only `/home/teng/pingtai_final_20260430` was found beyond the current skill hub.
  - Built a partial-migrated synthetic legacy harness with an existing `.project_os/branches/main/branch.json`, flat `.project_os/tasks/<task_id>/`, flat `runs/<run_id>/`, old index headers, and an artifact path outside the run directory.
  - Found that migration apply could succeed but strict `validate` still failed when `.project_os/spec/` and root entry files such as `PROJECT_STATE.md` / `DECISIONS.md` were missing.
  - Enhanced `_migration.py` so `migrate-branch-first` scaffold adoption now plans/applies missing spec templates, root human entry files, runtime pointer files, `current/project/`, `release/`, branch helper directories/files, and incomplete branch manifests.
  - Updated `project_adoption.md`, README, the complete development plan, and project state docs to document full scaffold adoption behavior.

### Verification
- Partial-migrated synthetic dogfood passed: dry-run reported full scaffold/index/task/run repairs; `migrate-branch-first --apply --mode copy` succeeded; `validate` returned 0 errors / 0 warnings; `doctor` returned `ok=true`; and `start` resolved branch `main`, task `t_old`, and run `r_old`.
- Re-ran real-project dry-run on `/home/teng/pingtai_final_20260430`; it now reports 28 actions with 18 scaffold repairs, 1 branch repair, 1 task, 1 run, and 7 index repairs, still with `safe_to_apply=true`.
- Re-ran copied real-project migration on `/tmp`: apply actions 28; `validate` returned 0 errors / 0 warnings; `doctor` returned `ok=true`; and `start` resolved branch `main` plus task `20260619_nmr_gcf_poc`.

## Session: 2026-06-24 — Hand-edited manifest migration diagnostics

### Code/documentation implementation
- **Status:** complete for this migration diagnostics increment
- Actions taken:
  - Enhanced `migrate-branch-first` dry-run diagnostics for hand-edited legacy task/run manifests.
  - Task actions now expose `manifest_task_id`, `manifest_branch_id`, and malformed task manifest repairs.
  - Run actions now expose `manifest_run_id`, `manifest_branch_id`, and `manifest_task_id`.
  - Dry-run conflicts now block unsafe apply for malformed task/run/branch manifests, task/run ID mismatches between directory names and manifest contents, task/run branch mismatches with the target branch, and duplicate result IDs.
  - Dry-run warnings now report run manifests whose `task_id` cannot be found, result rows whose run/task provenance cannot be inferred, and missing result paths.
  - Added `infer_run_id_for_result_from_links()` so result rows with artifacts outside `runs/` can still backfill run provenance from task-local `result_links.tsv`.
  - Updated project adoption docs, the complete development plan, and project state records.

### Verification
- Negative hand-edited manifest smoke passed: dry-run returned `safe_to_apply=false` and reported `task_id_mismatch`, `task_branch_mismatch`, `malformed_task_manifest`, `run_id_mismatch`, `run_branch_mismatch`, `malformed_run_manifest`, and `duplicate_result_id` conflicts, plus unresolved provenance warnings.
- Positive external-artifact smoke passed: a result path outside `runs/` with task-local `result_links.tsv` `run_id` produced no unresolved-run warning, `migrate-branch-first --apply --mode copy` succeeded, `validate` returned 0 errors / 0 warnings, and `results.tsv` was backfilled with branch/task/run provenance.

## Session: 2026-06-24 — Legacy run provenance preservation dogfood

### Code/documentation implementation
- **Status:** complete for this migration preservation increment
- Actions taken:
  - Continued real-project dogfood using `/home/teng/pingtai_final_20260430` copied to `/tmp`.
  - Verified repeated migration behavior: after an initial `--mode copy`, a second dry-run reports `target_exists` for task/run targets and `safe_to_apply=false`; with `--replace`, the conflicts become non-blocking only after explicit review/flag.
  - Verified `--mode move` adoption on a copy removes flat sources, leaves a second dry-run with 0 actions, and passes `validate`, `doctor`, and `start`.
  - Built a real-project-derived `analysis_runs/<run_id>/` case to cover an unusual run root with result paths under `analysis_runs/`.
  - Found that old `RUN_MANIFEST.json` provenance shapes such as dict `inputs`, dict `outputs`, and string-list `commands` were being normalized to empty lists, losing historical provenance.
  - Enhanced `_migration.py` so legacy run manifest `inputs`, `commands`, `outputs`, `promoted`, and `key_results` are normalized into current structured fields instead of dropped.
  - Enhanced migration dry-run `manifest_repairs` to report provenance-shape normalization (`normalize_inputs_shape`, `normalize_outputs_shape`, `normalize_commands_entries`, etc.).
  - Updated `project_adoption.md`, the complete development plan, and `findings.md` to document preservation and dry-run visibility.

### Verification
- `python3 -m py_compile skills/local/research-project-os/scripts/*.py`: passed after the migration changes.
- Real copied project move migration passed with preserved provenance: migrated legacy run manifest kept 5 inputs, 4 commands, 7 outputs, and 5 metrics; `validate` returned 0 errors / 0 warnings.
- `analysis_runs/` unusual-root smoke passed: dry-run returned `safe_to_apply=true` with no warnings; apply moved the run to `analysis_runs/main/<run_id>/`, rewrote result/link paths, preserved input/output/command entries, and `validate` returned 0 errors / 0 warnings.

## Session: 2026-06-24 — Cross-branch legacy migration mode

### Code/documentation implementation
- **Status:** complete for explicit cross-branch adoption mode
- Actions taken:
  - Added `--preserve-manifest-branches` to `migrate-branch-first`.
  - Kept default migration conservative: legacy task/run manifest `branch_id` values that disagree with `--branch-id` still produce blocking branch mismatch conflicts.
  - In preserve mode, migration plans scaffold/branch repairs for every valid manifest branch ID and reports `planned_branches` in dry-run output.
  - Task actions and run actions now carry their target `branch_id`; apply uses that branch for target paths, manifest normalization, task link-table normalization, and final branch creation.
  - Backfill and path rewrite now use run-derived branch ownership so result rows can land on the correct branch instead of defaulting to the CLI branch.
  - Added invalid `branch_id` conflict handling to block unsafe path creation.
  - Added `run_task_branch_mismatch` blocking diagnostics when a run manifest's target branch disagrees with the branch of its referenced task, even in preserve mode.
  - Updated `project_adoption.md`, README, the complete development plan, and `findings.md`.

### Verification
- Default cross-branch smoke passed: a flat legacy project containing `main` and `alt` manifest branch IDs returned `safe_to_apply=false` with `task_branch_mismatch` and `run_branch_mismatch`.
- Preserve-mode smoke passed: the same project with `--preserve-manifest-branches` reported `planned_branches=alt,main`, applied successfully, created `.project_os/branches/alt` and `.project_os/branches/main`, moved runs to `runs/alt/r_alt` and `runs/main/r_main`, rewrote result/link/output paths, and passed `validate` with 0 errors / 0 warnings plus `doctor ok=true`.
- Negative preserve-mode smoke passed: a run on branch `main` referencing a task on branch `alt` returned `safe_to_apply=false` with `run_task_branch_mismatch`.

## Session: 2026-06-24 — Short-trigger route approval/provenance hardening

### Code/documentation implementation
- **Status:** complete for this routing hardening increment
- Actions taken:
  - Searched local project areas for additional real `.project_os` samples; only the already-dogfooded `/home/teng/pingtai_final_20260430` was found beyond smoke projects.
  - Refactored `project_os.py` route/explain-trigger argparse setup into a shared `add_route_args()` helper to keep both aliases behaviorally identical.
  - Added route-layer support for `--pip-freeze` and `--freeze-file`, so the `捕获运行环境` short trigger can plan a full `capture-run-env --pip-freeze --freeze-file ...` command.
  - Hardened short-trigger safety gates: promotion and release `route --apply` now require `--approved`; otherwise the route plan stays `ready=false` with an explicit missing approval.
  - Added approval gating for route-planned registration of `accepted/current/release` results.
  - Updated `short_trigger_router.md`, `research-project-os/SKILL.md`, README, the complete development plan, and project state records.

### Verification
- Targeted route smoke passed on a temporary harness project: `捕获运行环境 --pip-freeze --freeze-file` planned the expected command; promotion/release apply plans were blocked without `--approved` and ready with `--approved`; validate returned 0 errors / 0 warnings.

## Session: 2026-06-24 — Documentation/template contract convergence

### Documentation/template implementation
- **Status:** complete for this consistency increment
- Actions taken:
  - Updated `harness_contract.md` to replace the ambiguous “canonical files” table with a state-layer table that separates canonical machine state, runtime pointers, branch/task/run provenance, human handoff views, generated displays, and deferred hooks contract.
  - Updated `project_adoption.md` with an explicit entry-path decision table: fresh adoption uses `init` dry-run; old flat, partial branch-first, mixed, or hand-edited harnesses use `migrate-branch-first` dry-run before apply.
  - Synchronized `_schema.py` built-in `SPEC_TEXTS` with the newer template spec files so newly initialized projects receive current policy text for run package capture, current-result derived views, journal/current snapshot audit, and user-profile canonical boundaries.
  - Updated the complete development plan P1.12 section and recorded the documentation-contract finding.
  - Updated `docs/SKILL_ROUTING_MATRIX.md` and README recommendation flow so long-running project prompts route to the branch-first harness, `route` planning layer, canonical indexes, and derived human views instead of manual root-index edits.

### Verification
- `python3 -m py_compile skills/local/research-project-os/scripts/_schema.py`: passed.
- Temporary new-project smoke verified generated spec text contains the updated run package capture, current-result view, journal/current snapshot audit, and user-profile canonical-boundary policy.
- `python3 -m py_compile skills/local/research-project-os/scripts/*.py`: passed.
- `git diff --check`: passed after trimming trailing blank lines.
- `python3 scripts/validate_skills.py`: 70 skills, 0 errors, 11 existing credential-word warnings.
- `python3 scripts/sync_skills.py --dry-run`: total 679 / ok 592 / skip 65 / update 20 / write 2; not applied.

## Session: 2026-06-24 — Routing doc cleanup and final non-destructive validation

### Documentation implementation
- **Status:** complete for this routing consistency increment
- Actions taken:
  - Updated `docs/BIOINFO_WRITING_REFACTOR_PLAN.md` to remove the residual old routing that treated `planning-with-files` as the default “big project kernel”.
  - The bioinfo/writing refactor plan now separates long-running project workbench needs from temporary planning needs:
    - long-term `.project_os` harness / branch-task-run-result-data provenance / continuation -> `research-project-os` or `project-skeleton`;
    - temporary multi-step work without `.project_os` -> `planning-with-files`.
  - Updated `docs/RESEARCH_PROJECT_OS_COMPLETE_DEVELOPMENT_PLAN.md` P1.12 to record this routing cleanup.
  - Confirmed by grep that the only remaining old-phrase hit is the new explanatory note documenting that the old wording was removed.

### Verification
- `python3 -m py_compile skills/local/research-project-os/scripts/*.py`: passed.
- `git diff --check`: passed.
- `python3 scripts/validate_skills.py`: 70 skills, 0 errors, 11 existing credential-word warnings.
- `python3 scripts/sync_skills.py --dry-run`: total 679 / ok 592 / skip 65 / update 20 / write 2; not applied.

## Session: 2026-06-24 — Sessionized runtime focus slice

### Code/documentation implementation
- **Status:** complete for the P2.2 foundation slice
- Actions taken:
  - Added `skills/local/research-project-os/scripts/_sessions.py`.
  - Added optional session-aware pointer resolution in `_project_io.py`: global pointers remain the default, while a non-empty `.project_os/runtime/current_session` shadows focus with `.project_os/runtime/sessions/<session_id>/current_branch`, `current_task`, and `current_run`.
  - Added public CLI commands: `create-session`, `set-current-session`, `list-sessions`, `show-session`, `set-session-focus`, and `close-session`.
  - Wired session validation into `validate` / `doctor`, session display into `start` / `status`, and session summary into `export-dashboard`.
  - Added short-trigger routes for `新建会话`, `切会话`, `列出会话`, `当前会话`, `更新会话焦点`, and `关闭会话`.
  - Updated runtime/session docs in `research-project-os`, `project-skeleton`, references, templates, README, routing matrix, `PROJECT_STATE.md`, and the complete development plan.

### Verification
- Targeted session smoke passed on a temporary harness project:
  - `new-project --apply`;
  - create `main` and `alt` branch-local tasks;
  - `create-session --session-id s_alt --branch-id alt --task-id t_alt --set-current`;
  - `start` resolved `current_session=s_alt`, `runtime_focus_source=session`, branch/task `alt/t_alt`;
  - session-scoped `create-run` wrote under the `alt/t_alt` context;
  - `set-current-session --clear` returned `start` to global `main/t_main`;
  - `route "新建会话"` and `route "切会话"` produced deterministic plans;
  - `validate` returned 0 errors / 0 warnings and `doctor` returned `ok=true`.
- `python3 -m py_compile skills/local/research-project-os/scripts/*.py`: passed before documentation sync.
- Final non-destructive checks after documentation sync passed:
  - `python3 -m py_compile skills/local/research-project-os/scripts/*.py`
  - `git diff --check`
  - `python3 scripts/validate_skills.py`: 70 skills, 0 errors, 11 existing credential-word warnings.
  - `python3 scripts/sync_skills.py --dry-run`: total 679 / ok 592 / skip 65 / update 20 / write 2; not applied.

## Session: 2026-06-24 — Manual report-only hooks dispatcher foundation

### Code/documentation implementation
- **Status:** complete for the P2.1 manual/report-only foundation slice; active automatic hooks remain disabled.
- Actions taken:
  - Added `skills/local/research-project-os/scripts/_hooks.py` as a hooks command group.
  - Exposed `project_os.py list-hooks` and `project_os.py dispatch-hooks` through the stable CLI facade.
  - `list-hooks` reports the default-disabled hooks policy, implemented handler kinds, and the non-canonical/report-only boundary.
  - `dispatch-hooks` reads `.project_os/journals/events.jsonl` and emits report-only JSON for `session_summary`, `reminder`, `opt_in_maintenance`, and report-only placeholder `guard` kinds.
  - `dispatch-hooks --write-report` writes generated reports under `.project_os/exports/hooks/` and is treated as a write command for advisory locking, but it does not write canonical state.
  - Added short-trigger intents for `hook状态` / `hooks状态` / `列出hooks` and `hook报告` / `hook提醒` / `派发hook`.
  - Hardened the `hook提醒` route so it plans `dispatch-hooks --kind reminder` by default, matching the documented short-trigger behavior.
  - Updated hooks/event-journal docs and templates so manual hook reports are documented as already available, while active automatic hooks remain future opt-in work.
  - Updated the complete development plan, routing matrix, short-trigger router reference, lifecycle event list, and project state records.

### Verification
- Targeted hooks smoke on a temporary harness project passed before the final documentation sync:
  - `new-project --apply`;
  - `list-hooks` reported `active_dispatcher_enabled=false` and `manual_dispatcher_available=true`;
  - `dispatch-hooks --limit 1` generated session/reminder/maintenance reports;
  - `dispatch-hooks --kind reminder --write-report` wrote a generated report under `.project_os/exports/hooks/`;
  - `validate` returned 0 errors / 0 warnings and `doctor` returned `ok=true`.
- Final non-destructive checks after documentation sync and the `hook提醒` route consistency fix passed:
  - targeted `hook提醒` route smoke confirmed `dispatch-hooks --kind reminder` planning;
  - `python3 -m py_compile skills/local/research-project-os/scripts/*.py`;
  - `git diff --check`;
  - `python3 scripts/validate_skills.py`: 70 skills, 0 errors, 11 existing credential-word warnings;
  - `python3 scripts/sync_skills.py --dry-run`: total 679 / ok 592 / skip 65 / update 20 / write 2; not applied.

## Session: 2026-06-24 — Hooks route parameter parity hardening

### Code/documentation implementation
- **Status:** complete for this small consistency increment.
- Actions taken:
  - Added route/explain-trigger argparse support for hooks dispatcher options: `--event-index`, `--event`, `--limit`, `--write-report`, and `--output`.
  - Updated `_router.py` so `hook报告` / `hook提醒` / `派发hook` can plan targeted `dispatch-hooks` commands for a specific journal line, event name, recent-event limit, handler kind, and generated report output.
  - Preserved the boundary that hooks routes only plan manual/report-only dispatcher commands; they do not execute suggested hook commands and do not write canonical state.
  - Updated `short_trigger_router.md`, `research-project-os/SKILL.md`, the complete development plan, and project state records.

### Verification
- Targeted route smoke passed on a temporary harness project:
  - `route "hook报告" --event project.initialized --kind reminder --limit 3 --write-report --output .project_os/exports/hooks_custom` planned the expected dispatcher command and generated-view safety gate.
  - `route "hook报告" --event-index 1` planned exact event-line dispatch.
- Final non-destructive validation passed:
  - `python3 -m py_compile skills/local/research-project-os/scripts/*.py`;
  - `git diff --check`;
  - `python3 scripts/validate_skills.py`: 70 skills, 0 errors, 11 existing credential-word warnings;
  - `python3 scripts/sync_skills.py --dry-run`: total 679 / ok 592 / skip 65 / update 20 / write 2; not applied.

## Session: 2026-06-24 — Session pause/resume lifecycle

### Code/documentation implementation
- **Status:** complete for this P2.2 session lifecycle increment.
- Actions taken:
  - Added `pause-session` and `resume-session` CLI commands.
  - `pause-session` marks a session as `paused` and clears it from `.project_os/runtime/current_session` if it was active.
  - `resume-session` marks a session as `active` again and can switch to it with `--set-current`.
  - `set-current-session` and `set-session-focus` now reject paused sessions until they are resumed.
  - `validate` / `doctor` now report an error if `current_session` points to a non-active session.
  - Added `session.paused` and `session.resumed` lifecycle events and reminder-hook awareness.
  - Added short-trigger routes for `暂停会话` and `恢复会话`.
  - Updated session runtime docs/templates, `_schema.py` built-in template text, README, routing matrix, complete plan, and project state.

### Verification
- Targeted session lifecycle smoke passed on a temporary harness project:
  - create session and set current;
  - pause current session and confirm it clears active focus;
  - confirm direct `set-current-session` on paused session is rejected;
  - resume with `--set-current`;
  - validate returns 0 errors / 0 warnings;
  - route plans for `暂停会话` and `恢复会话` are generated with the expected safety notes.
- Final non-destructive validation passed:
  - `python3 -m py_compile skills/local/research-project-os/scripts/*.py`;
  - `git diff --check`;
  - `python3 scripts/validate_skills.py`: 70 skills, 0 errors, 11 existing credential-word warnings;
  - `python3 scripts/sync_skills.py --dry-run`: total 679 / ok 592 / skip 65 / update 20 / write 2; not applied.

## Session: 2026-06-24 — Dashboard session focus visualization

### Code/documentation implementation
- **Status:** complete for this generated-view dashboard increment.
- Actions taken:
  - Enhanced `export-dashboard` payload with a derived `session_focus` summary: current session, active focus, status counts, active/paused/closed counts, current-session row, and stale-current marker.
  - Extended generated graph output with session nodes and `focus_branch` / `focus_task` / `focus_run` edges.
  - Extended static dashboard HTML with session focus cards, stale-current indicator, session status counts, and the existing sessions table.
  - Extended optional dashboard SQLite export with `session_focus` and `sessions` tables.
  - Preserved the generated-view boundary: dashboard JSON/HTML/SQLite remain derived inspection views and must not be edited as canonical state.
  - Updated harness contract, complete development plan, README, project state, progress, and findings.

### Verification
- Targeted dashboard smoke passed on a temporary harness project:
  - created one active session and one paused session;
  - exported dashboard JSON/HTML/SQLite;
  - verified `session_focus.count == 2`, `active_count == 1`, `paused_count == 1`, and `current_session` matches the active session;
  - verified graph contains session nodes and focus edges;
  - verified HTML contains the Session focus section;
  - verified SQLite contains `session_focus`, `sessions`, `graph_nodes`, and `graph_edges` tables;
  - validate returned 0 errors / 0 warnings.
- Final non-destructive validation for this increment is recorded in the current assistant turn summary.

## Session: 2026-06-24 — Report-only session cleanup planner

### Code/documentation implementation
- **Status:** complete for this small P2.2 session archive/GC planning increment.
- Actions taken:
  - Added `plan-session-cleanup` to `_sessions.py` and exposed it through `project_os.py`.
  - The command defaults to dry-run/report-only behavior and selects closed sessions by default; it also supports `--status`, `--min-age-days`, `--include-current`, and optional `--write-report --output`.
  - Generated reports are written under `.project_os/exports/session_cleanup/` and are inspection views only.
  - No session directory is deleted, moved, archived, or rewritten; canonical branch/task/run/result state is unchanged.
  - Added `会话清理` / `规划会话清理` short-trigger routing to plan `plan-session-cleanup` without executing physical cleanup.
  - Updated session runtime templates, `_schema.py` built-in spec text, harness contract, short-trigger reference, README, routing matrix, complete development plan, project state, progress, and findings.

### Verification
- Targeted session cleanup smoke passed on a temporary harness project:
  - created active, paused, and closed sessions;
  - `plan-session-cleanup` defaulted to the closed-session candidate only;
  - `plan-session-cleanup --status closed --status paused --write-report` wrote a generated JSON report and selected closed + paused candidates;
  - `route "会话清理" --status closed --min-age-days 0 --write-report --output .project_os/exports/session_cleanup` planned the expected report-only command and safety gates;
  - `validate` returned 0 errors / 0 warnings.
- Final non-destructive validation for this increment is recorded in the current assistant turn summary.

## Session: 2026-06-24 — Dashboard/doctor session cleanup advisory view

### Code/documentation implementation
- **Status:** complete for this generated-view/advisory hardening increment.
- Actions taken:
  - Extended `export-dashboard` payload with a derived `session_cleanup` candidate summary built from the existing report-only cleanup planner.
  - Added Session cleanup candidates to dashboard HTML.
  - Added SQLite table `session_cleanup_candidates` for downstream inspection.
  - Added a warning-level `doctor` advisory check for closed session cleanup candidates; `doctor --repair-plan` now suggests `plan-session-cleanup --status closed --write-report`.
  - Preserved the boundary that cleanup candidates are not errors and do not make `doctor` fail; no session directories are deleted, moved, archived, or rewritten.
  - Updated harness contract, complete development plan, README/routing matrix, project state, progress, and findings.

### Verification
- Targeted dashboard/doctor smoke passed on a temporary harness project:
  - created and closed a session;
  - exported dashboard JSON/HTML/SQLite;
  - verified JSON `session_cleanup.candidate_count == 1` and candidate `closed_s`;
  - verified HTML contains `Session cleanup candidates`;
  - verified SQLite contains `session_cleanup_candidates` with `closed_s`;
  - verified `doctor --repair-plan` includes warning-level `session_cleanup_candidates` advisory and `plan-session-cleanup` suggestion.
- Final non-destructive validation for this increment is recorded in the current assistant turn summary.

## Session: 2026-06-24 — Hooks dashboard/doctor advisory hardening

### Code/documentation implementation
- **Status:** complete for this small consistency increment.
- Actions taken:
  - Extended `export-dashboard` with a generated `hooks` status/config view: active dispatcher flag, manual dispatcher availability, config request status, event source presence, event count, malformed event count, latest event, generated hook report count, allowed kinds, and unknown allowed kinds.
  - Added Hooks status and Allowed hook kinds sections to generated dashboard HTML.
  - Added SQLite tables `hooks_status` and `hooks_allowed_kinds` to generated dashboard exports.
  - Added `validate` warnings and `doctor --repair-plan` advisory checks for hooks config that requests active dispatch, unknown hook kinds, or a missing configured event source.
  - Kept active automatic hooks disabled: this increment only exposes inspection/advisory surfaces and does not execute suggested commands or write canonical state.
  - Updated README, routing matrix, `research-project-os/SKILL.md`, `hooks_contract.md`, and the complete development plan.

### Verification
- Targeted hooks dashboard/doctor smoke passed on a temporary harness project:
  - `list-hooks` reported manual dispatcher availability and disabled active dispatcher;
  - `export-dashboard --sqlite --apply` wrote dashboard JSON/HTML/SQLite with `hooks` payload and `hooks_status` / `hooks_allowed_kinds` tables;
  - `doctor --repair-plan` reported clean hook checks on default config;
  - `validate` returned 0 errors / 0 warnings.
- Targeted negative hook-config smoke passed:
  - when `hooks.enabled=true` and an unknown kind were injected, `validate` reported warning-level hooks config issues;
  - `doctor --repair-plan` suggested `list-hooks` without failing health or enabling automation.
- Final non-destructive validation for this increment is recorded in the current assistant turn summary.

## Session: 2026-06-24 — Real migration dogfood and diagnostics hardening

### Code/documentation implementation
- **Status:** complete for this dogfood/hardening increment.
- Actions taken:
  - Found a real legacy/partial harness candidate at `/home/teng/pingtai_final_20260430` and only operated on `/tmp` copies.
  - Dogfooded `migrate-branch-first` dry-run, `--apply --mode copy`, repeated migration target-exists checks, `--replace` dry-run, and fresh-copy `--apply --mode move`.
  - Hardened migration JSON output so `summary`, `conflicts`, `warnings`, and `safe_to_apply` are mirrored directly under both `dry_run_migration` and `migrated_branch_first`, not only nested inside `diagnostics`.
  - Hardened `doctor --repair-plan` adapter suggestions so missing Codex/Claude adapter blocks now suggest `install-adapters --platforms codex|claude --apply` instead of a generic `doctor` command.
  - Updated `project_adoption.md`, README, `research-project-os/SKILL.md`, the complete development plan, findings, task plan, and project state.

### Verification
- Real-project copy dogfood passed:
  - dry-run reported top-level `safe_to_apply=true`, `actions=30`, `scaffold_repairs=20`, `tasks=1`, `runs=1`, `index_repairs=7`, and 0 conflicts/warnings;
  - copy-mode apply returned top-level diagnostics and then `validate` returned 0 errors / 0 warnings;
  - `doctor --repair-plan` returned `ok=true` with warning-level adapter suggestions, now mapped to `install-adapters` commands;
  - `start` resolved `current_branch=main`, `current_task=20260619_nmr_gcf_poc`, and the branch-first task path;
  - repeated migration without `--replace` reported blocking `target_exists` for task/run, while `--replace` dry-run made those conflicts non-blocking;
  - fresh-copy move-mode apply validated cleanly and moved the flat run; only an empty legacy `.project_os/tasks/` container remained, and post-move dry-run showed actions=0.
- Final non-destructive validation passed:
  - `python3 -m py_compile skills/local/research-project-os/scripts/*.py`;
  - `git diff --check`;
  - `python3 scripts/validate_skills.py`: 70 skills, 0 errors, 11 existing warnings;
  - `python3 scripts/sync_skills.py --dry-run`: total 679 / ok 592 / skip 65 / update 20 / write 2; not applied.

## Session: 2026-06-24 — Restore-journal repair-plan and route hardening

### Code/documentation implementation
- **Status:** complete for this small consistency hardening increment.
- Actions taken:
  - Added `restore-journal` to the `project_os.py` public CLI facade, implemented in `_project_branch.py`.
  - `restore-journal` defaults to dry-run; with `--apply --approved` it only creates a missing `.project_os/journals/events.jsonl` and appends a `journal.restored` event.
  - Hardened `doctor --repair-plan` so a missing default event journal suggests approval-gated `restore-journal --apply --approved`, while non-default hooks event-source paths still require config review.
  - Added short-trigger support for `恢复事件日志`; `route --apply` remains non-ready unless paired with `--approved`.
  - Added `journal.restored` to lifecycle docs and manual hook reminder behavior; reminders suggest `validate`, `doctor --repair-plan`, and `summarize-state` without executing them.
  - Updated event journal templates, `SKILL.md`, `short_trigger_router.md`, `hooks_contract.md`, `harness_contract.md`, `integrity_rules.md`, README, routing matrix, and the complete development plan.
  - Preserved the boundary that `restore-journal` does not overwrite existing journals, synthesize historical lifecycle events, or implement crash replay.

### Verification
- Targeted restore-journal smoke passed on a temporary harness project:
  - removed `.project_os/journals/events.jsonl` after `new-project`;
  - `doctor --repair-plan` produced one restore-journal step with approval required;
  - `route "恢复事件日志" --apply` stayed non-ready without `--approved`;
  - `restore-journal --apply --approved` recreated the missing file and appended `journal.restored`;
  - `dispatch-hooks --event journal.restored --kind reminder` suggested non-executed validation/review commands;
  - post-restore `validate` had 0 errors and expected snapshot-coverage warning because historical events were not reconstructed.
- Final non-destructive validation for this increment is recorded in the current assistant turn summary.

## Session: 2026-06-24 — Report-only recovery planner foundation

### Code/documentation implementation
- **Status:** complete for the P2.3 safety-foundation slice.
- Actions taken:
  - Added `_recovery.py` with `build_recovery_plan` and `command_plan_recovery`.
  - Exposed `plan-recovery` via `project_os.py` with `--max-lock-age-seconds`, `--max-tmp-files`, `--write-report`, and `--output`.
  - Kept `plan-recovery` report-only: report writes go under `.project_os/exports/recovery/` and do not mutate canonical state or append lifecycle events.
  - Added short-trigger route support for `恢复计划`, `恢复检查`, `崩溃恢复检查`, `recovery plan`, and `plan recovery`.
  - Added warning-level `doctor --repair-plan` advisory for recovery candidates and a repair-plan suggestion to run `plan-recovery --write-report`.
  - Extended generated dashboard JSON/HTML/SQLite with recovery inspection summary and SQLite `recovery_status` / `recovery_summary` tables.
  - Updated `SKILL.md`, `short_trigger_router.md`, `harness_contract.md`, `integrity_rules.md`, `lifecycle_events.md`, templates, `_schema.py` built-in spec text, README, routing matrix, and the complete development plan.

### Verification
- Targeted recovery smoke created a temporary harness, injected a stale lock, malformed journal line, and tmp file, and confirmed `plan-recovery` reported all candidates without modifying canonical state.
- Route smoke confirmed `route "恢复检查" --write-report` returns a ready `plan-recovery --write-report` plan with explicit no replay/rollback/delete/lock-removal safety notes.
- Dashboard smoke confirmed `dashboard.json` includes `recovery.summary`, HTML includes Recovery inspection, and SQLite includes `recovery_status` / `recovery_summary`.
- Final non-destructive validation for this increment is recorded in the current assistant turn summary.

## Session: 2026-06-24 — Dashboard current-result/promotion-audit generated view

### Code/documentation implementation
- **Status:** complete for this P2.4 generated-view increment.
- Actions taken:
  - Extended `_export.py` dashboard payload with `current_results`, reusing `current_result_views` and `promotion_audit` from `_views.py`.
  - Added HTML sections for current result counts, current result rows, branch current-result counts, and promotion audit warnings.
  - Added SQLite tables `current_results_status`, `current_results`, `current_result_branch_counts`, and `promotion_audit`.
  - Preserved the boundary that dashboard output is generated inspection only; it does not promote results, repair `current/`, rewrite `results.tsv`, or become canonical state.
  - Updated the complete plan, `SKILL.md`, README, routing matrix, harness contract, integrity rules, project state, progress, findings, and task plan.

### Verification
- Targeted dashboard smoke passed on a temporary harness project:
  - created task/run/result;
  - promoted the result to `current/branches/main/result.txt`;
  - exported dashboard JSON/HTML/SQLite;
  - verified JSON `current_results.counts`, branch counts, and `audit_ok`;
  - verified HTML contains `Current results and promotion audit`;
  - verified SQLite contains the new current-result/promotion-audit tables and a branch-scoped current result row.
- Final non-destructive validation for this increment is recorded in the current assistant turn summary.

## Session: 2026-06-24 — Current-result short-trigger route consistency

### Code/documentation implementation
- **Status:** complete for this small router/documentation consistency increment.
- Actions taken:
  - Added the `show_current_results` intent to the short-trigger router for `当前结果` / `查看当前结果` / `currentresults` / `showcurrent`.
  - The route plans `show-current --scope <all|project|branch> --audit`; if `--branch-id` is provided with default `--scope all`, the plan narrows to branch scope.
  - Preserved promotion disambiguation: `设为当前结果` and `替换当前结果` still route to approval-gated `promote-result`, not to the read-only current-result view.
  - Updated `SKILL.md`, `short_trigger_router.md`, README, routing matrix, and the complete development plan so `当前结果` is documented as read-only.
  - Boundary: this route does not promote results, repair `current/`, rewrite `results.tsv`, or mutate canonical state.

### Verification
- Targeted route smoke confirmed:
  - `当前结果` resolves to `show_current_results` and plans `show-current --scope all --audit` on an initialized harness.
  - `查看当前结果 --scope branch --branch-id main --no-audit` plans branch-scoped `show-current` without audit.
  - `设为当前结果` and `替换当前结果` continue to resolve to promotion intents.
- Final non-destructive validation for this increment is recorded in the current assistant turn summary.

## Session: 2026-06-24 — Summarize-state current-result/session focus alignment

### Code/documentation implementation
- **Status:** complete for this small consistency increment.
- Actions taken:
  - Updated `_decision_handoff.py` so `summarize-state` uses `focus_payload(root)` rather than only global runtime pointers.
  - Added a `runtime_focus` block to the JSON payload, making session-aware focus resolution explicit.
  - Added a read-only `current_results` block derived from `_views.current_result_views` and `_views.promotion_audit`.
  - The summary now includes all/project/current-branch current result counts, project and current-branch current rows, `audit_ok`, and promotion-audit warning counts.
  - Preserved the boundary that this is a status/handoff summary only: it does not promote results, repair `current/`, rewrite `results.tsv`, or modify canonical state.
  - Updated the complete development plan, README, routing matrix, `research-project-os/SKILL.md`, project state, progress, findings, and task plan.

### Verification
- Targeted summarize-state smokes passed:
  - current-result smoke verified `current_results.project_count`, branch count, and `audit_ok` after a promoted current result;
  - session-focus smoke verified `runtime_focus` and top-level current branch/task/run follow the active session focus.
- Final non-destructive validation passed:
  - `python3 -m py_compile skills/local/research-project-os/scripts/*.py`;
  - `git diff --check`;
  - `python3 scripts/validate_skills.py`: 70 skills, 0 errors, 11 existing warnings;
  - `python3 scripts/sync_skills.py --dry-run`: total 679 / ok 592 / skip 65 / update 20 / write 2; not applied.

## Session: 2026-06-24 — Status run/result summary hardening

### Code/documentation implementation
- **Status:** complete for this P0.5 consistency increment.
- Actions taken:
  - Enhanced `status` in `_project_branch.py` with a full `runtime_focus` payload so status follows session-aware pointer resolution.
  - Added `runs_summary` with active/open run counts, current run row, current branch/task active counts, and last run summary derived from `.project_os/indexes/runs.tsv`.
  - Added `results_summary` with candidate/accepted/current counts, latest candidate rows, project/current-branch current result rows, `audit_ok`, and promotion-audit warning counts derived from `.project_os/indexes/results.tsv` and `current/` targets.
  - Preserved the read-only boundary: `status` does not refresh indexes, append journal events, promote results, repair `current/`, or rewrite run/result manifests.
  - Updated the complete development plan, README, routing matrix, `research-project-os/SKILL.md`, project state, progress, findings, and task plan.

### Verification
- Targeted status smoke passed on a temporary harness project:
  - created task/run;
  - registered one candidate result and one promoted current result;
  - verified `runtime_focus`, `runs_summary.active_count`, `runs_summary.last_run`, `results_summary.candidate_count`, `results_summary.branch_current_count`, and `audit_ok`.
- Final non-destructive validation for this increment is recorded in the current assistant turn summary.

## Session: 2026-06-24 — Direct promotion/release approval-gate hardening

### Code/documentation implementation
- **Status:** complete for this safety/consistency increment.
- Actions taken:
  - Added `--approved` to direct `promote-result` and `build-release` CLI parsers.
  - Hardened `_result_release.py` so `promote-result --apply` fails unless `--approved` is present; dry-run promotion remains available without approval.
  - Hardened `_result_release.py` so `build-release --apply` fails unless `--approved` is present; dry-run release planning remains available without approval.
  - Updated `_router.py` so promotion/release `route --apply --approved` planned commands include both `--apply` and `--approved`; `route --apply` without approval still remains non-ready.
  - Updated `SKILL.md`, README, routing matrix, short-trigger reference, result/release specs/templates, `_schema.py` built-in specs, the complete development plan, project state, progress, findings, and task plan.

### Verification
- Targeted approval-gate smoke passed on a temporary harness project:
  - promotion dry-run succeeded without approval;
  - `promote-result --apply` without `--approved` failed before mutating canonical state;
  - `promote-result --apply --approved` succeeded;
  - release dry-run succeeded without approval;
  - `build-release --apply` without `--approved` failed;
  - `build-release --apply --approved` succeeded;
  - route smoke confirmed `route --apply --approved` includes `--approved` in planned promotion/release commands.
- Final non-destructive validation for this increment is recorded in the current assistant turn summary.

## Session: 2026-06-24 — Restore-journal direct approval-gate hardening

### Code/documentation implementation
- **Status:** complete for this safety/consistency increment.
- Actions taken:
  - Added `--approved` to the direct `restore-journal` CLI parser.
  - Hardened `_project_branch.py` so `restore-journal --apply` fails unless `--approved` is present; dry-run restore planning remains available without approval.
  - Updated `_router.py` so `恢复事件日志 route --apply --approved` planned commands include both `--apply` and `--approved`; route `--apply` without approval remains non-ready.
  - Updated repair/recovery suggestion surfaces so missing-journal commands from `doctor --repair-plan` and `plan-recovery` include `--apply --approved`.
  - Updated user-facing docs/templates/plan references so journal restoration is consistently documented as dry-run first, then reviewed `--apply --approved`.

### Verification
- Targeted restore-journal approval-gate smoke passed on a temporary harness project:
  - dry-run `restore-journal` succeeded without writing the missing journal;
  - direct `restore-journal --apply` without `--approved` failed and did not create `events.jsonl`;
  - `route "恢复事件日志" --apply` stayed non-ready without approval;
  - `route "恢复事件日志" --apply --approved` planned an executable command containing both flags;
  - `doctor --repair-plan` and `plan-recovery` suggested `restore-journal --apply --approved`;
  - direct `restore-journal --apply --approved` recreated the missing journal and appended `journal.restored`.
- Final non-destructive validation for this increment is recorded in the current assistant turn summary.

## Session: 2026-06-24 — Disposable E2E coverage audit

### Coverage audit
- **Status:** complete for this audit increment.
- Actions taken:
  - Added `docs/RESEARCH_PROJECT_OS_E2E_COVERAGE.md` as the release/dogfood coverage record for the `research-project-os` CLI.
  - Enumerated `project_os.py` subcommands from `sub.add_parser(...)`.
  - Compared them with `r.os("<subcommand>", ...)` calls in `smoke_project_os_e2e.py`.
  - Confirmed the smoke script covers all **80/80** public CLI subcommands.
  - Confirmed negative approval-gate coverage for `register-result`, `accept-result`, `promote-result`, `build-release`, `restore-journal`, `externalize-asset`, and `adopt-external-asset`.

### Boundaries confirmed
- The E2E smoke remains disposable: it creates temporary harness projects and explicit temporary external primary/backup roots.
- It does not use real project paths, default external storage roots, active/background hooks, physical session cleanup, crash replay/rollback, or destructive real-project migration.
- Externalization checks explicitly enforce no hard link and no symlink assumptions; canonical asset recovery remains `asset_id + asset_locations.tsv`.

### Verification
- Coverage audit command reported:
  - CLI subcommands: 80
  - smoke-covered subcommands: 80
  - missing coverage: 0
- Full disposable E2E rerun passed:
  - commands: 119
  - expected approval-gate failures: 7
  - main fixture validate: 0 errors / 0 warnings
  - external asset location roles: backup, mirror, primary
- Repository validation after the documentation/state update passed:
  - `python3 -m py_compile skills/local/research-project-os/scripts/*.py`
  - `python3 scripts/validate_skills.py`: 66 skills, 0 errors, 11 existing warnings
  - `python3 scripts/sync_skills.py --dry-run`: total 683 / ok 612 / skip 51 / update 18 / write 2
  - `git diff --check`
