#!/usr/bin/env python3
"""Pick recommended Chinese cities for OPC founders."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
DIMENSIONS = (
    "tax_policy",
    "living_cost",
    "startup_policy",
    "climate",
    "digital_infra",
    "industry",
    "talent",
    "admin_efficiency",
)
BASE_WEIGHTS = {
    "tax_policy": 1.0,
    "living_cost": 1.0,
    "startup_policy": 1.0,
    "climate": 1.0,
    "digital_infra": 1.0,
    "industry": 1.0,
    "talent": 1.0,
    "admin_efficiency": 1.0,
}
SPICY_PROVINCES = {"四川", "重庆", "湖南", "湖北"}
INDUSTRY_KEYWORDS = {
    "跨境电商": ("跨境", "外贸", "独立站", "亚马逊", "shopify"),
    "AI SaaS": ("saas", "SaaS", "ai", "AI", "软件", "订阅"),
    "内容创作": ("自媒体", "内容", "小红书", "视频号", "公众号", "博主"),
    "直播电商": ("直播", "带货", "短视频", "抖音"),
    "教育知识付费": ("课程", "知识付费", "教育", "培训"),
    "企业服务": ("企业服务", "b2b", "B2B", "客户管理", "协作"),
    "软件外包": ("外包", "接单", "开发服务"),
    "硬件出海": ("硬件", "出海", "电子", "供应链"),
    "制造业服务": ("制造", "工厂", "产业带"),
    "工业软件": ("工业软件", "mes", "ERP", "物联网"),
    "本地生活": ("本地生活", "到店", "餐饮", "门店"),
    "文旅": ("旅游", "文旅", "民宿", "旅居"),
    "医疗健康": ("医疗", "医生", "医院", "健康"),
    "金融科技": ("金融", "支付", "风控"),
    "新能源": ("新能源", "光伏", "电池", "储能"),
    "游戏动漫": ("游戏", "动漫", "二次元"),
    "物流": ("物流", "仓储", "供应链"),
    "消费品牌": ("品牌", "消费品", "美妆", "食品"),
    "数字游民": ("数字游民", "远程", "旅居", "自由职业", "咖啡馆"),
    "法律财税服务": ("财税", "法务", "代账", "合规"),
}


def load_json(relative_path: str) -> Any:
    path = SKILL_ROOT / relative_path
    with path.open("r", encoding="utf-8") as file_obj:
        return json.load(file_obj)


def parse_budget(text: str) -> int | None:
    match = re.search(r"预算\s*([0-9]+(?:\.[0-9]+)?)\s*万", text)
    if match:
        return int(float(match.group(1)) * 10000)
    match = re.search(r"预算\s*([0-9]{4,6})", text)
    if match:
        return int(match.group(1))
    match = re.search(r"月预算\s*([0-9]+(?:\.[0-9]+)?)\s*万", text)
    if match:
        return int(float(match.group(1)) * 10000)
    return None


def detect_industries(text: str) -> list[str]:
    lowered = text.lower()
    detected: list[str] = []
    for industry, keywords in INDUSTRY_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in lowered:
                detected.append(industry)
                break
    return detected or ["企业服务"]


def parse_preferences(text: str) -> dict[str, Any]:
    budget = parse_budget(text)
    industries = detect_industries(text)
    province_match = re.search(r"户籍([\u4e00-\u9fa5]{2,3})", text)
    preferences: dict[str, Any] = {
        "raw_input": text,
        "budget_cny": budget,
        "industries": industries,
        "prefer_south": any(word in text for word in ("南方", "华南", "江南")),
        "fear_cold": any(word in text for word in ("怕冷", "不冷", "暖和", "温暖")),
        "avoid_spicy": any(word in text for word in ("不爱辣", "不能吃辣", "怕辣", "清淡")),
        "need_medical": any(word in text for word in ("三甲", "医院", "医疗", "老人", "医生", "孩子", "小孩")),
        "prefer_non_tier1": any(word in text for word in ("非一线", "不要一线", "不去一线")),
        "slow_life": any(word in text for word in ("慢生活", "旅居", "数字游民", "自由职业")),
        "hukou_province": province_match.group(1) if province_match else None,
        "explicit_cities": [],
    }
    return preferences


def build_weights(preferences: dict[str, Any]) -> dict[str, float]:
    weights = dict(BASE_WEIGHTS)
    budget = preferences.get("budget_cny")
    if budget and budget <= 12000:
        weights["living_cost"] *= 1.5
    if preferences["need_medical"]:
        weights["living_cost"] *= 0.8
        weights["talent"] *= 1.15
    if "跨境电商" in preferences["industries"]:
        weights["tax_policy"] *= 1.3
        weights["industry"] *= 1.25
        weights["digital_infra"] *= 1.15
    if preferences["slow_life"] or "数字游民" in preferences["industries"]:
        weights["living_cost"] *= 1.25
        weights["climate"] *= 1.25
    return weights


def dimension_score(city: dict[str, Any], weights: dict[str, float]) -> float:
    weighted_sum = 0.0
    total_weight = 0.0
    for dimension in DIMENSIONS:
        weight = weights[dimension]
        weighted_sum += city["dimensions"][dimension]["score"] * weight
        total_weight += weight
    return weighted_sum / total_weight


def industry_score(city_name: str, industries: list[str], matrix: dict[str, Any]) -> float:
    values = []
    scores = matrix.get("scores", {})
    for industry in industries:
        city_scores = scores.get(industry, {})
        if city_name in city_scores:
            values.append(city_scores[city_name])
    return sum(values) / len(values) if values else 70.0


def apply_filters(city: dict[str, Any], preferences: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if preferences["prefer_non_tier1"] and city["tier"] == "一线":
        reasons.append("用户倾向非一线，过滤一线城市")
    if preferences["fear_cold"] and city["dimensions"]["climate"]["avg_temp"] < 15:
        reasons.append("用户怕冷，过滤年均温低于 15℃ 城市")
    if preferences["prefer_south"] and not city.get("is_southern"):
        reasons.append("用户倾向南方，过滤非南方城市")
    if preferences["need_medical"] and city.get("medical_resource_score", 0) < 72:
        reasons.append("用户需要医疗资源，过滤医疗资源不足城市")
    budget = preferences.get("budget_cny")
    if budget and city.get("monthly_cost_base", 0) > budget * 1.35:
        reasons.append("城市月成本显著超过预算")
    return not reasons, reasons


def soft_adjustments(
    city: dict[str, Any],
    preferences: dict[str, Any],
) -> tuple[float, list[str], list[str]]:
    adjustment = 0.0
    highlights: list[str] = []
    concerns: list[str] = []
    if preferences["avoid_spicy"] and city.get("province") in SPICY_PROVINCES:
        adjustment -= 6.0
        concerns.append("用户不爱辣，本地饮食适应性需评估")
    hukou_province = preferences.get("hukou_province")
    if hukou_province and hukou_province == city.get("province"):
        adjustment += 4.0
        highlights.append("户籍同省，社保、家庭距离和落地手续更友好")
    if city.get("digital_nomad_score", 0) >= 88:
        highlights.append("数字游民和远程工作友好度高")
    if city["dimensions"]["tax_policy"].get("park_rebate_max", 0) >= 0.36:
        highlights.append("园区返还上限较高，适合进一步核实政策")
    if city["dimensions"]["living_cost"]["score"] >= 82:
        highlights.append("生活成本压力较低")
    if city.get("medical_resource_score", 0) >= 88:
        highlights.append("医疗资源较强")
    if city["tier"] == "一线":
        concerns.append("一线城市成本和竞争压力较高")
    if city.get("monthly_cost_base", 0) >= 18000:
        concerns.append("月综合成本偏高")
    if city.get("medical_resource_score", 0) < 72:
        concerns.append("医疗资源相对弱，家庭型用户需谨慎")
    return adjustment, highlights[:4], concerns[:4]


def make_recommendations(text: str, top_n: int = 5) -> dict[str, Any]:
    # pylint: disable=too-many-locals
    cities = load_json("references/cities.json")
    matrix = load_json("references/industry_city_matrix.json")
    preferences = parse_preferences(text)
    weights = build_weights(preferences)
    recommendations = []
    filtered_out = []

    for city in cities:
        allowed, filter_reasons = apply_filters(city, preferences)
        if not allowed:
            filtered_out.append({"city": city["city"], "reasons": filter_reasons})
            continue
        base_score = dimension_score(city, weights)
        industry_match = industry_score(city["city"], preferences["industries"], matrix)
        adjustment, highlights, concerns = soft_adjustments(city, preferences)
        final_score = base_score * 0.72 + industry_match * 0.28 + adjustment
        if "跨境电商" in preferences["industries"]:
            final_score += city["dimensions"]["tax_policy"].get("park_rebate_max", 0) * 8
        recommendations.append({
            "city": city["city"],
            "province": city["province"],
            "tier": city["tier"],
            "score": round(final_score, 1),
            "industry_match_score": round(industry_match, 1),
            "monthly_cost_estimate_cny": city["monthly_cost_base"],
            "highlights": highlights,
            "concerns": concerns,
            "matched_clusters": city["dimensions"]["industry"].get("cluster", []),
            "next_steps": city.get("next_steps_template", [])[:3],
            "data_source_note": city.get("data_source_note", "种子数据，待人工核校"),
        })

    recommendations.sort(key=lambda item: item["score"], reverse=True)
    top = recommendations[:top_n]
    checklist = []
    for item in top[:3]:
        checklist.extend(item["next_steps"][:1])

    return {
        "status": "ok",
        "parsed_preferences": preferences,
        "weights": {key: round(value, 2) for key, value in weights.items()},
        "top_recommendations": top,
        "next_steps_checklist": checklist,
        "filtered_out_count": len(filtered_out),
        "filtered_out_sample": filtered_out[:5],
        "disclaimer": "结果基于种子数据和规则评分，不构成法律、税务、投资或落户建议；请做人工核校。",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Recommend Chinese cities for OPC founders.")
    parser.add_argument("query", help="Natural language preference query")
    parser.add_argument("--top", type=int, default=5, help="Number of cities to return")
    args = parser.parse_args()
    result = make_recommendations(args.query, max(3, min(args.top, 5)))
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
