# 🔬 Research Orchestrator

A Claude skill that merges multiple deep research reports into one verified, authoritative document — with every link checked, every fact cross-referenced, and every claim sourced.

## Problem

You run 2–3 deep research sessions on the same topic and get back overlapping, sometimes contradictory reports with dead links and unverified claims. Manually comparing, verifying, and merging them is tedious.

## Solution

Upload your research files → the skill automatically:

1. **Parses** all documents (Markdown, PDF, plain text)
2. **Compares** them section-by-section — finds agreements, contradictions, unique insights
3. **Verifies** every URL (HTTP check, redirect tracking) and every factual claim (cross-reference + web search)
4. **Merges** the best content into a single unified report
5. **Outputs** a professional DOCX with inline citations, verification report, and source quality ratings

## Features

| Feature | Details |
|---|---|
| **Link Verification** | Parallel HTTP checking (10 threads), redirect tracking, page title extraction |
| **Fact Cross-Referencing** | Claims corroborated across documents are marked verified; single-source claims get web search confirmation |
| **Source Quality Tiers** | Tier 1 (official/gov/journals) → Tier 2 (reputable secondary) → Tier 3 (forums/blogs) |
| **Contradiction Resolution** | Flags disagreements, uses web search as tiebreaker, documents reasoning |
| **Unverified Claims Appendix** | Claims that can't be confirmed are separated — not deleted, not mixed in |
| **DOCX Output** | TOC, inline hyperlinks, color-coded verification status, full verification stats |

## Installation

### As a Claude Skill (.skill file)

Download `research-orchestrator.skill` from [Releases](https://github.com/Co4an/research_orchestrator/releases) and install via Claude settings.

### Manual

Clone this repo and point Claude to the `SKILL.md`:

```bash
git clone https://github.com/Co4an/research_orchestrator.git
```

## Usage

Upload 2+ research documents to Claude and say:

```
Compare these research reports, verify everything, and create one final document.
```

or:

```
Merge these deep research outputs — check all links, cross-reference facts, give me a single verified DOCX.
```

The skill triggers automatically when it detects multiple research documents + merge/compare/verify intent.

### Trigger Phrases

- "compare research", "merge reports", "combine deep research"
- "verify links in my research", "check sources", "fact-check these documents"
- "create unified report", "best of all research", "make one good version"

## Architecture

```
┌─────────────────────────────────────────────────┐
│                  INPUT (2+ docs)                 │
│           .md  .pdf  .txt  .html                 │
└──────────────────┬──────────────────────────────┘
                   │
          ┌────────▼────────┐
          │  Phase 1: Parse  │  → inventory.json
          └────────┬────────┘
                   │
        ┌──────────▼──────────┐
        │  Phase 2: Compare    │  → comparison.json
        │  (agreement matrix)  │    (contradictions, coverage)
        └──────────┬──────────┘
                   │
     ┌─────────────▼──────────────┐
     │     Phase 3: Verify         │
     │  ├─ Layer 1: Link check     │  → link_results.json
     │  ├─ Layer 2: Fact x-ref     │  → verification.json
     │  └─ Layer 3: Source quality  │
     └─────────────┬──────────────┘
                   │
        ┌──────────▼──────────┐
        │  Phase 4: Merge      │  Best content + citations
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │  Phase 5: DOCX out   │  → Final document
        └─────────────────────┘
```

## Bundled Scripts

### `scripts/extract_urls.py`

Extracts all URLs from text files with surrounding context and line numbers.

```bash
python scripts/extract_urls.py report1.md report2.md > urls.json
```

### `scripts/check_links.py`

Validates URLs in parallel — checks HTTP status, follows redirects, extracts page titles.

```bash
python scripts/check_links.py urls.json > results.json
```

Output:
```json
{
  "total": 42,
  "ok": 38,
  "broken": 4,
  "results": [...]
}
```

## Output Structure

The final DOCX follows this structure:

- **Executive Summary** — synthesized key findings
- **Main Sections** — best content per topic, with inline `[Source](URL)` citations
- **Source Comparison Notes** — where sources agreed/disagreed and which was used
- **Verified Sources** — numbered list of all working URLs with tier ratings
- **Appendix: Unverified Claims** — claims that couldn't be confirmed
- **Verification Report** — stats (links checked, facts verified, contradictions resolved)

## Requirements

- Claude with computer use (Claude.ai or Claude Code)
- Python 3.8+ (available in Claude's environment)
- `docx` skill for DOCX generation

## License

MIT
