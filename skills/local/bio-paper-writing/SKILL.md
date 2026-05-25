---
name: bio-paper-writing
description: "Draft or restructure bioinformatics manuscripts from EVIDENCE_PACK.md, figures, tables, analysis summaries, or Chinese notes. Use for 生信论文, 写abstract, 写introduction, 写Results, 写Discussion, 根据结果写论文, 中文实验记录写英文论文. Do not run analyses, validate accessions, or fabricate datasets, statistics, software versions, mechanisms, or citations."
---

# Bioinformatics Manuscript Writing

Use this as the **writing router and manuscript-argument builder** for bioinformatics papers. It consumes evidence; it does not create evidence.

## Boundary

This skill does:

- draft or restructure title, abstract, introduction, Results, Discussion, conclusion, significance, outline, and section plans
- convert Chinese author notes into manuscript-ready English while preserving the underlying evidence boundary
- build a claim-evidence-boundary map from `EVIDENCE_PACK.md`, figure/table inventories, analysis summaries, and author notes
- route specialized work to the narrower bio writing skills when that is safer

This skill does **not**:

- run RNA-seq, enrichment, database, accession, sequence, protein, phylogenetic, or reproduction work
- verify database records or literature facts on its own
- fabricate sample sizes, p values, FDR values, accessions, versions, genome builds, mechanisms, figure panels, or citations
- hide weak evidence behind polished prose

If evidence is missing or ambiguous, mark it explicitly and recommend `bioinfo-evidence-orchestrator` before drafting stronger claims.

## When to open extra files

| File | Open when |
|---|---|
| [references/evidence-pack-input.md](references/evidence-pack-input.md) | Before drafting from an `EVIDENCE_PACK.md` or mixed evidence bundle |
| [references/article-types.md](references/article-types.md) | Choosing the manuscript architecture for omics, resource, method, biomarker, or mechanism papers |
| [references/section-workflows.md](references/section-workflows.md) | Drafting a specific section such as abstract, introduction, Results, Discussion, title, or conclusion |

## Intake

Identify, without over-asking when the context is sufficient:

- requested section or product
- paper type and target journal style, if provided
- study question, organism/system, assay type, dataset inventory, and analysis workflow
- main findings and their evidence strength
- figure/table inventory and intended message of each item
- limitations, validation status, and claims that require softer wording

Minimum safe input for polished prose is at least one supported claim plus its evidence and boundary. If absent, produce a scaffold with placeholders rather than filling the gap.

## Routing

| User asks for | Prefer |
|---|---|
| Full manuscript logic, abstract, introduction, Discussion, title, outline | this skill |
| Figure-by-figure Results prose | `bio-results-writing` |
| Reproducible Methods from workflow provenance | `bio-methods-writing` |
| Editing, polishing, translation, claim calibration | `bio-polishing` |
| Reviewer response or revision letter | `bio-reviewer-response` |
| Data/code availability wording | `bio-data-code-availability` |
| Chinese group-meeting PPT from a bio paper | `bio-paper2ppt` |
| Missing analysis, database validation, or evidence pack creation | `bioinfo-evidence-orchestrator` |

## Workflow

1. **Audit the evidence package.** Separate confirmed facts, inferred interpretation, missing information, and unsupported claims.
2. **Build the argument before drafting.** Use: `In [biological system], we address [gap] by [approach], showing [finding], supported by [evidence], within [boundary].`
3. **Choose architecture by article type.** Use `references/article-types.md` when the paper type is not obvious.
4. **Draft from evidence outward.** Keep each major claim close to the figure/table, dataset, statistic, or literature support that justifies it.
5. **Calibrate language.** Use strong verbs only for direct evidence; use `suggest`, `indicate`, `are consistent with`, or `may` for exploratory or indirect evidence.
6. **Check reproducibility signals.** Dataset accessions/paths, software, versions, design formula, covariates, thresholds, and validation should match the supplied evidence.
7. **Return prose plus audit notes.** Do not bury missing inputs.

## Output format

Default output:

1. `Draft:` requested manuscript prose.
2. `Section outline:` 3-7 bullets when a section or full paper structure is involved.
3. `Claim-evidence-boundary map:` major claims with evidence and status.
4. `Missing information / risk flags:` only material issues.
5. `中文核对:` concise explanation for Chinese author notes or when useful.
