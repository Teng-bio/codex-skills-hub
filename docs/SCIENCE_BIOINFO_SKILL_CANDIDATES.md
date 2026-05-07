# 科研 / 生物信息 Skill 补充候选清单

更新时间：2026-05-07

目标：围绕 `planning-with-files` 构建科研工作流，而不是让单个 skill 单独承担全部任务。复杂科研任务仍以 `task_plan.md` / `findings.md` / `progress.md` 作为任务内核，下面的 science/bioinfo skills 作为阶段性工具层自动触发。

当前状态：推荐安装批次 A 已安装到 `~/.agents/skills`，并复制到 `~/.codex/skills` 以确保 Codex 可自动触发；所有新增 `SKILL.md` description 已补充中文触发词。

新增本地路由 skill：`literature-method-data-miner`。它专门承接用户的短提示词，例如“文献是怎么做的”“这篇文献怎么做的”“参考文献的做法”。默认语义不是普通摘要，而是：

- 从文献正文、方法、结果、图表、附录和补充材料中提取科研方法；
- 收集数据来源、样本/数据集、参数、软件、统计和验证信息；
- 如果文献没有提供，则先通过深度调研/数据库检索找到相关文献；
- 输出方法-数据矩阵、补充材料检查表和可借鉴科研思路。

## 已有基础能力

当前仓库已经具备的基础层：

| 层级 | 已有 skill | 用途 |
|---|---|---|
| 任务内核 | `planning-with-files` | 大项目逐步推进、阶段计划、进度恢复 |
| 项目状态 | `project-state-maintainer` | 每个项目的 durable state |
| 版本/结果守护 | `project-flow-guard`, `project-version-curator` | 重跑、current/baseline/release、混乱目录盘点 |
| 通用调研 | `auto-deep-research`, `web-search`, `llm-context`, `research-orchestrator` | 搜索、网页上下文、报告合并核验 |
| 复现/调试基础 | `bug-repro-plan`, `log-summarizer`, `ci-failure-triage` | 最小复现、日志和 CI triage |

## 选择原则

1. **不要重复替代 `planning-with-files`**：新 skill 只负责某个阶段，例如 PubMed 检索、序列检索、论文复现环境、科学批判性审读。
2. **优先安装自动触发清晰的 skill**：description 中包含生信、论文、文献综述、复现、PubMed、sequence、RNA-seq、phylogenetics 等触发意图。
3. **先装高价值低冲突批次**：先覆盖文献检索、论文阅读/复现、生信数据库/组学分析、科学审稿/可视化；小众/重叠 skill 后续按项目需要补。
4. **安装后必须同步到 hub**：安装到 `~/.codex/skills` 后运行 `scripts/sync_skills.py --apply --commit --push`。

## 推荐安装批次 A：核心科研 / 生信工作流

这一批建议优先安装，覆盖用户当前最常见需求：生物信息、论文阅读、总结、复现。

| 方向 | 推荐 skill | 来源 | 安装量/质量信号 | 作用 | 典型触发 |
|---|---|---|---|---|---|
| 科研数据库总路由 | `tooluniverse` | `mims-harvard/tooluniverse` | GitHub stars 约 1.3K；ToolUniverse 列出 100+ 专项 skill | 生命科学数据库总入口，覆盖 UniProt/PubMed/ChEMBL/ClinVar/GWAS 等 | 生物、医学、药物、基因、蛋白、疾病、化合物问题 |
| 文献深度调研 | `tooluniverse-literature-deep-research` | `mims-harvard/tooluniverse` | SkillForge science 页面高排名 | 面向科学问题做证据分级文献深度研究 | 深度调研、文献综述、研究进展、机制证据 |
| PubMed 检索 | `pubmed-database` | `sickn33/antigravity-awesome-skills` | GitHub stars 约 36K；SkillForge 显示 PubMed API skill | MeSH/布尔查询、PubMed E-utilities | PubMed、MeSH、医学文献、找论文 |
| 系统综述 | `systematic-literature-review` | `huangwb8/chineseresearchlatex` | GitHub stars 约 1.5K；中文科研 LaTeX 生态 | 多源检索、去重、评分、分主题、输出综述 | 系统综述、related work、文献调研、中文综述 |
| arXiv 论文读取 | `read-arxiv-paper` | `karpathy/nanochat` | GitHub stars 约 53K | 获取 arXiv TeX 源而非只读 PDF，适合公式/结构拆解 | 读 arXiv、论文公式、TeX 源码 |
| 论文复现上下文 | `paper-context-resolver` | `lllllllama/ai-paper-reproduction-skill` | skills 安装量很高；repo stars 较低，需作为工具型 skill 使用 | 解析论文复现关键缺口：数据集版本、split、checkpoint、评估协议 | 复现论文、找数据版本、评估协议不清 |
| 论文复现环境 | `env-and-assets-bootstrap` | `lllllllama/ai-paper-reproduction-skill` | 与 paper-context-resolver 同源 | 准备依赖、checkpoint、dataset/cache 路径 | 复现环境、缺模型、缺数据、依赖安装 |
| 仓库进入与复现计划 | `repo-intake-and-plan` | `lllllllama/ai-paper-reproduction-skill` | 与复现 pipeline 同源 | 读入论文代码仓库并形成复现计划 | 读论文 repo、复现实验计划 |
| 最小运行与审计 | `minimal-run-and-audit` | `lllllllama/ai-paper-reproduction-skill` | 与复现 pipeline 同源 | 先跑最小实验并记录差异/失败原因 | 最小运行、audit reproduction、复现失败 |
| 论文转可复现 notebook | `implement-paper` | `marimo-team/skills` | GitHub stars 约 129；marimo 官方相关 | 把论文方法转交互式 marimo notebook | implement paper、论文变代码、教学 notebook |
| 序列检索 | `tooluniverse-sequence-retrieval` | `mims-harvard/tooluniverse` | skills find 显示约 1.4K installs | 从 NCBI/ENA 检索 DNA/RNA/蛋白序列，处理 accession/gene 消歧 | 序列、FASTA、NCBI、ENA、accession |
| 蛋白结构检索 | `tooluniverse-protein-structure-retrieval` | `mims-harvard/tooluniverse` | ToolUniverse 生信专项 | PDB/AlphaFold 等结构相关检索 | 蛋白结构、PDB、AlphaFold |
| RNA-seq/DESeq2 | `tooluniverse-rnaseq-deseq2` | `mims-harvard/tooluniverse` | ToolUniverse 组学专项 | bulk RNA-seq 差异表达、DESeq2 结果解释 | RNA-seq、DESeq2、差异表达 |
| 系统发育 | `tooluniverse-phylogenetics` | `mims-harvard/tooluniverse` | ToolUniverse 生信专项 | 系统发育、同源、树、进化分析 | phylogeny、系统发育、ortholog、进化 |
| 富集解释 | `tooluniverse-gene-enrichment` | `mims-harvard/tooluniverse` | ToolUniverse pathway 专项 | GO/pathway/gene set enrichment 解释 | GO 富集、pathway、gene set |
| 科学批判性审读 | `scientific-critical-thinking` | `davila7/claude-code-templates` | GitHub stars 约 26K；SkillForge science 高排名 | 系统检查方法学、统计、实验设计 | 批判性审读、方法学问题、统计有效性 |
| 科学可视化 | `scientific-visualization` | `davila7/claude-code-templates` | 同源高 stars | 期刊级图表、多面板科学图 | 科学绘图、figure、多面板图 |
| 科学 slides | `scientific-slides` | `davila7/claude-code-templates` | SkillForge science 高排名 | 科学汇报/论文 slides | 科研汇报、论文 slides、conference presentation |

## 推荐安装命令

注意：本机 git 全局配置里有旧代理 `127.0.0.1:7890`，直接 `npx skills add` 可能 clone 失败。推荐临时绕过 git 全局配置：

```bash
GIT_CONFIG_GLOBAL=/dev/null npx skills add mims-harvard/tooluniverse -g -y --copy --skill tooluniverse
GIT_CONFIG_GLOBAL=/dev/null npx skills add mims-harvard/tooluniverse -g -y --copy --skill tooluniverse-literature-deep-research
GIT_CONFIG_GLOBAL=/dev/null npx skills add mims-harvard/tooluniverse -g -y --copy --skill tooluniverse-sequence-retrieval
GIT_CONFIG_GLOBAL=/dev/null npx skills add mims-harvard/tooluniverse -g -y --copy --skill tooluniverse-protein-structure-retrieval
GIT_CONFIG_GLOBAL=/dev/null npx skills add mims-harvard/tooluniverse -g -y --copy --skill tooluniverse-rnaseq-deseq2
GIT_CONFIG_GLOBAL=/dev/null npx skills add mims-harvard/tooluniverse -g -y --copy --skill tooluniverse-phylogenetics
GIT_CONFIG_GLOBAL=/dev/null npx skills add mims-harvard/tooluniverse -g -y --copy --skill tooluniverse-gene-enrichment

GIT_CONFIG_GLOBAL=/dev/null npx skills add sickn33/antigravity-awesome-skills -g -y --copy --skill pubmed-database
GIT_CONFIG_GLOBAL=/dev/null npx skills add huangwb8/chineseresearchlatex -g -y --copy --skill systematic-literature-review
GIT_CONFIG_GLOBAL=/dev/null npx skills add karpathy/nanochat -g -y --copy --skill read-arxiv-paper

GIT_CONFIG_GLOBAL=/dev/null npx skills add lllllllama/ai-paper-reproduction-skill -g -y --copy --skill paper-context-resolver
GIT_CONFIG_GLOBAL=/dev/null npx skills add lllllllama/ai-paper-reproduction-skill -g -y --copy --skill env-and-assets-bootstrap
GIT_CONFIG_GLOBAL=/dev/null npx skills add lllllllama/ai-paper-reproduction-skill -g -y --copy --skill repo-intake-and-plan
GIT_CONFIG_GLOBAL=/dev/null npx skills add lllllllama/ai-paper-reproduction-skill -g -y --copy --skill minimal-run-and-audit
GIT_CONFIG_GLOBAL=/dev/null npx skills add marimo-team/skills -g -y --copy --skill implement-paper

GIT_CONFIG_GLOBAL=/dev/null npx skills add davila7/claude-code-templates -g -y --copy --skill scientific-critical-thinking
GIT_CONFIG_GLOBAL=/dev/null npx skills add davila7/claude-code-templates -g -y --copy --skill scientific-visualization
GIT_CONFIG_GLOBAL=/dev/null npx skills add davila7/claude-code-templates -g -y --copy --skill scientific-slides
```

安装后同步到 hub：

```bash
cd /home/teng/claude_code/codex-skills-hub
python scripts/sync_skills.py --apply
python scripts/validate_skills.py
git add .
git commit -m 'feat: add science and bioinformatics skills'
git push
```

## 后续批次 B：按项目需要再补

| 方向 | 候选 skill | 说明 |
|---|---|---|
| 单细胞 | `tooluniverse-single-cell`, `anthropics/life-sciences@single-cell-rna-qc`, `starlitnightly/omicverse` 系列 | 如果开始 scRNA-seq 项目再装，避免触发过多 |
| 代谢组/天然产物 | `tooluniverse-metabolomics-analysis`, `tooluniverse-metabolomics`, `metabolomics-workbench-database` | 和 BGC / natural product 方向可能相关 |
| 比较基因组 | `tooluniverse-comparative-genomics` | 对 ortholog、跨物种比较很有用 |
| CRISPR screen | `tooluniverse-crispr-screen-analysis` | 需要功能基因组筛选时再装 |
| 药物/靶点 | `tooluniverse-drug-target-validation`, `tooluniverse-drug-repurposing`, `tooluniverse-chemical-compound-retrieval` | 如果转到药物发现/化合物方向再装 |
| 多维论文阅读 | `multi-dimensional-paper-reader` | 功能有吸引力，但当前 installs/stars 较低，建议先观察或本地二次改造 |
| peer review | `peer-review`, `academic-paper-reviewer` | 与 `scientific-critical-thinking` 有重叠，后续按写稿/审稿需求补 |

## 与 planning-with-files 的组合模板

### 论文阅读 / 总结

1. `planning-with-files` 建立 `task_plan.md`。
2. `pubmed-database` / `read-arxiv-paper` 获取文献与结构化材料。
3. `tooluniverse-literature-deep-research` 写证据分级 findings。
4. `scientific-critical-thinking` 审查方法学与统计。
5. 输出进入 `findings.md` 和 `progress.md`。

### 论文复现

1. `planning-with-files` 建立复现阶段计划。
2. `paper-context-resolver` 补齐数据、split、checkpoint、metric。
3. `env-and-assets-bootstrap` 准备环境与资源。
4. `repo-intake-and-plan` 读入 repo 并拆复现步骤。
5. `minimal-run-and-audit` 跑最小实验并记录差异。
6. `bug-repro-plan` / `log-summarizer` 处理失败。
7. 结果由 `project-flow-guard` 管控 current/baseline。

### 生信分析

1. `planning-with-files` 固定分析问题和输入输出。
2. `tooluniverse` 路由到专项，例如 sequence / protein / RNA-seq / phylogenetics / enrichment。
3. 关键数据库证据写入 `findings.md`。
4. 中间表和图由 `project-flow-guard` 管控版本。
5. 最终报告/图表可用 `scientific-visualization`、`scientific-slides`。
