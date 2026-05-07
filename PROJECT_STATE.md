# PROJECT_STATE

## Project Summary
Personal GitHub-backed skill library for Codex/agent skills. It mirrors global and workspace skills, stores locally authored skills, and provides safe sync/validation automation.

## Current Goal
Create a well-organized repository that can store current skills and automatically upload newly created or modified skills to GitHub.

## Current Status
- planning-with-files is global and mirrored into skills/global/planning-with-files/.
- Science/bioinformatics suite is installed and documented.
- New local/global skill literature-method-data-miner now captures short prompts like 文献是怎么做的 and maps them to method/data/supplement extraction workflows.

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
- Created literature-method-data-miner under skills/local and installed it globally under ~/.codex/skills.
- Added an output template for paper list, method/data matrix, supplement checklist, and cross-paper synthesis.
- Updated README.md and docs/SCIENCE_BIOINFO_SKILL_CANDIDATES.md to document the shorthand prompt routing.
- Ran scripts/sync_skills.py --apply and scripts/validate_skills.py.

## Open Problems
- Current Codex session must be restarted before literature-method-data-miner appears in the active skill list.
- Need run smoke prompts after restart: 文献是怎么做的, 这篇文献怎么做的, 参考文献的做法, 从文献收集正文和附录数据.

## Next Step
- Commit and push literature-method-data-miner plus docs/registry updates.
- After restart, test whether short Chinese prompts trigger literature-method-data-miner automatically.

## Resume Prompt
literature-method-data-miner has been created to interpret 文献是怎么做的 as method/data/supplement extraction from provided or discovered papers. Commit and push, then restart Codex and smoke-test the shorthand prompts.
