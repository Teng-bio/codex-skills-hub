---
name: research-project-os
description: Operate and bootstrap a repository-local research project harness under `.project_os/` for long-running scientific or analysis projects. Use when the user asks for research-project-os, project harness, 项目骨架, 新项目骨架, 搭项目骨架, 初始化项目骨架, 研究项目骨架, 科研项目骨架, 项目工作流骨架, 项目工作台, 长期科研项目管理, run provenance, RESULTS_INDEX, DATA_ASSETS, current_task, continue 当前任务, task/runtime pointers, result promotion, or release workflow.
---

# research-project-os

Use this skill to operate a **project-local harness**, not to create a second scientific plan.

Core split:

```text
.project_os/                 # agent harness, runtime pointers, task/run/result indexes
PROJECT_STATE.md             # thin human handoff
DATA_ASSETS.md               # data/source registry
RUNS_INDEX.tsv               # human-facing run index
RESULTS_INDEX.md             # accepted/candidate/legacy result entry point
DECISIONS.md                 # durable decisions
```

## Startup

1. Detect the project root.
2. Read `PROJECT_STATE.md` when present.
3. If `.project_os/` exists, read:
   - `.project_os/workflow.md`
   - `.project_os/runtime/current_task`
   - the active task `context_manifest.jsonl`
4. Load only files listed in the context manifest unless the user asks for broader inventory.
5. Use `scripts/project_os.py` for deterministic operations.

## Core commands

From this skill directory:

```bash
python scripts/project_os.py new-project --root <project> --title "..." --profile research --platforms codex --apply
python scripts/project_os.py init --root <project> --apply
python scripts/project_os.py start --root <project>
python scripts/project_os.py status --root <project>
python scripts/project_os.py doctor --root <project>
python scripts/project_os.py install-adapters --root <project> --platforms codex --apply
python scripts/project_os.py validate --root <project>
python scripts/project_os.py create-task --root <project> --title "..." --kind analysis --set-current
python scripts/project_os.py create-run --root <project> --task-id <task_id> --slug "..."
python scripts/project_os.py register-result --root <project> --run-id <run_id> --path <path> --status candidate
python scripts/project_os.py refresh-indexes --root <project>
```

Use `new-project` or `init` without `--apply` first when adopting an unfamiliar project.

## Project skeleton entry

When triggered by `项目骨架`, `新项目骨架`, or `搭项目骨架`:

- If `.project_os/` is absent, run `new-project` as a dry-run first and ask before applying unless the user clearly requested changes.
- If `.project_os/` exists, run `start` and resume from the active task/run.
- Treat `project_os.py` as the deterministic backend; users do not need to remember Python commands.

## Operating rules

- Treat `.project_os/` as the agent workspace and runtime source of truth.
- Treat root Markdown/TSV/JSON files as the human-readable project entry points.
- Runs are provenance, not the place humans should search manually for final results.
- Promotion to `current/` or release requires explicit user approval.
- Do not invent or replace domain plans. Link existing authoritative plans from task context manifests.
- Do not move, delete, quarantine, or rewrite historical runs without a dry-run plan and user approval.
- Keep `PROJECT_STATE.md` thin; put task/run/result detail in `.project_os/` indexes and task folders.

## References

Read only what the current task needs:

- `references/harness_contract.md` for the file contract.
- `references/workflow_phases.md` for Intake→Release phases.
- `references/project_adoption.md` for adding `.project_os/` to an existing project.
- `references/context_manifest_schema.md`, `task_schema.md`, `run_manifest_schema.md`, `result_index_schema.md`, and `data_asset_schema.md` for schemas.
- `references/adapter_policy.md` for Codex/Claude/OpenCode boundary rules.
- `references/safety_and_boundaries.md` for non-destructive operation rules.
