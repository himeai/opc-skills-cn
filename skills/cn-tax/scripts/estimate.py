#!/usr/bin/env python3
"""cn-tax: 税负近似测算（增值税 + 附加税 + 所得税）.

Input:  "entity=...|period=quarter|year|revenue=...|cost=...|[headcount=...]"
Output: JSON {entity, period, taxes: [...], total_tax, effective_rate, cautions: [...]}

不替代税务师；仅作内部预估。
"""

from __future__ import annotations

from cli_common import (  # type: ignore[import-not-found]
    load_ref,
    parse_money,
    require,
    run_kv_cli,
)


VALID_PERIODS = ("quarter", "year")


def _vat_small_scale(revenue: float, period: str, vat_meta: dict) -> dict:
    rate = vat_meta["current_rate"]
    threshold = (
        vat_meta["quarterly_exempt_threshold"]
        if period == "quarter"
        else vat_meta["quarterly_exempt_threshold"] * 4
    )
    if revenue <= threshold:
        return {
            "name": "vat",
            "label": "增值税（小规模）",
            "base": revenue,
            "rate": 0.0,
            "amount": 0.0,
            "note": (
                f"销售额 {revenue:.2f} ≤ 免征额度 {threshold:.0f}，"
                "假设全部为普票；如开具专票部分仍需按 1% 计税"
            ),
        }
    amount = revenue * rate
    return {
        "name": "vat",
        "label": "增值税（小规模）",
        "base": revenue,
        "rate": rate,
        "amount": round(amount, 2),
        "note": f"超过免征额度，按 {rate * 100:.1f}% 全额计税（预估）",
    }


def _vat_general(revenue: float, vat_meta: dict) -> dict:
    rate = vat_meta["rates"]["modern_services"]
    amount = revenue * rate
    return {
        "name": "vat",
        "label": "增值税（一般纳税人 / 现代服务业 6%）",
        "base": revenue,
        "rate": rate,
        "amount": round(amount, 2),
        "note": "本 skill 未建模进项抵扣；实际应纳 = 销项 - 进项，请按实际抵扣计算",
    }


def _additional_tax(vat_amount: float, rules: dict, is_small_scale: bool) -> dict:
    rates = rules["additional_tax"]["rates"]
    rate = (
        rates["urban_maintenance"]["city"]
        + rates["education_surcharge"]
        + rates["local_education_surcharge"]
    )
    base = vat_amount
    raw = base * rate
    if is_small_scale:
        raw *= rules["additional_tax"]["small_scale_reduction"]
    return {
        "name": "additional_tax",
        "label": "附加税费（城建 7% + 教育费 3% + 地方 2%）",
        "base": base,
        "rate": rate,
        "amount": round(raw, 2),
        "note": "假设市区税率 7%；县/镇为 5%，其它 1%。小规模 / 小微减半计征",
    }


def _corporate_income(profit: float, rules: dict, headcount: int | None) -> dict:
    meta = rules["corporate_income"]
    threshold = meta["small_micro_threshold"]
    is_small_micro = (
        profit <= threshold["income"]
        and (headcount is None or headcount <= threshold["headcount"])
    )
    if is_small_micro and profit > 0:
        rate = meta["small_micro_effective_rate"]
        return {
            "name": "corporate_income",
            "label": "企业所得税（小型微利综合 5%）",
            "base": profit,
            "rate": rate,
            "amount": round(profit * rate, 2),
            "note": meta["small_micro_rate_note"],
        }
    rate = meta["standard_rate"]
    return {
        "name": "corporate_income",
        "label": "企业所得税（标准 25%）",
        "base": max(profit, 0),
        "rate": rate,
        "amount": round(max(profit, 0) * rate, 2),
        "note": "未享受小型微利；如有研发加计 / 高新优惠请在实际申报中扣除",
    }


def _individual_business_income(profit: float, rules: dict) -> dict:
    meta = rules["individual_business_income"]
    if profit <= 0:
        return {
            "name": "individual_business_income",
            "label": "个人经营所得（个体 / 个独）",
            "base": 0.0, "rate": 0.0, "amount": 0.0,
            "note": "经营所得 ≤0，无个人经营所得税",
        }
    bracket_rate = 0.0
    deduct = 0.0
    for br in meta["brackets"]:
        if br["upper"] is None or profit <= br["upper"]:
            bracket_rate = br["rate"]
            deduct = br["deduct"]
            break
    raw = profit * bracket_rate - deduct
    halve_threshold = meta["halve_under_threshold"]
    if profit <= halve_threshold:
        raw *= 0.5
        note = "100 万以内部分减半征收（政策延续）"
    else:
        note = "超过 100 万部分不享受减半"
    return {
        "name": "individual_business_income",
        "label": "个人经营所得（个体 / 个独）",
        "base": profit,
        "rate": bracket_rate,
        "amount": round(max(raw, 0), 2),
        "note": note,
    }


def build_estimate(fields: dict[str, str]) -> dict:
    """Estimate the tax burden for an entity in a given period."""
    entity, period = require(fields, "entity", "period")
    revenue = parse_money(fields.get("revenue", "0"), "revenue")
    cost = parse_money(fields.get("cost", "0"), "cost")
    headcount_raw = fields.get("headcount")
    headcount = int(headcount_raw) if headcount_raw else None

    if period not in VALID_PERIODS:
        raise ValueError(f"period must be one of {VALID_PERIODS}")

    rules = load_ref("rules")
    if entity not in rules["entities"]:
        raise ValueError(f"unknown entity '{entity}'")

    ent_meta = rules["entities"][entity]
    profit = revenue - cost

    taxes: list[dict] = []
    if ent_meta["vat_default"] == "small_scale":
        vat = _vat_small_scale(revenue, period, rules["vat"]["small_scale"])
    else:
        vat = _vat_general(revenue, rules["vat"]["general"])
    taxes.append(vat)
    taxes.append(_additional_tax(
        vat["amount"], rules, ent_meta["vat_default"] == "small_scale"
    ))

    if ent_meta["income_tax_type"] == "corporate":
        taxes.append(_corporate_income(profit, rules, headcount))
    else:
        taxes.append(_individual_business_income(profit, rules))

    total = round(sum(t["amount"] for t in taxes), 2)
    effective = round(total / revenue, 4) if revenue > 0 else 0.0

    cautions = [
        "结果为本地近似计算，实际以电子税务局申报系统为准",
        "未建模：进项发票 / 研发加计 / 残保金 / 印花税 / 房产税等",
        "请勿据此结果做申报；本 skill 不替代税务师",
    ]

    return {
        "entity": entity,
        "entity_label": ent_meta["label"],
        "period": period,
        "revenue": revenue,
        "cost": cost,
        "profit": round(profit, 2),
        "taxes": taxes,
        "total_tax": total,
        "effective_rate": effective,
        "cautions": cautions,
    }


def main() -> int:
    """Entry point for estimate.py."""
    return run_kv_cli(
        'estimate.py "entity=X|period=quarter|year|revenue=X|cost=X|headcount=X"',
        build_estimate,
    )


if __name__ == "__main__":
    raise SystemExit(main())
