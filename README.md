# codex-skills-hub

这是个人 GitHub-backed Codex / agent skill 库，用来集中管理、同步、验证、发布本机和项目内的 skills。

仓库地址：

```text
https://github.com/Teng-bio/codex-skills-hub.git
```

## 这个仓库解决什么问题

- 把 `~/.codex/skills` 中的全局 skill 版本化备份。
- 把全局 skill 和项目级 workspace skill 纳入同一个 inventory；当前以通用 `.project_os/` 长期项目工作台为主，已移除会抢占路由的旧规划/状态/系统发育专项 skill。
- 所有新写的自定义 skill 先放到 `skills/local/`，通过统一标准验证、同步、提交、推送。
- 生成机器可读和人可读的 skill 清单：
  - `registry/SKILL_INVENTORY.tsv`
  - `registry/skills.json`
- 支持后续自动上传新 skill：
  - `scripts/sync_skills.py --watch --apply --commit --push`

## 目录结构

```text
skills/
  global/                 # 从 ~/.codex/skills 镜像过来的全局 skills
  workspace/              # 从项目 .codex/skills 镜像过来的 workspace skills
  local/                  # 本仓库原创/自定义 skills，未来新 skill 优先放这里
registry/
  SKILL_INVENTORY.tsv     # 生成的人可读 inventory
  skills.json             # 生成的机器可读 inventory
  sources.tsv             # 同步来源配置
docs/
  OPERATING_MODEL.md      # skill 库运营规则
scripts/
  new_skill.py            # 标准化创建新 skill
  sync_skills.py          # dry-run/apply/commit/push/watch 同步工具
  validate_skills.py      # 轻量验证 SKILL.md
services/
  codex-skills-hub-sync.service.example
```

## 新建 skill 的标准流程

推荐使用 `skill-library-publisher` 工作流，或者直接运行：

```bash
cd /home/teng/claude_code/codex-skills-hub

python3 scripts/new_skill.py my-skill-name \
  --description "Describe what this skill does. Use when 用户说..." \
  --apply \
  --sync \
  --commit \
  --push
```

手动创建时遵守：

```text
skills/local/<skill-name>/SKILL.md
```

然后运行：

```bash
python3 scripts/validate_skills.py
python3 scripts/sync_skills.py --apply --commit --push
```

`research-project-os` 这种 harness 级 skill 还应运行可重复端到端 smoke：

```bash
python3 skills/local/research-project-os/scripts/smoke_project_os_e2e.py
```

该脚本只创建临时项目和临时 external primary/backup roots，覆盖 bootstrap、branch/session/task/run、asset/result/release、hooks/recovery、approval gates、no-hardlink 外置资产和最终 validate。

面向用户可见的新 skill 还必须同步维护：

```text
README.md                         # GitHub 首页说明和触发方式
docs/SKILL_ROUTING_MATRIX.md      # 如果改变路由边界
PROJECT_STATE.md                  # 如果改变当前技能体系状态
registry/SKILL_INVENTORY.tsv      # 由 sync 脚本生成
registry/skills.json              # 由 sync 脚本生成
```

## 自动同步 / 自动上传

重要：自动上传不是默认后台行为。默认只有在显式运行 `sync_skills.py --apply --commit --push`，或安装并启动 user service 后，才会提交和推送。

预览变化：

```bash
python3 scripts/sync_skills.py --dry-run
```

同步 inventory 和镜像：

```bash
python3 scripts/sync_skills.py --apply
```

同步、提交、推送：

```bash
python3 scripts/sync_skills.py --apply --commit --push
```

持续监控并自动上传：

```bash
python3 scripts/sync_skills.py --watch --interval 60 --apply --commit --push
```

也可以参考：

```text
services/codex-skills-hub-sync.service.example
```

如果要启用真正的后台自动上传，可安装 user service：

```bash
mkdir -p ~/.config/systemd/user
cp services/codex-skills-hub-sync.service.example ~/.config/systemd/user/codex-skills-hub-sync.service
systemctl --user daemon-reload
systemctl --user enable --now codex-skills-hub-sync.service
systemctl --user status codex-skills-hub-sync.service
```

如果没有启用该服务，新建 skill 后不会自动出现在 GitHub，必须手动 commit/push。

## 触发原则

Codex 选择 skill 时主要依赖每个 `SKILL.md` frontmatter 的 `description`。因此每个 skill 的 description 必须写清楚：

1. 这个 skill 做什么；
2. 什么用户意图/关键词应该触发它；
3. 中文触发词也要写进去；
4. 复杂项目中，输出应该写回哪里；已有 `.project_os/` 的项目必须先写回 branch/task/run/result/asset 索引和 derived human views，不能另建并行状态系统。

## Skill 总览与触发方式

### 核心工作流 / 项目状态

| Skill | 作用 | 典型触发语 | 位置 |
|---|---|---|---|
| `research-project-os` | 通用长期科研/工程项目的第一路由和主控 harness：在每个项目内维护 `.project_os/` 工作台、branch/task/run/result/asset/release/session/recovery/hooks 索引；所有“继续/计划/状态/运行/结果/绘图/系统发育/大文件外置”先经 `project_os.py route` 或 `start/status` 建立上下文，再执行领域命令并记录 provenance。保留 no-hardlink 外置资产策略，`asset_id + asset_locations.tsv` 为可迁移数据引用；promotion/release/restore-journal apply 均需 `--approved`。旧 `planning-with-files`、`project-state-maintainer`、`tooluniverse-phylogenetics` 的重叠触发词已并入此 skill。 | `research-project-os`、`project harness`、`.project_os`、`项目骨架`、`开工`、`继续项目`、`继续当前任务`、`继续下一步`、`大项目`、`逐步推进`、`当前进展`、`恢复上下文`、`制定计划`、`拆解任务`、`task_plan.md`、`findings.md`、`progress.md`、`项目状态`、`写一个项目状态文档`、`更新项目状态文档`、`总结项目状态`、`开始分析`、`先跑`、`先画`、`绘图`、`画图`、`发育树`、`系统发育`、`进化树`、`Newick`、`FASTA比对`、`PHYLIP`、`Nexus`、`alignment`、`tree`、`parsimony`、`treeness`、`RCV`、`DVMC`、`ortholog`、`同源基因`、`分子进化`、`bootstrap`、`开始运行`、`记录结果`、`当前结果`、`外置数据`、`纳管外置数据`、`release workflow` | `skills/local/research-project-os/` |
| `project-skeleton` | `research-project-os` 的短入口/触发别名：把“项目骨架/新项目骨架/开工/继续项目/先画/先跑”等路由到 `.project_os/` bootstrap 或 resume 流程。 | `项目骨架`、`新项目骨架`、`搭项目骨架`、`初始化项目骨架`、`项目工作流骨架`、`研究项目骨架`、`科研项目骨架`、`开工`、`继续项目`、`继续下一步`、`当前进展`、`项目状态`、`开始分析`、`先跑`、`先画`、`绘图`、`画图` | `skills/local/project-skeleton/` |
| `project-literature-bridge` | 项目报告 × 外置文献库 × Obsidian 的桥接工作流：读取项目状态/报告/结果索引和外置文献库，生成独立 Obsidian 项目文献桥接库；把项目问题、短标题论文说明、Evidence Record、方法借鉴、风险和下一步任务配对起来。默认不把项目根目录变成 vault，不移动/复制外置文献库；论文笔记标题要求简短、主题明确。 | `项目总结和论文说明搭配`、`项目-文献桥接`、`项目报告与文献库`、`Obsidian项目文献库`、`外置文献库索引`、`根据项目报告整理参考文献`、`把论文映射到项目模块`、`文献证据矩阵`、`论文标题要简短概括主题` | `skills/local/project-literature-bridge/` |
| `project-flow-guard` | 事前防乱：formal run 只作 provenance，使用 `RUN_MANIFEST.json` 和 `RUNS_INDEX.tsv` 记录来源；accepted/candidate 结果通过 `RESULTS_INDEX.md` 和 `current/` 发现。branch/workstream 只在长期方向且用户确认后创建。 | `重跑`、`重新生成`、`保留这个版本`、`设为当前版本`、`release`、`打包`、`开分支`、`snapshot`、`清理旧版本`、`RUN_MANIFEST.json` | `skills/global/project-flow-guard/` |
| `project-version-curator` | 事后整理：对已经混乱的目录做 inventory、版本冲突检测、cleanup/release dry-run；优先信任 `RESULTS_INDEX.md` / registry，`final/current` 文件名只作线索。 | `整理结果`、`太混乱了`、`清理目录`、`版本混乱`、`final/current/v1/v2 很多`、`生成 inventory`、`dry-run cleanup`、`release planning` | `skills/global/project-version-curator/` |

项目维护模型：

```text
research-project-os       # 当前主控：.project_os branch/task/run/result/asset/session/release harness
project-flow-guard        # 未来运行防乱：runs 只作 provenance，current/index 才是入口
project-version-curator   # 既有混乱整理：inventory/conflict audit/release dry-run
```

`research-project-os` 现在是已有 `.project_os/` 项目的主控工作台。旧规划、薄状态、系统发育专项 skill 的重叠触发已迁入它；其他领域 skill 只能作为执行/检索辅助，不能绕过 harness 创建第二套状态。

维护文档的 canonical source 固定为：

```text
Markdown = 人类总结、状态、决策、结果入口
TSV      = 可筛选索引和 registry
JSON     = run manifest / 结构化元数据
```

SQLite / HTML 只能作为后续自动生成的查询或展示层，不作为维护源文档。

### Skill 发现、创建、发布

| Skill | 作用 | 典型触发语 | 位置 |
|---|---|---|---|
| `find-skills` | 查找、比较、安装现有 agent skills，作为 skill 生态的发现层。 | `找 skill`、`有没有 skill`、`搜索 skill`、`管理 skill 库`、`补全 skill 生态`、`安装 skill` | `skills/global/find-skills/` |
| `write-a-skill` | 编写新的 agent skill，指导结构、frontmatter、progressive disclosure、脚本/引用资源。 | `写一个 skill`、`创建 skill`、`build a skill`、`new skill` | `skills/global/write-a-skill/` |
| `skill-library-publisher` | 本仓库的标准发布流程：新建/更新 skill 后验证、同步 inventory、commit、push 到 GitHub。 | `创建skill`、`新建skill`、`上传skill`、`同步skill库`、`发布skill到GitHub`、`自动上传skill`、`skill仓库入库` | `skills/local/skill-library-publisher/`；同时镜像到 `skills/global/skill-library-publisher/` |

### 调研 / 搜索 / RAG

| Skill | 作用 | 典型触发语 | 位置 |
|---|---|---|---|
| `auto-deep-research` | 自动编排搜索、网页上下文、deep research 本地报告；当前版本不再调用 `answers`。 | `查资料`、`搜资料`、`深度调研`、`文献综述`、`找论文`、`verify online claims`、`research` | `skills/global/auto-deep-research/` |
| `web-search` | Web 搜索端点，返回结果、摘要、URL、缩略图等。 | `搜索网页`、`web search`、`查找网页结果`、`找链接` | `skills/global/web-search/` |
| `llm-context` | 获取适合 LLM/RAG 使用的网页正文、表格、代码等上下文。 | `提取网页内容`、`RAG grounding`、`llm context`、`网页原文上下文` | `skills/global/llm-context/` |
| `answers` | 基于 OpenAI-compatible `/chat/completions` 的 AI-grounded answer。当前生态中不作为 `auto-deep-research` 的自动依赖。 | `AI answer`、`single-search answer`、`deep research answer`、明确要求使用 answers | `skills/global/answers/` |
| `research-orchestrator` | 合并、比对、去重、核验多个 research report。 | `合并报告`、`compare research`、`merge reports`、`fact-check these documents`、`create unified report` | `skills/global/research-orchestrator/` |

### 科研 / 生物信息 / 论文复现

详细候选、选择依据和后续批次见：

```text
docs/SCIENCE_BIOINFO_SKILL_CANDIDATES.md
```

#### 生信自动路由、证据线和写作线

这组 skills 解决一个核心问题：用户通常不会说具体 skill 名，只会说“这些结果能不能写文章”“下一步怎么做”“帮我写一下”。因此新增了一个自动路由入口，先判断任务属于证据/分析还是写作/投稿材料。

核心边界：

```text
生信 Agent 负责事实和证据，不写论文。
写作 Skill 负责表达和投稿材料，不跑分析。
二者通过 EVIDENCE_PACK.md 交接。
```

| Skill | 作用 | 典型触发语 | 位置 |
|---|---|---|---|
| `bio-research-auto-router` | 模糊任务自动路由入口。用户不用说 skill 名，它根据任务判断走证据线、写作线、文献方法挖掘、PubMed/ToolUniverse 或复现链。 | `帮我看看这些结果`、`这个能不能写文章`、`下一步怎么做`、`整理一下生信结果`、`写论文`、`改文章`、`审稿意见怎么回`、`做组会PPT` | `skills/local/bio-research-auto-router/`；同时镜像到 `skills/global/bio-research-auto-router/` |
| `bioinfo-evidence-orchestrator` | 生信证据总控，只负责分析路由、证据整理、风险表、图表清单和 `EVIDENCE_PACK.md`，不写论文。 | `生信分析`、`组学分析`、`GEO/SRA/accession`、`QC`、`富集分析`、`RNA-seq`、`写论文前整理结果`、`复现生信流程` | `skills/local/bioinfo-evidence-orchestrator/`；同时镜像到 `skills/global/bioinfo-evidence-orchestrator/` |
| `bio-paper-writing` | 生信论文写作总控，从证据包、图表、分析摘要或中文笔记写 abstract、introduction、discussion、title、outline。 | `生信论文`、`写abstract`、`写introduction`、`写Discussion`、`根据结果写论文`、`中文实验记录写英文论文` | `skills/local/bio-paper-writing/`；同时镜像到 `skills/global/bio-paper-writing/` |
| `bio-results-writing` | 根据 figure/table/evidence pack 写 Results 段落和图文对应表，不跑分析、不补 FDR/p value。 | `根据图表写结果`、`生信Results`、`RNA-seq结果写作`、`富集结果写作`、`多组学结果段落` | `skills/local/bio-results-writing/`；同时镜像到 `skills/global/bio-results-writing/` |
| `bio-methods-writing` | 根据 workflow provenance、命令、配置、软件版本和作者笔记写可复现 Methods。 | `生信Methods`、`材料与方法`、`workflow写法`、`可复现方法`、`软件参数怎么写` | `skills/local/bio-methods-writing/`；同时镜像到 `skills/global/bio-methods-writing/` |
| `bio-polishing` | 生信论文润色、中译英、术语统一、claim calibration 和 overclaim 检查。 | `生信论文润色`、`中译英`、`SCI润色`、`Results润色`、`Discussion润色`、`术语统一`、`overclaim检查` | `skills/local/bio-polishing/`；同时镜像到 `skills/global/bio-polishing/` |
| `bio-reviewer-response` | 生信审稿意见逐点回复，覆盖 batch effect、FDR、外部验证、数据泄露、样本量、可复现性等问题。 | `生信审稿回复`、`逐点回复`、`大修回复`、`reviewer质疑batch effect`、`FDR`、`外部验证`、`数据泄露` | `skills/local/bio-reviewer-response/`；同时镜像到 `skills/global/bio-reviewer-response/` |
| `bio-data-code-availability` | 生信 Data / Code Availability，覆盖 GEO、SRA、ENA、BioProject、BioSample、PRIDE、GitHub、Zenodo 等。 | `生信数据可用性`、`代码可用性`、`GEO/SRA/ENA`、`BioProject`、`BioSample`、`PRIDE`、`Zenodo`、`source data` | `skills/local/bio-data-code-availability/`；同时镜像到 `skills/global/bio-data-code-availability/` |
| `bio-paper2ppt` | 生信论文转中文组会 / journal club PPT，强调 workflow、关键图、证据链、局限性和讨论问题。 | `生信论文转PPT`、`组会汇报`、`journal club`、`多组学论文汇报`、`单细胞论文汇报` | `skills/local/bio-paper2ppt/`；同时镜像到 `skills/global/bio-paper2ppt/` |

常见自然语言路由示例：

| 用户说法 | 默认处理 |
|---|---|
| `这些结果能不能写文章` | `bio-research-auto-router` -> `bioinfo-evidence-orchestrator`，先判断证据强度和缺口 |
| `帮我分析并写文章` | 先证据线生成 `EVIDENCE_PACK.md`，再进入写作线 |
| `这些图帮我写一下` | `bio-results-writing` |
| `这个流程帮我写成材料方法` | `bio-methods-writing` |
| `这段帮我改得像论文` | `bio-polishing` |
| `审稿人这个问题怎么回` | `bio-reviewer-response` |
| `数据和代码怎么写` | `bio-data-code-availability` |
| `做个组会 PPT` | `bio-paper2ppt` |
| `这篇文献是怎么做的` | `literature-method-data-miner` |

| Skill | 作用 | 典型触发语 | 位置 |
|---|---|---|---|
| `literature-method-data-miner` | 把“文献是怎么做的”这类短提示自动理解为：从文献中提取科研方法、正文/表图/附录/补充材料数据、复现细节和可借鉴做法；如果文献未提供，则先走深度调研找文献。 | `文献是怎么做的`、`这篇文献怎么做的`、`参考文献是怎么做的`、`文献里的方法`、`参考文献的做法`、`从文献找科研方法`、`正文和附录数据`、`补充材料数据` | `skills/local/literature-method-data-miner/`；同时镜像到 `skills/global/literature-method-data-miner/` |
| `tooluniverse` | 生命科学数据库总路由，用于基因、蛋白、疾病、药物、化合物等事实查证和数据库查询。 | `生物`、`医学`、`生命科学`、`基因`、`蛋白`、`疾病`、`药物`、`UniProt`、`ChEMBL`、`ClinVar`、`GWAS` | `skills/global/tooluniverse/` |
| `tooluniverse-literature-deep-research` | 科学文献深度调研，包含主题消歧、证据分级、主题提取和结构化报告。 | `文献深度调研`、`研究进展`、`机制证据`、`证据分级`、`基因/蛋白/药物/疾病综述` | `skills/global/tooluniverse-literature-deep-research/` |
| `pubmed-database` | PubMed / E-utilities / MeSH 查询与医学文献检索。 | `PubMed`、`MeSH`、`医学文献`、`布尔检索`、`批量文献检索` | `skills/global/pubmed-database/` |
| `systematic-literature-review` | 系统综述流水线：多源检索、去重、逐篇评分、分主题、写综述。 | `系统综述`、`文献综述`、`related work`、`相关工作`、`文献调研` | `skills/global/systematic-literature-review/` |
| `read-arxiv-paper` | 对 arXiv 论文下载 TeX 源并解析公式/结构。 | `读arXiv论文`、`arXiv URL`、`TeX源`、`论文公式`、`解析论文结构` | `skills/global/read-arxiv-paper/` |
| `paper-reading-workflow` | 论文精读总路由：用户要 read / 精读 / 总结 / 拆解 / 批判性审读 / 生成 Obsidian 笔记时默认走该路由，将任务导向 `deeppapernote` 核心生产流程，同时强制加入 `literature-method-data-miner`（方法/数据/复现）和 `scientific-critical-thinking`（证据强度/局限/过度声称）两个分析视角，默认输出一篇整合中文 Obsidian Markdown 笔记。 | `精读论文`、`read this paper`、`拆解这篇论文`、`批判性审读`、`生成论文笔记`、`paper-reading-workflow` | `skills/local/paper-reading-workflow/` |
| `deeppapernote` | 单篇论文深度精读笔记生成器：给定论文标题/DOI/URL/arXiv ID/Zotero 条目/本地 PDF，生成结构化中文 Markdown 笔记，含证据分析、图表占位和 Obsidian vault 写入。 | `给这篇论文生成深度笔记`、`写论文精读笔记`、`deep paper note`、`deeppapernote`、`逐篇精读`、`论文深度笔记` | `skills/global/deeppapernote/` |
| `literature-reading-and-synthesis` | 科学论文主动阅读与综合：阅读策略、claim/evidence 抽取、图表拆解、跨论文比较、文献追踪、synthesis matrix、可复用笔记。 | `精读论文`、`每篇文章总结`、`阅读策略`、`claim extraction`、`synthesis matrix`、`figure unpacking`、`跨论文比较` | `skills/global/literature-reading-and-synthesis/` |
| `paper-context-resolver` | 论文复现中补齐关键论文细节，例如数据集版本、split、checkpoint、metric。 | `论文复现`、`复现细节`、`数据集版本`、`dataset split`、`评估协议`、`checkpoint映射` | `skills/global/paper-context-resolver/` |
| `env-and-assets-bootstrap` | 复现环境和资源准备，聚焦 conda、依赖、checkpoint、dataset/cache 路径。 | `复现环境`、`依赖安装`、`checkpoint路径`、`dataset路径`、`cache目录` | `skills/global/env-and-assets-bootstrap/` |
| `repo-intake-and-plan` | 扫描论文代码仓库，读取 README，提取最小可信复现计划。 | `论文代码仓库`、`复现仓库`、`README扫描`、`复现计划`、`最小可信复现` | `skills/global/repo-intake-and-plan/` |
| `minimal-run-and-audit` | 跑最小 smoke test / inference / evaluation，并记录标准化复现证据。 | `最小复现运行`、`smoke test`、`复现实验审计`、`repro_outputs`、`评估命令` | `skills/global/minimal-run-and-audit/` |
| `implement-paper` | 把论文方法实现为交互式 marimo notebook。 | `实现论文`、`论文变代码`、`paper to code`、`marimo`、`教学notebook` | `skills/global/implement-paper/` |
| `tooluniverse-sequence-retrieval` | 从 NCBI/ENA 检索 DNA/RNA/蛋白序列。 | `序列检索`、`FASTA`、`NCBI`、`ENA`、`GenBank`、`RefSeq`、`accession` | `skills/global/tooluniverse-sequence-retrieval/` |
| `tooluniverse-protein-structure-retrieval` | 检索 PDB/PDBe/AlphaFold 蛋白结构并做质量/元数据整理。 | `蛋白结构`、`PDB`、`PDBe`、`AlphaFold`、`三维结构`、`晶体结构` | `skills/global/tooluniverse-protein-structure-retrieval/` |
| `tooluniverse-rnaseq-deseq2` | RNA-seq / PyDESeq2 差异表达分析和结果解释。 | `RNA-seq`、`转录组`、`DESeq2`、`差异表达`、`DEG`、`count matrix` | `skills/global/tooluniverse-rnaseq-deseq2/` |
| `tooluniverse-gene-enrichment` | GO/KEGG/Reactome/GSEA/ORA 富集和通路分析。 | `基因富集`、`GO富集`、`KEGG`、`Reactome`、`GSEA`、`通路分析` | `skills/global/tooluniverse-gene-enrichment/` |
| `scientific-critical-thinking` | 科研严谨性、方法学、实验设计、统计有效性和证据质量审查。 | `批判性审读`、`方法学评估`、`统计有效性`、`偏倚`、`混杂`、`证据质量` | `skills/global/scientific-critical-thinking/` |
| `scientific-visualization` | 期刊级科学数据图表、多面板图、误差棒、显著性标记和导出格式；偏数据可视化。 | `科学绘图`、`科研图表`、`期刊级figure`、`多面板图`、`显著性标记` | `skills/global/scientific-visualization/` |
| `scientific-explanatory-schematics` | 科研解释性插图的必要性判定、brief、设计模式和质量验收；用于文献笔记/项目总览中的技术路线图、机制图、原理图、补充图、原文 Figure/Table 讲解，强调原文证据优先和自绘图证据边界。 | `技术路线图`、`技术机制图`、`机制图`、`原理图`、`技术原理说明图`、`流程图`、`工作流图`、`方法路线图`、`项目路线图`、`研究框架图`、`模型架构图`、`证据链图`、`混杂控制图`、`补充图`、`一图流`、`图解`、`示意图`、`配图`、`论文Figure讲解`、`原文图讲解`、`Figure/Table拆解`、`插图太丑`、`插图不好看`、`重画/美化插图`、`绘图质量`、`graphical abstract`、`workflow schematic`、`mechanism diagram`、`model architecture figure` | `skills/local/scientific-explanatory-schematics/`；同时镜像到 `skills/global/scientific-explanatory-schematics/` |
| `scientific-slides` | 科研汇报、会议报告、答辩 PPT / Beamer 的结构和设计。 | `科研汇报`、`论文slides`、`会议报告`、`答辩PPT`、`scientific talk` | `skills/global/scientific-slides/` |

常用中文提示语的预期路由：

| 用户说法 | 优先触发 | 说明 |
|---|---|---|
| `文献是怎么做的`、`这篇文献怎么做的`、`参考文献是怎么做的` | `literature-method-data-miner` | 默认理解为提取科研方法、正文/表图/附录/补充材料数据、复现细节和可借鉴做法；如果文献未给出，先找文献。 |
| `寻找参考文献`、`搜索文献`、`查参考文献` | `auto-deep-research`；生物医学语境下再叠加 `pubmed-database` / `tooluniverse-literature-deep-research` | 普通找文献走通用调研；明确 PubMed/生信/医学时走专业数据库。 |
| `帮我找几篇 XXX 的参考文献` | `auto-deep-research` + `pubmed-database` | 适合快速列论文、DOI、PMID、摘要和相关性。 |
| `做系统综述`、`文献综述`、`related work` | `systematic-literature-review` | 适合多源检索、去重、逐篇评分、主题分组和综述写作。 |
| `根据这几篇文献有什么想法`、`整合这几篇文献` | `research-orchestrator` + `scientific-critical-thinking` | 多篇文献上传/给出后，先整合，再做方法学和创新点分析。 |
| `参考文献的做法`、`论文里的实验做法怎么复现` | `literature-method-data-miner`；复现细节缺口时叠加 `paper-context-resolver` | 区分“提取/比较科研方法”和“补齐复现细节”。 |
| `这个论文代码怎么跑/怎么复现` | `repo-intake-and-plan` → `env-and-assets-bootstrap` → `minimal-run-and-audit` | 如果落入已有 `.project_os/` 项目，先经 `research-project-os` 建 task/run，再逐阶段推进。 |
| `逐篇精读`、`每篇文章都要总结`、`论文深度笔记` | `paper-reading-workflow` → `deeppapernote`（强制 `literature-method-data-miner` + `scientific-critical-thinking` 两个视角）；`paper-reading-workflow` 不可用时回退 `literature-reading-and-synthesis` | 在 `project-literature-bridge` 深读模式下逐篇生成完整笔记，替换浅层摘要。 |

### 需求澄清 / 拆任务 / 执行辅助

| Skill | 作用 | 典型触发语 | 位置 |
|---|---|---|---|
| `grill-me` | 一次问一个问题，澄清需求、方案、约束和风险。 | `先讨论`、`先问清楚`、`完善方案`、`需求澄清`、`方案评审`、`把思路问透` | `skills/global/grill-me/` |
| `ticket-breakdown` | 把任务、ticket、issue 拆成小步骤和验收条件。 | `拆任务`、`拆步骤`、`验收步骤`、`把当前任务拆小`、`ticket breakdown` | `skills/global/ticket-breakdown/` |
| `small-script-generator` | 生成小型安全脚本或批处理 helper，默认注重 dry-run 和安全性。 | `写个小脚本`、`生成脚本`、`批量处理`、`自动化处理`、`dry-run script` | `skills/global/small-script-generator/` |
| `config-file-explainer` | 解释配置文件、关键选项、风险和安全修改方式。 | `解释配置`、`看一下 config`、`config.toml`、`yaml/json/toml 配置`、`配置项什么意思` | `skills/global/config-file-explainer/` |

### 调试 / 验证 / 日志

| Skill | 作用 | 典型触发语 | 位置 |
|---|---|---|---|
| `log-summarizer` | 总结日志、错误输出、traceback、运行失败原因，并给下一步。 | `分析日志`、`看报错`、`traceback`、`error output`、`长任务失败日志` | `skills/global/log-summarizer/` |
| `bug-repro-plan` | 制定最小可复现 bug 计划，包括环境、步骤、期望/实际、证据清单。 | `复现 bug`、`最小复现`、`reproduce issue`、`问题复现步骤` | `skills/global/bug-repro-plan/` |
| `ci-failure-triage` | 分析 CI/build/test pipeline 失败，区分稳定失败和 flaky。 | `CI 失败`、`GitHub Actions`、`pipeline failed`、`build failed`、`flaky CI` | `skills/global/ci-failure-triage/` |

### 内容编辑 / 汇报 / PPT

| Skill | 作用 | 典型触发语 | 位置 |
|---|---|---|---|
| `edit-article` | 修改、润色、重构文章草稿。 | `改文章`、`润色`、`修改 draft`、`edit article`、`revise` | `skills/global/edit-article/` |
| `ppt-image-first` | PPT/汇报 deck 的对话优先、图片预览优先工作流。 | `做 PPT`、`汇报 PPT`、`答辩稿`、`presentation`、`deck`、`路演 deck` | `skills/global/ppt-image-first/` |

## 推荐组合方式

### 大项目继续推进

1. 如果项目已有或需要 `.project_os/`，优先用 `research-project-os` / `project-skeleton`：`开工`、`项目骨架`、`大项目`、`逐步推进`、`继续下一步`、`当前进展`、`制定计划`、`拆解任务`、`task_plan.md`、`项目状态`、`写一个项目状态文档`、`开始分析`、`先跑`、`先画`、`绘图`、`发育树`、`系统发育`、`Newick`、`alignment/tree/parsimony/treeness/RCV`、`新建会话`、`切会话`、`暂停会话`、`恢复会话`、`会话清理`、`恢复检查`、`开始运行`、`记录结果` 等短触发先经 `project_os.py route` 生成计划。
2. 需求不清时用 `grill-me`；需要拆小步骤时用 `ticket-breakdown`。
3. 有正式生成型分析、重跑或换参数时，通过 harness 创建 branch/task/run，并把 provenance 写入 `RUN_MANIFEST.json`；`RUNS_INDEX.tsv` 由 canonical `.project_os/indexes/runs.tsv` 单向刷新。
4. 结果进入 candidate/accepted/current/release 时走 result CLI 和 approval gate；`RESULTS_INDEX.md` 是 derived human view，只有用户确认或明确 promote/release 时才进入 `current/` / `release/`。
5. 结束前用 `summarize-state` 或 `update-handoff` 更新薄人类入口；长细节放入 branch/task/run/result/asset/release 对应文件。

### 整理混乱项目结果

1. `project-version-curator` 先读 `PROJECT_STATE.md`、`RESULTS_INDEX.md`、`DECISIONS.md`、`DATA_ASSETS.md` 和 registries。
2. 生成 inventory / conflict audit / `CURATION_PLAN.md`，只做 dry-run，不直接删除。
3. 不信任文件名里的 `final/current`；以 `RESULTS_INDEX.md`、`current/`、registry 和 `DECISIONS.md` 判断 accepted/candidate/legacy/superseded。
4. 如需真正 copy/move/archive/release，再交给 `project-flow-guard` 或显式用户确认。
5. 最后由 `research-project-os summarize-state` / `update-handoff` 记录整理结论、关键入口和下一步。

### 新建并上传 skill

1. 触发 `skill-library-publisher`。
2. 在 `skills/local/<skill-name>/SKILL.md` 创建新 skill。
3. 运行 `validate_skills.py`。
4. 运行 `sync_skills.py --apply --commit --push`。

## 当前 inventory

生成文件：

```text
registry/SKILL_INVENTORY.tsv
registry/skills.json
```

刷新方式：

```bash
python scripts/sync_skills.py --apply
```
