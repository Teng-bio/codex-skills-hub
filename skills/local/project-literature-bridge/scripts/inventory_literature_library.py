#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


EXTS = {".pdf", ".md", ".txt", ".tsv", ".bib", ".ris"}


def short_title(path: Path) -> str:
    stem = path.stem
    stem = re.sub(r"(?i)[_-]?(arxiv|biorxiv|nat[a-z]*|plos[a-z]*|nucleicacidsresearch|nar|jmr|analchem|chemometrics|frontiers)[_-]?", "_", stem)
    stem = re.sub(r"20\d{2}|19\d{2}", "", stem)
    stem = re.sub(r"[_\-\s]+", "_", stem).strip("_")
    parts = [p for p in stem.split("_") if p]
    if len(parts) >= 2:
        return "_".join(parts[:2])
    return stem[:24] if len(stem) > 24 else stem


def main() -> int:
    ap = argparse.ArgumentParser(description="Inventory an external literature library without modifying it.")
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    root = Path(args.root).expanduser().resolve()
    out = Path(args.out).expanduser()
    rows = []
    for p in sorted(root.rglob("*")):
        if p.is_file() and p.suffix.lower() in EXTS:
            rows.append({
                "short_title": short_title(p),
                "filename": p.name,
                "ext": p.suffix.lower(),
                "topic_dir": p.parent.relative_to(root).as_posix() if p.parent != root else ".",
                "source_path": str(p),
            })

    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["short_title", "filename", "ext", "topic_dir", "source_path"], delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    print(f"rows={len(rows)} out={out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

