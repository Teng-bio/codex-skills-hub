#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

OS_DIR = '.project_os'
ROOT_ENTRY_FILES = ['PROJECT_STATE.md', 'DATA_ASSETS.md', 'RESULTS_INDEX.md', 'RUNS_INDEX.tsv', 'DECISIONS.md']
TASK_REQUIRED_FIELDS = ['task_id', 'title', 'status', 'kind', 'branch_id', 'created_at', 'updated_at', 'stage', 'objective_file', 'context_manifest']
RUN_REQUIRED_FIELDS = ['run_id', 'task_id', 'status', 'created_at', 'code_ref', 'environment', 'inputs', 'parameters', 'commands', 'outputs', 'metrics', 'result_status']
RESULT_STATUSES = {'draft', 'candidate', 'accepted', 'current', 'superseded', 'legacy', 'release'}
TASK_STATUSES = {'active', 'paused', 'blocked', 'completed', 'archived', 'superseded'}
RUN_STATUSES = {'active', 'completed', 'failed', 'pending_review', 'archived', 'superseded'}

INDEX_HEADERS = {
    'tasks.tsv': ['task_id', 'status', 'kind', 'branch_id', 'stage', 'title', 'task_path', 'created_at', 'updated_at', 'notes'],
    'branches.tsv': ['branch_id', 'status', 'parent_branch_id', 'title', 'created_at', 'notes'],
    'runs.tsv': ['run_id', 'task_id', 'status', 'result_status', 'run_path', 'created_at', 'closed_at', 'notes'],
    'results.tsv': ['result_id', 'task_id', 'run_id', 'status', 'type', 'path', 'title', 'created_at', 'accepted_at', 'replaced_by', 'notes'],
    'assets.tsv': ['asset_id', 'kind', 'path', 'version', 'source_url', 'source_note', 'immutable', 'status', 'registered_at', 'notes'],
}
RUN_LINK_HEADERS = ['run_id', 'status', 'path', 'created_at', 'notes']
RESULT_LINK_HEADERS = ['result_id', 'status', 'path', 'run_id', 'created_at', 'notes']
ROOT_RUNS_HEADERS = INDEX_HEADERS['runs.tsv']

WORKFLOW_TEXT = '''# Project OS Workflow

Default phases:

```text
Intake -> Plan -> Research -> Run -> Evaluate -> Promote -> Archive -> Release
```

Rules:

- Read `PROJECT_STATE.md` and this workflow before substantive work.
- Resolve continuation from `runtime/current_task`, `runtime/current_branch`, and `runtime/current_run`.
- Load task context from `tasks/<task_id>/context_manifest.jsonl`.
- Put generated run outputs under `runs/<run_id>/` or the project-approved run directory.
- Register runs and results in `.project_os/indexes/` and root human indexes.
- Promote to `current/` only after explicit user approval.
- Update `PROJECT_STATE.md` or task `handoff.md` before stopping when project state changed.
'''

CONFIG_TEXT = '''schema_version: 1
project_os_dir: .project_os
run_roots:
  - runs
  - analysis_runs
human_entry_files:
  - PROJECT_STATE.md
  - DATA_ASSETS.md
  - RESULTS_INDEX.md
  - RUNS_INDEX.tsv
  - DECISIONS.md
promotion_requires_user_approval: true
adapters:
  codex: true
  claude_code: false
  opencode: false
'''

SPEC_TEXTS = {
    'project_rules.md': '# Project rules\n\nLink project-specific rules here. For Codex projects, summarize or point to `AGENTS.md`.\n',
    'task_tree.md': '# Task tree\n\nLong-lived directions and task relationships. Keep details in task directories.\n',
    'context_manifest.md': '# Context manifest policy\n\nTask context should be loaded from `context_manifest.jsonl` instead of whole-repo guessing.\n',
    'run_provenance.md': '# Run provenance policy\n\nEvery formal run should have `RUN_MANIFEST.json` with inputs, parameters, code reference, environment, commands, outputs, metrics, and status.\n',
    'result_curation.md': '# Result curation policy\n\nResults move from draft to candidate to accepted/current only through explicit review and registration.\n',
    'data_assets.md': '# Data assets policy\n\nUse root `DATA_ASSETS.md` for data/source provenance. Do not infer provenance from filenames alone.\n',
    'user_profile.md': '# User profile policy\n\nOptional project-local collaboration preferences. Keep this reviewable and low sensitivity.\n',
    'release_packaging.md': '# Release packaging policy\n\nRelease packages should contain accepted outputs, manifests, checksums, environment notes, and source run references.\n',
}

ROOT_DOC_DEFAULTS = {
    'PROJECT_STATE.md': '# PROJECT_STATE\n\n## Project Summary\n\nTBD.\n\n## Current Goal\n\nTBD.\n\n## Current Status\n\n- Harness initialized; project-specific status still needs review.\n\n## Key Paths\n\n- `.project_os/`\n\n## Decisions\n\n- TBD.\n\n## Recent Changes\n\n- Initialized research-project-os harness.\n\n## Open Problems\n\n- Fill in project-specific state.\n\n## Next Step\n\n- Review project state and create the first active task.\n\n## Resume Prompt\n\nContinue by reading `PROJECT_STATE.md` and `.project_os/workflow.md`.\n',
    'DATA_ASSETS.md': '# DATA_ASSETS\n\nRecord raw data, reference databases, external resources, versions, source URLs, checksums when practical, and provenance caveats.\n',
    'RESULTS_INDEX.md': '# RESULTS_INDEX\n\nHuman-facing index of accepted, candidate, legacy, and release outputs.\n',
    'RUNS_INDEX.tsv': '\t'.join(ROOT_RUNS_HEADERS) + '\n',
    'DECISIONS.md': '# DECISIONS\n\nDurable project decisions.\n',
}

class ProjectOSError(Exception):
    pass


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec='seconds')


def timestamp() -> str:
    return datetime.now().strftime('%Y%m%d_%H%M%S')


def slugify(text: str, max_len: int = 48) -> str:
    slug = re.sub(r'[^a-zA-Z0-9]+', '_', text.strip().lower())
    slug = re.sub(r'_+', '_', slug).strip('_')
    return (slug or 'task')[:max_len].strip('_') or 'task'


def project_os(root: Path) -> Path:
    return root / OS_DIR


def relpath(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def print_json(payload: Any) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except FileNotFoundError as exc:
        raise ProjectOSError(f'Missing JSON file: {path}') from exc
    except json.JSONDecodeError as exc:
        raise ProjectOSError(f'Malformed JSON file: {path}: {exc}') from exc
    if not isinstance(data, dict):
        raise ProjectOSError(f'Expected JSON object: {path}')
    return data


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline='', encoding='utf-8') as handle:
        return list(csv.DictReader(handle, delimiter='\t'))


def write_tsv(path: Path, headers: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, delimiter='\t', lineterminator='\n')
        writer.writeheader()
        for row in rows:
            writer.writerow({h: '' if row.get(h) is None else str(row.get(h, '')) for h in headers})


def upsert_tsv(path: Path, headers: list[str], key: str, row: dict[str, Any]) -> None:
    rows = read_tsv(path)
    out: list[dict[str, Any]] = []
    seen = False
    for existing in rows:
        if existing.get(key) == row.get(key):
            out.append(row)
            seen = True
        else:
            out.append(existing)
    if not seen:
        out.append(row)
    write_tsv(path, headers, out)


def ensure_initialized(root: Path) -> None:
    if not (project_os(root) / 'workflow.md').exists():
        raise ProjectOSError(f'Missing {OS_DIR}/workflow.md. Run init first.')


def write_missing_file(path: Path, text: str, apply: bool, actions: list[dict[str, str]]) -> None:
    if path.exists():
        actions.append({'status': 'exists', 'path': path.as_posix()})
        return
    actions.append({'status': 'create' if apply else 'would_create', 'path': path.as_posix()})
    if apply:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')


def ensure_dir(path: Path, apply: bool, actions: list[dict[str, str]]) -> None:
    if path.exists():
        actions.append({'status': 'exists', 'path': path.as_posix()})
        return
    actions.append({'status': 'mkdir' if apply else 'would_mkdir', 'path': path.as_posix()})
    if apply:
        path.mkdir(parents=True, exist_ok=True)


def command_init(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    os_dir = project_os(root)
    actions: list[dict[str, str]] = []
    dirs = [
        os_dir,
        os_dir / 'spec',
        os_dir / 'tasks',
        os_dir / 'runtime',
        os_dir / 'runtime' / 'sessions',
        os_dir / 'journals',
        os_dir / 'indexes',
        os_dir / 'exports',
        root / 'runs',
        root / 'current',
        root / 'release',
    ]
    for directory in dirs:
        ensure_dir(directory, args.apply, actions)
    write_missing_file(os_dir / 'workflow.md', WORKFLOW_TEXT, args.apply, actions)
    write_missing_file(os_dir / 'config.yaml', CONFIG_TEXT, args.apply, actions)
    for name, text in SPEC_TEXTS.items():
        write_missing_file(os_dir / 'spec' / name, text, args.apply, actions)
    for pointer in ['current_task', 'current_branch', 'current_run']:
        write_missing_file(os_dir / 'runtime' / pointer, '', args.apply, actions)
    for name, headers in INDEX_HEADERS.items():
        write_missing_file(os_dir / 'indexes' / name, '\t'.join(headers) + '\n', args.apply, actions)
    for name, text in ROOT_DOC_DEFAULTS.items():
        write_missing_file(root / name, text, args.apply, actions)
    print_json({'root': root.as_posix(), 'applied': bool(args.apply), 'actions': actions})
    return 0


def current_pointer(root: Path, name: str) -> str:
    path = project_os(root) / 'runtime' / name
    return path.read_text(encoding='utf-8').strip() if path.exists() else ''


def count_rows(path: Path) -> int:
    return len(read_tsv(path)) if path.exists() else 0


def command_status(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    os_dir = project_os(root)
    initialized = (os_dir / 'workflow.md').exists()
    indexes = os_dir / 'indexes'
    payload = {
        'root': root.as_posix(),
        'initialized': initialized,
        'current_task': current_pointer(root, 'current_task') if initialized else '',
        'current_branch': current_pointer(root, 'current_branch') if initialized else '',
        'current_run': current_pointer(root, 'current_run') if initialized else '',
        'counts': {
            'tasks': count_rows(indexes / 'tasks.tsv'),
            'runs': count_rows(indexes / 'runs.tsv'),
            'results': count_rows(indexes / 'results.tsv'),
            'assets': count_rows(indexes / 'assets.tsv'),
        } if initialized else {},
    }
    print_json(payload)
    return 0


def task_dir(root: Path, task_id: str) -> Path:
    return project_os(root) / 'tasks' / task_id


def task_json_path(root: Path, task_id: str) -> Path:
    return task_dir(root, task_id) / 'task.json'


def default_context_manifest() -> str:
    lines = [
        {'type': 'state', 'path': 'PROJECT_STATE.md', 'purpose': 'current project state', 'required': True},
        {'type': 'workflow', 'path': '.project_os/workflow.md', 'purpose': 'project workflow contract', 'required': True},
        {'type': 'data', 'path': 'DATA_ASSETS.md', 'purpose': 'data/source provenance', 'required': False},
        {'type': 'result', 'path': 'RESULTS_INDEX.md', 'purpose': 'human-facing result index', 'required': False},
        {'type': 'decision', 'path': 'DECISIONS.md', 'purpose': 'durable decisions', 'required': False},
    ]
    return ''.join(json.dumps(line, ensure_ascii=False) + '\n' for line in lines)


def command_create_task(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    ensure_initialized(root)
    created = now_iso()
    task_id = args.task_id or f"{datetime.now().strftime('%Y%m%d')}_{slugify(args.title)}"
    tdir = task_dir(root, task_id)
    if tdir.exists():
        raise ProjectOSError(f'Task already exists: {task_id}')
    tdir.mkdir(parents=True)
    (tdir / 'research').mkdir()
    task = {
        'task_id': task_id,
        'title': args.title,
        'status': 'active',
        'kind': args.kind,
        'parent_task_id': args.parent_task_id,
        'branch_id': args.branch_id,
        'created_at': created,
        'updated_at': created,
        'owner': args.owner or '',
        'stage': args.stage,
        'objective_file': 'objective.md',
        'context_manifest': 'context_manifest.jsonl',
        'notes': args.notes or '',
    }
    write_json(tdir / 'task.json', task)
    (tdir / 'objective.md').write_text(f"# Objective\n\n{args.title}\n", encoding='utf-8')
    (tdir / 'context.md').write_text('# Context\n\nAdd task-specific context here.\n', encoding='utf-8')
    (tdir / 'context_manifest.jsonl').write_text(default_context_manifest(), encoding='utf-8')
    (tdir / 'decisions.md').write_text('# Decisions\n\n', encoding='utf-8')
    write_tsv(tdir / 'run_links.tsv', RUN_LINK_HEADERS, [])
    write_tsv(tdir / 'result_links.tsv', RESULT_LINK_HEADERS, [])
    (tdir / 'handoff.md').write_text('# Handoff\n\nCurrent handoff notes.\n', encoding='utf-8')
    refresh_task_index(root)
    if args.set_current:
        set_pointer(root, 'current_task', task_id)
    print_json({'created_task': task_id, 'path': relpath(root, tdir), 'set_current': bool(args.set_current)})
    return 0


def set_pointer(root: Path, name: str, value: str) -> None:
    path = project_os(root) / 'runtime' / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.strip() + ('\n' if value.strip() else ''), encoding='utf-8')


def command_set_current_task(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    ensure_initialized(root)
    if not task_json_path(root, args.task_id).exists():
        raise ProjectOSError(f'Missing task: {args.task_id}')
    set_pointer(root, 'current_task', args.task_id)
    print_json({'current_task': args.task_id})
    return 0


def git_ref(root: Path) -> dict[str, Any]:
    try:
        commit = subprocess.run(['git', '-C', root.as_posix(), 'rev-parse', 'HEAD'], text=True, capture_output=True, check=True).stdout.strip()
        status = subprocess.run(['git', '-C', root.as_posix(), 'status', '--porcelain'], text=True, capture_output=True, check=True).stdout.strip()
        return {'git_commit': commit, 'dirty': bool(status), 'git_available': True}
    except Exception:
        return {'git_commit': None, 'dirty': None, 'git_available': False}


def command_create_run(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    ensure_initialized(root)
    if not task_json_path(root, args.task_id).exists():
        raise ProjectOSError(f'Missing task: {args.task_id}')
    run_id = args.run_id or f"{timestamp()}__{slugify(args.slug)}"
    run_root = root / args.run_root
    rdir = run_root / run_id
    if rdir.exists():
        raise ProjectOSError(f'Run already exists: {relpath(root, rdir)}')
    for subdir in ['', 'inputs', 'outputs', 'plots', 'tables', 'scripts', 'logs', 'docs']:
        (rdir / subdir).mkdir(parents=True, exist_ok=True)
    manifest = {
        'run_id': run_id,
        'task_id': args.task_id,
        'status': 'active',
        'created_at': now_iso(),
        'closed_at': None,
        'code_ref': git_ref(root),
        'environment': {'python': sys.executable, 'conda_env': os.environ.get('CONDA_DEFAULT_ENV'), 'packages': {}},
        'inputs': [],
        'parameters': {},
        'commands': [],
        'outputs': [],
        'metrics': {},
        'result_status': 'draft',
        'promoted_to': [],
        'notes': args.notes or '',
    }
    write_json(rdir / 'RUN_MANIFEST.json', manifest)
    task = read_json(task_json_path(root, args.task_id))
    task['updated_at'] = now_iso()
    write_json(task_json_path(root, args.task_id), task)
    upsert_tsv(task_dir(root, args.task_id) / 'run_links.tsv', RUN_LINK_HEADERS, 'run_id', {
        'run_id': run_id,
        'status': 'active',
        'path': relpath(root, rdir / 'RUN_MANIFEST.json'),
        'created_at': manifest['created_at'],
        'notes': args.notes or '',
    })
    set_pointer(root, 'current_run', run_id)
    refresh_run_index(root)
    print_json({'created_run': run_id, 'path': relpath(root, rdir), 'current_run': run_id})
    return 0


def find_run_manifest(root: Path, run_id: str) -> Path | None:
    for run_root in ['runs', 'analysis_runs']:
        candidate = root / run_root / run_id / 'RUN_MANIFEST.json'
        if candidate.exists():
            return candidate
    for base in [root / 'runs', root / 'analysis_runs']:
        if base.exists():
            for path in base.glob('*/RUN_MANIFEST.json'):
                try:
                    data = read_json(path)
                except ProjectOSError:
                    continue
                if data.get('run_id') == run_id:
                    return path
    return None


def command_close_run(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    ensure_initialized(root)
    if args.status not in RUN_STATUSES:
        raise ProjectOSError(f'Invalid run status: {args.status}')
    manifest_path = find_run_manifest(root, args.run_id)
    if not manifest_path:
        raise ProjectOSError(f'Missing run: {args.run_id}')
    manifest = read_json(manifest_path)
    manifest['status'] = args.status
    manifest['closed_at'] = now_iso()
    if args.notes:
        manifest['notes'] = args.notes
    write_json(manifest_path, manifest)
    refresh_run_index(root)
    print_json({'closed_run': args.run_id, 'status': args.status, 'manifest': relpath(root, manifest_path)})
    return 0


def project_relative_or_absolute(root: Path, raw: str) -> tuple[Path, str]:
    path = Path(raw).expanduser()
    if path.is_absolute():
        resolved = path.resolve()
        return resolved, relpath(root, resolved)
    return (root / path).resolve(), path.as_posix()


def command_register_result(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    ensure_initialized(root)
    if args.status not in RESULT_STATUSES:
        raise ProjectOSError(f'Invalid result status: {args.status}')
    if args.status in {'accepted', 'current', 'release'} and not args.approved:
        raise ProjectOSError('accepted/current/release registration requires --approved')
    manifest_path = find_run_manifest(root, args.run_id)
    if not manifest_path:
        raise ProjectOSError(f'Missing run: {args.run_id}')
    manifest = read_json(manifest_path)
    source_path, stored_path = project_relative_or_absolute(root, args.path)
    if not source_path.exists() and not args.allow_missing:
        raise ProjectOSError(f'Result path does not exist: {source_path}')
    created = now_iso()
    result_id = args.result_id or f"result_{timestamp()}__{slugify(Path(stored_path).stem)}"
    row = {
        'result_id': result_id,
        'task_id': manifest.get('task_id', ''),
        'run_id': args.run_id,
        'status': args.status,
        'type': args.type,
        'path': stored_path,
        'title': args.title or Path(stored_path).name,
        'created_at': created,
        'accepted_at': created if args.status in {'accepted', 'current', 'release'} else '',
        'replaced_by': '',
        'notes': args.notes or '',
    }
    upsert_tsv(project_os(root) / 'indexes' / 'results.tsv', INDEX_HEADERS['results.tsv'], 'result_id', row)
    task_id = str(manifest.get('task_id') or '')
    if task_id and task_dir(root, task_id).exists():
        upsert_tsv(task_dir(root, task_id) / 'result_links.tsv', RESULT_LINK_HEADERS, 'result_id', {
            'result_id': result_id,
            'status': args.status,
            'path': stored_path,
            'run_id': args.run_id,
            'created_at': created,
            'notes': args.notes or '',
        })
    outputs = manifest.setdefault('outputs', [])
    outputs.append({'result_id': result_id, 'path': stored_path, 'status': args.status, 'type': args.type, 'title': row['title']})
    manifest['result_status'] = args.status if args.status != 'draft' else manifest.get('result_status', 'draft')
    write_json(manifest_path, manifest)
    print_json({'registered_result': result_id, 'status': args.status, 'path': stored_path})
    return 0


def command_promote_result(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    ensure_initialized(root)
    results_path = project_os(root) / 'indexes' / 'results.tsv'
    rows = read_tsv(results_path)
    matches = [r for r in rows if r.get('result_id') == args.result_id]
    if not matches:
        raise ProjectOSError(f'Missing result: {args.result_id}')
    row = matches[0]
    source_path, _ = project_relative_or_absolute(root, row['path'])
    dest_path, dest_stored = project_relative_or_absolute(root, args.to)
    if not source_path.exists():
        raise ProjectOSError(f'Source result path does not exist: {source_path}')
    if dest_path.exists() and not args.replace:
        raise ProjectOSError(f'Destination exists; pass --replace to overwrite: {dest_path}')
    payload = {'result_id': args.result_id, 'source': relpath(root, source_path), 'destination': dest_stored, 'applied': bool(args.apply)}
    if not args.apply:
        print_json({'dry_run_promotion': payload})
        return 0
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    if source_path.is_file():
        shutil.copy2(source_path, dest_path)
    else:
        if dest_path.exists():
            shutil.rmtree(dest_path)
        shutil.copytree(source_path, dest_path)
    for existing in rows:
        if existing.get('result_id') == args.result_id:
            existing['status'] = 'current'
            existing['accepted_at'] = existing.get('accepted_at') or now_iso()
            existing['notes'] = (existing.get('notes', '') + '; promoted to ' + dest_stored).strip('; ')
    write_tsv(results_path, INDEX_HEADERS['results.tsv'], rows)
    index = root / 'RESULTS_INDEX.md'
    with index.open('a', encoding='utf-8') as handle:
        handle.write(f"\n## Promoted result: {args.result_id}\n\n- Status: current\n- Source: `{row['path']}`\n- Current path: `{dest_stored}`\n- Source run: `{row.get('run_id', '')}`\n- Promoted at: {now_iso()}\n")
    manifest_path = find_run_manifest(root, row.get('run_id', ''))
    if manifest_path:
        manifest = read_json(manifest_path)
        promoted_to = manifest.setdefault('promoted_to', [])
        promoted_to.append(dest_stored)
        manifest['result_status'] = 'current'
        write_json(manifest_path, manifest)
    print_json({'promoted_result': payload})
    return 0


def refresh_task_index(root: Path) -> None:
    rows: list[dict[str, Any]] = []
    base = project_os(root) / 'tasks'
    if base.exists():
        for task_file in sorted(base.glob('*/task.json')):
            task = read_json(task_file)
            rows.append({
                'task_id': task.get('task_id', task_file.parent.name),
                'status': task.get('status', ''),
                'kind': task.get('kind', ''),
                'branch_id': task.get('branch_id', ''),
                'stage': task.get('stage', ''),
                'title': task.get('title', ''),
                'task_path': relpath(root, task_file.parent),
                'created_at': task.get('created_at', ''),
                'updated_at': task.get('updated_at', ''),
                'notes': task.get('notes', ''),
            })
    write_tsv(project_os(root) / 'indexes' / 'tasks.tsv', INDEX_HEADERS['tasks.tsv'], rows)


def refresh_run_index(root: Path) -> None:
    rows: list[dict[str, Any]] = []
    for run_root in [root / 'runs', root / 'analysis_runs']:
        if not run_root.exists():
            continue
        for manifest_file in sorted(run_root.glob('*/RUN_MANIFEST.json')):
            manifest = read_json(manifest_file)
            rows.append({
                'run_id': manifest.get('run_id', manifest_file.parent.name),
                'task_id': manifest.get('task_id', ''),
                'status': manifest.get('status', ''),
                'result_status': manifest.get('result_status', ''),
                'run_path': relpath(root, manifest_file.parent),
                'created_at': manifest.get('created_at', ''),
                'closed_at': manifest.get('closed_at', ''),
                'notes': manifest.get('notes', ''),
            })
    write_tsv(project_os(root) / 'indexes' / 'runs.tsv', INDEX_HEADERS['runs.tsv'], rows)
    write_tsv(root / 'RUNS_INDEX.tsv', ROOT_RUNS_HEADERS, rows)


def command_refresh_indexes(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    ensure_initialized(root)
    refresh_task_index(root)
    refresh_run_index(root)
    for name in ['branches.tsv', 'results.tsv', 'assets.tsv']:
        path = project_os(root) / 'indexes' / name
        if not path.exists():
            write_tsv(path, INDEX_HEADERS[name], [])
    print_json({'refreshed': ['tasks.tsv', 'runs.tsv', 'RUNS_INDEX.tsv', 'branches.tsv', 'results.tsv', 'assets.tsv']})
    return 0


def validate_headers(path: Path, expected: list[str], errors: list[dict[str, str]]) -> None:
    if not path.exists():
        errors.append({'path': path.as_posix(), 'issue': 'missing index'})
        return
    first = path.read_text(encoding='utf-8', errors='replace').splitlines()[:1]
    actual = first[0].split('\t') if first else []
    if actual != expected:
        errors.append({'path': path.as_posix(), 'issue': f'header mismatch: expected {expected}, got {actual}'})


def validate_context_manifest(root: Path, path: Path, errors: list[dict[str, str]], warnings: list[dict[str, str]]) -> None:
    if not path.exists():
        errors.append({'path': path.as_posix(), 'issue': 'missing context manifest'})
        return
    for idx, line in enumerate(path.read_text(encoding='utf-8').splitlines(), start=1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append({'path': path.as_posix(), 'issue': f'line {idx}: malformed JSONL: {exc}'})
            continue
        for key in ['type', 'path', 'purpose', 'required']:
            if key not in item:
                errors.append({'path': path.as_posix(), 'issue': f'line {idx}: missing key {key}'})
        item_path = str(item.get('path', ''))
        required = bool(item.get('required', False))
        if item_path and not Path(item_path).is_absolute():
            target = root / item_path
        else:
            target = Path(item_path) if item_path else None
        if required and target and not target.exists():
            errors.append({'path': path.as_posix(), 'issue': f'line {idx}: required context path missing: {item_path}'})
        elif target and item_path and not target.exists():
            warnings.append({'path': path.as_posix(), 'issue': f'line {idx}: optional context path missing: {item_path}'})


def command_validate(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    os_dir = project_os(root)
    for path in [os_dir / 'workflow.md', os_dir / 'config.yaml']:
        if not path.exists():
            errors.append({'path': path.as_posix(), 'issue': 'missing required harness file'})
    for subdir in ['spec', 'tasks', 'runtime', 'indexes']:
        if not (os_dir / subdir).exists():
            errors.append({'path': (os_dir / subdir).as_posix(), 'issue': 'missing required harness directory'})
    for pointer in ['current_task', 'current_branch', 'current_run']:
        path = os_dir / 'runtime' / pointer
        if not path.exists():
            errors.append({'path': path.as_posix(), 'issue': 'missing runtime pointer'})
    for name, headers in INDEX_HEADERS.items():
        validate_headers(os_dir / 'indexes' / name, headers, errors)
    for name in ROOT_ENTRY_FILES:
        path = root / name
        if not path.exists():
            warnings.append({'path': path.as_posix(), 'issue': 'missing root human entry file'})
    current_task = current_pointer(root, 'current_task') if (os_dir / 'runtime').exists() else ''
    if current_task and not task_json_path(root, current_task).exists():
        errors.append({'path': (os_dir / 'runtime' / 'current_task').as_posix(), 'issue': f'points to missing task: {current_task}'})
    current_run = current_pointer(root, 'current_run') if (os_dir / 'runtime').exists() else ''
    if current_run and not find_run_manifest(root, current_run):
        errors.append({'path': (os_dir / 'runtime' / 'current_run').as_posix(), 'issue': f'points to missing run: {current_run}'})
    tasks_base = os_dir / 'tasks'
    if tasks_base.exists():
        for task_file in sorted(tasks_base.glob('*/task.json')):
            try:
                task = read_json(task_file)
            except ProjectOSError as exc:
                errors.append({'path': task_file.as_posix(), 'issue': str(exc)})
                continue
            for field in TASK_REQUIRED_FIELDS:
                if field not in task:
                    errors.append({'path': task_file.as_posix(), 'issue': f'missing task field: {field}'})
            if task.get('status') and task.get('status') not in TASK_STATUSES:
                warnings.append({'path': task_file.as_posix(), 'issue': f'nonstandard task status: {task.get("status")}'})
            context_name = task.get('context_manifest', 'context_manifest.jsonl')
            validate_context_manifest(root, task_file.parent / context_name, errors, warnings)
    for run_base in [root / 'runs', root / 'analysis_runs']:
        if run_base.exists():
            for manifest_file in sorted(run_base.glob('*/RUN_MANIFEST.json')):
                try:
                    manifest = read_json(manifest_file)
                except ProjectOSError as exc:
                    errors.append({'path': manifest_file.as_posix(), 'issue': str(exc)})
                    continue
                for field in RUN_REQUIRED_FIELDS:
                    if field not in manifest:
                        errors.append({'path': manifest_file.as_posix(), 'issue': f'missing run field: {field}'})
                if manifest.get('status') and manifest.get('status') not in RUN_STATUSES:
                    warnings.append({'path': manifest_file.as_posix(), 'issue': f'nonstandard run status: {manifest.get("status")}'})
                if manifest.get('task_id') and not task_json_path(root, str(manifest['task_id'])).exists():
                    warnings.append({'path': manifest_file.as_posix(), 'issue': f'run task_id not found in .project_os/tasks: {manifest.get("task_id")}'})
    results_path = os_dir / 'indexes' / 'results.tsv'
    if results_path.exists():
        for row in read_tsv(results_path):
            if row.get('status') and row['status'] not in RESULT_STATUSES:
                warnings.append({'path': results_path.as_posix(), 'issue': f'nonstandard result status: {row.get("status")}'})
            if row.get('path'):
                target, _ = project_relative_or_absolute(root, row['path'])
                if not target.exists():
                    warnings.append({'path': results_path.as_posix(), 'issue': f'result path missing: {row.get("path")}'})
    payload = {'root': root.as_posix(), 'errors': len(errors), 'warnings': len(warnings), 'error_items': errors, 'warning_items': warnings}
    print_json(payload)
    return 1 if errors else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Operate a repository-local research-project-os harness')
    sub = parser.add_subparsers(dest='command', required=True)

    def add_root(p: argparse.ArgumentParser) -> None:
        p.add_argument('--root', default='.', help='Project root')

    p = sub.add_parser('init', help='Create .project_os scaffold; dry-run unless --apply')
    add_root(p)
    p.add_argument('--apply', action='store_true', help='Actually write files')
    p.set_defaults(func=command_init)

    p = sub.add_parser('status', help='Show current harness state')
    add_root(p)
    p.set_defaults(func=command_status)

    p = sub.add_parser('validate', help='Validate harness files, pointers, indexes, tasks, and runs')
    add_root(p)
    p.set_defaults(func=command_validate)

    p = sub.add_parser('create-task', help='Create a task knowledge directory')
    add_root(p)
    p.add_argument('--title', required=True)
    p.add_argument('--kind', default='analysis')
    p.add_argument('--task-id', default='')
    p.add_argument('--branch-id', default='main')
    p.add_argument('--parent-task-id', default=None)
    p.add_argument('--owner', default='')
    p.add_argument('--stage', default='Intake')
    p.add_argument('--notes', default='')
    p.add_argument('--set-current', action='store_true')
    p.set_defaults(func=command_create_task)

    p = sub.add_parser('set-current-task', help='Set runtime/current_task')
    add_root(p)
    p.add_argument('--task-id', required=True)
    p.set_defaults(func=command_set_current_task)

    p = sub.add_parser('create-run', help='Create a run directory and RUN_MANIFEST.json')
    add_root(p)
    p.add_argument('--task-id', required=True)
    p.add_argument('--slug', required=True)
    p.add_argument('--run-id', default='')
    p.add_argument('--run-root', default='runs')
    p.add_argument('--notes', default='')
    p.set_defaults(func=command_create_run)

    p = sub.add_parser('close-run', help='Close/update a run status')
    add_root(p)
    p.add_argument('--run-id', required=True)
    p.add_argument('--status', required=True, choices=sorted(RUN_STATUSES))
    p.add_argument('--notes', default='')
    p.set_defaults(func=command_close_run)

    p = sub.add_parser('register-result', help='Register a run output in results.tsv')
    add_root(p)
    p.add_argument('--run-id', required=True)
    p.add_argument('--path', required=True)
    p.add_argument('--status', default='candidate')
    p.add_argument('--type', default='file')
    p.add_argument('--title', default='')
    p.add_argument('--result-id', default='')
    p.add_argument('--notes', default='')
    p.add_argument('--allow-missing', action='store_true')
    p.add_argument('--approved', action='store_true', help='Required for accepted/current/release status')
    p.set_defaults(func=command_register_result)

    p = sub.add_parser('promote-result', help='Promote a registered result to current/; dry-run unless --apply')
    add_root(p)
    p.add_argument('--result-id', required=True)
    p.add_argument('--to', required=True)
    p.add_argument('--apply', action='store_true')
    p.add_argument('--replace', action='store_true')
    p.set_defaults(func=command_promote_result)

    p = sub.add_parser('refresh-indexes', help='Refresh task and run indexes')
    add_root(p)
    p.set_defaults(func=command_refresh_indexes)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except ProjectOSError as exc:
        print_json({'error': str(exc)})
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
