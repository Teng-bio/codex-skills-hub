# PROJECT_STATE

## Project Summary
Personal GitHub-backed skill library for Codex/agent skills. It mirrors global and workspace skills, stores locally authored skills, and provides safe sync/validation automation.

## Current Goal
Maintain a structured local skill library for research workflows, with a clear two-lane bioinformatics architecture: evidence/analysis orchestration and manuscript-writing support.

## Current Status
- 2026-06-19: Committed and pushed `research-project-os` to GitHub at commit `b7d5077` (`feat(skills): add research project os harness`).
- 2026-06-19: Installed `research-project-os` into `/home/teng/.codex/skills/research-project-os` and refreshed the hub mirror, so fresh Codex sessions should be able to discover it after skill metadata reload.
- 2026-06-19: Real-project adoption smoke test completed in `/home/teng/pingtai_final_20260430`: `.project_os/` was initialized with an active task `20260619_nmr_gcf_poc`, context manifest linked to the existing NMR-GCF planning hierarchy, indexes were refreshed, and `project_os.py validate` passed with 0 errors / 0 warnings.
- 2026-06-19: Implemented `skills/local/research-project-os/` Milestone 1: concise router `SKILL.md`, schema/policy references, `.project_os` templates, and stdlib Python CLI covering init/status/validate/create-task/set-current-task/create-run/close-run/register-result/promote-result/refresh-indexes. Smoke test on a temporary project passed with 0 validation errors and 0 warnings.
- 2026-06-19: Added a researched implementation plan for `research-project-os` as a Trellis-style repository-local harness plus small skill suite, rather than one oversized skill. The plan incorporates Trellis workflow/task/runtime ideas, Codex official skill/plugin/AGENTS/hooks/subagent boundaries, and scientific run provenance / FAIR / RO-Crate principles.
- Hub validation reports 68 skills, 0 errors, and 11 known credential-word warnings from existing mirrored skills only.
- `nature-skills` is clean and is no longer used as the implementation target for this refactor.
- Natural-language auto routing is implemented as `skills/local/bio-research-auto-router/`.
- Bioinformatics evidence line is implemented as `skills/local/bioinfo-evidence-orchestrator/`.
- Bioinformatics writing line is implemented as:
  - `bio-paper-writing`
  - `bio-results-writing`
  - `bio-methods-writing`
  - `bio-polishing`
  - `bio-reviewer-response`
  - `bio-data-code-availability`
  - `bio-paper2ppt`
- Added natural-language routing so users can write vague prompts without naming skills.
- The bio routing/writing skills have also been installed to `/home/teng/.codex/skills` and `/home/teng/.agents/skills` for future-session auto-triggering.
- Registry files have been refreshed with `python3 scripts/sync_skills.py --apply`.

## Key Paths
- /home/teng/.codex/skills/research-project-os/
- skills/global/research-project-os/
- docs/RESEARCH_PROJECT_OS_HARNESS_IMPLEMENTATION_PLAN.md
- skills/local/research-project-os/SKILL.md
- skills/local/research-project-os/references/
- skills/local/research-project-os/templates/project_os/
- skills/local/research-project-os/scripts/project_os.py
- docs/BIOINFO_WRITING_REFACTOR_PLAN.md
- docs/SKILL_ROUTING_MATRIX.md
- task_plan.md
- findings.md
- progress.md
- skills/local/bio-research-auto-router/SKILL.md
- skills/local/bioinfo-evidence-orchestrator/SKILL.md
- skills/local/bio-paper-writing/SKILL.md
- skills/local/bio-results-writing/SKILL.md
- skills/local/bio-methods-writing/SKILL.md
- skills/local/bio-polishing/SKILL.md
- skills/local/bio-reviewer-response/SKILL.md
- skills/local/bio-data-code-availability/SKILL.md
- skills/local/bio-paper2ppt/SKILL.md
- registry/SKILL_INVENTORY.tsv
- registry/skills.json

## Decisions
- `research-project-os` should be implemented as a repository-local harness/workspace under `.project_os/` plus a concise `research-project-os` router skill and deterministic CLI/scripts; project facts belong in `.project_os/` and root human entry files, not in a giant `SKILL.md`.
- Initial implementation should start with one thin router skill plus references/templates/scripts, then split into `project-os-run/result/data/release/profile` subskills only after real-project smoke tests stabilize the boundaries.
- 生信 Agent 负责事实和证据，不写论文。
- 写作 Skill 负责表达和投稿材料，不跑分析。
- `EVIDENCE_PACK.md` is the handoff contract between the evidence line and writing line.
- Existing `tooluniverse-*`, `pubmed-database`, `literature-method-data-miner`, `scientific-critical-thinking`, visualization, and reproduction skills remain the analysis/database layer; new bio skills do not duplicate them.
- Writing tasks are split by product type to avoid one oversized manuscript-writing skill.

## Recent Changes
- Installed `research-project-os` to `/home/teng/.codex/skills/` and re-ran `scripts/sync_skills.py --apply`, adding the global mirror entry under `skills/global/research-project-os/`.
- Fixed `scripts/sync_skills.py` to generate `registry/SKILL_INVENTORY.tsv` with LF line endings instead of csv default CRLF, removing `git diff --check` trailing-whitespace warnings from generated TSV diffs.
- Real-adopted `research-project-os` into `/home/teng/pingtai_final_20260430` without replacing that project's `AGENTS.md`, `PROJECT_STATE.md`, or authoritative NMR-GCF plans; the project harness now has runtime pointers, task context, `RUNS_INDEX.tsv`, and `RESULTS_INDEX.md`.
- Created `research-project-os` local skill with 44 files and refreshed `registry/SKILL_INVENTORY.tsv` / `registry/skills.json` via `python3 scripts/sync_skills.py --apply`.
- Added README and `docs/SKILL_ROUTING_MATRIX.md` entries for `research-project-os` routing and its boundary with `planning-with-files`, `project-state-maintainer`, `project-flow-guard`, and `project-version-curator`.
- Added `docs/RESEARCH_PROJECT_OS_HARNESS_IMPLEMENTATION_PLAN.md`, covering target `.project_os/` layout, schemas, CLI commands, Codex/Claude/OpenCode adapter policy, implementation milestones, and the planned workflow in `/home/teng/claude_code/codex-skills-hub`.
- Added planning documents for the bioinformatics/writing refactor.
- Added `bioinfo-evidence-orchestrator` plus an evidence-pack template.
- Added `bio-paper-writing` plus references for evidence-pack intake, article types, and section workflows.
- Added six specialized bio writing skills with one-level references where useful.
- Added `bio-research-auto-router` for vague natural-language task selection.
- Installed the bio skill suite into global user skill directories for automatic selection in future sessions.
- Updated `README.md` so the GitHub landing page documents the bio auto-router, evidence line, writing line, and natural-language routing examples.
- Fixed `scripts/new_skill.py` to use the running Python interpreter instead of assuming `python` exists.
- Clarified that auto-upload requires either explicit `sync_skills.py --apply --commit --push` or an installed user service.
- Updated planning/progress/findings files.
- Ran validation, dry-run sync, apply sync, second validation, and registry grep checks.

## Open Problems
- `research-project-os` is implemented, installed to the global Codex skill directory, smoke-tested, committed, and pushed; it is not yet packaged as a plugin.
- No real-project smoke test has yet been run through the full `EVIDENCE_PACK.md -> writing skill` handoff.
- The current active Codex session's listed skills may remain stale until a fresh session reloads local/global skill metadata.
- The background auto-upload service is documented but not currently enabled by default.

## Next Step
- Start a fresh Codex session later to confirm `research-project-os` appears in the available skill list; plugin packaging remains optional future work.
- Commit the auto-routing enhancement if accepted.
- In a fresh Codex session, test natural prompts for boundary routing:
  - “这些结果能不能写文章” -> `bio-research-auto-router` -> `bioinfo-evidence-orchestrator`
  - “帮我整理这个GSE数据写论文前的证据包” -> `bioinfo-evidence-orchestrator`
  - “根据这个EVIDENCE_PACK写abstract” -> `bio-paper-writing`
  - “根据这些图写Results” -> `bio-results-writing`
  - “写Methods，材料如下” -> `bio-methods-writing`
  - “审稿人质疑batch effect怎么回” -> `bio-reviewer-response`

## Resume Prompt
Bioinformatics skill refactor is implemented in `codex-skills-hub`: natural-language auto-router, evidence orchestrator, and seven writing-line skills. `research-project-os` Milestone 1 is implemented under `skills/local/research-project-os/`, installed to `/home/teng/.codex/skills/research-project-os`, mirrored under `skills/global/research-project-os/`, smoke-tested on temp and real projects, and pushed to GitHub at commit `b7d5077`. Next step is verifying in a fresh session that the skill auto-loads.
