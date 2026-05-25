---
name: bio-research-auto-router
description: "Broad auto-router for vague Chinese or English bioinformatics, life-science research, omics, manuscript, paper-writing, reviewer-response, data-availability, PPT, literature-method, accession, GEO/SRA, RNA-seq, enrichment, workflow, or evidence-pack tasks when the user does not name a specific skill. Use for prompts like 帮我看看这些结果, 这个能不能写文章, 下一步怎么做, 整理一下生信结果, 写论文, 改文章, 审稿意见怎么回, 做组会PPT. Routes to bioinfo-evidence-orchestrator, bio-paper-writing, bio-results-writing, bio-methods-writing, bio-polishing, bio-reviewer-response, bio-data-code-availability, bio-paper2ppt, literature-method-data-miner, and existing tooluniverse/pubmed/reproduction skills."
---

# Bio Research Auto Router

Use this lightweight router when the user gives a natural, vague, or mixed life-science/bioinformatics request and does **not** name a specific skill.

The goal is to choose the right lane automatically:

```text
facts / analysis / validation / reproduction / evidence -> evidence lane
manuscript prose / polishing / reviewer response / availability / PPT -> writing lane
mixed request -> evidence first, writing second
```

## First decision

| User intent clue | Route |
|---|---|
| 查、验证、分析、跑、复现、QC、accession、GEO/SRA、数据库、基因/蛋白/通路事实 | `bioinfo-evidence-orchestrator` or existing specialist skills |
| “这些结果能不能写文章”, “写论文前整理一下”, “帮我看看结果靠谱吗” | `bioinfo-evidence-orchestrator` first |
| 写 abstract/introduction/discussion/title/outline/整篇文章 | `bio-paper-writing` |
| 根据图、表、结果、figure legend 写 Results | `bio-results-writing` |
| 写材料与方法、Methods、workflow 写法、软件参数描述 | `bio-methods-writing` |
| 润色、中译英、改段落、SCI 语言、术语统一、overclaim 检查 | `bio-polishing` |
| 审稿意见、rebuttal、大修/小修、batch effect/FDR/外部验证/数据泄露质疑 | `bio-reviewer-response` |
| Data Availability、Code Availability、数据/代码上传、GEO/SRA/ENA/BioProject/BioSample/PRIDE/GitHub/Zenodo | `bio-data-code-availability` |
| 组会 PPT、journal club、论文汇报、paper to PPT | `bio-paper2ppt` |
| “文献是怎么做的”, “参考文献的做法”, 从文献找方法/数据/补充材料 | `literature-method-data-miner` |
| PubMed、MeSH、找医学文献 | `pubmed-database` or `auto-deep-research` |
| RNA-seq/DESeq2、富集、序列、蛋白结构、系统发育 | relevant `tooluniverse-*` specialist skill |
| 论文代码怎么跑、仓库复现、README-first reproduction | `repo-intake-and-plan` -> `env-and-assets-bootstrap` -> `minimal-run-and-audit` |

## Default rules for vague prompts

1. If the user says “能不能写文章/有没有价值/下一步怎么做” and provides results or datasets, create or request an `EVIDENCE_PACK.md` first.
2. If the user provides prose and asks “改一下/润色/更像论文”, use writing/polishing, not analysis.
3. If the user asks “分析并写”, split into two phases: evidence first, writing second.
4. If a requested writing claim lacks evidence, flag the gap instead of inventing support.
5. Ask a clarification question only when choosing the wrong lane would be risky. Otherwise infer and proceed.

## Optional reference

Open [references/vague-prompt-map.md](references/vague-prompt-map.md) when testing or tuning natural-language routing examples.

## Default output when routing only

```text
我会按这个任务类型处理：<chosen lane / skill>
原因：<1 sentence>
下一步产物：<EVIDENCE_PACK.md / Results draft / Methods draft / response tracker / PPT plan / etc.>
```
