---
name: bio-data-code-availability
description: "Prepare or audit Data Availability and Code Availability statements for bioinformatics manuscripts. Use for 生信数据可用性, 代码可用性, GEO/SRA/ENA/BioProject/BioSample/PRIDE/Zenodo/GitHub accession, FAIR清单, source data. Do not invent repository records, accessions, DOIs, licences, embargo dates, or access restrictions."
---

# Bioinformatics Data and Code Availability

Use this skill to prepare transparent availability statements and repository action lists for bioinformatics manuscripts.

## Boundary

This skill does:

- draft Data Availability and Code Availability statements from supplied repository records and project notes
- map raw data, processed data, source data, code, workflows, models, and metadata to stable locations
- recommend suitable bioinformatics repositories when records are not yet prepared
- audit FAIR metadata and missing fields

This skill does **not**:

- create repository submissions itself unless separately asked in an implementation task
- fabricate accessions, DOIs, repository names, licences, embargo dates, ethics restrictions, or data-use processes
- rewrite Methods or Results beyond availability wording

If accession validation is required, route to `bioinfo-evidence-orchestrator` or relevant database skills first.

## When to open extra files

| File | Open when |
|---|---|
| [references/bio-repositories.md](references/bio-repositories.md) | Choosing repositories, identifiers, and availability-statement patterns |

## Workflow

1. **Inventory assets.** List generated raw data, processed data, source data for figures, metadata, scripts, notebooks, workflows, containers, trained models, and reused public datasets.
2. **Classify access route.** Public repository, controlled-access repository, within article/supplement, reused public data, institutional repository, or justified request.
3. **Map each asset to an identifier.** Use accession, DOI, release tag, commit hash, or stable URL only if supplied.
4. **Separate data and code.** Draft separate statements unless the target journal requests a combined section.
5. **Add missing-action checklist.** Include repository submission, metadata README, licence, versioned release, and source-data table needs.
6. **Flag weak wording.** `Available upon reasonable request` is weak unless a specific restriction and request process are supplied.

## Output format

```text
Data Availability
[ready-to-paste text]

Code Availability
[ready-to-paste text]

Repository/action checklist
| Asset | Recommended location | Identifier/status | Missing metadata/action |
|---|---|---|---|

Risk flags
- ...

中文核对
- ...
```
