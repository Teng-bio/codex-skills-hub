# AI-assisted scientific figure generation quality control

Use AI image/diagram generation as a draft renderer, not as the scientific authority. For exact technical diagrams, prefer deterministic vector drawing, Figma/Inkscape/Illustrator, BioRender-style editable components, or programmatic SVG.

## When AI assistance is appropriate

Use AI generation only when it helps with:

- first-pass layout exploration;
- polished icon/scene drafts for biological context;
- converting a clear brief or sketch into a cleaner visual;
- presentation-grade explanatory illustrations where exact geometry is less critical.

Avoid AI generation when:

- labels must be exact and numerous;
- the figure contains quantitative data, axes, tables, chemical structures, or precise molecular pathways;
- the model may invent experimental steps, molecules, organisms, or evidence;
- the output cannot be edited or audited;
- the source paper figure would be more accurate and traceable.

## Architect → renderer workflow

1. **Architect:** create the logic first — central message, pattern, panels, nodes, arrow meanings, exact labels, evidence boundary.
2. **Renderer:** generate or draw only after the architecture is stable.
3. **Inspector:** audit labels, arrows, claim scope, accessibility, and editability.
4. **Editor:** correct labels and layout in an editable tool; do not accept the first image as final.
5. **Exporter:** save editable source plus PNG preview.
6. **Embedder:** insert only after caption and evidence boundary are correct.

## AI prompt requirements

A good request must include:

- exact scientific context and target audience;
- one-sentence central message;
- selected diagram pattern and reading order;
- exact labels and forbidden labels;
- node/arrow list and arrow semantics;
- color roles and accessibility constraints;
- output aspect ratio and export target;
- caption/evidence-boundary text;
- explicit prohibitions: no invented data, no extra pathways, no random labels, no decorative icons, no red/green-only coding.

## Inspection checklist

- **Label accuracy:** every label is spelled exactly as requested; no extra terms appear.
- **Structural accuracy:** all required nodes exist; no required nodes are missing; arrow direction is correct.
- **Scientific plausibility:** no invented mechanism, molecule, organism, organelle, or measurement appears.
- **Claim boundary:** the visual distinguishes measured data, inferred links, model predictions, validation, and uncertainty.
- **Editability:** final working file is SVG/PDF/PPT/Figma/BioRender-style editable source when possible.
- **Accessibility:** colorblind-safe, grayscale readable, sufficient contrast, direct labels.
- **Resolution:** PNG preview is crisp at intended Obsidian/PPT size.
- **Copyright/traceability:** it does not imitate or recreate a copyrighted paper figure as if it were original; source inspirations are cited in the note when relevant.

## Acceptance decisions

- **Accept after edit:** the draft is correct and improved by manual cleanup.
- **Use as layout reference only:** the image has useful composition but labels/science are unreliable.
- **Redraw manually:** exact labels/structure matter more than illustration polish.
- **Discard:** hallucinated science, unreadable text, poor hierarchy, or uneditable raster output.

## Caption convention

For self-drawn or AI-assisted visuals in notes:

```markdown
> 项目解读示意图，非原文证据。该图用于解释 <central message>；原始证据见 <Figure/Table/source>。虚线/灰色元素表示 <uncertainty/boundary>。
```

Never caption an AI-assisted schematic as if it were an experimental result.
