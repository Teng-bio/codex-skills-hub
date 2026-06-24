# Findings & Decisions

## Requirements

- Reorganize the skill ecosystem based on existing local skills first.
- Keep bioinformatics Agent functions separate from manuscript writing skills.
- Reuse existing `tooluniverse-*`, `pubmed-database`, `literature-method-data-miner`, `scientific-critical-thinking`, and reproduction skills.
- First concrete skill should be `bioinfo-evidence-orchestrator`, not a full duplicated bioinformatics toolkit.

## Research Findings

- `codex-skills-hub` already mirrors global skills and has a local authored-skill area at `skills/local/`.
- Existing local skill `literature-method-data-miner` is a good example of a router-style skill with a compact `SKILL.md` and one reference template.
- Hub scripts support validation and inventory refresh:
  - `scripts/validate_skills.py`
  - `scripts/sync_skills.py --apply`

## Technical Decisions

| Decision | Rationale |
|---|---|
| Keep orchestrator lightweight | The existing `tooluniverse-*` and PubMed skills should do domain work |
| Put detailed evidence-pack schema in a reference file | Progressive disclosure keeps `SKILL.md` concise |
| Do not update `nature-skills` in this phase | User asked to plan and refactor based on local skills first |

## Resources

- `docs/BIOINFO_WRITING_REFACTOR_PLAN.md`
- `docs/SKILL_ROUTING_MATRIX.md`
- `skills/local/literature-method-data-miner/SKILL.md`
- `docs/OPERATING_MODEL.md`

## Implementation Findings: Bio Writing Line

- Writing tasks should be routed by product type, not by source material alone:
  - full manuscript/abstract/introduction/discussion/outline -> `bio-paper-writing`
  - figure/table-grounded Results -> `bio-results-writing`
  - workflow provenance -> `bio-methods-writing`
  - prose repair/translation/overclaim -> `bio-polishing`
  - revision letters -> `bio-reviewer-response`
  - repository and FAIR wording -> `bio-data-code-availability`
  - Chinese paper presentation -> `bio-paper2ppt`
- The safest shared contract remains `EVIDENCE_PACK.md` plus figure/table inventories.
- Specialized writing skills should route back to `bioinfo-evidence-orchestrator` when evidence, accession validation, database facts, or new analyses are missing.
- No new skill duplicates the existing ToolUniverse, PubMed, RNA-seq, enrichment, sequence, protein structure, phylogenetics, visualization, or reproduction skills.

## Auto-routing Finding

- Users should not need to say exact skill names. A broad router skill should capture natural prompts such as “这些结果能不能写文章”, “帮我看看下一步”, “这个流程写成方法”, “审稿人这个怎么回”, and then select the evidence or writing lane.
- Ambiguous mixed requests should default to evidence first, then manuscript writing.

## Harness Roadmap Findings: 2026-06-23

- The comprehensive-project effort is harness-first, not skill-first.
- Current skills are operation entry points: `research-project-os` is the main router and `project-skeleton` is the short Chinese trigger alias.
- The durable product should be the `.project_os/` workflow, runtime pointers, task/run/result indexes, and root human-readable state/index files.
- Next priority should not be immediate plugin packaging. First validate natural triggers in a fresh Codex session and harden the CLI lifecycle with positive and negative smoke tests.
- Plugin packaging, hooks, dashboards, and subskills should be treated as later layers after the harness contract is stable in real projects.

## Full Core Harness Scope Finding: 2026-06-23

- The harness should not be reduced to a minimal state tracker. Required core capabilities include branch/workstream management, task context, run lifecycle control, result lifecycle control, data assets, decisions/handoff, and release packaging.
- Plugin packaging, hooks, dashboards, and subskill splitting are not discarded. They are deferred extension layers and the core design should reserve stable interfaces for them.
- Future hooks should observe stable lifecycle events and call existing CLI commands; hooks should not be required for the core harness to operate.
- Plugin packaging should be treated as a distribution step after the file contract and CLI semantics stabilize.

## Branch-First Architecture Finding: 2026-06-23

- Branch/workstream should not remain a flat logical field only; it should become a first-class physical workspace under `.project_os/branches/<branch_id>/`.
- Formal run provenance should default to `runs/<branch_id>/<run_id>/` so branch ownership is obvious from the filesystem, not only from manifest fields.
- Global indexes remain required even with branch-first directories, because cross-branch search, future dashboards, hooks, plugins, and summary commands need one canonical aggregation layer.
- Branch-first layout should be the default for new projects, while earlier flat layouts can be supported temporarily and migrated later through an explicit dry-run migration path.

## Branch-First Schema Finding: 2026-06-23

- The branch-first layout now has a dedicated schema document: `docs/RESEARCH_PROJECT_OS_BRANCH_FIRST_SCHEMAS.md`.
- Global TSV headers should converge toward explicit branch-aware fields instead of minimal flat rows; in particular, `branches.tsv`, `tasks.tsv`, `runs.tsv`, `results.tsv`, `assets.tsv`, and `releases.tsv` should all have stable headers before CLI expansion.
- Branch-local task paths should move from `.project_os/tasks/<task_id>/` to `.project_os/branches/<branch_id>/tasks/<task_id>/`.
- Formal run manifests should default to `runs/<branch_id>/<run_id>/RUN_MANIFEST.json`.
- Result promotion should distinguish branch-level current slots (`current/branches/<branch_id>/`) from project-level current slots (`current/project/`).
## Complete Harness Development Plan Finding: 2026-06-23

- The canonical planning surface is now `docs/RESEARCH_PROJECT_OS_COMPLETE_DEVELOPMENT_PLAN.md`, which merges the original harness implementation plan, branch-first architecture/schema contracts, full P0/P1/P2 roadmap, adapter policy, hook deferral policy, and design lessons from `addyosmani/agent-skills`.
- P0 is not a minimal skill-only implementation. P0 includes schema/constants freeze, branch-first initialization, branch commands, branch-local tasks, branch-aware run/result lifecycle, index/doctor/validate hardening, Codex/Claude thin adapters, skill routing cleanup, and smoke adoption.
- Plugin packaging remains deferred. Hooks remain deferred until the user is comfortable with their semantics and until core CLI/file contracts are stable.

## Harness Review Adoption Finding: 2026-06-23

- The canonical harness roadmap is `docs/RESEARCH_PROJECT_OS_COMPLETE_DEVELOPMENT_PLAN.md`; older planning docs are retained only as historical or detailed references.
- Adopt global uniqueness for `task_id`, `run_id`, and `result_id` to keep cross-branch indexes and short-trigger lookup simple.
- Treat `.project_os/indexes/*.tsv` as canonical machine registries; root `RUNS_INDEX.tsv`, `RESULTS_INDEX.md`, and `DATA_ASSETS.md` are derived human views.
- Add `.project_os/project.json` as the project identity/schema anchor and `.project_os/journals/events.jsonl` as the append-only lifecycle event stream.
- Runtime recovery should automatically load branch `branch.json`, `objective.md`, and `context.md` before active task context.
- P0 should include only minimal smoke/validation, while deeper integrity rules, asset impact tracking, structured repair plans, migration implementation, consistency hardening, and code splitting belong to P1.
- Active hooks dispatcher, full WAL/replay, rich dashboard/export UI, plugin packaging, and broader adapters remain deferred extension layers, not removed scope. Sessionized runtime pointers were originally deferred, but the basic runtime focus slice was later implemented on 2026-06-24.

## P0 Implementation Finding: 2026-06-23

- The first branch-first CLI vertical slice is now implemented in `skills/local/research-project-os/scripts/project_os.py`.
- New harness initialization creates `.project_os/project.json`, `.project_os/journals/events.jsonl`, `.project_os/branches/main/`, `runs/main/`, `current/branches/main/`, and canonical indexes.
- Branch, task, run, and result operations now preserve branch provenance through paths, manifests, and TSV rows.
- Codex and Claude adapters are both supported as thin generated files; neither is canonical state.
- A temporary-project smoke test proved the P0 core loop through promotion and validation, but the full project is not complete yet: asset commands, decisions/handoff commands, release packaging, migration, integrity rules, structured repair plans, full consistency hardening, hooks dispatcher, dashboard, plugin packaging, and broader adapters remain future work.

## Asset/Decision/Release Implementation Finding: 2026-06-23

- Asset registry is now part of the usable core: `.project_os/indexes/assets.tsv` remains canonical, `DATA_ASSETS.md` is generated, and `asset_usage.tsv` is refreshed from run manifest asset references.
- Run provenance now has append-only CLI helpers for inputs, commands, outputs, and metrics, reducing direct JSON hand edits.
- Decisions are stored in root/scope Markdown plus `.project_os/journals/decisions.jsonl`; lifecycle events still go to `events.jsonl` for future hooks/dashboards.
- Release packaging now works as a guarded dry-run/apply command that copies explicit accepted/current results to `release/<release_id>/` with `README.md`, `MANIFEST.tsv`, and `CHECKSUMS.tsv`.
- Initial lifecycle hardening now includes accepted/superseded/current result helpers, task context/stage helpers, run status updates, and a guarded flat -> branch-first migration command.
- The next highest-value gap is integrity/repair-plan hardening and migration edge cases, not hooks or plugin packaging.

## Integrity Hardening Finding: 2026-06-23

- `doctor --repair-plan` now provides a safe non-executing bridge between detection and repair; destructive/provenance-changing repairs remain gated by explicit approval.
- Derived human views are intentionally checked for drift against canonical machine indexes, reinforcing the rule that root docs are views, not source-of-truth registries.
- Task `depends_on` and result `replaced_by` now behave as DAG-like structures with validation support, which enables future impact analysis without implementing hooks yet.
- Advisory locking has been added at the CLI level for state-changing commands; full WAL/replay is still deferred.
- Run closure now generates `RUN_SUMMARY.md`, improving human handoff while preserving `RUN_MANIFEST.json` as provenance source.

## Migration and Run Provenance Finding: 2026-06-23

- Migration should not only move flat task/run directories; it must also normalize old canonical TSV headers because earlier prototypes may have persisted flat `tasks.tsv`, `runs.tsv`, or `results.tsv`.
- Patching legacy result rows with `branch_id`, `promoted_to`, and `replaced_by` is safe when defaulting to the selected migration branch, but missing historical artifact paths should remain warnings rather than destructive fixes.
- Run parameters and environment capture are core provenance, not dashboard concerns; they now live in `RUN_MANIFEST.json` via CLI commands.

## Short Trigger Router Implementation Finding: 2026-06-23

- Short trigger routing should be a deterministic planning layer, not only prose in `SKILL.md`.
- `project_os.py route` / `explain-trigger` now turns compact phrases into auditable intent plans with state, missing fields, safety gates, planned commands, and verification commands.
- Keeping the router non-executing avoids accidental promotion/release/archive actions while still making phrases such as `开工`, `新建分支`, `开始运行`, `记录结果`, and `设为当前结果` operationally concrete.
- Future slash commands or platform-specific command palettes should call the same route/intent layer rather than inventing separate behavior.

## Module Split and Export Finding: 2026-06-23

- `project_os.py` exceeded the P1.11 split threshold, so stable subsystems should be extracted incrementally rather than by one large risky rewrite.
- The short-trigger router is a good first split target because it is non-executing and has a clear dependency boundary; it now lives in `scripts/_router.py`.
- Dashboard/export should remain a generated view over canonical TSV/JSON/journal state. JSON/HTML/SQLite exports are useful for inspection but must not become the registry or edit surface.

## Export Split and Migration Path-Rewrite Finding: 2026-06-23

- Dashboard/export has a clean dependency boundary and now lives in `scripts/_export.py`; `project_os.py` should remain the CLI facade while low-risk subsystems are extracted gradually.
- Migration/adoption must rewrite paths, not only move directories. When flat `runs/<run_id>/` becomes `runs/<branch_id>/<run_id>/`, result rows, task link tables, and run manifest inputs/outputs must all be patched together.
- Synthetic migration smoke showed that missing path warnings can come from stale registry paths even when files were successfully moved; path rewrite is therefore part of adoption correctness, not cosmetic cleanup.
- Dry-run migration reports should expose repair categories such as old link-table headers and sparse run manifests so users can decide whether to apply, replace, or handle conflicts manually.

## Schema Split Finding: 2026-06-23

- Schema/constants/templates are a safe second split after router/export because they are mostly static data and are consumed across command groups.
- Keeping `project_os.py` as a CLI facade while importing `_schema.py` reduces merge pressure without forcing a risky command-by-command rewrite.
- Further splits should prioritize low-coupling helpers next: path resolution, IO/journal, and integrity checks before command groups.

## Paths and Project IO Split Finding: 2026-06-23

- Low-level path and IO helpers are safe split targets because command groups depend on them but they do not depend on command semantics.
- Module naming matters: `_io.py` collides with Python's built-in `_io` module, so project-local IO helpers should use an unambiguous name such as `_project_io.py`.
- After schema, paths, IO, router, and export are split, the next useful split is either integrity/doctor/validate or a stable command group such as release/result.

## Integrity and Views Split Finding: 2026-06-23

- Integrity checks are reusable enough to split before command groups, but they should depend only on schema/path/IO/view helpers, not on `project_os.py` command functions.
- Derived Markdown views (`RESULTS_INDEX.md`, `DATA_ASSETS.md`) are part of consistency checking, so their generation should live in a helper module that both `refresh-indexes` and `validate/doctor` can share.
- `command_validate` and `command_doctor` can remain in the CLI facade for now; later they can move once all helper dependencies are clean.

## Hooks Contract Reservation Finding: 2026-06-23

- Hooks should be treated as a reserved automation layer, not as part of the core harness runtime.
- The stable integration point is `.project_os/journals/events.jsonl`; future handlers should observe journal events and call `project_os.py` commands instead of editing `.project_os/indexes/*.tsv`, runtime pointers, run manifests, result rows, or release manifests directly.
- A default-disabled `hooks:` config block plus `.project_os/spec/hooks.md` gives future hooks a clear extension surface without making hooks necessary for bootstrap, resume, validate, promotion, release, or migration.
- Guard hooks are high-risk and should only be added after read-only/session-summary, reminder, and opt-in maintenance hooks have been dogfooded.

## Result/Release Module Split Finding: 2026-06-23

- Result lifecycle and release packaging form a coherent command boundary because both are governed by explicit approval/promotion/release gates and share canonical result rows.
- Splitting them into `_result_release.py` reduces `project_os.py` toward a CLI facade while preserving the same public commands and file contract.
- Future guard hooks should attach around this command group, but the module itself must remain callable without hooks and must continue to enforce approval gates directly.

## Task/Run Module Split Finding: 2026-06-23

- Task lifecycle and run provenance are a coherent module boundary because both depend on branch-aware task paths, current task/run pointers, and run manifest discovery.
- `_result_release.py` should reuse `_task_run.py` helpers for `task_dir` and `find_run_manifest`; otherwise result lifecycle and run lifecycle can silently diverge on branch-first path rules.
- The next split should target asset helpers, because `add-run-input` needs asset lookup/usage updates and asset commands currently share overlapping helper logic.
- The public CLI should remain stable while modules are split: users and adapters should still call `project_os.py <command>` rather than importing internal modules directly.

## Asset Module Split Finding: 2026-06-23

- Asset registry and run asset usage must share one helper module because run inputs/outputs can update `asset_usage.tsv` and `DATA_ASSETS.md` without going through asset commands directly.
- `_assets.py` is the right boundary for checksum, URL detection, asset row lookup, asset path resolution, and asset usage upserts; `_task_run.py` should consume these helpers rather than reimplement them.
- `register-asset --run-id` needs to call run provenance code, while `_task_run.py` also needs asset helpers. A local import inside the command avoids a module-level cycle while preserving one public CLI surface.
- Keeping asset commands behind `project_os.py` means adapters and short-trigger routing do not need to know that the implementation moved.

## Decision/Handoff Module Split Finding: 2026-06-23

- Decision recording, handoff updates, and state summary form a coherent module boundary because they operate on journals and human handoff files rather than directly owning task/run/result lifecycle mutations.
- `_decision_handoff.py` should depend on canonical helpers and existing task/run/asset refresh functions, but not on `project_os.py`; this keeps the main file as a CLI facade instead of a shared library.
- `summarize-state` needs fresh branch/task/run/asset views, so the decision/handoff module includes a small branch-index refresh helper and reuses `_task_run.py` / `_assets.py` refresh functions.
- The next highest-value work is no longer this split; it is real-project adoption dogfooding and stronger migration conflict reporting, or continued splitting of project/branch/init/adapters/migration command groups.

## Project/Branch Module Split Finding: 2026-06-23

- Project bootstrap, adapter installation, status/start, refresh-indexes, and branch commands share project identity, branch workspace, runtime pointer, and adapter-template concerns, so `_project_branch.py` is a coherent boundary.
- The public CLI must remain `project_os.py`; route/export modules still receive the CLI facade as a compatibility context so existing helper lookups continue to work.
- After this split, `project_os.py` is much closer to a facade: the largest remaining command bodies are migration/adoption and validate/doctor.
- The next code split should target `migrate-branch-first` only if it also improves conflict reporting; otherwise real-project adoption dogfooding has higher product value than another mechanical split.

## Migration Module Split and Conflict Diagnostics Finding: 2026-06-23

- `migrate-branch-first` is now a coherent module boundary because adoption needs specialized planning, path mapping, conflict classification, and dry-run reporting that should not bloat the CLI facade.
- Dry-run migration should be treated as the primary safety interface: users need `safe_to_apply`, blocking conflicts, warnings, and repair categories before any file movement/copying occurs.
- Conflict reporting is now good enough for synthetic edge cases, but real-project dogfooding remains necessary because legacy projects may contain project-specific paths, manually edited manifests, or partially migrated directories.
- After extracting `_migration.py`, the largest remaining `project_os.py` command bodies are `validate` and `doctor`; however, real adoption trials may be more valuable than another immediate mechanical split.

## Health Command Module Split Finding: 2026-06-23

- `validate` and `doctor` form a coherent health-check command boundary, while `_integrity.py` should remain the reusable helper layer used by health checks and future maintenance commands.
- Keeping `project_os.py` as the only CLI/argparse entry still gives adapters, short triggers, and future hooks one stable command surface even as implementation modules split internally.
- After `_health.py`, most major command groups are extracted; further splitting should be driven by real adoption pain or concrete maintenance risk, not by module count alone.

## Current/Result Derived View Finding: 2026-06-23

- Current result display should be a derived view over `results.tsv` plus `promoted_to` targets, not a second canonical registry.
- Project-level current targets under `current/project/` should not automatically appear in branch current views; branch current views should be based on `current/branches/<branch_id>/` targets, with only legacy/migrated targetless `status=current` rows included for compatibility.
- A lightweight promotion audit in `show-current --audit` is useful before active hooks: it surfaces missing current targets, duplicate current targets, and cross-branch promotions without enforcing policy via hooks.
- Promotion audit should also run during health checks as warnings. This catches current-target drift in normal `validate` / `doctor` workflows while keeping repair non-destructive and explicit.

## Dashboard Graph Export Finding: 2026-06-23

- A graph view is useful enough to include in generated dashboard exports now, but it must remain a derived inspection layer over canonical indexes, manifests, current targets, and events.
- The graph should represent relationships, not own relationships: branch/task/run/result/asset/release rows remain authoritative, while `graph.nodes`, `graph.edges`, `graph_nodes`, and `graph_edges` are regenerated views.
- JSON/HTML/SQLite graph exports give humans and future tooling an immediate provenance map without requiring active hooks, plugin packaging, or an editable dashboard UI.
- Richer graph visualization can be deferred because the stable generated graph payload already gives later UI work a clean data contract.

## Journal Snapshot Audit Finding: 2026-06-23

- Journal/current snapshot consistency is a P1 health-check concern, not a full WAL replay feature.
- `events.jsonl` should be checked in both directions: event references should still resolve to current canonical rows, and non-legacy snapshot rows should have lifecycle event coverage.
- Rows predating `project.adopted` need legacy/adoption tolerance; otherwise migration dogfooding would create noisy false positives for historical rows.
- Missing event coverage should remain a warning with repair guidance toward state review or decision recording. Agents should not synthesize lifecycle events after the fact merely to silence warnings.

## Run Lifecycle Provenance Finding: 2026-06-24

- Package capture belongs in run provenance, not dashboard/export state: the raw `pip freeze` file is stored under the run directory and `RUN_MANIFEST.json` records the structured summary.
- `RUN_SUMMARY.md` should be a generated human handoff over the manifest, not a replacement for `RUN_MANIFEST.json`.
- A short package sample in `RUN_SUMMARY.md` is useful for review, while the freeze file and manifest preserve the full package evidence.
- The remaining run lifecycle work should now be driven by real-project dogfooding fields rather than generic package-capture or summary gaps.

## Real Legacy Harness Adoption Finding: 2026-06-24

- Real dogfooding showed that older flat harnesses may have `.project_os/workflow.md`, runtime pointers, flat `.project_os/tasks/`, and old index headers, but no `project.json`, `events.jsonl`, or branch-first workspace.
- `migrate-branch-first` should be the safe adoption entry for those projects; it must not require users to manually create the target branch before the dry-run can explain the repair.
- Dry-run migration reports need to include scaffold repairs separately from task/run movement so users can distinguish non-destructive anchor creation from provenance-moving operations.
- Legacy timestamp handling must tolerate timezone-naive timestamps in old manifests/indexes; journal/adoption comparisons should normalize them instead of crashing.
- The copied real-project migration path is now a stronger verification target than purely synthetic migration smokes: apply on a copy, then `validate`, `doctor`, and `start` must all pass before applying to a real project.

## Partial Migration Scaffold Finding: 2026-06-24

- A project can be neither fully flat nor fully branch-first: it may already contain `.project_os/branches/main/branch.json` while still keeping flat tasks/runs and missing spec/root-entry scaffold.
- Adoption migration should therefore not stop at project/journal/branch anchors. It must also create missing `.project_os/spec/*.md`, root human entry files, runtime pointer files, `current/project/`, `release/`, and branch helper directories/files when they are absent.
- The goal of `migrate-branch-first --apply` is a project that passes strict `validate` immediately; users should not need to run a second `init --apply` after adoption just to fill standard scaffold.

## Portable Externalization Finding: 2026-06-24

- Large-asset externalization must be portable across machines, filesystems, and mount layouts. Hard links are therefore the wrong primitive for the canonical design.
- Canonical recovery should resolve through:
  - `asset_id`
  - `.project_os/indexes/asset_locations.tsv`
  - location metadata such as role, path, storage root, checksum, and availability
- `assets.tsv` should keep the logical/canonical asset row, while `asset_locations.tsv` records primary/backup/mirror locations and old-path mappings.
- Symlinks may still exist in real projects as convenience links, but they must remain optional compatibility aids rather than a recovery requirement.
- Externalization should stay narrowly scoped:
  - copy/move
  - checksum verify
  - register asset
  - register locations
  - report old-path references
  - no hardlink creation
  - no automatic symlink creation
  - no automatic script/manifest/doc rewriting

## Externalization Smoke and Pilot Finding: 2026-06-24

- Temporary-project dogfood showed the portable externalization loop is operational end-to-end: report-only planning, dry-run apply preview, approval-gated apply, checksum verification, location listing, generated data-asset view refresh, and health checks all behaved correctly.
- Smoke testing also found two subtle metadata issues worth fixing immediately:
  - CLI-supplied external roots must be preserved when recording `storage_root`
  - later `refresh-assets`/primary sync must not overwrite richer primary-location notes created during externalization
- The real pilot project `/home/teng/BGCdetection/target_BGC_mining/typeII_pks` is not yet a harness project, so externalization there must begin with adoption dry-run rather than direct harness commands.
- The real pilot already contains symlink-based convenience paths, including a broken symlink to the missing in-project FAA copy. This is a useful real-world confirmation that canonical recovery cannot assume symlink presence or correctness.
- FAA reference pressure in the real pilot is nontrivial (49 basename hits, 8 exact old absolute-path hits), so future adoption/externalization reporting should emphasize manual repair guidance rather than automatic rewrites.
- External artifact paths outside `runs/` should remain valid and should not be rewritten merely because a run directory was migrated; path rewrite should only change paths covered by the flat-run path map.

## Hand-edited Manifest Migration Finding: 2026-06-24

- Legacy projects may have task/run directory names that disagree with `task.json.task_id` or `RUN_MANIFEST.json.run_id`; migration must block these rather than silently changing object identity.
- Legacy manifests may already carry a `branch_id` from a different workstream; migration must require either the matching `--branch-id` or explicit manifest repair before apply.
- Malformed task/run/branch manifests are apply blockers because canonical provenance cannot be safely inferred.
- Result rows with paths outside `runs/` are not inherently bad. If task-local `result_links.tsv` supplies `run_id`, migration can backfill branch/task/run provenance without rewriting the external artifact path.
- Dry-run diagnostics should distinguish blocking identity/provenance conflicts from warnings that require review but do not necessarily make adoption unsafe.

## Legacy Run Provenance Shape Migration Finding: 2026-06-24

- Real legacy run manifests may store `inputs` and `outputs` as dicts, `commands` as a list of strings, `promoted` instead of `promoted_to`, and key results under project-specific fields such as `key_results`.
- Migration must not satisfy the new schema by replacing those older shapes with empty lists; that silently loses provenance even when `validate` still passes.
- The safer behavior is to normalize legacy dict/string/list shapes into structured entries with migration notes and preserve non-path values under `value` fields.
- Dry-run should expose these changes in `manifest_repairs` (`normalize_inputs_shape`, `normalize_outputs_shape`, `normalize_commands_entries`, etc.) so users can see that a structural provenance normalization will happen before apply.
- Unusual run roots such as `analysis_runs/<run_id>/` should follow the same preservation and path-rewrite logic as `runs/<run_id>/`; branch-aware targets become `analysis_runs/<branch_id>/<run_id>/`.

## Cross-Branch Legacy Migration Finding: 2026-06-24

- Default migration should remain conservative: `--branch-id <id>` is a single target branch for unannotated flat layouts, and a legacy manifest `branch_id` mismatch should block instead of silently merging workstreams.
- Some legacy projects may already contain trustworthy `branch_id` values across flat tasks/runs. These need an explicit mode rather than separate manual migrations per branch.
- `--preserve-manifest-branches` is the safer explicit contract: dry-run reports `planned_branches`, scaffold repairs are planned for each legacy branch, and tasks/runs are moved into `.project_os/branches/<legacy_branch>/tasks/...` plus `runs/<legacy_branch>/<run_id>/`.
- Cross-branch path rewriting must use each run's target branch, not the default branch, otherwise `results.tsv`, task link tables, and run manifest outputs can point to the wrong physical location.
- Invalid legacy branch IDs must block migration because using them as path components would create unsafe or surprising directories.
- Even in preserve mode, a run and the task it references must belong to the same target branch. If `RUN_MANIFEST.json.branch_id` and the referenced `task.json.branch_id` disagree, migration should block with `run_task_branch_mismatch` instead of relying on post-apply validation.

## Short Trigger Approval/Provenance Routing Finding: 2026-06-24

- The short-trigger router is useful only if it can express the same provenance and approval semantics as the underlying CLI; otherwise users fall back to raw commands for routine actions such as environment capture.
- `捕获运行环境` should be able to pass `--pip-freeze` and `--freeze-file` through the route layer because package capture is part of run provenance, not an advanced dashboard-only feature.
- Planning `--apply` from a short trigger is still not equivalent to executing it. The route plan should remain non-ready unless promotion/release apply requests are paired with explicit `--approved`, preserving the harness rule that current/release state changes need user approval.
- Keeping `route` and `explain-trigger` on one shared argparse helper reduces drift between the two aliases and makes future trigger parameters safer to add.

## Documentation Contract Convergence Finding: 2026-06-24

- The harness contract must not call root human documents canonical; they are handoff/derived views, while `.project_os/indexes/*.tsv`, `.project_os/project.json`, `.project_os/journals/events.jsonl`, runtime pointers, branch/task manifests, and run manifests are the machine/provenance sources of truth.
- Adoption documentation should route fresh projects to `init` dry-run, but old flat or partial harnesses to `migrate-branch-first` dry-run first so branch mapping, scaffold repairs, target existence, and provenance rewrites are visible.
- Template text has two sources: files under `templates/project_os/spec/` and the `_schema.py` `SPEC_TEXTS` used by `init/new-project`. Both must stay aligned, otherwise newly initialized projects can receive stale policy files even when repository templates look correct.
- New-project generated spec files should include the already implemented run package capture, detailed `RUN_SUMMARY.md`, current-result derived views, and journal/current snapshot audit policies.

## Routing Boundary Cleanup Finding: 2026-06-24

- Older bioinfo/writing planning docs can silently route long-running project prompts back to `planning-with-files` if they still call it the “big project kernel”.
- The stable boundary should be phrased consistently across docs: `research-project-os` owns long-running project harness, continuation, and provenance; `planning-with-files` remains useful for temporary multi-step tasks that do not need `.project_os`.
- Keeping this boundary explicit prevents duplicate state systems (`task_plan.md`/`progress.md` vs `.project_os`) from being created for the same long-lived project.

## Sessionized Runtime Focus Finding: 2026-06-24

- Named sessions are useful as runtime focus overlays, not as new project state identities. A session should answer “this conversation/work context is currently looking at which branch/task/run?” while canonical branch/task/run/result state remains in indexes and manifests.
- Backward compatibility is simple if `.project_os/runtime/current_session` is optional and empty by default: existing projects and commands continue to use global `current_branch/current_task/current_run`.
- When `current_session` is set, all pointer reads/writes should go through the same helper layer (`current_pointer` / `set_pointer`) so command groups do not need session-specific forks.
- Session validation belongs in normal `validate` / `doctor`: missing session manifests, broken session pointers, and session references to missing branch/task/run objects should be surfaced before future hooks or dashboards rely on them.
- Short triggers such as `新建会话` and `切会话` should route to deterministic CLI plans. They must not create separate branch/task/run identities or bypass promotion/release approval gates.
- Future session hooks can summarize focus on session start, but active hook dispatch should remain separate from the now-working session pointer foundation.

## Manual Hooks Dispatcher Finding: 2026-06-24

- Hooks are useful before full automation if they are framed as a manual report layer over `events.jsonl`, not as an active background system.
- `dispatch-hooks` should generate summaries, reminders, and maintenance suggestions but must not auto-run suggested commands; otherwise it would bypass the same approval and provenance gates the harness is designed to preserve.
- Generated hook reports under `.project_os/exports/hooks/` are inspection views only. Canonical machine state remains `.project_os/indexes/*.tsv`, `.project_os/project.json`, `.project_os/journals/events.jsonl`, runtime pointers, and branch/task/run/result/release manifests.
- Guard hooks are high risk and should remain report-only placeholders until there is explicit user/project opt-in, clear bypass behavior, and more real-project dogfooding.
- The short-trigger router can safely expose `hook状态` and `hook报告` because those phrases route to deterministic CLI plans/reports, not hidden automation.

## Hooks Route Parity Finding: 2026-06-24

- If short triggers expose `hook报告`, they should be able to express the same safe selection controls as the manual dispatcher: exact event line, event-name filter, recent-event limit, handler kind, and generated report output.
- Planning `--write-report` from the route layer is acceptable only because hook reports are generated inspection views; the route plan must explicitly preserve that they are not canonical machine state.
- Hook route parity should not be confused with active hooks: route/explain-trigger still only returns a command plan and must not run suggested maintenance commands or bypass promotion/release approval gates.

## Session Pause/Resume Finding: 2026-06-24

- Session lifecycle needs a middle state between active and closed so users can temporarily park a conversation/work context without deleting its branch/task/run focus.
- Pausing a current session should clear `.project_os/runtime/current_session` rather than leaving the harness in a non-actionable active focus; this keeps global pointers usable until the session is resumed.
- Resuming is an explicit action and may optionally set the session current. This prevents accidentally switching work contexts while still keeping short triggers simple.
- Validation should treat `current_session -> paused/closed` as an error, because active commands should only shadow pointers through an active session.

## Dashboard Session Focus Finding: 2026-06-24

- Once sessions can be active, paused, resumed, and closed, dashboard output should show the runtime focus overlay explicitly; otherwise users can see branch/task/run graph state but miss why the current focus is routed through a session.
- Session focus belongs in generated dashboard views, not in new canonical tables. The source remains runtime pointers and session manifests.
- Adding session nodes and focus edges to the generated graph makes the relationship between a conversation/work context and branch/task/run visible without changing branch/task/run identity.
- SQLite dashboard exports should expose the same derived session information as JSON/HTML for downstream inspection, while preserving the rule that SQLite is not an editable state store.

## Report-only Session Cleanup Finding: 2026-06-24

- Session archive/GC should start as a candidate report, not a physical cleanup operation, because session directories are runtime focus evidence and may still be useful for handoff/debugging even after closure.
- The safe default is closed-session-only dry-run output; paused sessions can be included explicitly when the user wants review candidates, while active/current sessions should remain excluded unless explicitly requested.
- Generated cleanup reports belong under `.project_os/exports/session_cleanup/` and are not canonical state. They should help humans decide whether to resume, close, dashboard-export, or manually archive later.
- Short triggers such as `会话清理` must never route to delete/move operations. If physical session archive/GC is ever added, it must be explicit, reviewed, approval-gated, validation-gated, and should not create a second canonical session registry.

## Dashboard/Doctor Session Cleanup Advisory Finding: 2026-06-24

- Cleanup candidates should be visible where users already inspect project health, but they should not be treated as validation errors: a closed session is legitimate historical runtime evidence, not broken state.
- Dashboard is the right place for an always-derived overview (`session_cleanup` JSON/HTML/SQLite), while `doctor --repair-plan` should provide an advisory command to generate a more detailed report.
- The advisory must not make `doctor` fail because the next action is optional review, not required repair.
- Reusing the same `build_session_cleanup_plan` helper keeps CLI reports, dashboard views, hook reminders, and doctor suggestions aligned without introducing a second session cleanup state model.

## Hooks Dashboard/Doctor Advisory Finding: 2026-06-24

- Manual hooks become easier to reason about when their disabled/available status is visible in the same generated dashboard used for branch/task/run/session inspection.
- Hooks config drift should be surfaced early, but only as advisory warnings: a project may accidentally set `hooks.enabled=true` or add unknown kinds, yet this harness build must still not activate automatic dispatch.
- `doctor --repair-plan` should point users back to `list-hooks` and config review rather than attempting to rewrite hooks config automatically.
- Dashboard hooks status, hook report counts, and SQLite hook tables are generated inspection views. They must not become a second hook registry or a switch that enables active hooks.

## Real Migration Dogfood Finding: 2026-06-24

- A real partial/legacy harness at `/home/teng/pingtai_final_20260430` matched the important adoption class: old `.project_os/tasks/`, old indexes/spec/config/runtime, no `project.json`, no event journal, no branch workspace, and one flat run under `runs/<run_id>/`.
- Running dogfood only on `/tmp` copies confirmed the migration path can create missing scaffold, copy or move flat task/run objects, validate cleanly, and resume with `start` without touching the original project.
- Users and scripts benefit from top-level `safe_to_apply`, `summary`, `conflicts`, and `warnings`; keeping them only under `diagnostics` makes quick triage and jq checks unnecessarily fragile.
- Repeated migration diagnostics are useful real-world evidence: `target_exists` must block by default and become non-blocking only when `--replace` is explicit.
- `--mode move` can leave an empty legacy `.project_os/tasks/` directory after moving all task children. This is benign and should not trigger automatic deletion; if cleanup is added later it should be an explicit report/cleanup planner, not part of migration apply.
- Adapter repair-plan suggestions should be actionable. Missing Codex/Claude adapter warnings should point to `install-adapters --platforms codex|claude --apply` with approval required, not back to `doctor`.

## Restore-journal Repair Finding: 2026-06-24

- A missing `events.jsonl` is a different problem from missing object-level lifecycle coverage. The former can be safely repaired by creating the absent event source; the latter is provenance-sensitive and should remain a warning that triggers review.
- `restore-journal` should be minimal and auditable: dry-run first, approval-gated apply, create only the missing journal, append `journal.restored`, and never synthesize historical lifecycle events.
- Repair-plan suggestions should distinguish the default event journal path from arbitrary `hooks.event_source` values. Non-default missing sources are likely config drift and should point to config review rather than silently creating a new source.
- Short-trigger support for `恢复事件日志` is useful, but apply must require `--approved` because it writes canonical event-source state.

## Report-only Recovery Planner Finding: 2026-06-24

- Full WAL/crash replay is too risky to add before more real-project evidence; the safe intermediate step is a report-only recovery planner that finds candidates without acting on them.
- Stale locks, tmp leftovers, malformed event lines, missing harness paths, pointer drift, index drift, and stale generated views are useful to see together because they often appear after interrupted CLI operations or manual edits.
- `plan-recovery --write-report` should not append lifecycle events: the report itself is a generated inspection view, and recording it in `events.jsonl` would mutate the canonical event source during recovery inspection.
- `doctor --repair-plan` can point to `plan-recovery` as an advisory, but the presence of recovery candidates should remain warning-level unless existing validation rules already identify a concrete error.
- Short triggers such as `恢复检查` are safe only if they route to report-only planning. They must not become aliases for automatic tmp deletion, lock removal, journal rewrite, replay, or rollback.
- Dashboard recovery summaries help users notice candidate issues, but the full detailed report should remain under `.project_os/exports/recovery/` and be treated as non-canonical.

## Dashboard Current-Result View Finding: 2026-06-24

- Users need to see “当前结果” in the same generated dashboard where they inspect graph/session/recovery state; otherwise they must jump between `RESULTS_INDEX.md`, `show-current --audit`, and dashboard exports.
- The safe implementation is to reuse the existing `show-current --audit` helper layer (`current_result_views` and `promotion_audit`) rather than introducing a second result/current interpretation.
- Dashboard JSON/HTML/SQLite can expose current/project/branch result rows and promotion-audit warnings, but those rows must remain derived from `results.tsv` and `current/` targets.
- SQLite tables such as `current_results` and `promotion_audit` are useful for inspection/querying, but they must not become an editable result registry or a backdoor for promotion.
- Promotion, replacement, release inclusion, and current-target repair still require the existing approval-gated CLI commands and validation/doctor review.

## Current-Result Short-Trigger Finding: 2026-06-24

- Users naturally say `当前结果` when they want to inspect the currently promoted output, so this phrase needs an explicit route rather than relying on the broader result/promotion wording.
- `当前结果` must remain read-only and route to `show-current --audit`; otherwise it can be confused with `设为当前结果`, which is an approval-gated promotion operation.
- Branch-aware inspection should be easy: when a branch id is supplied, the router can safely narrow the plan to branch scope without mutating state.
- Keeping this route in the same non-executing router layer preserves the harness boundary: short phrases produce auditable command plans, not hidden result promotion, current-target repair, or canonical-state rewrites.

## Summarize-State Focus/Current-Result Finding: 2026-06-24

- `summarize-state` is the natural handoff payload for agents, so it should not lag behind `status`, `show-current`, or dashboard views when new runtime/current-result layers are added.
- Session-aware focus must be visible in the summary; otherwise a future agent may see global pointers while commands are actually routed through `.project_os/runtime/current_session`.
- Current-result summary belongs in `summarize-state`, but only as a derived read-only view from `results.tsv` and `current/` targets. It should reuse the same helper layer as `show-current --audit` and dashboard exports to avoid conflicting interpretations.
- Keeping `current_results` as counts/rows/audit warning counts is enough for handoff; promotion, replacement, current-target repair, and release inclusion must still go through their explicit approval-gated commands.

## Status Run/Result Summary Finding: 2026-06-24

- `status` is the first command users and agents run to understand whether the harness is usable, so it needs to show more than raw pointers and row counts.
- The safe implementation is still read-only: derive active/last run and candidate/current result summaries from existing indexes and current targets without refreshing indexes or touching manifests.
- `status`, `summarize-state`, `show-current --audit`, and dashboard exports should reuse the same current-result interpretation so branch/project current rows do not disagree.
- The command should expose enough frontier information to answer “what is active, what was last run, and what result is current?” while leaving promotion, repair, release, and index refresh to explicit commands.

## Direct Approval-Gate Finding: 2026-06-24

- Router-level approval checks are not enough if the direct CLI can still apply promotion or release without the same `--approved` flag.
- The safer invariant is: dry-run promotion/release/journal-restoration requires no approval, but any write path that changes `current/`, `results.tsv`, release artifacts, `releases.tsv`, or the canonical event journal must require both `--apply` and `--approved`.
- The short-trigger router should pass `--approved` into planned commands when approval is present, so a ready route plan is executable as-is and does not rely on hidden context.
- This keeps current-result inspection, promotion, release packaging, and manual hooks aligned around explicit approval gates rather than implicit agent judgment.
- Repair-plan and recovery suggestions should also include `--approved` when they recommend approval-gated write commands; otherwise copied commands may fail or teach the wrong safety habit.

## Disposable E2E Coverage Finding: 2026-06-24

- A harness-level skill needs a repeatable disposable release smoke, not just targeted one-off command snippets, because CLI surface drift is otherwise easy to miss after many small feature slices.
- The coverage audit should be mechanical: enumerate public `project_os.py` subcommands and compare them against smoke-script invocations. The current audit shows 80/80 public subcommands covered.
- Approval gates need both positive and negative coverage. It is not enough to verify that approved writes succeed; unapproved `--apply` paths must fail before changing canonical state.
- External asset tests must pass explicit temporary storage roots. Relying on configured default roots in smoke tests can accidentally touch real storage.
- No-hardlink/no-symlink checks belong in the E2E smoke because portability is a product invariant, not only a documentation promise.
- Report-only features (`plan-session-cleanup`, `plan-recovery`, manual hook dispatch, migration dry-run) should remain covered without turning the smoke into a physical cleanup, crash replay, background hook, or real-project migration test.
