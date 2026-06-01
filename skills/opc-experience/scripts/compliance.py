#!/usr/bin/env python3
"""compliance.py — 高净值体验合规与风险红线。

input format:
  scope=payment,insurance,medical,legal  # 取多个用 ,
  experience_id=space_suborbital  # 可选：针对单个体验
"""

from __future__ import annotations

import json
import sys

from common import DISCLAIMER, load_ref, parse_kv, parse_list


def check(input_str: str) -> dict:
    fields = parse_kv(input_str)
    scope = parse_list(fields.get("scope", "payment,insurance,medical,legal"))
    exp_id = fields.get("experience_id", "")

    ref = load_ref("compliance.json")
    out: dict = {"scope": scope}

    if "payment" in scope:
        out["payment_compliance"] = ref["payment_compliance"]
    if "insurance" in scope:
        out["insurance_required"] = ref["insurance_required"]
    if "medical" in scope:
        out["medical_baseline"] = ref["medical_baseline"]
        out["exit_entry"] = ref["exit_entry"]
    if "legal" in scope:
        out["legal_redlines"] = ref["legal_redlines"]
        out["ethics_caution"] = ref["ethics_caution"]

    if exp_id:
        exp_ref = load_ref("experiences.json")
        match = next((e for e in exp_ref["experiences"] if e["id"] == exp_id), None)
        if match:
            out["experience_focus"] = {
                "name": match["name"],
                "category": match["category"],
                "tier": match["tier"],
                "price_cny_range": [match["price_cny_min"], match["price_cny_max"]],
                "fitness": match["fitness"],
                "lead_months": match["lead_months"],
                "highlights": match.get("highlights", []),
                "notes": match.get("notes", ""),
            }
            # 太空 / 极地 / 高山专项保险提示
            cat = match["category"]
            ins = ref["insurance_required"]
            if "太空" in match["name"] or match["id"].startswith("space_"):
                out["specific_insurance"] = ins.get("space")
            elif cat == "极地探险":
                out["specific_insurance"] = ins.get("polar_cruise")
            elif cat == "登山远征":
                out["specific_insurance"] = ins.get("everest")
            elif cat == "极速极限":
                out["specific_insurance"] = ins.get("f1_track")

    out["disclaimer"] = DISCLAIMER
    return out


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: compliance.py 'scope=payment,insurance,medical,legal|experience_id=...'", file=sys.stderr)
        return 2
    try:
        out = check(sys.argv[1])
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
