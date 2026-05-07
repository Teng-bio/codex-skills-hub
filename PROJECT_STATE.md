# PROJECT_STATE

## Project Summary
Personal GitHub-backed skill library for Codex/agent skills. It mirrors global and workspace skills, stores locally authored skills, and provides safe sync/validation automation.

## Current Goal
Create a well-organized repository that can store current skills and automatically upload newly created or modified skills to GitHub.

## Current Status
- Local repository scaffold is complete and committed on main.
- Initial sync mirrored 20 global skills, 1 workspace skill, and 1 local authored publisher skill into registry.
- New global skill installed: skill-library-publisher, so future requests to create/update/upload/sync skills should auto-trigger the publishing workflow.
- Remote origin is configured as git@github.com:Teng-bio/codex-skills-hub.git, but GitHub reports repository not found.
- gh CLI is not installed, so remote repository creation still requires GitHub web UI, installing/logging into gh, or a GitHub API token.

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
- Created skill-library-publisher under skills/local and installed it globally.
- Added scripts/new_skill.py for standardized skill scaffolding.
- Ran scripts/sync_skills.py --apply to mirror skills and generate inventory.
- Initialized git repository and committed initial skill hub.
- Configured origin to git@github.com:Teng-bio/codex-skills-hub.git; remote does not exist yet.

## Open Problems
- Need create GitHub repository Teng-bio/codex-skills-hub before push can succeed.
- Validation has warnings for credential-like words in some mirrored skill docs; no errors, but review before public publishing if repository will be public.
- Need decide whether auto-upload service should be enabled after first successful push.

## Next Step
- Create the GitHub repository named codex-skills-hub under Teng-bio.
- Then run: git -C /home/teng/claude_code/codex-skills-hub push -u origin main.
- For future new skills, use skill-library-publisher workflow or scripts/new_skill.py --apply --sync --commit --push.

## Resume Prompt
Continue from /home/teng/claude_code/codex-skills-hub. The local repo is committed and origin is set, but the GitHub repo does not exist yet. Create Teng-bio/codex-skills-hub on GitHub, push main, then optionally enable scripts/sync_skills.py --watch for auto-upload.
