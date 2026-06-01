#!/usr/bin/env python3
"""budget.py — 单次行程或环球预算估算（4 档）。

input format:
  cities=巴黎,罗马,巴塞罗那|days=20|tier=business
"""

from __future__ import annotations

import json
import sys

from common import DISCLAIMER, load_ref, parse_kv, parse_int, parse_list


def estimate(input_str: str) -> dict:
    fields = parse_kv(input_str)
    cities = parse_list(fields.get("cities", ""))
    days = parse_int(fields.get("days", "0"))
    tier = fields.get("tier", "comfort")

    dests_ref = load_ref("destinations.json")
    budgets_ref = load_ref("budgets.json")

    matched = [d for d in dests_ref["destinations"] if d["city"] in cities]
    if not matched and cities:
        return {
            "error": "未匹配到任何 city；请检查拼写或参考 destinations.json",
            "cities_input": cities,
            "disclaimer": DISCLAIMER,
        }

    tier_def = next((t for t in budgets_ref["tiers"] if t["tier_en"] == tier), budgets_ref["tiers"][1])
    multiplier = tier_def["daily_multiplier"]

    # 没指定 days 则按 stay_days_recommended 求和
    if days <= 0:
        days = sum(d.get("stay_days_recommended", 3) for d in matched) or 14

    # 平均日预算
    if matched:
        avg_daily_mid = sum(d.get("avg_daily_cny_mid", 1000) for d in matched) / len(matched)
    else:
        avg_daily_mid = 1200
    daily_cost = int(avg_daily_mid * multiplier)
    lodging_food = daily_cost * days

    flight_cny = tier_def["intl_flight_cny_round"]
    insurance = int(budgets_ref["auxiliary_costs"]["insurance_cny_per_month"][tier_def["tier_en"]] * (days / 30))
    countries = {d["country"] for d in matched}
    visa = budgets_ref["auxiliary_costs"]["visa_avg_cny_per_country"] * len(countries)
    contingency = int((lodging_food + flight_cny) * 0.15)
    total = lodging_food + flight_cny + insurance + visa + contingency

    return {
        "tier": tier_def["tier"],
        "tier_remark": tier_def["tier_remark"],
        "lodging_style": tier_def["lodging"],
        "transport_style": tier_def["transport"],
        "food_style": tier_def["food"],
        "experience_style": tier_def["experience"],
        "cities": cities,
        "countries_count": len(countries),
        "days": days,
        "daily_cost_cny": daily_cost,
        "breakdown_cny": {
            "lodging_food_local": lodging_food,
            "intl_flight": flight_cny,
            "insurance": insurance,
            "visa": visa,
            "contingency_15pct": contingency,
        },
        "total_cny": total,
        "per_person_per_day_cny": int(total / max(days, 1)),
        "tips": budgets_ref["tips"],
        "disclaimer": DISCLAIMER,
    }


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: budget.py 'cities=...|days=...|tier=shoestring/comfort/business/luxury'", file=sys.stderr)
        return 2
    try:
        out = estimate(sys.argv[1])
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
