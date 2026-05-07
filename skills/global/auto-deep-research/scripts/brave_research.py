#!/usr/bin/env python3
"""Brave Search / LLM Context deep-research orchestrator."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

BASE = "https://api.search.brave.com/res/v1"
API_ENV_VARS = {
    "search": "BRAVE_SEARCH_API_KEY",
    "autosuggest": "BRAVE_AUTOSUGGEST_API_KEY",
    "spellcheck": "BRAVE_SPELLCHECK_API_KEY",
}


def load_api_key(kind: str = "search") -> str:
    env_var = API_ENV_VARS.get(kind, "BRAVE_SEARCH_API_KEY")
    key = os.environ.get(env_var, "").strip()
    if key:
        return key
    env_path = Path.home() / ".codex" / "secrets" / "brave_search.env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.startswith(env_var + "="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit(f"{env_var} not found in env or ~/.codex/secrets/brave_search.env")


def slugify(text: str, max_len: int = 48) -> str:
    s = re.sub(r"[^\w\u4e00-\u9fff.-]+", "-", text.strip(), flags=re.UNICODE).strip("-")
    return (s[:max_len] or "research")


def normalize_query(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def request_json(
    url: str,
    *,
    key_kind: str = "search",
    method: str = "GET",
    payload: dict[str, Any] | None = None,
    timeout: int = 60,
) -> dict[str, Any]:
    key = load_api_key(key_kind)
    data = None
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": key,
        "User-Agent": "codex-auto-deep-research/1.1",
    }
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return {"error": f"HTTP {e.code}", "body": body}
    except Exception as e:
        return {"error": type(e).__name__, "body": str(e)}


def web_search(query: str, count: int = 10, freshness: str | None = None, country: str = "US", lang: str = "en") -> dict[str, Any]:
    params = {
        "q": query,
        "count": str(max(1, min(count, 20))),
        "country": country,
        "search_lang": lang,
        "safesearch": "moderate",
        "extra_snippets": "true",
        "include_fetch_metadata": "true",
    }
    if freshness:
        params["freshness"] = freshness
    url = BASE + "/web/search?" + urllib.parse.urlencode(params)
    return request_json(url, key_kind="search", timeout=45)


def llm_context(query: str, count: int = 20, max_tokens: int = 8192, lang: str = "en") -> dict[str, Any]:
    params = {
        "q": query,
        "count": str(max(1, min(count, 50))),
        "search_lang": lang,
        "maximum_number_of_urls": str(max(1, min(count, 50))),
        "maximum_number_of_tokens": str(max(1024, min(max_tokens, 32768))),
        "context_threshold_mode": "balanced",
    }
    url = BASE + "/llm/context?" + urllib.parse.urlencode(params)
    return request_json(url, key_kind="search", timeout=90)


def spellcheck(query: str, country: str = "US") -> dict[str, Any]:
    params = {"q": query, "country": country}
    url = BASE + "/spellcheck/search?" + urllib.parse.urlencode(params)
    return request_json(url, key_kind="spellcheck", timeout=30)


def suggest(query: str, count: int = 5, country: str = "US", lang: str = "en", rich: bool = False) -> dict[str, Any]:
    params = {
        "q": query,
        "country": country,
        "lang": lang,
        "count": str(max(1, min(count, 20))),
        "rich": "true" if rich else "false",
    }
    url = BASE + "/suggest/search?" + urllib.parse.urlencode(params)
    return request_json(url, key_kind="autosuggest", timeout=30)


def extract_query_candidates(data: dict[str, Any]) -> list[str]:
    out: list[str] = []
    if not isinstance(data, dict):
        return out
    for item in data.get("results", []):
        if not isinstance(item, dict):
            continue
        for key in ("query", "text", "value", "suggestion"):
            value = item.get(key)
            if isinstance(value, str) and value.strip():
                out.append(normalize_query(value))
                break
    return out


def choose_corrected_query(original: str, spell_result: dict[str, Any]) -> str:
    original_n = normalize_query(original)
    for cand in extract_query_candidates(spell_result):
        if cand.lower() != original_n.lower():
            return cand
    return original_n


def build_query_bundle(original: str, corrected: str, suggest_result: dict[str, Any], max_queries: int = 4) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []

    def add(q: str) -> None:
        q = normalize_query(q)
        k = q.lower()
        if q and k not in seen:
            seen.add(k)
            out.append(q)

    add(corrected)
    add(original)
    for cand in extract_query_candidates(suggest_result):
        add(cand)
        if len(out) >= max_queries:
            break
    return out[:max_queries]


def top_web_results_multi(items: list[dict[str, Any]], limit: int = 12) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    seen: set[str] = set()
    for item in items:
        query = item.get("query", "")
        data = item.get("data", {})
        for r in data.get("web", {}).get("results", [])[:10]:
            url = r.get("url", "")
            if not url or url in seen:
                continue
            seen.add(url)
            out.append({
                "title": r.get("title", ""),
                "url": url,
                "description": r.get("description", ""),
                "age": r.get("age", ""),
                "query": query,
            })
            if len(out) >= limit:
                return out
    return out


def write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def run_full(args: argparse.Namespace) -> int:
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = Path(args.out or (Path.home() / ".codex" / "research" / f"{ts}-{slugify(args.query)}"))
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[0/4] spellcheck -> {out_dir/'spellcheck.json'}", file=sys.stderr)
    spell = spellcheck(args.query)
    write_json(out_dir / "spellcheck.json", spell)
    corrected_query = choose_corrected_query(args.query, spell)

    print(f"[1/4] autosuggest -> {out_dir/'suggest.json'}", file=sys.stderr)
    suggest_result = suggest(corrected_query, count=max(5, min(args.count, 8)), lang=args.search_lang)
    write_json(out_dir / "suggest.json", suggest_result)
    query_bundle = build_query_bundle(args.query, corrected_query, suggest_result, max_queries=max(1, min(args.max_queries, 8)))
    write_json(out_dir / "expanded_queries.json", {
        "original_query": args.query,
        "corrected_query": corrected_query,
        "queries": query_bundle,
    })

    print(f"[2/4] web-search -> {out_dir/'web_search.json'}", file=sys.stderr)
    web_results_by_query: list[dict[str, Any]] = []
    for query in query_bundle:
        web_results_by_query.append({
            "query": query,
            "data": web_search(query, count=args.count, freshness=args.freshness, lang=args.search_lang),
        })
    write_json(out_dir / "web_search.json", web_results_by_query)

    context_query = corrected_query or args.query
    print(f"[3/4] llm-context -> {out_dir/'llm_context.json'}", file=sys.stderr)
    ctx = llm_context(context_query, count=max(args.count, 10), max_tokens=args.max_context_tokens, lang=args.search_lang)
    write_json(out_dir / "llm_context.json", ctx)

    related = [q for q in query_bundle if q.lower() != context_query.lower()]

    meta = {
        "query": args.query,
        "created_at": dt.datetime.now().isoformat(timespec="seconds"),
        "language": args.language,
        "mode": "web_search_plus_llm_context",
        "corrected_query": corrected_query,
        "expanded_queries": query_bundle,
        "context_query": context_query,
        "related_query_angles": related[:3],
    }
    write_json(out_dir / "request.json", meta)

    sources = top_web_results_multi(web_results_by_query, limit=12)
    report_lines = [
        "# Deep Research Report\n",
        f"**Query:** {args.query}\n",
        f"**Created:** {meta['created_at']}\n",
        f"**Corrected Query:** {corrected_query}\n",
        "\n## Query Expansion\n",
    ]
    for i, q in enumerate(query_bundle, 1):
        report_lines.append(f"{i}. `{q}`")
    report_lines += ["\n## Top web sources\n"]
    for i, s in enumerate(sources, 1):
        report_lines.append(
            f"{i}. [{s['title']}]({s['url']}) — {s.get('description','')} "
            f"{('('+s.get('age','')+')') if s.get('age') else ''} "
            f"[from query: `{s.get('query','')}`]"
        )
    report_lines += [
        "\n## LLM context artifact\n",
        f"- Raw extracted context JSON: `{out_dir / 'llm_context.json'}`",
        "- Use the saved context plus top sources above for final synthesis; no external answer-generation API is called.",
        "\n## Artifact files\n",
    ]
    for name in [
        "request.json",
        "spellcheck.json",
        "suggest.json",
        "expanded_queries.json",
        "web_search.json",
        "llm_context.json",
    ]:
        report_lines.append(f"- `{out_dir / name}`")
    (out_dir / "report.md").write_text("\n".join(report_lines), encoding="utf-8")

    print(json.dumps({
        "out_dir": str(out_dir),
        "report": str(out_dir / "report.md"),
        "queries": query_bundle,
        "sources": sources,
    }, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Brave research orchestrator")
    sub = p.add_subparsers(dest="mode", required=True)

    for name in ["web", "context", "spellcheck", "suggest", "full"]:
        sp = sub.add_parser(name)
        sp.add_argument("query")
        sp.add_argument("--count", type=int, default=10)
        sp.add_argument("--freshness", default=None, help="pd/pw/pm/py or YYYY-MM-DDtoYYYY-MM-DD")
        sp.add_argument("--search-lang", default="en")

    sub.choices["context"].add_argument("--max-context-tokens", type=int, default=8192)
    sub.choices["suggest"].add_argument("--rich", action="store_true")

    full = sub.choices["full"]
    full.add_argument("--language", default="zh")
    full.add_argument("--iterations", type=int, default=None, help=argparse.SUPPRESS)  # deprecated, ignored
    full.add_argument("--seconds", type=int, default=None, help=argparse.SUPPRESS)  # deprecated, ignored
    full.add_argument("--max-queries", type=int, default=4, help="Maximum expanded query variants for web search")
    full.add_argument("--max-context-tokens", type=int, default=12000)
    full.add_argument("--out", default=None)

    args = p.parse_args()
    if args.mode == "web":
        print(json.dumps(web_search(args.query, args.count, args.freshness, lang=args.search_lang), ensure_ascii=False, indent=2))
        return 0
    if args.mode == "context":
        print(json.dumps(llm_context(args.query, args.count, args.max_context_tokens, lang=args.search_lang), ensure_ascii=False, indent=2))
        return 0
    if args.mode == "spellcheck":
        print(json.dumps(spellcheck(args.query), ensure_ascii=False, indent=2))
        return 0
    if args.mode == "suggest":
        print(json.dumps(suggest(args.query, args.count, lang=args.search_lang, rich=args.rich), ensure_ascii=False, indent=2))
        return 0
    if args.mode == "full":
        return run_full(args)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
