# Research Project OS — 系统架构审查

Date: 2026-06-23
Scope: 仅评估系统架构的完整性与合理性，不涉及交付节奏或范围裁剪。
Target: `docs/RESEARCH_PROJECT_OS_COMPLETE_DEVELOPMENT_PLAN.md` + branch-first schemas + references。

---

## 0. 结论

整体架构**骨架健全、分层合理、溯源链完整**，作为科研项目 harness 的核心模型是站得住的。

但从「系统是否完整」的角度看，存在 **6 个真正缺失的架构件**、**3 处需要消解的设计张力**、**4 项可优化的硬化点**。其中最关键的一条：

> 已经定义了 21 个 lifecycle event 名称，却没有承载它们的**事件日志（append-only journal）**。补上这一件，可同时解决审计、崩溃恢复（WAL）、hooks 派发、dashboard 数据源四个目前分散或悬空的需求。

下面按「实体模型 → 缺失件 → 设计张力 → 硬化点 → 已经做对的部分」展开。

---

## 1. 实体关系全景（按现有 schema 还原）

```text
project (root, 无显式 manifest)
  └── branch (branches.tsv + branch.json + 物理目录)
        └── task (tasks.tsv + task.json, 树形: parent_task_id)
              └── run (runs.tsv + RUN_MANIFEST.json)
                    └── result (results.tsv, status 机)
asset (assets.tsv, 全局)        ──► run.inputs[].asset_id
result ──► promote ──► current/{project,branches}/
result + branch ──► release (releases.tsv + MANIFEST.tsv)
decision (project/task/branch scope)
handoff (task / branch 级)
runtime pointers: current_branch / current_task / current_run
```

溯源正向链是完整的：

```text
asset → run.input → run → result → promotion(current) → release
```

这是这套架构最大的优点，下面的问题都不否定这一点。

---

## 2. 真正缺失的架构件（Tier 1）

### A1. 事件日志 / Journal —— 最关键缺口

现状：`lifecycle_events.md` 锁定了 21 个事件名，目录树里有 `.project_os/journals/`，但**没有任何 schema 定义 journal 写什么、何时写、什么格式**。

为什么这是架构级缺口，而不是锦上添花：

- **审计**：现在「什么时候发生了什么」只能从各文件的 `created_at/updated_at` 反推，无法回答「这个 result 的 status 经历过哪些变化」。
- **崩溃恢复**：第 4 节会讲多文件写入无事务保证；append-only journal 天然就是 write-ahead log，崩溃后可重放。
- **hooks 派发**：P2 的 hooks 需要一个事件源。如果 journal 先存在，hooks 只是「订阅 journal 尾部」，不需要改任何核心命令。
- **dashboard**：时间线视图、活动流都需要事件序列，而不是状态快照。

建议补一个最小契约：

```text
.project_os/journals/events.jsonl   # append-only, 永不重写
```

```jsonl
{"ts":"2026-06-23T15:30:00+08:00","event":"run.created","branch_id":"main","task_id":"...","run_id":"...","actor":"cli","detail":{}}
{"ts":"...","event":"result.promoted","result_id":"...","from":"accepted","to":"current","target":"current/project/heatmap.png"}
```

一条规则：**所有改状态的 CLI 命令，先 append journal，再改其它文件**。这一条同时把 A1 / 第 4 节一致性 / hooks 接口三件事打通。

### A2. 引用完整性与级联规则未定义

schema 定义了外键（`branch_id` / `task_id` / `run_id`）和 `replaced_by` / `superseded` 字段，但**没有定义级联语义**：

- archive 一个 branch 时，其下 active 的 task / run 怎么处理？强制级联 archive？禁止？还是只警告？
- supersede 一个 result，它关联的 run 状态是否要变？supersede 链能否跨 branch？能否成环？
- task 标记 `superseded` 后，它产出的 `current` result 是否仍然有效？

`doctor` 计划里检查「孤儿」，但**检测不等于规则**。一个完整的数据模型必须先声明「允许/禁止/级联」的状态约束，doctor 才有判据。建议新增一份 `references/integrity_rules.md`：实体删除/归档/废弃的级联矩阵 + supersede 图的约束（DAG、不跨 branch 或显式允许跨 branch）。

### A3. Asset 的反向溯源与完整性校验点缺失

正向有 `run.inputs[].asset_id`，但**没有反向索引**：给定一个 asset，找不到「哪些 run / result 依赖它」。

后果直接打到溯源承诺上：当一个 asset 被标 `deprecated` / `unavailable` / `replaced`，无法回答「哪些已 accepted 的 result 受影响、需要重跑」。这正是科研复现最关心的问题。

同时，`immutable` 和 `checksum` 是有了字段、**没有校验时机**：

- 在哪个命令点验证 immutable asset 没被改？
- run 引用 asset 时是否核对 checksum？

建议：
1. `refresh-indexes` 时构建 asset→run→result 反向引用（可落到 journal 派生视图或 `assets.tsv` 增列 / 单独 `asset_usage.tsv`）。
2. 定义 `verify-asset` / 在 `doctor` 中加 immutable asset checksum 漂移检测。

### A4. 缺少 Project 身份清单

`project_id` 只在 task_plan 的 Phase 1 提了一句，**没有进入任何 schema**。当前「项目」只靠根目录存在若干文件来识别，没有 `.project_os/project.json`。

这导致几个能力没有落点：
- `schema_version`（演化/迁移的根基）无处安放。
- 多项目 dashboard / plugin / 跨项目引用没有稳定项目标识。
- profile（research / ml / 等）、创建时间、harness 版本无处记录。

建议新增：

```json
// .project_os/project.json
{
  "project_id": "codex_skills_hub",
  "schema_version": 1,
  "profile": "research",
  "harness_version": "0.x",
  "created_at": "...",
  "default_branch": "main"
}
```

这是整套体系的「根锚点」，缺它则迁移、分发、聚合三条线都没有起点。

### A5. Promotion 状态有三处记录，未声明唯一真相源

promotion 状态同时写在：

```text
1. RUN_MANIFEST.json  -> promoted_to[]
2. results.tsv        -> promoted_to / status
3. 物理 current/      -> 实际文件存在
```

三处簿记、无仲裁规则 → 必然漂移。架构上必须显式声明：

> `current/` 物理存在 + `results.tsv` 为权威；`RUN_MANIFEST.promoted_to` 为派生/可选冗余。

并由 `doctor` 检查三者一致。否则「人类去哪找当前结果」这条核心承诺会被三套不一致的记录破坏。

### A6. 一致性模型未定义（原子性 + 并发）

一次 `register-result` 至少写 4 个文件（results.tsv、task 内 result_links.tsv、可能的 RESULTS_INDEX.md、RUN_MANIFEST）。当前：

- 无原子写入（中途崩溃 = 部分写入）。
- 无锁（agent + hook + 后台脚本可并发踩同一索引）。

这不是工程细节，而是**数据模型的一致性契约缺失**。最小补法：

- 写 TSV/JSON 一律 temp file + `os.replace`（原子）。
- `.project_os/runtime/lock` 顾问锁，索引写入期间持有。
- 配合 A1 的 journal 做 WAL，崩溃后可对账。

---

## 3. 需要消解的设计张力（Tier 2）

### T1. 全局 current 指针 vs branch-first 并行 —— 最深的张力

branch-first 的全部理由是**支持多方向并行**（main / method_a / review_r2 同时推进）。但 runtime 只有**单一全局** `current_branch / current_task / current_run`，强制串行注意力。

这是架构内部的目标冲突。两条出路，必须选一条并写进文档：

1. **承认 current = 单一焦点**：明确「同一时刻只有一个活跃上下文」，branch-first 只为隔离与归档服务，不为并行执行。简单、自洽。
2. **session 化指针**：`.project_os/runtime/sessions/` 目录现在有名无实。把 current 指针下放到 session 级，全局只记「最近 session」。支持真并行，但复杂度上升。

无论选哪个，目前「目录树里有 sessions/ 但无定义」本身就是个悬空件，必须补 schema 或删掉。

### T2. config.run_roots（列表）vs branch-first 默认路径

`config.yaml` 有 `run_roots: [runs, analysis_runs]`，而 branch-first 规定 `runs/<branch_id>/<run_id>/`。两者关系没讲清：

- 自定义 run root 是否也要 `<root>/<branch_id>/<run_id>/`？
- 多个 run root 并存时，create-run 默认选哪个？

建议明确：自定义 run root 一律套用 branch-aware 子结构，`config` 只改前缀不改层级；默认 root 在 `project.json` / `config` 里单值指定。

### T3. Task 是树（parent_task_id）但科研依赖是 DAG

task 只有 `parent_task_id`（树），但真实研究里「task B 用 task A 的 result」是 DAG 依赖。现在这种上游依赖只能塞进 `context_manifest` 指一个 RESULTS_INDEX 路径，**没有结构化的 task→result / task→task 依赖**。

后果：恢复派生工作时，agent 无法机器化地知道「这个 task 依赖哪些上游产物，上游变了我要不要重跑」。建议在 task.json 增 `depends_on: {tasks:[], results:[]}`，让 context manifest 能由依赖自动推导一部分。这也反哺 A3 的影响面分析。

---

## 4. 可优化的硬化点（Tier 3）

### O1. Result `type` 应有受控词表

results.tsv 的 `type` 是自由文本，而 asset 有 `kind` 词表。建议给 result 也定一个推荐词表（如 `figure / table / model / dataset / report / metric`），否则跨项目 dashboard / release 过滤会不一致。

### O2. workflow stage 应可按 profile/kind 收窄

`Intake→Plan→Research→Run→Evaluate→Promote→Archive→Release` 是单一全局管线。但 `figure_rebuild` 或 `review_r2` 类分支的生命周期完全不同。建议 stage 词表可由 profile 收窄，而不是所有 task 共用 8 段。

### O3. repair-plan 应升为结构化产物

doctor 检测、validate 校验，但「怎么修」目前只是文字建议。建议 `doctor`/`validate` 能输出一份**有序、可执行的 CLI 修复序列**（machine-readable）。这同时是 hooks 的天然前置（guard hook 读 repair-plan 决定是否拦截）。

### O4. 跨 branch 提升路径确认为一等公民

`promote-result --to current/project/` 实际上是把 method_a 分支的 result 提升为项目级当前——这是跨 branch 操作。架构上它能成立（result 始终保留 branch 身份），但建议在文档里把「跨 branch 提升 / 把分支成果并入 main」显式列为受支持的一等路径，避免被误解为越界。

---

## 5. 架构已经做对的部分（不要动）

- **正向溯源链完整**：asset→run→result→release，是整套设计的脊梁。
- **物理目录 + 全局索引双轨**：隔离与聚合各得其所，结论正确。
- **promotion 显式授权 + dry-run**：守门位置精准。
- **human docs / agent harness 分离**：PROJECT_STATE.md 等人类入口与 `.project_os/` 机器状态边界清晰。
- **lifecycle event 词表前置**：方向对，只差 A1 的承载体。
- **context_manifest 控制读取面**：抑制全仓库乱读，是可恢复性的关键设计。

---

## 6. 建议补充的契约文档清单

| 新增/修改 | 目的 | 对应缺口 |
|---|---|---|
| `references/event_journal_schema.md` | 定义 append-only 事件日志格式与写入时机 | A1 |
| `references/integrity_rules.md` | 级联/废弃/supersede 图约束矩阵 | A2 |
| `.project_os/project.json` + schema | 项目身份与 schema_version 锚点 | A4 |
| `assets.tsv` 反向引用 / `asset_usage` | asset→run→result 影响面 | A3 |
| `references/consistency_model.md` | 原子写入 + 顾问锁 + WAL 对账 | A6 |
| promotion「唯一真相源」声明（写入 harness_contract.md） | 消解三处簿记漂移 | A5 |
| runtime/sessions 定义 或 删除 | 消解 current 指针张力 | T1 |
| task.json `depends_on` | task DAG 依赖 | T3 |

---

## 7. 一句话总结

这套架构的**骨架和溯源链是完整且正确的**，不需要推翻。它缺的是把已经隐含承诺的东西落成契约：一个**事件日志**做时间维度的真相源，一套**完整性/级联规则**约束实体关系，一个**项目身份锚点**承载版本与分发，外加**一致性模型**和**唯一真相源**声明来消除多处簿记的漂移。补齐这几件，它就从「状态快照型 harness」升级为「带审计与可恢复保证的项目操作系统」。
