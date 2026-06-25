---
name: scientific-explanatory-schematics
description: Create, critique, or redesign high-quality scientific explanatory schematics for paper notes, project technical-route notes, mechanism/principle diagrams, graphical abstracts, Obsidian/PPT reading aids, and source Figure/Table explanations. Use when users ask to make, explain, judge, improve, redraw, or replace scientific schematics; decide whether to self-draw versus use original paper figures; or mention 技术路线图, 技术机制图, 机制图, 原理图, 技术原理说明图, 流程图, 工作流图, 方法路线图, 项目路线图, 研究框架图, 模型架构图, 证据链图, 混杂控制图, 补充图, 一图流, 图解, 示意图, 配图, 论文Figure讲解, 原文图讲解, Figure/Table拆解, 插图太丑/不好看, 重画/美化插图, 绘图质量, graphical abstract, workflow schematic, mechanism diagram, model architecture figure, figure quality. Prioritizes original Figure/Table evidence, visual hierarchy, evidence boundaries, and optional-only schematics.
---

# Scientific Explanatory Schematics

Use this skill to decide whether a scientific note needs a supplemental schematic and, if yes, to create or redesign it without weakening the evidence chain or adding visual clutter.

## Operating stance

1. **Do not draw by default.** A supplemental schematic is optional. Prefer clear prose plus original Figure/Table when that already explains the point.
2. **Treat original figures as primary evidence.** For paper notes, first insert or unpack the source Figure/Table; self-drawn visuals are only interpretive scaffolds.
3. **Mark interpretation explicitly.** Caption self-drawn visuals as “项目解读示意图，非原文证据” or equivalent. Never let a schematic imply experimental proof.
4. **Reject decorative diagrams.** Avoid generic box-arrow chains, stock-icon decoration, unexplained arrows, dense labels, and gradients that reduce contrast.
5. **Use one figure for one message.** If the figure needs multiple central claims, split it into panels or use text/table instead.
6. **Inspect before embedding.** If a draft is not clearer than the surrounding prose, keep it as a draft or remove it.

## Necessity gate

Create a new schematic only when it does at least one of these jobs:

- integrates evidence scattered across several source figures, tables, or project files;
- explains a technical route, model architecture, decision gate, mechanism, or confounder structure that prose alone makes hard to follow;
- separates what is measured, inferred, trained, ranked, validated, or still uncertain;
- compares methods or candidate explanations more clearly than paragraphs;
- helps a project overview note orient readers before detailed sections.

Do **not** create a new schematic when the source Figure/Table already carries the evidence, the content is a simple list/table, the drawing would only restate headings, or the available evidence cannot support the visual claim.

## Workflow

1. **Triage output.** Choose: no new figure, source Figure/Table insert, source Figure/Table unpacking without image, supplemental vector schematic, or AI-assisted illustration draft.
2. **Inventory evidence.** List the exact paper figures/tables, project documents, matrices, local outputs, and assumptions the visual will summarize.
3. **Select a pattern.** Use `references/design-patterns.md` to choose evidence cascade, parallel multimodal route, architecture map, decision gate, mechanism model, comparison matrix, figure navigator, or confounding map.
4. **Write a brief before drawing.** Use `references/schematic-brief-template.md`; include central message, node list, arrow semantics, evidence boundary, caption, output format, and acceptance checks.
5. **Render deliberately.** Prefer editable SVG/PDF plus PNG preview for Obsidian/PPT reuse. Use AI generation only as a draft renderer when appropriate, never as the scientific authority.
6. **Review against gates.** Use `references/quality-rubric.md` and, for AI/image-generation drafts, `references/ai-generation-qc.md`.
7. **Embed conservatively.** Place the visual near the text it supports; cite source Figure/Table nearby when relevant; include a boundary-aware caption.
8. **Record the decision.** Note whether the figure was kept, removed, replaced by source figure, kept as draft, or redesigned from brief.

## Reference routing

- Read `references/design-patterns.md` when selecting a diagram type or redesigning a poor schematic.
- Read `references/quality-rubric.md` when critiquing an existing figure or deciding whether a draft is acceptable.
- Read `references/schematic-brief-template.md` before creating any new supplemental schematic or image-generation request.
- Read `references/ai-generation-qc.md` before using image-generation, AI diagram, or non-deterministic visual tools.
- Read `references/paper-note-figure-captions.md` when adding or explaining original paper figures/tables in Obsidian paper notes.
- Read `references/obsidian-project-route-figures.md` for project overview notes such as “当前技术路线.md”.

## Obsidian/project-note conventions

- Use relative image paths and verify all links.
- Prefer editable SVG for line art and PNG for preview/embedding.
- Keep captions short but explicit about evidence scope.
- For project overview notes, a clean text route can be better than a poor diagram.
- If the user says a figure is ugly, first remove or demote the bad embed, then propose a redesign brief instead of rushing a replacement.
