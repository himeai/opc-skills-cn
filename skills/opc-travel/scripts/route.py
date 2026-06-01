#!/usr/bin/env python3
"""route.py — 按主题 / 时长 / 预算 / 出发月份生成环球路线。

input format:
  themes=自然,海岛|months=45|start_month=4|tier=comfort|continents=亚洲,欧洲,北美

输出：
  - 推荐路线（按建议天数 + 大洲走法 + 季节匹配）
  - 总预算估算（机票 + 食宿 + 体验 + 保险 + 应急）
  - 半球切换提示
"""

from __future__ import annotations

import json
import sys

from common import DISCLAIMER, load_ref, parse_kv, parse_int, parse_list


def score_destination(dest: dict, themes: list[str], start_month: int, total_months: int, continents: list[str]) -> float:
    score = 0.0
    if themes:
        overlap = len(set(dest.get("themes", [])) & set(themes))
        score += overlap * 3.0
    if continents and dest.get("continent") not in continents:
        return -1.0
    best_months = dest.get("best_months", [])
    if best_months:
        # 行程任意月份命中 best_months 即加分（按 stay_days 估算月份覆盖）
        cur = start_month
        days_left = int(total_months)
        hit = False
        while days_left > 0:
            if cur in best_months:
                hit = True
                break
            cur = cur % 12 + 1
            days_left -= 30
        if hit:
            score += 2.0
        else:
            score -= 1.0
    return score


def build_route(input_str: str) -> dict:
    fields = parse_kv(input_str)
    themes = parse_list(fields.get("themes", ""))
    days = parse_int(fields.get("days", "30"))
    start_month = int(fields.get("start_month", "4"))
    tier = fields.get("tier", "comfort")
    continents = parse_list(fields.get("continents", ""))

    dests_ref = load_ref("destinations.json")
    budgets_ref = load_ref("budgets.json")

    candidates = []
    for d in dests_ref["destinations"]:
        s = score_destination(d, themes, start_month, days, continents)
        if s < 0:
            continue
        candidates.append((s, d))
    candidates.sort(key=lambda x: -x[0])

    # 选直到塞满 days
    selected = []
    used_days = 0
    for s, d in candidates:
        stay = d.get("stay_days_recommended", 3)
        if used_days + stay > days:
            continue
        selected.append({
            "city": d["city"],
            "country": d["country"],
            "continent": d["continent"],
            "stay_days": stay,
            "themes": d.get("themes", []),
            "best_months": d.get("best_months", []),
            "highlights": d.get("highlights", []),
            "avg_daily_cny_mid": d.get("avg_daily_cny_mid", 1000),
        })
        used_days += stay
        if used_days >= days:
            break

    # 预算
    tier_def = next((t for t in budgets_ref["tiers"] if t["tier_en"] == tier), budgets_ref["tiers"][1])
    multiplier = tier_def["daily_multiplier"]
    daily_total = sum(int(s["avg_daily_cny_mid"] * multiplier * s["stay_days"]) for s in selected)
    flight_cny = tier_def["intl_flight_cny_round"]
    insurance_cny = budgets_ref["auxiliary_costs"]["insurance_cny_per_month"][tier_def["tier_en"]] * (days / 30)
    visa_cny = budgets_ref["auxiliary_costs"]["visa_avg_cny_per_country"] * len({s["country"] for s in selected})
    contingency_cny = int((daily_total + flight_cny) * 0.15)
    total_cny = int(daily_total + flight_cny + insurance_cny + visa_cny + contingency_cny)

    # 大洲分组
    by_continent: dict[str, list[str]] = {}
    for s in selected:
        by_continent.setdefault(s["continent"], []).append(s["city"])

    return {
        "input": fields,
        "tier": tier_def["tier"],
        "tier_remark": tier_def["tier_remark"],
        "total_days": days,
        "used_days": used_days,
        "stops": selected,
        "stops_count": len(selected),
        "by_continent": by_continent,
        "budget_breakdown_cny": {
            "lodging_food_local": daily_total,
            "intl_flight": flight_cny,
            "insurance": int(insurance_cny),
            "visa_estimate": visa_cny,
            "contingency_15pct": contingency_cny,
        },
        "total_cny": total_cny,
        "tips": [
            "环球路线建议每 6 周回家一次以避免疲劳",
            "时差 ≥ 8h 建议中转地停 1-2 晚倒时差",
            f"出发月 {start_month} 月，已按目的地最佳季节排序",
        ],
        "disclaimer": DISCLAIMER,
    }


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: route.py 'themes=...|days=...|start_month=...|tier=shoestring/comfort/business/luxury|continents=...'", file=sys.stderr)
        return 2
    try:
        out = build_route(sys.argv[1])
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
