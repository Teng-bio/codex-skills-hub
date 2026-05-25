# Bioinformatics Slide Structures

## Default 12-slide Chinese group-meeting deck

1. 标题页：论文问题和一句话结论
2. 背景：生物学或临床问题为什么重要
3. 缺口：现有数据、方法或机制解释的不足
4. 数据与研究设计：队列、数据集、样本、assay
5. 分析流程：从原始数据到主要证据
6. 关键结果 1：全局模式或主发现
7. 关键结果 2：通路、细胞类型、模块或候选基因
8. 关键结果 3：验证、对照、外部数据或稳健性
9. 方法可靠性：QC、统计设计、baseline、消融或敏感性分析
10. 综合模型：这篇文章认为发生了什么
11. 局限性：样本、批次、验证、可复现性、泛化边界
12. 总结与讨论问题

## Method or pipeline paper variant

Use:

`problem -> method idea -> workflow -> benchmark design -> baseline comparison -> ablation/robustness -> usability -> limitations`

## Resource or atlas paper variant

Use:

`community need -> dataset construction -> quality control -> resource content -> query/use cases -> reuse value -> limits and availability`

## Biomarker paper variant

Use:

`clinical problem -> cohort design -> discovery -> model/marker performance -> external validation -> bias/confounding -> clinical boundary`

## Slide evidence rules

- One slide should have one main message.
- A workflow slide should explain why each step matters, not only list tools.
- Enrichment plots support pathway hypotheses, not full mechanism by themselves.
- Validation slides should separate internal validation from external validation.
- Use limitation slides to prepare discussion, not as an afterthought.
