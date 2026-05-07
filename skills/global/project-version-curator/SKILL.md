---
name: project-version-curator
description: Post-hoc audit and cleanup planning for already messy project directories where many dated, v1/v2/v3, final/current, intermediate, figure, table, and script files are mixed together. Use when Codex is asked to audit existing version clutter, generate an inventory, detect duplicate/conflicting historical files, or create a dry-run cleanup/release plan after the fact. For active development-time guardrails, new runs, promotion, baselines, or branching, use project-flow-guard instead.
---

# Project Version Curator

## Core principle

Never clean by deleting first. Treat the existing project as a working archive, then create a separate release/staging area with a manifest, provenance, and checksums.

Default stance:

1. Inventory first.
2. Classify files as final/candidate/intermediate/archive/temporary.
3. Detect conflicting versions.
4. Create a release/staging folder by copy or symlink.
5. Only delete/quarantine after explicit user approval.

## Recommended workflow

### 1. Read project state

If `PROJECT_STATE.md` exists, read it before changes. If the project uses a state policy, update it after meaningful changes.

### 2. Generate an inventory

Use the bundled script:

```bash
python ~/.codex/skills/project-version-curator/scripts/project_version_curator.py inventory \
  --root . \
  --out project_inventory.tsv
```

Add hashes only for final packaging or duplicate analysis because it is slower:

```bash
python ~/.codex/skills/project-version-curator/scripts/project_version_curator.py inventory \
  --root . \
  --out project_inventory_with_sha256.tsv \
  --sha256
```

### 3. Detect version conflicts

```bash
python ~/.codex/skills/project-version-curator/scripts/project_version_curator.py conflicts \
  --manifest project_inventory.tsv \
  --out version_conflicts.tsv
```

Review groups with many files sharing a similar semantic key, especially files containing `final`, `current`, `v\d+`, or dates.

### 4. Create a publication/release skeleton

Dry run first:

```bash
python ~/.codex/skills/project-version-curator/scripts/project_version_curator.py init-release \
  --root . \
  --name publication_release_YYYYMMDD
```

Apply:

```bash
python ~/.codex/skills/project-version-curator/scripts/project_version_curator.py init-release \
  --root . \
  --name publication_release_YYYYMMDD \
  --apply
```

### 5. For future active development, prefer project-flow-guard

This skill is for post-hoc audit and cleanup planning. For active development, use:

```bash
python ~/.codex/skills/project-flow-guard/scripts/project_flow_guard.py start-run \
  --root . \
  --task "task name"
```

## Directory policy for scientific publication projects

Use this top-level separation:

```text
project/
├── raw/ or reference_library/          # immutable input/reference data
├── runs/                              # timestamped analysis attempts
├── current/                           # small stable pointers/copies to accepted outputs
├── publication_release_YYYYMMDD/      # clean paper/data package
├── scripts/                           # maintained scripts, not one-off throwaways
├── docs/                              # methods, decisions, figure notes
├── archive/                           # old but intentionally retained material
└── PROJECT_STATE.md
```

For a publication release:

```text
publication_release_YYYYMMDD/
├── README.md
├── DATA_DICTIONARY.md
├── MANIFEST.tsv
├── CHECKSUMS.sha256
├── 00_metadata/
├── 01_input_data/
├── 02_processed_data/
├── 03_final_tables/
├── 04_figures/
├── 05_scripts/
├── 06_environment/
└── 99_archive_index/
```

## Naming rules

Prefer deterministic names:

```text
<analysis>__<dataset>__<parameter>__<status>__<YYYYMMDD>.<ext>
```

Examples:

```text
osc_ssn__myxo11refs__score360__final__20260430.svg
osc_phylogeny__all201__fasttree_lg_gamma__final__20260430.pdf
osc_motif_alignment__all201__hslss_windows__final__20260430.tsv
```

Rules:

- Use one date token at the end.
- Avoid stacking `final_final`, `new_final`, `current_v3_final`.
- `current` should be a symlink or tiny pointer/copy, not a new independent version.
- Keep old attempts in `runs/`; do not mix them with accepted outputs.
- Every final figure/table must have a source script and source data path in a manifest.

## Promotion states

Use these statuses consistently:

- `draft`: exploratory, not trusted.
- `candidate`: plausible final, needs review.
- `accepted`: selected for manuscript.
- `release`: copied into publication package.
- `archive`: retained for provenance but not part of the paper.

Avoid using `final` until the file is accepted for a specific manuscript/release.

## Bundled resources

- `scripts/project_version_curator.py`: inventory, conflict detection, release skeleton creation, and new run directory creation.
- `references/versioning_policy.md`: more detailed versioning and release rules.
