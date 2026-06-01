#!/usr/bin/env python3
"""xiaohongshu-ops: 关键词矩阵.

Input:  "<product_or_word>|<industry>"
Output: JSON {core, long_tail, tags}
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SEEDS_PATH = ROOT / "references" / "keyword_seeds.json"


def _load_seeds() -> dict:
    return json.loads(SEEDS_PATH.read_text(encoding="utf-8"))


def build_keywords(product: str, industry: str) -> dict:
    seeds = _load_seeds().get("industries", {})
    industry_meta = seeds.get(industry, {})

    core = list(dict.fromkeys([product] + industry_meta.get("core", [])))
    long_tail_base = industry_meta.get("long_tail", [])
    long_tail = [f"{product} {kw}" if product and kw not in product else kw
                 for kw in long_tail_base]
    tags = industry_meta.get("tags", [])

    return {
        "product": product,
        "industry": industry,
        "core": core,
        "long_tail": long_tail,
        "tags": tags,
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: keywords.py \"<product>|<industry>\"", file=sys.stderr)
        return 1
    parts = sys.argv[1].split("|")
    if len(parts) != 2:
        print("error: expected 2 '|'-separated fields", file=sys.stderr)
        return 1
    product, industry = (part.strip() for part in parts)

    try:
        result = build_keywords(product, industry)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
