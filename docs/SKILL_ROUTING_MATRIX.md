# Skill Routing Matrix for Bioinformatics Agent and Writing Skills

更新日期：2026-05-25

用途：定义用户请求应触发哪个 skill，避免“生信分析”和“论文写作”混在一起。

---

## 0. 当前已落地本地 skills

本轮已在 `skills/local/` 中落地两条线：

```text
生信证据线：
  bioinfo-evidence-orchestrator

自动路由线：
  bio-research-auto-router

论文写作线：
  bio-paper-writing
  bio-results-writing
  bio-methods-writing
  bio-polishing
  bio-reviewer-response
  bio-data-code-availability
  bio-paper2ppt
```

执行红线保持不变：证据线不写 manuscript prose；写作线不跑分析、不验证 accession、不补造统计或机制。

---

## 1. 总体路由原则

```text
分析、验证、数据库、QC、复现、证据整理 -> 生信 Agent / 已有生信工具 skill
论文段落、润色、审稿回复、PPT、投稿材料 -> 写作 skill
复杂多阶段项目 -> planning-with-files 作为任务内核
```

禁止混淆：

- 生信 Agent 不写 abstract、Results、Discussion、rebuttal。
- 写作 skill 不跑 RNA-seq、富集、数据库验证、workflow 复现。
- 如果用户同时要求“分析并写论文”，先生成 `EVIDENCE_PACK.md`，再进入写作。

### 1.1 模糊请求的自动路由

如果用户没有说 skill 名，只说“帮我看看”“下一步怎么做”“能不能写文章”“帮我整理一下”“帮我写一下”，优先触发 `bio-research-auto-router` 做第一层判断：

| 模糊说法 | 默认路线 | 原因 |
|---|---|---|
| “这些结果能不能写文章” | `bioinfo-evidence-orchestrator` | 先判断证据强度、缺口和风险 |
| “帮我分析并写文章” | 证据线 -> 写作线 | 混合任务必须先形成 evidence pack |
| “这些图帮我写一下” | `bio-results-writing` | 图表到 Results prose |
| “流程帮我写成材料方法” | `bio-methods-writing` | provenance 到 Methods |
| “这段帮我改得像论文” | `bio-polishing` | 已有文本优先润色/重构 |
| “审稿人这个问题怎么回” | `bio-reviewer-response` | 逐点回复和 action mapping |
| “数据和代码怎么写” | `bio-data-code-availability` | availability statement |
| “做个组会 PPT” | `bio-paper2ppt` | paper/evidence 到中文 slides |

默认原则：能判断就直接选，不要求用户说具体 skill 名；只有“分析还是写作”会导致高风险误判时才追问。

---

## 2. 一级路由表

| 用户请求类型 | 优先触发 | 可叠加 | 不应触发 |
|---|---|---|---|
| 生信数据库事实查询 | `tooluniverse` | `pubmed-database`, `tooluniverse-sequence-retrieval`, `tooluniverse-protein-structure-retrieval` | `bio-paper-writing` |
| PubMed/MeSH 文献检索 | `pubmed-database` | `auto-deep-research`, `tooluniverse-literature-deep-research` | `bio-polishing` |
| 文献深度调研 | `tooluniverse-literature-deep-research` | `research-orchestrator`, `scientific-critical-thinking` | `bio-results-writing` |
| 文献方法/数据挖掘 | `literature-method-data-miner` | `paper-context-resolver`, `auto-deep-research` | 普通摘要类 skill |
| RNA-seq/DESeq2 分析 | `tooluniverse-rnaseq-deseq2` | `tooluniverse-gene-enrichment`, `scientific-critical-thinking` | `bio-paper-writing` |
| GO/KEGG/Reactome/GSEA | `tooluniverse-gene-enrichment` | `tooluniverse`, `scientific-visualization` | `bio-paper-writing`/`bio-results-writing` |
| 序列检索/FASTA | `tooluniverse-sequence-retrieval` | `tooluniverse-phylogenetics` | `bio-paper-writing` |
| 蛋白结构/PDB/AlphaFold | `tooluniverse-protein-structure-retrieval` | `tooluniverse` | `bio-polishing` |
| 系统发育 | `tooluniverse-phylogenetics` | `tooluniverse-sequence-retrieval` | `bio-paper-writing` |
| 论文代码复现 | `repo-intake-and-plan` | `env-and-assets-bootstrap`, `minimal-run-and-audit`, `paper-context-resolver` | `bio-paper-writing` |
| 科研严谨性/统计/偏倚审查 | `scientific-critical-thinking` | `tooluniverse-*`, `pubmed-database` | `bio-polishing` unless prose is provided |
| 科学绘图 | `scientific-visualization` | `nature-figure` | `bio-paper-writing` |
| 做科研汇报/PPT | `scientific-slides` | `nature-paper2ppt`, `bio-paper2ppt` | `tooluniverse-rnaseq-deseq2` unless analysis requested |
| 生信论文 abstract/introduction/results/discussion | `bio-paper-writing` | `bioinfo-evidence-orchestrator` if evidence missing | `tooluniverse-*` unless user requests analysis |
| 生信论文润色/中译英 | `bio-polishing` | `nature-polishing` patterns | `tooluniverse-*` |
| 审稿意见回复 | `bio-reviewer-response` | `nature-response`, `scientific-critical-thinking` | `tooluniverse-*` unless reviewer requests analysis validation |
| Data/code availability | `bio-data-code-availability` | `nature-data`, `tooluniverse` for accession validation | `bio-paper-writing` |

---

## 3. 生信 Agent 总控候选路由

当前 `bioinfo-evidence-orchestrator` 不替代已有 skill，只做路由和证据包汇总。

| 用户说法 | `bioinfo-evidence-orchestrator` 应做什么 | 下游 skill |
|---|---|---|
| “帮我分析这个 GSE 数据集能不能写文章” | 识别 dataset -> 查 accession -> 规划分析 -> 产出 evidence pack | `tooluniverse`, `pubmed-database`, `scientific-critical-thinking` |
| “这个 RNA-seq 结果靠谱吗” | 检查 count matrix/metadata/design/QC/FDR -> 风险表 | `tooluniverse-rnaseq-deseq2`, `scientific-critical-thinking` |
| “这些 DEG 做个富集解释” | 检查物种/ID/background -> 路由富集 -> 汇总结果 | `tooluniverse-gene-enrichment` |
| “这个基因的功能和通路查一下” | 查数据库并记录来源 | `tooluniverse` |
| “这个 accession 对不对” | 验证 accession 和数据库记录 | `tooluniverse`, `pubmed-database` |
| “文献是怎么做的” | 转为方法/数据/补充材料挖掘任务 | `literature-method-data-miner` |
| “论文代码怎么复现” | 进入 README-first 复现链 | `repo-intake-and-plan` -> `env-and-assets-bootstrap` -> `minimal-run-and-audit` |
| “帮我整理这些结果，后面写论文用” | 只整理 evidence pack 和 figure inventory | `scientific-critical-thinking`, relevant tooluniverse skill |

输出必须是结构化材料：

```text
EVIDENCE_PACK.md
RISK_TABLE.md
FIGURE_INVENTORY.md
MISSING_INFO.md
```

不输出：

```text
Abstract
Results prose
Discussion prose
Reviewer response
```

---

## 4. 写作总控候选路由

当前 `bio-paper-writing` 只写 manuscript prose，不跑分析。

| 用户说法 | 应触发 | 输入要求 | 输出 |
|---|---|---|---|
| “根据这个 evidence pack 写 abstract” | `bio-paper-writing` | `EVIDENCE_PACK.md` | Abstract + claim-evidence-boundary map |
| “根据这些图写 Results” | `bio-results-writing` 或 `bio-paper-writing` | figure/table inventory 或用户描述 | Results paragraphs + overclaim flags |
| “帮我写 Methods” | `bio-methods-writing` | workflow provenance、software、版本、参数、数据来源 | reproducible Methods draft + missing fields |
| “帮我写 Introduction” | `bio-paper-writing` | research question、gap、主要发现、文献背景 | Introduction outline/draft |
| “帮我写 Discussion” | `bio-paper-writing` | main findings、limitations、validation status | Discussion draft with boundary language |
| “润色这段生信论文” | `bio-polishing` | draft text | Polished prose + terminology/overclaim checks |
| “把中文实验记录写成英文论文段落” | `bio-paper-writing` 或 `bio-polishing` | Chinese notes + evidence | English prose + missing evidence flags |
| “审稿人质疑 batch effect 怎么回” | `bio-reviewer-response` | reviewer comment + actual analyses/actions | response strategy + draft response + missing action flags |
| “写 data availability” | `bio-data-code-availability` | accession、repository、code location、restrictions | Data/code availability draft + checklist |

如果输入缺少证据，写作 skill 应输出：

```text
需要先由 bioinfo-evidence-orchestrator 生成/补齐 EVIDENCE_PACK.md
```

而不是自行分析或编造。

---

## 5. 与 nature-* skills 的边界

| 请求 | 应用 nature skill | 应用 bio writing skill | 说明 |
|---|---|---|---|
| 泛科研 Nature 风格 abstract | `nature-writing` | 可选 | 不强调生信术语和可复现细节 |
| 生信论文 abstract | `bio-paper-writing` | 是 | 需要 dataset、pipeline、statistical design、claim boundary |
| 泛学术英文润色 | `nature-polishing` | 可选 | 适合通用学术写作 |
| RNA-seq/scRNA-seq/多组学段落润色 | `bio-polishing` | 是 | 需要术语、统计、机制边界检查 |
| Nature/CNS 引用筛选 | `nature-citation` | 否 | 生信默认不应只限 Nature/CNS |
| 生信证据引用 | `bioinfo-evidence-orchestrator` 或 `pubmed-database` | 是 | 应按证据层级，不按期刊品牌 |
| 通用 Data Availability | `nature-data` | 可选 | 适合 Springer/Nature 通用政策 |
| 生信 Data/code availability | `bio-data-code-availability` | 是 | 需要 GEO/SRA/ENA/BioProject/BioSample/PRIDE 等 |
| 通用论文转 PPT | `nature-paper2ppt`, `scientific-slides` | 可选 | 适合 journal club |
| 生信论文转 PPT | `bio-paper2ppt` | 是 | 需要 pipeline、omics figure、evidence ladder |

---

## 6. 测试用例矩阵

### 6.1 应触发生信 Agent，不应触发写作

| 测试提示 | 应触发 | 不应触发 | 验收 |
|---|---|---|---|
| “帮我查一下 GSEXXXXX 是什么数据” | `tooluniverse` / `bioinfo-evidence-orchestrator` | `bio-paper-writing` | 返回 accession 表，不写论文 |
| “这些基因做 GO/KEGG 富集” | `tooluniverse-gene-enrichment` | `bio-paper-writing`/`bio-results-writing` | 要求 species、ID type、background |
| “这个 RNA-seq count matrix 用 DESeq2 分析” | `tooluniverse-rnaseq-deseq2` | `bio-results-writing` | 输出分析结果和 QC/设计说明 |
| “这个 workflow 能复现吗” | `repo-intake-and-plan` / `minimal-run-and-audit` | `bio-methods-writing` | 输出复现计划/审计，不写 Methods |
| “这篇文献怎么做的” | `literature-method-data-miner` | `bio-paper-writing` | 输出方法-数据矩阵 |

### 6.2 应触发写作，不应触发生信分析

| 测试提示 | 应触发 | 不应触发 | 验收 |
|---|---|---|---|
| “根据这个 evidence pack 写 abstract” | `bio-paper-writing` | `tooluniverse-rnaseq-deseq2` | 只写 abstract，标注缺失证据 |
| “把这段中文结果写成英文 Results” | `bio-results-writing` | `tooluniverse-gene-enrichment` | 不新增分析，不编造 FDR |
| “润色这段 single-cell 论文 discussion” | `bio-polishing` | `tooluniverse` | 检查 overclaim 和术语 |
| “写 Methods，材料如下” | `bio-methods-writing` | `repo-intake-and-plan` unless repo path provided | 输出可复现 Methods + missing fields |
| “审稿人说没有外部验证，帮我回复” | `bio-reviewer-response` | `bioinfo-evidence-orchestrator` unless需要验证数据 | 标记是否需要新分析或作者确认 |

### 6.3 混合请求应拆两步

| 测试提示 | 正确流程 | 错误流程 |
|---|---|---|
| “帮我分析 GSE 数据并写一篇文章” | 先 `bioinfo-evidence-orchestrator` 生成 evidence pack，再 `bio-paper-writing` 写 outline/sections | 直接写完整论文 |
| “跑一下 DESeq2 然后写 Results” | 先 `tooluniverse-rnaseq-deseq2`，再 `bio-results-writing` | 直接假设 DEG 结果 |
| “根据文献方法设计我的论文并写 introduction” | 先 `literature-method-data-miner`，再 `bio-paper-writing` | 边找边写，不区分证据 |
| “审稿人要 batch correction，帮我分析并回复” | 先证据/分析层判断可做动作，再 `bio-reviewer-response` | 直接承诺已做 batch correction |

---

## 7. Description 编写规则

后续新增或修改 `SKILL.md` frontmatter description 必须写清：

1. 做什么。
2. 何时触发。
3. 中文触发词。
4. 明确“不做什么”，尤其是分析/写作边界。

### `bioinfo-evidence-orchestrator` description 应包含

```text
Use when the user asks to analyze, validate, reproduce, inspect, organize, or prepare evidence from bioinformatics datasets, omics results, gene lists, workflows, database records, or papers. Produces EVIDENCE_PACK.md. Do not use for manuscript prose drafting, polishing, reviewer responses, or PPT writing.
```

中文触发词：

```text
生信分析、组学分析、数据库查证、accession、GEO、SRA、QC、富集、复现、整理证据、写论文前整理结果
```

### `bio-paper-writing` description 应包含

```text
Use to draft or restructure bioinformatics manuscripts from evidence packs, figures, tables, analysis summaries, or Chinese notes. Do not run analyses, validate accessions, or invent datasets, statistics, software versions, mechanisms, or citations.
```

中文触发词：

```text
生信论文、写 abstract、写 Results、写 Discussion、根据结果写论文、中文实验记录写英文论文
```

---

## 8. 当前执行状态与下一步建议

已完成：

1. 创建并验证 `bioinfo-evidence-orchestrator`。
2. 创建 `bio-paper-writing` 写作总控。
3. 拆分并创建 `bio-results-writing`、`bio-methods-writing`、`bio-polishing`、`bio-reviewer-response`、`bio-data-code-availability`、`bio-paper2ppt`。
4. 用本矩阵第 6 节的边界测试作为后续触发验收基准。

后续建议：

1. 在真实项目中用一个 `EVIDENCE_PACK.md` 跑通“证据线 -> 写作线”交接。
2. 若频繁出现生信图表解释任务，再新增轻量 `bioinfo-omics-figure-brief`，但仍不要让它写 Results prose。
3. 若需要投稿期刊政策核验，写作 skill 只负责草稿，具体政策仍应按目标期刊页面即时核对。
