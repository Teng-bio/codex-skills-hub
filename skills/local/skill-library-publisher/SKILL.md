---
name: skill-library-publisher
description: Manage a GitHub-backed Codex skill library and publish newly created or updated skills using the user's standard repository workflow. Use when the user says 创建skill, 新建skill, 写skill, 更新skill, 上传skill, 同步skill库, 发布skill到GitHub, 自动上传skill, skill仓库, skill库入库, or wants future skills validated, inventoried, committed, and pushed to the skills repository.
---

# Skill Library Publisher

## Purpose

Use the personal skill repository as the canonical place for authored skills:

```text
/home/teng/claude_code/codex-skills-hub
```

Repository layout:

```text
skills/local/<skill-name>/       # new authored skills go here first
skills/global/<skill-name>/      # mirror of ~/.codex/skills
skills/workspace/<project>/<skill-name>/
registry/SKILL_INVENTORY.tsv
registry/skills.json
scripts/sync_skills.py
scripts/validate_skills.py
```

## Workflow for new skills

1. Normalize the skill name to lowercase hyphen-case.
2. Create the skill under:

   ```text
   /home/teng/claude_code/codex-skills-hub/skills/local/<skill-name>/SKILL.md
   ```

3. Keep `SKILL.md` concise:
   - YAML frontmatter has `name` and `description`.
   - `description` includes explicit Chinese and English trigger phrases.
   - Body contains workflow/checklists only; large details go one level down into `references/`.
4. Validate:

   ```bash
   python scripts/validate_skills.py
   ```

5. Refresh mirrors and inventory:

   ```bash
   python scripts/sync_skills.py --apply
   ```

6. Commit and push when remote exists:

   ```bash
   python scripts/sync_skills.py --apply --commit --push
   ```

## Workflow for modified skills

When a global or workspace skill was edited, run from the repo root:

```bash
python scripts/sync_skills.py --dry-run
python scripts/sync_skills.py --apply --commit --push
```

If GitHub remote is missing or push fails, keep the local commit and report the exact remote setup needed.

## Safety rules

- Do not commit secrets: `.env`, tokens, private keys, `*.pem`, `*.key`.
- Do not edit mirrored third-party skills as if they are authored local skills; copy/adapt into `skills/local/` if a custom version is needed.
- Prefer dry-run before apply.
- If creating a hook-heavy skill, keep it local/workspace until one real project validates it.

## Auto-upload service

To keep the repository synced automatically after manual skill edits, use:

```bash
python scripts/sync_skills.py --watch --interval 60 --apply --commit --push
```

For a user service, adapt:

```text
services/codex-skills-hub-sync.service.example
```
