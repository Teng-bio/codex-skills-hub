---
name: bio-methods-writing
description: "Draft reproducible bioinformatics Methods from workflow provenance, commands, configs, EVIDENCE_PACK.md, software lists, and author notes. Use for 生信Methods, 材料与方法, workflow写法, 可复现方法, RNA-seq/富集/单细胞/系统发育方法写作. Do not run or debug analyses, infer missing parameters, or fabricate versions, genome builds, accessions, or thresholds."
---

# Bioinformatics Methods Writing

Use this skill to turn workflow provenance into a reproducible Methods section. It documents what was done; it does not execute or repair the workflow.

## Boundary

This skill does:

- draft Methods subsections for data sources, preprocessing, QC, statistics, omics analyses, validation, and software availability
- normalize workflow notes into journal-ready prose
- identify missing reproducibility fields
- keep methods aligned with evidence packs and analysis logs

This skill does **not**:

- run pipelines, debug code, validate accession records, or choose parameters after the fact
- fabricate package versions, genome builds, reference databases, thresholds, random seeds, sample exclusions, or command options
- write Results interpretations

If provenance is too incomplete, produce a Methods skeleton plus missing-fields table and route analysis/provenance recovery to `bioinfo-evidence-orchestrator` or reproduction skills.

## When to open extra files

| File | Open when |
|---|---|
| [references/methods-provenance-checklist.md](references/methods-provenance-checklist.md) | Building or auditing the Methods provenance table |

## Workflow

1. **Collect provenance.** Use workflow tables, commands, notebooks, logs, README files, config files, and `EVIDENCE_PACK.md`.
2. **Group by reproducible step.** Typical order: data acquisition, preprocessing, QC, normalization, analysis, statistics, validation, visualization, software.
3. **Write methods with enough detail to repeat.** Include versions, parameters, reference assets, thresholds, and exclusion criteria only when supplied.
4. **Separate methods from results.** Do not include observed outcomes unless needed to define filtering or QC criteria.
5. **Normalize terminology.** Use standard names for repositories, assays, packages, genome assemblies, annotations, and statistical models.
6. **Create a missing-fields table.** Mark what the author must confirm.

## Output format

```text
Methods draft
[subsections]

Reproducibility table
| Step | Tool/package | Version | Key parameters | Input/output | Missing fields |
|---|---|---|---|---|---|

Author confirmation needed
- ...

中文核对
- ...
```
