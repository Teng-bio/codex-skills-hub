# PROJECT_STATE

## Project Summary
Personal GitHub-backed skill library for Codex/agent skills. It mirrors global and workspace skills, stores locally authored skills, and provides safe sync/validation automation.

## Current Goal
Create a well-organized repository that can store current skills and automatically upload newly created or modified skills to GitHub.

## Current Status
- All SKILL.md files under ~/.codex/skills and ~/.agents/skills pass local frontmatter and description length validation.
- Hub validation reports 48 skills, 0 errors, and 11 known credential-word warnings only.
- The science/bioinformatics flow has been smoke-checked with codex exec --ephemeral; no skipped/invalid skill loading warning appeared.
- Chinese trigger descriptions are mirrored into .agents duplicates for the science suite, so either .codex or .agents source can route short Chinese prompts.

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
- Copied literature-method-data-miner into ~/.agents/skills so npx/global agent listing also sees it.
- Mirrored Chinese-trigger descriptions from ~/.codex/skills into duplicate ~/.agents/skills for 17 science/bioinformatics skills.
- Ran prompt-substring simulations for 文献是怎么做的, 寻找参考文献, 搜索文献, 参考文献的做法, 根据这几篇文献有什么想法, PubMed, RNA-seq, 系统发育, 基因富集, 科学绘图.
- Ran codex exec --ephemeral -C /home/teng/claude_code/codex-skills-hub 只输出 OK and confirmed no invalid SKILL.md warning appeared.

## Open Problems
- The current chat session skill list may still be stale; a fresh Codex session is needed for active skill list confirmation.
- Duplicate names exist across ~/.codex/skills and ~/.agents/skills by design after npx installation plus Codex copy; both copies are valid and now have matching trigger descriptions for the science suite.

## Next Step
- Commit and push the PROJECT_STATE update if desired.
- In a new Codex session, test natural prompts: 文献是怎么做的, 搜索文献, 根据这几篇文献有什么想法, RNA-seq差异表达怎么做, 系统发育分析.

## Resume Prompt
Skill startup validation passed: no invalid SKILL.md files, no >1024 descriptions, codex exec starts without skipped-skill warnings, and Chinese trigger routing simulations hit the intended skills. Continue with fresh-session prompt smoke tests if needed.
