#!/usr/bin/env python3
"""visa.py — 中国普通护照签证矩阵查询。

input format:
  countries=日本,法国,美国|order=date  # 输出按 leadtime 排序的办理建议
"""

from __future__ import annotations

import json
import sys

from common import DISCLAIMER, load_ref, parse_kv, parse_list


def query(input_str: str) -> dict:
    fields = parse_kv(input_str)
    countries = parse_list(fields.get("countries", ""))
    order = fields.get("order", "date")

    visa_ref = load_ref("visa_cn.json")
    matrix = visa_ref["matrix"]
    by_country = {row["country"]: row for row in matrix}

    found = []
    not_found = []
    for c in countries:
        if c in by_country:
            found.append(by_country[c])
        else:
            not_found.append(c)

    if order == "date":
        found.sort(key=lambda r: -r["leadtime_days"])

    total_fee = sum(r["fee_cny_est"] for r in found)
    max_lead = max([r["leadtime_days"] for r in found], default=0)

    schedule = []
    for r in found:
        schedule.append({
            "country": r["country"],
            "policy_kind": r["policy_kind"],
            "stay_days": r["stay_days"],
            "fee_cny_est": r["fee_cny_est"],
            "leadtime_days": r["leadtime_days"],
            "apply_before_departure_days": r["leadtime_days"] + 7,
            "notes": r["notes"],
        })

    return {
        "countries_input": countries,
        "found": len(found),
        "not_found": not_found,
        "schedule": schedule,
        "policy_legend": visa_ref["policy_legend"],
        "total_fee_cny_est": total_fee,
        "earliest_apply_before_departure_days": max_lead + 7,
        "common_extra_costs": visa_ref["common_extra_costs"],
        "warnings": [
            "签证政策随时变动，出发前请到中国领事服务网（cs.mfa.gov.cn）和目的国驻华使馆官网核实",
            "申根任意国签证可入所有申根国，但行程主停留国必须明确",
            "美 / 加 / 申 / 英任一签证可帮你解锁多国免签（中南美 / 加勒比常用）",
        ],
        "updated": visa_ref.get("_updated"),
        "disclaimer": DISCLAIMER,
    }


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: visa.py 'countries=日本,法国,美国|order=date'", file=sys.stderr)
        return 2
    try:
        out = query(sys.argv[1])
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
