#!/usr/bin/env python3
"""Development-time project flow/version guard.

Safe-by-default helper for Codex skills. It creates lightweight ledgers and
isolated run/branch/baseline folders. It never deletes original files.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import os
import re
import shutil
import sys
from pathlib import Path


RUN_SUBDIRS = ["inputs", "outputs", "plots", "tables", "scripts", "logs", "docs"]
FLOW_FILES = {
    "RUNS.tsv": ["run_id", "branch_id", "parent_run_id", "task", "intent", "status", "run_path", "created_at", "closed_at", "note"],
    "BRANCHES.tsv": ["branch_id", "parent_baseline", "status", "branch_path", "created_at", "description"],
    "BASELINES.tsv": ["baseline_id", "source", "status", "baseline_path", "created_at", "description"],
    "FILE_REGISTRY.tsv": ["canonical_path", "source_path", "source_run_id", "branch_id", "state", "checksum", "size_bytes", "updated_at", "note"],
    "PROMOTIONS.tsv": ["promoted_at", "source_path", "canonical_path", "source_run_id", "branch_id", "action", "previous_canonical_path", "reason"],
    "CHANGELOG.tsv": ["timestamp", "session_id", "intent", "changed_paths", "tests", "status", "note"],
}


def stamp() -> str:
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def iso() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


def slugify(text: str, max_len: int = 72) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", text)
    text = text.strip("-")
    if not text:
        text = "task"
    return text[:max_len].strip("-") or "task"


def root_path(s: str | Path) -> Path:
    return Path(s).expanduser().resolve()


def flow_dir(root: Path) -> Path:
    return root / ".project_flow"


def ensure_under(path: Path, root: Path) -> Path:
    path = path.expanduser().resolve()
    root = root.expanduser().resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise SystemExit(f"Refusing path outside project root: {path}") from exc
    return path


def sha256_file(path: Path, chunk: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        while True:
            b = fh.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def rel(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def ensure_tsv(path: Path, fields: list[str]) -> None:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t")
            w.writeheader()


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def append_tsv(path: Path, row: dict[str, str], fields: list[str]) -> None:
    ensure_tsv(path, fields)
    with path.open("a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        w.writerow({k: row.get(k, "") for k in fields})


def init_flow(root: Path) -> None:
    fd = flow_dir(root)
    fd.mkdir(parents=True, exist_ok=True)
    for name, fields in FLOW_FILES.items():
        ensure_tsv(fd / name, fields)
    for pointer in ["ACTIVE_RUN", "ACTIVE_BRANCH"]:
        p = fd / pointer
        if not p.exists():
            p.write_text("", encoding="utf-8")
    decisions = fd / "DECISIONS.md"
    if not decisions.exists():
        decisions.write_text("# Project decision log\n\n", encoding="utf-8")


def get_pointer(root: Path, name: str) -> str:
    p = flow_dir(root) / name
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8").strip()


def set_pointer(root: Path, name: str, value: str) -> None:
    (flow_dir(root) / name).write_text(value.strip() + ("\n" if value.strip() else ""), encoding="utf-8")


def run_base(root: Path, branch_id: str = "") -> Path:
    if branch_id:
        return root / "branches" / branch_id / "runs"
    active_branch = get_pointer(root, "ACTIVE_BRANCH")
    if active_branch:
        return root / "branches" / active_branch / "runs"
    return root / "runs"


def find_run(root: Path, run_id: str) -> dict[str, str] | None:
    init_flow(root)
    for row in read_tsv(flow_dir(root) / "RUNS.tsv"):
        if row.get("run_id") == run_id:
            return row
    return None


def make_manifest(run_path: Path, run_id: str, task: str, intent: str, branch_id: str, parent_run_id: str) -> None:
    text = f"""# Run Manifest: {run_id}

- intent: {intent}
- task: {task}
- branch_id: {branch_id}
- parent_run_id: {parent_run_id}
- status: active
- created_at: {iso()}

## Inputs

| role | path | checksum/status | note |
|---|---|---|---|

## Commands

```text
```

## Outputs

| path | role | state | note |
|---|---|---|---|

## Decisions / notes
"""
    (run_path / "RUN_MANIFEST.md").write_text(text, encoding="utf-8")


def cmd_init(args: argparse.Namespace) -> int:
    root = root_path(args.root)
    init_flow(root)
    for d in ["runs", "branches", "baselines", "current", "release", "archive"]:
        (root / d).mkdir(exist_ok=True)
    print(f"Initialized project flow guard at {flow_dir(root)}")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    root = root_path(args.root)
    init_flow(root)
    print(f"root\t{root}")
    print(f"active_branch\t{get_pointer(root, 'ACTIVE_BRANCH')}")
    print(f"active_run\t{get_pointer(root, 'ACTIVE_RUN')}")
    for name in ["RUNS.tsv", "BRANCHES.tsv", "BASELINES.tsv", "FILE_REGISTRY.tsv", "PROMOTIONS.tsv"]:
        rows = read_tsv(flow_dir(root) / name)
        print(f"{name}\t{len(rows)} rows")
    return 0


def cmd_start_run(args: argparse.Namespace) -> int:
    root = root_path(args.root)
    init_flow(root)
    branch_id = args.branch or get_pointer(root, "ACTIVE_BRANCH")
    parent_run_id = args.parent_run or ""
    run_id = f"{stamp()}__{slugify(args.task)}"
    base = run_base(root, branch_id if args.branch else "")
    run_path = base / run_id
    for d in RUN_SUBDIRS:
        (run_path / d).mkdir(parents=True, exist_ok=False)
    make_manifest(run_path, run_id, args.task, args.intent, branch_id, parent_run_id)
    append_tsv(
        flow_dir(root) / "RUNS.tsv",
        {
            "run_id": run_id,
            "branch_id": branch_id,
            "parent_run_id": parent_run_id,
            "task": args.task,
            "intent": args.intent,
            "status": "active",
            "run_path": rel(run_path, root),
            "created_at": iso(),
            "closed_at": "",
            "note": args.note or "",
        },
        FLOW_FILES["RUNS.tsv"],
    )
    set_pointer(root, "ACTIVE_RUN", run_id)
    print(run_path)
    return 0


def update_run_status(root: Path, run_id: str, status: str, note: str = "") -> None:
    rows = read_tsv(flow_dir(root) / "RUNS.tsv")
    found = False
    for r in rows:
        if r.get("run_id") == run_id:
            r["status"] = status
            r["closed_at"] = iso() if status in {"completed", "failed", "pending_review", "closed"} else r.get("closed_at", "")
            if note:
                r["note"] = note
            found = True
            break
    if not found:
        raise SystemExit(f"Run not found: {run_id}")
    write_tsv(flow_dir(root) / "RUNS.tsv", rows, FLOW_FILES["RUNS.tsv"])


def cmd_close_run(args: argparse.Namespace) -> int:
    root = root_path(args.root)
    init_flow(root)
    run_id = args.run_id or get_pointer(root, "ACTIVE_RUN")
    if not run_id:
        raise SystemExit("No run id provided and no ACTIVE_RUN.")
    update_run_status(root, run_id, args.status, args.note or "")
    if get_pointer(root, "ACTIVE_RUN") == run_id and args.clear_active:
        set_pointer(root, "ACTIVE_RUN", "")
    print(f"{run_id}\t{args.status}")
    return 0


def cmd_register(args: argparse.Namespace) -> int:
    root = root_path(args.root)
    init_flow(root)
    run_id = args.run_id or get_pointer(root, "ACTIVE_RUN")
    branch_id = args.branch or get_pointer(root, "ACTIVE_BRANCH")
    p = ensure_under((root / args.path) if not Path(args.path).is_absolute() else Path(args.path), root)
    checksum = sha256_file(p) if p.is_file() and args.sha256 else ""
    append_tsv(
        flow_dir(root) / "FILE_REGISTRY.tsv",
        {
            "canonical_path": "",
            "source_path": rel(p, root),
            "source_run_id": run_id,
            "branch_id": branch_id,
            "state": args.state,
            "checksum": checksum,
            "size_bytes": str(p.stat().st_size) if p.exists() and p.is_file() else "",
            "updated_at": iso(),
            "note": args.note or args.role or "",
        },
        FLOW_FILES["FILE_REGISTRY.tsv"],
    )
    print(f"registered\t{rel(p, root)}\t{args.state}")
    return 0


def archive_existing(root: Path, dest: Path, run_id: str) -> str:
    if not dest.exists():
        return ""
    archive_dir = root / "archive" / "replaced_current" / stamp()
    archive_dir.mkdir(parents=True, exist_ok=True)
    archived = archive_dir / dest.name
    shutil.copy2(dest, archived)
    return rel(archived, root)


def cmd_promote(args: argparse.Namespace) -> int:
    root = root_path(args.root)
    init_flow(root)
    run_id = args.run_id or get_pointer(root, "ACTIVE_RUN")
    branch_id = args.branch or get_pointer(root, "ACTIVE_BRANCH")
    source = Path(args.source)
    if not source.is_absolute():
        if run_id and not source.exists():
            rr = find_run(root, run_id)
            if rr:
                source = root / rr["run_path"] / source
        else:
            source = root / source
    source = ensure_under(source, root)
    if not source.exists() or not source.is_file():
        raise SystemExit(f"Source file does not exist: {source}")
    current_base = root / "branches" / branch_id / "current" if args.scope == "branch" and branch_id else root / "current"
    dest = current_base / args.canonical
    ensure_under(dest, root)
    dest.parent.mkdir(parents=True, exist_ok=True)
    previous = archive_existing(root, dest, run_id)
    if args.method == "copy":
        shutil.copy2(source, dest)
    elif args.method == "link":
        if dest.exists():
            dest.unlink()
        dest.symlink_to(source)
    elif args.method == "manifest":
        # Do not materialize; write a tiny pointer file.
        dest.write_text(f"source_path\t{rel(source, root)}\n", encoding="utf-8")
    else:
        raise SystemExit(f"Unknown method: {args.method}")
    checksum = sha256_file(source) if args.sha256 else ""
    append_tsv(
        flow_dir(root) / "FILE_REGISTRY.tsv",
        {
            "canonical_path": rel(dest, root),
            "source_path": rel(source, root),
            "source_run_id": run_id,
            "branch_id": branch_id,
            "state": "accepted",
            "checksum": checksum,
            "size_bytes": str(source.stat().st_size),
            "updated_at": iso(),
            "note": args.reason or "",
        },
        FLOW_FILES["FILE_REGISTRY.tsv"],
    )
    append_tsv(
        flow_dir(root) / "PROMOTIONS.tsv",
        {
            "promoted_at": iso(),
            "source_path": rel(source, root),
            "canonical_path": rel(dest, root),
            "source_run_id": run_id,
            "branch_id": branch_id,
            "action": f"promote_to_{args.scope}_current",
            "previous_canonical_path": previous,
            "reason": args.reason or "",
        },
        FLOW_FILES["PROMOTIONS.tsv"],
    )
    print(f"promoted\t{rel(source, root)}\t=>\t{rel(dest, root)}")
    return 0


def list_current_files(root: Path) -> list[Path]:
    current = root / "current"
    if not current.exists():
        return []
    return [p for p in current.rglob("*") if p.is_file()]


def cmd_seal_baseline(args: argparse.Namespace) -> int:
    root = root_path(args.root)
    init_flow(root)
    baseline_id = f"{stamp()}__{slugify(args.name)}"
    bdir = root / "baselines" / baseline_id
    bdir.mkdir(parents=True, exist_ok=False)
    rows = []
    for p in list_current_files(root):
        rows.append(
            {
                "role": "current",
                "path": rel(p, root),
                "size_bytes": str(p.stat().st_size),
                "checksum": sha256_file(p) if args.sha256 else "",
                "note": "",
            }
        )
    with (bdir / "MANIFEST.tsv").open("w", newline="", encoding="utf-8") as fh:
        fields = ["role", "path", "size_bytes", "checksum", "note"]
        w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t")
        w.writeheader()
        w.writerows(rows)
    project_state = root / "PROJECT_STATE.md"
    if project_state.exists():
        shutil.copy2(project_state, bdir / "PROJECT_STATE.snapshot.md")
    (bdir / "BASELINE.md").write_text(
        f"# Baseline: {baseline_id}\n\n- created_at: {iso()}\n- source: {args.source or 'current'}\n- reason: {args.description or args.name}\n\nSee `MANIFEST.tsv`.\n",
        encoding="utf-8",
    )
    append_tsv(
        flow_dir(root) / "BASELINES.tsv",
        {
            "baseline_id": baseline_id,
            "source": args.source or "current",
            "status": "sealed",
            "baseline_path": rel(bdir, root),
            "created_at": iso(),
            "description": args.description or args.name,
        },
        FLOW_FILES["BASELINES.tsv"],
    )
    print(bdir)
    return 0


def cmd_start_branch(args: argparse.Namespace) -> int:
    root = root_path(args.root)
    init_flow(root)
    branch_id = f"{stamp()}__{slugify(args.name)}"
    bpath = root / "branches" / branch_id
    for d in ["inputs", "runs", "current", "docs", "scripts", "release"]:
        (bpath / d).mkdir(parents=True, exist_ok=False)
    (bpath / "PARENT_BASELINE").write_text((args.baseline or "") + "\n", encoding="utf-8")
    (bpath / "BRANCH_STATE.md").write_text(
        f"# Branch: {branch_id}\n\n- created_at: {iso()}\n- parent_baseline: {args.baseline or ''}\n- description: {args.description or args.name}\n\n",
        encoding="utf-8",
    )
    append_tsv(
        flow_dir(root) / "BRANCHES.tsv",
        {
            "branch_id": branch_id,
            "parent_baseline": args.baseline or "",
            "status": "active",
            "branch_path": rel(bpath, root),
            "created_at": iso(),
            "description": args.description or args.name,
        },
        FLOW_FILES["BRANCHES.tsv"],
    )
    if args.set_active:
        set_pointer(root, "ACTIVE_BRANCH", branch_id)
    print(bpath)
    return 0


def newest_baseline(root: Path) -> str:
    rows = read_tsv(flow_dir(root) / "BASELINES.tsv")
    rows = [r for r in rows if r.get("status") == "sealed"]
    if not rows:
        return ""
    rows.sort(key=lambda r: r.get("created_at", ""), reverse=True)
    return rows[0]["baseline_id"]


def cmd_checkpoint_branch(args: argparse.Namespace) -> int:
    root = root_path(args.root)
    init_flow(root)
    if args.promote_source and args.canonical:
        promote_ns = argparse.Namespace(
            root=str(root),
            source=args.promote_source,
            canonical=args.canonical,
            run_id=args.run_id or "",
            branch=args.promote_branch or get_pointer(root, "ACTIVE_BRANCH"),
            scope=args.promote_scope,
            method=args.promote_method,
            reason=args.reason or args.description or "checkpoint-and-branch",
            sha256=args.sha256,
        )
        cmd_promote(promote_ns)
        promoted_run_id = args.run_id or get_pointer(root, "ACTIVE_RUN")
        if promoted_run_id:
            existing = find_run(root, promoted_run_id)
            if existing and existing.get("status") == "active":
                update_run_status(root, promoted_run_id, "completed", "closed by checkpoint-and-branch")
    baseline_id = args.baseline or newest_baseline(root)
    if not baseline_id or args.force_new_baseline:
        # Inline seal baseline behavior.
        ns = argparse.Namespace(root=str(root), name=args.name, source="checkpoint-and-branch", description=args.description or args.name, sha256=args.sha256)
        cmd_seal_baseline(ns)
        baseline_id = newest_baseline(root)
    nsb = argparse.Namespace(root=str(root), name=args.name, baseline=baseline_id, description=args.description or args.name, set_active=True)
    cmd_start_branch(nsb)
    set_pointer(root, "ACTIVE_RUN", "")
    print(f"checkpoint-and-branch\tbaseline={baseline_id}")
    return 0


def cmd_build_release(args: argparse.Namespace) -> int:
    root = root_path(args.root)
    init_flow(root)
    version = slugify(args.version)
    rdir = root / "release" / version
    rdir.mkdir(parents=True, exist_ok=False)
    current = root / "current"
    rows = []
    if current.exists():
        for p in current.rglob("*"):
            if not p.is_file():
                continue
            dest = rdir / p.relative_to(current)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dest)
            rows.append({"release_path": rel(dest, root), "source_current_path": rel(p, root), "size_bytes": str(p.stat().st_size), "checksum": sha256_file(p) if args.sha256 else ""})
    fields = ["release_path", "source_current_path", "size_bytes", "checksum"]
    with (rdir / "MANIFEST.tsv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t")
        w.writeheader()
        w.writerows(rows)
    print(rdir)
    return 0


def cmd_dry_cleanup(args: argparse.Namespace) -> int:
    root = root_path(args.root)
    init_flow(root)
    promoted_runs = {r.get("source_run_id") for r in read_tsv(flow_dir(root) / "PROMOTIONS.tsv") if r.get("source_run_id")}
    print("| Target | Proposed action | Reason |")
    print("|---|---|---|")
    for r in read_tsv(flow_dir(root) / "RUNS.tsv"):
        if r.get("run_id") not in promoted_runs and r.get("status") in {"completed", "failed", "closed", "pending_review"}:
            print(f"| {r.get('run_path')} | REVIEW/ARCHIVE | run status={r.get('status')}; no promoted outputs recorded |")
    print("\nDry run only. No files were moved or deleted.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Development-time project flow/version guard.")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init")
    s.add_argument("--root", default=".")
    s.set_defaults(func=cmd_init)

    s = sub.add_parser("status")
    s.add_argument("--root", default=".")
    s.set_defaults(func=cmd_status)

    s = sub.add_parser("start-run")
    s.add_argument("--root", default=".")
    s.add_argument("--task", required=True)
    s.add_argument("--intent", default="artifact_run")
    s.add_argument("--branch", default="")
    s.add_argument("--parent-run", default="")
    s.add_argument("--note", default="")
    s.set_defaults(func=cmd_start_run)

    s = sub.add_parser("close-run")
    s.add_argument("--root", default=".")
    s.add_argument("--run-id", default="")
    s.add_argument("--status", default="pending_review", choices=["completed", "failed", "pending_review", "closed"])
    s.add_argument("--note", default="")
    s.add_argument("--clear-active", action="store_true")
    s.set_defaults(func=cmd_close_run)

    s = sub.add_parser("register")
    s.add_argument("--root", default=".")
    s.add_argument("--path", required=True)
    s.add_argument("--run-id", default="")
    s.add_argument("--branch", default="")
    s.add_argument("--state", default="draft", choices=["draft", "candidate", "accepted", "release", "archived"])
    s.add_argument("--role", default="")
    s.add_argument("--note", default="")
    s.add_argument("--sha256", action="store_true")
    s.set_defaults(func=cmd_register)

    s = sub.add_parser("promote")
    s.add_argument("--root", default=".")
    s.add_argument("--source", required=True)
    s.add_argument("--canonical", required=True)
    s.add_argument("--run-id", default="")
    s.add_argument("--branch", default="")
    s.add_argument("--scope", default="project", choices=["project", "branch"])
    s.add_argument("--method", default="copy", choices=["copy", "link", "manifest"])
    s.add_argument("--reason", default="")
    s.add_argument("--sha256", action="store_true")
    s.set_defaults(func=cmd_promote)

    s = sub.add_parser("seal-baseline")
    s.add_argument("--root", default=".")
    s.add_argument("--name", required=True)
    s.add_argument("--source", default="")
    s.add_argument("--description", default="")
    s.add_argument("--sha256", action="store_true")
    s.set_defaults(func=cmd_seal_baseline)

    s = sub.add_parser("start-branch")
    s.add_argument("--root", default=".")
    s.add_argument("--name", required=True)
    s.add_argument("--baseline", default="")
    s.add_argument("--description", default="")
    s.add_argument("--set-active", action="store_true")
    s.set_defaults(func=cmd_start_branch)

    s = sub.add_parser("checkpoint-and-branch")
    s.add_argument("--root", default=".")
    s.add_argument("--name", required=True)
    s.add_argument("--baseline", default="")
    s.add_argument("--description", default="")
    s.add_argument("--force-new-baseline", action="store_true")
    s.add_argument("--sha256", action="store_true")
    s.add_argument("--promote-source", default="", help="Optional source output to promote before sealing baseline.")
    s.add_argument("--canonical", default="", help="Canonical current path for --promote-source.")
    s.add_argument("--run-id", default="", help="Run id for optional promotion.")
    s.add_argument("--promote-branch", default="", help="Branch id for optional promotion.")
    s.add_argument("--promote-scope", default="project", choices=["project", "branch"])
    s.add_argument("--promote-method", default="copy", choices=["copy", "link", "manifest"])
    s.add_argument("--reason", default="")
    s.set_defaults(func=cmd_checkpoint_branch)

    s = sub.add_parser("build-release")
    s.add_argument("--root", default=".")
    s.add_argument("--version", required=True)
    s.add_argument("--sha256", action="store_true")
    s.set_defaults(func=cmd_build_release)

    s = sub.add_parser("dry-run-cleanup")
    s.add_argument("--root", default=".")
    s.set_defaults(func=cmd_dry_cleanup)
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
