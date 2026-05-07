# PROJECT_STATE

## Project Summary
Personal GitHub-backed skill library for Codex/agent skills. It mirrors global and workspace skills, stores locally authored skills, and provides safe sync/validation automation.

## Current Goal
Create a well-organized repository that can store current skills and automatically upload newly created or modified skills to GitHub.

## Current Status
- Science/bioinformatics batch A is installed globally for Codex under ~/.codex/skills and mirrored into skills/global/.
- Exact Chinese trigger phrases for literature search and multi-paper idea synthesis have been added to relevant SKILL.md descriptions.
- README.md now contains a common Chinese prompt routing table for references, literature search, multi-paper synthesis, paper methods, and paper reproduction.

## Key Paths
- docs/SCIENCE_BIOINFO_SKILL_CANDIDATES.md
- README.md
- skills/global/tooluniverse/SKILL.md
- skills/global/tooluniverse-literature-deep-research/SKILL.md
- skills/global/pubmed-database/SKILL.md
- skills/global/systematic-literature-review/SKILL.md
- skills/global/paper-context-resolver/SKILL.md
- skills/global/env-and-assets-bootstrap/SKILL.md
- skills/global/repo-intake-and-plan/SKILL.md
- skills/global/minimal-run-and-audit/SKILL.md
- skills/global/implement-paper/SKILL.md
- registry/SKILL_INVENTORY.tsv
- registry/skills.json

## Decisions
- Keep planning-with-files as the task kernel; science/bioinformatics skills are phase tools, not replacements.
- Install a broad but bounded batch A first: literature, PubMed, paper reading/reproduction, core bioinformatics, critique, visualization, slides.
- Copy npx-installed skills from ~/.agents/skills into ~/.codex/skills because this Codex environment loads skills from ~/.codex/skills.
- Patch third-party SKILL.md descriptions with Chinese trigger phrases so automatic triggering works for Chinese prompts.
- Leave single-cell, metabolomics, comparative genomics, CRISPR, drug-target, peer review, and multi-dimensional paper reader for optional batch B.

## Recent Changes
- Patched descriptions for auto-deep-research, research-orchestrator, tooluniverse-literature-deep-research, pubmed-database, systematic-literature-review, scientific-critical-thinking, paper-context-resolver, and read-arxiv-paper with exact Chinese trigger phrases such as 寻找参考文献、搜索文献、根据这几篇文献有什么想法、参考文献的做法.
- Ran scripts/sync_skills.py --apply to mirror the trigger phrase updates into skills/global.
- Ran scripts/validate_skills.py after trigger updates.

## Open Problems
- Codex should be restarted to load the new skills in the current session skill list.
- Validation warnings remain credential-word heuristics; no forbidden secret-like files were detected.
- The machine still has git global proxy entries pointing at 127.0.0.1:7890; future npx skills add may need GIT_CONFIG_GLOBAL=/dev/null unless the proxy config is fixed.

## Next Step
- Commit and push the trigger phrase updates.
- After Codex restart, test prompts: 寻找参考文献、搜索文献、根据这几篇文献有什么想法、参考文献的做法、这个论文代码怎么复现.

## Resume Prompt
Exact Chinese literature/reference trigger phrases have been added and synced. Continue by committing and pushing, then ask the user to restart Codex before testing automatic skill routing.
