#!/usr/bin/env python3
"""opc-property match: 给定预算 / 用途 / 偏好，输出 Top 3 候选地（国内+海外混合）.

Input (`|` 分隔, `=` 键值):
  budget_cny=3000w|purpose=自住|family=有学龄子女|residency=希望有第二身份|risk_pref=中

Output: JSON {segment, top_picks:[{type, location, why, fit_score, ...}], notes}
"""

from __future__ import annotations

import json
import sys

from common import DISCLAIMER, load_ref, parse_int_cny, parse_kv


def _segment(budget_cny: int, segments: list[dict]) -> dict:
    for seg in segments:
        if seg["min_cny"] <= budget_cny < seg["max_cny"]:
            return seg
    return segments[-1]


def _score_property(prop: dict, purpose: str, family: str) -> float:
    score = 5.0
    name = prop.get("name", "")
    highlights = " ".join(prop.get("highlights", []))
    if "学" in family or "子女" in family:
        if "学区" in highlights or "学位" in highlights or "教育" in highlights:
            score += 2
    if purpose in ("自住", "改善"):
        if "改善" in prop.get("type", "") or "院落" in prop.get("type", "") or "顶豪" in prop.get("type", ""):
            score += 1.5
    if purpose in ("投资", "保值", "资产配置"):
        if "流动" in highlights or "强" in highlights:
            score += 1
    if "海景" in highlights or "江景" in highlights or "公园" in highlights or "湖" in highlights:
        score += 0.8
    return round(score, 2)


def _score_overseas(market: dict, residency: str, risk_pref: str) -> float:
    score = 5.0
    needs_id = "希望" in residency or "需要" in residency or "想要" in residency
    res_link = market.get("residency_link", "")
    if needs_id:
        if "金签" in res_link or "Golden Visa" in res_link or "买房 ≥" in res_link:
            score += 3
        elif "购房不直接给身份" in res_link or "不直接" in res_link:
            score -= 1
    if risk_pref == "低":
        if market["country"] in ("英国", "美国", "新加坡", "日本", "法国"):
            score += 1
        if market["city"] == "迪拜":
            score -= 0.5
    if risk_pref == "高":
        if market["city"] == "迪拜":
            score += 1
    return round(score, 2)


def match(fields: dict[str, str]) -> dict:
    budget_raw = fields.get("budget_cny", "1000w")
    budget_cny = parse_int_cny(budget_raw)
    purpose = fields.get("purpose", "自住")
    family = fields.get("family", "")
    residency = fields.get("residency", "")
    risk_pref = fields.get("risk_pref", "中")

    cn = load_ref("cn_premium_properties.json")
    overseas = load_ref("global_markets.json")
    seg = _segment(budget_cny, cn["buyer_segmentation"]["segments"])

    cn_pool = []
    for tier_key in seg["fit_tiers"]:
        tier_obj = cn.get(f"tier_{tier_key}", {})
        for p in tier_obj.get("properties", []):
            if budget_cny >= p["typical_total_cny_range"][0]:
                p_copy = dict(p)
                p_copy["tier"] = tier_key
                p_copy["fit_score"] = _score_property(p, purpose, family)
                cn_pool.append(p_copy)
    cn_pool.sort(key=lambda x: x["fit_score"], reverse=True)

    overseas_pool = []
    for m in overseas["markets"]:
        if m["city"] in seg["fit_overseas"]:
            m_copy = {
                "city": m["city"],
                "country": m["country"],
                "buyer_total_budget_cny_range": m["buyer_total_budget_cny_range"],
                "core_areas": m["core_areas"][:3],
                "residency_link": m["residency_link"],
                "highlights": m.get("highlights", []),
                "risks": m.get("risks", []),
                "fit_score": _score_overseas(m, residency, risk_pref),
            }
            overseas_pool.append(m_copy)
    overseas_pool.sort(key=lambda x: x["fit_score"], reverse=True)

    domestic_picks = [
        {
            "type": "domestic",
            "tier": p["tier"],
            "name": p["name"],
            "city": p["city"],
            "district": p["district"],
            "why": "; ".join(p.get("highlights", [])),
            "buyer_profile": p.get("buyer_profile", ""),
            "liquidity": p.get("liquidity", ""),
            "fit_score": p["fit_score"],
        }
        for p in cn_pool[:3]
    ]
    overseas_picks = [
        {
            "type": "overseas",
            "city": m["city"],
            "country": m["country"],
            "core_areas": m["core_areas"],
            "residency_link": m["residency_link"],
            "why": "; ".join(m["highlights"]),
            "risks": m["risks"],
            "fit_score": m["fit_score"],
        }
        for m in overseas_pool[:3]
    ]

    return {
        "input": {
            "budget_cny": budget_cny,
            "budget_label": budget_raw,
            "purpose": purpose,
            "family": family,
            "residency": residency,
            "risk_pref": risk_pref,
        },
        "segment": {"label": seg["label"], "fit_tiers": seg["fit_tiers"], "fit_overseas": seg["fit_overseas"]},
        "domestic_picks": domestic_picks,
        "overseas_picks": overseas_picks,
        "next_steps": [
            "看房窗口期：每个候选标的至少实地走访 2 次（白天 + 夜晚）",
            "持有成本：用 holding_cost.py 跑 5 年总持有成本对比",
            "资金路径：用 compliance.py 检查跨境合规预算",
            "若涉及海外：先咨询持牌移民律师 + 私行客户经理（不在本工具范围内）",
        ],
        "disclaimer": DISCLAIMER,
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(
            "usage: match.py 'budget_cny=3000w|purpose=自住|family=有学龄子女|residency=希望有第二身份|risk_pref=中'",
            file=sys.stderr,
        )
        return 1
    try:
        fields = parse_kv(sys.argv[1].strip())
        result = match(fields)
    except (OSError, json.JSONDecodeError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
