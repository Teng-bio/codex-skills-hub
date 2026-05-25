# Task Plan: Bioinformatics Skill Library Refactor

## Goal
Create a clean two-lane skill architecture in `codex-skills-hub`: bioinformatics evidence orchestration plus manuscript-writing skills, reusing existing local/global skills instead of duplicating analysis tools.

## Current Phase
Auto-routing enhancement complete; ready for real-project smoke testing.

## Phases

### Phase 1: Planning documents
- [x] Write `docs/BIOINFO_WRITING_REFACTOR_PLAN.md`
- [x] Write `docs/SKILL_ROUTING_MATRIX.md`
- [x] Keep `nature-skills` clean
- **Status:** complete

### Phase 2: Evidence orchestrator skill
- [x] Create `skills/local/bioinfo-evidence-orchestrator/SKILL.md`
- [x] Add a minimal reference template for `EVIDENCE_PACK.md`
- [x] Validate with `scripts/validate_skills.py`
- [x] Refresh registry with `scripts/sync_skills.py --apply`
- **Status:** complete

### Phase 3: Bio manuscript writing router
- [x] Review orchestrator boundaries after validation
- [x] Create `skills/local/bio-paper-writing/SKILL.md`
- [x] Add references for evidence-pack input, article types, and section workflows
- **Status:** complete

### Phase 4: Specialized bio writing skills
- [x] Create `bio-results-writing`
- [x] Create `bio-methods-writing`
- [x] Create `bio-polishing`
- [x] Create `bio-reviewer-response`
- [x] Create `bio-data-code-availability`
- [x] Create `bio-paper2ppt`
- [x] Add one-level reference files where useful
- **Status:** complete

### Phase 5: Validation and registry sync
- [x] Run `python3 scripts/validate_skills.py`
- [x] Run `python3 scripts/sync_skills.py --dry-run`
- [x] Run `python3 scripts/sync_skills.py --apply`
- [x] Re-run `python3 scripts/validate_skills.py`
- [x] Check registry entries for all new `bio-*` skills
- **Status:** complete

## Decisions Made

| Decision | Rationale |
|---|---|
| Use `codex-skills-hub/skills/local` for authored skills | Hub operating model says new authored skills go under `skills/local/` |
| Keep `bioinfo-evidence-orchestrator` lightweight | Existing `tooluniverse-*`, PubMed, scientific-critical-thinking, and reproduction skills should do domain work |
| Use `EVIDENCE_PACK.md` as handoff contract | Keeps analysis and writing responsibilities separate |
| Create a separate writing line | User explicitly needs both the bioinfo agent and paper-writing skills without overlap |
| Split Results, Methods, polishing, reviewer response, availability, and PPT | These tasks have different failure modes and trigger phrases |
| Do not edit `nature-skills` during implementation | User asked to plan and refactor from `codex-skills-hub` first |

## Errors Encountered

| Error | Attempt | Resolution |
|---|---:|---|
| Earlier draft changes were made in `nature-skills` before planning was complete | 1 | Backed up to `/tmp/nature-skills-draft-backup-20260525-104128` and reverted `nature-skills` to clean status |
| `python scripts/validate_skills.py` failed because `python` is not installed | 1 | Re-ran with `python3 scripts/validate_skills.py`; validation passed with pre-existing warnings only |

### Phase 6: Natural-language auto routing
- [x] Create `bio-research-auto-router`
- [x] Add vague prompt mapping reference
- [x] Update routing documentation
- **Status:** complete

## Acceptance Summary

- 生信 Agent 线：`bioinfo-evidence-orchestrator` 只负责路由、证据整理和 `EVIDENCE_PACK.md`。
- 写作线：`bio-paper-writing` 与 6 个专项 skill 只负责 manuscript prose、润色、审稿回复、availability、PPT，不跑分析。
- Registry 已同步，验证为 0 errors；11 warnings 来自既有 global/local mirrored skills 的 credential-like word 检查，不是本轮新增 bio skills。
