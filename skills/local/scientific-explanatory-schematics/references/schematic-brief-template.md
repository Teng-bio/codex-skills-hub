# Schematic brief template

Write this brief before creating a supplemental schematic. The brief is the contract; drawing starts only after the contract is coherent.

```markdown
## Schematic brief

- Working title:
- Output decision: no new figure / source Figure insert / source Figure unpacking / supplemental schematic / AI-assisted draft
- Is a new figure necessary? Why not just text, table, or original figures?
- Audience and use case: Obsidian note / group meeting / PPT / manuscript planning
- Central message in one sentence:
- Evidence sources to summarize:
  - Paper Figure/Table:
  - Project document/matrix:
  - Local data/output:
  - Assumptions or interpretation:
- What the figure may claim:
- What the figure must not imply:
- Diagram pattern: evidence cascade / parallel multimodal route / decision gate / architecture map / comparison matrix / mechanism model / confounding map / figure navigator
- Reading order and entry point:
- Primary nodes, max 5–7 per panel:
- Grouping/layers/lanes:
- Arrow semantics:
  - solid arrow =
  - dashed arrow =
  - blunt/inhibitory arrow =
  - feedback arrow =
- Color roles:
- Visual hierarchy plan: focal element, muted context, emphasis method
- Labels that must appear exactly:
- Labels to avoid or keep in caption instead:
- Accessibility plan: grayscale meaning, colorblind-safe coding, direct labels
- Output format: SVG + PNG / PDF + PNG / PNG only / PPT page image
- File naming and target path:
- Caption draft:
- Acceptance checks:
  - central message visible in 3–5 seconds
  - readable at preview and slide size
  - not a generic box-arrow chain
  - arrow meanings are defined
  - original Figure/Table still cited nearby when relevant
  - self-drawn status marked if applicable
  - no overclaim beyond source evidence
```

## Generation request pattern

When using an image-generation, AI diagram, or slide-generation tool, pass the brief rather than a vague request.

Use a two-stage request:

1. **Architect stage:** ask for layout logic, panels, nodes, arrow semantics, and label list only. Do not render yet.
2. **Renderer stage:** ask for the visual using the approved architecture and exact labels.

Include:

- scientific context;
- exact labels;
- diagram pattern and reading order;
- style constraints: clean white background, high contrast, restrained palette, direct labels, no decorative icons;
- evidence boundary text for the caption;
- aspect ratio and export format;
- what to avoid.

Do not ask for “make it beautiful” without specifying message, evidence, layout, labels, and acceptance checks.

## Compact renderer prompt skeleton

```text
Create an editable scientific schematic, not a decorative illustration.
Central message: <one sentence>.
Layout: <pattern>, reading <direction>, <panel/lane structure>.
Exact labels: <list>.
Arrow meanings: <solid/dashed/etc.>.
Color roles: <role=color family>, colorblind-safe, readable in grayscale.
Style: clean vector, white background, direct labels, no gradients, no tiny text, no stock icons unless semantically necessary.
Evidence boundary: this is an interpretive project schematic, not original experimental evidence.
Avoid: invented data, extra labels, extra arrows, photorealism, crowded panels, red-green coding.
Export: SVG/PDF editable source plus PNG preview.
```
