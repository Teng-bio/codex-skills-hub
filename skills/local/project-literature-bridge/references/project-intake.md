# Project intake

## Read order

Prefer authoritative project reports and state files:

1. `AGENTS.md`
2. `PROJECT_STATE.md`
3. `DATA_ASSETS.md`
4. `RESULTS_INDEX.md`
5. `DECISIONS.md`
6. `RUNS_INDEX.tsv`
7. `docs/README.md`
8. `docs/PROJECT_COMPLETE_GUIDE.md`
9. Current plan files named inside `PROJECT_STATE.md` or `docs/README.md`
10. Current task context under `.project_os/` when present

## Extraction targets

Extract only these first:

- project objective
- current branch/task/focus
- current technical route
- key problems and blockers
- current accepted/candidate/legacy results
- external literature/data paths
- decisions that constrain future work
- next steps stated by the project

## Boundaries

- Do not infer a new project plan if the project already has an authoritative plan.
- Do not treat old archive files as current unless the state file says so.
- Do not use filenames such as `final`, `latest`, or `current` as proof of acceptance without index/state support.
- Do not crawl the whole source tree unless asked for code audit.

## Output blocks for project notes

Use these blocks in `01-项目总览/`:

```md
## 当前结论

## 依据来源

## 当前问题

## 相关论文

## 可执行下一步

## 不确定点
```

