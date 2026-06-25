#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


DIRS = [
    "01-项目总览",
    "02-论文说明",
    "03-项目-论文配对",
    "04-证据矩阵",
    "05-源路径索引",
    "_system",
]


FILES = {
    "00-Hub.md": "# 项目文献桥接库\n\n## 项目\n\n## 当前问题\n\n## 关键论文\n\n## 下一步\n",
    "01-项目总览/当前状态.md": "# 当前状态\n\n## 当前结论\n\n## 依据来源\n\n## 不确定点\n",
    "01-项目总览/当前技术路线.md": "# 当前技术路线\n\n## 路线摘要\n\n## 相关论文\n\n## 风险\n",
    "01-项目总览/当前问题清单.md": "# 当前问题清单\n\n| 问题 | 相关论文 | 证据强度 | 下一步 |\n|---|---|---|---|\n",
    "01-项目总览/下一步任务.md": "# 下一步任务\n\n| 任务 | 依据 | 验收标准 |\n|---|---|---|\n",
    "04-证据矩阵/文献支持矩阵.md": "# 文献支持矩阵\n\n| 项目模块/问题 | 相关论文 | 支持内容 | 证据强度 | 项目动作 | 风险 |\n|---|---|---|---|---|---|\n",
    "04-证据矩阵/方法借鉴矩阵.md": "# 方法借鉴矩阵\n\n| 方法 | 来源论文 | 可复用组件 | 输入 | 输出 | 改造成本 | 优先级 |\n|---|---|---|---|---|---|---|\n",
    "04-证据矩阵/风险与未证明点.md": "# 风险与未证明点\n\n| 风险 | 来源 | 影响模块 | 当前证据 | 需要补的验证 |\n|---|---|---|---|---|\n",
    "05-源路径索引/项目报告源路径.md": "# 项目报告源路径\n\n",
    "05-源路径索引/外置文献库索引.md": "# 外置文献库索引\n\n",
    "_system/registry.md": "# Registry\n\n| ID | Type | Path | Source |\n|---|---|---|---|\n",
    "_system/lint-report.md": "# Lint report\n\n尚未运行检查。\n",
}


def main() -> int:
    ap = argparse.ArgumentParser(description="Scaffold an Obsidian project-literature bridge vault.")
    ap.add_argument("--vault", required=True, help="Target vault directory")
    ap.add_argument("--project-name", required=True)
    ap.add_argument("--project-root", required=True)
    ap.add_argument("--literature-root", required=True)
    ap.add_argument("--apply", action="store_true", help="Write files; default is dry-run")
    args = ap.parse_args()

    vault = Path(args.vault).expanduser()
    actions: list[str] = []
    for d in DIRS:
        actions.append(f"mkdir {vault / d}")
    for rel in FILES:
        actions.append(f"write {vault / rel}")

    if not args.apply:
        print("DRY-RUN")
        print("\n".join(actions))
        return 0

    vault.mkdir(parents=True, exist_ok=True)
    for d in DIRS:
        (vault / d).mkdir(parents=True, exist_ok=True)
    for rel, body in FILES.items():
        path = vault / rel
        if path.exists():
            continue
        path.write_text(body, encoding="utf-8")

    meta = (
        f"project_name: {args.project_name}\n"
        f"project_root: {Path(args.project_root).expanduser()}\n"
        f"literature_root: {Path(args.literature_root).expanduser()}\n"
    )
    (vault / "_system" / "source-paths.txt").write_text(meta, encoding="utf-8")
    print(f"created_or_updated={vault}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

