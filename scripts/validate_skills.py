#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / 'skills'
REQUIRED = {'name', 'description'}
FORBIDDEN_NAMES = {'.env'}
FORBIDDEN_SUFFIXES = ('.pem', '.key')
SYSTEM_MIRROR_EXCLUDES = {'imagegen', 'openai-docs', 'plugin-creator', 'skill-creator', 'skill-installer'}


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith('---'):
        return {}
    end = text.find('\n---', 3)
    if end < 0:
        return {}
    out = {}
    for line in text[3:end].splitlines():
        if ':' in line and not line.startswith(' '):
            k, v = line.split(':', 1)
            out[k.strip()] = v.strip().strip('"\'')
    return out


def main() -> int:
    issues = []
    skill_files = sorted(SKILLS_ROOT.rglob('SKILL.md')) if SKILLS_ROOT.exists() else []
    for path in skill_files:
        rel_parts = path.relative_to(ROOT).parts
        if len(rel_parts) >= 3 and rel_parts[0] == 'skills' and rel_parts[1] == 'global' and rel_parts[2] in SYSTEM_MIRROR_EXCLUDES:
            continue
        text = path.read_text(encoding='utf-8', errors='replace')
        fm = parse_frontmatter(text)
        missing = sorted(REQUIRED - set(fm))
        if missing:
            issues.append({'path': path.relative_to(ROOT).as_posix(), 'level': 'error', 'issue': f'missing frontmatter keys: {missing}'})
        desc = fm.get('description', '')
        if len(desc) < 30:
            issues.append({'path': path.relative_to(ROOT).as_posix(), 'level': 'warning', 'issue': 'description is short; auto-trigger may be weak'})
        if re.search(r'api[_-]?key|token|password|secret', text, re.I):
            issues.append({'path': path.relative_to(ROOT).as_posix(), 'level': 'warning', 'issue': 'contains credential-like words; review before push'})
    for path in ROOT.rglob('*'):
        if path.is_file() and (path.name in FORBIDDEN_NAMES or path.name.endswith(FORBIDDEN_SUFFIXES)):
            issues.append({'path': path.relative_to(ROOT).as_posix(), 'level': 'error', 'issue': 'forbidden secret-like file'})
    summary = {
        'skill_count': len(skill_files),
        'errors': sum(1 for i in issues if i['level'] == 'error'),
        'warnings': sum(1 for i in issues if i['level'] == 'warning'),
        'issues': issues[:200],
        'truncated': max(0, len(issues) - 200),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if summary['errors'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
