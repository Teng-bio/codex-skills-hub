# Paper note schema

Each paper note should be a Chinese Obsidian Markdown note with a short title.

## Frontmatter

```yaml
---
type: paper-note
status: source-note | deep-read-draft | deep-read
short_title:
full_title:
source_path:
project_modules:
claim_strength: speculative | observed | supported | strong
read_level: metadata-only | abstract-only | partial-text | full-text
---
```

## Required sections

```md
# 短标题

## 一句话主题

## 解决什么问题

## 数据 / 输入 / 输出

## 方法怎么做

## 关键证据

## 原文关键图表讲解

For each high-value original Figure/Table, either insert the usable image/crop or write a text-only unpacking block. Use this pattern:

```md
### Figure/Table X：中文说明标题

![Figure/Table X](relative/path/to/image.png)

- **图中展示什么**：
- **技术路线对应哪一步**：
- **关键结果怎么读**：
- **支持了什么结论**：
- **不能证明什么**：
- **项目启发**：
```

## 对项目的用法

| 项目模块 | 相关性 | 可借鉴点 | 风险 |
|---|---|---|---|

## 证明了什么

## 没证明什么

## 复现或转化需要什么

## Evidence Record

## 链接
```

For full paper reading requests, extend this schema with `references/deep-paper-reading.md`.

## Writing rules

- Keep the note project-facing, not abstract-facing.
- Separate author claims from project interpretation.
- High-value original Figure/Table evidence should be inserted and explained when usable. If not inserted, state the original location, why it cannot be inserted reliably, and whether repair is needed.
- Self-drawn diagrams can only supplement understanding; caption them as project interpretation rather than original evidence.
- Put full bibliographic detail inside the note, not in the note title.
- If only metadata/abstract was read, mark `claim_strength: speculative` and do not use it to support a strong project recommendation.
- If the paper is central to implementation or the user asks for 逐篇精读/每篇文章总结, route through `paper-reading-workflow` -> `deeppapernote` before finalizing the note. If those skills are unavailable, emulate them with `deep-paper-reading.md`.
