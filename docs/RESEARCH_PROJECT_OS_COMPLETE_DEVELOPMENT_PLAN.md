# Research Project OS 完整开发文档（合并版）

Date: 2026-06-23
Status: canonical merged development plan

本文档合并并取代开发时的分散路线说明，整合来源包括：

- `docs/RESEARCH_PROJECT_OS_HARNESS_IMPLEMENTATION_PLAN.md`
- `docs/RESEARCH_PROJECT_OS_BRANCH_FIRST_ARCHITECTURE.md`
- `docs/RESEARCH_PROJECT_OS_BRANCH_FIRST_SCHEMAS.md`
- `task_plan.md`
- `skills/local/research-project-os/references/*.md`
- 两份审查报告：`docs/RESEARCH_PROJECT_OS_PLAN_REVIEW.md` 与 `docs/RESEARCH_PROJECT_OS_REVIEW.md`

## Review adoption update: 2026-06-23

本轮审查意见已合并进本文档，形成新的 canonical 开发基线：

- 采纳 **task_id / run_id / result_id 项目内全局唯一**，避免全局索引冲突。
- 采纳 **`.project_os/indexes/*.tsv` 为 canonical machine registry**；根部 `RUNS_INDEX.tsv`、`RESULTS_INDEX.md`、`DATA_ASSETS.md` 是面向人的 derived view / handoff view；若 root `DATA_ASSETS.md` 已是手写文档，harness 保留它并把生成版写到 `.project_os/exports/views/DATA_ASSETS.generated.md`。
- 新增 **`.project_os/project.json`** 作为 project identity、schema version、profile 与 default branch 的根锚点。
- 新增 **`.project_os/journals/events.jsonl`** 作为 append-only lifecycle event journal；后续 hooks/dashboard/repair 都以它为事件源。
- `config.yaml` 字段区分 **declarative** 与 **descriptive**，避免用户误以为所有配置都会改变 CLI 行为。
- runtime 恢复链自动加载 branch `branch.json`、`objective.md`、`context.md`，task manifest 只承担 task/root-scoped context。
- P0 顺序调整为：schema freeze → init → branch → task+run → doctor/validate → result → short router → adapters → smoke adoption。
- P0 做最小 smoke/验证，不引入完整测试产品线；完整 integrity、asset impact、repair-plan、migration 与一致性硬化进入 P1。
- 明确后置项：full WAL/lock/crash recovery、active hooks dispatcher、rich dashboard 与 plugin packaging；sessionized runtime pointers 先作为 P2.2 基础切片实现，再继续后续增强。

本文档的目标不是再写一个大 prompt，而是把 `research-project-os` 明确为一个 **repository-local project harness** 的工程开发计划。

## Implementation update: 2026-06-24

P2.1 **Manual report-only hooks dispatcher foundation** 已经落地，但 active automatic hooks 仍保持禁用：

- 新增 `skills/local/research-project-os/scripts/_hooks.py`，并通过 `project_os.py` 暴露 `list-hooks` 与 `dispatch-hooks`。
- `list-hooks` 输出当前 hooks policy、默认 disabled 配置、可用 handler 种类与示例命令。
- `dispatch-hooks` 只读取 `.project_os/journals/events.jsonl`，生成 report-only payload；默认 kind 为 `session_summary`、`reminder`、`opt_in_maintenance`。
- 已支持 hook kinds：`session_summary`、`reminder`、`opt_in_maintenance`、`guard`；其中 `guard` 仍只是 report-only placeholder，不阻塞操作。
- `dispatch-hooks --write-report` 可把非 canonical 报告写到 `.project_os/exports/hooks/hook_report_<timestamp>.json`，并走 advisory lock。
- 短触发路由已支持 `hook状态` / `hooks状态` / `列出hooks` / `hook报告` / `hook提醒` / `派发hook`，但仍只生成计划或报告，不自动执行建议命令。
- `route` / `explain-trigger` 的 hooks 路由已透传 `--event-index`、`--event`、`--limit`、`--kind`、`--write-report`、`--output`，可规划针对特定 journal line/event 的手动报告；`--write-report` 仍只写 generated view。
- `export-dashboard` 已暴露 hooks status/config/event-source/report-count generated view；SQLite 对应 `hooks_status` 与 `hooks_allowed_kinds` 表。
- `validate` / `doctor --repair-plan` 已加入 hooks config advisory：如果配置请求 active dispatcher、声明未知 allowed kind、或 event source 缺失，会给 warning 与 `list-hooks`/恢复 journal 的非执行式建议。
- hooks 当前不得写 canonical state、不得绕过 `--apply` / `--approved` gates、不得成为 harness 必需依赖。


P1/P2 consistency hardening update: **restore-journal** 已作为缺失事件日志的最小修复入口落地：

- 新增 `project_os.py restore-journal`，默认 dry-run；`--apply --approved` 只在 `.project_os/journals/events.jsonl` 缺失且已显式批准时创建该文件并 append `journal.restored`。
- `restore-journal` 不覆盖已有 journal，不合成历史 lifecycle events，也不替代 journal/current snapshot provenance review。
- `doctor --repair-plan` 对缺失默认 event source 给出 approval-gated `restore-journal --apply --approved` 建议；对非默认 hooks event source 仍要求先审查配置。
- 短触发路由新增 `恢复事件日志`，`route --apply` 必须配合 `--approved` 才 ready。
- manual hook reminder 已识别 `journal.restored` 并建议 `validate` / `doctor --repair-plan` / `summarize-state`，仍不执行命令。

P2.2 **Sessionized runtime pointers** 的基础 CLI/runtime 切片已经落地：

- 新增 `.project_os/runtime/current_session` 与 `.project_os/runtime/sessions/<session_id>/current_branch|current_task|current_run`。
- `current_session` 为空时继续使用全局 runtime pointers，保持旧项目兼容；非空时读写对应 session 指针。
- 新增 `create-session`、`set-current-session`、`list-sessions`、`show-session`、`set-session-focus`、`pause-session`、`resume-session`、`close-session`。
- `start` / `status` / `validate` / `doctor` / `export-dashboard` 已能展示或校验 session focus。
- 短触发路由已支持 `新建会话`、`切会话`、`列出会话`、`当前会话`、`更新会话焦点`、`暂停会话`、`恢复会话`、`关闭会话`。
- session lifecycle 已支持 `active` / `paused` / `closed`；paused/closed session 不能成为 `current_session`，必须先 `resume-session`。
- 新增 `plan-session-cleanup` 作为 session archive/GC 的 dry-run/report-only 切片：默认只列出 closed session candidate，可选 paused/status/age 过滤，并可写 `.project_os/exports/session_cleanup/session_cleanup_plan_<timestamp>.json` generated report；不删除、不移动、不改写 session runtime 目录。

该切片只改变 runtime focus，不创建新的 branch/task/run 身份；session 指针仍必须指向 canonical branch/task/run manifests 与 indexes。

P2.3 **Report-only recovery planner foundation** 已作为 full WAL/crash recovery 的安全基础切片落地，但仍不做 replay/rollback/自动修复：

- 新增 `skills/local/research-project-os/scripts/_recovery.py`，并通过 `project_os.py plan-recovery` 暴露。
- `plan-recovery` 默认只输出检查报告；`--write-report` 只写 `.project_os/exports/recovery/recovery_plan_<timestamp>.json` generated view。
- 当前检查范围包括 advisory lock 候选、atomic-write `*.tmp` 残留、malformed `events.jsonl` 行、必需 harness 路径缺失、runtime pointer 漂移、manifest/index drift、root derived view drift 与 dashboard stale advisory。
- `plan-recovery` 不删除 tmp、不移除 lock、不重放 journal、不 rollback、不改写 canonical state。
- 短触发路由已支持 `恢复计划` / `恢复检查` / `崩溃恢复检查`，只生成 `plan-recovery` 命令计划。
- `doctor --repair-plan` 会以 warning-level advisory 暴露 recovery candidates，并建议 report-only `plan-recovery --write-report`；不会因为存在候选项而使 clean harness 失败。
- `export-dashboard` 已包含派生 `recovery` summary；HTML 展示 Recovery inspection，SQLite 导出 `recovery_status` 与 `recovery_summary` 表。
- 完整 WAL replay、crash rollback、自动 lock/tmp cleanup 仍后置，必须另行设计 explicit review/approval/validation gate。

P1.5 **Decision/handoff state summary consistency update** 已补齐 `summarize-state` 的 runtime/current-result 摘要：

- `summarize-state` 现在使用同一套 session-aware runtime focus 解析：当 `.project_os/runtime/current_session` 非空时，摘要中的 current branch/task/run 来自对应 session focus；为空时继续使用 global runtime pointers。
- 输出 payload 新增 `runtime_focus`，用于明确当前是否处在 named session、session 指向哪个 branch/task/run，以及全局 fallback 指针是什么。
- 输出 payload 新增 `current_results` 派生摘要，复用 `show-current --audit` / dashboard 使用的 current-result helpers，包含 all/project/current-branch counts、project/branch current result rows、`audit_ok` 与 promotion-audit warning counts。
- 该补齐只让 state summary 更完整；current-result 摘要仍从 `.project_os/indexes/results.tsv` 与 `current/` targets 派生，不 promote result、不 repair `current/`、不改写 `results.tsv` 或 result manifests。

P0.5 **Status read-only summary hardening** 已补齐 status 的运行/结果前沿摘要：

- `status` 现在输出完整 `runtime_focus`，与 sessionized pointer 行为一致；顶层 `current_branch` / `current_task` / `current_run` 保持兼容。
- `status.runs_summary` 从 `.project_os/indexes/runs.tsv` 派生 active/open run 数量、当前 run row、当前 branch/task 的 active run 数量，以及 last run summary。
- `status.results_summary` 从 `.project_os/indexes/results.tsv` 与 `current/` targets 派生 candidate/accepted/current counts、latest candidate rows、project/current-branch current result rows、`audit_ok` 与 promotion-audit warning counts。
- 该命令仍是纯只读状态检查：不 refresh indexes、不 append event、不 promote result、不 repair `current/`、不改写 `results.tsv` 或 run/result manifest。

P0/P1 **Direct CLI approval-gate hardening** 已补齐 promotion/release/restore-journal 直接命令与 router 的一致性：

- `promote-result --apply` 现在必须显式携带 `--approved`；不带 `--approved` 时直接 CLI 会拒绝写入 `current/` 和 `results.tsv`。
- `build-release --apply` 现在必须显式携带 `--approved`；不带 `--approved` 时直接 CLI 会拒绝复制 release artifact 和写 `releases.tsv`。
- `restore-journal --apply` 现在必须显式携带 `--approved`；不带 `--approved` 时直接 CLI 会拒绝创建/写入 `.project_os/journals/events.jsonl`。
- 短触发 router 在 promotion/release/restore-journal `route --apply --approved` 时会把 `--approved` 传递给 planned command；`route --apply` 但无 `--approved` 仍保持 `ready=false`。
- `doctor --repair-plan` 与 `plan-recovery` 给出的缺失 journal 建议命令现在也包含 `--apply --approved`，复制执行时不再绕过直接 CLI gate。
- dry-run promotion/release/restore-journal 仍不需要 `--approved`，便于先审查目标路径、release manifest plan、缺失 journal 状态和安全门。

P1 **Large asset externalization / 大文件统一外置** 正式纳入核心收敛范围：

- 目标不是把大文件放入 `.project_os/`，而是让项目目录保持轻量，`.project_os` 只登记 asset metadata、location、checksum、usage 与恢复映射。
- 默认采用 dry-run/report-first：先扫描大文件、断裂 symlink、run manifest 输入、脚本中的旧路径引用，再生成外置计划；不直接移动、不删除、不覆盖、不创建 hard link。
- 支持两个用户指定目标盘：
  - `/media/teng/HP_P900`：当前更适合作为 primary large-asset store。
  - `/media/teng/备份盘2`：当前更适合作为 backup / mirror / critical-only store，是否复制大文件由策略决定。
- 新增多位置模型：`assets.tsv` 保留 asset 的主路径/逻辑入口；`.project_os/indexes/asset_locations.tsv` 记录同一 asset 在 primary/backup/mirror/archive 等多个物理位置。
- 后续 CLI 规划为：`plan-externalize-assets`、`externalize-asset`、`adopt-external-asset`、`verify-external-assets`、`list-asset-locations`。其中真正复制/移动或 registry-only adoption apply 必须 `--apply --approved`，并先 checksum 验证；hard link 禁止作为功能路径；symlink 只能作为本地非 canonical 便捷项且默认不生成。
- 对真实试点 `/home/teng/BGCdetection/target_BGC_mining/typeII_pks`，`/media/teng/HP_P900/bgcdetecttion/typeiipks/target_all_faa.renamed_for_Chen2022_HMMER.faa` 应登记为 external asset，而不是复制回项目目录；旧 run 输入断链应进入 repair/adoption plan。

---

## 1. 总结论

`research-project-os` 应实现为：

```text
项目内 harness          .project_os/
人类入口文档            PROJECT_STATE.md, DATA_ASSETS.md, RUNS_INDEX.tsv, RESULTS_INDEX.md, DECISIONS.md
确定性执行后端          skills/local/research-project-os/scripts/project_os.py
Agent 入口              research-project-os skill + project-skeleton alias
平台适配                Codex / Claude thin adapters first
后置扩展                hooks, dashboards, subskills, plugin packaging
```

核心判断：

> **harness 是产品主体，skill 是入口，CLI 是确定性执行层，adapter 是平台接入层，hooks/plugin/dashboard 是后续扩展层。**

当前开发不应只停留在 skill 文本，也不应一开始做 plugin。第一目标是把 `.project_os/`、branch/task/run/result/release 的状态机和文件契约跑通。

---

## 2. 范围边界

### 2.1 当前必须完成的核心能力

核心 harness 需要覆盖：

1. project bootstrap / adoption
2. branch / workstream 管理
3. task 管理与 context manifest
4. run lifecycle 与 provenance
5. result lifecycle 与 promotion
6. data asset registry 与大文件统一外置
7. decision / handoff 管理
8. release packaging
9. indexes / doctor / validate
10. Codex + Claude thin adapters
11. 自然语言短入口与 skill 路由
12. hooks/plugin/dashboard/subskill 的接口预留

### 2.2 当前不做但必须预留的能力

以下能力不是舍弃，而是后置：

| 能力 | 当前状态 | 预留方式 |
|---|---|---|
| plugin packaging | 不实现 | 保持脚本/模板自包含，避免绝对路径，保留 manifest 设计位 |
| hooks | 不实现 active hook | 固定 lifecycle event 名称，CLI 支持 dry-run/json/idempotent |
| dashboard/export | 已有基础 generated view；rich dashboard 后置 | JSON/HTML/SQLite 只从 canonical state 派生，不能反写为 source of truth |
| subskills | 不拆分 | references 与 CLI command group 保持清晰，后续可拆 |
| OpenCode/Cursor/Gemini adapter | 不做 | adapter policy 保持平台无关 |

### 2.3 明确非目标

当前阶段不要做：

- 不做主动 hook 执行逻辑；但必须落地默认 disabled 的 hooks contract、`config.yaml` 预留块与 `.project_os/spec/hooks.md`。
- 不做 Codex plugin 打包。
- 不做可编辑 dashboard/state UI；只允许 generated view。
- 不拆出大量 subskills。
- 不做破坏性 cleanup。
- 不替代任何项目已有的科学/分析计划。
- 不把 chat memory 当作项目状态来源。
- 不把 external mirrored skills 当成本地原创内容。

---

## 3. 核心概念区别

| 概念 | 作用 | 是否核心状态来源 | 是否当前实现重点 |
|---|---|---:|---:|
| harness | 项目内状态、流程、索引、provenance | 是 | 是 |
| skill | 让 agent 知道何时、如何操作 harness | 否 | 是，但要保持薄 |
| CLI/backend | 确定性创建/修改/校验项目文件 | 是 | 是 |
| adapter | 让 Codex/Claude 接入同一套 harness | 否 | 只做 Codex/Claude |
| hook | 特定事件自动执行辅助动作 | 否 | 暂不实现，仅预留 |
| plugin | 分发/安装/打包 | 否 | 后置 |
| dashboard | 生成展示视图 | 否 | 后置 |

简化比喻：

```text
CLI/backend = 发动机
.project_os = 车架和仪表盘数据
skill = 驾驶手册和入口
adapter = 不同平台的插头
hook = 自动开灯/提醒的小机关
plugin = 包装盒和安装包
```

---

## 4. 设计原则

1. **Harness first, skills second**
   项目事实存在 `.project_os/` 和根部索引文件中，skill 只负责路由与行为约束。

2. **Branch-first physical workspace**
   branch/workstream 不只是字段，而是物理目录：`.project_os/branches/<branch_id>/`。

3. **Global indexes remain mandatory**
   物理 branch 提供隔离，全局 indexes 提供查询、聚合和未来 dashboard/hooks/plugin 的稳定入口。

4. **Context manifest over whole-repo reading**
   agent 恢复任务时只读当前 task 的 `context_manifest.jsonl` 列出的文件，而不是全仓库乱读。

5. **Run is provenance, result is discoverable output**
   runs 用于记录产生过程，人类查找成果应通过 `RESULTS_INDEX.md`、`current/`、`release/`。

6. **Promotion requires explicit approval**
   任何进入 `current/` 或 `release/` 的动作都需要明确授权，不能自动发生。

7. **Hooks cannot own core logic**
   不运行 hooks 时，harness 也必须完整可用。

8. **Adapters are disposable, `.project_os/` is canonical**
   Codex/Claude 文件只指向 `.project_os/`，不能复制出另一套状态。

9. **Progressive disclosure**
   `SKILL.md` 保持短，细节放 references，确定性操作放 scripts。

10. **No second scientific plan**
    对已有科研项目，harness 记录计划、任务、运行和结果，不发明新的科学路线。

---

## 5. 总体架构

### 5.1 分层架构

```text
L0 Contract/schema layer
   references/*.md
   docs/*SCHEMAS.md
   .project_os/spec/*.md

L1 Core harness engine
   scripts/project_os.py
   deterministic CLI operations

L2 Project state files
   .project_os/
   PROJECT_STATE.md
   DATA_ASSETS.md
   RUNS_INDEX.tsv
   RESULTS_INDEX.md
   DECISIONS.md
   current/
   runs/
   release/

L3 Agent entry layer
   research-project-os/SKILL.md
   project-skeleton/SKILL.md
   natural-language triggers
   short commands/aliases later

L4 Distribution/automation layer
   Codex/Claude adapters first
   hooks later
   dashboards later
   plugins later
```

### 5.2 数据流

```text
用户自然语言 / 短命令
        ↓
research-project-os / project-skeleton skill
        ↓
project_os.py CLI
        ↓
.project_os/branches/<branch_id>/tasks/<task_id>/
runs/<branch_id>/<run_id>/
.project_os/indexes/*.tsv
        ↓
RESULTS_INDEX.md / current/ / release/
```

---

## 6. 目标项目文件结构

采用 branch-first 物理结构，并新增 project identity 与 event journal：

```text
<project>/
├── PROJECT_STATE.md                    # thin human handoff / resume entry
├── DATA_ASSETS.md                      # human asset view; protected when hand-authored
├── RESULTS_INDEX.md                    # derived human result entry point
├── RUNS_INDEX.tsv                      # derived human run view
├── DECISIONS.md                        # human decision log / handoff summary
├── AGENTS.md                           # optional Codex adapter
├── CLAUDE.md                           # optional Claude adapter
├── current/
│   ├── project/
│   └── branches/
│       └── <branch_id>/
├── release/
│   └── <release_id>/
│       ├── MANIFEST.tsv
│       ├── CHECKSUMS.tsv
│       ├── README.md
│       └── files...
├── runs/
│   └── <branch_id>/
│       └── <run_id>/
│           ├── RUN_MANIFEST.json
│           └── outputs...
└── .project_os/
    ├── project.json                    # project identity / schema anchor
    ├── workflow.md
    ├── config.yaml
    ├── runtime/
    │   ├── current_session             # optional active session focus; empty => global pointers
    │   ├── current_branch              # global active focus when current_session is empty
    │   ├── current_task
    │   ├── current_run
    │   └── sessions/
    │       └── <session_id>/
    │           ├── session.json
    │           ├── current_branch
    │           ├── current_task
    │           └── current_run
    ├── spec/
    │   ├── project_rules.md
    │   ├── branch_model.md
    │   ├── task_tree.md
    │   ├── context_manifest.md
    │   ├── run_provenance.md
    │   ├── result_curation.md
    │   ├── data_assets.md
    │   ├── event_journal.md
    │   ├── hooks.md
    │   ├── integrity_rules.md
    │   ├── user_profile.md
    │   └── release_packaging.md
    ├── branches/
    │   ├── main/
    │   │   ├── branch.json
    │   │   ├── objective.md
    │   │   ├── context.md
    │   │   ├── handoff.md
    │   │   ├── decisions.md
    │   │   ├── research/
    │   │   ├── notes/
    │   │   └── tasks/
    │   │       └── <task_id>/
    │   │           ├── task.json
    │   │           ├── objective.md
    │   │           ├── context.md
    │   │           ├── context_manifest.jsonl
    │   │           ├── handoff.md
    │   │           ├── decisions.md
    │   │           ├── run_links.tsv
    │   │           └── result_links.tsv
    │   └── <branch_id>/
    │       └── ... same structure ...
    ├── indexes/                         # canonical machine registries
    │   ├── branches.tsv
    │   ├── tasks.tsv
    │   ├── runs.tsv
    │   ├── results.tsv
    │   ├── assets.tsv
    │   ├── asset_locations.tsv          # P1 multi-location view for external large assets
    │   ├── asset_usage.tsv              # P1 derived impact view
    │   └── releases.tsv
    ├── journals/
    │   └── events.jsonl                 # append-only lifecycle event journal
    └── exports/
        ├── task_graph.html              # generated later
        ├── run_graph.html               # generated later
        └── result_dashboard.html        # generated later
```

关键约束：

- 新项目必须采用此结构；旧 flat layout 通过 dry-run migration plan 迁移。
- `runtime/sessions/` 已作为 P2.2 基础切片实现；session 只 shadow runtime focus，不创建第二套 branch/task/run canonical state。
- `.project_os/indexes/*.tsv` 是 machine-readable canonical registry；根部 Markdown/TSV 是面向人的派生入口。

---

## 7. Runtime pointer 解析规则

Runtime focus 分为两层：

1. **Global focus**：默认兼容模式，由全局 runtime pointer 表示。
2. **Session focus**：当 `.project_os/runtime/current_session` 非空时，读写该 session 目录下的 pointer。

全局 pointer：

```text
.project_os/runtime/current_branch
.project_os/runtime/current_task
.project_os/runtime/current_run
```

session pointer：

```text
.project_os/runtime/current_session
.project_os/runtime/sessions/<session_id>/session.json
.project_os/runtime/sessions/<session_id>/current_branch
.project_os/runtime/sessions/<session_id>/current_task
.project_os/runtime/sessions/<session_id>/current_run
```

解析规则：

```text
if runtime/current_session is empty:
  active_focus = global current_branch/current_task/current_run
else:
  active_focus = runtime/sessions/<session_id>/current_branch/current_task/current_run
```

恢复顺序：

```text
active current_branch
  -> .project_os/branches/<branch_id>/branch.json
  -> .project_os/branches/<branch_id>/objective.md
  -> .project_os/branches/<branch_id>/context.md
  -> active current_task
  -> .project_os/branches/<branch_id>/tasks/<task_id>/task.json
  -> .project_os/branches/<branch_id>/tasks/<task_id>/context_manifest.jsonl
  -> active current_run
  -> runs/<branch_id>/<run_id>/RUN_MANIFEST.json
```

说明：

- Branch context 是运行环境的一部分，由 pointer 解析链自动加载。
- `context_manifest.jsonl` 仍保持 task-scoped，用于列出 task/root 级必要上下文，不需要重复列 branch `objective.md` 与 `context.md`。
- `current_session` 为空时，历史命令和旧项目继续使用 global focus。
- `current_session` 指向 session 时，`create-task` / `create-run` / `set-current-*` 等 pointer 读写会落在该 session 指针中。
- session 不创建 branch/task/run/result 新身份；它只保存“这一次工作上下文看向哪里”。
- session directory 必须包含 `session.json` 与三个 pointer 文件；`validate` / `doctor` 会检查它们是否指向存在的 canonical 对象。

Session CLI：

```bash
python scripts/project_os.py create-session --root <project> --session-id paper_a --branch-id main --set-current
python scripts/project_os.py set-current-session --root <project> --session-id paper_a
python scripts/project_os.py set-current-session --root <project> --clear
python scripts/project_os.py list-sessions --root <project>
python scripts/project_os.py show-session --root <project>
python scripts/project_os.py set-session-focus --root <project> --session-id paper_a --branch-id main --task-id <task_id>
python scripts/project_os.py close-session --root <project> --session-id paper_a
```

`doctor` 必须检查：

- `current_session` 为空或指向存在的 session。
- session id 格式合法。
- session pointer 文件存在。
- `current_branch` 是否存在对应 branch row、branch workspace、`branch.json`。
- branch `objective.md` / `context.md` 是否存在或可解释缺失。
- `current_task` 是否属于 `current_branch`。
- `current_run` 是否属于当前 task/branch。
- pointer 指向的文件是否真实存在。

---

## 8. Schema 合约摘要

本文档是开发路线与关键决策的 canonical source。`docs/RESEARCH_PROJECT_OS_BRANCH_FIRST_SCHEMAS.md` 与 `skills/local/research-project-os/references/*.md` 保留为详细 schema/reference，但若冲突，以本文档的采纳决策为准，并在 P0.1 同步修正。

### 8.0 全局 schema 决策

#### ID uniqueness

- `branch_id`：项目内唯一。
- `task_id`：项目内全局唯一，不采用 `(branch_id, task_id)` 复合键作为 canonical key。
- `run_id`：项目内全局唯一。
- `result_id`：项目内全局唯一。
- `asset_id` / `release_id`：项目内全局唯一。

原因：全局索引、短触发词、人工恢复和跨 branch 查询都更简单。Branch 归属仍必须写入每一行，不能只从 ID 推断。

#### Canonical vs derived

```text
Canonical machine registries: .project_os/indexes/*.tsv
Canonical project identity:    .project_os/project.json
Canonical event stream:        .project_os/journals/events.jsonl
Human derived views:           RUNS_INDEX.tsv, RESULTS_INDEX.md, DATA_ASSETS.md or .project_os/exports/views/DATA_ASSETS.generated.md
Human handoff summary:         PROJECT_STATE.md
```

规则：

- `refresh-indexes` 单向刷新 root human views，不从 root views 反向 merge 回 canonical TSV。
- `doctor` 检测 canonical registry 与 derived view 不一致时先报告，不自动修复。
- `PROJECT_STATE.md` 是薄 handoff，不是 task/run/result 的 machine source。

#### Promotion source of truth

Promotion 的唯一真相源由两部分组成：

```text
.project_os/indexes/results.tsv   # status / promoted_to / accepted_at / replaced_by
current/                          # 实际可发现的当前文件或 manifest pointer
```

`RUN_MANIFEST.json.promoted_to` 是可选冗余/缓存，便于从 run 反查结果，但不作为仲裁源。`doctor` 应检查三者漂移。

#### Result type recommended vocabulary

`results.tsv.type` 推荐使用受控词表：

```text
figure, table, dataset, model, report, metric, text, artifact, package, other
```

#### Config semantics

`config.yaml` 字段必须标注 declarative/descriptive：

| 字段 | 类型 | 说明 |
|---|---|---|
| `schema_version` | descriptive | 记录 schema 版本；迁移命令读取，但普通命令不因用户手改而改变行为。 |
| `run_roots` | declarative | `create-run` 默认使用第一个 root，并一律套用 `<run_root>/<branch_id>/<run_id>/`。 |
| `default_run_root` | declarative | 若实现，优先于 `run_roots[0]`。 |
| `adapters.*` | descriptive | 记录安装状态；`install-adapters` 以命令参数为准。 |
| `promotion_requires_user_approval` | declarative, guarded | 默认 true；即便未来允许 false，P0 仍强制 dry-run/apply 门控。 |
| `runtime.current_session` | descriptive/runtime | 说明 session focus 文件位置；实际 active session 以 `.project_os/runtime/current_session` 为准。 |
| `runtime.session_pointer_names` | descriptive/runtime | 声明 session pointer 文件名：`current_branch`、`current_task`、`current_run`。 |
| `hooks.enabled` | declarative, deferred | P0 仅预留，不执行 active hooks。 |
| `hooks.mode` | descriptive/deferred | 当前固定为 `disabled`；未来 dispatcher 才读取。 |
| `hooks.dispatcher` | descriptive/deferred | 当前为 `none`；不得被 P0/P1 当作执行入口。 |
| `hooks.event_source` | descriptive contract | 指向 `.project_os/journals/events.jsonl`，供未来 hook/dashboard/repair 观察。 |
| `hooks.allowed_kinds` | design contract | 声明未来可添加的 hook 类型：session summary、reminder、opt-in maintenance、guard。 |
| `hooks.policy.*` | design contract | 记录 hooks 必须调用 CLI、不能直写 canonical state、默认非阻塞、guard 必须 opt-in。 |

### 8.1 `.project_os/project.json`

```json
{
  "project_id": "codex_skills_hub",
  "schema_version": 1,
  "profile": "research",
  "harness_version": "0.x",
  "created_at": "2026-06-23T00:00:00+08:00",
  "default_branch": "main"
}
```

`project_id` 可由项目目录名 slug 化生成，用户可在 dry-run 阶段调整。

### 8.2 `.project_os/journals/events.jsonl`

Append-only，一行一个事件，不重写历史：

```jsonl
{"ts":"2026-06-23T15:30:00+08:00","event":"run.created","branch_id":"main","task_id":"20260623_nmr_main_qc","run_id":"20260623_153000__nmr_main_qc","actor":"cli","detail":{}}
{"ts":"2026-06-23T15:45:00+08:00","event":"result.promoted","branch_id":"main","task_id":"20260623_nmr_main_qc","run_id":"20260623_153000__nmr_main_qc","result_id":"20260623_result_qc_table","actor":"cli","detail":{"target":"current/branches/main/qc_table.tsv"}}
```

最小字段：

| 字段 | 说明 |
|---|---|
| `ts` | ISO timestamp with timezone |
| `event` | lifecycle event name |
| `actor` | `cli`, `codex`, `claude`, `hook`, or user-defined |
| `branch_id` | 可为空，但 branch/task/run/result 事件必须写 |
| `task_id` | 可为空 |
| `run_id` | 可为空 |
| `result_id` | 可为空 |
| `detail` | 小型 JSON object，不放大文件或长日志 |

P0 规则：所有 P0 实现的状态修改命令必须 append 事件；完整 WAL/lock/crash recovery 进入 P1/P2 硬化。若 journal 文件本身缺失，使用 `restore-journal` dry-run/review 后再 `--apply --approved`，该命令只创建缺失文件并记录 `journal.restored`，不重建历史事件。

### 8.3 `branches.tsv`

```text
branch_id	status	parent_branch_id	title	branch_path	task_root	run_root	current_root	git_branch	created_at	closed_at	notes
```

状态：

```text
active, paused, completed, archived, abandoned
```

### 8.4 `branch.json`

```json
{
  "branch_id": "main",
  "title": "Main analysis line",
  "status": "active",
  "parent_branch_id": "",
  "git_branch": null,
  "branch_path": ".project_os/branches/main",
  "task_root": ".project_os/branches/main/tasks",
  "run_root": "runs/main",
  "current_root": "current/branches/main",
  "created_at": "2026-06-23T00:00:00+08:00",
  "closed_at": null,
  "objective_file": "objective.md",
  "context_file": "context.md",
  "handoff_file": "handoff.md",
  "notes": ""
}
```

### 8.5 `tasks.tsv`

```text
task_id	branch_id	status	kind	stage	title	task_path	parent_task_id	created_at	updated_at	owner	priority	notes
```

状态：

```text
active, paused, blocked, completed, archived, superseded
```

阶段：

```text
Intake, Plan, Research, Run, Evaluate, Promote, Archive, Release
```

### 8.6 `task.json`

```json
{
  "task_id": "20260623_nmr_main_qc",
  "title": "NMR main-line QC pass",
  "status": "active",
  "kind": "analysis",
  "stage": "Run",
  "branch_id": "main",
  "parent_task_id": null,
  "depends_on": {"tasks": [], "results": []},
  "task_path": ".project_os/branches/main/tasks/20260623_nmr_main_qc",
  "created_at": "2026-06-23T15:30:00+08:00",
  "updated_at": "2026-06-23T15:30:00+08:00",
  "owner": "",
  "priority": "normal",
  "objective_file": "objective.md",
  "context_file": "context.md",
  "context_manifest": "context_manifest.jsonl",
  "handoff_file": "handoff.md",
  "notes": ""
}
```

`depends_on` 在 P0 可为空，P1 开始用于 task DAG / upstream impact 分析。

### 8.7 `runs.tsv`

```text
run_id	branch_id	task_id	status	result_status	run_path	created_at	closed_at	code_ref	notes
```

run 状态：

```text
active, completed, failed, pending_review, archived, superseded
```

result status：

```text
draft, candidate, accepted, current, superseded, legacy, release
```

### 8.8 `RUN_MANIFEST.json`

```json
{
  "run_id": "20260623_153000__nmr_main_qc",
  "branch_id": "main",
  "task_id": "20260623_nmr_main_qc",
  "status": "active",
  "created_at": "2026-06-23T15:30:00+08:00",
  "closed_at": null,
  "code_ref": {
    "git_commit": null,
    "dirty": null,
    "git_available": null
  },
  "environment": {
    "python": null,
    "conda_env": null,
    "packages": {}
  },
  "inputs": [],
  "parameters": {},
  "commands": [],
  "outputs": [],
  "metrics": {},
  "result_status": "draft",
  "promoted_to": [],
  "notes": ""
}
```

### 8.9 `results.tsv`

```text
result_id	branch_id	task_id	run_id	status	type	path	title	created_at	accepted_at	promoted_to	replaced_by	notes
```

### 8.10 `assets.tsv`

```text
asset_id	kind	path	version	source_url	source_note	immutable	status	registered_at	checksum	notes
```

说明：

- `path` 是 asset 的主路径或逻辑入口；可以是 project-relative，也可以是 external absolute path。
- 当同一 asset 有多个物理副本/镜像时，`assets.tsv.path` 保持 primary/read path；多位置细节写入 `asset_locations.tsv`。
- 大文件不复制进 `.project_os/`；`.project_os` 只登记 metadata、checksum、location 与 usage。
- 不使用 hard link 管理资产，因为 harness 必须可跨机器、跨挂载点、跨平台迁移；canonical 引用必须是 `asset_id` + location registry，而不是 inode 级链接。
- symlink 也不能作为 canonical source；若某个本地项目为了兼容旧脚本保留 symlink，它只能是非 canonical convenience，并且必须能通过 `asset_locations.tsv` 重新解析。

### 8.10a `asset_locations.tsv`（P1 multi-location asset view）

```text
asset_id	location_id	role	path	storage_root	status	size_bytes	checksum	registered_at	last_checked_at	notes
```

推荐 role：

```text
primary, backup, mirror, archive, cache, unavailable
```

规则：

- `asset_id` 必须存在于 `assets.tsv`。
- `location_id` 项目内唯一，建议使用 `hp_p900`、`backup2` 等稳定短名加路径 slug。
- `role=primary` 代表默认读取位置；`backup/mirror/archive` 代表备份或替代位置。
- `status` 至少区分 `available`、`missing`、`stale_checksum`、`unchecked`。
- `checksum` 可为空，但如果存在必须与 `assets.tsv.checksum` 一致；不一致由 `doctor/verify-external-assets` 报 warning/error。
- 目标盘可在 `config.yaml.external_assets.roots` 中声明，当前已知用户目标盘为：
  - `/media/teng/HP_P900`
  - `/media/teng/备份盘2`

### 8.11 `asset_usage.tsv`（P1 derived impact view）

```text
asset_id	branch_id	task_id	run_id	result_id	usage_kind	registered_at	notes
```

### 8.12 `releases.tsv`

```text
release_id	status	path	created_at	source_branch_ids	source_result_ids	notes
```

### 8.13 Flat → branch-first migration mapping

P0.1 必须冻结映射；实现命令可在 P1.7 完成：

| 旧路径/字段 | 新路径/字段 | 动作 |
|---|---|---|
| `.project_os/tasks/<task_id>/` | `.project_os/branches/main/tasks/<task_id>/` | dry-run 后移动或复制，默认 main |
| `runs/<run_id>/` | `runs/main/<run_id>/` | dry-run 后移动或复制，默认 main |
| `RUN_MANIFEST.json` 无 `branch_id` | `branch_id: main` | 字段补全 |
| old `tasks.tsv` | new `tasks.tsv` with `branch_id` | header 升级，补 main |
| old `runs.tsv` | new `runs.tsv` with `branch_id` | header 升级，补 main |
| old `results.tsv` | new `results.tsv` with `branch_id`, `promoted_to` | header 升级，补 main / 空 promoted_to |
| `run_links.tsv` 旧路径 | branch-aware run path | 路径更新 |
| root `RUNS_INDEX.tsv` | derived from `.project_os/indexes/runs.tsv` | 不反向 merge |

---

## 9. 核心工作流

科学/分析项目的 harness workflow：

```text
Intake -> Plan -> Research -> Run -> Evaluate -> Promote -> Archive -> Release
```

| 阶段 | 目标 | 主要文件 |
|---|---|---|
| Intake | 检测项目、读取状态、建立/恢复 harness | `PROJECT_STATE.md`, `.project_os/config.yaml` |
| Plan | 选择 branch/task，不替代已有权威计划 | `branch.json`, `task.json`, `objective.md` |
| Research | 收集文献/方法/工具上下文 | `research/`, `context_manifest.jsonl` |
| Run | 建立正式运行与 provenance | `RUN_MANIFEST.json`, `runs.tsv` |
| Evaluate | 评估输出、记录指标和局限 | run reports, `result_links.tsv` |
| Promote | 用户确认后设为 accepted/current | `RESULTS_INDEX.md`, `current/` |
| Archive | 标记 superseded/legacy，不删除历史 | `results.tsv`, `DECISIONS.md` |
| Release | 打包 accepted/current 结果 | `release/<release_id>/` |

---

## 10. CLI 总设计

统一入口：

```bash
python scripts/project_os.py <command> --root <project> [options]
```

原则：

- 写操作尽量支持 dry-run 或明确 `--apply`。
- 危险动作必须显式授权。
- read/list/show/status 尽量支持 `--json`。
- command 负责真实状态修改，skill 不手写状态。
- hook 未来只能调用 CLI，不复制业务逻辑。

### 10.1 命令组

#### Project

```text
new-project
init
start
status
doctor
validate
refresh-indexes
install-adapters
```

#### Branch

```text
create-branch
set-current-branch
list-branches
show-branch
archive-branch
```

#### Task

```text
create-task
set-current-task
list-tasks
show-task
update-task
update-task-stage
close-task
add-dependency
remove-dependency
add-context
remove-context
update-handoff
```

#### Run

```text
create-run
set-current-run
show-run
list-runs
update-run
add-run-input
add-run-command
add-run-output
add-run-metric
close-run
```

#### Result

```text
register-result
list-results
show-result
accept-result
promote-result
supersede-result
show-current
```

#### Asset

```text
register-asset
list-assets
show-asset
update-asset
checksum-asset
refresh-assets
plan-externalize-assets
externalize-asset
verify-external-assets
list-asset-locations
```

#### Decision / Release

```text
record-decision
list-decisions
summarize-state
build-release
list-releases
show-release
validate-release
```

---

## 11. P0：第一优先开发范围

P0 的定义：

> **让 branch-first harness 可以在真实项目中完成从 bootstrap/resume → branch → task/run → doctor/validate → result → current 的最小闭环，同时具备短触发路由、Codex/Claude 入口和后续 hooks/plugin 的接口预留。**

P0 不是简单 skill，也不是全部最终功能。Branch/workstream、task/run 控制、canonical indexes、event journal、doctor/validate、result promotion、短触发路由都属于 P0。

### P0.0 文档权威性与审查采纳

目标：消除多份 plan 冲突。

步骤：

1. 本文档作为 canonical merged plan。
2. 旧 plan / branch architecture / branch schema / `task_plan.md` 标记 superseded，保留为历史或详细 reference。
3. 两份审查报告的采纳项写入本文档。
4. `PROJECT_STATE.md`、`progress.md`、`findings.md` 指向本文档。

验收：未来 agent 先读本文档，不再在旧路线图之间摇摆。

### P0.1 Schema freeze

目标：冻结 `project_os.py` 与 branch-first schema 的最低共同契约。

步骤：

1. 更新 `INDEX_HEADERS`：
   - `branches.tsv` 使用完整 branch-first header。
   - `tasks.tsv` 把 `branch_id` 放在 canonical 位置。
   - `runs.tsv` 加 `branch_id` 和 `code_ref`。
   - `results.tsv` 加 `branch_id`, `promoted_to`。
   - 新增 `releases.tsv`。
2. 增加 `.project_os/project.json` schema 与默认生成规则。
3. 增加 `.project_os/journals/events.jsonl` 最小 schema 与 append helper。
4. 固定 ID 策略：`task_id` / `run_id` / `result_id` 项目内全局唯一。
5. 固定 canonical/derived 关系：`.project_os/indexes/*.tsv` canonical，root views 单向生成。
6. 固定 config.yaml declarative/descriptive 语义。
7. 固定 result type 推荐词表。
8. 固定 promotion truth source：`results.tsv` + `current/`，`RUN_MANIFEST.promoted_to` 为冗余。
9. 固定 status 枚举与 required fields。
10. 固定路径 helper：
    - `branch_dir(root, branch_id)`
    - `branch_task_dir(root, branch_id, task_id)`
    - `run_dir(root, branch_id, run_id)`
    - `branch_current_dir(root, branch_id)`
11. 冻结 flat → branch-first migration mapping，但不在 P0 强制实现迁移命令。

验收：

- 代码常量与本文档 Section 8 一致。
- 没有新命令继续写旧 `.project_os/tasks/<task_id>/`。
- `project.json` 与 `events.jsonl` 至少能在 init/new-project 后存在。

### P0.2 Init / new-project branch-first 化

目标：初始化项目时创建完整 branch-first 骨架。

步骤：

1. `init` / `new-project` 创建：
   - `.project_os/project.json`
   - `.project_os/journals/events.jsonl`
   - `.project_os/branches/main/`
   - `.project_os/branches/main/tasks/`
   - `runs/main/`
   - `current/branches/main/`
   - `current/project/`
2. 创建 `.project_os/branches/main/branch.json`。
3. 创建 branch 文件：`objective.md`, `context.md`, `handoff.md`, `decisions.md`, `research/`, `notes/`。
4. 初始化 `.project_os/runtime/current_branch` 为 `main`。
5. 初始化 `.project_os/indexes/branches.tsv` 并写入 `main` row。
6. 初始化 `.project_os/indexes/releases.tsv`。
7. 写入 `project.initialized` / `project.adopted` event。
8. `.project_os/spec/` 增加或更新 `branch_model.md` 与 event journal 说明。
9. 更新 `.project_os/workflow.md` 中 task/run 路径说明。

验收：

- 空项目执行 `new-project --apply` 后能直接 `start`。
- 默认 branch `main` 同时存在 branch row、物理目录、`branch.json` 和 runtime pointer。

### P0.3 Branch commands

目标：branch/workstream 成为一等对象。

命令：

```text
create-branch
set-current-branch
list-branches
show-branch
archive-branch
```

步骤：

1. `create-branch` 支持 `--branch-id`, `--title`, `--parent-branch-id`, `--git-branch`, `--notes`, `--set-current`。
2. 创建 branch workspace，并 upsert `branches.tsv`。
3. `set-current-branch` 检查 branch 存在且未 archived/abandoned；若 current_task 不属于新 branch，提示而不静默修改。
4. `list-branches` 支持 `--status`, `--json`。
5. `show-branch` 输出 branch metadata、task count、run count、current path。
6. `archive-branch` 只标记状态和 `closed_at`，不删除历史。
7. 每个状态修改写 `events.jsonl`。

验收：多个 branch 可并存；archive 不破坏历史；current branch 解析稳定。

### P0.4 Task + Run branch-aware 最小闭环

目标：task 和 run 一起切到 branch-aware helper，避免中间态 task 已 branch-first 而 run 仍 flat。

Task 步骤：

1. 修改 `task_dir()` / `task_json_path()`，支持 branch-aware lookup。
2. `create-task` 默认使用 `current_branch`，也支持 `--branch-id`。
3. task workspace 写到 `.project_os/branches/<branch_id>/tasks/<task_id>/`。
4. task.json 写入完整 branch-aware fields，`depends_on` P0 可为空。
5. `tasks.tsv` 写入完整 row。
6. `set-current-task` 检查 task 与 current_branch 一致。
7. `start` 先解析 current_branch，再解析 branch context，再解析 task。
8. `list-tasks` 支持 `--branch-id`, `--status`, `--stage`, `--json`。
9. `show-task` 输出 objective、stage、handoff、context manifest summary。

Run 步骤：

1. `create-run` 默认读取 task 的 `branch_id`。
2. run path 默认 `runs/<branch_id>/<run_id>/`。
3. `RUN_MANIFEST.json` 写入 `branch_id`, `task_id`, `status`, `created_at`, `code_ref`, `environment`, `inputs`, `commands`, `outputs`, `metrics`, `result_status`。
4. `runs.tsv` 写入 branch-aware row。
5. task-local `run_links.tsv` 写入 run link。
6. `set-current-run` 检查 run/task/branch 一致。
7. `show-run` 输出 manifest summary。
8. `list-runs` 支持 `--branch-id`, `--task-id`, `--status`, `--json`。
9. `close-run` 写 `closed_at` 和 final status。
10. `find_run_manifest()` 支持 branch-aware 查找。
11. Task/run 状态修改写 journal。

验收：

- future agent 能从 current branch/task/run 只读必要 context。
- 每个 run 都能追溯 branch/task。
- 关闭 run 不自动 promote result。

### P0.5 Doctor / validate 提前

目标：在 result lifecycle 前具备最小自诊断能力。

步骤：

1. `refresh-indexes` 支持 branches/tasks/runs/results/assets/releases 的 canonical TSV。
2. root `RUNS_INDEX.tsv` 从 `.project_os/indexes/runs.tsv` 单向派生。
3. `status` 输出 current branch/task/run、counts、runtime focus、last/active/open run summary、candidate/accepted/current result summary 与 current-result/promotion-audit 派生摘要；只读，不刷新索引、不写 canonical state。
4. `doctor` 检查：
   - 缺失 root docs
   - 缺失 `.project_os/`
   - 缺失 `project.json` / `events.jsonl`
   - current pointer 无效
   - branch context 缺失
   - task/run/result branch 不一致
   - branch row 无目录
   - 目录无 branch row
   - run manifest malformed
   - result path 缺失
   - canonical TSV 与 root derived view 漂移
5. `validate` 做严格机器校验。
6. 所有 repair 建议先输出，不自动修。
7. P0 可输出 human-readable repair hints；结构化 `repair-plan.json` 放 P1。

验收：任何中断状态都能给出可读诊断；future hooks 可调用 `doctor/validate`，但当前不依赖 hooks。

### P0.6 Result lifecycle 最小闭环

目标：结果可登记、可查询、可安全 promotion。

步骤：

1. `register-result` 从 run manifest 解析 branch/task。
2. `results.tsv` 写入 branch-aware row。
3. task-local `result_links.tsv` 写入 result link。
4. `list-results` 支持 `--branch-id`, `--task-id`, `--status`, `--json`。
5. `show-result` 输出来源 run/task/branch 和 path。
6. `promote-result`：
   - dry-run 默认。
   - `--apply --approved` 才写入/copy。
   - `--replace` 才覆盖已有 target。
   - 支持 `current/branches/<branch_id>/` 与 `current/project/`。
   - 写 `promoted_to` / `accepted_at`。
7. promotion 支持跨 branch 提升到 `current/project/`，但必须在 result 中保留原 `branch_id`。
8. 更新或刷新 `RESULTS_INDEX.md` human view。
9. 写 `result.registered` / `result.promoted` event。

验收：candidate / accepted / current 状态区分清楚；用户不用翻 run 目录找当前结果；promotion 有明确授权边界。

### P0.7 Short trigger router 与 skill routing

目标：把短触发词做成正式路由工作层，而不是在 description 中堆关键词。

核心规则：

```text
short phrase -> intent -> state check -> CLI action -> verification
```

新增/维护文件：

```text
skills/local/research-project-os/references/short_trigger_router.md
skills/local/research-project-os/SKILL.md
skills/local/project-skeleton/SKILL.md
README.md
docs/SKILL_ROUTING_MATRIX.md
```

步骤：

1. 将短触发分组为 bootstrap/resume、session runtime focus、branch/workstream、task、run lifecycle、result lifecycle、data asset、decision/release。
2. 每个触发词必须映射到稳定 intent，而不是自由操作。
3. 每个 intent 必须定义状态检查、缺失信息问题、CLI command、写后 verification。
4. 在 CLI 中提供非执行式路由解释命令：

   ```bash
   project_os.py route --root <project> "开工"
   project_os.py explain-trigger --root <project> "记录结果" --path <path>
   ```

   输出必须包含 `intent`、当前 state、缺失字段、safety gates、planned commands 和 verification commands。
5. 更新 `research-project-os/SKILL.md` 与 `project-skeleton/SKILL.md`。
6. 增加反逃避规则：不能先跑后补 run、不能直接改 `current/`、不能从短触发路由 destructive cleanup。

验收：用户用短中文就能触发正确 harness intent；skill 不变成巨型手册；`route`/`explain-trigger` 能在不改文件的前提下给出可审计执行计划。

### P0.8 Codex + Claude adapters

目标：先只支持 Codex 和 Claude，保持薄 adapter。

Codex adapter：

1. 保留/更新 `install-adapters --platforms codex`。
2. 写入或更新 `AGENTS.md` managed block。
3. 可选创建 repo-scoped skill `.agents/skills/project-skeleton/SKILL.md`。
4. 只说明读取 `PROJECT_STATE.md`、`.project_os/workflow.md`、runtime pointers、active task manifest，并使用 `project_os.py`。
5. 不复制 canonical state。

Claude adapter：

1. 扩展 `install-adapters --platforms claude`。
2. 创建或 managed-update `CLAUDE.md`。
3. `CLAUDE.md` 只作为入口说明，不复制状态。
4. 暂不创建 active hooks，暂不依赖 `.claude/hooks/`。

验收：Codex/Claude 都能从同一套 `.project_os/` 恢复；adapter 文件可重生成。

### P0.9 Smoke adoption（最小验证，不做完整测试体系）

目标：在临时项目里跑通最小闭环，并保留可重复的命令清单。

步骤：

1. `new-project --root <tmp-project>` dry-run。
2. `new-project --root <tmp-project> --apply`。
3. `install-adapters --platforms codex,claude --apply`。
4. `create-branch --branch-id method_a --title ...`。
5. `set-current-branch --branch-id method_a`。
6. `create-task --title ... --set-current`。
7. `create-run --task-id ... --slug ...`。
8. 创建一个临时 result 文件并 `register-result --run-id ... --path ... --status candidate`。
9. `promote-result --result-id ... --to current/branches/method_a/...` dry-run。
10. 用户确认后 `promote-result ... --apply --approved`。
11. `refresh-indexes`、`doctor`、`validate`。
12. 用一个小 shell/python smoke 脚本记录上述命令，作为开发验证，不作为独立产品功能。

验收：

- 文件结构符合 branch-first。
- `start` 能恢复当前 branch/task/run。
- `RESULTS_INDEX.md` / indexes 可定位结果。
- `events.jsonl` 记录关键状态变化。
- 无需 hooks/plugin/dashboard/subskills 也能完整运行。

---

## 12. P1：完整核心能力补齐

P1 的目标是把 P0 vertical slice 扩成完整日常可用 harness，并补齐审查中提出但不阻塞 P0 的完整性硬化。

### P1.1 Task 管理增强

1. `update-task-stage`
2. `close-task`
3. `add-context`
4. `remove-context`
5. `update-handoff`
6. task priority/owner 支持
7. context manifest required file 检查
8. `task.json.depends_on` 正式启用：`tasks[]` 与 `results[]` 支持 DAG 依赖

### P1.2 Run 管理增强

Status: implemented for the current P1 core baseline.

1. `update-run`
2. `add-run-input`
3. `add-run-command`
4. `add-run-output`
5. `add-run-metric`
6. `add-run-parameter`
7. `capture-run-env --pip-freeze --freeze-file <relative-path>`
8. run environment/code_ref 捕获增强：Python executable/version、platform、conda/virtualenv hint、package count、unparsed freeze lines、captured_at 与 freeze file 路径。
9. run close 时生成详细 `RUN_SUMMARY.md`，覆盖 identity、counts、parameters、inputs、commands、outputs、metrics、promoted targets、environment、package sample 与 notes。

### P1.3 Result 管理增强

1. `accept-result`
2. `supersede-result`
3. `show-current`
4. `RESULTS_INDEX.md` 生成/刷新规则
5. branch-level current 与 project-level current 显示分离
6. supersede/replaced_by 链接检查，避免环

### P1.4 Data asset registry 与影响面

1. `register-asset`
2. `list-assets`
3. `show-asset`
4. `update-asset`
5. `checksum-asset`
6. run input 可引用 `asset_id`
7. generated asset Markdown 从 `assets.tsv` 单向刷新；root `DATA_ASSETS.md` 仅在缺失或已由 harness 生成时覆盖，手写 root 文档保留，生成版写入 `.project_os/exports/views/DATA_ASSETS.generated.md`
8. 新增/刷新 `.project_os/indexes/asset_usage.tsv`，支持 asset → run → result 反向追踪
9. `doctor` 检查 immutable asset checksum 漂移

### P1.4a Large asset externalization / 大文件统一外置

目标：把项目中的大型数据文件、外部存储文件、断裂 symlink 与 run 输入统一纳入 asset registry，而不是让每个 run/branch 复制一份大文件。

默认目标盘策略：

```text
primary large store: /media/teng/HP_P900
backup/mirror store: /media/teng/备份盘2
```

当前观察到 `/media/teng/HP_P900` 可用空间更大，更适合默认承载大 FASTA/HMMER 输入；`/media/teng/备份盘2` 可作为重要资产的 backup/mirror，是否复制超大文件需要由策略和剩余空间决定。

新增/规划命令：

```bash
python scripts/project_os.py plan-externalize-assets --root <project> --threshold 500M --primary-root /media/teng/HP_P900 --backup-root /media/teng/备份盘2 --write-report
python scripts/project_os.py externalize-asset --root <project> --path <large-file> --primary-root /media/teng/HP_P900 --mode copy --apply --approved
python scripts/project_os.py adopt-external-asset --root <project> --path /media/teng/HP_P900/.../target_all_faa.renamed_for_Chen2022_HMMER.faa --asset-id target_all_faa_chen2022_hmmer --old-path runs/.../inputs/target_all_faa.renamed_for_Chen2022_HMMER.faa --write-report
python scripts/project_os.py verify-external-assets --root <project>
python scripts/project_os.py list-asset-locations --root <project>
```

`plan-externalize-assets` dry-run report 应包含：

1. project 内超过阈值的大文件候选。
2. 已经外置但尚未登记的 external absolute paths。
3. 断裂 symlink 与可能的新外置路径映射。
4. run manifest / task context / root docs / scripts 中引用的旧路径。
5. 目标盘挂载状态、可用空间、预估复制量。
6. 建议的 `asset_id`、primary location、backup location、checksum 策略。
7. 是否只登记 external path、是否建议后续 run manifest input 改为引用 `asset_id`、是否存在需要人工处理的旧脚本路径；默认不建议创建 symlink。

`externalize-asset` 安全门：

1. 默认 dry-run。
2. `--apply --approved` 才允许复制或移动。
3. 推荐默认 `--mode copy`：copy → checksum verify → register asset/location → report old-path-to-asset mapping。
4. `--mode move` 必须额外审批；移动后也不删除 provenance，不静默改脚本。
5. 不自动改科研脚本中的路径；只在 report 中列出需要人工确认的替换点。
6. 不把大文件写入 `.project_os/`；只写 `assets.tsv`、`asset_locations.tsv`、`asset_usage.tsv`、generated asset view 与 generated report。
7. 禁止 hard link；不依赖 inode、设备号或本机挂载语义。
8. symlink 不作为 canonical 状态；如未来支持本地 symlink 兼容层，也必须单独 opt-in、可重建、可忽略。

`adopt-external-asset` 安全门：

1. 适用于文件已经在项目外部的场景，不再 copy/move。
2. 默认 dry-run。
3. `--apply --approved` 才允许写 `assets.tsv` / `asset_locations.tsv` / `asset_usage.tsv` / generated asset view / generated report；手写 root `DATA_ASSETS.md` 不被覆盖。
4. apply 时只做 checksum、asset/location 注册、old-path/backup/mirror/archive mapping、可选 run/task usage link。
5. 不创建 hard link，不创建 symlink，不自动改脚本、手写 root docs 或 run manifest。

对 `typeII_pks` 试点的直接映射：

```text
asset_id: target_all_faa_chen2022_hmmer
primary path: /media/teng/HP_P900/bgcdetecttion/typeiipks/target_all_faa.renamed_for_Chen2022_HMMER.faa
kind: data/input
size: ~9.1G
usage: Chen2022 HMMER whole-FAA screening and downstream broad KS scans
adoption note: old project-relative run input path/symlink should be mapped to asset_id/location, not blindly recreated as hardlink/symlink
```

### P1.5 Decision / handoff

1. `record-decision`
2. `list-decisions`
3. project/task/branch scope decision
4. `summarize-state`
5. 保持 `PROJECT_STATE.md` thin
6. decision 事件写入 `events.jsonl`

当前实现状态：

- `record-decision`、`list-decisions`、`update-handoff`、`summarize-state` 已由 `_decision_handoff.py` 承接，public CLI 仍通过 `project_os.py` 调用。
- `summarize-state` 会刷新 branch/task/run/asset_usage 索引后输出 project/root、counts、active branch/task/run、recent events。
- `summarize-state` 已接入 session-aware runtime focus：payload 同时保留 `current_branch` / `current_task` / `current_run` 的兼容字段，并新增 `runtime_focus` 展示 session/global pointer 解析结果。
- `summarize-state` 已补入 `current_results` 派生摘要，包含 all/project/current-branch current result counts、project/branch rows、`audit_ok` 与 promotion-audit warning counts；该部分只读派生，不 promote、不 repair、不写 result/current canonical state。

### P1.6 Release packaging

1. `build-release`
2. `list-releases`
3. `show-release`
4. `validate-release`
5. release `MANIFEST.tsv`
6. release `CHECKSUMS.tsv`
7. release `README.md`
8. `--apply --approved` 后 release row 写入 `releases.tsv`
9. release 事件写入 `events.jsonl`

### P1.7 Migration / adoption

1. 检测旧 flat layout：`.project_os/tasks/<task_id>/` 与 `runs/<run_id>/`。
2. 根据 Section 8.13 生成 migration dry-run plan。
3. 仅在用户明确同意后迁移。
4. 不删除旧 run/result；必要时保留 legacy manifest。
5. 旧 `RUN_MANIFEST.json` 的 dict/string/list provenance shape 不得静默丢弃；迁移应规范化到当前结构化 `inputs` / `commands` / `outputs` / `promoted_to` / `metrics`，并在 dry-run `manifest_repairs` 中显式报告。
6. 默认 `--branch-id` 仍是单目标 branch；当旧 task/run manifest 已带可信 `branch_id` 且存在多 workstream 时，显式 `--preserve-manifest-branches` 可保留这些旧 branch 并生成多个物理目录。未加该 flag 时 branch mismatch 必须阻塞，避免静默合并 workstream。
7. 迁移后 `refresh-indexes` + `doctor` + `validate`。

### P1.8 Integrity rules

新增 `references/integrity_rules.md` 或等价 spec：

1. branch archive 时 active task/run 的处理规则。
2. result supersede/replaced_by DAG 约束。
3. task superseded 后 current result 的有效性规则。
4. 跨 branch promotion 的允许范围和审计字段。
5. `doctor` 按规则区分 error/warning/info。

### P1.9 Repair plan structured output

1. `doctor --json` 输出问题列表。
2. `doctor --repair-plan` 输出有序、可执行但默认不执行的 CLI 建议。
3. repair plan 不执行 destructive 操作，除非未来单独确认。

### P1.10 Consistency model hardening

1. JSON/TSV 写入使用 temp file + `os.replace`。
2. 索引写入期间使用 `.project_os/runtime/lock` 顾问锁。
3. `events.jsonl` 作为轻量审计/WAL；完整 crash replay 可后置。
4. `doctor` 能对账 journal 与当前 snapshot。

当前实现状态：

- temp+replace 已用于 JSON/TSV 写入。
- state-changing CLI 已通过 `.project_os/runtime/lock` 顾问锁保护。
- `validate` / `doctor` 已检查 event 引用是否仍能解析到当前 branch/task/run/result/asset/release snapshot。
- `validate` / `doctor` 已检查当前 snapshot 中非 legacy/adopted 的 branch/task/run/result/asset/release 是否有 `events.jsonl` 覆盖；缺口以 warning 暴露，repair-plan 指向 `summarize-state` / 人工 provenance review，不自动改写 journal。缺失 journal 文件本身时，repair-plan 可建议 approval-gated `restore-journal --apply --approved`，但仍不合成历史事件。
- 完整 crash replay / rollback / repair automation 仍后置到 P2。

### P1.11 `project_os.py` 拆分边界

P0 可保留单文件，但满足任一条件应拆分：

- `project_os.py` 超过 1500 行。
- 命令组超过 8 个且频繁变更。
- 多人同时开发不同命令组。

目标结构：

```text
scripts/
  project_os.py          # CLI entry + dispatch
  _router.py             # short-trigger planning layer（已拆出）
  _export.py             # dashboard/export generated views（已拆出）
  _schema.py             # headers/status/required fields/templates（已拆出）
  _paths.py              # project-local path helpers（已拆出）
  _project_io.py         # JSON/TSV/JSONL IO, pointers, events, advisory lock（已拆出）
  _templates.py          # workflow/config/spec templates（已并入 _schema.py，后续可再拆）
  _journal.py            # append event helper（已并入 _project_io.py，后续可再拆）
  _views.py              # derived Markdown/HTML-ish source text generators（已拆出）
  _integrity.py          # reusable integrity/repair-plan helpers（已拆出）
  _health.py             # validate/doctor command group（已拆出）
  _result_release.py     # result lifecycle + release packaging commands（已拆出）
  _task_run.py          # task lifecycle + run provenance commands（已拆出）
  _assets.py            # asset registry/checksum/usage commands + helpers（已拆出）
  _decision_handoff.py  # decision journal + handoff/state summary commands（已拆出）
  _project_branch.py    # init/new-project/status/start/adapters/refresh + branch commands（已拆出）
  _migration.py         # flat -> branch-first adoption/migration + conflict diagnostics（已拆出）
  _commands/            # 后续可选更细拆分，不急于引入
    validate.py
```

当前拆分状态：

- `project_os.py` 仍是唯一 CLI facade 和 argparse dispatch 入口。
- `_result_release.py` 已承接 `register-result`、`accept-result`、`promote-result`、`supersede-result`、`show-current`、`list-results`、`show-result`、`build-release`、`list-releases`、`show-release`、`validate-release`。
- `_task_run.py` 已承接 task lifecycle 与 run provenance 命令：`create-task`、`set-current-task`、`list-tasks`、`show-task`、`update-task`、`update-task-stage`、`close-task`、`add-dependency`、`remove-dependency`、`add-context`、`remove-context`、`create-run`、`set-current-run`、`list-runs`、`show-run`、`update-run`、`close-run`、`add-run-input`、`add-run-command`、`add-run-output`、`add-run-metric`、`add-run-parameter`、`capture-run-env`。
- Result/release 模块复用 `_task_run.py` 的 `task_dir` / `find_run_manifest` 解析逻辑，避免 result/run 路径解析出现第二套规则。
- `_assets.py` 已承接 asset registry、checksum、usage refresh 与 asset command group：`register-asset`、`list-assets`、`show-asset`、`update-asset`、`checksum-asset`、`refresh-assets`。
- `_task_run.py` 复用 `_assets.py` 的 `find_asset_row`、`asset_usage_row`、`upsert_asset_usage`、`looks_like_url`，`register-asset --run-id` 通过局部导入调用 `add_run_input`，避免模块级循环依赖。
- `_decision_handoff.py` 已承接 decision / handoff / state summary command group：`record-decision`、`list-decisions`、`update-handoff`、`summarize-state`。其中 `summarize-state` 在模块内刷新 branch/task/run/asset usage 索引，避免回依赖 CLI facade，并输出 session-aware `runtime_focus` 与只读派生 `current_results` 摘要。
- `_project_branch.py` 已承接 project/bootstrap/branch 入口命令：`init`、`new-project`、`install-adapters` / `build-adapters`、`status`、`start`、`refresh-indexes`、`create-branch`、`set-current-branch`、`list-branches`、`show-branch`、`archive-branch`，并保留 `project_os.py` 作为唯一 public CLI facade。
- `_migration.py` 已承接 `migrate-branch-first` 及其 helper，并增强 dry-run/apply diagnostics：目标目录已存在、task_id/run_id/result_id 冲突、malformed run manifest、result path 缺失或无法映射、asset path 缺失等会在 apply 前显式报告；`summary` / `conflicts` / `warnings` / `safe_to_apply` 同时镜像在输出顶层，便于脚本和用户直接读取。
- `_health.py` 已承接 `validate` / `doctor` 命令体；`_integrity.py` 继续保留可复用校验 helper 和 repair-plan 生成逻辑，public CLI 仍通过 `project_os.py validate|doctor` 调用。
- 下一步更适合继续真实项目 adoption dogfood，而不是继续做机械拆分。

### P1.12 Documentation / routing

目标：保持 user-facing 文档、reference/schema、模板内置文本、README 与当前实现一致，避免旧 flat-layout 或错误 canonical source 表述继续扩散。

当前实现状态：

- `research-project-os/SKILL.md`、`project-skeleton/SKILL.md`、README、`docs/SKILL_ROUTING_MATRIX.md` 与 `short_trigger_router.md` 已描述 branch-first、route/explain-trigger、approval gates、Codex/Claude adapters 与 hooks-disabled contract。
- `harness_contract.md` 已明确区分 canonical machine state（`.project_os/indexes/*.tsv`、`.project_os/project.json`、`.project_os/journals/events.jsonl`、runtime pointers、branch/task/run manifests）与 root human derived/handoff views（`PROJECT_STATE.md`、`RESULTS_INDEX.md`、`DATA_ASSETS.md`、`RUNS_INDEX.tsv`）。
- `project_adoption.md` 已区分 fresh `init` adoption、old flat harness migration、partial branch-first scaffold repair、mixed/hand-edited manifest dry-run gating。
- `_schema.py` 的内置 `SPEC_TEXTS` 已同步到模板目录，确保新项目 `init/new-project` 生成的 `.project_os/spec/*.md` 包含 run package capture、current-result derived views、journal/current snapshot audit 和 canonical-boundary说明。
- `docs/BIOINFO_WRITING_REFACTOR_PLAN.md` 中旧的“大项目任务内核”表述已收敛为：长期项目工作台/continuation/provenance/计划/状态触发走 `research-project-os` / `project-skeleton`。

后续只按实现变更做增量同步；不要让文档引导用户直接编辑 canonical state。

---

## 13. P2：后置扩展层

P2 是扩展层，不阻塞核心 harness 使用。以下能力不是舍弃，而是在 P0/P1 契约稳定后添加。

### P2.1 Hooks dispatcher

P2.1 当前已经完成 **manual report-only dispatcher 基础层**；尚未启用 active automatic dispatcher，也没有 handler 自动执行机制。P0/P1 已保证 lifecycle events 与 `events.jsonl` 可作为事件源，P2.1 在此基础上提供可手动调用的观察/提醒/report 层。

当前已落地命令：

```bash
list-hooks
dispatch-hooks
```

当前已落地能力：

1. `list-hooks`：展示当前 hooks policy、默认 disabled 配置、可用 handler kind、是否会写 canonical state、是否会阻塞操作。
2. `dispatch-hooks`：从 `.project_os/journals/events.jsonl` 选择最近事件、指定事件名或指定 line/index，生成 report-only JSON。
3. 默认 dispatch kinds：`session_summary`、`reminder`、`opt_in_maintenance`。
4. 可选 kind：`guard`，但当前只是 report-only placeholder，不阻塞 promotion/release/archive。
5. `dispatch-hooks --write-report`：把报告写入 `.project_os/exports/hooks/`；该目录是 generated view，不是 canonical state。
6. 短触发路由支持 `hook状态`、`hooks状态`、`列出hooks`、`hook报告`、`hook提醒`、`派发hook`。
7. hooks 短触发 route 已支持 dispatcher 参数透传：`--event-index` 精确选 journal line；`--event` + `--limit` 选择最近匹配事件；`--kind` 选择 handler；`--write-report --output` 只规划写 generated report。
8. dashboard JSON/HTML/SQLite 已展示 hooks status/config/event source/report counts；这些仍是 generated inspection views。
9. `validate` / `doctor --repair-plan` 已检查 hooks config 是否错误请求 active dispatcher、是否包含未知 kind、event source 是否存在；所有问题均为 warning/advisory，不会启动自动 hooks。

当前仍禁止/未做：

- 不启用 active automatic hook dispatcher。
- 不自动执行 suggested commands。
- 不让 hook 自己修改 canonical state。
- 不让 hook 成为系统必需依赖。
- 不默认启用高风险 guard hook。
- 不绕过 `promote-result`、`build-release` 等命令已有的 `--apply` / `--approved` gates。

实现顺序与状态：

| 顺序 | 能力 | 当前状态 |
|---:|---|---|
| 1 | 只读 session summary report | 已实现，manual report-only |
| 2 | low-risk reminder reports | 已实现，manual report-only |
| 3 | opt-in `doctor` / `validate` / `refresh-indexes` maintenance suggestion | 已实现为建议命令，不执行 |
| 4 | promote/release/archive guard hooks | 仅 report-only placeholder；未来 opt-in |
| 5 | active automatic dispatcher | 后置，等待更多 real-project dogfood |

当前实现文件：

- `scripts/_hooks.py`
- `scripts/project_os.py` 中 `list-hooks` / `dispatch-hooks` CLI facade
- `references/hooks_contract.md`
- `templates/project_os/spec/hooks.md`
- `_schema.py` 内置 hooks spec/config
- `_router.py` hooks 短触发 intent

### P2.2 Sessionized runtime pointers

基础 CLI/runtime 切片已实现。目标是允许同一项目中保留多个“工作会话焦点”，例如写论文会话、方法 A 会话、复现实验会话；每个 session 只保存当前 branch/task/run 指针，不复制 canonical state。

```text
.project_os/runtime/sessions/<session_id>/current_branch
.project_os/runtime/sessions/<session_id>/current_task
.project_os/runtime/sessions/<session_id>/current_run
.project_os/runtime/current_session
.project_os/runtime/sessions/<session_id>/session.json
```

已落地命令：

```bash
create-session
set-current-session
list-sessions
show-session
set-session-focus
pause-session
resume-session
close-session
plan-session-cleanup
```

已接入：

- `current_pointer()` / `set_pointer()`：`current_session` 非空时自动读写 session pointer，否则读写 global pointer。
- `start` / `status`：输出 `current_session` 与 `runtime_focus_source`；`status` 额外输出完整 `runtime_focus`、run frontier summary 与 result/current audit summary。
- `validate` / `doctor`：校验 current session、session manifest 和 session pointer 有效性。
- `export-dashboard`：输出 session summary、session focus 与 session cleanup candidate 派生视图，仍为 generated view。
- `plan-session-cleanup`：输出 closed/paused session archive/GC candidate report；`--write-report` 只写 `.project_os/exports/session_cleanup/` generated view。
- `doctor --repair-plan`：当 closed session cleanup candidates 存在时输出 warning-level advisory 与 report-only `plan-session-cleanup --write-report` 建议；不把候选项视为错误。
- `route` / `explain-trigger`：支持 `新建会话`、`切会话`、`列出会话`、`当前会话`、`更新会话焦点`、`暂停会话`、`恢复会话`、`关闭会话`、`会话清理`。

后续增强但非当前阻塞项：

1. session lifecycle 的 paused/resumed 基础状态已落地；archive/garbage-collection 已有 report-only planner，未来若做物理 cleanup 必须显式 review/approval。
2. session start summary 已有 manual report-only hook；未来可在明确 opt-in 后接入 active dispatcher。
3. session garbage-collection / archive 目前不做删除/移动，只生成 candidate report。
4. dashboard 中更好的 session focus 可视化基础已落地；后续只做更丰富 UI/交互增强。

不允许：

- session 直接覆盖 `.project_os/indexes/*.tsv` 或 branch/task/run manifests。
- session 拥有独立 task/run/result 身份空间。
- 用 session 绕过 promotion/release approval gate。
- 从短触发或默认 cleanup planner 自动删除/移动 session 目录。

### P2.3 Full WAL / lock / crash recovery

P1 做 temp+replace、顾问锁和 journal 对账；完整 replay/rollback/repair automation 后置到 P2。

当前实现状态：

- 已落地 `plan-recovery` 作为 report-only crash/recovery inspection foundation。
- 报告内容：
  - `.project_os/runtime/lock` 是否存在、pid 是否仍在运行、lock 年龄与 stale candidate 原因；
  - `.project_os/` 与根部 entry 的 atomic-write `*.tmp` / `.tmp.*` 残留；
  - `.project_os/journals/events.jsonl` 缺失、malformed line、缺 key warning；
  - 必需 harness 文件/目录与 root human entry 缺失；
  - runtime pointer 是否指向缺失 branch/task/run/session；
  - branch/task/run manifest 与 indexes 的 ID drift；
  - `RESULTS_INDEX.md`、managed `DATA_ASSETS.md` 或 `.project_os/exports/views/DATA_ASSETS.generated.md`、`RUNS_INDEX.tsv` 和 dashboard generated view 的 stale advisory。
- `--write-report` 只写 `.project_os/exports/recovery/recovery_plan_<timestamp>.json`，不写 canonical state。
- `doctor --repair-plan` 与 dashboard 只暴露 advisory，不执行修复。

仍后置：

- event journal replay；
- operation WAL / transaction log；
- crash rollback；
- 自动清理 lock/tmp；
- 根据 journal 重建对象或历史事件。

这些能力若未来实现，必须显式命令、dry-run first、用户审批、validate/doctor gate，并且不得绕过现有 promotion/release/checksum/provenance approval gate。

### P2.4 Dashboard/export

1. `export-dashboard`
2. task/run/result graph
3. static HTML
4. optional SQLite export as generated view only

注意：SQLite/HTML 只能是 generated view，不能成为 canonical source。

当前实现状态：

- `export-dashboard` 已提供 dry-run/apply。
- apply 后生成 `.project_os/exports/dashboard.json` 与 `.project_os/exports/dashboard.html`。
- `--sqlite` 可额外生成 `.project_os/exports/dashboard.sqlite`。
- dashboard payload 已包含派生 `graph.nodes` / `graph.edges`、节点类型计数与边关系计数。
- HTML 已渲染 graph summary、graph nodes table 与 graph edges table。
- SQLite 已生成 `graph_nodes` 与 `graph_edges` 表。
- 当前 graph 覆盖 project、branch、task、run、result、current target、asset、release 节点，以及 ownership、provenance、promotion、asset usage、release inclusion 等边。
- dashboard payload 已包含派生 `session_focus`，HTML 渲染 session focus cards/status counts/sessions table，SQLite 生成 `session_focus` 与 `sessions` 表。
- dashboard payload 已包含派生 `session_cleanup`、hooks status/config view 和 recovery inspection summary；HTML 展示 cleanup candidates、hooks status 与 recovery summary；SQLite 生成 `session_cleanup_candidates`、`hooks_status`、`hooks_allowed_kinds`、`recovery_status`、`recovery_summary`。
- dashboard payload 已包含派生 `current_results`，复用 `show-current --audit` 的 current/project/branch 结果视图与 promotion audit；HTML 展示 current result counts/current result rows/branch counts/audit warnings；SQLite 生成 `current_results_status`、`current_results`、`current_result_branch_counts`、`promotion_audit` 表。
- graph 已包含 session 节点以及 `focus_branch` / `focus_task` / `focus_run` 边，用于展示 runtime focus overlay。
- 这些文件只从 canonical indexes / journal / runtime pointers / config 派生，不反向写入 canonical state。

Short-trigger current-result route update:

- `route` / `explain-trigger` 已支持 `当前结果` / `查看当前结果`，生成只读 `show-current --scope <all|project|branch> --audit` 计划。
- 当显式传入 `--branch-id` 且 scope 仍为默认 `all` 时，路由会收窄为 branch scope，避免用户想看 branch 当前结果却得到 project/all 混合视图。
- 该路由只查看 current-result 派生视图；它不等同于 `设为当前结果` / `替换当前结果`，不得 promote result、不得 repair `current/`、不得写 `results.tsv` 或其他 canonical state。

### P2.5 Subskills

仅在主 router 太大或路由稳定后拆：

```text
project-os-branch
project-os-task
project-os-run
project-os-result
project-os-data
project-os-release
```

规则：

- subskill 调用同一个 `project_os.py`。
- subskill 不复制 schema。
- subskill 不发明新状态。

### P2.6 Plugin packaging

后置到真实项目 smoke test 之后。

未来结构可能是：

```text
plugins/research-project-os/
├── .codex-plugin/plugin.json
├── skills/
├── references/
├── scripts/
├── templates/
└── hooks/              # disabled by default
```

验收：

- local install works。
- uninstall 不破坏项目内 `.project_os/`。
- hooks 默认不启用或必须明确说明。

### P2.7 More adapters

后续再考虑：

- OpenCode
- Cursor
- Gemini
- Antigravity

---

## 14. Hooks 预留说明

当前不启用 active automatic hooks，但已提供 manual report-only dispatcher。事件名必须稳定，所有自动化都必须围绕 `events.jsonl` 与 `project_os.py` CLI 展开。

### 14.1 Lifecycle events

Lifecycle events in P0+ must be appended to `.project_os/journals/events.jsonl`; manual hook reports already read this journal, while active automatic hooks remain deferred and may later subscribe to the same source.

```text
project.initialized
project.adopted
journal.restored
branch.created
branch.changed
branch.archived
task.created
task.changed
task.closed
run.created
run.updated
run.closed
session.created
session.changed
session.paused
session.resumed
session.closed
result.registered
result.accepted
result.promoted
result.superseded
asset.registered
asset.updated
release.created
release.validated
decision.recorded
handoff.updated
state.updated
export.created
```

### 14.2 P0/P1 已预留的文件契约

当前阶段不启动自动 hooks，但模板和 reference 中保留明确契约，并已有手动 report-only CLI：

```text
skills/local/research-project-os/references/hooks_contract.md
.project_os/spec/hooks.md
.project_os/config.yaml hooks:
project_os.py list-hooks
project_os.py dispatch-hooks
```

默认配置：

```yaml
hooks:
  enabled: false
  mode: disabled
  dispatcher: none
  event_source: .project_os/journals/events.jsonl
  allowed_kinds:
    - session_summary
    - reminder
    - opt_in_maintenance
    - guard
  policy:
    must_call_cli: true
    cannot_write_canonical_state_directly: true
    failure_is_non_blocking_by_default: true
    guard_hooks_require_opt_in: true
```

解释：

- `enabled: false` 是当前实际状态，不触发 handler。
- `event_source` 固定指向 lifecycle journal，避免未来再发明第二套事件源。
- `must_call_cli` 表示 hook 不能复制核心逻辑，只能调用 `project_os.py`。
- `cannot_write_canonical_state_directly` 表示 hook 不得直接改 `.project_os/indexes/*.tsv`、runtime pointers、branch/task/run/result/release canonical 文件。
- `failure_is_non_blocking_by_default` 表示 reminder/summary/maintenance 类 hook 失败不应破坏主流程。
- `guard_hooks_require_opt_in` 表示 promote/release/archive 这类 guard 只能在用户明确启用后拦截。

### 14.3 Hook 分类

| 类型 | 触发时机 | 例子 | 当前做不做 |
|---|---|---|---|
| Session hooks | 会话开始/恢复后 | 显示 current session/branch/task/run | 已做 manual report-only；不自动触发 |
| Lifecycle hooks | 命令完成后 | run.closed 后提示 register-result / refresh-indexes / doctor | 已做 manual reminder report；不执行命令 |
| Maintenance hooks | 低风险维护建议 | 建议 `refresh-indexes` / `doctor` / `validate` | 已做 opt-in suggestion；不执行命令 |
| Guard hooks | 高风险动作前 | promote/release/archive 前二次提醒 | 仅 report-only placeholder；未来 opt-in |

### 14.4 hook 原则

1. hook 不拥有业务逻辑。
2. hook 只调用现有 CLI。
3. hook 默认失败不破坏主流程。
4. hook 从只读/提醒开始。
5. guard hook 必须 opt-in。
6. hooks 不新增 canonical state。

### 14.5 dispatcher / handler 接口

当前 manual dispatcher 与未来 active dispatcher 都以 journal event 为输入。最小 event payload：

```json
{
  "ts": "2026-06-23T00:00:00Z",
  "event": "run.closed",
  "actor": "cli",
  "branch_id": "main",
  "task_id": "task_...",
  "run_id": "run_...",
  "result_id": "",
  "asset_id": "",
  "release_id": "",
  "detail": {}
}
```

handler 输出应是非 canonical 的 summary 或 JSON：

```json
{
  "hook_id": "session-summary",
  "kind": "session_summary",
  "event": "session.start",
  "status": "ok",
  "message": "Current branch main; no active run.",
  "suggested_commands": [
    "python scripts/project_os.py status --root <project>"
  ]
}
```

dispatcher 实现顺序：

1. 只读 session summary。✅ manual report-only 已实现。
2. reminder hooks。✅ manual report-only 已实现。
3. opt-in `doctor` / `validate` / `refresh-indexes` maintenance。✅ 已实现为建议命令，不执行。
4. promote/release/archive guard hooks。当前仅 report-only placeholder；未来必须 opt-in。
5. active automatic dispatcher。后置，等待更多真实项目 dogfood。

不允许先做会自动改状态的 hook。

---

## 15. 从 `addyosmani/agent-skills` 吸收的设计点

参考仓库：`https://github.com/addyosmani/agent-skills`

可吸收：

1. **meta-skill / routing layer**
   我们应强化 `research-project-os` / `project-skeleton` 的路由职责。

2. **短命令映射长流程**
   后续可引入 `/project-start`, `/branch-new`, `/run-open`, `/result-promote` 等入口。

3. **标准 skill anatomy**
   `Overview / When to Use / Core Process / Common Rationalizations / Red Flags / Verification`。

4. **anti-rationalization**
   明确禁止 agent 跳过 run 登记、跳过 promotion 审批、直接改 current。

5. **progressive disclosure**
   `SKILL.md` 只做入口，references/scripts 承载细节。

6. **hooks 的正确定位**
   session start hook 可用于未来自动恢复现场，但不是当前 P0。

7. **plugin packaging 的正确定位**
   plugin 是分发层，不应驱动核心文件契约。

不可直接照搬：

- 不用它的 `spec -> plan -> build -> test -> review -> ship` 替换我们的科研项目生命周期。
- 不直接导入 external repo 作为本地原创 skill。
- 不把 persona/agents 作为当前核心目标。

---

## 16. 当前代码与目标差距

当前 `project_os.py` 已完成 P0 branch-first vertical slice，并补入部分 P1/P0-adjacent 能力。

已落地能力：

1. `INDEX_HEADERS` 已覆盖 `branches/tasks/runs/results/assets/asset_usage/releases`。
2. `init/new-project` 创建 `.project_os/project.json`、`.project_os/journals/events.jsonl`、`.project_os/branches/main/`、`runs/main/`、`current/branches/main/`。
3. branch/task/run/result 的创建、列出、展示、runtime pointer 与 promotion 最小闭环已 branch-aware。
4. Codex 与 Claude thin adapters 已实现。
5. asset registry 已具备 `register/list/show/update/checksum/refresh`，run input 可引用 `asset_id`。
6. decision/handoff 已具备 `record-decision`、`list-decisions`、`update-handoff`、`summarize-state`；其中 `summarize-state` 已补齐 session-aware `runtime_focus` 与只读派生 `current_results` 摘要，可同时查看当前 project/branch/task/run 与当前结果/audit 概览。
7. release packaging 已具备 dry-run/apply、`MANIFEST.tsv`、`CHECKSUMS.tsv`、`README.md`、`validate-release`。
8. result/task/run 增强命令已补入：`accept-result`、`supersede-result`、`show-current`、`update-task`、`update-task-stage`、`close-task`、`add-dependency`、`remove-dependency`、`add-context`、`remove-context`、`update-run`。
9. flat → branch-first migration 已具备 `migrate-branch-first` dry-run/apply 基础能力。
10. `doctor` / `validate` 已检查 branch/task/run/result 基础一致性，并扩展到 asset checksum、release package、derived view drift、dependency/replacement DAG、event reference 与 journal/current-snapshot coverage。
11. `doctor --repair-plan` 已输出非执行式修复建议；写操作已有 `.project_os/runtime/lock` 顾问锁。
12. run close 会补环境快照并写详细 `RUN_SUMMARY.md`；`capture-run-env --pip-freeze --freeze-file <path>` 会把 package snapshot 写入 run 目录下的 freeze 文件，并在 manifest 中记录 `environment.package_capture`。
13. 短触发路由已有 CLI planning surface：`route` / `explain-trigger`，可把 `开工`、`新建分支`、`开始运行`、`记录结果`、`捕获运行环境`、`当前结果`、`查看当前结果`、`设为当前结果`、`hook报告` 等短语解析为 intent、缺失字段、安全门、planned commands 和 verification commands，且不直接执行写操作；`当前结果` / `查看当前结果` 只规划只读 `show-current --audit`，不等同于 result promotion；路由层已支持 `--pip-freeze/--freeze-file` 透传，hooks route 已支持 `--event-index/--event/--limit/--kind/--write-report/--output` 透传，并要求 promotion/release 的 `route --apply` 必须同时带 `--approved` 才进入 ready 状态。
14. `project_os.py` 已开始按 P1.11 拆分；短触发 router 已提取为 `scripts/_router.py`，dashboard/export 已提取为 `scripts/_export.py`，schema/constants/templates 已提取为 `scripts/_schema.py`，路径 helpers 已提取为 `scripts/_paths.py`，IO/event/pointer/lock helpers 已提取为 `scripts/_project_io.py`，derived view 生成已提取为 `scripts/_views.py`，integrity/repair-plan helpers 已提取为 `scripts/_integrity.py`，result/release 命令已提取为 `scripts/_result_release.py`，task/run 命令已提取为 `scripts/_task_run.py`，asset 命令与 helper 已提取为 `scripts/_assets.py`，decision/handoff/state summary 命令已提取为 `scripts/_decision_handoff.py`，project/bootstrap/branch/adapters 命令已提取为 `scripts/_project_branch.py`，migration/adoption 命令已提取为 `scripts/_migration.py`，validate/doctor 命令已提取为 `scripts/_health.py`，主入口仍保留统一 CLI dispatch。
15. `export-dashboard` 已实现 generated dashboard/export：JSON + static HTML，`--sqlite` 可生成 SQLite 派生视图；dashboard payload 已包含 derived graph nodes/edges、`session_focus`、`session_cleanup` candidate view、hooks/recovery advisory summary，以及 `current_results` current-result/promotion-audit view；HTML/SQLite 也暴露 graph/session/current-result/promotion-audit/cleanup/hook/recovery inspection tables。这些输出不作为 canonical state。
16. `migrate-branch-first` 已增强 adoption edge cases：dry-run 暴露 missing scaffold anchors、missing branch workspace、link-table/run-manifest repair、旧 run manifest provenance shape normalization、目标目录冲突、ID/path 冲突、手工编辑 manifest 的 task/run ID 或 branch mismatch、run/task branch ownership mismatch、invalid legacy branch ID、malformed task/run/branch manifest、missing result/asset path、无法回填 result provenance、`planned_branches` 与 safe_to_apply 标记；`summary` / `conflicts` / `warnings` / `safe_to_apply` 已在 dry-run 与 apply 输出顶层镜像，避免调用方必须深入 `diagnostics`；默认单目标 branch 保守迁移，显式 `--preserve-manifest-branches` 可保留旧 manifest 中已有 branch 并迁入多个 branch-first 物理目录；apply 后会补齐旧 `project.json` / `events.jsonl` / `.project_os/spec/*.md` / root entry files / runtime pointers / current 与 release 目录 / branch workspace / missing indexes，补齐旧 run manifest 必需字段，规范化旧 dict/string/list `inputs` / `commands` / `outputs` / `promoted` / `key_results` 而不丢弃 provenance，升级 task run/result link headers，回填 result 的 branch/task/run 归属，并在 flat run 迁移后重写旧 artifact/result/asset path。
17. `show-current` 已增强为 current/result 分层派生视图：`--scope all|project|branch` 可区分 project-level 与 branch-level current targets，`--audit` 可报告 missing current targets、duplicate current targets、cross-branch promotions；`RESULTS_INDEX.md` 也会生成 Current views 分区。
18. Promotion audit 已接入 `validate` / `doctor --repair-plan`，current-target drift 会以 warning 和非破坏性修复建议暴露，而不需要 active hooks。
19. Journal/current snapshot 对账已接入 `validate` / `doctor --repair-plan`：当前 snapshot 中缺少 lifecycle event 覆盖的非 legacy 对象会以 warning 暴露；指向缺失对象的 event 也会被报告。
20. Sessionized runtime pointers 基础切片已落地：`create-session`、`set-current-session`、`list-sessions`、`show-session`、`set-session-focus`、`pause-session`、`resume-session`、`close-session` 通过 `.project_os/runtime/current_session` 与 `.project_os/runtime/sessions/<session_id>/current_*` shadow global focus；`start/status/validate/doctor/export-dashboard/route` 已接入 session 信息，并禁止 paused/closed session 成为 active current session。
21. Session archive/GC 的 report-only planner 已落地：`plan-session-cleanup` 默认 dry-run，只列出 closed/paused 等 candidate，`--write-report` 只写 generated JSON，不删除、不移动、不改写 runtime session state；短触发 `会话清理` 只规划该命令；`export-dashboard` 与 `doctor --repair-plan` 也能显示 cleanup candidate advisory。
22. Disposable E2E release smoke 已固化为 `scripts/smoke_project_os_e2e.py`，覆盖全部 80 个 public `project_os.py` subcommands；`docs/RESEARCH_PROJECT_OS_E2E_COVERAGE.md` 记录覆盖审计。该 smoke 只使用临时项目和显式临时 external roots，并覆盖 approval-gate negative paths、generated views、report-only recovery/session cleanup/hooks、restore-journal fixture、protected `DATA_ASSETS.md` fixture、migration dry-run，以及 no-hardlink/no-symlink externalization 检查。

剩余主要差距：

1. migration/adoption 已通过真实项目 `/home/teng/pingtai_final_20260430` 的只读扫描与 `/tmp` 副本 dogfood：dry-run 顶层 diagnostics safe，`--apply --mode copy` 和 fresh-copy `--apply --mode move` 后均 validate 0 errors / 0 warnings、doctor `ok=true`、start 可恢复 `main` / `20260619_nmr_gcf_poc`；重复迁移能正确暴露 target_exists，`--replace` dry-run 将冲突降为 non-blocking；move 后仅保留空 legacy `.project_os/tasks/` 容器且后续 dry-run actions=0。此前还已通过真实项目 dry-run dogfood、真实项目 move/copy 复制迁移验证、重复迁移 target_exists/`--replace` dogfood、`analysis_runs/` unusual root dogfood、cross-branch legacy manifest synthetic dogfood、partial-migrated synthetic dogfood、hand-edited manifest negative smoke，以及 external artifact positive smoke：旧 flat harness 缺 `project.json` / `events.jsonl` / spec 模板 / root entry files / branch workspace / current-release 目录 / 新 index headers 时，dry-run 能报告 scaffold/branch/index repairs；manifest ID/branch mismatch、malformed manifests、duplicate IDs 会阻止 safe apply；旧 run manifest dict/string/list provenance shape 会被显式报告并规范化保留；显式 `--preserve-manifest-branches` 可把旧多 branch workstream 拆入多个物理目录；外部 artifact path 可通过 task-local `result_links.tsv` 回填 run provenance；后续仍需更多真实跨 branch 或重度手工修改样本。
2. validate/doctor 命令体已从 `project_os.py` 抽出到 `_health.py`；后续健康检查增强应由真实项目 dogfood 证据驱动。
3. result lifecycle 的 current/project/branch 分层展示与基础 promotion audit 已落地；后续仍可补更细审计字段或 UI 展示。
4. dashboard graph/session focus 的 generated JSON/HTML/SQLite inspection view 已落地；后续 rich dashboard 主要是 UI/交互增强，不应引入新的 canonical state。
5. run lifecycle 包版本捕获与详细 summary 已落地；后续只根据真实项目 dogfooding 补充字段，不再作为主要缺口。
6. 一致性硬化中的 journal snapshot 对账已落地；完整 crash recovery / WAL replay 仍后置。
7. manual report-only hooks dispatcher 与 sessionized runtime pointers 基础 CLI/runtime 已完成；session cleanup 已有 report-only planner；active automatic hooks dispatcher、plugin packaging、物理 session archive/GC 和更多 adapters 仍为后置扩展。
8. E2E smoke 已覆盖全 CLI surface，但仍应继续在真实项目副本/真实 adopted harness 上做 dogfood；真实项目 dogfood 不应直接并入 disposable smoke，以免引入环境依赖或误触真实数据。

---

## 17. 推荐提交批次

### Commit 1：文档审查采纳与 canonical plan

- 更新本文档。
- 旧路线文档标记 superseded。
- 更新 `PROJECT_STATE.md`、`progress.md`、`findings.md`、`task_plan.md`。

### Commit 2：schema constants + project identity + journal

- 更新 `project_os.py` headers/status/helper。
- 新增 `.project_os/project.json` 生成。
- 新增 `.project_os/journals/events.jsonl` 与 append helper。

### Commit 3：init/new-project branch-first

- 修改 init/new-project 模板。
- 创建 main branch workspace。
- 写 runtime current_branch。

### Commit 4：branch commands

- create/list/show/set/archive branch。
- doctor branch pointer 检查。

### Commit 5：task/run branch-aware migration

- task path 改为 branch-local。
- run path 改为 `runs/<branch_id>/<run_id>/`。
- start/status/list/show 更新。

### Commit 6：doctor/validate baseline

- 提前补齐最小 self-diagnosis。
- 检查 project.json/events/current pointers/schema headers。

### Commit 7：result minimal lifecycle

- register/list/show/promote。
- current branch/project target。
- RESULTS_INDEX.md derived view。

### Commit 8：short trigger router + Codex/Claude adapter

- `research-project-os/SKILL.md` anatomy。
- `project-skeleton` 触发。
- Codex/Claude managed docs。
- README/routing docs。

### Commit 9：P0 smoke adoption

- 临时项目验证脚本/命令清单。
- `doctor` / `validate` baseline。

---

## 18. 成功标准

核心 harness 成功的标准：

1. 可以初始化或接管一个项目。
2. 存在 `.project_os/project.json` 作为 project identity/schema anchor。
3. 可以解析 current branch/task/run。
4. 多个 workstream 不混淆 provenance。
5. 每个 branch 同时有 index row 和物理 workspace。
6. 每个 formal run 有 branch-aware `RUN_MANIFEST.json`。
7. result 能从 draft/candidate 到 accepted/current。
8. data asset 能被登记并被 run 引用。
9. decision/handoff 不依赖聊天记录。
10. release 可从 accepted/current results 打包。
11. Codex/Claude 能通过薄 adapter 使用同一套 `.project_os/`。
12. 不启用 hooks/plugin/dashboard/subskills 时系统仍完整可用。
13. `events.jsonl` 记录关键 lifecycle events，可供后续 hooks/dashboard 使用。
14. 未来 hooks/plugin/dashboard/subskills 有稳定接口可接入。
15. 缺失事件日志时有最小、可审计、approval-gated 的 `restore-journal` 入口，不需要手工补写或盲目 re-init。

---

## 19. 开发时必须遵守的仓库规则

来自 `AGENTS.md`：

1. 新 authored skills 放在 `skills/local/<skill-name>/`。
2. 不把 mirrored external skills 当本地原创。
3. 修改 user-facing skill 时同步更新 README。
4. registry 文件由 `scripts/sync_skills.py` 生成。
5. commit 前运行：

```bash
python3 scripts/validate_skills.py
python3 scripts/sync_skills.py --dry-run
```

6. 不提交 secrets、`.env`、cache。
7. unrelated global mirror updates 与 harness 变更分开提交。

---

## 20. 下一步执行入口

截至 2026-06-23，P0 branch-first vertical slice 与多项 P1 能力已经落地；当前不再从 P0.1 重新开始，而是继续做 **P1 收敛与真实项目 dogfooding**。

当前可直接执行的下一步：

1. **继续真实项目 adoption dogfood**：`/home/teng/pingtai_final_20260430` 副本 dry-run/copy/move/repeated target_exists/`--replace` 已通过；此前 `analysis_runs/` unusual root、cross-branch legacy manifest synthetic、partial-migrated synthetic、hand-edited manifest negative、external artifact positive cases 也已通过。继续收集更多旧项目样本，重点观察真实跨 branch 旧数据和更复杂的手工改动 manifest。
2. **继续增强 migration 真实场景报告**：根据更多 dogfood 结果补充更复杂冲突类别，而不是只做 synthetic case。
3. **继续收敛 CLI facade**：validate/doctor 已拆出；后续只做小规模 facade cleanup，保持 public CLI 不变。
4. **完善 current/result 审计细节**：基础 branch/project/all current 视图已完成；后续可继续补更细审计字段或 UI 展示，保持 `results.tsv` 为 canonical registry。
5. **保留 dashboard rich UI 后置**：generated graph payload/HTML/SQLite 已可检查 provenance map；后续只做 UI/交互增强，不让 dashboard 反写状态。
6. **继续保持 active hooks/plugin 后置**：维护当前 hooks contract 与 manual report-only dispatcher，不实现自动执行 dispatcher；plugin packaging 仍等核心文件契约 dogfood 稳定后再做。
7. **Session 基础已完成，后续只做增强**：基础 session focus 已可用于多上下文切换；manual session summary hook report 已可用；paused/resumed 与 cleanup report planner 已落地。下一步不再扩大 session scope，除非真实项目 dogfood 证明需要物理 archive/GC 或 active session hook。
8. **Journal 修复只保持最小化**：`restore-journal` 已覆盖缺失 event source 的安全恢复入口；不要把它扩展成历史事件自动重建或 crash replay。

已完成并需保持不回退的 P0/P1 基线：

```text
branch-first init/new-project
branch/task/run/result canonical indexes
events.jsonl lifecycle journal
Codex + Claude thin adapters
short-trigger route/explain-trigger planning layer
asset registry + run provenance appenders
decision/handoff + release packaging
doctor/validate + repair-plan + advisory lock
journal/current snapshot audit
restore-journal missing event-source repair entry
result/release module split
task/run module split
asset module split
decision/handoff module split
project/branch/init/adapter module split
migration module split + conflict diagnostics
real legacy harness scaffold adoption
dashboard graph generated view
run package capture + detailed RUN_SUMMARY.md
```
