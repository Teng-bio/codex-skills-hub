#!/usr/bin/env python3
"""
Check all URLs extracted from research documents.
Input: JSON array of {"url": "...", "context": "...", "source_file": "..."} on stdin or as file arg.
Output: JSON with results for each URL.
"""
import json
import sys
import urllib.request
import urllib.error
import ssl
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Relaxed SSL for checking availability
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

TIMEOUT = 15
MAX_WORKERS = 10
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"


def check_url(entry):
    url = entry["url"].strip()
    result = {
        "url": url,
        "context": entry.get("context", ""),
        "source_file": entry.get("source_file", ""),
        "status": None,
        "ok": False,
        "error": None,
        "redirect_url": None,
        "title": None,
    }

    if not url.startswith(("http://", "https://")):
        result["error"] = "not_a_url"
        return result

    try:
        req = urllib.request.Request(url, method="GET", headers={"User-Agent": USER_AGENT})
        resp = urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx)
        result["status"] = resp.getcode()
        result["ok"] = 200 <= resp.getcode() < 400
        result["redirect_url"] = resp.geturl() if resp.geturl() != url else None
        # Try to get title from first 8KB
        try:
            head = resp.read(8192).decode("utf-8", errors="ignore")
            m = re.search(r"<title[^>]*>(.*?)</title>", head, re.IGNORECASE | re.DOTALL)
            if m:
                result["title"] = m.group(1).strip()[:200]
        except Exception:
            pass
    except urllib.error.HTTPError as e:
        result["status"] = e.code
        result["ok"] = False
        result["error"] = f"HTTP {e.code}"
    except urllib.error.URLError as e:
        result["error"] = str(e.reason)[:200]
    except Exception as e:
        result["error"] = str(e)[:200]

    return result


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            entries = json.load(f)
    else:
        entries = json.load(sys.stdin)

    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {pool.submit(check_url, e): e for e in entries}
        for fut in as_completed(futures):
            results.append(fut.result())

    # Sort: broken first
    results.sort(key=lambda r: (r["ok"], r["url"]))

    summary = {
        "total": len(results),
        "ok": sum(1 for r in results if r["ok"]),
        "broken": sum(1 for r in results if not r["ok"]),
        "results": results,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
