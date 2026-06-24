---
name: project-skeleton
description: Thin Chinese trigger/alias for bootstrapping or resuming a `.project_os/` research project harness. Use when the user says 项目骨架, 新项目骨架, 搭项目骨架, 初始化项目骨架, 项目工作流骨架, 研究项目骨架, 科研项目骨架, 开工, 继续项目, 继续下一步, 大项目, 逐步推进, 制定计划, 拆解任务, 当前进展, 恢复上下文, task_plan.md, findings.md, progress.md, 项目状态, 写一个项目状态文档, 开始分析, 先跑, 先画, 绘图, or 画图 in a durable project; then defer to research-project-os.
---

# project-skeleton

Use this as a short entry point for `research-project-os`.

If `.project_os/` exists in the current project or a parent directory, never create `task_plan.md` / `findings.md` / `progress.md` as the primary memory and never start a parallel project-state workflow. Resume the harness first.

## Route

1. Detect the project root.
2. For a machine-readable plan, use `project_os.py route --root <project> "项目骨架"` or `project_os.py route --root <project> "开工"` first.
3. If `.project_os/` is missing, use the `research-project-os` skill and run its `project_os.py new-project` flow as a dry-run first unless the user explicitly asked to apply changes.
4. If `.project_os/` exists, use the `research-project-os` skill and run its `project_os.py start` flow to load project state, optional `current_session`, active branch/task/run, and context manifest.
5. Keep this skill thin: do not duplicate the harness contract; defer to `research-project-os` references and scripts.

## Preferred user-facing phrases

Map these to the flow above:

- `新项目骨架` / `搭项目骨架` / `初始化项目骨架` -> bootstrap a new `.project_os/` harness.
- `项目骨架` / `项目工作流骨架` -> auto-detect bootstrap vs resume.
- `开工` / `继续项目` -> resume existing `.project_os/` state.
- `大项目` / `逐步推进` / `制定计划` / `拆解任务` / `task_plan.md` / `findings.md` / `progress.md` -> use `.project_os` branch/task/session state instead of the old planning-file kernel.
- `项目状态` / `写一个项目状态文档` / `更新项目状态文档` -> use `.project_os` status/summarize-state instead of a parallel project-state workflow.

## Router note

This is only the bootstrap/resume alias. Other short phrases such as `新建分支`, `新建会话`, `切会话`, `暂停会话`, `恢复会话`, `会话清理`, `开始运行`, `记录结果`, and `设为当前结果` should route through `research-project-os` and `references/short_trigger_router.md`.
