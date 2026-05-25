# Bioinformatics Polishing Checklist

## Terminology consistency

Check that the manuscript uses one consistent form for:

- RNA-seq, scRNA-seq, snRNA-seq, spatial transcriptomics, ATAC-seq, WGS, WES, proteomics, metabolomics
- differential expression, differentially expressed genes, DEGs
- gene set enrichment, over-representation analysis, GSEA, GO, KEGG, Reactome
- count matrix, normalization, batch correction, covariate, design formula
- accession, BioProject, BioSample, GEO, SRA, ENA, PRIDE
- gene symbols, protein names, species names, and italicization where applicable

## Overclaim checks

Flag or soften wording when prose claims:

- causality from association-only omics evidence
- clinical utility without independent validation or prospective testing
- mechanism from enrichment alone
- universal generalizability from a single dataset or small cohort
- pathway activation from gene-list enrichment without orthogonal support
- batch-free or bias-free conclusions without QC evidence

## Safer wording

- `is associated with` rather than `drives` when no perturbation evidence exists
- `is consistent with` rather than `demonstrates` for indirect support
- `may contribute to` rather than `is responsible for` for exploratory mechanisms
- `in this dataset/cohort` when generalizability is limited
- `requires validation` when external or experimental support is absent
