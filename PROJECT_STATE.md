# PROJECT_STATE

## Project Summary
Personal GitHub-backed skill library for Codex/agent skills. It mirrors global and workspace skills, stores locally authored skills, and provides safe sync/validation automation.

## Current Goal
Create a well-organized repository that can store current skills and automatically upload newly created or modified skills to GitHub.

## Current Status
- Local repository scaffold is complete and committed on main.
- Initial sync mirrored global/workspace/local skills into registry.
- Global skill installed: skill-library-publisher, so future requests to create/update/upload/sync skills should auto-trigger the publishing workflow.
- Remote origin is configured as git@github.com:Teng-bio/codex-skills-hub.git.
- Initial main branch has been pushed to GitHub successfully.

## Key Paths
- skills/local/skill-library-publisher/SKILL.md
- /home/teng/.codex/skills/skill-library-publisher/SKILL.md
- scripts/new_skill.py
- scripts/sync_skills.py
- scripts/validate_skills.py
- registry/SKILL_INVENTORY.tsv
- registry/skills.json
- docs/OPERATING_MODEL.md
- services/codex-skills-hub-sync.service.example

## Decisions
- Future authored skills should be created under skills/local/<skill-name>/ first.
- After creating or editing a skill, run validate, sync inventory, commit, and push.
- skill-library-publisher is the standard workflow skill for new/updated skill publication.
- Provider/system skills under ~/.codex/skills/.system are excluded from inventory/publishing by default.
- Auto-upload is explicit via scripts/sync_skills.py --watch --apply --commit --push or the example user service.

## Recent Changes
- Pushed initial codex-skills-hub repository to GitHub remote git@github.com:Teng-bio/codex-skills-hub.git.
- Confirmed local main tracks origin/main.

## Open Problems
- Validation has warnings for credential-like words in some mirrored skill docs; no errors, but review before public publishing if repository is public.
- Need decide whether auto-upload service should be enabled after confirming GitHub repo visibility and contents.

## Next Step
- Optionally inspect the GitHub repository contents in browser.
- If automatic upload is desired, enable the watcher command or adapt services/codex-skills-hub-sync.service.example.
- For future new skills, use skill-library-publisher workflow or scripts/new_skill.py --apply --sync --commit --push.

## Resume Prompt
codex-skills-hub has been pushed to git@github.com:Teng-bio/codex-skills-hub.git. Continue by deciding whether to enable automatic watch-based sync, or create the next local skill under skills/local/ using scripts/new_skill.py.
