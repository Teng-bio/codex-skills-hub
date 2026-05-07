# codex-skills-hub

Personal Codex / agent skill library for storing, auditing, syncing, and publishing local skills.

## Goals

- Keep a versioned copy of local skills from `~/.codex/skills`.
- Keep selected workspace skills, e.g. `planning-with-files`, in one repo.
- Generate a durable skill inventory and sync manifest.
- Support safe automatic upload of newly created or modified skills.
- Avoid global pollution: install/use decisions are recorded before promotion.

## Directory layout

```text
skills/
  global/                 # mirrored from ~/.codex/skills/<skill>/
  workspace/              # mirrored from project-local .codex/skills/<skill>/
  local/                  # skills authored directly in this repository
registry/
  SKILL_INVENTORY.tsv     # generated inventory
  skills.json             # generated machine-readable inventory
  sources.tsv             # configured sync sources
docs/
  OPERATING_MODEL.md      # workflow, ownership, and promotion policy
scripts/
  sync_skills.py          # dry-run/apply/commit/push/watch sync tool
  validate_skills.py      # lightweight SKILL.md validation
services/
  codex-skills-hub-sync.service.example
```

## Safe sync

Preview:

```bash
python scripts/sync_skills.py --dry-run
```

Apply local mirror update:

```bash
python scripts/sync_skills.py --apply
```

Apply, commit, and push:

```bash
python scripts/sync_skills.py --apply --commit --push
```

Watch and auto-upload:

```bash
python scripts/sync_skills.py --watch --interval 60 --apply --commit --push
```

## Current GitHub remote plan

Default remote target:

```text
git@github.com:Teng-bio/codex-skills-hub.git
```

If the GitHub repository does not exist yet, create it on GitHub first or install/login `gh`, then push this local repo.
