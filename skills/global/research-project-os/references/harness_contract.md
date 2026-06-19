# Harness contract

`research-project-os` is a repository-local harness for long-running research and analysis projects.

## Canonical layers

| Layer | Purpose | Canonical files |
|---|---|---|
| Human handoff | concise project status and entry points | `PROJECT_STATE.md`, `RESULTS_INDEX.md`, `DATA_ASSETS.md`, `RUNS_INDEX.tsv`, `DECISIONS.md` |
| Agent harness | workflow, task knowledge, runtime pointers, indexes | `.project_os/` |
| Run provenance | actual commands, inputs, parameters, environment, outputs | `runs/<run_id>/RUN_MANIFEST.json` or `analysis_runs/<run_id>/RUN_MANIFEST.json` |
| Generated display | dashboards/HTML/SQLite exports | `.project_os/exports/` |

Generated display files are never the source of truth unless a project explicitly changes this policy.

## Required invariant

A future agent must be able to answer these questions from files without chat history:

1. What is the current active task?
2. Which context files should be loaded for that task?
3. Which run is active or most recent?
4. Which results are draft, candidate, accepted, current, legacy, or release?
5. Which data assets and reference resources were used?
6. What must be done next?

## What the harness must not do

- Do not replace a project-specific scientific, analysis, or engineering plan.
- Do not silently promote outputs to accepted/current.
- Do not treat old filenames such as `final` as proof of acceptance.
- Do not use chat memory as the only record of task state.
