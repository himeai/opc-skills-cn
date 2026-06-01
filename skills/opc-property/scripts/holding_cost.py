#!/usr/bin/env python3
"""opc-property holding_cost: 5 年持有成本测算（一次性税 + 年度税 + 物业 + 净租金 + 退出税）.

Input: city=纽约|total_cny=5000w|hold_years=5|rent_out=yes
Output: JSON 各项金额 + 净持有成本 + 隐含年化
"""

from __future__ import annotations

import json
import sys

from common import DISCLAIMER, load_ref, parse_int_cny, parse_kv


def estimate(fields: dict[str, str]) -> dict:
    city = fields.get("city", "上海")
    total_cny = parse_int_cny(fields.get("total_cny", "1000w"))
    hold_years = int(fields.get("hold_years", "5"))
    rent_out = fields.get("rent_out", "no").lower() in ("y", "yes", "true", "1")

    data = load_ref("holding_costs.json")
    params = data["city_params"].get(city, data["default_params"])

    transaction_tax = total_cny * params["transaction_tax_pct"] / 100
    annual_property_tax = total_cny * params["annual_property_tax_pct"] / 100
    annual_management = total_cny * params["annual_management_pct"] / 100

    if rent_out:
        gross_rent = total_cny * params["rental_yield_pct"] / 100
        net_rent = gross_rent * (1 - params["income_tax_on_rent_pct"] / 100)
    else:
        gross_rent = 0
        net_rent = 0

    yearly_holding = annual_property_tax + annual_management - net_rent
    total_holding = transaction_tax + yearly_holding * hold_years
    exit_tax_on_principal = total_cny * params["exit_tax_pct"] / 100
    full_cycle_cost = total_holding + exit_tax_on_principal

    implied_break_even_appreciation_pct = round(full_cycle_cost / total_cny / hold_years * 100, 2)

    return {
        "input": {
            "city": city,
            "total_cny": total_cny,
            "hold_years": hold_years,
            "rent_out": rent_out,
        },
        "params_used": params,
        "one_time": {
            "transaction_tax_cny": round(transaction_tax),
            "transaction_tax_pct": params["transaction_tax_pct"],
        },
        "annual": {
            "property_tax_cny": round(annual_property_tax),
            "management_cny": round(annual_management),
            "gross_rent_cny": round(gross_rent),
            "net_rent_cny": round(net_rent),
            "net_holding_cost_cny": round(yearly_holding),
        },
        "five_year_summary": {
            "total_holding_cny": round(total_holding),
            "exit_tax_on_principal_cny": round(exit_tax_on_principal),
            "full_cycle_cost_cny": round(full_cycle_cost),
            "implied_break_even_annual_appreciation_pct": implied_break_even_appreciation_pct,
        },
        "interpretation": [
            f"{city} 持有 {hold_years} 年总成本约 ¥{round(full_cycle_cost):,}（含进出场税与物业 / 净租金调整后）",
            f"年化升值 ≥ {implied_break_even_appreciation_pct}% 才能覆盖持有成本",
            "数据为本地静态参数，实际以税务师 / 评估师测算为准",
        ],
        "tips": data["tips"],
        "disclaimer": DISCLAIMER,
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(
            "usage: holding_cost.py 'city=纽约|total_cny=5000w|hold_years=5|rent_out=yes'",
            file=sys.stderr,
        )
        return 1
    try:
        fields = parse_kv(sys.argv[1].strip())
        result = estimate(fields)
    except (OSError, json.JSONDecodeError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
