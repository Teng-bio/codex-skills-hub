---
name: bio-reviewer-response
description: "Draft, audit, or revise point-by-point reviewer responses for bioinformatics manuscripts. Use for 生信审稿回复, 逐点回复, 大修回复, reviewer质疑batch effect/FDR/外部验证/数据泄露/样本量/方法可复现. Do not claim analyses, revisions, citations, line numbers, figures, or validations were completed unless supplied by the author."
---

# Bioinformatics Reviewer Response

Use this skill to prepare traceable reviewer responses for bioinformatics manuscripts, especially when comments involve omics analysis, statistics, validation, reproducibility, or data availability.

## Boundary

This skill does:

- segment editor and reviewer comments into an auditable tracker
- classify bioinformatics concerns and response actions
- draft professional point-by-point replies from supplied author actions and evidence
- flag when new analysis, evidence-pack updates, or author confirmation is needed

This skill does **not**:

- claim that analyses, validations, line edits, new figures, or citations were completed unless the user supplied them
- run the requested new analysis itself
- invent line numbers, figure panels, supplementary items, reviewer IDs, or journal policy details
- use defensive or dismissive language

If a reviewer asks for new computation or database validation, route that action to `bioinfo-evidence-orchestrator` first, then draft the response after results are available.

## When to open extra files

| File | Open when |
|---|---|
| [references/bio-reviewer-issue-taxonomy.md](references/bio-reviewer-issue-taxonomy.md) | Classifying reviewer comments and mapping them to safe response actions |

## Workflow

1. **Preserve comments.** Keep each editor/reviewer point faithful and assign IDs such as `E.1`, `R1.1`, `R2.3`.
2. **Classify issues.** Identify statistics, batch effects, multiple testing, validation, reproducibility, data/code availability, biological interpretation, figures, or writing.
3. **Map action state.** Use `completed`, `planned`, `not feasible with justification`, `clarification only`, or `AUTHOR_INPUT_NEEDED`.
4. **Draft response strategy.** Lead with changes and evidence; disagree only with a concise scientific reason.
5. **Cross-reference supplied materials.** Use only provided line numbers, figure panels, tables, supplements, or manuscript changes.
6. **Run response QA.** Every concern should have a response, action, and unresolved flag if needed.

## Output format

```text
Response strategy summary
- Decision type:
- Main bioinformatics risks:
- Recommended order:

Comment-response tracker
| ID | Reviewer concern | Bioinfo issue type | Proposed action | Evidence/change supplied | Missing input |
|---|---|---|---|---|---|

Draft point-by-point response
[editor-readable response]

Actions for bioinfo evidence layer
- ...

中文核对
- ...
```
