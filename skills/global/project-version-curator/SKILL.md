---
name: project-version-curator
description: Post-hoc audit, cleanup planning, and release/staging preparation for already messy project directories where many dated, v1/v2/v3, final/current, intermediate, figure, table, and script files are mixed together. Use when Codex is asked to audit existing version clutter, generate an inventory, detect duplicate/conflicting historical files, map files to accepted/candidate/legacy status using project indexes, or create a dry-run cleanup/release plan after the fact. For active development-time guardrails, new runs, promotion, baselines, or branching, use project-flow-guard instead.
---

# Project Version Curator

## Core principle

Never clean by deleting first. Treat the existing project as a working archive, then create a separate release/staging area with a manifest, provenance, and checksums.

This is a **post-hoc curator**. It must respect the active project maintenance framework rather than replace it:

- `PROJECT_STATE.md` is the thin state entry point.
- `RESULTS_INDEX.md` is more authoritative than filenames for current/candidate/legacy results.
- `DECISIONS.md` explains why a result/route is accepted, legacy, or superseded.
- `DATA_ASSETS.md` explains authoritative data paths and copy restrictions.
- `RUNS_INDEX.tsv`, `.project_flow/`, and `RUN_MANIFEST.json` describe generated-run provenance.

Canonical curation outputs should be Markdown, TSV, and JSON. SQLite/HTML may be generated for query/display only, not as canonical cleanup sources, unless the user explicitly changes policy.

Default stance:

1. Inventory first.
2. Cross-check project indexes before trusting filename hints such as `final` or `current`.
3. Classify files as accepted/candidate/legacy/superseded/intermediate/archive/temporary.
4. Detect conflicting versions.
5. Create a release/staging folder by copy or symlink.
6. Only delete/quarantine after explicit user approval.

## Recommended workflow

### 1. Read project state

If `PROJECT_STATE.md` exists, read it before changes. If the project uses a state policy, update it after meaningful changes.

Also read these if present and relevant:

- `RESULTS_INDEX.md`
- `DECISIONS.md`
- `DATA_ASSETS.md`
- `RUNS_INDEX.tsv`
- `.project_flow/FILE_REGISTRY.tsv`
- `.project_flow/PROMOTIONS.tsv`
- `.project_flow/RUNS.tsv`

Treat `RESULTS_INDEX.md` / `current/` / registry entries as stronger evidence than file names like `final`, `latest`, or `current_v3`.

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

Important: `final` in a filename is only a filename hint. Prefer `accepted`, `release`, `legacy`, or `superseded` states from indexes/registries when available.

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

For non-publication cleanup planning, produce a dry-run curation plan instead of moving files:

```text
CURATION_PLAN.md          # human-readable plan: keep/promote/archive/quarantine candidates
project_inventory.tsv     # complete inventory
version_conflicts.tsv     # conflict groups
curation_summary.json     # optional machine-readable summary
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
├── RESULTS_INDEX.md                   # human entry point for accepted/candidate/legacy outputs
├── DECISIONS.md                       # decision log
├── DATA_ASSETS.md                     # data source/path/copying rules
├── RUNS_INDEX.tsv                     # concise run index, if used
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
- `current` should be a symlink, tiny pointer, or explicitly promoted copy, not a new independent version.
- Keep old attempts in `runs/`; do not mix them with accepted outputs.
- Every accepted/release figure/table must have a source script and source data path in a manifest or index.
- Do not introduce new `final_*` names during cleanup; map old `final` files to `accepted`, `release`, `legacy`, or `superseded`.

## Promotion states

Use these statuses consistently:

- `draft`: exploratory, not trusted.
- `candidate`: plausible accepted output, needs review.
- `accepted`: selected for manuscript.
- `release`: copied into publication package.
- `archive`: retained for provenance but not part of the paper.
- `legacy`: old route retained for comparison/provenance, not the active result.
- `superseded`: replaced by a newer accepted/candidate output.

Avoid using `final` as a new status. If old filenames contain `final`, treat it as a clue to audit, not proof of acceptance.

## Handoff updates

After a meaningful curation or release-planning turn:

1. Update `PROJECT_STATE.md` with only a concise summary and next step.
2. Update `RESULTS_INDEX.md` if accepted/candidate/legacy result entry points changed.
3. Update `DECISIONS.md` if a cleanup/release/legacy decision was made.
4. Never delete/quarantine files without explicit user approval after a dry-run plan.

## Bundled resources

- `scripts/project_version_curator.py`: inventory, conflict detection, release skeleton creation, and new run directory creation.
- `references/versioning_policy.md`: more detailed versioning and release rules.
