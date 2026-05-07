---
name: auto-deep-research
description: "Automatically orchestrates web search, raw web context, and deep research for requests to search, 查资料, 搜资料, 深度搜索, 调研, 文献综述, 找论文/资料/来源, look up, research, gather sources, compare current tools, or verify online claims. Use when the user asks for search/research without naming a specific search skill; it routes only through Brave spellcheck, autosuggest, web search, LLM context, and local report orchestration."
---

# Auto Deep Research

Use this as the default research router whenever the user asks to search or gather online/project资料, even if they do not name a specific search skill.

## Routing

1. **Clarify only if necessary**: if scope is too broad, ask one short question; otherwise choose sensible defaults.
2. **Quick lookup**: for a narrow fact or source list, run `scripts/brave_research.py web "<query>"` or `context`.
3. **Query optimization**: use spellcheck and autosuggest first to refine the query when helpful.
4. **Deep research**: for academic/project/tool comparison/current-state questions, run:
   ```bash
   python3 ~/.codex/skills/auto-deep-research/scripts/brave_research.py full "<query>" --language zh --max-queries 4
   ```
5. **Multiple existing reports**: use `research-orchestrator` after collecting or receiving 2+ research documents.

## Source discipline

- Prefer primary sources: official docs, papers, standards, government, reputable repos/issues.
- Separate **事实**, **推断**, and **未验证/未知**.
- For academic topics, prioritize papers, reviews, datasets, methods docs; avoid relying only on blogs.
- For current/latest/company/product/legal/medical/financial facts, verify with search before answering.
- Save artifacts; cite URLs in the final answer.

## Output format

Return concise Chinese output:

1. **结论摘要**
2. **关键来源**: title + URL + why it matters
3. **已确认事实 / 推断 / 不确定点**
4. **建议下一步**
5. **本次调研产物路径** if files were generated

## Environment

The script reads:

- `BRAVE_SEARCH_API_KEY` for `web-search` and `llm-context`
- `BRAVE_AUTOSUGGEST_API_KEY` for `suggest`
- `BRAVE_SPELLCHECK_API_KEY` for `spellcheck`

These can also be stored in `~/.codex/secrets/brave_search.env`.
