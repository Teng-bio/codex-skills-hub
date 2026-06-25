---
name: paper-reading-workflow
description: Use when the user asks to read, 精读, 总结, 拆解, 批判性审读, or make an Obsidian note for a research paper, PDF, arXiv paper, DOI, paper URL, or local literature file, especially when they care about 论文怎么做, 方法/数据/实验, 证据强度, 局限, 复现, or 项目借鉴.
---

# Paper Reading Workflow

## Core Rule

Use this as the default paper-reading router for the user.

The target output is normally one polished Chinese Obsidian Markdown note, not three separate reports. Treat `deeppapernote` as the main production workflow, and force two lenses into its planning and final note:

- `literature-method-data-miner`: method, data, experiment, figure/table evidence, reproducibility, reusable ideas.
- `scientific-critical-thinking`: evidence strength, overclaiming, limitations, bias, generalization, and replication risk.

Only create separate method-mining or critique files when the user explicitly asks for comparison, audit, review, or multi-paper synthesis.

## Required Sub-Skills

- **REQUIRED MAIN SKILL:** Use `deeppapernote` for a single-paper deep note, PDF processing, note planning, figure/table placement, linting, and Obsidian save.
- **REQUIRED LENS:** Use `literature-method-data-miner` whenever the user asks or implies "这篇文献怎么做的", "方法", "数据", "实验", "复现", or "借鉴".
- **REQUIRED LENS:** Use `scientific-critical-thinking` before finalizing the note whenever the user wants quality judgment, limitations, evidence strength, claim boundaries, or serious reading rather than a shallow summary.
- **REQUIRED FIGURE/TABLE LENS:** Use `scientific-explanatory-schematics` rules whenever the note needs original Figure/Table insertion, Figure/Table unpacking, technical-route diagrams, mechanism diagrams, or supplemental schematics.

If one of these skills is unavailable, say which skill is missing and continue with the same checklist manually.

## Workflow

1. Resolve the paper source.
   - Prefer the user's local PDF path, then DOI/arXiv/URL.
   - If identity is ambiguous, clarify before writing.
   - For `deeppapernote`, honor its Python and pipeline requirements instead of shortcutting.

2. Run the DeepPaperNote pipeline as the main path.
   - Produce the normal evidence bundle, figure/table decisions, note plan, linted final note, and Obsidian save.
   - Do not present an abstract-only or title-only summary as a finished reading note.

3. Force method/data coverage into the note plan.
   - Research question and task definition.
   - Data/materials, datasets, samples, splits, sources, or corpus.
   - Method workflow with input, operation, and output.
   - Model/software/parameters/statistics/evaluation protocol.
   - Main figure/table evidence and key numbers.
   - Supplement/code/repository/reproducibility details.
   - What can be reused in the user's project and what is risky.

4. Force original Figure/Table coverage into the note plan.
   - Inventory all source visuals that affect method understanding, task definition, main results, ablations, comparisons, limitations, or project decisions.
   - Insert high-value original figures/tables when a usable image or crop is available.
   - If an important visual cannot be inserted, add a text-only unpacking block with the source location and concrete reason.
   - For every inserted or text-only high-value visual, explain: what is shown, which route step it corresponds to, how to read the result, what conclusion it supports, what it cannot prove, and what it suggests for the user's project.
   - Use self-drawn schematics only as optional interpretation; caption them as `项目解读示意图，非原文证据`.

5. Force critical-thinking coverage before final save.
   - What the paper proves.
   - What it does not prove.
   - Whether conclusions are proportional to evidence.
   - Whether results depend on narrow datasets, tasks, metrics, model choices, or prompts.
   - Missing ablations, weak baselines, statistical issues, hallucination risk, bias/confounding, and generalization limits.
   - Concrete follow-up checks or replication experiments.

6. Save one integrated Chinese note unless instructed otherwise.
   - Keep DeepPaperNote's required structure.
   - Add method/data and rigor checks as sections or subsections, not detached chat commentary.
   - Prefer durable Obsidian output under the user's knowledge-base path when provided.

## Success Criteria

A paper-reading run is successful only if the final artifact can answer these questions:

| Question | Required evidence |
|---|---|
| 这篇论文解决什么问题？ | Problem, task, and paper claim are explicit. |
| 数据/任务/输入输出是什么？ | Dataset or material details are identified or marked missing. |
| 方法到底怎么做？ | Stepwise mechanism with enough detail to explain or reproduce. |
| 关键结果靠什么支撑？ | High-value original Figures/Tables are inserted and explained when usable; otherwise explicitly unpacked with the omission reason. Metrics and key numbers are cited or summarized. |
| 论文证明了什么、没证明什么？ | Claim boundaries and unsupported extensions are separated. |
| 复现需要什么？ | Parameters, code/data links, evaluation protocol, and missing details are listed. |
| 对我有什么用？ | Reusable ideas, project mapping, risks, and next reading items are concrete. |

## Common Mistakes

- Do not generate three long files by default. The normal output is one integrated DeepPaperNote-style note.
- Do not treat `literature-method-data-miner` as a replacement for DeepPaperNote; it is a method/data extraction lens.
- Do not treat `scientific-critical-thinking` as generic criticism; tie every critique to evidence, experiment design, result interpretation, or missing information.
- Do not leave valuable original figures as unexamined thumbnails or one-line captions; decode the figure/table and state the evidence boundary.
- Do not call the run complete before DeepPaperNote's required lint/review/save stages are actually complete.
- Do not leave useful judgments only in chat if the user asked for a knowledge-base artifact; write them into the note.

## Reusable Invocation

When the user asks to read a paper, apply this instruction internally:

```text
Use DeepPaperNote as the main workflow. In the note plan and final Chinese Obsidian note, force the literature-method-data-miner checklist for method/data/experiment/reproducibility/reuse, and force the scientific-critical-thinking checklist for evidence strength, claim boundaries, limitations, overclaiming, and replication risk. Output one integrated Markdown note unless the user explicitly asks for separate files.
Also force the scientific-explanatory-schematics Figure/Table rule: every high-value original visual should be inserted and explained when usable, or explicitly unpacked without image with the reason it was not inserted.
```
