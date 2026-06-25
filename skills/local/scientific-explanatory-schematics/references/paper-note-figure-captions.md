# Paper-note figure and table unpacking pattern

For paper notes, original Figure/Table is the evidence anchor. A self-drawn schematic may help orientation, but it must not replace source figure reading.

## High-value source visual rule

Treat a paper Figure/Table as high-value when it materially helps the reader understand at least one of these:

- the method, model architecture, mechanism, or experimental workflow;
- the data/task definition, sample composition, feature construction, or evaluation protocol;
- the main result, key comparison, ablation, benchmark, or error analysis;
- a risk, confounder, negative result, limitation, or claim boundary;
- a result that changes how the user's project should design, rank, validate, or de-risk a method.

For every high-value Figure/Table, choose exactly one documented handling mode:

| Mode | Use when | Required note treatment |
|---|---|---|
| `insert` | A usable source image/crop/table is available and traceable. | Embed it near the relevant section and add the standard unpacking bullets. |
| `text-only-unpack` | The visual is important but cannot be inserted reliably. | Add the text-only block with source location and concrete reason. |
| `repair-needed` | The current note has a broken/mis-cropped/low-resolution asset. | Mark the defect and the extraction/cropping action needed before finalizing. |
| `skip-low-value` | The visual is repetitive, peripheral, or not needed for this note's argument. | Mention only in a compact coverage table if useful; do not create clutter. |

Do not silently skip a high-value Figure/Table. If it is not inserted, the note must say why.

## Figure handling workflow

1. **Inventory source visuals:** list all figures/tables/supplementary figures relevant to the note section.
2. **Choose handling mode:** insert image, crop panel, summarize as text only, repair, or skip as low-value.
3. **Check traceability:** preserve figure number, panel labels, source path/URL, caption context, and enough surrounding legend to avoid ambiguity.
4. **Explain before abstracting:** decode panels, axes, labels, controls, comparisons, and result direction before writing the takeaway.
5. **State boundary:** distinguish author interpretation from what the displayed data directly support.
6. **Fix broken assets:** if the image is missing, low-resolution, or incorrectly cropped, do not pretend it is inserted; mark it for repair or use a textual unpacking block.
7. **Check coverage:** before finalizing, verify that every high-value method/data/result/risk visual is either inserted and explained or explicitly unpacked without image.

## Optional coverage table

Use this table when a paper has many figures/tables or when auditing an existing note:

```markdown
| 原文图表 | 价值判断 | 处理方式 | 位置/原因 |
|---|---|---|---|
| Fig. 1 | 方法总览，高价值 | insert | 方法主线；解释整体流程 |
| Fig. 2 | 主要结果，高价值 | text-only-unpack | 当前裁图缺失坐标轴，需后续补图 |
| Table S3 | 重复参数表，低价值 | skip-low-value | 只在复现清单中提及 |
```

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
- Do not treat a valuable original Figure/Table as handled unless it is either inserted and explained or explicitly unpacked without image.
- Decode the figure before writing the take-home.
- Keep observed results, author interpretation, and project inspiration separate.
- Do not turn correlation, ranking, retrieval, or weak supervision into verified causality.
- If using a crop, preserve enough panel labels and legend context for traceability.
- Prefer one figure block per important source figure rather than one vague paragraph for many figures.
- For inserted high-value images, a one-line caption is not enough; include the standard bullets or equivalent nearby prose that covers the same six points.
- Low-value supplementary or repetitive visuals may be grouped or skipped, but do not use that exception for method overview, main result, ablation, or risk/limitation visuals.
- If a self-drawn schematic is added nearby, caption it as interpretation and keep the source Figure/Table reference close.
