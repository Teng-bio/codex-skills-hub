# research-project-os harness implementation plan

Date: 2026-06-19

## 1. Conclusion

`research-project-os` should be implemented as a **repository-local harness plus a small skill suite**, not as one oversized `SKILL.md`.

The stable split should be:

```text
Project harness/workspace   .project_os/ in each research project
Human entry points          PROJECT_STATE.md, DATA_ASSETS.md, RUNS_INDEX.tsv, RESULTS_INDEX.md, DECISIONS.md
Reusable agent methods      skills/local/research-project-os/ and narrow subskills
Deterministic mechanics     Python CLI/scripts and JSON schema checks
Distribution                local skills first; optional Codex plugin later
```

This mirrors the useful part of Trellis: project knowledge is stored in repo files, while platform-specific agent entry points only teach the agent how to operate those files.

## 2. Sources checked

### Agent harness and Trellis

- Trellis GitHub / docs / npm pages describe Trellis as a multi-platform agent harness that persists specs, tasks, PRDs, workflow gates, workspace journals, and platform-aware generated files in the repository.
- Trellis sources emphasize:
  - scoped specs instead of monolithic prompt files;
  - task-centered workflow under `.trellis/tasks/`;
  - workspace journals for session continuity;
  - context injection from task-specific files;
  - multi-platform adapters for Claude Code, Cursor, Codex, OpenCode, etc.
- OpenAI's harness engineering article argues for a short `AGENTS.md` as a map, a structured in-repository knowledge store as source of truth, progressive disclosure, validation/linters, and agent-readable execution plans/progress/decision logs.

### Codex official behavior

From the current Codex manual:

- Skills are reusable workflow packages with `SKILL.md`, optional references/scripts, and progressive disclosure.
- Skills should stay focused; descriptions drive implicit routing.
- Codex reads skills from repo/user/admin/system locations, including `$REPO_ROOT/.agents/skills` and `$HOME/.agents/skills`; distribution beyond local authoring should use plugins.
- Plugins are the installable distribution unit that can bundle skills, apps, MCP config, hooks, and assets.
- `AGENTS.md` is durable repo guidance and should point to deeper project docs when rules are too long.
- Hooks can enforce lifecycle checks, but repo-local hooks require trust review and should be introduced only after the file-based harness is stable.
- Subagents help with read-heavy parallel exploration and reduce context pollution, but Codex only spawns them when explicitly asked; the harness should support subagent context manifests but not depend on them.
- Memories are local recall, not the canonical source for rules or project facts.

### Scientific provenance

FAIR workflow / RO-Crate / W3C PROV literature supports these requirements:

- run provenance must record people/tools/entities/activities that produced outputs;
- prospective provenance: planned workflow, code, parameters, inputs;
- retrospective provenance: actual commands, timestamps, outputs, checksums, environment;
- manifests should be machine-actionable and minimal enough to be maintained;
- human-facing summaries should point to canonical structured metadata rather than duplicating it.

## 3. Design principles

1. **Harness first, skills second**  
   The project truth lives in `.project_os/` and root index files. Skills are just agent operating procedures.

2. **Short entry point, deep references**  
   `AGENTS.md` and `research-project-os/SKILL.md` should be maps. Detailed rules live in `.project_os/workflow.md`, `.project_os/spec/`, and skill `references/`.

3. **No second scientific plan**  
   For existing projects such as `pingtai_final_20260430`, the harness must reference existing authoritative plans; it must not invent a new method route or replace project-specific planning.

4. **Context manifests over whole-repo reading**  
   Agents should read only the task/workflow/spec/run/result files listed in `context_manifest.jsonl`, plus required root entry points.

5. **Runtime pointers solve “continue”**  
   `.project_os/runtime/current_task`, `current_branch`, and `current_run` are the source for continuation, not chat memory.

6. **Run -> result -> accepted -> release is the scientific core**  
   Runs are provenance. Humans discover useful outputs through `RESULTS_INDEX.md`, `current/`, and release manifests.

7. **Deterministic CLI for repeatable checks**  
   Agent prose should not be the only enforcement layer. Use Python scripts for init, schema validation, index refresh, run manifest checks, and inventory.

8. **Adapter boundary from day one**  
   Core `.project_os/` files are platform-neutral. Codex/Claude/OpenCode adapters only generate small platform files or instructions.

## 4. Target per-project harness layout

```text
.project_os/
├── workflow.md
├── config.yaml
├── spec/
│   ├── project_rules.md
│   ├── task_tree.md
│   ├── context_manifest.md
│   ├── run_provenance.md
│   ├── result_curation.md
│   ├── data_assets.md
│   ├── user_profile.md
│   └── release_packaging.md
├── tasks/
│   └── <task_id>/
│       ├── task.json
│       ├── objective.md
│       ├── context.md
│       ├── context_manifest.jsonl
│       ├── research/
│       ├── decisions.md
│       ├── run_links.tsv
│       ├── result_links.tsv
│       └── handoff.md
├── runtime/
│   ├── current_task
│   ├── current_branch
│   ├── current_run
│   └── sessions/
├── journals/
├── indexes/
│   ├── tasks.tsv
│   ├── branches.tsv
│   ├── runs.tsv
│   ├── results.tsv
│   └── assets.tsv
└── exports/
    ├── task_graph.html
    ├── run_graph.html
    └── project_dashboard.html
```

Root human entry points remain:

```text
PROJECT_STATE.md
DATA_ASSETS.md
RESULTS_INDEX.md
RUNS_INDEX.tsv
DECISIONS.md
current/
runs/ or analysis_runs/
release/
```

`.project_os/` is the agent workspace and structured memory. It does not replace the root human-facing files.

## 5. Skill-suite layout in codex-skills-hub

Create authored skills under:

```text
/home/teng/claude_code/codex-skills-hub/skills/local/
```

Recommended first package:

```text
skills/local/research-project-os/
├── SKILL.md
├── references/
│   ├── harness_contract.md
│   ├── workflow_phases.md
│   ├── project_adoption.md
│   ├── task_schema.md
│   ├── context_manifest_schema.md
│   ├── run_manifest_schema.md
│   ├── result_index_schema.md
│   ├── data_asset_schema.md
│   ├── adapter_policy.md
│   └── safety_and_boundaries.md
├── templates/
│   └── project_os/
│       ├── workflow.md
│       ├── config.yaml
│       ├── spec/*.md
│       ├── tasks/example_task/*
│       └── runtime/.gitkeep
└── scripts/
    ├── project_os.py
    ├── validate_project_os.py
    ├── init_project_os.py
    ├── refresh_indexes.py
    ├── create_task.py
    ├── create_run.py
    ├── close_run.py
    ├── register_result.py
    └── promote_result.py
```

Then split only when the monolithic router becomes crowded:

```text
project-os-intake
project-os-task
project-os-run
project-os-result
project-os-data
project-os-release
project-os-profile
```

The first version should not create seven large skills immediately. Implement one thin router skill plus references/scripts; split after real-project smoke tests reveal stable boundaries.

## 6. Core workflow phases

The harness workflow should support scientific projects rather than Trellis' pure software loop:

```text
Intake -> Plan -> Research -> Run -> Evaluate -> Promote -> Archive -> Release
```

Phase duties:

| Phase | Agent action | Required files |
|---|---|---|
| Intake | detect project, read state, inventory existing docs/assets/runs | `PROJECT_STATE.md`, `.project_os/config.yaml`, `DATA_ASSETS.md` |
| Plan | select or create task/branch; do not override existing authoritative plan | `tasks/<id>/objective.md`, `task.json`, `context_manifest.jsonl` |
| Research | collect literature/tool/method context; save reports | `tasks/<id>/research/`, `decisions.md` |
| Run | create timestamped run and structured provenance | `RUN_MANIFEST.json`, `runs.tsv`, `RUNS_INDEX.tsv` |
| Evaluate | compare outputs, record metrics/caveats | run report, `result_links.tsv` |
| Promote | explicit user-approved accepted/current result | `RESULTS_INDEX.md`, `current/`, promotions log |
| Archive | mark superseded/legacy without deleting | `results.tsv`, `DECISIONS.md` |
| Release | package accepted files with manifest/checksums | `release/<release_id>/MANIFEST.tsv` |

## 7. Minimal schemas to implement first

### `task.json`

```json
{
  "task_id": "20260619_nmr_gcf_poc",
  "title": "NMR-GCF POC",
  "status": "active",
  "kind": "analysis",
  "parent_task_id": null,
  "branch_id": "main",
  "created_at": "2026-06-19T20:00:00+08:00",
  "updated_at": "2026-06-19T20:00:00+08:00",
  "owner": "teng",
  "stage": "Run",
  "objective_file": "objective.md",
  "context_manifest": "context_manifest.jsonl",
  "notes": ""
}
```

### `context_manifest.jsonl`

One JSON object per line:

```jsonl
{"type":"state","path":"PROJECT_STATE.md","purpose":"current status","required":true}
{"type":"workflow","path":".project_os/workflow.md","purpose":"phase rules","required":true}
{"type":"spec","path":"docs/CURRENT_NMR_GCF_OPTIMIZATION_PLAN.md","purpose":"authoritative method plan","required":true}
{"type":"run","path":"runs/20260619_x/RUN_MANIFEST.json","purpose":"provenance","required":false}
{"type":"result","path":"RESULTS_INDEX.md","purpose":"accepted outputs","required":false}
```

### `RUN_MANIFEST.json`

```json
{
  "run_id": "20260619_200000__task_slug",
  "task_id": "20260619_nmr_gcf_poc",
  "status": "active",
  "created_at": "2026-06-19T20:00:00+08:00",
  "closed_at": null,
  "code_ref": {"git_commit": null, "dirty": true},
  "environment": {"python": null, "conda_env": null, "packages": {}},
  "inputs": [],
  "parameters": {},
  "commands": [],
  "outputs": [],
  "metrics": {},
  "result_status": "draft",
  "promoted_to": [],
  "notes": ""
}
```

### `results.tsv`

```text
result_id	task_id	run_id	status	type	path	title	created_at	accepted_at	replaced_by	notes
```

Statuses:

```text
draft, candidate, accepted, current, superseded, legacy, release
```

### `assets.tsv`

```text
asset_id	kind	path	version	source_url	source_note	immutable	status	registered_at	notes
```

## 8. CLI commands to implement

Use one `project_os.py` entry point first:

```bash
python scripts/project_os.py init --root <project>
python scripts/project_os.py status --root <project>
python scripts/project_os.py validate --root <project>
python scripts/project_os.py create-task --root <project> --title "..." --kind analysis
python scripts/project_os.py set-current-task --root <project> --task-id <id>
python scripts/project_os.py create-run --root <project> --task-id <id> --slug "..."
python scripts/project_os.py close-run --root <project> --run-id <id> --status completed
python scripts/project_os.py register-result --root <project> --run-id <id> --path <path> --status candidate
python scripts/project_os.py promote-result --root <project> --result-id <id> --to current/<path>
python scripts/project_os.py refresh-indexes --root <project>
```

Implementation rules:

- fail fast on malformed JSON/TSV;
- no silent default provenance;
- no destructive cleanup command in v1;
- `promote-result` requires explicit argument and should report what it will replace;
- validation must check runtime pointers, index rows, required root docs, and orphaned run/result links.

## 9. Adapter strategy

### Codex

- Skills live in `skills/local/` in the hub, then installed or mirrored to `~/.codex/skills` / `~/.agents/skills`.
- Optional repo-scoped skills can live in `$REPO_ROOT/.agents/skills`.
- Optional project config/agents can live in `.codex/`, but should be generated only after the core harness works.
- Do not rely on Codex memories as project truth.
- Plugins are a later distribution target when the workflow is stable.

### Claude Code

- Generate a small `CLAUDE.md` / `.claude/skills` adapter that points to `.project_os/workflow.md` and the same task/context manifests.
- Do not fork the source of truth into Claude-only files.

### OpenCode / Cursor / other tools

- Generate only platform entry files that say:
  1. read `.project_os/workflow.md`;
  2. read runtime pointers;
  3. load `context_manifest.jsonl`;
  4. update handoff/state/index files before stopping.

## 10. Implementation sequence

### Milestone 0 — specification freeze

Outputs:

- this plan;
- initial schema reference files;
- decision: `.project_os/` is canonical harness workspace, `skills/local/research-project-os/` is the operating interface.

Acceptance:

- no code yet required;
- agreed folder names and boundaries.

### Milestone 1 — harness templates and validator

Create:

```text
skills/local/research-project-os/templates/project_os/
skills/local/research-project-os/references/*.md
skills/local/research-project-os/scripts/validate_project_os.py
```

Acceptance:

- a blank project can be initialized in dry-run mode;
- validator catches missing `workflow.md`, missing runtime pointer targets, malformed JSONL/TSV, and missing root human entry points.

### Milestone 2 — CLI vertical slice

Implement:

```text
init
status
create-task
set-current-task
create-run
register-result
refresh-indexes
validate
```

Acceptance:

- creates `.project_os/`;
- creates one task;
- creates one run manifest;
- links a candidate result;
- updates `.project_os/indexes/*.tsv`;
- does not promote anything automatically.

### Milestone 3 — router skill

Create concise `research-project-os/SKILL.md`:

- detect `.project_os/`;
- read `workflow.md`;
- read runtime pointers;
- read task `context_manifest.jsonl`;
- route to existing project-state/project-flow/version skills only as helpers;
- call CLI for deterministic operations;
- update handoff and `PROJECT_STATE.md`.

Acceptance:

- description triggers on `research-project-os`, `project harness`, `项目工作台`, `run provenance`, `结果版本管理`, `继续当前任务`;
- body stays short and delegates detail to references.

### Milestone 4 — first real-project adoption

Use `pingtai_final_20260430` as a smoke test **without replacing its current NMR-GCF plan**.

Adoption rules:

- `.project_os/spec/project_rules.md` points to existing `AGENTS.md`.
- `.project_os/spec/current_plan.md` points to `docs/CURRENT_NMR_GCF_OPTIMIZATION_PLAN.md`.
- task `20260619_nmr_gcf_poc` points to existing M0-M9 plan and detailed execution manual.
- runtime `current_task` points to this task.
- no old run cleanup; only inventory/dry-run.

Acceptance:

- `continue` can resolve current task/run from files;
- validator passes;
- `PROJECT_STATE.md` remains thin and points to `.project_os/`.

### Milestone 5 — result promotion and release packaging

Implement:

```text
promote-result
build-release
checksum manifest
release README template
```

Acceptance:

- promotion requires explicit user approval;
- accepted outputs are discoverable from `RESULTS_INDEX.md` and `current/`;
- release folder has `MANIFEST.tsv` and checksums.

### Milestone 6 — split subskills only after stable use

Split out subskills if the router grows too large:

- `project-os-run`
- `project-os-result`
- `project-os-data`
- `project-os-release`
- `project-os-profile`

Acceptance:

- each subskill has a narrow trigger and no duplicate schemas.

### Milestone 7 — plugin packaging

Only after at least one real project validates the workflow:

```text
research-project-os-plugin/
├── .codex-plugin/plugin.json
├── skills/
├── assets/
└── hooks/
```

Acceptance:

- local plugin marketplace works;
- no hook is enabled by default unless trusted and documented.

## 11. Work commands in codex-skills-hub

Initial repository workflow:

```bash
cd /home/teng/claude_code/codex-skills-hub
git status --short
python3 scripts/validate_skills.py
python3 scripts/sync_skills.py --dry-run
```

Create first skill:

```bash
python3 scripts/new_skill.py research-project-os \
  --description "Operate a repository-local research project harness under .project_os for long-running research projects. Use when the user asks for project harness, research-project-os, 项目工作台, 长期科研项目管理, run provenance, RESULTS_INDEX, DATA_ASSETS, current_task, continue 当前任务, or result promotion/release workflow." \
  --apply
```

Then add references/templates/scripts manually and run:

```bash
python3 scripts/validate_skills.py
python3 scripts/sync_skills.py --dry-run
python3 scripts/sync_skills.py --apply
```

Commit/push only after review:

```bash
python3 scripts/sync_skills.py --apply --commit --push
```

## 12. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Harness becomes another giant prompt system | Keep `SKILL.md` and `AGENTS.md` as maps; move schemas to references and enforcement to CLI |
| Conflicts with project-specific plans | Harness stores pointers and provenance; it must not invent method plans |
| Too many files for small projects | `init` supports levels: `basic`, `research`, `publication` |
| Context manifest becomes stale | `validate` checks paths and required files; `refresh-indexes` updates derived indexes |
| Agent silently promotes bad result | promotion command requires explicit user approval and updates `RESULTS_INDEX.md` |
| Multi-platform files diverge | adapters are generated from `.project_os/config.yaml`; platform files are not canonical |
| User profile stores sensitive data | keep profile opt-in, local, low-sensitivity, and reviewable; never store secrets |

## 13. Immediate next step

Do not start with a full plugin or seven subskills.

Start with:

1. `skills/local/research-project-os/SKILL.md`;
2. `references/` schemas and policies;
3. `templates/project_os/`;
4. `scripts/project_os.py` with `init/status/validate/create-task/create-run/register-result/refresh-indexes`;
5. one smoke adoption in `pingtai_final_20260430`.

This gives a real harness, not a giant skill, while keeping the implementation small enough to validate quickly.

