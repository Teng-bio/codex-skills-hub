# Skill Routing Matrix for Bioinformatics, Writing, and Project Harness Skills

更新日期：2026-06-24

用途：定义用户请求应触发哪个 skill，避免“生信分析”“论文写作”和“长期项目 harness/工作台”混在一起。

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
长期项目工作台 / run-result-data provenance / 项目 continuation -> research-project-os
已有 .project_os 项目里的计划/状态/绘图/系统发育/运行请求（含旧 planning/state/phylogeny 触发词） -> research-project-os first
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

### 1.2 长期项目工作台请求

当用户的问题不是具体生信分析/写作，而是“多个长期项目如何继续、run/result/data 怎么追踪、continue 到底继续哪个分支、如何做项目 harness/工作台”时，优先触发 `research-project-os`，不要新建第二套主计划。

`research-project-os` 当前是 **harness-first** 工作台入口：

- branch/workstream 是物理目录：`.project_os/branches/<branch_id>/`。
- formal run 默认进入 `runs/<branch_id>/<run_id>/`。
- canonical machine state 是 `.project_os/indexes/*.tsv`、`.project_os/project.json`、`.project_os/journals/events.jsonl`。
- `PROJECT_STATE.md`、`RESULTS_INDEX.md`、`DATA_ASSETS.md`、`RUNS_INDEX.tsv` 是 human handoff / derived views。
- `runtime/current_session` 为空时使用全局 current branch/task/run；非空时使用 `.project_os/runtime/sessions/<session_id>/current_*`，session 只切换 runtime focus，不创建第二套 branch/task/run 身份；paused/closed session 不能成为当前会话；`plan-session-cleanup` / `会话清理` 只生成 closed/paused session cleanup candidate report，不删除、不移动 session 目录；dashboard 与 doctor repair-plan 也只显示 advisory/generated cleanup candidate view。
- `show-current --audit` 与 `export-dashboard` 都只生成 current-result / promotion-audit 派生视图；dashboard JSON/HTML/SQLite 可展示 current/project/branch result 与 audit warning，但不成为 result/current 的写入入口。
- `status` 是只读 operational snapshot：会输出 session-aware runtime focus、counts、active/last run summary、candidate/current result summary 与 promotion-audit warning counts；它不刷新索引、不写 journal、不 promote、不 repair `current/`。
- `summarize-state` 是只读 handoff/status payload，会同时输出 session-aware runtime focus 与 current-result/audit 派生摘要；它不 promote、不 repair、不写 result/current canonical state。
- 短触发 `当前结果` / `查看当前结果` 只路由到只读 `show-current --audit`；它不等同于 `设为当前结果`，不会 promote、repair、改写 `results.tsv` 或改动 `current/`。
- 短触发词先走 `project_os.py route` / `explain-trigger` 生成计划，不直接改文件。
- promotion/release 的直接 CLI 与短触发 `--apply` 都需要显式 `--approved`；dry-run 仍可无 approval 先审查计划。
- hooks 当前是 manual report-only 层：`list-hooks` / `dispatch-hooks` 只读 `events.jsonl` 并生成报告/建议命令，不自动执行、不写 canonical state；dashboard/doctor/validate 只暴露 hooks config/status advisory，不启用 active dispatcher。事件日志缺失时走 `restore-journal` dry-run/`--apply --approved`，而不是手工补历史。

| 用户说法 | 默认路线 | 原因 |
|---|---|---|
| “做一个 research-project-os harness” | `research-project-os` | 需要 `.project_os/` workflow/branch/task/runtime/indexes |
| “项目骨架 / 新项目骨架 / 搭项目骨架” | `project-skeleton` -> `research-project-os` | bootstrap/resume 的短入口，先 dry-run 或 start |
| “开工 / 继续项目 / 继续当前任务 / 继续下一步 / 大项目 / 逐步推进 / 恢复上下文” | `research-project-os` route/start | 读取 `runtime/current_branch`、`current_task`、`current_run`；无 harness 时先 dry-run bootstrap |
| “当前进展 / 项目状态 / 写一个项目状态文档 / 总结项目状态 / 更新项目状态文档” | `research-project-os` route/status/summarize-state | 状态从 `.project_os` indexes/views 派生，不用独立状态 skill |
| “制定计划 / 拆解任务 / task_plan.md / findings.md / progress.md / plan out / break down” | `research-project-os` route -> task tree/session/handoff | 原 planning-with-files 触发词进入 `.project_os`，不再创建平行 planning-file kernel |
| “先画 / 画图 / 绘图 / 开始分析 / 先跑” | `research-project-os` route -> task/run | 先建立 branch/task/run，再执行领域命令并记录 provenance |
| “系统发育 / 发育树 / 进化树 / Newick / FASTA比对 / PHYLIP / Nexus / alignment / tree / parsimony / treeness / RCV / DVMC / ortholog / 同源基因 / 分子进化 / bootstrap” | `research-project-os` route -> task/run/assets/results | 原 phylogeny 触发词先进入 harness，避免绕过 `.project_os/` 项目状态 |
| “新建分支 / 开一个方向” | `research-project-os` route/create-branch | 创建 branch-first 物理工作区 |
| “新建会话 / 切会话 / 当前会话 / 暂停会话 / 恢复会话” | `research-project-os` route/session CLI | 在多个 runtime focus 间切换，仍指向 canonical branch/task/run |
| “会话清理 / 规划会话清理” | `research-project-os` route/session cleanup planner | 只生成 archive/GC candidate report，不做物理删除/移动 |
| “恢复计划 / 恢复检查 / 崩溃恢复检查” | `research-project-os` route/recovery planner | 只生成 crash/recovery inspection report，不做 replay/rollback/tmp 删除/lock 移除 |
| “恢复事件日志” | `research-project-os` route/restore-journal | 仅在 `events.jsonl` 缺失时 dry-run/`--apply --approved` 创建 journal 并记录 `journal.restored` |
| “hook状态 / hook报告 / hook提醒” | `research-project-os` route/hooks CLI | 查看默认禁用的 hook policy 或从 `events.jsonl` 生成 manual report-only 提醒 |
| “开始运行 / 记录结果 / 设为当前结果” | `research-project-os` route -> run/result CLI | run/result/promotion 走同一套 approval gate |
| “当前结果 / 查看当前结果” | `research-project-os` route -> `show-current --audit` | 只读 current-result 派生视图，不 promotion、不 repair、不写 canonical state |
| “长期科研项目管理太乱了” | `research-project-os` + 只读 inventory | 先建立项目工作台和索引，不直接清理 |
| “run provenance 和结果采用状态怎么管” | `research-project-os`，必要时叠加 `project-flow-guard` | harness 管结构，flow-guard 管新 run/promotion 护栏 |

---

## 2. 一级路由表

| 用户请求类型 | 优先触发 | 可叠加 | 不应触发 |
|---|---|---|---|
| 长期科研项目 harness / `.project_os` / branch/task/run/result/data/release 索引 | `research-project-os` | `project-skeleton`, `project-flow-guard`, `project-version-curator` | 已移除的旧规划/状态 skill |
| 生信数据库事实查询 | `tooluniverse` | `pubmed-database`, `tooluniverse-sequence-retrieval`, `tooluniverse-protein-structure-retrieval` | `bio-paper-writing` |
| PubMed/MeSH 文献检索 | `pubmed-database` | `auto-deep-research`, `tooluniverse-literature-deep-research` | `bio-polishing` |
| 文献深度调研 | `tooluniverse-literature-deep-research` | `research-orchestrator`, `scientific-critical-thinking` | `bio-results-writing` |
| 文献方法/数据挖掘 | `literature-method-data-miner` | `paper-context-resolver`, `auto-deep-research` | 普通摘要类 skill |
| RNA-seq/DESeq2 分析 | `tooluniverse-rnaseq-deseq2` | `tooluniverse-gene-enrichment`, `scientific-critical-thinking` | `bio-paper-writing` |
| GO/KEGG/Reactome/GSEA | `tooluniverse-gene-enrichment` | `tooluniverse`, `scientific-visualization` | `bio-paper-writing`/`bio-results-writing` |
| 序列检索/FASTA | `tooluniverse-sequence-retrieval`；若在 `.project_os` 项目内先 `research-project-os` | `tooluniverse` | `bio-paper-writing` |
| 蛋白结构/PDB/AlphaFold | `tooluniverse-protein-structure-retrieval` | `tooluniverse` | `bio-polishing` |
| 系统发育 | `research-project-os` first | `tooluniverse-sequence-retrieval`, `scientific-visualization` | standalone phylogeny skill |
| 论文代码复现 | `repo-intake-and-plan` | `env-and-assets-bootstrap`, `minimal-run-and-audit`, `paper-context-resolver` | `bio-paper-writing` |
| 科研严谨性/统计/偏倚审查 | `scientific-critical-thinking` | `tooluniverse-*`, `pubmed-database` | `bio-polishing` unless prose is provided |
| 科学数据图表/统计图 | `scientific-visualization` | `nature-figure` | `bio-paper-writing` |
| 科研解释性插图/技术路线图/机制图/原理图 | `scientific-explanatory-schematics` | `scientific-visualization` for data panels, `scientific-slides` for presentation packaging | `bio-paper-writing` unless prose writing is requested |
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
