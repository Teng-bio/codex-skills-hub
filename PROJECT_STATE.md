# PROJECT_STATE

## Project Summary
Personal GitHub-backed skill library for Codex/agent skills. It mirrors global and workspace skills, stores locally authored skills, and provides safe sync/validation automation.

## Current Goal
Create a well-organized repository that can store current skills and automatically upload newly created or modified skills to GitHub.

## Current Status
- Local repository scaffold is complete and committed on main.
- Initial sync mirrors global/workspace/local skills into registry.
- planning-with-files has been promoted to a global Codex skill and mirrored into skills/global/planning-with-files/.
- Global skill installed: skill-library-publisher, so future requests to create/update/upload/sync skills should auto-trigger the publishing workflow.
- Remote origin is configured as git@github.com:Teng-bio/codex-skills-hub.git and main has been pushed.
- README.md documents the skill catalog, trigger phrases, and now marks planning-with-files as global.

## Key Paths
- skills/global/planning-with-files/SKILL.md
- skills/workspace/pipeline_v2/planning-with-files/SKILL.md
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
- planning-with-files is the global planning kernel; workspace copy remains mirrored as pilot provenance/backup.
- Future authored skills should be created under skills/local/<skill-name>/ first.
- After creating or editing a skill, run validate, sync inventory, commit, and push.
- skill-library-publisher is the standard workflow skill for new/updated skill publication.
- Provider/system skills under ~/.codex/skills/.system are excluded from inventory/publishing by default.
- Auto-upload is explicit via scripts/sync_skills.py --watch --apply --commit --push or the example user service.

## Recent Changes
- Ran scripts/sync_skills.py --apply after global promotion of planning-with-files.
- Added skills/global/planning-with-files/ mirror and refreshed registry/SKILL_INVENTORY.tsv plus registry/skills.json.
- Updated README.md so planning-with-files appears as a global skill with its workspace pilot mirror noted.
- Validated skills after sync; validation has 0 errors and 8 known credential-word warnings only.

## Open Problems
- Validation still warns about credential-like words in some mirrored skill docs; no errors, but review before making the repository public.
- Need decide whether auto-upload service should be enabled after confirming GitHub repo visibility and contents.

## Next Step
- Commit and push the planning-with-files global mirror plus README/inventory updates.
- If desired later, enable automatic watch-based sync using scripts/sync_skills.py --watch or the example service.
- Continue Retron result organization with manifest-only current/README.md and current/MANIFEST.tsv only after explicit user approval.

## Resume Prompt
planning-with-files has been promoted to global and mirrored into the skill hub. Continue by verifying git status, committing and pushing the global mirror/README/inventory update, then return to Retron result organization if requested.
