# Research Project OS 开发方案审查报告

Date: 2026-06-23
Status: formal review of `RESEARCH_PROJECT_OS_COMPLETE_DEVELOPMENT_PLAN.md`
Reviewer: harness 构建专家视角（纯方案层面，不涉及代码实现状态）

---

## 1. 审查范围

本报告对 `docs/RESEARCH_PROJECT_OS_COMPLETE_DEVELOPMENT_PLAN.md` 进行纯方案设计层面的审查，涵盖：

- 架构分层与设计原则
- 范围边界与优先级划分
- Schema 契约定义
- 工作流与状态机设计
- 安全门与操作边界
- 扩展层接口预留
- 文档组织与权威性
- 设计完整性

不涉及当前代码实现状态的比对。

---

## 2. 总体结论

**综合评分：4.5 / 5**

这是一份架构判断成熟、契约定义严谨的 harness 设计方案。分层清晰、边界明确、扩展性预留到位。核心设计决策（harness-first、branch-first 物理工作区、run/result 语义分离、promotion 三层门控、hook 只调 CLI 不拥有逻辑）都是正确的。

需要在 schema freeze 阶段闭合的问题集中在 **几处设计决策的显式化**（ID 唯一性、canonical 关系、config 语义）和 **两个结构性缺口**（迁移映射表、测试策略）。这些问题不改变架构方向，只需在 P0.1 中一并处理。

---

## 3. 设计亮点（应保持）

### 3.1 Harness-first 产品定位

方案明确区分了七层概念并定义了优先级：

| 概念 | 作用 | 是否核心状态来源 | 当前实现重点 |
|---|---|---:|---:|
| harness | 项目内状态、流程、索引、provenance | 是 | 是 |
| skill | 让 agent 知道何时、如何操作 harness | 否 | 是，但保持薄 |
| CLI/backend | 确定性创建/修改/校验项目文件 | 是 | 是 |
| adapter | 让 Codex/Claude 接入同一套 harness | 否 | 只做 Codex/Claude |
| hook | 特定事件自动执行辅助动作 | 否 | 暂不实现，仅预留 |
| plugin | 分发/安装/打包 | 否 | 后置 |
| dashboard | 生成展示视图 | 否 | 后置 |

这避免了最常见的失败模式——把 skill prompt 当产品，导致状态散落在聊天记忆里不可恢复。

### 3.2 Branch-first 物理工作区

方案把 branch 做成物理目录隔离而非纯字段。对于科研项目多线并行（方法 A vs 方法 B vs 方向探索）的场景：

- **隔离**：branch 下的 task / research / notes / decisions 互不干扰
- **聚合**：全局 `indexes/*.tsv` 提供跨 branch 查询和未来 dashboard 入口
- **provenance**：run 路径 `runs/<branch_id>/<run_id>/` 天然携带 branch 归属

设计原则第 2 条（物理隔离）和第 3 条（全局索引强制）的组合是架构支柱。

### 3.3 Run / Result 语义分离

> "Run is provenance, result is discoverable output"

run 记录"产生过程"（inputs/commands/code_ref/environment），result 回答"成果在哪"（status/promotion/current）。人类通过 `RESULTS_INDEX.md` 和 `current/` 查找成果，不需要翻 run 目录。

### 3.4 Promotion 三层安全门

- dry-run 默认（先看会发生什么）
- `--apply` 显式授权（才真正写入/复制）
- `--replace` 独立确认（才覆盖已有 target）

加上 promotion 目标区分 `current/branches/<branch_id>/` 和 `current/project/`，以及 `promoted_to` / `accepted_at` / `replaced_by` 审计字段，在科研场景下是恰当的。

### 3.5 Hook 边界定义

- hook 不拥有业务逻辑
- hook 只调用现有 CLI
- hook 默认失败不破坏主流程
- hook 从只读/提醒开始
- guard hook 必须 opt-in
- hooks 不新增 canonical state

保证了"不启用 hook 时 harness 完整可用"这个核心约束。Lifecycle event 名称已冻结，未来 hook 有稳定接口可挂。

### 3.6 短触发路由层

路由链 `phrase -> intent -> state check -> CLI action -> verification` 定义清晰。每个 intent 都绑定了状态检查、缺失信息处理、CLI command 和写后验证。短触发词提升为正式工作层（P0.8），而非在 skill description 里堆关键词。

---

## 4. 需要推敲的设计问题

### 4.1 [高] task_id / run_id 全局唯一性未定义

**问题**

方案采用 branch-local 存储（`.project_os/branches/<branch_id>/tasks/<task_id>/`），但全局索引 `tasks.tsv` 是聚合的。如果两个 branch 各自创建同名 task，`task_id` 会在全局索引中冲突。

当前 schema 中 `tasks.tsv` 的 key 是 `task_id` 单字段，没有 `(branch_id, task_id)` 复合键的约定。`runs.tsv` 同理。

**影响**

- schema freeze 无法正确定义 upsert 语义
- `find_run_manifest()` 等查找函数无法确定全局唯一性
- 多 branch 场景下索引冲突

**需要决策**

从以下两个方案中选择一个并在 schema 中显式声明：

- **方案 A**：task_id / run_id 强制全局唯一（生成时加 branch 前缀或时间戳保证），单字段 key。优点：查找简单；缺点：ID 较长。
- **方案 B**：允许 branch-local 唯一，全局索引用 `(branch_id, task_id)` 复合 key。优点：ID 可读性好；缺点：upsert 逻辑更复杂。

**推荐**：方案 A，因为全局唯一 ID 对人类和 agent 都更简单，且科研场景下 task/run 数量有限，ID 长度不构成负担。

---

### 4.2 [高] RUNS_INDEX.tsv 与 indexes/runs.tsv 的 canonical 关系模糊

**问题**

方案说"root `RUNS_INDEX.tsv` 从 `.project_os/indexes/runs.tsv` 派生或同步"，但没有定义：

- 哪个是 canonical source of truth？
- 派生方向是单向还是双向？
- 两者不一致时 `doctor` 报告还是自动修复？
- `refresh-indexes` 是覆盖 root 文件还是 merge？

同样的关系适用于 `RESULTS_INDEX.md` 与 `indexes/results.tsv`、`DATA_ASSETS.md` 与 `indexes/assets.tsv`。

**影响**

- 用户不确定修改哪个文件
- `refresh-indexes` 和 `doctor` 行为不明确
- 未来 hooks 调用时不清楚从哪里读

**需要明确的原则**

> `.project_os/indexes/*.tsv` 是 canonical，root 人类可读文件（`RUNS_INDEX.tsv` / `RESULTS_INDEX.md` / `DATA_ASSETS.md`）是 derived view。`refresh-indexes` 单向生成。`doctor` 检测不一致时报告但不自动修复。

方案在原则第 8 条暗示了 `.project_os/` 是 canonical，但需要在 schema 层面显式声明 root 文件的 derived 地位。

---

### 4.3 [中] config.yaml 的语义边界未分类

**问题**

`CONFIG_TEXT` 定义了 `schema_version`、`run_roots`、`adapters`、`promotion_requires_user_approval` 等配置项，但方案没有说明每一项是：

- **declarative**（声明期望状态，CLI 读取并遵守行为）
- **descriptive**（记录当前状态，不影响行为）

例如：
- `run_roots` 影响 `create-run` 默认路径吗？还是仅记录允许的 run 根目录？
- `adapters.codex: true / claude_code: false` 是记录已安装状态，还是控制是否允许安装？
- `promotion_requires_user_approval: true` 如果改为 false 会关闭安全门吗？

**影响**

- 用户会误以为修改 config 就能改变行为，但实际上 CLI 不读取
- 或者相反，用户以为 config 是纯记录，但某些项实际影响逻辑

**需要明确**

在 schema 或 harness_contract.md 中为每一项标注类型：

| 配置项 | 类型 | 说明 |
|---|---|---|
| `schema_version` | descriptive | 记录 schema 版本，不改变行为 |
| `run_roots` | declarative | `create-run` 默认从此列表第一项读取 |
| `adapters.*` | descriptive | 记录已安装状态，`install-adapters` 不依赖此值 |
| `promotion_requires_user_approval` | declarative | 若为 false 则 `promote-result` 可跳过 dry-run 直接 apply（高风险，默认 true） |

---

### 4.4 [中] 迁移策略缺乏具体映射表

**问题**

P1.7 的 migration/adoption 只有 5 条原则性描述。对于 flat layout → branch-first 迁移，实际涉及：

| 旧路径/字段 | 新路径/字段 | 迁移动作 |
|---|---|---|
| `.project_os/tasks/<task_id>/` | `.project_os/branches/main/tasks/<task_id>/` | 物理移动 |
| `runs/<run_id>/` | `runs/main/<run_id>/` | 物理移动 |
| `RUN_MANIFEST.json` 缺 `branch_id` | 补 `"branch_id": "main"` | 字段补全 |
| `tasks.tsv` 旧 header | 新 header（含 `branch_id`） | header + 行迁移 |
| `runs.tsv` 旧 header | 新 header（含 `branch_id`） | header + 行迁移 |
| `results.tsv` 旧 header | 新 header（含 `branch_id`, `promoted_to`） | header + 行迁移 |
| `run_links.tsv` 中路径 | 更新为 branch-aware 路径 | 路径更新 |

**影响**

- schema freeze 后如果发现迁移缺信息，又要改 schema
- 迁移命令实现时缺乏明确规范

**建议**

在 P0.1 schema freeze 时同步定义迁移映射表（即使迁移命令在 P1 才实现），放入 `docs/RESEARCH_PROJECT_OS_BRANCH_FIRST_SCHEMAS.md` 或新增 `references/migration_mapping.md`。

---

### 4.5 [中] context_manifest.jsonl 未覆盖 branch 级别

**问题**

`default_context_manifest()` 只列 root 级文件（`PROJECT_STATE.md` / `workflow.md` / `DATA_ASSETS.md` 等）。branch-first 后，恢复 task 时还应加载 branch 的 `objective.md` 和 `context.md`。

方案原则第 4 条说"agent 恢复任务时只读当前 task 的 context_manifest"，但如果 manifest 不包含 branch 级文件，agent 恢复时会缺少 branch 上下文。

**建议**

明确 branch context 是 **运行环境** 的一部分，由 runtime pointer 解析自动加载，不经过 task manifest。在 runtime pointer 解析规则中显式加入：

```
current_branch
  -> .project_os/branches/<branch_id>/objective.md   # 自动加载
  -> .project_os/branches/<branch_id>/context.md      # 自动加载
  -> current_task
  -> .project_os/branches/<branch_id>/tasks/<task_id>/context_manifest.jsonl  # manifest 只列 task 级和 root 级
```

这样 manifest 保持 task-scoped，branch context 由解析链自动带入。

---

### 4.6 [中] 文档冗余与权威性

**问题**

方案声称自己是 canonical merged plan，但仍保留 4 个来源文档：

| 文档 | 内容 | 与 canonical plan 的关系 |
|---|---|---|
| `RESEARCH_PROJECT_OS_HARNESS_IMPLEMENTATION_PLAN.md` | 早期 harness 实现计划 | 内容已被 canonical plan 第 10-13 节覆盖 |
| `RESEARCH_PROJECT_OS_BRANCH_FIRST_ARCHITECTURE.md` | branch-first 架构设计 | 内容已被 canonical plan 第 5-7 节覆盖 |
| `RESEARCH_PROJECT_OS_BRANCH_FIRST_SCHEMAS.md` | branch-first schema | 内容已被 canonical plan 第 8 节覆盖 |
| `task_plan.md` | 15 phase 路线图 | 与 canonical plan 的 P0/P1/P2 高度重叠但结构不同 |

**影响**

- agent 恢复时不确定以哪个为准
- 文档间可能出现不一致描述

**建议**

在旧文档头部加标记：

```markdown
> ⚠️ Status: superseded by `docs/RESEARCH_PROJECT_OS_COMPLETE_DEVELOPMENT_PLAN.md`
> This document is retained as historical context only.
```

或者将旧文档中不在 canonical plan 中的唯一内容合并进来后归档。`task_plan.md` 应明确标注以 `RESEARCH_PROJECT_OS_COMPLETE_DEVELOPMENT_PLAN.md` 为准。

---

### 4.7 [低] P0 内部顺序的依赖关系

**问题**

当前 P0 顺序：
```
Schema → Init → Branch → Task → Run → Result → Doctor → Router → Adapters → Smoke
```

几处依赖问题：

1. **Task（P0.4）和 Run（P0.5）应合并**：它们的路径迁移改的是同一批 helper 函数（`task_dir()` / `run_dir()` / `find_run_manifest()`），分开做会导致中间态不可用（task 已在 branch 内但 run 仍在扁平路径）。

2. **Doctor（P0.7）应在 Result（P0.6）之前**：result 的 `register-result` 依赖 doctor 能验证 branch/task/run 一致性。

3. **Smoke（P0.10）应包含最小自动化验证**：方案只定义了 11 步手动操作，但没有自动化检查。P0 完成后每次验证都靠手动跑 11 步，回归风险很高。

**建议调整后的 P0 顺序**

```
P0.1 Schema freeze（含 ID 唯一性决策、canonical 关系声明、config 语义分类、迁移映射表）
P0.2 Init branch-first
P0.3 Branch commands
P0.4 Task + Run branch-aware（合并执行）
P0.5 Doctor / validate（提前）
P0.6 Result minimal lifecycle
P0.7 Short trigger router
P0.8 Codex / Claude adapters
P0.9 Smoke adoption（含最小自动化验证）
```

---

### 4.8 [低] 单文件 project_os.py 的扩展边界

**问题**

方案全部命令（P0 约 30 个，P1 完成后约 50+ 个）都指向单一 `project_os.py`。方案没有讨论这个文件何时应该拆分、按什么边界拆分。

**影响**

- 文件膨胀到被动拆分时，拆分时机和边界不理想
- 多人协作时单文件成为瓶颈

**建议**

在方案中定义拆分触发条件和目标结构（不阻塞 P0）：

```
触发条件（满足任一）：
- project_os.py 超过 1500 行
- 命令组超过 8 个
- 多人同时开发不同命令组

目标结构：
scripts/
  project_os.py          # CLI 入口 + dispatch
  _schema.py             # INDEX_HEADERS, REQUIRED_FIELDS, STATUSES
  _paths.py              # branch_dir, task_dir, run_dir, helpers
  _templates.py          # WORKFLOW_TEXT, CONFIG_TEXT, SPEC_TEXTS
  _commands/
    project.py
    branch.py
    task.py
    run.py
    result.py
    asset.py
    release.py
```

---

### 4.9 [低] 测试策略缺失

**问题**

方案 P0.10 只定义了手动 smoke test 步骤（11 步），P1 和 P2 中也没有任何自动化测试计划。`project_os.py` 在 P1 完成后预计 2000-3000 行，没有测试守护，branch-first 迁移这类大改动极易回归。

**建议**

在 P0 中增加一个轻量测试模块，不需要复杂框架，stdlib `unittest` 即可：

```
tests/test_project_os.py
  - test_init_creates_branch_first_layout
  - test_create_branch_creates_workspace_and_index
  - test_task_uses_branch_path
  - test_run_uses_branch_path
  - test_register_result_links_to_run
  - test_promote_result_dry_run_does_not_write
  - test_promote_result_apply_writes_to_current
  - test_doctor_detects_broken_pointers
  - test_validate_detects_header_mismatch
  - test_refresh_indexes_rebuilds_all
```

重点验证 **路径正确性** 和 **状态一致性**，不追求全覆盖。

---

## 5. 设计完整性检查

| 维度 | 状态 | 说明 |
|---|---|---|
| 状态机定义 | ✅ 完整 | branch/task/run/result 各自有明确状态枚举和转换 |
| 文件契约 | ✅ 完整 | 每个文件都有 schema 和字段定义 |
| 路径契约 | ✅ 完整 | branch-first 路径规则明确 |
| 安全门 | ✅ 完整 | dry-run / apply / replace 三层门控 + 非破坏性原则 |
| 扩展预留 | ✅ 完整 | hooks / plugin / dashboard / subskill / adapter 五层均有接口冻结 |
| 工作流阶段 | ✅ 完整 | Intake→Release 八阶段，阶段-文件映射清晰 |
| ID 唯一性 | ⚠️ 未定义 | task_id/run_id 全局 vs branch-local 未决策 |
| Canonical 关系 | ⚠️ 模糊 | root 文件与 indexes 的派生方向未显式声明 |
| Config 语义 | ⚠️ 未分类 | declarative vs descriptive 未区分 |
| 迁移映射 | ⚠️ 不足 | flat→branch-first 缺具体字段映射表 |
| Branch context 加载 | ⚠️ 未定义 | context_manifest 未覆盖 branch 级文件 |
| 文档权威性 | ⚠️ 冗余 | 旧文档未标记 superseded |
| 测试策略 | ❌ 缺失 | 无自动化测试计划 |
| 拆分边界 | ⚠️ 未定义 | 单文件扩展边界无触发条件 |
| P0 内部顺序 | ⚠️ 可优化 | task+run 应合并，doctor 应提前 |

---

## 6. 汇总：需在 P0.1 Schema Freeze 中闭合的决策

以下问题建议在 P0.1 schema freeze 阶段一并解决，避免后续返工：

| # | 问题 | 决策内容 | 优先级 |
|---|---|---|---|
| 1 | ID 唯一性 | task_id/run_id 全局唯一（方案 A）或复合键（方案 B） | 高 |
| 2 | Canonical 关系 | `.project_os/indexes/*.tsv` 为 canonical，root 文件为 derived view | 高 |
| 3 | Config 语义 | 每项标注 declarative / descriptive | 中 |
| 4 | 迁移映射表 | 定义 flat→branch-first 的完整字段/路径映射 | 中 |
| 5 | Branch context 加载 | 明确由 runtime pointer 解析自动加载，不经过 task manifest | 中 |
| 6 | 文档权威性 | 旧文档标记 superseded | 中 |
| 7 | 测试策略 | 定义最小测试模块和核心测试用例 | 低（P0.9 之前） |
| 8 | 拆分边界 | 定义触发条件和目标结构 | 低（P1 前） |

---

## 7. 逐项评估

| 维度 | 评分 | 说明 |
|---|---|---|
| 架构设计 | ⭐⭐⭐⭐⭐ | 分层清晰，原则正确，branch-first 决策优秀 |
| Schema 契约 | ⭐⭐⭐⭐ | 字段定义完整，但 ID 唯一性和 canonical 关系需补 |
| 工作流定义 | ⭐⭐⭐⭐⭐ | Intake→Release 阶段定义清晰，阶段-文件映射完整 |
| 优先级划分 | ⭐⭐⭐⭐ | P0/P1/P2 合理，内部顺序需微调 |
| 安全设计 | ⭐⭐⭐⭐⭐ | 三层门控 + 非破坏性原则完备 |
| 扩展预留 | ⭐⭐⭐⭐⭐ | 五个扩展层都有接口冻结和实现原则 |
| 契约严密性 | ⭐⭐⭐⭐ | 核心契约严密，几处关系需显式声明 |
| 完整性 | ⭐⭐⭐⭐ | 覆盖面广，迁移映射和测试策略是缺口 |

---

## 8. 结论

方案的核心架构决策是正确的。harness-first + branch-first + run/result 分离 + promotion 安全门 + hook 边界 + 短触发路由，这套组合在科研项目管理场景下是成熟的设计。

需要在 P0.1 schema freeze 中闭合 8 项设计决策（见第 6 节），其中 2 项高优先级（ID 唯一性、canonical 关系）直接影响 schema 正确性，4 项中优先级影响契约严密性，2 项低优先级影响长期可维护性。

闭合这些问题后，方案可以进入 P0 实现阶段，按调整后的顺序执行。
