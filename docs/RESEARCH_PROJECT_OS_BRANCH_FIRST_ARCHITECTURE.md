# Research Project OS Branch-First Architecture

> Status: superseded by `docs/RESEARCH_PROJECT_OS_COMPLETE_DEVELOPMENT_PLAN.md`
> Retained as historical context / detailed reference only. If it conflicts with the complete plan, follow the complete plan.


Date: 2026-06-23

## 1. Decision

Adopt a **branch-first physical workspace architecture** for `research-project-os`.

A branch/workstream is not only a `branch_id` column in global indexes. Each branch gets its own physical workspace under:

```text
.project_os/branches/<branch_id>/
```

Formal run outputs also use branch-aware layout by default:

```text
runs/<branch_id>/<run_id>/
```

Global indexes remain mandatory for cross-branch search, dashboards, hooks, plugin packaging, and summary commands.

## 2. Why branch-first

Scientific and analysis projects often have multiple active directions:

- main analysis line;
- alternative methods;
- parameter exploration;
- figure/table rebuild branches;
- validation branches;
- reviewer-response branches;
- release-preparation branches.

A purely logical `branch_id` field is easy to lose in a flat tree. Physical branch workspaces make project state easier to inspect, archive, and resume.

## 3. Design principle

```text
Physical branch directories provide isolation.
Global indexes provide search and aggregation.
```

Do not duplicate the whole project per branch. A branch directory stores branch-local harness knowledge: tasks, handoff, decisions, research notes, and branch-local links. Shared data assets, project-level decisions, project state, global indexes, current results, and release packages remain at the root or global `.project_os/` level.

## 4. Target project layout

```text
<project>/
├── PROJECT_STATE.md
├── DATA_ASSETS.md
├── RESULTS_INDEX.md
├── RUNS_INDEX.tsv
├── DECISIONS.md
├── AGENTS.md                         # optional repo guidance
├── current/
│   ├── project/                       # project-level current accepted outputs
│   └── branches/
│       └── <branch_id>/               # branch-level current accepted outputs
├── release/
│   └── <release_id>/
│       ├── MANIFEST.tsv
│       ├── CHECKSUMS.tsv
│       ├── README.md
│       └── files...
├── runs/
│   └── <branch_id>/
│       └── <run_id>/
│           ├── RUN_MANIFEST.json
│           └── outputs...
└── .project_os/
    ├── workflow.md
    ├── config.yaml
    ├── runtime/
    │   ├── current_branch
    │   ├── current_task
    │   ├── current_run
    │   └── sessions/
    ├── spec/
    │   ├── project_rules.md
    │   ├── branch_model.md
    │   ├── task_tree.md
    │   ├── context_manifest.md
    │   ├── run_provenance.md
    │   ├── result_curation.md
    │   ├── data_assets.md
    │   ├── user_profile.md
    │   └── release_packaging.md
    ├── branches/
    │   ├── main/
    │   │   ├── branch.json
    │   │   ├── objective.md
    │   │   ├── context.md
    │   │   ├── handoff.md
    │   │   ├── decisions.md
    │   │   ├── research/
    │   │   ├── notes/
    │   │   └── tasks/
    │   │       └── <task_id>/
    │   │           ├── task.json
    │   │           ├── objective.md
    │   │           ├── context.md
    │   │           ├── context_manifest.jsonl
    │   │           ├── handoff.md
    │   │           ├── decisions.md
    │   │           ├── run_links.tsv
    │   │           └── result_links.tsv
    │   └── <branch_id>/
    │       └── ... same structure ...
    ├── indexes/
    │   ├── branches.tsv
    │   ├── tasks.tsv
    │   ├── runs.tsv
    │   ├── results.tsv
    │   ├── assets.tsv
    │   └── releases.tsv
    ├── journals/
    └── exports/
        ├── task_graph.html            # generated, future
        ├── run_graph.html             # generated, future
        └── result_dashboard.html      # generated, future
```

## 5. Branch workspace structure

Each branch directory is a local namespace:

```text
.project_os/branches/<branch_id>/
├── branch.json
├── objective.md
├── context.md
├── handoff.md
├── decisions.md
├── research/
├── notes/
└── tasks/
    └── <task_id>/
        ├── task.json
        ├── objective.md
        ├── context.md
        ├── context_manifest.jsonl
        ├── handoff.md
        ├── decisions.md
        ├── run_links.tsv
        └── result_links.tsv
```

### File responsibilities

| File | Purpose |
|---|---|
| `branch.json` | machine-readable branch metadata |
| `objective.md` | branch goal and scope |
| `context.md` | branch background and assumptions |
| `handoff.md` | where this branch stopped and how to continue |
| `decisions.md` | branch-level decisions |
| `research/` | branch-specific literature/method notes |
| `notes/` | lightweight branch notes |
| `tasks/` | branch-local tasks |

## 6. Branch metadata

`branch.json` should contain at least:

```json
{
  "branch_id": "main",
  "title": "Main analysis line",
  "status": "active",
  "parent_branch_id": "",
  "git_branch": null,
  "created_at": "2026-06-23T00:00:00+08:00",
  "closed_at": null,
  "objective_file": "objective.md",
  "context_file": "context.md",
  "handoff_file": "handoff.md",
  "notes": ""
}
```

Branch statuses:

```text
active, paused, completed, archived, abandoned
```

## 7. Runtime pointers

Runtime pointers remain global:

```text
.project_os/runtime/current_branch
.project_os/runtime/current_task
.project_os/runtime/current_run
```

Resolution order for resume:

```text
current_branch
  -> .project_os/branches/<branch_id>/
  -> current_task
  -> .project_os/branches/<branch_id>/tasks/<task_id>/context_manifest.jsonl
  -> current_run
  -> runs/<branch_id>/<run_id>/RUN_MANIFEST.json
```

If `current_task` points to a task whose `branch_id` differs from `current_branch`, `doctor` must report an inconsistency.

## 8. Run layout

Default formal run path:

```text
runs/<branch_id>/<run_id>/RUN_MANIFEST.json
```

`RUN_MANIFEST.json` must include:

```json
{
  "run_id": "...",
  "branch_id": "main",
  "task_id": "...",
  "status": "active",
  "created_at": "...",
  "closed_at": null,
  "inputs": [],
  "commands": [],
  "outputs": [],
  "metrics": {},
  "notes": ""
}
```

A project may use a different run root only if recorded in `.project_os/config.yaml`.

## 9. Result layout

Results are registered globally but retain branch identity:

- `.project_os/indexes/results.tsv` contains all results.
- Branch task `result_links.tsv` contains branch-local task links.
- `RESULTS_INDEX.md` summarizes project-level accepted/current/candidate/legacy results.
- `current/branches/<branch_id>/` contains branch-level current outputs.
- `current/project/` contains project-level current outputs.

Result rows should contain:

```text
result_id branch_id task_id run_id status type path title created_at accepted_at promoted_to replaced_by notes
```

## 10. Global indexes

Even with physical branch directories, global indexes are required:

```text
.project_os/indexes/branches.tsv
.project_os/indexes/tasks.tsv
.project_os/indexes/runs.tsv
.project_os/indexes/results.tsv
.project_os/indexes/assets.tsv
.project_os/indexes/releases.tsv
```

Global indexes answer cross-branch questions:

- Which branches exist?
- Which tasks are active across all branches?
- Which runs are active/failed/completed?
- Which results are candidates or current?
- Which assets are used by multiple branches?
- Which releases include which branches/results?

## 11. Command path mapping

| Command | Primary path touched |
|---|---|
| `create-branch` | `.project_os/branches/<branch_id>/`, `.project_os/indexes/branches.tsv` |
| `set-current-branch` | `.project_os/runtime/current_branch` |
| `archive-branch` | `.project_os/branches/<branch_id>/branch.json`, `branches.tsv` |
| `create-task` | `.project_os/branches/<branch_id>/tasks/<task_id>/` |
| `set-current-task` | `.project_os/runtime/current_task` |
| `create-run` | `runs/<branch_id>/<run_id>/RUN_MANIFEST.json` |
| `set-current-run` | `.project_os/runtime/current_run` |
| `register-result` | `.project_os/indexes/results.tsv`, task `result_links.tsv` |
| `promote-result` | `current/branches/<branch_id>/` or `current/project/` |
| `build-release` | `release/<release_id>/` |
| `refresh-indexes` | `.project_os/indexes/*.tsv`, root summaries |
| `doctor` | reads all canonical indexes and runtime pointers |

## 12. Migration from older flat layout

Earlier versions used:

```text
.project_os/tasks/<task_id>/
runs/<run_id>/
```

Migration target:

```text
.project_os/branches/main/tasks/<task_id>/
runs/main/<run_id>/
```

Migration should be dry-run first and must not delete old files automatically. The migration command can be added later:

```text
migrate-branch-layout --from-flat --to-branch main --apply
```

Until migration exists, `doctor` may support both layouts but should recommend branch-first for new projects.

## 13. Future extension interfaces

### Plugin packaging

The plugin should package the same branch-first templates. No plugin-specific project state should replace `.project_os/`.

### Hooks

Hooks may later observe lifecycle events such as:

```text
branch.created
branch.changed
task.created
run.created
run.closed
result.registered
result.promoted
release.created
```

Hooks should call CLI commands or validators; they should not implement a second state model.

### Dashboard

Dashboards should read `.project_os/indexes/*.tsv` and branch metadata. They are generated views only.

### Subskills

Future subskills such as `project-os-branch` or `project-os-run` should call the same CLI and preserve this branch-first layout.

## 14. Non-goals

- Do not copy the entire project for each branch.
- Do not treat harness branch as necessarily identical to Git branch.
- Do not delete archived branch directories.
- Do not make dashboard/export files canonical state.
- Do not require hooks for the core harness to work.
