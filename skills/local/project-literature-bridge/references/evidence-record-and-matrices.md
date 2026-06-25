# Evidence records and bridge matrices

## Evidence Record

Use one record per reusable claim.

```md
### ER-001

- Source: [[short-paper-note]]
- Source type: full paper | preprint | project report | dataset | abstract-only | metadata-only
- Claim:
- Claim type: author claim | project interpretation | cross-paper synthesis
- Claim strength: speculative | observed | supported | strong
- Supports:
- Contradicts / weakens:
- Method / dataset / metric:
- Limitation:
- Project relevance:
- Allowed wording:
- Forbidden stronger wording:
```

## Claim strength

- `speculative`: plausible idea; not enough evidence for project action alone.
- `observed`: reported observation or example; may guide exploration.
- `supported`: backed by methods/results enough to justify a cautious project task.
- `strong`: replicated, directly relevant, or supported by multiple strong sources.

## Project-paper support matrix

```md
| 项目模块/问题 | 相关论文 | 支持内容 | 证据强度 | 项目动作 | 风险 |
|---|---|---|---|---|---|
| M1 NMR峰特征 | [[DEEPPicker1D_NMR峰拾取]] | 峰位、峰宽、置信度可作为峰对象特征 | supported | loader保留peak_features | 需校准ppm轴 |
```

## Method reuse matrix

```md
| 方法 | 来源论文 | 可复用组件 | 输入 | 输出 | 改造成本 | 优先级 |
|---|---|---|---|---|---|---|
```

## Risk matrix

```md
| 风险 | 来源 | 影响模块 | 当前证据 | 需要补的验证 |
|---|---|---|---|---|
```

## Next-action matrix

```md
| 下一步 | 对应项目问题 | 支持论文/报告 | 验收标准 | 备注 |
|---|---|---|---|---|
```

