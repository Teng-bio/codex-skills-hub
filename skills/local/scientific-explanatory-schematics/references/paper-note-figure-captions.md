# Paper-note figure and table unpacking pattern

For paper notes, original Figure/Table is the evidence anchor. A self-drawn schematic may help orientation, but it must not replace source figure reading.

## Figure handling workflow

1. **Inventory source visuals:** list all figures/tables/supplementary figures relevant to the note section.
2. **Choose handling mode:** insert image, crop panel, summarize as text only, or skip if irrelevant.
3. **Check traceability:** preserve figure number, panel labels, source path/URL, caption context, and enough surrounding legend to avoid ambiguity.
4. **Explain before abstracting:** decode panels, axes, labels, controls, comparisons, and result direction before writing the takeaway.
5. **State boundary:** distinguish author interpretation from what the displayed data directly support.
6. **Fix broken assets:** if the image is missing, low-resolution, or incorrectly cropped, do not pretend it is inserted; mark it for repair or use a textual unpacking block.

## Inserted figure block

```markdown
### Figure X：中文说明标题

![Figure X](relative/path/to/image.png)

- **图中展示什么**：说明 panels、坐标轴、对象、比较组、颜色/符号含义。
- **技术路线对应哪一步**：把图连接到方法流程、实验逻辑或模型结构中的具体环节。
- **关键结果怎么读**：先说观察到的模式，再说作者据此提出的解释。
- **支持了什么结论**：只写该图直接支持的 claim。
- **不能证明什么**：写出边界、替代解释或仍需验证的点。
- **项目启发**：该图对当前项目的方法、特征、评估或风险控制有什么可借鉴之处。
```

## Text-only unpacking block

Use this when the figure cannot be legally/稳定地插入、当前图片缺失、或原图过复杂但仍需解释。

```markdown
### Figure X（未插入，文字拆解）：中文说明标题

- **原图位置**：PDF 第 X 页 / DOI / URL / 本地路径。
- **图中展示什么**：...
- **关键结果怎么读**：...
- **与本文技术路线关系**：...
- **证据边界**：...
- **后续是否需要补图**：需要 / 不需要；原因：...
```

## Rules

- Do not summarize only the abstract.
- Decode the figure before writing the take-home.
- Keep observed results, author interpretation, and project inspiration separate.
- Do not turn correlation, ranking, retrieval, or weak supervision into verified causality.
- If using a crop, preserve enough panel labels and legend context for traceability.
- Prefer one figure block per important source figure rather than one vague paragraph for many figures.
- If a self-drawn schematic is added nearby, caption it as interpretation and keep the source Figure/Table reference close.
