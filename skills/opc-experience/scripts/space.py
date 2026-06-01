#!/usr/bin/env python3
"""space.py — 太空旅行（去太空）专项查询。

input format:
  tier=suborbital  # 或 orbital / lunar_deepspace / all
  budget_cny=500w  # 可选，过滤
"""

from __future__ import annotations

import json
import sys

from common import DISCLAIMER, load_ref, parse_kv, parse_int_cny


def query(input_str: str) -> dict:
    fields = parse_kv(input_str)
    tier = fields.get("tier", "all")
    budget = parse_int_cny(fields.get("budget_cny", "0")) if fields.get("budget_cny") else None

    ref = load_ref("space_travel.json")

    tiers = ref["tiers"]
    providers = ref["providers"]

    if tier != "all":
        tiers = [t for t in tiers if t["tier_en"] == tier]
        providers = [p for p in providers if (
            (tier == "suborbital" and p["tier"] == "亚轨道")
            or (tier == "orbital" and p["tier"] == "轨道级")
            or (tier == "lunar_deepspace" and p["tier"] == "月球级 / 深空")
        )]

    if budget:
        providers = [p for p in providers if p.get("fee_cny_est", 999_999_999_999) <= budget]

    return {
        "tier_filter": tier,
        "budget_cny_filter": budget,
        "tiers": tiers,
        "providers": providers,
        "decision_checklist": ref["checklist_decision"],
        "regulatory_notes": ref["regulatory_notes"],
        "warnings": ref["warnings"],
        "summary_for_chinese_buyer": [
            "亚轨道（90-100 km，失重 4 分钟）：Virgin Galactic 票价 60 万 USD，约 435 万 CNY；Blue Origin 拍卖 / 邀约制",
            "轨道级（绕地球 ISS 10 天）：Axiom × SpaceX 单座 5500 万 USD，约 4 亿 CNY",
            "月球级（深空环月）：dearMoon 项目重组中，10 亿 CNY+",
            "所有跨境支付必须走合规渠道：每年 5 万美元购汇 + 境外资产长期积累 + 持牌私行 ODI；任何「换汇 / 蚂蚁搬家 / 地下钱庄」都是违法",
        ],
        "disclaimer": DISCLAIMER,
    }


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: space.py 'tier=suborbital|orbital|lunar_deepspace|all|budget_cny=...'", file=sys.stderr)
        return 2
    try:
        out = query(sys.argv[1])
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
