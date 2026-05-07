# PROJECT_STATE

## Project Summary
Personal GitHub-backed skill library for Codex/agent skills. It mirrors global and workspace skills, stores locally authored skills, and provides safe sync/validation automation.

## Current Goal
Create a well-organized repository that can store current skills and automatically upload newly created or modified skills to GitHub.

## Current Status
- Local repository scaffold created.
- Sync sources configured in `registry/sources.tsv`.
- Need run initial sync, initialize git, and push after GitHub remote exists.

## Key Paths
- README.md
- AGENTS.md
- docs/OPERATING_MODEL.md
- registry/sources.tsv
- scripts/sync_skills.py
- scripts/validate_skills.py
- skills/global/
- skills/workspace/
- skills/local/

## Decisions
- Use `skills/local/` for newly authored skills.
- Mirror installed global skills into `skills/global/`.
- Mirror selected workspace skills under `skills/workspace/<workspace>/`.
- Use dry-run by default for sync.
- Auto-upload is implemented by `sync_skills.py --watch --apply --commit --push`, not by hidden destructive hooks.

## Recent Changes
- Initial project scaffold created.

## Open Problems
- GitHub remote repository may not exist yet.
- `gh` is not installed, so remote creation requires GitHub web UI, GitHub API token, or installing/logging into GitHub CLI.

## Next Step
- Run initial skill sync and commit local repo.
- Create GitHub repo `Teng-bio/codex-skills-hub` or configure another remote.
- Push local main branch.

## Resume Prompt
Continue setting up `/home/teng/claude_code/codex-skills-hub`: run sync/validation, initialize git, then create/push the GitHub remote when authentication tooling is available.
