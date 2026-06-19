#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import filecmp
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SOURCES = REPO / 'registry' / 'sources.tsv'
INVENTORY_TSV = REPO / 'registry' / 'SKILL_INVENTORY.tsv'
INVENTORY_JSON = REPO / 'registry' / 'skills.json'

EXCLUDE_DIRS = {'.git', '__pycache__', '.pytest_cache', '.ruff_cache', 'node_modules'}
EXCLUDE_SUFFIXES = ('.pyc', '.tmp', '.log')
SECRET_NAMES = {'.env', '.env.local'}
SECRET_SUFFIXES = ('.key', '.pem')
BACKUP_MARKERS = ('.bak', 'backup')


@dataclass
class Action:
    status: str
    action: str
    path: str
    detail: str = ''


def rel(p: Path) -> str:
    try:
        return p.resolve().relative_to(REPO.resolve()).as_posix()
    except ValueError:
        return p.as_posix()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def load_sources() -> list[dict[str, str]]:
    if not SOURCES.exists():
        raise SystemExit(f'Missing {SOURCES}')
    with SOURCES.open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f, delimiter='\t'))
    return [r for r in rows if r.get('enabled', '').lower() in {'yes', 'true', '1'}]


def safe_name(name: str) -> str:
    return ''.join(c if c.isalnum() or c in '._-' else '-' for c in name).strip('-') or 'unnamed'


def workspace_slug(source_id: str) -> str:
    sid = source_id
    if sid.endswith('_workspace'):
        sid = sid[:-10]
    return safe_name(sid)


def should_exclude(path: Path) -> bool:
    parts = set(path.parts)
    if parts & EXCLUDE_DIRS:
        return True
    name = path.name
    if name in SECRET_NAMES:
        return True
    if name.endswith(EXCLUDE_SUFFIXES) or name.endswith(SECRET_SUFFIXES):
        return True
    low = name.lower()
    if any(marker in low for marker in BACKUP_MARKERS):
        return True
    return False


def iter_skill_dirs(root: Path) -> list[Path]:
    if not root.exists():
        return []
    out = []
    for p in root.rglob('SKILL.md'):
        if not p.is_file() or should_exclude(p):
            continue
        rel_parts = p.relative_to(root).parts
        # Do not mirror hidden provider/system skill trees such as .system by default.
        if any(part.startswith('.') for part in rel_parts):
            continue
        out.append(p.parent)
    return sorted(out)


def copy_tree(src: Path, dst: Path, *, apply: bool, actions: list[Action]) -> None:
    for path in sorted(src.rglob('*')):
        rel_parts = path.relative_to(src).parts
        if any(part.startswith('.') for part in rel_parts) or should_exclude(path):
            if path.is_dir():
                continue
            actions.append(Action('skip', 'exclude', rel(dst / path.relative_to(src)), 'excluded by policy'))
            continue
        target = dst / path.relative_to(src)
        if path.is_dir():
            if not target.exists():
                actions.append(Action('create' if not apply else 'created', 'mkdir', rel(target)))
                if apply:
                    target.mkdir(parents=True, exist_ok=True)
            continue
        if not target.exists():
            actions.append(Action('create' if not apply else 'created', 'copy', rel(target), f'from {path}'))
            if apply:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, target)
            continue
        try:
            same = filecmp.cmp(path, target, shallow=False)
        except OSError:
            same = False
        if same:
            actions.append(Action('ok', 'skip', rel(target), 'identical'))
        else:
            actions.append(Action('update' if not apply else 'updated', 'copy', rel(target), f'from {path}'))
            if apply:
                shutil.copy2(path, target)


def parse_skill(skill_dir: Path, source: dict[str, str], dest_dir: Path) -> dict[str, str]:
    skill_md = skill_dir / 'SKILL.md'
    text = skill_md.read_text(encoding='utf-8', errors='replace')
    name = skill_dir.name
    description = ''
    if text.startswith('---'):
        end = text.find('\n---', 3)
        if end != -1:
            fm = text[3:end].splitlines()
            for line in fm:
                if line.startswith('name:'):
                    name = line.split(':', 1)[1].strip().strip('"\'') or name
                if line.startswith('description:'):
                    description = line.split(':', 1)[1].strip().strip('"\'')
    files = [p for p in skill_dir.rglob('*') if p.is_file() and not should_exclude(p)]
    return {
        'name': name,
        'source_id': source.get('source_id', ''),
        'scope': source.get('scope', ''),
        'source_path': skill_dir.as_posix(),
        'repo_path': rel(dest_dir),
        'files': str(len(files)),
        'bytes': str(sum(p.stat().st_size for p in files)),
        'description': description,
        'synced_at': datetime.now().isoformat(timespec='seconds'),
    }


def write_inventory(items: list[dict[str, str]], *, apply: bool, actions: list[Action]) -> None:
    fields = ['name', 'scope', 'source_id', 'source_path', 'repo_path', 'files', 'bytes', 'description', 'synced_at']
    tsv_lines = []
    from io import StringIO
    buf = StringIO()
    writer = csv.DictWriter(buf, fieldnames=fields, delimiter='\t', lineterminator='\n')
    writer.writeheader()
    for item in sorted(items, key=lambda x: (x['scope'], x['name'], x['source_id'])):
        writer.writerow({k: item.get(k, '') for k in fields})
    tsv_text = buf.getvalue()
    json_text = json.dumps(sorted(items, key=lambda x: (x['scope'], x['name'], x['source_id'])), ensure_ascii=False, indent=2) + '\n'
    for path, text in [(INVENTORY_TSV, tsv_text), (INVENTORY_JSON, json_text)]:
        old = path.read_text(encoding='utf-8') if path.exists() else None
        if old == text:
            actions.append(Action('ok', 'skip', rel(path), 'inventory unchanged'))
        else:
            actions.append(Action('create' if old is None and not apply else 'write' if not apply else 'written', 'write', rel(path), 'generated inventory'))
            if apply:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding='utf-8')


def sync_once(*, apply: bool) -> tuple[list[Action], list[dict[str, str]]]:
    actions: list[Action] = []
    items: list[dict[str, str]] = []
    for source in load_sources():
        root = Path(source['path']).expanduser()
        scope = source.get('scope', '')
        if not root.exists():
            actions.append(Action('warning', 'missing-source', root.as_posix(), source.get('source_id', '')))
            continue
        skill_dirs = iter_skill_dirs(root)
        if not skill_dirs:
            actions.append(Action('warning', 'no-skills', root.as_posix(), source.get('source_id', '')))
            continue
        for skill_dir in skill_dirs:
            if scope == 'global':
                dest = REPO / 'skills' / 'global' / safe_name(skill_dir.name)
            elif scope == 'workspace':
                dest = REPO / 'skills' / 'workspace' / workspace_slug(source.get('source_id', 'workspace')) / safe_name(skill_dir.name)
            else:
                dest = REPO / 'skills' / safe_name(scope) / safe_name(skill_dir.name)
            copy_tree(skill_dir, dest, apply=apply, actions=actions)
            items.append(parse_skill(skill_dir, source, dest))
    # Include local authored skills in inventory, but do not mirror them elsewhere.
    local_root = REPO / 'skills' / 'local'
    for skill_dir in iter_skill_dirs(local_root):
        items.append(parse_skill(skill_dir, {'source_id': 'repo_local', 'scope': 'local'}, skill_dir))
    write_inventory(items, apply=apply, actions=actions)
    return actions, items


def has_git_changes() -> bool:
    res = subprocess.run(['git', 'status', '--porcelain'], cwd=REPO, text=True, capture_output=True, check=False)
    return bool(res.stdout.strip())


def git_commit_and_push(*, push: bool, message: str | None = None) -> None:
    if not has_git_changes():
        print('[sync-skills] no git changes')
        return
    subprocess.run(['git', 'add', '.'], cwd=REPO, check=True)
    msg = message or f'chore(skills): sync local skill library {datetime.now().strftime("%Y-%m-%d %H:%M")}'
    subprocess.run(['git', 'commit', '-m', msg], cwd=REPO, check=True)
    if push:
        subprocess.run(['git', 'push', '-u', 'origin', 'main'], cwd=REPO, check=True)


def print_actions(actions: list[Action], *, max_lines: int = 200) -> None:
    payload = {
        'summary': {
            'total': len(actions),
            **{s: sum(1 for a in actions if a.status == s) for s in sorted({a.status for a in actions})},
        },
        'actions': [asdict(a) for a in actions[:max_lines]],
        'truncated': max(0, len(actions) - max_lines),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def main() -> int:
    ap = argparse.ArgumentParser(description='Mirror local Codex skills into this repository')
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument('--dry-run', action='store_true', help='Preview changes; default')
    mode.add_argument('--apply', action='store_true', help='Apply mirror/inventory updates')
    ap.add_argument('--commit', action='store_true', help='Commit changes after apply')
    ap.add_argument('--push', action='store_true', help='Push after commit')
    ap.add_argument('--watch', action='store_true', help='Run continuously')
    ap.add_argument('--interval', type=int, default=60)
    ap.add_argument('--message', default='')
    args = ap.parse_args()
    apply = bool(args.apply)
    if (args.commit or args.push) and not apply:
        raise SystemExit('--commit/--push require --apply')

    while True:
        actions, _ = sync_once(apply=apply)
        print_actions(actions)
        if apply and (args.commit or args.push):
            git_commit_and_push(push=args.push, message=args.message or None)
        if not args.watch:
            break
        time.sleep(max(5, args.interval))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
