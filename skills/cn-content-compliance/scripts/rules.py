#!/usr/bin/env python3
"""cn-content-compliance: 列出指定行业/平台的完整规则.

Input:  "<industry>|<platform>"
Output: JSON {industry, platform, categories: {...}}
"""

from __future__ import annotations

from cli_common import (  # type: ignore[import-not-found]
    collect_categories,
    normalize_industry,
    normalize_platform,
    run_pipe_cli,
)


def export_rules(industry: str, platform: str) -> dict:
    industry = normalize_industry(industry)
    platform = normalize_platform(platform)
    categories = collect_categories(industry, platform)

    out_categories = {}
    for category_name, category_meta in categories:
        out_categories[category_name] = {
            "severity": category_meta.get("severity", "medium"),
            "law_ref": category_meta.get("law_ref", ""),
            "pattern_count": len(category_meta.get("patterns", [])),
            "patterns": category_meta.get("patterns", []),
        }

    return {
        "industry": industry,
        "platform": platform,
        "category_count": len(out_categories),
        "categories": out_categories,
    }


def main() -> int:
    return run_pipe_cli(
        "rules.py \"<industry>|<platform>\"",
        2,
        export_rules,
    )


if __name__ == "__main__":
    raise SystemExit(main())
