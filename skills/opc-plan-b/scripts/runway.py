#!/usr/bin/env python3
"""opc-plan-b: 个人现金流体检 + 失业金 + 灵活就业社保参考.

Input (`|` 分隔，`=` 键值):
  city=杭州|monthly_cost=8000|cash=30000|debt=0|has_house_loan=yes|prev_contribution_years=3

Output: JSON {runway_months, threshold, unemployment_benefit, flexible_insurance, action_list}
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "references" / "personal_finance.json"


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


def _city_unemployment(data: dict, city: str) -> tuple[str, list[int]]:
    table = data["unemployment_insurance"]["monthly_amount_cny_by_city"]
    if city in table:
        return city, table[city]
    return "二三线参考", table["二三线参考"]


def _city_pension(data: dict, city: str) -> tuple[str, list[int]]:
    table = data["flexible_employment_insurance"]["pension"]["monthly_payment_cny_by_city"]
    if city in table:
        return city, table[city]
    return "二三线参考", table["二三线参考"]


def _city_medical(data: dict, city: str) -> list[int]:
    table = data["flexible_employment_insurance"]["medical"]["monthly_payment_cny_by_city"]
    if city in table:
        return table[city]
    return table["二三线参考"]


def _duration_band(years: float) -> str:
    if years < 1:
        return "缴费不足 1 年（不可领）"
    if years <= 5:
        return "1-5_years"
    if years <= 10:
        return "5-10_years"
    return "10+_years"


def _threshold(months: float) -> dict:
    thresholds = {
        "green": "跑道 ≥ 12 个月：可以从容找下一份",
        "yellow": "跑道 6-12 个月：建议立即开始零工 / 摆摊补贴",
        "orange": "跑道 3-6 个月：必须立即降本 + 上零工，不要犹豫",
        "red": "跑道 < 3 个月：考虑变卖资产 / 短租房 / 回老家过渡",
    }
    if months >= 12:
        level = "green"
    elif months >= 6:
        level = "yellow"
    elif months >= 3:
        level = "orange"
    else:
        level = "red"
    return {"level": level, "advice": thresholds[level]}


def build_runway(fields: dict[str, str]) -> dict:
    data = _load()
    city = fields.get("city", "二三线参考")
    try:
        monthly_cost = float(fields.get("monthly_cost", "8000"))
        cash = float(fields.get("cash", "30000"))
        debt = float(fields.get("debt", "0"))
    except ValueError as exc:
        raise ValueError(f"bad number: {exc}") from exc

    has_house_loan = _is_yes(fields.get("has_house_loan", "no"))

    try:
        contribution_years = float(fields.get("prev_contribution_years", "0"))
    except ValueError:
        contribution_years = 0.0
    is_employee_history = _is_yes(fields.get("was_employee", "no"))

    raw_runway = cash / max(monthly_cost, 1.0)
    runway_months = round(raw_runway, 1)
    threshold = _threshold(runway_months)

    duration_band = _duration_band(contribution_years)
    duration_table = data["unemployment_insurance"]["duration_months_by_contribution"]
    if duration_band in duration_table:
        duration_text = duration_table[duration_band]
    else:
        duration_text = "不可领"

    matched_city, monthly_range = _city_unemployment(data, city)
    if not is_employee_history:
        eligible_note = "你不是雇员身份（个独 / 个体投资人本人通常不缴失业保险），多数情况不可领"
        eligible = False
    elif contribution_years < 1:
        eligible_note = "缴费不满 1 年，不可领"
        eligible = False
    else:
        eligible_note = "符合基本条件（具体以户籍 / 居住地人社局为准）"
        eligible = True

    pension_city_key, pension_range = _city_pension(data, city)
    medical_range = _city_medical(data, city)

    danger_thresholds = data["runway_calculation"]["danger_thresholds"]

    action_list = []
    if threshold["level"] in {"orange", "red"}:
        action_list.append("立即开始零工 / 摆摊（参考 gig.py / stall.py）")
        action_list.append("把外食 / 订阅 / 健身等可砍支出全部砍掉")
    if threshold["level"] == "red":
        action_list.append("考虑短租 / 退房合住 / 回老家过渡")
        action_list.append("变卖非必要资产（车、奢侈品、不常用电子产品）")
    if has_house_loan:
        action_list.append("⚠️ 有房贷 → 优先保障还款；如已断供风险，主动联系银行申请「停息挂账」或「分期重组」")
    if debt > 0:
        action_list.append(f"⚠️ 有 {int(debt)} 元负债 → 不要再借新还旧；先看 credit_protection.must_do")
    if eligible:
        action_list.append(f"前往户籍地 / 居住地人社局申请失业金（{matched_city} 标准约 {monthly_range[0]}-{monthly_range[1]} 元 / 月）")
    action_list.append("到社保经办处办理灵活就业身份切换，医保不要断缴 3 个月以上")

    return {
        "city": city,
        "matched_city": matched_city,
        "monthly_cost_cny": int(monthly_cost),
        "cash_cny": int(cash),
        "debt_cny": int(debt),
        "runway_months": runway_months,
        "threshold": threshold,
        "danger_thresholds": danger_thresholds,
        "unemployment_benefit": {
            "eligible": eligible,
            "eligible_note": eligible_note,
            "estimated_monthly_cny_range": monthly_range,
            "duration_band": duration_band,
            "max_duration": duration_text,
            "concurrent_benefits": list(data["unemployment_insurance"]["concurrent_benefits"]),
        },
        "flexible_insurance": {
            "pension_monthly_range_cny": pension_range,
            "medical_monthly_range_cny": medical_range,
            "registration_path": list(data["flexible_employment_insurance"]["registration_path"]),
            "warning": "医保断缴 3 个月以上需重新计算等待期，不建议断",
        },
        "credit_protection": {
            "must_do": list(data["credit_protection"]["must_do"]),
            "avoid": list(data["credit_protection"]["avoid"]),
        },
        "must_keep": list(data["runway_calculation"]["must_keep_expenses"]),
        "can_cut": list(data["runway_calculation"]["can_cut_expenses"]),
        "action_list": action_list,
        "general_notes": list(data["general_notes"]),
        "disclaimer": "本数据仅作个人现金流体检参考；不构成金融 / 法律建议，复杂情况请咨询持牌顾问。",
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(
            "usage: runway.py 'city=杭州|monthly_cost=8000|cash=30000|debt=0|has_house_loan=yes'",
            file=sys.stderr,
        )
        return 1
    try:
        fields = _parse_kv(sys.argv[1].strip())
        result = build_runway(fields)
    except (OSError, json.JSONDecodeError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
