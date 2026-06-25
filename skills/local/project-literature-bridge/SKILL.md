---
name: project-literature-bridge
description: Connects a local research/project directory with an external literature library and generates an independent Obsidian project-literature bridge knowledge base pairing project summaries, short topic-focused paper notes, evidence records, method reuse, risks, and next actions. Use when 用户要项目总结和论文说明搭配、项目-文献桥接、项目报告与文献库、Obsidian项目文献库、外置文献库索引、根据项目报告整理参考文献、把论文映射到项目模块、文献证据矩阵、论文标题要简短概括主题、逐篇精读论文、每篇文章总结、论文深度笔记、deep paper note、deeppapernote、paper-reading-workflow、literature-reading-and-synthesis.
---

# Project Literature Bridge

## Core rule

Build a separate Obsidian knowledge base that answers:

```text
项目现在的问题是什么 -> 哪些论文解释/支持/反驳 -> 可借鉴什么方法 -> 风险是什么 -> 下一步怎么做
```

Do **not** turn the project root into an Obsidian vault. Do **not** move, rename, deduplicate, or copy the external literature library unless the user explicitly asks.

## Required routing

Use this skill as the bridge controller, then call or emulate these component skills when relevant:

- `research-project-os`: read `.project_os`, `PROJECT_STATE.md`, `DATA_ASSETS.md`, `RESULTS_INDEX.md`, `DECISIONS.md`, and current task context.
- `literature-reading-and-synthesis`: entry router for `read / 精读 / 总结 / 拆解 / 批判性审读 / Obsidian note` paper tasks. (Installed from `jjfroehlich/agent-skills-for-academic-research`; formerly referenced as `paper-reading-workflow`.)
- `deeppapernote`: main producer for one-paper deep notes when writing detailed Chinese Obsidian paper summaries.
- `pdf`: extract local PDF text/tables/metadata before summarizing.
- `literature-method-data-miner`: extract method/data/experiment/reproducibility/reuse details from papers.
- `scientific-critical-thinking`: assess evidence strength, limitations, overclaiming, bias, and replication risk.

If `literature-reading-and-synthesis` or `deeppapernote` is unavailable in the current runtime, do not stop. Emulate them with `references/deep-paper-reading.md` and mark notes as `status: deep-read-draft` until full PDF extraction/reading is complete.

## Workflow

1. **Resolve inputs**
   - `project_root`: local project directory.
   - `literature_root`: external paper/library directory.
   - `vault_root`: independent Obsidian vault or a new folder under the user's Obsidian container.
   - If the target vault is not explicit, create a new project-specific folder, not a parent catch-all vault.

2. **Read project state first**
   - Prefer authoritative files. See `references/project-intake.md`.
   - Read only reports, state, plans, indexes, and user-approved guide documents by default.
   - Avoid full source-code crawling unless the user asks for implementation audit.

3. **Inventory the literature library**
   - Read README/manifest/TSV files before PDFs.
   - List PDF/Markdown files by topic folder.
   - Do not parse every PDF by default; select core papers according to project problems.
   - Use concise paper note titles. See `references/vault-schema.md`.

4. **Switch to deep-read mode when requested**
   - Trigger when the user asks `逐篇精读`, `每篇文章都要总结`, `论文深度笔记`, `read every paper`, or similar.
   - Route each selected PDF through `literature-reading-and-synthesis` -> `deeppapernote` when available.
   - Otherwise use `pdf` extraction plus the checklist in `references/deep-paper-reading.md`.
   - Replace metadata-only notes with full notes; do not leave central papers as shallow summaries.
   - Track progress in `<vault_root>/_system/deep-read-progress.tsv`.

5. **Build the bridge map**
   - Extract project modules/problems.
   - Map each module to supporting papers, method ideas, evidence strength, risks, and next actions.
   - Mark unsupported project claims explicitly instead of hiding uncertainty.

6. **Write Obsidian notes**
   - Use the vault layout in `references/vault-schema.md`.
   - Use the paper note schema in `references/paper-note-schema.md`.
   - For full paper reading, use `references/deep-paper-reading.md` in addition to the paper note schema.
   - Use evidence and matrix templates in `references/evidence-record-and-matrices.md`.
   - Keep note titles short: enough to identify the topic, not a full bibliographic sentence.

7. **Validate**
   - Source paths exist.
   - Every project recommendation links to paper/project evidence or is marked `待证实`.
   - Every paper-derived recommendation includes a limitation/risk note.
   - In deep-read mode, every selected PDF has a progress row and a note with `status: deep-read-draft` or `status: deep-read`.
   - External library files remain untouched unless explicitly approved.

## Deterministic helpers

Optional scripts:

```bash
python skills/local/project-literature-bridge/scripts/scaffold_bridge_vault.py \
  --vault <vault_root> --project-name <name> --project-root <project_root> --literature-root <literature_root> --apply

python skills/local/project-literature-bridge/scripts/inventory_literature_library.py \
  --root <literature_root> --out <vault_root>/05-源路径索引/外置文献库索引.tsv
```

Run helpers in dry-run mode first when available.

## Success criteria

The final vault must let the user answer:

| Question | Expected location |
|---|---|
| 项目现在做什么？ | `01-项目总览/当前状态.md` |
| 当前关键问题是什么？ | `01-项目总览/当前问题清单.md` |
| 哪些论文支持哪些模块？ | `03-项目-论文配对/` and `04-证据矩阵/文献支持矩阵.md` |
| 每篇论文对项目有什么用？ | `02-论文说明/*.md` |
| 哪些结论可靠，哪些只是启发？ | `04-证据矩阵/风险与未证明点.md` |
| 下一步怎么做？ | `01-项目总览/下一步任务.md` |
