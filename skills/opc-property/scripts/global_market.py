#!/usr/bin/env python3
"""opc-property global_market: 海外 10 大豪宅市场对照表 + 推荐.

Input: budget_cny=5000w|residency=希望第二身份|tax_pref=低税|family=有学龄子女
Output: ranked markets + 关键税费 / 身份联动 / 风险提示
"""

from __future__ import annotations

import json
import sys

from common import DISCLAIMER, load_ref, parse_int_cny, parse_kv


def _score(market: dict, residency: str, tax_pref: str, family: str) -> float:
    score = 5.0
    res = market.get("residency_link", "")
    needs_id = residency and ("希望" in residency or "需要" in residency or "想要" in residency)
    if needs_id:
        if "金签" in res or "Golden Visa" in res or "买房 ≥" in res:
            score += 3
        elif "已废" in res or "禁令" in res or "不直接" in res:
            score -= 1
    if tax_pref == "低税":
        if market["city"] in ("迪拜", "新加坡"):
            score += 2 if market["city"] == "迪拜" else 0
        if market["city"] in ("伦敦", "巴黎", "纽约", "悉尼"):
            score -= 1
    if "学" in family or "子女" in family:
        if market["city"] in ("伦敦", "纽约", "新加坡", "悉尼", "温哥华", "洛杉矶"):
            score += 1.5
    return round(score, 2)


def market(fields: dict[str, str]) -> dict:
    budget_cny = parse_int_cny(fields.get("budget_cny", "3000w"))
    residency = fields.get("residency", "")
    tax_pref = fields.get("tax_pref", "中")
    family = fields.get("family", "")

    data = load_ref("global_markets.json")
    policy = load_ref("policy_residency.json")
    by_country = {p["country"]: p for p in policy["programs"]}

    ranked = []
    for m in data["markets"]:
        lo, hi = m["buyer_total_budget_cny_range"]
        if budget_cny < lo * 0.5:
            continue
        score = _score(m, residency, tax_pref, family)
        if budget_cny < lo:
            score -= 1.5
        prog = by_country.get(m["country"])
        ranked.append({
            "city": m["city"],
            "country": m["country"],
            "buyer_total_budget_cny_range": [lo, hi],
            "fit_score": score,
            "core_areas": m["core_areas"],
            "trophy_buildings": m.get("trophy_buildings", []),
            "tax": m["tax"],
            "ownership_path": m["ownership_path"],
            "residency_link": m["residency_link"],
            "highlights": m.get("highlights", []),
            "risks": m.get("risks", []),
            "linked_program": {
                "name": prog["name"],
                "min_property_cny": prog.get("min_property_cny"),
                "min_property_local": prog.get("min_property_local"),
                "visa_years": prog.get("visa_years"),
                "physical_residency_required": prog.get("physical_residency_required"),
                "as_of": prog.get("as_of"),
            } if prog else None,
        })
    ranked.sort(key=lambda x: x["fit_score"], reverse=True)

    return {
        "input": {
            "budget_cny": budget_cny,
            "residency": residency,
            "tax_pref": tax_pref,
            "family": family,
        },
        "ranked": ranked,
        "tips": [
            "迪拜进场最快、零税、可叠加金签；新加坡是亚洲家办首选但 ABSD 60% 拦死外国人",
            "纽约 / 伦敦 / 巴黎 适合「一辈子」级别配置，进场印花税要 5-17% 不要短炒",
            "温哥华 / 加拿大目前对外国人有买房禁令（延至 2027），需先解决身份",
            "葡萄牙 / 西班牙 黄金签证房产路径已关闭，不要再听旧攻略",
        ],
        "outflow_quota_warning": data["outflow_quota"]["comment"],
        "disclaimer": DISCLAIMER,
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(
            "usage: global_market.py 'budget_cny=5000w|residency=希望第二身份|tax_pref=低税|family=有学龄子女'",
            file=sys.stderr,
        )
        return 1
    try:
        fields = parse_kv(sys.argv[1].strip())
        result = market(fields)
    except (OSError, json.JSONDecodeError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
