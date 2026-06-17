# Claude Code Integration

## 概述

从 2026-06-17 起，`codex-skills-hub` 同时同步 **Codex** 和 **Claude Code** 两个全局 skill 目录：

- **Codex**: `~/.codex/skills` → `skills/global/`
- **Claude Code**: `~/.claude/skills` → `skills/global/`

这确保了两个工具使用统一的 skill 库，新建的 skill 会自动镜像到两边。

## 同步配置

在 `registry/sources.tsv` 中配置了两个源：

```tsv
source_id	scope	path	enabled	note
global_codex_skills	global	/home/teng/.codex/skills	yes	Installed global Codex skills
global_claude_skills	global	/home/teng/.claude/skills	yes	Installed global Claude Code skills
```

## 工作流

### 创建新 skill

使用 `skill-library-publisher` skill 或手动执行：

```bash
cd /home/teng/claude_code/codex-skills-hub

# 1. 创建新 skill
python3 scripts/new_skill.py my-new-skill \
  --description "Skill description. Use when 用户说..." \
  --apply

# 2. 同步并提交
python3 scripts/sync_skills.py --apply --commit --push
```

新 skill 会自动出现在：
- `skills/local/my-new-skill/`（原始创作位置）
- GitHub 仓库（版本控制）

### 安装到全局

创建并测试 skill 后，安装到全局目录：

```bash
# 安装到 Codex
ln -s ~/claude_code/codex-skills-hub/skills/local/my-new-skill ~/.codex/skills/

# 安装到 Claude Code
ln -s ~/claude_code/codex-skills-hub/skills/local/my-new-skill ~/.claude/skills/
```

下次同步时会自动镜像到 `skills/global/`。

### 更新现有 skill

```bash
cd /home/teng/claude_code/codex-skills-hub

# 1. 直接编辑 skill 文件
vim skills/global/some-skill/SKILL.md

# 2. 同步并提交
python3 scripts/sync_skills.py --apply --commit --push
```

### 自动同步（可选）

启用 watch 模式进行持续同步：

```bash
cd /home/teng/claude_code/codex-skills-hub
python3 scripts/sync_skills.py --watch --apply --commit --push --interval 300
```

或使用 systemd service（见 `services/codex-skills-hub-sync.service.example`）。

## Skill 命名规则

### Codex Skills（无命名空间）

大多数 skills 直接使用名称，无前缀：

```
/implement-paper
/planning-with-files
/bio-paper-writing
```

### CCG Skills（带命名空间）

CCG 工具和质量门使用 `ccg:` 前缀：

```
/ccg:verify-security
/ccg:verify-quality
/ccg:verify-change
/ccg:verify-module
/ccg:gen-docs
```

其他 CCG impeccable skills 也使用 `ccg:` 前缀：

```
/ccg:polish
/ccg:clarify
/ccg:optimize
```

## 目录结构

```
codex-skills-hub/
├── skills/
│   ├── global/           # 从 ~/.codex/skills 和 ~/.claude/skills 镜像
│   │   ├── ccg/          # CCG 工具套件（Claude Code 特有）
│   │   ├── bio-*/        # 生信相关 skills
│   │   ├── planning-with-files/
│   │   └── ...
│   ├── local/            # 本仓库原创 skills（优先创建位置）
│   └── workspace/        # 项目级 workspace skills
├── registry/
│   ├── SKILL_INVENTORY.tsv  # 人可读清单
│   ├── skills.json          # 机器可读清单
│   └── sources.tsv          # 同步源配置
└── docs/
    └── CLAUDE_CODE_INTEGRATION.md  # 本文档
```

## 差异说明

### Codex 特有 skills

- 原始 Codex CLI 工具的 skills

### Claude Code 特有 skills

- **CCG 套件**: 质量门工具（verify-security, verify-quality 等）
- **CCG domains**: 知识领域自动路由（AI, 架构, DevOps, 前端设计等）
- **CCG impeccable**: 高级代码质量工具

### 共享 skills

绝大多数 skills 在两个环境中共享，包括：
- 生信研究 skills（bio-*）
- 文献和论文 skills（paper-*, literature-*）
- 通用开发 skills（planning-with-files, implement-paper 等）

## 故障排除

### Skills 未出现在 Claude Code

1. 确认 skill 已安装到 `~/.claude/skills/`
2. 重启 Claude Code 会话
3. 检查 skill 的 `user-invocable` 元数据设置

### 同步冲突

如果两个源中有相同文件但内容不同，同步脚本会标记为 conflict。手动解决：

```bash
# 查看冲突
cd ~/claude_code/codex-skills-hub
python3 scripts/sync_skills.py --dry-run | grep conflict

# 手动合并后重新同步
python3 scripts/sync_skills.py --apply
```

## 参考

- [codex-skills-hub README](../README.md)
- [OPERATING_MODEL.md](./OPERATING_MODEL.md)
- CCG 规则: `~/.claude/rules/ccg-skills.md`
- CCG 路由: `~/.claude/rules/ccg-skill-routing.md`
