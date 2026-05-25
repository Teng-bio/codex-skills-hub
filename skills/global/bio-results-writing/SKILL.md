---
name: bio-results-writing
description: "Write bioinformatics Results sections from figures, tables, EVIDENCE_PACK.md, analysis summaries, and Chinese result notes. Use for 生信Results, 根据图表写结果, RNA-seq结果写作, 富集结果写作, 单细胞/多组学结果段落. Do not run analyses, change statistics, or fabricate p values, FDR, sample sizes, figure panels, or mechanisms."
---

# Bioinformatics Results Writing

Use this skill for figure- and table-grounded Results prose. It reports what was observed; it does not perform analyses or interpret beyond the data.

## Boundary

This skill does:

- write Results subsections and figure-by-figure paragraphs from supplied evidence
- organize results into an evidence ladder rather than raw analysis chronology
- calibrate claims by statistical support, validation, and figure status
- produce missing-information flags for incomplete figures, tables, or statistics

This skill does **not**:

- run DESeq2, enrichment, clustering, survival, model evaluation, or database validation
- invent FDR, p values, log fold changes, sample counts, accession IDs, panel labels, or mechanisms
- write the Discussion unless the user explicitly asks for a brief transition sentence

## When to open extra files

| File | Open when |
|---|---|
| [references/results-evidence-checklist.md](references/results-evidence-checklist.md) | Auditing figures/tables before writing or when evidence is incomplete |

## Workflow

1. **Inventory evidence units.** For each figure/table, capture panel, assay, comparison, statistic, and intended message.
2. **Sort by argument logic.** Prefer `dataset/QC -> global pattern -> focused finding -> pathway/module -> validation` over tool chronology.
3. **Write claim-first subsection openings.** Each paragraph should start with what the result shows, then provide evidence.
4. **Keep Results distinct from Discussion.** State observations and immediate data-grounded meaning; avoid broad causal or translational claims.
5. **Use quantitative details exactly as supplied.** If details are absent, use qualitative wording and flag the missing field.
6. **Check figure callouts.** Every panel referenced in prose must exist in the supplied inventory.
7. **Return draft plus audit table.** Include unresolved evidence gaps.

## Output format

```text
Results draft
[section or paragraphs]

Figure-to-text map
| Figure/table | Written claim | Evidence used | Missing fields |
|---|---|---|---|

Overclaim / missing-stat flags
- ...

中文核对
- ...
```
