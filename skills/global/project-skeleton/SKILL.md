---
name: project-skeleton
description: Thin Chinese trigger/alias for bootstrapping or resuming a repository project workflow skeleton. Use when the user says 项目骨架, 新项目骨架, 搭项目骨架, 初始化项目骨架, 项目工作流骨架, 研究项目骨架, 科研项目骨架, 开工, 继续项目, or asks to scaffold a durable research/project harness.
---

# project-skeleton

Use this as a short entry point for `research-project-os`.

## Route

1. Detect the project root.
2. If `.project_os/` is missing, use the `research-project-os` skill and run its `project_os.py new-project` flow as a dry-run first unless the user explicitly asked to apply changes.
3. If `.project_os/` exists, use the `research-project-os` skill and run its `project_os.py start` flow to load project state, active task, active run, and context manifest.
4. Keep this skill thin: do not duplicate the harness contract; defer to `research-project-os` references and scripts.

## Preferred user-facing phrases

Map these to the flow above:

- `新项目骨架` / `搭项目骨架` / `初始化项目骨架` -> bootstrap a new `.project_os/` harness.
- `项目骨架` / `项目工作流骨架` -> auto-detect bootstrap vs resume.
- `开工` / `继续项目` -> resume existing `.project_os/` state.
