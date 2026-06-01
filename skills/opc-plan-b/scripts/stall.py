#!/usr/bin/env python3
"""opc-plan-b: 摆摊选品 ROI + 城市政策 + 备案路径.

Input (`|` 分隔，`=` 键值):
  city=成都|budget_cny=3000|category=小吃热食|night_or_day=night

Output: JSON {city_policy, category_picks, roi_estimate, license_required, equipment, warnings}
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "references" / "stall_policies.json"


def _load() -> dict:
    return json.loads(TEMPLATES.read_text(encoding="utf-8"))


def _parse_kv(raw: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for chunk in raw.split("|"):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "=" not in chunk:
            raise ValueError(f"bad field '{chunk}'")
        key, value = chunk.split("=", 1)
        fields[key.strip()] = value.strip()
    return fields


def _resolve_category(key: str, categories: dict) -> str:
    if key in categories:
        return key
    for ck in categories:
        if key in ck or ck in key:
            return ck
    return next(iter(categories))


def _estimate_roi(cat: dict, budget: float, daily_orders: int) -> dict:
    avg_price = (cat["selling_price_cny"][0] + cat["selling_price_cny"][1]) / 2
    avg_cost = (cat["ingredients_cost_per_unit_cny"][0] + cat["ingredients_cost_per_unit_cny"][1]) / 2
    daily_revenue = avg_price * daily_orders
    daily_cogs = avg_cost * daily_orders
    daily_gross = daily_revenue - daily_cogs
    monthly_gross = daily_gross * 25
    payback_days = round(budget / daily_gross, 1) if daily_gross > 0 else None
    return {
        "avg_price_cny": round(avg_price, 1),
        "avg_unit_cogs_cny": round(avg_cost, 1),
        "daily_orders_assumed": daily_orders,
        "daily_revenue_cny": round(daily_revenue),
        "daily_gross_cny": round(daily_gross),
        "monthly_gross_cny_25_days": round(monthly_gross),
        "payback_days_for_startup_cost": payback_days,
        "note": "未扣摊位费 / 通勤 / 损耗 / 个人时薪机会成本，仅看毛利",
    }


def build_stall(fields: dict[str, str]) -> dict:
    data = _load()
    city = fields.get("city", "成都")
    if city not in data["cities"]:
        for ck in data["cities"]:
            if city in ck or ck in city:
                city = ck
                break
        else:
            city = "成都"
    city_policy = data["cities"][city]

    cat_input = fields.get("category", "小吃热食")
    cat_key = _resolve_category(cat_input, data["categories"])
    category = data["categories"][cat_key]

    try:
        budget = float(fields.get("budget_cny", "3000"))
    except ValueError as exc:
        raise ValueError(f"bad budget_cny: {exc}") from exc

    daily_orders_low = category["daily_orders_typical"][0]
    daily_orders_mid = (category["daily_orders_typical"][0] + category["daily_orders_typical"][1]) // 2

    roi_low = _estimate_roi(category, budget, daily_orders_low)
    roi_mid = _estimate_roi(category, budget, daily_orders_mid)

    suggest_picks = list(category["examples"])[:4]

    equipment = ["折叠摊位 / 推车", "灯具 + 充电宝", "收款码 + 备用现金", "雨布 / 遮阳伞"]
    if "热食" in cat_key or "小吃" in cat_key:
        equipment.extend(["不锈钢操作台", "煤气罐 / 电磁炉", "餐厨垃圾袋 + 餐厨垃圾签约"])
    if "饮品" in cat_key:
        equipment.extend(["保温桶 / 制冰机", "搅拌器", "一次性杯具"])

    in_budget = budget >= category["startup_cost_cny"][0]
    budget_note = (
        f"你的预算 {int(budget)} 元 在该品类起步成本区间 "
        f"{category['startup_cost_cny'][0]}-{category['startup_cost_cny'][1]} 元 "
        f"内（{'OK' if in_budget else '不足，建议下调品类或增加预算'}）"
    )

    return {
        "city": city,
        "city_policy": city_policy,
        "category": cat_key,
        "category_overview": category,
        "suggested_picks": suggest_picks,
        "budget_check": {
            "user_budget_cny": int(budget),
            "category_startup_cost_cny": category["startup_cost_cny"],
            "in_budget": in_budget,
            "note": budget_note,
        },
        "roi_estimate_low": roi_low,
        "roi_estimate_mid": roi_mid,
        "equipment_checklist": equipment,
        "license_required": list(category["license_required"]),
        "general_warnings": list(data["general_warnings"]),
        "disclaimer": "本数据仅作选品起点；最终以当地市集运营方政策与实际客流为准。",
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(
            "usage: stall.py 'city=成都|budget_cny=3000|category=小吃热食|night_or_day=night'",
            file=sys.stderr,
        )
        return 1
    try:
        fields = _parse_kv(sys.argv[1].strip())
        result = build_stall(fields)
    except (OSError, json.JSONDecodeError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
