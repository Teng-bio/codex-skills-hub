# PROJECT_STATE

## Project Summary
Personal GitHub-backed skill library for Codex/agent skills. It mirrors global and workspace skills, stores locally authored skills, and provides safe sync/validation automation.

## Current Goal
Maintain a structured local skill library for research workflows, with a clear two-lane bioinformatics architecture: evidence/analysis orchestration and manuscript-writing support.

## Current Status
- Hub validation reports 56 skills, 0 errors, and 11 known credential-word warnings from existing mirrored skills only.
- `nature-skills` is clean and is no longer used as the implementation target for this refactor.
- Bioinformatics evidence line is implemented as `skills/local/bioinfo-evidence-orchestrator/`.
- Bioinformatics writing line is implemented as:
  - `bio-paper-writing`
  - `bio-results-writing`
  - `bio-methods-writing`
  - `bio-polishing`
  - `bio-reviewer-response`
  - `bio-data-code-availability`
  - `bio-paper2ppt`
- Registry files have been refreshed with `python3 scripts/sync_skills.py --apply`.

## Key Paths
- docs/BIOINFO_WRITING_REFACTOR_PLAN.md
- docs/SKILL_ROUTING_MATRIX.md
- task_plan.md
- findings.md
- progress.md
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
- 生信 Agent 负责事实和证据，不写论文。
- 写作 Skill 负责表达和投稿材料，不跑分析。
- `EVIDENCE_PACK.md` is the handoff contract between the evidence line and writing line.
- Existing `tooluniverse-*`, `pubmed-database`, `literature-method-data-miner`, `scientific-critical-thinking`, visualization, and reproduction skills remain the analysis/database layer; new bio skills do not duplicate them.
- Writing tasks are split by product type to avoid one oversized manuscript-writing skill.

## Recent Changes
- Added planning documents for the bioinformatics/writing refactor.
- Added `bioinfo-evidence-orchestrator` plus an evidence-pack template.
- Added `bio-paper-writing` plus references for evidence-pack intake, article types, and section workflows.
- Added six specialized bio writing skills with one-level references where useful.
- Updated planning/progress/findings files.
- Ran validation, dry-run sync, apply sync, second validation, and registry grep checks.

## Open Problems
- No real-project smoke test has yet been run through the full `EVIDENCE_PACK.md -> writing skill` handoff.
- The current active Codex session's listed skills may remain stale until a fresh session reloads local/global skill metadata.
- Repository changes are not committed or pushed yet.

## Next Step
- Optionally commit and push the current refactor.
- In a fresh Codex session, test natural prompts for boundary routing:
  - “帮我整理这个GSE数据写论文前的证据包” -> `bioinfo-evidence-orchestrator`
  - “根据这个EVIDENCE_PACK写abstract” -> `bio-paper-writing`
  - “根据这些图写Results” -> `bio-results-writing`
  - “写Methods，材料如下” -> `bio-methods-writing`
  - “审稿人质疑batch effect怎么回” -> `bio-reviewer-response`

## Resume Prompt
Bioinformatics skill refactor is implemented in `codex-skills-hub`: evidence orchestrator plus seven writing-line skills. Validation and registry sync pass with 0 errors. Continue with real-project smoke testing or commit/push if requested.
