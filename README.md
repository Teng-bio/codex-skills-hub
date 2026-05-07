# codex-skills-hub

这是个人 GitHub-backed Codex / agent skill 库，用来集中管理、同步、验证、发布本机和项目内的 skills。

仓库地址：

```text
git@github.com:Teng-bio/codex-skills-hub.git
```

## 这个仓库解决什么问题

- 把 `~/.codex/skills` 中的全局 skill 版本化备份。
- 把全局 skill 和项目级 workspace skill 都纳入同一个 inventory；`planning-with-files` 已从试点 workspace 版本提升为全局 skill。
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

python scripts/new_skill.py my-skill-name \
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
python scripts/validate_skills.py
python scripts/sync_skills.py --apply --commit --push
```

## 自动同步 / 自动上传

预览变化：

```bash
python scripts/sync_skills.py --dry-run
```

同步 inventory 和镜像：

```bash
python scripts/sync_skills.py --apply
```

同步、提交、推送：

```bash
python scripts/sync_skills.py --apply --commit --push
```

持续监控并自动上传：

```bash
python scripts/sync_skills.py --watch --interval 60 --apply --commit --push
```

也可以参考：

```text
services/codex-skills-hub-sync.service.example
```

## 触发原则

Codex 选择 skill 时主要依赖每个 `SKILL.md` frontmatter 的 `description`。因此每个 skill 的 description 必须写清楚：

1. 这个 skill 做什么；
2. 什么用户意图/关键词应该触发它；
3. 中文触发词也要写进去；
4. 复杂项目中，输出应该写回哪里，例如 `task_plan.md`、`findings.md`、`progress.md`、`PROJECT_STATE.md` 或 `.project_flow/`。

## Skill 总览与触发方式

### 核心工作流 / 项目状态

| Skill | 作用 | 典型触发语 | 位置 |
|---|---|---|---|
| `planning-with-files` | 大项目任务内核，用 `task_plan.md`、`findings.md`、`progress.md` 管理当前任务、阶段和进展。已全局安装，workspace 镜像保留为试点来源/对照。 | `继续下一步`、`大项目逐步推进`、`制定计划`、`拆解任务`、`恢复上下文`、`当前进展`、`task_plan.md`、`planning-with-files` | `skills/global/planning-with-files/`；试点镜像：`skills/workspace/pipeline_v2/planning-with-files/` |
| `project-state-maintainer` | 维护每个项目的 `PROJECT_STATE.md`，让项目可从文件恢复，而不是依赖聊天记录。 | `记录项目状态`、`更新项目状态文档`、`总结当前进展`、`下一步是什么`、`handoff`、`resume state` | `skills/global/project-state-maintainer/` |
| `project-flow-guard` | 管控生成产物、重跑、版本、current/baseline/release，避免文件覆盖和版本混乱。 | `重跑`、`重新生成`、`保留这个版本`、`设为当前版本`、`release`、`打包`、`开分支`、`snapshot`、`清理旧版本` | `skills/global/project-flow-guard/` |
| `project-version-curator` | 对已经混乱的目录做盘点、版本冲突检测、dry-run 整理方案。 | `整理结果`、`太混乱了`、`清理目录`、`版本混乱`、`final/current/v1/v2 很多`、`生成 inventory`、`dry-run cleanup` | `skills/global/project-version-curator/` |

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

1. `planning-with-files` 读取 active plan。
2. 需求不清时用 `grill-me`。
3. 需要拆小步骤时用 `ticket-breakdown`。
4. 有结果/版本/重跑时用 `project-flow-guard`。
5. 结束前用 `project-state-maintainer` 更新 `PROJECT_STATE.md`。

### 整理混乱项目结果

1. `project-version-curator` 做 inventory 和 dry-run 整理方案。
2. `project-flow-guard` 管控任何真正的 copy/move/archive/release 操作。
3. `project-state-maintainer` 记录当前整理状态。

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
