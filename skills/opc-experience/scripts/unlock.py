#!/usr/bin/env python3
"""unlock.py — 按预算 / 体能 / 类别 / 年龄筛选可解锁体验。

input format:
  budget_cny=500w|fitness=4|categories=极地探险,极速极限,飞行航天|age=35|max_lead_months=24
"""

from __future__ import annotations

import json
import sys

from common import DISCLAIMER, load_ref, parse_kv, parse_int_cny, parse_list


def unlock(input_str: str) -> dict:
    fields = parse_kv(input_str)
    budget = parse_int_cny(fields.get("budget_cny", "1000w"))
    fitness = int(fields.get("fitness", "3"))
    categories = parse_list(fields.get("categories", ""))
    age = int(fields.get("age", "35"))
    max_lead = int(fields.get("max_lead_months", "60"))

    ref = load_ref("experiences.json")
    matched = []
    for e in ref["experiences"]:
        if e["price_cny_min"] > budget:
            continue
        if e["fitness"] > fitness:
            continue
        if categories and e["category"] not in categories:
            continue
        lo, hi = e["age_window"]
        if age < lo or age > hi:
            continue
        if e["lead_months"] > max_lead:
            continue
        if not e.get("bookable_now", True):
            continue
        matched.append(e)

    matched.sort(key=lambda e: (e["price_cny_min"], e["lead_months"]))

    by_cat: dict[str, list[dict]] = {}
    for m in matched:
        by_cat.setdefault(m["category"], []).append({
            "id": m["id"],
            "name": m["name"],
            "tier": m["tier"],
            "price_cny_range": [m["price_cny_min"], m["price_cny_max"]],
            "lead_months": m["lead_months"],
            "fitness": m["fitness"],
            "season": m.get("season", "全年"),
            "highlights": m.get("highlights", []),
        })

    return {
        "input": fields,
        "budget_cny": budget,
        "your_fitness": fitness,
        "matched_count": len(matched),
        "by_category": by_cat,
        "tier_legend": ref["tier_legend"],
        "fitness_legend": ref["fitness_legend"],
        "warnings": [
            "高净值体验不等于安全。Titan 深潜 / 珠峰拥堵 / F1 赛道事故均有先例",
            "极限项目必须提前办高额医疗 + 救援保险（含直升机 / 医疗后送）",
            "65 岁以上参与高山 / 高反 / 离心机 4G 项目必须医师签字",
        ],
        "disclaimer": DISCLAIMER,
    }


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: unlock.py 'budget_cny=...|fitness=1..5|categories=...|age=...|max_lead_months=...'", file=sys.stderr)
        return 2
    try:
        out = unlock(sys.argv[1])
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
