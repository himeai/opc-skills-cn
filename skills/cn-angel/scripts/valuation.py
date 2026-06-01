#!/usr/bin/env python3
"""cn-angel: 中国天使轮估值参考器（4 种估值法平均 + 稀释表）.

Input (`|` 分隔，`=` 键值):
  stage=天使|industry=SaaS|round_size_cny_w=600
  |berkus_idea=0.8|berkus_prototype=0.7|berkus_team=0.9|berkus_strategic=0.5|berkus_rollout=0.4
  |sc_team=1.2|sc_opportunity=1.1|sc_product=1.0|sc_competition=0.9|sc_channel=1.0|sc_extra=1.0
  |annual_rev_cny_w=80|projected_exit_cny_w=80000

Output: JSON {pre_money_estimates:[...], pre_money_avg, post_money, dilution_table, sanity_check}
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "references" / "valuation_models.json"


def _load() -> dict:
    return json.loads(TEMPLATES.read_text(encoding="utf-8"))


def _f(value: str | None, default: float = 1.0) -> float:
    if value is None or value == "":
        return default
    try:
        return float(value)
    except ValueError:
        return default


def _berkus(fields: dict[str, str], data: dict) -> float | None:
    """Berkus 法估值（万元），5 项独立打分 0-1。"""
    keys = ["berkus_idea", "berkus_prototype", "berkus_team", "berkus_strategic", "berkus_rollout"]
    if not any(fields.get(k) for k in keys):
        return None
    axes = data["models"]["berkus"]["axes"]
    inputs = [
        _f(fields.get("berkus_idea"), 0.0),
        _f(fields.get("berkus_prototype"), 0.0),
        _f(fields.get("berkus_team"), 0.0),
        _f(fields.get("berkus_strategic"), 0.0),
        _f(fields.get("berkus_rollout"), 0.0),
    ]
    total = 0.0
    for axis, score in zip(axes, inputs):
        total += max(0.0, min(1.0, score)) * axis["max_value_cny_w"]
    return round(total, 1)


def _scorecard(fields: dict[str, str], data: dict) -> float | None:
    """Scorecard 法估值（万元），6 项加权 0.5-1.5。"""
    keys = ["sc_team", "sc_opportunity", "sc_product", "sc_competition", "sc_channel", "sc_extra"]
    if not any(fields.get(k) for k in keys):
        return None
    sc = data["models"]["scorecard"]
    baseline = sc["baseline_pre_money_cny_w"]
    weights = {axis["key"]: axis["weight"] for axis in sc["axes"]}
    inputs = {
        "team": _f(fields.get("sc_team"), 1.0),
        "opportunity": _f(fields.get("sc_opportunity"), 1.0),
        "product_tech": _f(fields.get("sc_product"), 1.0),
        "competition": _f(fields.get("sc_competition"), 1.0),
        "channel_partnership": _f(fields.get("sc_channel"), 1.0),
        "additional_factors": _f(fields.get("sc_extra"), 1.0),
    }
    multiplier = sum(
        max(0.5, min(1.5, inputs[k])) * weights[k] for k in weights
    )
    return round(baseline * multiplier, 1)


def _vc_method(fields: dict[str, str], round_size: float, data: dict) -> float | None:
    """VC 反推法估值（万元）：从 projected_exit 反推。"""
    proj_exit = _f(fields.get("projected_exit_cny_w"), 0.0)
    if proj_exit <= 0:
        return None
    vc = data["models"]["vc_method"]
    irr = vc["default_required_irr"]
    years = vc["default_years_to_exit"]
    dilution_to_exit = vc["default_dilution_to_exit"]
    required_return_multiple = (1 + irr) ** years
    investor_share_at_exit = required_return_multiple * round_size / proj_exit
    investor_share_now = investor_share_at_exit / (1 - dilution_to_exit)
    if investor_share_now <= 0 or investor_share_now >= 1:
        return None
    post_money = round_size / investor_share_now
    pre_money = post_money - round_size
    return round(pre_money, 1)


def _industry_multiple(fields: dict[str, str], industry: str, data: dict) -> float | None:
    """行业倍数法估值（万元）：基于 ARR 或对应 axis。"""
    rev = _f(fields.get("annual_rev_cny_w"), 0.0)
    if rev <= 0:
        return None
    cfg = data["models"]["industry_multiple"]["industry_default_multiple"]
    multi_meta = cfg.get(industry) or cfg["AI 应用"]
    return round(rev * multi_meta["value"], 1)


def _stage_range_check(stage: str, pre_money: float, data: dict) -> dict:
    ranges = data["stage_typical_ranges_cny_w"].get(stage) or data["stage_typical_ranges_cny_w"]["天使"]
    in_range = ranges["pre_money_min"] <= pre_money <= ranges["pre_money_max"]
    return {
        "stage": stage,
        "stage_typical_pre_money_min_cny_w": ranges["pre_money_min"],
        "stage_typical_pre_money_max_cny_w": ranges["pre_money_max"],
        "in_typical_range": in_range,
        "comment": (
            "估值在该阶段典型区间内" if in_range
            else f"估值偏离该阶段（{stage}）典型区间，需要更强 milestone 支撑"
        ),
    }


def build_valuation(fields: dict[str, str]) -> dict:
    data = _load()
    stage = fields.get("stage", "天使")
    industry = fields.get("industry", "AI 应用")
    round_size = _f(fields.get("round_size_cny_w"), 0.0)
    if round_size <= 0:
        raise ValueError("round_size_cny_w 必须 > 0")

    estimates = []
    for label, val in [
        ("Berkus 法", _berkus(fields, data)),
        ("Scorecard 法", _scorecard(fields, data)),
        ("VC 反推法", _vc_method(fields, round_size, data)),
        ("行业倍数法", _industry_multiple(fields, industry, data)),
    ]:
        if val is not None and val > 0:
            estimates.append({"method": label, "pre_money_cny_w": val})

    if not estimates:
        raise ValueError("至少需要提供一种估值法的输入参数")

    pre_money_avg = round(sum(e["pre_money_cny_w"] for e in estimates) / len(estimates), 1)
    post_money = round(pre_money_avg + round_size, 1)

    dilution_table = []
    shares = data["round_size_to_share_table"]["shares_to_evaluate"]
    for share in shares:
        # share = round_size / (pre_money + round_size) → pre_money = round_size / share - round_size
        pre = round(round_size / share - round_size, 1)
        dilution_table.append({
            "investor_share_pct": round(share * 100, 2),
            "implied_pre_money_cny_w": pre,
            "implied_post_money_cny_w": round(pre + round_size, 1),
        })

    dilution_warn = data["dilution_targets"]
    actual_dilution = round_size / (pre_money_avg + round_size)
    if actual_dilution > dilution_warn["danger_threshold_pct"]:
        dilution_alert = "danger"
    elif actual_dilution > dilution_warn["warning_threshold_pct"]:
        dilution_alert = "warning"
    elif actual_dilution > dilution_warn["healthy_max_pct"]:
        dilution_alert = "caution"
    else:
        dilution_alert = "healthy"

    return {
        "stage": stage,
        "industry": industry,
        "round_size_cny_w": round_size,
        "pre_money_estimates": estimates,
        "pre_money_avg_cny_w": pre_money_avg,
        "post_money_cny_w": post_money,
        "implied_dilution_pct": round(actual_dilution * 100, 2),
        "dilution_alert": dilution_alert,
        "dilution_table": dilution_table,
        "sanity_check": _stage_range_check(stage, pre_money_avg, data),
        "disclaimer": "本估值仅为教学/谈判参考，不构成投资意见；最终估值取决于市场和谈判。",
    }


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


def main() -> int:
    if len(sys.argv) != 2:
        print(
            "usage: valuation.py 'stage=天使|industry=SaaS|round_size_cny_w=600|...'",
            file=sys.stderr,
        )
        return 1
    try:
        fields = _parse_kv(sys.argv[1].strip())
        result = build_valuation(fields)
    except (OSError, json.JSONDecodeError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
