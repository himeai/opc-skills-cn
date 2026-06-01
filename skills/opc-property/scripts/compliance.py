#!/usr/bin/env python3
"""opc-property compliance: 跨境资金合规清单 + 红线提示.

Input: amount_cny=5000w|target_country=美国|use=境外购房|family_size=3
Output: JSON {legal_paths, red_lines, must_know, recommended_combo}
"""

from __future__ import annotations

import json
import sys

from common import DISCLAIMER, load_ref, parse_int_cny, parse_kv


def compliance(fields: dict[str, str]) -> dict:
    amount_cny = parse_int_cny(fields.get("amount_cny", "1000w"))
    target_country = fields.get("target_country", "")
    use = fields.get("use", "境外购房")
    family_size = int(fields.get("family_size", "1"))

    data = load_ref("capital_outflow.json")
    quota = data["personal_quota"]
    annual_per_person_cny = quota["annual_quota_usd"] * 7.2
    family_pool_cny = annual_per_person_cny * family_size

    coverage_years = round(amount_cny / max(family_pool_cny, 1), 1)

    paths = data["compliant_paths"]
    if "购房" in use or "不动产" in use:
        recommended = ["提前移居 / 持有外国身份后再置业", "ODI（境外直接投资备案）"]
        rejected_paths = [
            "❌ 个人 5 万美元额度不能用于境外购房（结售汇规定）",
            "❌ ODI 不得用于敏感行业（房地产 / 酒店 / 影城 / 体育俱乐部 / 娱乐业）的纯置业",
        ]
    elif "投资" in use or "金融" in use:
        recommended = ["QDII / QDLP / QDIE", "WMC 跨境理财通"]
        rejected_paths = []
    elif "工作" in use or "薪酬" in use:
        recommended = ["境外薪酬 / 顾问费 / 经营所得"]
        rejected_paths = []
    else:
        recommended = ["提前移居 / 持有外国身份后再置业"]
        rejected_paths = []

    return {
        "input": {
            "amount_cny": amount_cny,
            "target_country": target_country,
            "use": use,
            "family_size": family_size,
        },
        "annual_quota": {
            "per_person_usd": quota["annual_quota_usd"],
            "per_person_cny": round(annual_per_person_cny),
            "family_pool_cny": round(family_pool_cny),
            "scope": quota["scope"],
            "split_warning": quota["split_strategy_warning"],
        },
        "coverage_estimate": {
            "implied_years_at_full_quota": coverage_years,
            "comment": (
                "理论上即使整家用满额度也需要 "
                f"{coverage_years} 年才能搬完，且额度禁止用于境外购房——"
                "因此这条路对置业不可行。"
            ),
        },
        "recommended_legal_paths": [p for p in paths if p["name"] in recommended],
        "all_legal_paths": paths,
        "rejected_paths": rejected_paths,
        "red_lines": data["red_lines"],
        "must_know": data["must_know"],
        "professional_consult": [
            "持牌移民律师（身份路径）",
            "中资银行私行客户经理（合规通道）",
            "国际税务师（CRS + 报税）",
            "公证处 / 涉外律师（资金合法来源证明）",
        ],
        "disclaimer": DISCLAIMER,
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(
            "usage: compliance.py 'amount_cny=5000w|target_country=美国|use=境外购房|family_size=3'",
            file=sys.stderr,
        )
        return 1
    try:
        fields = parse_kv(sys.argv[1].strip())
        result = compliance(fields)
    except (OSError, json.JSONDecodeError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
