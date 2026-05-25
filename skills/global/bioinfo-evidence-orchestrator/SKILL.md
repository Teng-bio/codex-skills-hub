---
name: bioinfo-evidence-orchestrator
description: "Bioinformatics evidence orchestration skill. Use when the user asks to analyze, validate, reproduce, inspect, organize, or prepare evidence from bioinformatics datasets, omics results, gene lists, workflows, database records, accessions, papers, or figures before writing. Routes to existing skills such as tooluniverse, pubmed-database, literature-method-data-miner, tooluniverse-rnaseq-deseq2, tooluniverse-gene-enrichment, sequence/protein/phylogenetics skills, scientific-critical-thinking, and reproduction skills. Produces EVIDENCE_PACK.md, risk tables, figure inventories, and missing-information lists. Do not use for manuscript prose drafting, polishing, reviewer responses, or PPT writing. 中文触发词：生信分析、组学分析、数据库查证、GEO、SRA、accession、QC、富集分析、RNA-seq、DESeq2、整理证据、写论文前整理结果、复现生信流程。"
---

# Bioinformatics Evidence Orchestrator

Use this as a **router and evidence-pack builder** for bioinformatics work. It does not replace specialist database, omics, literature, visualization, or reproduction skills.

## Boundary

This skill does:

- classify the user's bioinformatics task and route to existing specialist skills
- collect confirmed evidence, inferred interpretation, risks, and missing information
- produce writing-ready structured artifacts such as `EVIDENCE_PACK.md`, `RISK_TABLE.md`, `FIGURE_INVENTORY.md`, and `MISSING_INFO.md`
- prepare the handoff to manuscript-writing skills without drafting the manuscript itself

This skill does **not**:

- write abstracts, introductions, Results prose, Discussions, reviewer responses, cover letters, or PPT text
- run specialist analyses itself when a dedicated skill exists
- invent sample sizes, accessions, p values, FDR values, software versions, genome builds, mechanisms, or citations
- make exploratory evidence sound causal or validated

If the user asks for both analysis and writing, first complete the evidence pack, then route to a writing skill in a separate step.

## Routing map

| User intent | Route to |
|---|---|
| PubMed, MeSH, PMID, biomedical literature search | `pubmed-database`; add `auto-deep-research` for broader web/literature discovery |
| Life-science database facts, genes, proteins, diseases, drugs, pathways, variants | `tooluniverse` |
| Literature deep research, mechanism evidence, evidence grading | `tooluniverse-literature-deep-research` |
| “文献是怎么做的”, method/data extraction from papers or supplements | `literature-method-data-miner` |
| RNA-seq count matrix, DESeq2, DEG, design formula, batch effects | `tooluniverse-rnaseq-deseq2`; add `scientific-critical-thinking` for rigor audit |
| GO/KEGG/Reactome/GSEA/ORA/gene-set analysis | `tooluniverse-gene-enrichment` |
| DNA/RNA/protein sequence, FASTA, GenBank, RefSeq, ENA | `tooluniverse-sequence-retrieval` |
| Protein structures, PDB, PDBe, AlphaFold | `tooluniverse-protein-structure-retrieval` |
| Phylogeny, alignments, Newick, orthologs, molecular evolution | `tooluniverse-phylogenetics` |
| Code repository reproduction or README-first paper repo intake | `repo-intake-and-plan` -> `env-and-assets-bootstrap` -> `minimal-run-and-audit` |
| Methodology, statistics, bias, confounding, evidence quality | `scientific-critical-thinking` |
| Publication figures from existing data | `scientific-visualization` or `nature-figure`; keep figure prose separate |
| Multi-step project with durable state | `planning-with-files`, plus `project-state-maintainer` and `project-flow-guard` when outputs/versions matter |

## Workflow

1. **Clarify the task type only if necessary.** If enough context exists, infer the route.
2. **Route to specialist skills** instead of reimplementing their methods.
3. **Capture provenance**: inputs, accessions, software/tools, versions, parameters, references, dates, and output paths when available.
4. **Assess evidence** with labels:
   - `confirmed`: directly supported by supplied data, logs, tables, or verified records
   - `inferred`: reasonable interpretation but not directly shown
   - `missing`: required for a strong claim but absent
   - `unsupported`: stated by the user but not supported by current evidence
5. **Build structured artifacts** using `references/evidence-pack-template.md` when preparing a writing handoff.
6. **Stop before prose writing.** Recommend the appropriate writing skill only after evidence is organized.

## Evidence discipline

- For datasets, preserve original accession/path and state source, organism, assay, sample count, groups, and metadata status.
- For workflows, record command/config/profile, engine, version, container/environment, reference genome, annotation, database versions, seeds, and outputs when known.
- For differential analysis, record normalization, design formula or contrast, covariates, filtering, multiple-testing method, thresholds, and effect-size fields.
- For enrichment, record species, ID namespace, gene universe/background, database/library, method, correction, and threshold.
- For figures, separate the figure's message from the evidence actually shown.
- Always mark missing or ambiguous items instead of filling them in.

## Default output

For short tasks, return:

1. `Route chosen:` specialist skill(s) and why.
2. `Evidence summary:` confirmed facts and key caveats.
3. `Risks / missing information:` items blocking stronger claims.
4. `Next step:` analysis, validation, or writing handoff.

For writing handoff or multi-part tasks, create or draft:

- `EVIDENCE_PACK.md`
- `RISK_TABLE.md`
- `FIGURE_INVENTORY.md`
- `MISSING_INFO.md`

Use the template in `references/evidence-pack-template.md`.
