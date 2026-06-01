#!/usr/bin/env python3
"""opc-property cn_city: 国内城市豪宅 7 维加权评分.

Input: budget_cny=3000w|priority=学区
Output: ranked cities + 顶级楼盘清单
"""

from __future__ import annotations

import json
import sys

from common import DISCLAIMER, load_ref, parse_int_cny, parse_kv


def cn_city(fields: dict[str, str]) -> dict:
    budget_cny = parse_int_cny(fields.get("budget_cny", "2000w"))
    priority = fields.get("priority", "")  # 学区/流动性/文化/性价比/气候

    data = load_ref("cn_cities.json")
    weights = dict(data["weights"])
    if priority == "学区":
        weights["school_district"] += 0.15
    elif priority == "流动性":
        weights["liquidity"] += 0.15
    elif priority == "文化":
        weights["culture_brand"] += 0.15
    elif priority == "性价比":
        weights["holding_cost_low"] += 0.10
        weights["rental_yield"] += 0.05
    elif priority == "气候":
        weights["culture_brand"] += 0.05
    total_w = sum(weights.values())
    weights = {k: v / total_w for k, v in weights.items()}

    ranked = []
    for c in data["cities"]:
        score = sum(c["scores"][k] * weights[k] for k in weights)
        ranked.append({
            "city": c["name"],
            "weighted_score": round(score, 3),
            "headline": c["headline"],
            "buyer_fit": c["buyer_fit"],
            "raw_scores": c["scores"],
        })
    ranked.sort(key=lambda x: x["weighted_score"], reverse=True)

    cn_pool = load_ref("cn_premium_properties.json")
    top_props_by_city: dict[str, list[dict]] = {}
    for tier_key in ("S", "A", "B"):
        tier_obj = cn_pool.get(f"tier_{tier_key}", {})
        for p in tier_obj.get("properties", []):
            if budget_cny < p["typical_total_cny_range"][0]:
                continue
            top_props_by_city.setdefault(p["city"], []).append({
                "tier": tier_key,
                "name": p["name"],
                "district": p["district"],
                "type": p.get("type", ""),
                "highlights": p.get("highlights", []),
                "typical_total_cny_range": p["typical_total_cny_range"],
            })

    for r in ranked:
        r["matching_properties"] = top_props_by_city.get(r["city"], [])

    return {
        "input": {"budget_cny": budget_cny, "priority": priority},
        "weights_normalized": {k: round(v, 3) for k, v in weights.items()},
        "ranked": ranked,
        "tips": [
            "Top 3 城市优先；同分用「成交流动性」和「学区」做 tie-breaker",
            "若预算只够 B 级，建议聚焦三亚 / 苏州 / 大理 / 厦门 旅居型资产",
            "学区房需结合最新学区划片政策，规则每年 6 月可能调整",
        ],
        "disclaimer": DISCLAIMER,
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: cn_city.py 'budget_cny=3000w|priority=学区'", file=sys.stderr)
        return 1
    try:
        fields = parse_kv(sys.argv[1].strip())
        result = cn_city(fields)
    except (OSError, json.JSONDecodeError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
