# PROJECT_STATE

## Project Summary
Personal GitHub-backed skill library for Codex/agent skills. It mirrors global and workspace skills, stores locally authored skills, and provides safe sync/validation automation.

## Current Goal
Create a well-organized repository that can store current skills and automatically upload newly created or modified skills to GitHub.

## Current Status
- Fixed ToolUniverse SKILL.md loader error by shortening the description under both ~/.codex/skills/tooluniverse and ~/.agents/skills/tooluniverse to 450 characters.
- Synced the fixed ~/.codex skill into skills/global/tooluniverse and refreshed registry files.
- validate_skills.py now enforces the Codex 1024-character description limit.

## Key Paths
- skills/local/literature-method-data-miner/SKILL.md
- skills/local/literature-method-data-miner/references/output-template.md
- skills/global/literature-method-data-miner/SKILL.md
- README.md
- docs/SCIENCE_BIOINFO_SKILL_CANDIDATES.md
- registry/SKILL_INVENTORY.tsv
- registry/skills.json

## Decisions
- Treat 文献是怎么做的 as a high-level shorthand for extracting research methods, main-text data, figure/table data, appendix/supplement data, reproducibility details, and reusable ideas.
- If papers are not provided, literature-method-data-miner should route through auto-deep-research/pubmed/tooluniverse-literature-deep-research before extraction.
- Keep this as a lightweight router skill under skills/local, mirrored globally for Codex triggering.

## Recent Changes
- Patched /home/teng/.codex/skills/tooluniverse/SKILL.md and /home/teng/.agents/skills/tooluniverse/SKILL.md after Codex reported invalid description length.
- Ran scripts/sync_skills.py --apply and scripts/validate_skills.py; validation has 0 errors.
- Added MAX_DESCRIPTION_CHARS=1024 check to scripts/validate_skills.py to prevent future skipped-skill loader errors.

## Open Problems
- User should restart Codex once more to confirm the ToolUniverse skipped-skill warning is gone.
- Validation still has known credential-word warnings only; they are unrelated to the description-length loader error.

## Next Step
- Commit and push the ToolUniverse description-length fix and validation guard.
- After restart, verify no invalid SKILL.md warning appears and that tooluniverse loads normally.

## Resume Prompt
ToolUniverse description was shortened in both ~/.codex and ~/.agents, synced to the hub, and validation now checks the 1024-character limit. Commit/push, then ask the user to restart Codex to verify the warning is gone.
