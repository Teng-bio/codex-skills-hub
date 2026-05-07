#!/usr/bin/env python3
"""
Create, inspect, and update a canonical PROJECT_STATE.md file.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


SECTION_ORDER: list[tuple[str, str, bool]] = [
    ("project_summary", "Project Summary", False),
    ("current_goal", "Current Goal", False),
    ("current_status", "Current Status", True),
    ("key_paths", "Key Paths", True),
    ("decisions", "Decisions", True),
    ("recent_changes", "Recent Changes", True),
    ("open_problems", "Open Problems", True),
    ("next_step", "Next Step", True),
    ("resume_prompt", "Resume Prompt", False),
]

DEFAULTS: dict[str, Any] = {
    "project_summary": "TODO",
    "current_goal": "TODO",
    "current_status": ["TODO"],
    "key_paths": [],
    "decisions": [],
    "recent_changes": [],
    "open_problems": [],
    "next_step": ["TODO"],
    "resume_prompt": "TODO",
}


def detect_project_root(cwd: Path) -> Path:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
        )
        root = result.stdout.strip()
        if root:
            return Path(root).resolve()
    except Exception:
        pass
    return cwd.resolve()


def normalize_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        stripped = value.strip()
        return [stripped] if stripped else []
    if isinstance(value, list):
        out: list[str] = []
        for item in value:
            text = str(item).strip()
            if text:
                out.append(text)
        return out
    text = str(value).strip()
    return [text] if text else []


def normalize_scalar(value: Any, default: str = "TODO") -> str:
    if value is None:
        return default
    text = str(value).strip()
    return text or default


def blank_state() -> dict[str, Any]:
    return {
        "project_summary": DEFAULTS["project_summary"],
        "current_goal": DEFAULTS["current_goal"],
        "current_status": list(DEFAULTS["current_status"]),
        "key_paths": list(DEFAULTS["key_paths"]),
        "decisions": list(DEFAULTS["decisions"]),
        "recent_changes": list(DEFAULTS["recent_changes"]),
        "open_problems": list(DEFAULTS["open_problems"]),
        "next_step": list(DEFAULTS["next_step"]),
        "resume_prompt": DEFAULTS["resume_prompt"],
    }


def parse_markdown(path: Path) -> dict[str, Any]:
    state = blank_state()
    if not path.exists():
        return state

    lines = path.read_text(encoding="utf-8").splitlines()
    current_key: str | None = None
    buckets: dict[str, list[str]] = {key: [] for key, _, _ in SECTION_ORDER}

    heading_map = {heading: key for key, heading, _ in SECTION_ORDER}

    for line in lines:
        if line.startswith("## "):
            heading = line[3:].strip()
            current_key = heading_map.get(heading)
            continue
        if current_key is None:
            continue
        buckets[current_key].append(line)

    for key, _, is_list in SECTION_ORDER:
        raw_lines = buckets[key]
        if is_list:
            items = []
            for line in raw_lines:
                stripped = line.strip()
                if stripped.startswith("- "):
                    items.append(stripped[2:].strip())
                elif stripped:
                    items.append(stripped)
            state[key] = items or list(DEFAULTS[key])
        else:
            text = "\n".join(line.rstrip() for line in raw_lines).strip()
            state[key] = text or DEFAULTS[key]

    return state


def render_markdown(state: dict[str, Any]) -> str:
    parts = ["# PROJECT_STATE", ""]
    for key, heading, is_list in SECTION_ORDER:
        parts.append(f"## {heading}")
        if is_list:
            items = normalize_list(state.get(key))
            if not items:
                items = list(DEFAULTS[key])
            parts.extend(f"- {item}" for item in items)
        else:
            parts.append(normalize_scalar(state.get(key), DEFAULTS[key]))
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def ensure_state_file(project_root: Path) -> Path:
    project_root.mkdir(parents=True, exist_ok=True)
    target = project_root / "PROJECT_STATE.md"
    if not target.exists():
        target.write_text(render_markdown(blank_state()), encoding="utf-8")
    return target


def update_state(project_root: Path, payload: dict[str, Any]) -> Path:
    target = ensure_state_file(project_root)
    state = parse_markdown(target)
    for key, _, is_list in SECTION_ORDER:
        if key not in payload:
            continue
        state[key] = normalize_list(payload[key]) if is_list else normalize_scalar(payload[key], DEFAULTS[key])
    target.write_text(render_markdown(state), encoding="utf-8")
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description="Maintain PROJECT_STATE.md in a project root.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_ensure = sub.add_parser("ensure", help="Create PROJECT_STATE.md if missing.")
    p_ensure.add_argument("--project-root", type=Path, default=None)

    p_show = sub.add_parser("show", help="Print structured PROJECT_STATE data as JSON.")
    p_show.add_argument("--project-root", type=Path, default=None)

    p_update = sub.add_parser("update", help="Merge a JSON payload into PROJECT_STATE.md.")
    p_update.add_argument("--project-root", type=Path, default=None)
    p_update.add_argument("--json", required=True, help="Partial JSON payload with updated sections.")

    args = parser.parse_args()
    root = detect_project_root(Path.cwd()) if args.project_root is None else args.project_root.resolve()

    if args.command == "ensure":
        path = ensure_state_file(root)
        print(str(path))
        return

    if args.command == "show":
        path = ensure_state_file(root)
        print(json.dumps(parse_markdown(path), ensure_ascii=False, indent=2))
        return

    if args.command == "update":
        payload = json.loads(args.json)
        path = update_state(root, payload)
        print(str(path))
        return


if __name__ == "__main__":
    main()
