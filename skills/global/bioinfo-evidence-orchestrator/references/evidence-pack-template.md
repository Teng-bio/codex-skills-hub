# Evidence Pack Template

Use this when handing bioinformatics evidence to writing skills. Do not include polished manuscript prose.

```markdown
# Evidence Pack

## 1. Study question
- Biological question:
- Computational question:
- Claim boundary:

## 2. Dataset inventory
| dataset | accession/path | organism | assay | samples | groups | metadata status | notes |
|---|---|---|---|---:|---|---|---|

## 3. Workflow provenance
| step | tool/package | version | parameters | reference assets | output | status |
|---|---|---|---|---|---|---|

## 4. Statistical design
- comparison/design formula:
- covariates/batch variables:
- normalization:
- multiple testing:
- thresholds:

## 5. Main findings
| finding ID | finding | evidence | figure/table | strength | caveat |
|---|---|---|---|---|---|

## 6. Figure/table inventory
| item | message | source data | key stats | writing use | status |
|---|---|---|---|---|---|

## 7. External validation and database support
| claim/finding | source | identifier | support level | notes |
|---|---|---|---|---|

## 8. Limitations and risks
- ...

## 9. Missing information
- ...

## 10. Writing handoff
- suggested manuscript sections:
- usable claims:
- claims needing softer wording:
- claims not supported:
```

## Strength labels

| Label | Meaning |
|---|---|
| `strong` | Directly supported, statistically controlled, reproducible, and ideally validated |
| `moderate` | Supported by primary analysis but missing external validation or some metadata/control details |
| `weak` | Exploratory, underpowered, assumption-sensitive, or missing key validation |
| `unsupported` | Mentioned but not supported by current evidence |
