---
name: project-flow-guard
description: Development-time project flow/version guard for Codex across any project. Use to prevent version confusion when work creates or regenerates nontrivial artifacts, promotes accepted outputs, branches long-lived directions, packages releases, or reorganizes files. It treats runs as provenance, not the human result entry point, and prefers md/tsv/json ledgers such as `RESULTS_INDEX.md`, `RUNS_INDEX.tsv`/`.project_flow/RUNS.tsv`, and `RUN_MANIFEST.json`. Trigger on 重跑, 重新生成, 重新绘图, 再生成一版, 改一版, 调整一下, 换参数, 换参考, 基于这版, 保留这个版本, 就用这个, 设为当前版本, make current, accept, promote, 冻结当前版本, 保存当前状态, snapshot, baseline, seal, 开分支, 新分析方向, 基于这个版本继续, branch, same data new analysis, release, 投稿, 打包, 清理旧版本, 整理目录, delete old versions, or similar.
---

# Project Flow Guard

## Prime directive

Prevent version confusion **during development, before files are created**.

Do not treat this as only a post-hoc cleanup skill. Use it as a preflight guard whenever work may create, regenerate, revise, promote, branch, release, or reorganize outputs.

Runs are **provenance**, not the primary place humans look for results. Accepted/candidate/legacy outputs should be discoverable through `PROJECT_STATE.md`, `RESULTS_INDEX.md`, `current/`, and TSV registries.

Canonical source formats are limited to Markdown (`.md`), TSV (`.tsv`), and JSON (`.json`). SQLite/HTML may be generated for query/display later, but do not treat them as canonical source unless the user explicitly changes project policy.

## First classify the task

Before writing files, classify the user's intent:

| Intent | Typical trigger | Required behavior |
|---|---|---|
| `source_edit` | fix code, patch script, edit config/docs | Edit in place when appropriate, but record changed files/tests/decisions. |
| `artifact_run` | 重跑, 重新生成, 重新绘图, generate table/report/model/data | Create or use an active run for provenance; generated draft artifacts go under that run, then accepted outputs are promoted and indexed. |
| `child_run` | 基于这版, 改一版, 换参数, change style/label/reference | Create a child run from the previous accepted/completed run. |
| `promote` | 保留这个版本, 就用这个, make current, accept | Copy/link/register selected outputs into `current/`; update registries. |
| `seal_baseline` | 冻结当前版本, snapshot, baseline, seal | Create a baseline manifest snapshot of accepted/current state. |
| `start_branch` | 开分支, 新分析方向, same data new analysis | Create a long-lived branch/workstream only when the direction is truly long-lived and user-confirmed. |
| `checkpoint_and_branch` | 保留这版并开分支, 基于这个版本继续 | Composite: promote if needed, seal baseline if needed, start branch. |
| `build_release` | release, 投稿, 打包, publication package | Package accepted/current files into a versioned release. |
| `cleanup` | 清理, 删除旧版本, 整理目录 | Dry-run only unless user explicitly confirms destructive actions. |

If multiple triggers appear, prefer the highest composite intent:

```text
promote + baseline + branch => checkpoint_and_branch
```

## Protected areas

Treat these as protected:

- `.project_flow/`: guardrail ledgers; update through this skill or deliberately with care.
- `current/`: accepted/canonical working outputs; update only via `promote`.
- `RESULTS_INDEX.md`: human result entry point; update when accepted/candidate/legacy result pointers change.
- `RUNS_INDEX.tsv` if present: human-facing run index; keep in sync with `.project_flow/RUNS.tsv` for formal runs.
- `release/`: immutable delivery/publication/package snapshots; update only via `build-release`.
- `baselines/`: snapshots; never edit in place.
- previous `runs/` outputs: read-only once closed, except continuing a failed/incomplete active run.

## Preflight checklist

Before any nontrivial write:

1. Locate project root.
2. Initialize `.project_flow/` if needed.
3. Read `PROJECT_STATE.md` if it exists, plus `RESULTS_INDEX.md` only if result entry points matter.
4. Read `ACTIVE_RUN`, `ACTIVE_BRANCH`, and relevant ledgers.
5. Classify the task.
6. Decide: edit source in place, continue active run, create new run, create child run, start a user-confirmed branch/workstream, promote, or release.
7. Verify proposed output paths:
   - generated artifacts go to an active run's `outputs/`, `plots/`, `tables/`, etc.;
   - `current/` only via promote;
   - `release/` only via build-release.
8. For cleanup/reorganization/deletion, produce a dry-run plan first.

Use the bundled CLI when practical:

```bash
python ~/.codex/skills/project-flow-guard/scripts/project_flow_guard.py <command> --root .
```

Common commands:

```bash
# Initialize ledgers.
python ~/.codex/skills/project-flow-guard/scripts/project_flow_guard.py init --root .

# Start a guarded artifact run.
python ~/.codex/skills/project-flow-guard/scripts/project_flow_guard.py start-run --root . --task "redraw figure" --intent artifact_run

# Promote a run output to current/.
python ~/.codex/skills/project-flow-guard/scripts/project_flow_guard.py promote --root . --run-id <run_id> --source outputs/file.pdf --canonical figures/file.pdf

# Freeze current state and start a new long-lived branch.
python ~/.codex/skills/project-flow-guard/scripts/project_flow_guard.py checkpoint-and-branch --root . --name "new analysis direction"
```

## Run lifecycle

Use a run for generated artifacts or exploratory work, but do not rely on `runs/` as the result discovery interface.

```text
runs/YYYYMMDD_HHMMSS__task-name/
├── inputs/
├── outputs/
├── plots/
├── tables/
├── scripts/
├── logs/
├── docs/
├── RUN_MANIFEST.json      # canonical structured run metadata
└── RUN_MANIFEST.md        # optional human summary, if produced
```

Inside a branch, runs live at:

```text
branches/<branch_id>/runs/<run_id>/
```

Rules:

- Failed/incomplete immediate debugging may `continue-run`.
- A successful result followed by a parameter/style/reference change should create a `child_run`.
- Do not overwrite a closed run from a different task.
- Every formal run should be registered in `.project_flow/RUNS.tsv`; if the project has root `RUNS_INDEX.tsv`, mirror a concise row there.
- `RUN_MANIFEST.json` is the canonical run-level manifest. Keep it concise: inputs, commands, parameters, outputs, status, promoted paths, superseded-by, and notes.
- Do not create a new run for tiny source edits, doc edits, or pure status updates unless they also create nontrivial generated artifacts.

Recommended statuses:

```text
active, completed, failed, pending_review, candidate, accepted, superseded, archived, legacy
```

Use the existing CLI statuses where applicable; use registry notes or `RESULTS_INDEX.md` to express `candidate/accepted/superseded/legacy` if the CLI status set is narrower.

## Branch/workstream and baseline lifecycle

Use `baseline` to freeze an accepted state. Use `branch` for a long-lived direction based on a baseline.

```text
baseline -> branch -> runs -> branch/current -> project/current -> release
```

Use `checkpoint_and_branch` when the user says anything like:

- 保留这个版本并继续
- 基于这个版本开分支
- 这个版本作为起点
- 保存当前状态然后做另一个分析
- branch from current
- same data new analysis

Do **not** create a branch/workstream for every parameter change. Treat a direction as long-lived only when most of these are true:

- It asks a different scientific/product question.
- It uses a different method/reference architecture.
- It will produce separate deliverables.
- It will likely require multiple runs.
- The user explicitly confirms it as a separate direction.

If unsure, keep the work in the current active direction as an ordinary run and mark the possible direction as `candidate` in notes rather than creating a branch.

Decision tree:

1. If the source files are not accepted/current, promote selected outputs first.
2. If no suitable baseline exists, seal a baseline.
3. Start a branch from that baseline.
4. Set the new branch as active context.

## Source edit sessions

For code/config/doc source edits, do not force everything into `runs/`. Instead:

- patch the intended source files normally;
- record changed paths, commands/tests, and rationale in `.project_flow/CHANGELOG.tsv` or `DECISIONS.md`;
- if the edit creates generated artifacts, those artifacts still go into a run.

## Promotion policy

Promotion is explicit. Triggered by: 保留这个版本, 就用这个, 设为当前版本, make current, accept, promote.

Promotion should:

1. identify source run/output;
2. choose canonical destination under `current/` or branch `current/`;
3. copy/link/register according to project policy and file size;
4. update `FILE_REGISTRY.tsv`;
5. append `PROMOTIONS.tsv`;
6. update `RUN_MANIFEST.json` for the source run when practical;
7. update `RESULTS_INDEX.md` when the promoted file changes what humans should use;
8. summarize what replaced what.

Default materialization strategy:

- small/medium files: copy;
- large files: manifest pointer or ask user before copy;
- projects already using DVC/DataLad/Git-LFS: register tool-managed pointer rather than duplicating data.

## Postflight checklist

After generating or modifying files:

1. Register outputs and changed files.
2. Update run status if a run was used.
3. Update `RUN_MANIFEST.json` with commands, parameters, outputs, and status.
4. Record important decisions in `DECISIONS.md` or `.project_flow/DECISIONS.md`.
5. If accepted/candidate/legacy entry points changed, update `RESULTS_INDEX.md` and `current/` via promote.
6. Report paths grouped by draft/candidate/accepted.
7. Ask for promotion only when useful; do not silently make outputs current.

## Bundled resources

- `scripts/project_flow_guard.py`: initialize guardrail ledgers, start/close runs, promote outputs, seal baselines, start branches, checkpoint-and-branch, build releases, and dry-run cleanup.
- `references/trigger-keywords.md`: expanded keyword table.
- `references/registry-schema.md`: TSV schemas and manifest templates.
