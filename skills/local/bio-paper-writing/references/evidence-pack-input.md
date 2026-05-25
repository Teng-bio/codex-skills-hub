# Evidence-Pack Input Guide

Use this guide before drafting from `EVIDENCE_PACK.md` or a mixed bundle of figures, tables, notes, and analysis outputs.

## Minimum fields for safe drafting

| Field | Needed for | If missing |
|---|---|---|
| Study question and claim boundary | abstract, introduction, Discussion | draft only a scaffold and request author confirmation |
| Dataset inventory | all manuscript claims | avoid sample-size, cohort, organism, and accession claims |
| Workflow provenance | Methods and reproducibility statements | route to `bio-methods-writing` or flag as missing |
| Statistical design | Results and Discussion | avoid precise inferential claims |
| Main findings table | all sections | do not infer findings from file names alone |
| Figure/table inventory | Results and PPT | write only high-level placeholders |
| External validation/database support | Discussion and rebuttal | use cautious language |
| Limitations and risks | Discussion, reviewer response | expose rather than hide |

## Evidence status language

| Status | Writing treatment |
|---|---|
| `strong` | direct claim is acceptable if evidence details are provided |
| `moderate` | claim can be stated with boundary or validation caveat |
| `weak` | use exploratory language and avoid broad implications |
| `unsupported` | do not write as a result; move to missing information or future work |

## Missing-information policy

- Use `[AUTHOR_CONFIRM: ...]` for facts the author likely knows.
- Use `[EVIDENCE_NEEDED: ...]` for claims requiring data, statistics, or provenance.
- Use `[CHECK_WITH_BIOINFO_AGENT: ...]` when database, accession, or analysis verification is needed.
- Never convert a missing field into smooth prose.
