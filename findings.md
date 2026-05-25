# Findings & Decisions

## Requirements

- Reorganize the skill ecosystem based on existing local skills first.
- Keep bioinformatics Agent functions separate from manuscript writing skills.
- Reuse existing `tooluniverse-*`, `pubmed-database`, `literature-method-data-miner`, `scientific-critical-thinking`, and reproduction skills.
- First concrete skill should be `bioinfo-evidence-orchestrator`, not a full duplicated bioinformatics toolkit.

## Research Findings

- `codex-skills-hub` already mirrors global skills and has a local authored-skill area at `skills/local/`.
- Existing local skill `literature-method-data-miner` is a good example of a router-style skill with a compact `SKILL.md` and one reference template.
- Hub scripts support validation and inventory refresh:
  - `scripts/validate_skills.py`
  - `scripts/sync_skills.py --apply`

## Technical Decisions

| Decision | Rationale |
|---|---|
| Keep orchestrator lightweight | The existing `tooluniverse-*` and PubMed skills should do domain work |
| Put detailed evidence-pack schema in a reference file | Progressive disclosure keeps `SKILL.md` concise |
| Do not update `nature-skills` in this phase | User asked to plan and refactor based on local skills first |

## Resources

- `docs/BIOINFO_WRITING_REFACTOR_PLAN.md`
- `docs/SKILL_ROUTING_MATRIX.md`
- `skills/local/literature-method-data-miner/SKILL.md`
- `docs/OPERATING_MODEL.md`

## Implementation Findings: Bio Writing Line

- Writing tasks should be routed by product type, not by source material alone:
  - full manuscript/abstract/introduction/discussion/outline -> `bio-paper-writing`
  - figure/table-grounded Results -> `bio-results-writing`
  - workflow provenance -> `bio-methods-writing`
  - prose repair/translation/overclaim -> `bio-polishing`
  - revision letters -> `bio-reviewer-response`
  - repository and FAIR wording -> `bio-data-code-availability`
  - Chinese paper presentation -> `bio-paper2ppt`
- The safest shared contract remains `EVIDENCE_PACK.md` plus figure/table inventories.
- Specialized writing skills should route back to `bioinfo-evidence-orchestrator` when evidence, accession validation, database facts, or new analyses are missing.
- No new skill duplicates the existing ToolUniverse, PubMed, RNA-seq, enrichment, sequence, protein structure, phylogenetics, visualization, or reproduction skills.

## Auto-routing Finding

- Users should not need to say exact skill names. A broad router skill should capture natural prompts such as “这些结果能不能写文章”, “帮我看看下一步”, “这个流程写成方法”, “审稿人这个怎么回”, and then select the evidence or writing lane.
- Ambiguous mixed requests should default to evidence first, then manuscript writing.
