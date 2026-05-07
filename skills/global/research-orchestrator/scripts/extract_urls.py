#!/usr/bin/env python3
"""
Extract all URLs from text/markdown files with surrounding context.
Usage: python extract_urls.py file1.md file2.txt ...
Output: JSON array of {url, context, source_file, line_number}
"""
import json
import re
import sys

URL_RE = re.compile(
    r'https?://[^\s\)\]\}\>"\'`,;]+',
    re.IGNORECASE
)

# Clean trailing punctuation that's not part of URL
TRAIL_RE = re.compile(r'[.\)\]\},;:!?\'"]+$')


def extract_from_file(filepath):
    results = []
    try:
        with open(filepath, encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except Exception as e:
        return [{"error": str(e), "source_file": filepath}]

    for i, line in enumerate(lines, 1):
        for m in URL_RE.finditer(line):
            url = TRAIL_RE.sub("", m.group(0))
            # Get context: surrounding text
            start = max(0, m.start() - 80)
            end = min(len(line), m.end() + 80)
            context = line[start:end].strip()
            results.append({
                "url": url,
                "context": context,
                "source_file": filepath,
                "line_number": i,
            })
    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_urls.py file1.md file2.txt ...", file=sys.stderr)
        sys.exit(1)

    all_urls = []
    seen = set()
    for fp in sys.argv[1:]:
        for entry in extract_from_file(fp):
            if "error" in entry:
                all_urls.append(entry)
                continue
            if entry["url"] not in seen:
                seen.add(entry["url"])
                all_urls.append(entry)

    print(json.dumps(all_urls, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
