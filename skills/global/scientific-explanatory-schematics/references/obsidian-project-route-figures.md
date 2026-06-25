# Obsidian project-route figures

Use this reference for project overview notes, especially technical-route pages such as `当前技术路线.md`.

## Principle

A project overview note does not need a diagram by default. Its first job is orientation: what the project is trying to do, what evidence exists, what remains uncertain, and what the next actions are. A poor diagram should be removed or demoted before a replacement is proposed.

## Figure strategy for project overview notes

1. **Start with a text route:** write the current route in 5–8 numbered steps.
2. **Identify the visual bottleneck:** ask which relationship is hard to understand in text.
3. **Use at most 1–3 high-value schematics:** overview route, architecture, evidence/risk. Do not create one giant all-in-one figure.
4. **Keep original evidence nearby:** project schematics should point to paper notes, source figures, evidence matrices, or project outputs.
5. **Caption interpretation:** mark self-drawn project diagrams as interpretation, not paper evidence.

## Recommended figure set

For a literature-bridge vault or NMR × GCF project, these are usually enough:

### 1. Current technical route overview

- **Purpose:** orient readers to the whole project.
- **Pattern:** parallel multimodal route + evidence cascade.
- **Lanes:** NMR/metabolome lane, genome/BGC/GCF lane, linking/ranking lane, validation/risk lane.
- **Should show:** input objects, feature construction, candidate pair generation, weak labels/rules, ranker, validation outputs.
- **Should not show:** detailed neural-network internals or every paper citation.

### 2. Model architecture / scoring schematic

- **Purpose:** explain how candidate NMR–GCF links are scored.
- **Pattern:** architecture map.
- **Should show:** encoders, representation space, scoring/loss/ranker, output candidate list.
- **Should not show:** experimental validation details unless they are inputs to training/evaluation.

### 3. Evidence and risk-control map

- **Purpose:** prevent overclaim by separating evidence from confounders.
- **Pattern:** confounding map or decision gate.
- **Should show:** evidence sources, known confounders, controls, unresolved risks, planned validation.
- **Should not show:** risk as a tiny footnote.

## Handling ugly existing figures

When the user flags a project figure as ugly:

1. Remove or demote the image from the main reading path if it distracts.
2. Preserve the file only if needed for provenance/draft history.
3. Write a schematic brief for a replacement.
4. Ask for or infer the target use case: Obsidian reading, group meeting slide, or manuscript planning.
5. Generate only after the brief passes the necessity gate.

## Asset naming

Use stable names:

```text
_assets/figures/<note-slug>__<figure-id>.svg
_assets/figures/<note-slug>__<figure-id>.png
_assets/figures/<note-slug>__<figure-id>.brief.md
```

Example:

```text
_assets/figures/current-technical-route__nmr-gcf-overview.svg
_assets/figures/current-technical-route__nmr-gcf-overview.png
_assets/figures/current-technical-route__nmr-gcf-overview.brief.md
```

## Caption pattern

```markdown
![当前技术路线示意图](../_assets/figures/current-technical-route__nmr-gcf-overview.png)

> 项目解读示意图，非原文证据。该图概括当前 NMR 特征、GCF 表征、候选关联排序与风险控制的工作路线；具体文献证据见 [[文献支持矩阵]] 和相关论文笔记。
```

## Validation before finalizing

- Verify relative image links in Obsidian.
- Confirm no broken embeds.
- Confirm the caption does not overclaim.
- Confirm the figure is clearer than the numbered text route.
- Confirm source evidence links remain accessible nearby.
