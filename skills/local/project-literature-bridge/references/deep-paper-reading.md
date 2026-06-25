# Deep paper reading workflow

Use this reference when the user asks to 精读论文 / 逐篇总结 / 每篇文章都要总结 / deep paper note.

## Preferred routing

For each paper:

```text
paper-reading-workflow
  -> deeppapernote
  -> pdf text/table extraction
  -> literature-method-data-miner (method/data/experiment lens)
  -> scientific-critical-thinking (evidence/critique lens)
  -> project-literature-bridge matrices
```

If `paper-reading-workflow` is unavailable, fall back to `literature-reading-and-synthesis` -> `deeppapernote`.
If `deeppapernote` is also unavailable, emulate the same output manually using the checklist below.

## Batch rule

- Do not claim all papers are deeply read until their PDF text has been extracted or the limitation is recorded.
- Process in batches when there are many PDFs.
- Maintain `_system/deep-read-progress.tsv`.

Progress columns:

```tsv
short_title	source_path	status	pages_read	extraction_method	note_path	updated_at	remarks
```

Status values:

- `queued`: selected but not started.
- `text-extracted`: PDF text/tables extracted.
- `deep-read-draft`: note written from extracted text, needs optional figure/table pass.
- `deep-read`: note completed enough for project use.
- `blocked`: PDF unreadable, missing, encrypted, scanned without OCR, or not a real PDF.

## Deep note sections

Add or replace shallow notes with these sections:

```md
## 论文身份

## 一句话结论

## 为什么纳入本项目

## 研究问题

## 数据与实验设计

## 方法流程

## 关键结果

## 原文关键图表讲解

### Figure/Table X：中文说明标题

![Figure/Table X](relative/path/to/image-or-crop.png)

- **图中展示什么**：
- **技术路线对应哪一步**：
- **关键结果怎么读**：
- **支持了什么结论**：
- **不能证明什么**：
- **项目启发**：

> 若高价值原文图无法稳定插入，保留同样的讲解结构，并写明原图位置、未插入原因和后续补图动作。

## 作者结论

## 我们对项目的解释

## 可复用方法

## 对项目模块的映射

| 项目模块 | 可用点 | 证据强度 | 落地动作 | 风险 |
|---|---|---|---|---|

## 局限与偏倚

## 不能支持的说法

## 复现/转化清单

## Evidence Records

## 需要回看原文的位置
```

## Extraction checklist

For each PDF, try in order:

1. `pdftotext -layout`
2. Python `pypdf`
3. Python `pdfplumber` for tables
4. OCR only if text extraction fails and OCR is available

Record the extraction method in progress.

## Evidence strength update

Update frontmatter after reading:

```yaml
status: deep-read-draft | deep-read
claim_strength: speculative | observed | supported | strong
read_level: full-text | partial-text | abstract-only | metadata-only
```

## Writing rules

- Keep the file name short and topic-first.
- Put bibliographic details in `## 论文身份`, not the title.
- Separate `作者结论` from `我们对项目的解释`.
- 尽量插入原文中真正有价值的 Figure/Table，并逐图讲解清楚；方法总览、数据/任务定义、核心结果、关键消融/对比、风险/局限相关图表不可静默跳过。
- 如果高价值原文图无法插入，必须在 `## 原文关键图表讲解` 中做文字拆解，并说明原图位置和未插入原因；不要用自绘图替代原文证据。
- Every project recommendation must include a limitation or risk.
- If the paper is methodologically unrelated but conceptually inspiring, mark evidence as `observed` or `speculative`, not `strong`.
- Never strengthen a project claim only because the paper is high-impact.
