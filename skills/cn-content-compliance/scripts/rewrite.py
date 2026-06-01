#!/usr/bin/env python3
"""cn-content-compliance: 把命中的违禁词替换为合规改写建议.

Input:  "<text>|<industry>|<platform>"
Output: JSON {original, rewritten, changes: [{from, to, category}]}
"""

from __future__ import annotations

from cli_common import (  # type: ignore[import-not-found]
    RULES_PATH,
    collect_categories,
    load_json,
    normalize_industry,
    normalize_platform,
    run_pipe_cli,
)


def rewrite_text(text: str, industry: str, platform: str) -> dict:
    industry = normalize_industry(industry)
    platform = normalize_platform(platform)
    rules = load_json(RULES_PATH)
    hints: dict[str, str] = rules.get("rewrite_hints", {})

    categories = collect_categories(industry, platform)
    # Sort phrases by length desc to avoid partial overlap
    candidates: list[tuple[str, str]] = []
    for category_name, category_meta in categories:
        for phrase in category_meta.get("patterns", []):
            candidates.append((phrase, category_name))
    candidates.sort(key=lambda item: -len(item[0]))

    rewritten = text
    changes = []
    seen: set[str] = set()
    for phrase, category_name in candidates:
        if phrase in seen or phrase not in rewritten:
            continue
        seen.add(phrase)
        replacement = hints.get(phrase)
        if replacement is None:
            changes.append({
                "from": phrase,
                "to": None,
                "category": category_name,
                "note": "未提供改写建议，建议人工删除或重写",
            })
            continue
        rewritten = rewritten.replace(phrase, replacement)
        changes.append({
            "from": phrase,
            "to": replacement,
            "category": category_name,
            "note": "已按 rewrite_hints 自动替换",
        })

    return {
        "industry": industry,
        "platform": platform,
        "original": text,
        "rewritten": rewritten,
        "changes": changes,
    }


def main() -> int:
    return run_pipe_cli(
        "rewrite.py \"<text>|<industry>|<platform>\"",
        3,
        rewrite_text,
    )


if __name__ == "__main__":
    raise SystemExit(main())
