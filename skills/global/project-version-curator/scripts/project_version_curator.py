#!/usr/bin/env python3
"""Project version curator utilities.

Safe-by-default helpers for research directories with many mixed versions.
No command deletes or moves original files.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import os
import re
import sys
from pathlib import Path
from typing import Iterable


DATE_RE = re.compile(r"(?:19|20)\d{6}(?:[_-]?\d{4,6})?")
VERSION_RE = re.compile(r"\bv\d+(?:[_-]?[a-z0-9]+)?\b", re.I)
RUN_RE = re.compile(r"(?:run|search_run)[_-]?(?:19|20)\d{6}[_-]?\d{4,6}", re.I)
STATUS_WORDS = {
    "final": "final",
    "current": "current",
    "accepted": "accepted",
    "release": "release",
    "candidate": "candidate",
    "draft": "draft",
    "tmp": "temporary",
    "temp": "temporary",
    "backup": "backup",
    "bak": "backup",
    "old": "archive",
    "archive": "archive",
    "deprecated": "archive",
}
MULTI_SUFFIXES = [
    ".tar.gz",
    ".tar.bz2",
    ".tar.xz",
    ".fastq.gz",
    ".fq.gz",
    ".fasta.gz",
    ".faa.gz",
    ".fa.gz",
    ".tsv.gz",
    ".csv.gz",
]


def now_date() -> str:
    return dt.datetime.now().strftime("%Y%m%d")


def now_stamp() -> str:
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def size_human(n: int) -> str:
    units = ["B", "K", "M", "G", "T"]
    x = float(n)
    for u in units:
        if x < 1024 or u == units[-1]:
            if u == "B":
                return f"{int(x)}B"
            return f"{x:.1f}{u}"
        x /= 1024
    return f"{n}B"


def relpath(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def full_suffix(name: str) -> str:
    lower = name.lower()
    for suf in MULTI_SUFFIXES:
        if lower.endswith(suf):
            return suf
    return "".join(Path(name).suffixes[-1:])


def strip_suffix(name: str) -> str:
    suf = full_suffix(name)
    return name[: -len(suf)] if suf else name


def sha256_file(path: Path, chunk: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        while True:
            b = fh.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def detect_category(rel: str, ext: str) -> str:
    p = rel.lower()
    e = ext.lower()
    if "/plots/" in p or "/figures/" in p or e in {".pdf", ".svg", ".png", ".jpg", ".jpeg", ".tif", ".tiff"}:
        return "figure"
    if "/tables/" in p or e in {".tsv", ".csv", ".xlsx", ".xls"}:
        return "table"
    if "/scripts/" in p or e in {".py", ".r", ".sh", ".ipynb"}:
        return "script"
    if "/docs/" in p or e in {".md", ".txt", ".docx", ".pptx"}:
        return "document"
    if any(x in p for x in ["/alignment/", "/fasta", "/reference", "reference_library"]):
        if e in {".fa", ".faa", ".fna", ".fasta", ".aln", ".gz"} or ".fa" in e:
            return "sequence"
        return "reference"
    if "search_run" in p or "/search_runs/" in p or "/runs/" in p:
        return "run_intermediate"
    if "/logs/" in p or e in {".log", ".err", ".out"}:
        return "log"
    if e in {".nwk", ".tree", ".tre"}:
        return "tree"
    return "other"


def detect_status(name: str, rel: str) -> str:
    blob = f"{name} {rel}".lower()
    hits = []
    for word, status in STATUS_WORDS.items():
        if re.search(rf"(^|[_\-. /]){re.escape(word)}($|[_\-. /])", blob):
            hits.append(status)
    if hits:
        priority = ["release", "accepted", "final", "current", "candidate", "draft", "temporary", "backup", "archive"]
        for p in priority:
            if p in hits:
                return p
    if "/search_runs/" in blob or "/runs/" in blob:
        return "intermediate"
    return "unknown"


def semantic_key(path: Path) -> str:
    stem = strip_suffix(path.name).lower()
    stem = DATE_RE.sub("", stem)
    stem = RUN_RE.sub("", stem)
    stem = VERSION_RE.sub("", stem)
    for word in list(STATUS_WORDS.keys()) + ["readable", "clean", "latest", "updated", "copy", "backup"]:
        stem = re.sub(rf"(^|[_\-.]){re.escape(word)}($|[_\-.])", "_", stem)
    stem = re.sub(r"[_\-.]+", "_", stem).strip("_")
    stem = re.sub(r"_+", "_", stem)
    return stem or strip_suffix(path.name).lower()


def iter_files(root: Path, include_hidden: bool = False) -> Iterable[Path]:
    skip_dirs = {".git", ".snakemake", "__pycache__", ".ipynb_checkpoints"}
    for dirpath, dirnames, filenames in os.walk(root):
        dpath = Path(dirpath)
        if not include_hidden:
            dirnames[:] = [d for d in dirnames if not d.startswith(".") and d not in skip_dirs]
            filenames = [f for f in filenames if not f.startswith(".")]
        else:
            dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        for fn in filenames:
            yield dpath / fn


def cmd_inventory(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    rows = []
    for path in iter_files(root, include_hidden=args.include_hidden):
        try:
            st = path.stat()
        except FileNotFoundError:
            continue
        rp = relpath(path, root)
        ext = full_suffix(path.name)
        date_tokens = ";".join(DATE_RE.findall(path.name))
        version_tokens = ";".join(VERSION_RE.findall(path.name))
        row = {
            "relpath": rp,
            "top_dir": rp.split("/", 1)[0],
            "filename": path.name,
            "size_bytes": str(st.st_size),
            "size_human": size_human(st.st_size),
            "mtime_iso": dt.datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds"),
            "ext": ext,
            "depth": str(rp.count("/") + 1),
            "category": detect_category(rp, ext),
            "status_hint": detect_status(path.name, rp),
            "date_tokens": date_tokens,
            "version_tokens": version_tokens,
            "semantic_key": semantic_key(path),
            "is_hidden": "yes" if any(part.startswith(".") for part in Path(rp).parts) else "no",
            "sha256": sha256_file(path) if args.sha256 else "",
        }
        rows.append(row)
    rows.sort(key=lambda r: r["relpath"])
    write_tsv(args.out, rows)
    print(f"Wrote {args.out} ({len(rows)} files)", file=sys.stderr)
    return 0


def write_tsv(path: str | Path, rows: list[dict]) -> None:
    if rows:
        fields = list(rows[0].keys())
    else:
        fields = []
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        if fields:
            w.writeheader()
            w.writerows(rows)


def read_tsv(path: str | Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def cmd_conflicts(args: argparse.Namespace) -> int:
    rows = read_tsv(args.manifest)
    groups: dict[tuple[str, str, str], list[dict]] = {}
    for r in rows:
        key = (r.get("semantic_key", ""), r.get("ext", ""), r.get("category", ""))
        groups.setdefault(key, []).append(r)

    out = []
    for (key, ext, category), files in groups.items():
        if len(files) < args.min_count:
            continue
        statuses = sorted(set(f.get("status_hint", "") for f in files if f.get("status_hint")))
        versions = sorted(set(f.get("version_tokens", "") for f in files if f.get("version_tokens")))
        dates = sorted(set(f.get("date_tokens", "") for f in files if f.get("date_tokens")))
        total_size = sum(int(f.get("size_bytes") or 0) for f in files)
        files_sorted = sorted(files, key=lambda f: f.get("mtime_iso", ""), reverse=True)
        n_finalish = sum(1 for f in files if f.get("status_hint") in {"release", "accepted", "final", "current"})
        out.append(
            {
                "semantic_key": key,
                "ext": ext,
                "category": category,
                "n_files": str(len(files)),
                "n_final_or_current": str(n_finalish),
                "total_size_bytes": str(total_size),
                "total_size_human": size_human(total_size),
                "statuses": ";".join(statuses),
                "versions": ";".join(v for v in versions if v),
                "dates": ";".join(d for d in dates if d),
                "newest_file": files_sorted[0].get("relpath", ""),
                "all_files": "|".join(f.get("relpath", "") for f in files_sorted[: args.max_files_per_group]),
            }
        )
    out.sort(key=lambda r: (int(r["n_final_or_current"]), int(r["n_files"]), int(r["total_size_bytes"])), reverse=True)
    write_tsv(args.out, out)
    print(f"Wrote {args.out} ({len(out)} conflict groups)", file=sys.stderr)
    return 0


RELEASE_DIRS = [
    "00_metadata",
    "01_input_data/reference_sequences",
    "01_input_data/candidate_sequences",
    "01_input_data/accession_lists",
    "02_processed_data/search_results",
    "02_processed_data/phylogeny",
    "02_processed_data/ssn",
    "02_processed_data/motif_annotation",
    "03_final_tables",
    "04_figures/main_figures",
    "04_figures/supplementary_figures",
    "04_figures/figure_source_files",
    "05_scripts",
    "06_environment",
    "99_archive_index",
]


def cmd_init_release(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    name = args.name.replace("YYYYMMDD", now_date())
    release = root / name
    print(f"Release skeleton: {release}")
    for d in RELEASE_DIRS:
        print(("CREATE " if args.apply else "WOULD CREATE ") + str(release / d))
        if args.apply:
            (release / d).mkdir(parents=True, exist_ok=True)
    files = {
        "README.md": "# Publication release\n\nDescribe data sources, workflow, files, and reproduction steps.\n",
        "DATA_DICTIONARY.md": "# Data dictionary\n\nDocument every final table column.\n",
        "MANIFEST.tsv": "relpath\tcategory\tsource_path\tstatus\tnote\n",
        "CHECKSUMS.sha256": "",
        "99_archive_index/excluded_intermediate_files.tsv": "source_path\treason\n",
        "99_archive_index/original_path_mapping.tsv": "release_path\tsource_path\n",
    }
    for rel, content in files.items():
        p = release / rel
        print(("CREATE " if args.apply else "WOULD CREATE ") + str(p))
        if args.apply:
            p.parent.mkdir(parents=True, exist_ok=True)
            if not p.exists():
                p.write_text(content, encoding="utf-8")
    return 0


def slugify(text: str) -> str:
    s = text.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "analysis"


def cmd_new_run(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    stamp = args.stamp or now_stamp()
    run_name = f"{stamp}__{slugify(args.task)}"
    base = root / args.module / "runs" / run_name if args.module else root / "runs" / run_name
    subdirs = ["inputs", "outputs", "tables", "plots", "logs", "scripts", "docs"]
    print(f"Run folder: {base}")
    for d in subdirs:
        print(("CREATE " if args.apply else "WOULD CREATE ") + str(base / d))
        if args.apply:
            (base / d).mkdir(parents=True, exist_ok=True)
    readme = base / "RUN_MANIFEST.md"
    content = (
        f"# Run manifest\n\n"
        f"- run_id: `{run_name}`\n"
        f"- task: `{args.task}`\n"
        f"- created: `{dt.datetime.now().isoformat(timespec='seconds')}`\n"
        f"- status: `draft`\n\n"
        "## Inputs\n\n## Commands\n\n## Outputs selected for promotion\n\n## Notes\n"
    )
    print(("CREATE " if args.apply else "WOULD CREATE ") + str(readme))
    if args.apply:
        readme.write_text(content, encoding="utf-8")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Audit and govern mixed-version project directories.")
    sub = p.add_subparsers(dest="cmd", required=True)

    inv = sub.add_parser("inventory", help="Generate file inventory TSV.")
    inv.add_argument("--root", default=".")
    inv.add_argument("--out", required=True)
    inv.add_argument("--sha256", action="store_true")
    inv.add_argument("--include-hidden", action="store_true")
    inv.set_defaults(func=cmd_inventory)

    conf = sub.add_parser("conflicts", help="Detect likely mixed versions from an inventory TSV.")
    conf.add_argument("--manifest", required=True)
    conf.add_argument("--out", required=True)
    conf.add_argument("--min-count", type=int, default=2)
    conf.add_argument("--max-files-per-group", type=int, default=25)
    conf.set_defaults(func=cmd_conflicts)

    rel = sub.add_parser("init-release", help="Create a safe publication release skeleton.")
    rel.add_argument("--root", default=".")
    rel.add_argument("--name", default="publication_release_YYYYMMDD")
    rel.add_argument("--apply", action="store_true", help="Actually create files/directories.")
    rel.set_defaults(func=cmd_init_release)

    nr = sub.add_parser("new-run", help="Create an isolated timestamped run folder.")
    nr.add_argument("--root", default=".")
    nr.add_argument("--module", default="", help="Optional module directory under root.")
    nr.add_argument("--task", required=True)
    nr.add_argument("--stamp", default="")
    nr.add_argument("--apply", action="store_true", help="Actually create files/directories.")
    nr.set_defaults(func=cmd_new_run)
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
