# Skill library operating model

## Ownership model

| Area | Meaning | Rule |
|---|---|---|
| `skills/global/` | Mirror of globally installed skills | Do not edit here first unless intentionally patching a global skill. |
| `skills/workspace/` | Mirror of project-local skills | Keep workspace context in path names. |
| `skills/local/` | Skills authored in this repo | Preferred place to create new skills. |
| `registry/` | Generated inventory and source config | Review diffs before publishing. |

## New skill workflow

1. Create new skill under `skills/local/<skill-name>/SKILL.md`.
2. Run `python scripts/validate_skills.py`.
3. Run `python scripts/sync_skills.py --apply` to refresh inventory.
4. Commit and push.
5. Only install globally/workspace after a real use case validates it.

## Auto-upload policy

Auto-upload is allowed only for repository changes that pass lightweight validation.
The sync script intentionally excludes common backup/cache/secret files.

## Exclusions

- `.git/`, `__pycache__/`, `.pytest_cache/`, `.ruff_cache/`, `node_modules/`
- `*.bak*`, `*.tmp`, `*.log`, `.env`, `*.key`, `*.pem`, `id_rsa*`, `id_ed25519*`

## Notes

`auto-deep-research` may be mirrored here, but its active design policy is no hidden `answers` routing/API dependency.
