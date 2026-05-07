# PROJECT_STATE

## Project Summary
Personal GitHub-backed skill library for Codex/agent skills. It mirrors global and workspace skills, stores locally authored skills, and provides safe sync/validation automation.

## Current Goal
Create a well-organized repository that can store current skills and automatically upload newly created or modified skills to GitHub.

## Current Status
- planning-with-files is global and mirrored into skills/global/planning-with-files/.
- Science/bioinformatics batch A is installed globally for Codex under ~/.codex/skills and mirrored into skills/global/.
- The batch covers ToolUniverse life-science routing, literature deep research, PubMed, systematic reviews, arXiv reading, paper reproduction, RNA-seq, phylogenetics, enrichment, scientific critique, visualization, and slides.
- README.md now documents the science/bioinformatics skills and trigger phrases.
- docs/SCIENCE_BIOINFO_SKILL_CANDIDATES.md records the selection rationale, install commands, and optional batch B.

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
- Installed 18 science/bioinformatics skills via npx skills add using GIT_CONFIG_GLOBAL=/dev/null to bypass stale git proxy settings.
- Copied the installed skills to ~/.codex/skills and added Chinese trigger phrases to their descriptions.
- Ran scripts/sync_skills.py --apply to mirror new skills into skills/global and refresh registry files.
- Ran scripts/validate_skills.py: 46 skills, 0 errors, 11 warnings for credential-like words only.
- Updated README.md with a science/bioinformatics skill catalog section.

## Open Problems
- Codex should be restarted to load the new skills in the current session skill list.
- Validation warnings remain credential-word heuristics; no forbidden secret-like files were detected.
- The machine still has git global proxy entries pointing at 127.0.0.1:7890; future npx skills add may need GIT_CONFIG_GLOBAL=/dev/null unless the proxy config is fixed.

## Next Step
- Commit and push the science/bioinformatics skills, README, candidate document, and refreshed registry.
- After restart, test Chinese trigger prompts for PubMed, paper reproduction, RNA-seq, phylogenetics, and scientific critique.
- Later, consider optional batch B only when a real project needs single-cell, metabolomics, comparative genomics, CRISPR, or drug discovery skills.

## Resume Prompt
Science/bioinformatics batch A has been installed and mirrored. Continue by committing and pushing the updated skill hub, then remind the user to restart Codex and run trigger smoke tests.
