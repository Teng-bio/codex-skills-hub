---

name: research-orchestrator
description: "Orchestrate, compare, verify, and merge multiple deep research reports into a single authoritative document. Use this skill whenever the user uploads 2+ research reports/documents and wants them compared, verified, merged, deduplicated, fact-checked, or synthesized into one. Also trigger when the user says 'compare research', 'merge reports', 'verify links in my research', 'combine deep research', 'check sources', 'fact-check these documents', 'create unified report', 'best of all research', or mentions having multiple deep research outputs. Trigger even if the user just uploads several long documents and asks to 'make one good version'. Do NOT use for single-document editing, simple summaries, or non-research content. 中文触发词：根据这几篇文献有什么想法、整合这几篇文献、比较这几篇论文、合并多篇文献、核验这些文献来源、从多篇文献提炼结论、综合多个研究报告。"
---

# Research Orchestrator

Merge multiple deep research reports into one verified, authoritative DOCX document. Every claim is cross-referenced, every link is checked, every fact is confirmed.

## High-Level Workflow

```
INPUT (2+ research docs) → PARSE → COMPARE → VERIFY → MERGE → OUTPUT (DOCX)
```

The five phases below must be executed in order. Each phase produces intermediate artifacts that feed the next.

---

## Phase 1: Parse & Inventory

Read all uploaded research documents and build a structured inventory.

### Supported input formats
- Markdown (.md, .txt)
- PDF (use the `pdf-reading` skill — rasterize + extract text)
- HTML (strip tags, preserve structure)
- Plain text pasted in chat

### Steps

1. Copy all uploaded files from `/mnt/user-data/uploads/` to `/home/claude/research-work/sources/`.
2. For each file, extract:
   - **Sections**: heading hierarchy, topic per section
   - **Claims**: factual assertions (numbers, dates, names, statistics, rankings)
   - **Sources/URLs**: every hyperlink or citation
   - **Unique insights**: points only this document makes
3. Save inventory as `/home/claude/research-work/inventory.json`:

```json
{
  "documents": [
    {
      "filename": "research_1.md",
      "sections": [{"heading": "...", "topic": "...", "claims": [...]}],
      "urls": [{"url": "...", "context": "...", "line": 42}],
      "unique_insights": ["..."]
    }
  ]
}
```

---

## Phase 2: Cross-Compare

Build a comparison matrix showing where documents agree, disagree, or have unique content.

### Steps

1. **Agreement check**: For each claim that appears in 2+ documents, note whether the facts match. Flag contradictions with both versions and source references.
2. **Coverage matrix**: Create a topic × document matrix showing which topics each doc covers and at what depth (none / brief / detailed).
3. **Quality ranking**: For each topic, identify which document has the best treatment (most detailed, best sourced, clearest explanation).
4. **Contradiction log**: List every factual disagreement with exact quotes from each source.

Save comparison to `/home/claude/research-work/comparison.json`.

Present a brief comparison summary to the user before proceeding — they may want to guide which document to prefer on contradictions.

---

## Phase 3: Verify

This is the most critical phase. Three layers of verification:

### Layer 1: Link Checking

Run the bundled scripts to extract and check every URL:

```bash
# Extract all URLs from source files
python /path/to/skill/scripts/extract_urls.py /home/claude/research-work/sources/* > /home/claude/research-work/urls.json

# Check all URLs
python /path/to/skill/scripts/check_links.py /home/claude/research-work/urls.json > /home/claude/research-work/link_results.json
```

Classify results:
- ✅ **Working** (HTTP 200): keep as-is
- ↗️ **Redirected** (3xx): update URL to final destination
- ❌ **Broken** (4xx/5xx/timeout): attempt to find replacement via web search, or remove
- ⚠️ **Paywalled / Soft-blocked**: note in final document

### Layer 2: Cross-Reference Facts

For claims that appear in only ONE document (no corroboration from other inputs):
1. Use `web_search` to verify. Search for the specific claim (name + number + date).
2. If confirmed by a reputable source, keep and add the confirming source as a citation.
3. If contradicted, flag and use the correct version.
4. If unverifiable (no search results either way), mark with a [⚠️ Unverified] tag and include it in a separate "Unverified Claims" appendix rather than the main body.

For claims in 2+ documents that agree: mark as verified (corroborated).
For claims in 2+ documents that contradict: use web search as tiebreaker.

### Layer 3: Source Quality Assessment

Rate each source/URL on a simple scale:
- **Tier 1**: Official sources (gov sites, company IR pages, peer-reviewed journals, major news outlets)
- **Tier 2**: Reputable secondary sources (well-known blogs, industry reports, Wikipedia with citations)
- **Tier 3**: Low-reliability (forums, undated pages, personal blogs without sources)

Prefer Tier 1 citations in the final document. Note Tier 3 sources explicitly.

Save full verification results to `/home/claude/research-work/verification.json`.

---

## Phase 4: Merge & Synthesize

Build the unified document by combining the best content from all sources.

### Merge Strategy

1. **Structure**: Use the best section structure from the comparison phase. If documents have different structures, create a new one that is logically organized by topic.
2. **Per section**: Take the best version (from quality ranking), then enrich with unique insights from other documents.
3. **Contradictions**: Use the verified/correct version. Note the disagreement in a footnote if relevant.
4. **Citations**: Every factual claim in the final document must have at least one working source link. Use inline citations: `[Source Name](URL)`.
5. **Unverified section**: Collect all unverifiable-but-potentially-useful claims in a clearly marked appendix.

### Document Structure

```
# [Topic Title]

## Executive Summary
Brief synthesis of key findings across all sources.

## [Main Sections — organized by topic]
Content with inline citations.

## Source Comparison Notes
Brief notes on where sources agreed/disagreed, which was used and why.

## Verified Sources
Numbered list of all working URLs used, with Tier ratings.

## Appendix: Unverified Claims
Claims that could not be confirmed or denied, with original source noted.

## Verification Report
- Total links checked: N
- Working: N (X%)
- Broken (removed/replaced): N
- Facts cross-referenced: N
- Facts verified via web search: N
- Contradictions resolved: N
```

---

## Phase 5: Generate DOCX Output

Use the `docx` skill (read `/mnt/skills/public/docx/SKILL.md`) to generate the final Word document.

The DOCX should include:
- Professional formatting with headings, table of contents
- Inline hyperlinks (only verified working URLs)
- Color-coded verification status where relevant (green = verified, yellow = single-source, red = unverified)
- Footer with generation date and source document list

Save final document to `/mnt/user-data/outputs/` and present via `present_files`.

---

## Communication with User

Throughout the process, keep the user informed:

1. **After Phase 1**: "I've parsed N documents. Here's what each covers: [brief summary]. Proceeding to compare."
2. **After Phase 2**: "Found X agreements, Y contradictions, Z unique insights. Here are the contradictions — which version do you prefer, or should I verify independently?" (Only ask if contradictions are significant.)
3. **After Phase 3**: "Verification complete: N/M links working, K facts confirmed via web search, J contradictions resolved. L claims unverifiable."
4. **After Phase 5**: Present the final DOCX.

If the user wants a quick result, compress phases 2-3 communication into a single status update.

---

## Edge Cases

- **Single document**: Still useful — run link checking and fact verification, produce a "verified edition."
- **Very large documents (>50 pages each)**: Process section-by-section rather than all at once. Prioritize executive summaries and key claims.
- **Non-English content**: Verify links and facts in the document's language. Use search queries in the appropriate language.
- **Documents on completely different topics**: Warn the user that merging may not make sense; offer to verify each independently instead.
