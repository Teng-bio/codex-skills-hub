---
name: literature-method-data-miner
description: "Interpret short Chinese literature-method prompts as a request to mine research methods and data from papers. Use when the user says 文献是怎么做的、这篇文献怎么做的、这些文献怎么做的、参考文献是怎么做的、文献里的方法、文献方法、参考文献的做法、从文献找科研方法、从文献收集数据、正文和附录数据、补充材料数据、根据文献找实验设计, even when papers were not provided and should be found through deep research first. In `.project_os` projects, route through research-project-os before recording literature findings."
---

# Literature Method Data Miner

把用户的短提示“文献是怎么做的”理解为完整科研阅读任务：

> 从相关文献中找到科研方法、实验/计算流程、数据来源、正文表图数据、附录/补充材料数据，并总结哪些做法可借鉴。

## Default interpretation

When triggered, do **not** ask the user to restate the long version. Assume the user wants:

1. Identify the relevant papers.
2. Extract methods from main text and supplement/appendix where available.
3. Collect structured research data from figures, tables, captions, methods, results, supplemental files, and repository links.
4. Compare how papers did the work.
5. Propose reusable ideas, risks, and next experiments/analyses.

Only ask a short clarification if **no topic/papers/project context exists at all**.

## Routing

Use this as a router, not a replacement for other skills:

- In an existing `.project_os` project, use `research-project-os` for task/run/result context before recording multi-paper findings.
- Use `auto-deep-research` when papers are not provided and need to be found.
- Use `pubmed-database` / `tooluniverse-literature-deep-research` for biomedical or life-science literature discovery.
- Use `read-arxiv-paper` for arXiv URLs or TeX-source reading.
- Use `research-orchestrator` when the user provides multiple papers/reports and wants synthesis.
- Use `scientific-critical-thinking` to evaluate method rigor, limitations, and idea quality.
- Use `paper-context-resolver` when the purpose is reproducing exact dataset split, preprocessing, metric, checkpoint, or runtime assumptions.

## Workflow

1. **Scope from context**
   - If PDFs/URLs/PMIDs/DOIs are provided, start from them.
   - If not provided, infer the topic from the project/chat and run literature discovery.
   - For large tasks, write/update `task_plan.md`, `findings.md`, and `progress.md`.

2. **For each paper, extract**
   - Bibliographic identity: title, year, DOI/PMID/arXiv, journal/conference.
   - Research question and hypothesis.
   - Data/materials: organism, cohort, samples, accession IDs, datasets, inclusion/exclusion criteria.
   - Method workflow: experiment/computation, software, parameters, statistics, validation.
   - Main-text data: tables, figure values/captions, key numerical results.
   - Supplement/appendix data: supplemental tables, extra methods, code/data links.
   - Reproducibility details: code, versions, seeds, hardware, checkpoints, splits, metrics.
   - Limitations/confounders and what is reusable.

3. **Synthesize across papers**
   - Create a method-comparison matrix.
   - Separate directly reusable methods from risky/underspecified methods.
   - Identify missing data or supplement files that must be downloaded.
   - Suggest concrete project adaptations and follow-up searches.

4. **Evidence discipline**
   - Do not invent unavailable supplement data.
   - Mark evidence as `main text`, `figure/table`, `supplement`, `code/repo`, or `inference`.
   - Cite exact paper/source for every extracted method or data item.

## Output shape

Prefer this compact structure:

1. `我默认把“文献怎么做的”理解为：方法 + 数据 + 附录/补充材料 + 可借鉴点。`
2. Paper/source list.
3. Method/data matrix.
4. Supplement/data availability checklist.
5. Cross-paper method comparison.
6. Ideas for our project.
7. Missing evidence / next retrieval steps.

See `references/output-template.md` for a reusable table template.
