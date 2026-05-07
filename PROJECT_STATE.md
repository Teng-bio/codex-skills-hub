# PROJECT_STATE

## Project Summary
Personal GitHub-backed skill library for Codex/agent skills. It mirrors global and workspace skills, stores locally authored skills, and provides safe sync/validation automation.

## Current Goal
Create a well-organized repository that can store current skills and automatically upload newly created or modified skills to GitHub.

## Current Status
- Local repository scaffold is complete and committed on main.
- Initial sync mirrored global/workspace/local skills into registry.
- Global skill installed: skill-library-publisher, so future requests to create/update/upload/sync skills should auto-trigger the publishing workflow.
- Remote origin is configured as git@github.com:Teng-bio/codex-skills-hub.git and main has been pushed.
- README.md has been expanded into a Chinese skill catalog explaining each skill role and trigger phrases.

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
- Rewrote README.md with repository purpose, directory layout, new skill workflow, auto-sync commands, trigger principles, and grouped skill catalog.
- Documented each current skill by role, typical trigger phrases, and repository path.
- Validated skills after README update; validation has 0 errors and known warnings only.

## Open Problems
- Validation still warns about credential-like words in some mirrored skill docs; no errors, but review before making the repository public.
- Need decide whether auto-upload service should be enabled after confirming GitHub repo visibility and contents.

## Next Step
- Commit and push the README catalog update.
- If desired, enable automatic watch-based sync using scripts/sync_skills.py --watch or the example service.
- For future new skills, use skill-library-publisher or scripts/new_skill.py --apply --sync --commit --push.

## Resume Prompt
README.md now documents each skill role and trigger phrases. Continue by pushing this documentation update, then decide whether to enable automatic watch-based sync.
