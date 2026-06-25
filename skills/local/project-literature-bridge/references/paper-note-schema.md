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
- Put full bibliographic detail inside the note, not in the note title.
- If only metadata/abstract was read, mark `claim_strength: speculative` and do not use it to support a strong project recommendation.
- If the paper is central to implementation or the user asks for 逐篇精读/每篇文章总结, route through `paper-reading-workflow` -> `deeppapernote` before finalizing the note. If those skills are unavailable, emulate them with `deep-paper-reading.md`.
