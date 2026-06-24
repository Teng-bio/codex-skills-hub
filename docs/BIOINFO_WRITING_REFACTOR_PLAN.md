# Bioinformatics Agent + Writing Skill Refactor Plan

更新日期：2026-05-25

目标：基于本地已有 `codex-skills-hub` skill 生态，重构 `nature-skills`/科研写作能力，而不是重复造一套生信分析工具。最终形成一个自动路由入口和两条互不重叠、但可协作的能力线：

0. **自动路由入口**：`bio-research-auto-router`，用于普通/模糊中文任务的第一层判断。
1. **生信 Agent 线**：查数据库、做/审分析、复现、QC、证据整理。
2. **论文写作 Skill 线**：根据已整理证据写论文、润色、审稿回复、PPT、Data/code availability。

核心原则：

```text
生信 Agent 负责事实和证据，不写论文。
写作 Skill 负责表达和投稿材料，不跑分析。
二者通过 EVIDENCE_PACK.md 交接。
```

---

## 1. 当前可复用本地能力

本计划以 `/home/teng/claude_code/codex-skills-hub` 为主仓库，优先复用其中 `skills/global/` 和 `skills/local/` 的已有能力。

### 1.1 生信/科研证据层已有能力

| 能力 | 已有 skill | 建议处理 |
|---|---|---|
| 生命科学数据库总路由 | `tooluniverse` | 直接复用，不重复实现数据库总入口 |
| 文献深度调研与证据分级 | `tooluniverse-literature-deep-research` | 直接复用，输出写入 evidence pack |
| PubMed / MeSH / E-utilities | `pubmed-database` | 直接复用，用于医学/生物文献检索 |
| 系统综述 | `systematic-literature-review` | 直接复用，不并入写作 skill |
| 文献方法和数据挖掘 | `literature-method-data-miner` | 重点复用，承接“文献是怎么做的”类需求 |
| RNA-seq / DESeq2 | `tooluniverse-rnaseq-deseq2` | 直接复用，作为专项分析工具 |
| GO/KEGG/Reactome/GSEA | `tooluniverse-gene-enrichment` | 直接复用，作为富集分析工具 |
| DNA/RNA/蛋白序列检索 | `tooluniverse-sequence-retrieval` | 直接复用 |
| 蛋白结构检索 | `tooluniverse-protein-structure-retrieval` | 直接复用 |
| 系统发育 | `research-project-os` first | 已有 `.project_os/` 项目中先建立 branch/task/run/result provenance，再调用项目脚本或通用工具执行 |
| 科研严谨性审查 | `scientific-critical-thinking` | 作为证据质量和方法学审计层 |
| 科学绘图 | `scientific-visualization` | 复用为通用绘图层；生信图可另建轻量包装 |
| 科研 slides | `scientific-slides` | 复用为通用科学汇报层 |
| 论文代码复现 | `repo-intake-and-plan`, `env-and-assets-bootstrap`, `minimal-run-and-audit`, `paper-context-resolver` | 直接复用，构成复现阶段工具链 |
| 长期项目工作台 | `research-project-os`, `project-skeleton` | 对需要 `.project_os/`、branch/task/run/result/data provenance、continuation 的长期项目作为 harness 入口 |
| 项目任务/状态内核 | `research-project-os` | 对 `.project_os/` 项目承接继续下一步、当前进展、制定计划、拆解任务、状态总结等触发 |
| 版本和产物守护 | `project-flow-guard`, `project-version-curator` | 对重跑、版本、结果整理进行守护 |

### 1.2 写作层已有能力

| 来源 | 已有能力 | 适合继承的部分 | 不应继承的部分 |
|---|---|---|---|
| `nature-writing` | Nature-style section drafting | section architecture、claim-evidence map、中文作者笔记转英文逻辑 | 不应绑定 Nature 作为唯一目标；不应承担生信分析 |
| `nature-polishing` | 学术英文润色 | 逻辑优先、claim calibration、overclaim check、section-aware polishing | 不应忽视生信术语和可复现报告要求 |
| `nature-response` | 审稿回复 | reviewer comment ID、action mapping、缺失证据标记 | 需要新增 batch effect、FDR、数据泄露、外部验证等生信审稿问题 |
| `nature-data` | Data Availability / FAIR | repository plan、FAIR checklist、DataCite 风格 | 需要加入 GEO/SRA/ENA/BioProject/BioSample/PRIDE 等生信仓库 |
| `nature-paper2ppt` | 论文转 PPT | evidence-first slide logic、中文组会场景 | 需要加入生信图表和 pipeline narrative |
| `nature-reader` | 全文阅读和图文对应 | source-grounded reading、figure/table placement | 需要增强 accession、software、pipeline、dataset extraction |

---

## 2. 目标能力分层

### 2.1 生信 Agent 线

生信 Agent 线不直接写论文，而是产生可追溯证据。

推荐最终本地 skills：

```text
skills/local/
  bio-research-auto-router/       # 自动识别模糊任务并路由到证据线或写作线
  bioinfo-evidence-orchestrator/    # 生信证据总控，路由到已有 tooluniverse/pubmed/复现/QC skills
  bioinfo-evidence-pack/            # 可选：只定义/校验 EVIDENCE_PACK.md 的结构
  bioinfo-omics-figure-brief/        # 可选：把数据图表转成“图表信息卡”，不写 Results prose
```

第一阶段只做：

```text
bioinfo-evidence-orchestrator
```

它的职责：

- 判断用户任务是文献、数据库、RNA-seq、富集、序列、蛋白结构、系统发育、复现还是 QC。
- 路由到已有本地/global skills。
- 整理分析结果、风险和缺失信息。
- 输出 `EVIDENCE_PACK.md`。
- 不写 abstract、Results、Discussion、cover letter 或 rebuttal。

### 2.2 论文写作 Skill 线

写作线只消费证据，不跑分析。

推荐最终本地 skills：

```text
skills/local/
  bio-paper-writing/                # 生信论文写作总控：title/abstract/introduction/results/discussion/outline
  bio-results-writing/              # 根据 figure/table/evidence pack 写 Results
  bio-methods-writing/              # 根据 pipeline/provenance 写可复现 Methods
  bio-polishing/                    # 生信论文润色和中译英
  bio-reviewer-response/            # 生信审稿意见回复
  bio-data-code-availability/       # 生信 Data/code availability
  bio-paper2ppt/                    # 生信论文转中文组会 PPT
```

本轮已按“先规划、再基于本地 skill 重构”的路线一次性落地完整写作线：

```text
bio-paper-writing
bio-results-writing
bio-methods-writing
bio-polishing
bio-reviewer-response
bio-data-code-availability
bio-paper2ppt
```

这些写作 skills 均只消费 `EVIDENCE_PACK.md`、figure/table、analysis summaries、author notes 或 manuscript drafts；缺证据时标记风险并回到 `bioinfo-evidence-orchestrator`，不自行分析。

---

## 3. 核心接口：EVIDENCE_PACK.md

所有生信 Agent 线输出都应尽量落到统一证据包。写作线默认只消费该证据包或用户显式提供的 figure/table/notes。

```markdown
# Evidence Pack

## 1. Study question
- Biological question:
- Computational question:
- Claim boundary:

## 2. Dataset inventory
| dataset | accession/path | organism | assay | samples | groups | metadata status | notes |
|---|---|---|---|---:|---|---|---|

## 3. Workflow provenance
| step | tool/package | version | parameters | reference assets | output | status |
|---|---|---|---|---|---|---|

## 4. Statistical design
- comparison/design formula:
- covariates/batch variables:
- normalization:
- multiple testing:
- thresholds:

## 5. Main findings
| finding ID | finding | evidence | figure/table | strength | caveat |
|---|---|---|---|---|---|

## 6. Figure/table inventory
| item | message | source data | key stats | writing use | status |
|---|---|---|---|---|---|

## 7. External validation and database support
| claim/finding | source | identifier | support level | notes |
|---|---|---|---|---|

## 8. Limitations and risks
- ...

## 9. Missing information
- ...

## 10. Writing handoff
- suggested manuscript sections:
- usable claims:
- claims needing softer wording:
- claims not supported:
```

### Strength labels

| Label | Meaning |
|---|---|
| `strong` | 直接证据支持，统计设计合理，有复现/验证或外部支持 |
| `moderate` | 主分析支持，但缺外部验证、部分元数据或部分控制项 |
| `weak` | 探索性结果，样本量/设计/验证不足 |
| `unsupported` | 用户提到但当前材料未支持 |

---

## 4. 新 skill 与已有 skill 的协作关系

### 4.1 `bioinfo-evidence-orchestrator` 应调用/路由的已有 skill

| 用户意图 | 优先路由 |
|---|---|
| 查 PubMed、MeSH、PMID、医学参考文献 | `pubmed-database` |
| 查生命科学数据库事实、基因、蛋白、疾病、药物、通路 | `tooluniverse` |
| 做文献深度调研、机制证据、证据分级 | `tooluniverse-literature-deep-research` |
| “文献是怎么做的/参考文献的做法” | `literature-method-data-miner` |
| RNA-seq / DEG / DESeq2 | `tooluniverse-rnaseq-deseq2` |
| GO/KEGG/Reactome/GSEA/ORA | `tooluniverse-gene-enrichment` |
| 序列、FASTA、GenBank、RefSeq | `tooluniverse-sequence-retrieval` |
| 蛋白结构、PDB、AlphaFold | `tooluniverse-protein-structure-retrieval` |
| 系统发育、Newick、ortholog | `research-project-os` first |
| 方法学、统计、偏倚、证据质量审查 | `scientific-critical-thinking` |
| 论文代码复现 | `repo-intake-and-plan` -> `env-and-assets-bootstrap` -> `minimal-run-and-audit` |
| 需要长期项目工作台、run/result/data provenance、继续当前分支/任务 | `research-project-os` / `project-skeleton` |
| 需要多阶段推进/当前进展/恢复上下文 | `research-project-os`（已有 `.project_os` 时） |

### 4.2 `bio-paper-writing` 应继承/参考的已有 skill

| 写作任务 | 参考来源 |
|---|---|
| section architecture | `nature-writing` |
| polish / overclaim / style | `nature-polishing` |
| evidence and method audit | `scientific-critical-thinking` |
| Data/code availability | `nature-data` + 生信仓库规则；当前由 `bio-data-code-availability` 承接 |
| Rebuttal structure | `nature-response` |
| PPT narrative | `nature-paper2ppt` + `scientific-slides`；当前由 `bio-paper2ppt` 承接生信组会场景 |
| Figures | `nature-figure` + `scientific-visualization` |

---

## 5. 命名和边界建议

### 5.1 不推荐的做法

- 不要把所有生信功能塞进一个巨大 `bioinfo-agent`。
- 不要复制 `tooluniverse-*` 已有专项 skill 的实现。
- 不要让 `bio-paper-writing` 调用数据库后直接改结论。
- 不要把 Nature/CNS 引用限制作为生信论文默认规则。
- 不要让写作 skill 为了流畅而补齐缺失的样本量、FDR、p value、accession、software version。

### 5.2 推荐命名

| 类型 | 推荐命名 |
|---|---|
| 生信证据总控 | `bioinfo-evidence-orchestrator` |
| 生信论文总写作 | `bio-paper-writing` |
| Results 专项 | `bio-results-writing` |
| Methods 专项 | `bio-methods-writing` |
| 润色专项 | `bio-polishing` |
| 审稿回复 | `bio-reviewer-response` |
| 数据代码可用性 | `bio-data-code-availability` |
| PPT | `bio-paper2ppt` |

---

## 6. 实施路线

### Phase 0：清理草稿和冻结现状

- 回滚误创建/未确认的 `nature-skills` bio 草稿。
- 不在 `nature-skills` 继续创建新 skill。
- 以 `codex-skills-hub` 为主规划仓库。

### Phase 1：只做规划文档

创建：

```text
docs/BIOINFO_WRITING_REFACTOR_PLAN.md
docs/SKILL_ROUTING_MATRIX.md
```

不创建任何 `skills/local/<new-skill>/`。

### Phase 2：创建一个生信证据总控 skill

创建：

```text
skills/local/bioinfo-evidence-orchestrator/SKILL.md
```

只做路由和 evidence pack，不重复实现数据库/分析。

### Phase 3：创建写作总控 skill

已创建：

```text
skills/local/bio-paper-writing/SKILL.md
skills/local/bio-paper-writing/references/evidence-pack-input.md
skills/local/bio-paper-writing/references/article-types.md
skills/local/bio-paper-writing/references/section-workflows.md
```

只消费 evidence pack、figure/table、author notes，不跑分析。

### Phase 4：拆分写作专项

已按使用边界拆出：

1. `bio-results-writing`
2. `bio-methods-writing`
3. `bio-polishing`
4. `bio-reviewer-response`
5. `bio-data-code-availability`
6. `bio-paper2ppt`

### Phase 5：验证触发边界

用 `docs/SKILL_ROUTING_MATRIX.md` 的测试用例检查：

- 是否误触发写作 skill 去跑分析。
- 是否误触发生信 agent 去写 prose。
- 是否和 `nature-*`、`tooluniverse-*`、`scientific-*` skills 产生冲突。
- 已执行 `scripts/validate_skills.py` 与 `scripts/sync_skills.py`，registry 中应包含全部 `bio-*` / `bioinfo-*` 本地 skills。

---

## 7. 验收标准

第一阶段完成标准：

- 规划文档存在且明确两条线边界。
- 没有创建新 skill。
- `nature-skills` 无未确认草稿改动。

第二阶段完成标准：

- `bioinfo-evidence-orchestrator` 可以把至少 10 类生信请求路由到已有 skill。
- 输出标准 `EVIDENCE_PACK.md`。
- 不写 manuscript prose。

第三阶段完成标准：

- `bio-paper-writing` 可以从 evidence pack 生成 abstract / Results / Discussion scaffold。
- 所有缺失证据用 placeholder 或 risk flag 表示。
- 不跑数据库、不跑分析、不编造结果。

第四阶段完成标准：

- `bio-results-writing`、`bio-methods-writing`、`bio-polishing`、`bio-reviewer-response`、`bio-data-code-availability`、`bio-paper2ppt` 均存在独立 `SKILL.md`。
- 每个专项 skill 都声明“只写作/整理表达，不做分析”的红线。
- 生信审稿、可用性声明和 PPT 场景覆盖 batch effect、FDR、外部验证、数据泄露、GEO/SRA/ENA/BioProject/BioSample/PRIDE、workflow narrative 等生信特有问题。

当前完成状态：

```text
Phase 1 规划文档：complete
Phase 2 bioinfo-evidence-orchestrator：complete
Phase 3 bio-paper-writing：complete
Phase 4 专项写作 skills：complete
Phase 5 验证和 registry 同步：complete after latest validation/sync
Auto-router：bio-research-auto-router added for vague prompt routing
```
