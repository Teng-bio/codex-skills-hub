#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LOCAL = REPO / 'skills' / 'local'


def slugify(name: str) -> str:
    s = name.strip().lower()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = re.sub(r'-+', '-', s).strip('-')
    if not s:
        raise SystemExit('Skill name normalized to empty string')
    if len(s) > 64:
        raise SystemExit('Skill name too long after normalization')
    return s


def template(name: str, description: str) -> str:
    return f'''---
name: {name}
description: {description}
---

# {name}

## Purpose

Describe the specific capability this skill provides.

## Workflow

1. Read the relevant project state and active planning files when present.
2. Apply the smallest safe step.
3. Validate outputs.
4. Record important decisions and next steps.

## Safety

- Prefer dry-run for file operations.
- Do not commit secrets or credentials.
- Keep generated artifacts under a guarded run when appropriate.
'''


def main() -> int:
    ap = argparse.ArgumentParser(description='Create a local skill in codex-skills-hub')
    ap.add_argument('name')
    ap.add_argument('--description', required=True, help='Frontmatter description with trigger phrases')
    ap.add_argument('--apply', action='store_true', help='Actually create files; default is dry-run')
    ap.add_argument('--sync', action='store_true', help='Run sync after creation; requires --apply')
    ap.add_argument('--commit', action='store_true', help='Commit after sync; requires --sync')
    ap.add_argument('--push', action='store_true', help='Push after commit; requires --commit')
    args = ap.parse_args()
    if (args.sync or args.commit or args.push) and not args.apply:
        raise SystemExit('--sync/--commit/--push require --apply')
    if (args.commit or args.push) and not args.sync:
        raise SystemExit('--commit/--push require --sync')
    if args.push and not args.commit:
        raise SystemExit('--push requires --commit')

    name = slugify(args.name)
    skill_dir = LOCAL / name
    skill_md = skill_dir / 'SKILL.md'
    print(f'skill_name={name}')
    print(f'path={skill_md}')
    if skill_md.exists():
        raise SystemExit(f'Already exists: {skill_md}')
    if args.apply:
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_md.write_text(template(name, args.description), encoding='utf-8')
        print('created')
        py = sys.executable or 'python3'
        subprocess.run([py, 'scripts/validate_skills.py'], cwd=REPO, check=True)
        if args.sync:
            cmd = [py, 'scripts/sync_skills.py', '--apply']
            if args.commit:
                cmd.append('--commit')
            if args.push:
                cmd.append('--push')
            subprocess.run(cmd, cwd=REPO, check=True)
    else:
        print('dry-run only; add --apply to create')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
