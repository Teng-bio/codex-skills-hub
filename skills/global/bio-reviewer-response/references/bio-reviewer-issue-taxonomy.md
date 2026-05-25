# Bioinformatics Reviewer Issue Taxonomy

## Common issue types

| Issue type | What to check before responding | Safe response action |
|---|---|---|
| Batch effect or confounding | metadata, covariates, design formula, QC plots | add analysis evidence or state limitation |
| Multiple testing / FDR | correction method, threshold, number of tests | clarify method or update results |
| Sample size / power | sample counts, cohort balance, independence | temper claim or justify exploratory scope |
| External validation | independent dataset, orthogonal assay, cross-cohort result | add validation if available or state boundary |
| Data leakage | train/test split, feature selection order, repeated samples | explain prevention or rerun with corrected design |
| Reproducibility | versions, parameters, reference genome, code, random seed | add Methods detail or code/data package |
| Biological mechanism | perturbation evidence, literature support, pathway evidence | soften mechanism claim if support is indirect |
| Enrichment interpretation | background set, ID namespace, database version, correction | clarify enrichment design |
| Figure readability | panel labels, legends, source data, statistics | revise figure/legend and state the change |
| Data/code availability | repository, accession, DOI, licence, restrictions | provide availability statement or action plan |

## Response wording rules

- Start by acknowledging the reviewer concern.
- State the concrete change or analysis only if supplied.
- If the concern is valid but unresolved, use `We agree and have clarified this limitation...` rather than pretending completion.
- If disagreeing, explain the scientific reason and indicate any manuscript clarification added.
- Avoid blaming reviewers or claiming constraints such as time as the main reason.
