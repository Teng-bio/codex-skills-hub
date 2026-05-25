# Vague Prompt Map

Use these examples to interpret ordinary user prompts without requiring skill names.

| User prompt | Route | Why |
|---|---|---|
| 帮我看看这个 GSE 能不能写文章 | `bioinfo-evidence-orchestrator` | need dataset inventory, evidence strength, risks |
| 这些差异基因下一步怎么做 | `bioinfo-evidence-orchestrator` -> `tooluniverse-gene-enrichment` | analysis/evidence step before prose |
| 这些图帮我写成论文结果 | `bio-results-writing` | figure-grounded Results prose |
| 这个流程帮我写材料方法 | `bio-methods-writing` | workflow provenance to Methods |
| 这段 discussion 帮我润色一下 | `bio-polishing` | manuscript prose already exists |
| 审稿人说没有外部验证怎么回 | `bio-reviewer-response` | reviewer response with missing-action flags |
| GEO 和 GitHub 都有了，帮我写数据代码可用性 | `bio-data-code-availability` | availability statement |
| 这篇文章做个组会 PPT | `bio-paper2ppt` | presentation from paper/evidence |
| 这篇文献是怎么做的 | `literature-method-data-miner` | method/data extraction from paper |
| 帮我分析并写一篇文章 | evidence first, then `bio-paper-writing` | mixed request must not skip evidence pack |
