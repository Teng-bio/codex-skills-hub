# Methods Provenance Checklist

## Data source fields

- repository and accession/path
- organism, tissue, disease/condition, assay, platform
- sample count, group definitions, inclusion/exclusion rules
- ethics/consent statement if human or clinical data are involved
- date of database download when relevant

## Workflow fields

- tool or package name
- version and environment/container if known
- command, configuration, or key parameters
- reference genome, annotation, transcriptome, database, or library version
- random seed or reproducibility setting when relevant
- input files and output files

## Statistics fields

- design formula or model
- contrast/comparison
- covariates and batch variables
- normalization and filtering
- multiple-testing correction
- thresholds for reporting
- validation split, cross-validation, external cohort, or test set if used

## Common Methods subsections

- Public data acquisition
- Quality control and preprocessing
- Differential expression or abundance analysis
- Gene-set, pathway, or network enrichment
- Single-cell/spatial processing if applicable
- Sequence, structure, or phylogenetic analysis if applicable
- Statistical analysis
- Visualization and software
- Data and code availability, usually routed to `bio-data-code-availability`
