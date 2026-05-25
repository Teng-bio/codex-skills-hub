---
name: bio-paper2ppt
description: "Create Chinese presentation plans or PPTX decks from bioinformatics papers, EVIDENCE_PACK.md, figures, tables, abstracts, or reading notes. Use for 生信论文转PPT, 组会汇报, journal club, 多组学/单细胞/算法论文汇报. Focus on story, workflow, evidence figures, limitations, and discussion questions; do not run analyses or fabricate results."
---

# Bioinformatics Paper to PPT

Use this skill to turn a bioinformatics paper or evidence pack into a Chinese group-meeting or journal-club presentation. It emphasizes workflow, evidence, validation, and limitations.

## Boundary

This skill does:

- build a slide story from a bioinformatics manuscript, evidence pack, PDF, abstract, figures, tables, or reading notes
- select figures as evidence rather than decoration
- write Chinese slide titles, concise bullets, and speaker notes
- create a PPTX when the user provides sufficient source files or asks for a deck artifact
- route general slide design execution to `scientific-slides` when helpful

This skill does **not**:

- run or verify analyses
- fabricate figure messages, statistical values, datasets, methods, or limitations
- turn every paper section into a slide mechanically

If the source evidence is incomplete, build a plan with placeholders and missing-source flags.

## When to open extra files

| File | Open when |
|---|---|
| [references/bio-slide-structures.md](references/bio-slide-structures.md) | Choosing slide structure for omics, method, resource, or biomarker papers |

## Workflow

1. **Identify audience and length.** Default to 10-14 slides for a 15-20 minute Chinese group meeting unless specified.
2. **Classify paper type.** Omics discovery, atlas/resource, computational method, biomarker, mechanism, or review.
3. **Build story spine.** `problem -> gap -> data/workflow -> key evidence -> validation -> contribution -> limitations -> discussion`.
4. **Select figures.** Prefer figures that directly support the story; crop or describe only supplied panels.
5. **Draft slides in Chinese.** Preserve gene/protein/tool/dataset names in English when clearer.
6. **Add speaker notes.** Include what to explain, what to be cautious about, and discussion prompts.
7. **If creating PPTX, audit density and readability.** Avoid text overflow and repeated generic layouts.

## Output format

For planning mode:

```text
Slide plan
| # | Title | Visual/evidence | Key message | Notes |
|---|---|---|---|---|

Missing assets
- ...
```

For deck mode, provide the PPTX path, source assets used, and a short QA report.
