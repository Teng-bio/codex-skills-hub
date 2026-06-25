# Deep paper reading workflow

Use this reference when the user asks to 精读论文 / 逐篇总结 / 每篇文章都要总结 / deep paper note.

## Preferred routing

For each paper:

```text
literature-reading-and-synthesis
  -> deeppapernote
  -> pdf text/table extraction
  -> scientific-critical-thinking
  -> project-literature-bridge matrices
```

If `literature-reading-and-synthesis` or `deeppapernote` is unavailable, emulate the same output manually.

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

## 图表/表格要点

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
- Every project recommendation must include a limitation or risk.
- If the paper is methodologically unrelated but conceptually inspiring, mark evidence as `observed` or `speculative`, not `strong`.
- Never strengthen a project claim only because the paper is high-impact.
