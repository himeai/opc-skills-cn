#!/usr/bin/env python3
"""cn-content-compliance: 扫描文案命中的违禁词.

Input:  "<text>|<industry>|<platform>"
Output: JSON {summary: {total_hits, highest_severity}, hits: [...]}
"""

from __future__ import annotations

from cli_common import (  # type: ignore[import-not-found]
    SEVERITY_ORDER,
    collect_categories,
    normalize_industry,
    normalize_platform,
    run_pipe_cli,
)


def scan_text(text: str, industry: str, platform: str) -> dict:
    industry = normalize_industry(industry)
    platform = normalize_platform(platform)
    categories = collect_categories(industry, platform)

    hits = []
    for category_name, category_meta in categories:
        severity = category_meta.get("severity", "medium")
        law_ref = category_meta.get("law_ref", "")
        for phrase in category_meta.get("patterns", []):
            idx = 0
            while True:
                pos = text.find(phrase, idx)
                if pos < 0:
                    break
                hits.append({
                    "phrase": phrase,
                    "position": pos,
                    "category": category_name,
                    "severity": severity,
                    "law_ref": law_ref,
                })
                idx = pos + len(phrase)

    highest = "none"
    for hit in hits:
        if SEVERITY_ORDER.get(hit["severity"], 0) > SEVERITY_ORDER.get(highest, 0):
            highest = hit["severity"]

    return {
        "text": text,
        "industry": industry,
        "platform": platform,
        "summary": {
            "total_hits": len(hits),
            "highest_severity": highest,
        },
        "hits": hits,
    }


def main() -> int:
    return run_pipe_cli(
        "check.py \"<text>|<industry>|<platform>\"",
        3,
        scan_text,
    )


if __name__ == "__main__":
    raise SystemExit(main())
