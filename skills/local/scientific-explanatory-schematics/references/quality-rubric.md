# Quality rubric for scientific explanatory schematics

Embed a schematic only if it passes the gates below. A figure that fails a hard gate should be removed, kept as a draft, or redesigned from a brief.

## Hard gates

1. **Necessity:** it explains a relationship that prose, a table, or original figures do not explain well.
2. **Grounding:** every node, arrow, label, and claim traces to a source figure/table, project document, local result, or explicitly marked interpretation.
3. **Boundary:** it states what is measured versus inferred and what the visual does not prove.
4. **Accuracy:** no hallucinated labels, molecules, organisms, axes, datasets, scores, or experimental steps.
5. **Readability:** text remains legible in Obsidian preview and on a PPT slide; labels are not flattened into an uneditable low-resolution bitmap.
6. **Hierarchy:** the reader can identify the entry point, main path, and focal result in 3–5 seconds.
7. **Accessibility:** color is not the only encoding; contrast is sufficient; red/green dependence is avoided.
8. **Restraint:** no decorative clutter, redundant boxes, gratuitous icons, or excessive arrow styles.

## Visual standards

- Use one dominant reading direction: left-to-right, top-to-bottom, circular only for true cycles, or parallel/nested only when comparison/detail levels require it.
- Limit primary nodes to about 5–7 per panel. If more are needed, use grouped lanes or split panels.
- Use semantic color roles, not random color. Example roles: source data, processing, evidence gate, output, risk/uncertainty.
- Use saturation and detail to focus attention: focal elements can be saturated/detailed; context/background should be muted.
- Use consistent arrow meanings. Define solid, dashed, inhibitory, feedback, or uncertainty arrows if more than one type appears.
- Prefer direct labels over distant legends; avoid excessive abbreviations.
- Use consistent shapes, colors, ordering, and orientation within the figure and across a figure set.
- Use whitespace and alignment to show grouping rather than drawing every group boundary.
- Keep caveats in the Markdown caption when they would overcrowd the image.
- Preserve editable source files when possible: SVG/PDF/AI/Figma/PPT source plus PNG preview.

## Review protocol

1. **3-second test:** what is the first thing the viewer notices? It should match the central message.
2. **Reading-path test:** can a viewer tell where to start and where to end without narration?
3. **Arrow-semantics test:** does each arrow mean data flow, time, causality, inference, ranking, inhibition, or feedback? If mixed, are meanings visually distinct and explained?
4. **Evidence audit:** can each visual element be traced to a source or marked as interpretation?
5. **Overclaim audit:** do arrows or captions imply causality when the evidence is correlation, retrieval, ranking, or weak supervision?
6. **Label audit:** are all terms exact, readable, and consistent with the paper/project vocabulary?
7. **Accessibility audit:** check grayscale interpretability and colorblind-safe alternatives; double-code important categories with shape/line style/position where needed.
8. **Output audit:** confirm relative paths, export resolution, editable source, and caption are present.

## Good diagram patterns

- **Evidence cascade:** raw objects → cleaned objects → candidate generation → filtering → ranking → validation.
- **Parallel multimodal route:** two or more evidence lanes converge into a linking/ranking/decision layer.
- **Decision gate:** each stage has pass/fail criteria, evidence input, and next action.
- **Architecture map:** separate encoders, shared representation, scorer/loss, and output; show what is trained versus frozen.
- **Comparison matrix:** methods as rows, capabilities/limits as columns.
- **Mechanism model:** biological or computational mechanism with explicit uncertainty markers.
- **Confounding map:** observed association plus possible confounders and controls.
- **Figure navigator:** source Figure/Table panels mapped to the technical route they support.

## Anti-patterns

- Equal-size boxes connected by identical arrows with no hierarchy.
- Too many nouns but no visual thesis.
- Arrows that imply causality when the evidence is only association.
- Recreating a paper figure poorly instead of using/citing the original.
- Decorative backgrounds, shadows, icons, or gradients that reduce contrast.
- Crowded bilingual text inside the image.
- A caption that claims more than the underlying evidence supports.
- A source-figure crop with missing panel labels, missing legend, or no traceable source.

## Review decision labels

- **Keep:** clear, grounded, readable, and evidence-safe.
- **Keep with caption fix:** visual is acceptable, but evidence boundary or source citation needs repair.
- **Use original figure instead:** source figure already carries the evidence better than a redraw.
- **Keep as draft only:** concept may help, but execution or evidence grounding is not ready for embedding.
- **Remove:** figure adds clutter, overclaims, or duplicates text.
- **Redesign from brief:** concept is useful but current execution is poor.
