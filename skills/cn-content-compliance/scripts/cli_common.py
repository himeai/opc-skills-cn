#!/usr/bin/env python3
"""Shared CLI helpers for cn-content-compliance scripts."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Callable


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run_pipe_cli(
    usage: str,
    expected_fields: int,
    builder: Callable[..., dict],
) -> int:
    """Parse '|'-separated argv[1] into N fields, run builder, print JSON."""
    if len(sys.argv) != 2:
        print(f"usage: {usage}", file=sys.stderr)
        return 1
    parts = sys.argv[1].split("|")
    if len(parts) != expected_fields:
        print(
            f"error: expected {expected_fields} '|'-separated fields",
            file=sys.stderr,
        )
        return 1
    fields = [part.strip() for part in parts]

    try:
        result = builder(*fields)
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False))
    return 0


ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = ROOT / "references" / "rules.json"

INDUSTRY_CATEGORIES = {
    "general": [],
    "medical": ["ad_law_medical"],
    "cosmetics": ["cosmetics", "ad_law_medical"],
    "food": ["food", "ad_law_medical"],
    "finance": ["finance"],
    "education": ["education"],
}

ALL_PLATFORMS = {"xiaohongshu", "douyin", "bilibili", "wechat_mp", "kuaishou"}

SEVERITY_ORDER = {"low": 1, "medium": 2, "high": 3}


def normalize_industry(industry: str) -> str:
    return industry if industry in INDUSTRY_CATEGORIES else "general"


def normalize_platform(platform: str) -> str:
    return platform if platform in ALL_PLATFORMS or platform == "general" else "general"


def collect_categories(industry: str, platform: str) -> list[tuple[str, dict]]:
    """Return list of (category_name, category_meta) applicable to industry+platform."""
    rules = load_json(RULES_PATH)
    industry = normalize_industry(industry)
    platform = normalize_platform(platform)

    selected: list[tuple[str, dict]] = []
    # Always include general ad-law categories
    for key in ("ad_law_extreme", "ad_law_misleading"):
        if key in rules:
            selected.append((key, rules[key]))
    # Industry-specific categories
    for key in INDUSTRY_CATEGORIES.get(industry, []):
        if key in rules:
            selected.append((key, rules[key]))
    # Platform-specific category
    if platform != "general":
        platform_meta = rules.get("platforms", {}).get(platform)
        if platform_meta:
            selected.append((f"platform:{platform}", platform_meta))
    return selected
