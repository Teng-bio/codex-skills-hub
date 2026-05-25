# Bioinformatics Repositories and Identifier Guide

## Common repository choices

| Asset type | Preferred repositories or records |
|---|---|
| Gene expression arrays or sequencing-derived expression | GEO, ArrayExpress, SRA/ENA/DDBJ as appropriate |
| Raw sequencing reads | SRA, ENA, DDBJ |
| Study-level metadata | BioProject, BioSample, GEO series, ENA study/sample records |
| Proteomics mass spectrometry | PRIDE / ProteomeXchange |
| Metabolomics | MetaboLights, Metabolomics Workbench |
| Genomes/assemblies/annotations | NCBI Assembly, GenBank, ENA, Figshare/Zenodo for derived annotations when suitable |
| Structures/models | PDB, EMDB, AlphaFold-related records, ModelArchive when suitable |
| Processed matrices, source data, supplementary tables | GEO supplementary files, Zenodo, Figshare, Dryad, institutional repository |
| Code, workflows, notebooks | GitHub/GitLab plus archived release in Zenodo or equivalent DOI repository |
| Containers/environments | Docker/Singularity registry plus versioned recipe, or archived environment files |

## Minimum metadata

- title and description
- creators and affiliations
- organism and assay type
- sample metadata table
- file list with raw/processed distinction
- methods or processing summary
- licence or terms of reuse
- version, release date, and identifier
- relation between manuscript figures and source files

## Statement patterns

Use explicit mapping:

`Raw sequencing data generated in this study have been deposited in [repository] under accession [ID]. Processed count matrices and sample metadata are available at [repository/record]. Source data for Figs. [X-Y] are provided as [file/location].`

For code:

`Analysis code and workflow configuration files are available at [repository] and archived at [DOI/release], with the version used for this manuscript corresponding to [tag/commit].`

For restricted data, include the reason, controller, request process, review criteria, and what metadata remain public.
