---
name: bio-polishing
description: "Polish, restructure, or translate bioinformatics manuscript prose while preserving evidence boundaries. Use for 生信论文润色, 中译英, SCI润色, Results润色, Discussion润色, 摘要润色, 术语统一, overclaim检查. Do not add new analyses, citations, statistics, accessions, software versions, or biological mechanisms not supplied by the user."
---

# Bioinformatics Manuscript Polishing

Use this skill to improve bioinformatics prose at the logic, paragraph, and sentence levels without changing the scientific record.

## Boundary

This skill does:

- polish English or bilingual bioinformatics manuscript text
- restructure paragraphs for clearer claim-evidence-boundary flow
- calibrate overstatements, causal language, novelty claims, and validation claims
- standardize bioinformatics terminology and abbreviations
- provide Chinese explanations of major edits when useful

This skill does **not**:

- add analyses, citations, accessions, statistics, sample sizes, software versions, or mechanisms
- convert a weak or exploratory result into a validated conclusion
- silently change the meaning of a claim

If the draft lacks evidence for a claim, flag it and suggest `bioinfo-evidence-orchestrator` rather than patching the prose.

## When to open extra files

| File | Open when |
|---|---|
| [references/terminology-overclaim-checklist.md](references/terminology-overclaim-checklist.md) | Checking domain terms, causal language, validation language, and section-specific pitfalls |

## Modes

- `light polish`: grammar, concision, flow, and terminology; preserve structure
- `logic polish`: reorder sentences or paragraphs to make claim-evidence-boundary explicit
- `Chinese-to-English`: translate scientific intent, not literal wording; keep gene/protein/tool names stable
- `audit only`: return issues and suggested fixes without rewriting

## Workflow

1. Identify section type: abstract, introduction, Results, Discussion, Methods, title, response, or availability.
2. Diagnose the main failure mode: unclear claim, evidence mismatch, overclaim, terminology inconsistency, sentence clutter, or missing boundary.
3. Preserve all factual values exactly as supplied.
4. Edit from section logic to paragraph logic to sentence polish.
5. Use cautious language for association-only, exploratory, underpowered, or unvalidated findings.
6. Return polished text plus a concise change log and evidence concerns.

## Output format

```text
Polished version
[edited text]

Key edits
- ...

Claim / terminology / overclaim flags
- ...

中文说明
- ...
```
