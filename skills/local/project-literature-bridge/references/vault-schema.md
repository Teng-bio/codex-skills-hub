# Vault schema and short-title rules

## Default vault layout

```text
<project>_项目文献桥接库/
├── 00-Hub.md
├── 01-项目总览/
│   ├── 当前状态.md
│   ├── 当前技术路线.md
│   ├── 当前问题清单.md
│   └── 下一步任务.md
├── 02-论文说明/
├── 03-项目-论文配对/
├── 04-证据矩阵/
│   ├── 文献支持矩阵.md
│   ├── 方法借鉴矩阵.md
│   └── 风险与未证明点.md
├── 05-源路径索引/
│   ├── 项目报告源路径.md
│   └── 外置文献库索引.md
└── _system/
    ├── registry.md
    └── lint-report.md
```

## Short paper note title rule

Paper note titles should be **short, topic-first, and project-useful**.

Prefer:

```text
CorrelativeMetabologenomics_真菌GCF关联.md
NPLinker_多证据链接.md
DEEPPicker1D_NMR峰拾取.md
SetTransformer_集合编码.md
PhyloAware_系统发育校正.md
```

Avoid:

```text
Correlative metabologenomics of 110 fungi reveals metabolite-gene cluster pairs_NatChemBiol2023_完整长标题.md
```

## Title construction

Use this priority:

```text
核心方法/模型 + "_" + 最短主题
```

Rules:

- Keep 8–24 visible Chinese/English characters when possible.
- Preserve an identifiable method name such as `NPLinker`, `DeepBGC`, `SetTransformer`.
- Add a short topic if the method name alone is ambiguous.
- Remove journal, year, subtitles, and promotional wording from the note title.
- Keep bibliographic detail inside frontmatter or the body, not the filename.

## Link style

Use Obsidian wikilinks for vault notes:

```md
[[NPLinker_多证据链接]]
```

Use absolute source paths only in source index or frontmatter:

```yaml
source_path: "/abs/path/to/paper.pdf"
```

