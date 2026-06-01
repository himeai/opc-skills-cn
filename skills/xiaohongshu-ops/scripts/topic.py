#!/usr/bin/env python3
"""xiaohongshu-ops: 选题工厂.

Input:  "<industry>|<audience>|<niche>"
Output: JSON {topics: [{title, angle, hook_type}, ...]}
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SEEDS_PATH = ROOT / "references" / "topic_seeds.json"


def _load_seeds() -> dict:
    return json.loads(SEEDS_PATH.read_text(encoding="utf-8"))


def _industry_meta(seeds: dict, industry: str) -> dict:
    meta = seeds.get("industries", {}).get(industry)
    if meta:
        return meta
    return {
        "default_pain": "选不对",
        "category": industry or "好物",
        "benchmark": "高端产品",
        "metric": "效果",
        "duration": "一段时间",
    }


def _format_hook(template: str, ctx: dict) -> str:
    out = template
    for key, value in ctx.items():
        out = out.replace("{" + key + "}", str(value))
    return out


def generate(industry: str, audience: str, niche: str) -> list[dict]:
    seeds = _load_seeds()
    angles = seeds.get("angles", [])
    meta = _industry_meta(seeds, industry)

    ctx = {
        "audience": audience or "你",
        "pain": meta["default_pain"],
        "category": niche or meta["category"],
        "benchmark": meta["benchmark"],
        "metric": meta["metric"],
        "duration": meta["duration"],
        "n": "5",
        "budget": "100",
        "popular": "网红同款",
        "action": f"做{niche or meta['category']}",
        "result": f"提升{meta['metric']}",
        "role": audience or "主理人",
    }

    topics = []
    for angle in angles:
        topics.append({
            "title": _format_hook(angle["hook"], ctx),
            "angle": angle["name"],
            "hook_type": angle["id"],
        })
    return topics


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: topic.py \"<industry>|<audience>|<niche>\"", file=sys.stderr)
        return 1
    parts = sys.argv[1].split("|")
    if len(parts) != 3:
        print("error: expected 3 '|'-separated fields", file=sys.stderr)
        return 1
    industry, audience, niche = (part.strip() for part in parts)

    try:
        topics = generate(industry, audience, niche)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(
        {"industry": industry, "audience": audience, "niche": niche, "topics": topics},
        ensure_ascii=False,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
