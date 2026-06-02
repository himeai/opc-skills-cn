#!/usr/bin/env python3
"""opc-dagong: 零工平台匹配（外卖 / 网约车 / 跑腿 / 众包 / 家政）.

Input (`|` 分隔，`=` 键值):
  city=杭州|wheels=电动车|hours_per_day=8|need_insurance=yes|prefer=外卖

Output: JSON {ranked: [{name, score, fit_reasons, ...}], notes}
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "references" / "gig_platforms.json"


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


def _is_yes(value: str) -> bool:
    return value.strip().lower() in {"yes", "y", "true", "1", "是", "有"}


def _score_platform(p: dict, ctx: dict) -> tuple[float, list[str]]:
    weights = ctx["weights"]
    earn = (p["earn_per_hour_cny"][0] + p["earn_per_hour_cny"][1]) / 2
    earn_norm = min(earn / 50.0, 1.5)
    barrier_text = p["entry_barrier"]
    barrier_norm = 1.0
    if "双证" in barrier_text or "运输证" in barrier_text:
        barrier_norm = 0.4
    elif "健康证" in barrier_text or "押金" in barrier_text:
        barrier_norm = 0.7

    insurance_norm = 0.3
    if "缴纳" in p["social_insurance"] or "意外险 + 重疾险" in p["social_insurance"]:
        insurance_norm = 1.0
    elif "意外险" in p["social_insurance"]:
        insurance_norm = 0.6

    vehicle_norm = 1.0
    wheels = ctx["wheels"]
    if "电动车" in p["vehicle_required"] and wheels not in {"电动车", "摩托车"}:
        vehicle_norm = 0.4
    elif "私家车" in p["vehicle_required"] and wheels != "私家车":
        vehicle_norm = 0.2
    elif "无" in p["vehicle_required"]:
        vehicle_norm = 1.0

    stability_norm = 0.7
    if "专送" in str(p["modes"]):
        stability_norm = 1.0
    elif "众包" in str(p["modes"]):
        stability_norm = 0.6

    score = (
        earn_norm * weights["earn"]
        + barrier_norm * weights["barrier"]
        + insurance_norm * weights["insurance"]
        + vehicle_norm * weights["vehicle_fit"]
        + stability_norm * weights["stability"]
    )

    fit_reasons = []
    if earn_norm >= 1.0:
        fit_reasons.append(f"时薪较高（{earn:.0f} 元 / h）")
    if barrier_norm >= 0.9:
        fit_reasons.append("入门门槛低")
    if insurance_norm >= 0.9:
        fit_reasons.append("有社保 / 五险")
    if vehicle_norm >= 0.9:
        fit_reasons.append("和你的交通工具匹配")
    if stability_norm >= 0.9:
        fit_reasons.append("订单稳定（专送 / B2C）")

    if ctx["need_insurance"] and insurance_norm < 0.6:
        fit_reasons.append("⚠️ 你需要五险但此平台不提供")
    if ctx["wheels"] == "无车" and "私家车" in p["vehicle_required"]:
        fit_reasons.append("⚠️ 你没有私家车")

    return round(score, 3), fit_reasons


def build_match(fields: dict[str, str]) -> dict:
    data = _load()
    wheels = fields.get("wheels", "电动车")
    need_insurance = _is_yes(fields.get("need_insurance", "no"))
    hours_per_day = fields.get("hours_per_day", "8")
    prefer_category = fields.get("prefer", "")
    city = fields.get("city", "未指定")

    ctx = {
        "weights": data["scoring_weights"],
        "wheels": wheels,
        "need_insurance": need_insurance,
    }

    candidates = data["platforms"]
    if prefer_category:
        filtered = [p for p in candidates if prefer_category in p["category"]]
        if filtered:
            candidates = filtered

    ranked = []
    for p in candidates:
        score, reasons = _score_platform(p, ctx)
        avg_earn = (p["earn_per_hour_cny"][0] + p["earn_per_hour_cny"][1]) / 2
        try:
            estimated_daily = round(avg_earn * float(hours_per_day))
        except ValueError:
            estimated_daily = None
        ranked.append({
            "name": p["name"],
            "category": p["category"],
            "score": score,
            "earn_per_hour_cny": p["earn_per_hour_cny"],
            "estimated_daily_cny": estimated_daily,
            "platform_take_pct": p["platform_take_pct"],
            "entry_barrier": p["entry_barrier"],
            "social_insurance": p["social_insurance"],
            "vehicle_required": p["vehicle_required"],
            "best_for": list(p["best_for"]),
            "warnings": list(p["warnings"]),
            "fit_reasons": reasons,
        })

    ranked.sort(key=lambda x: x["score"], reverse=True)

    return {
        "city": city,
        "wheels": wheels,
        "hours_per_day": hours_per_day,
        "need_insurance": need_insurance,
        "prefer_category": prefer_category or "全部",
        "ranked": ranked[:6],
        "general_notes": list(data["general_notes"]),
        "disclaimer": "本匹配仅作选择参考；具体抽成 / 收入随城市 / 阶段 / 平台政策动态变化，以平台公告为准。",
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(
            "usage: gig.py 'city=杭州|wheels=电动车|hours_per_day=8|need_insurance=yes'",
            file=sys.stderr,
        )
        return 1
    try:
        fields = _parse_kv(sys.argv[1].strip())
        result = build_match(fields)
    except (OSError, json.JSONDecodeError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
