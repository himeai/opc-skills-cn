#!/usr/bin/env python3
"""cn-tax: 申报清单 + 申报日历提示.

Input:  "entity=...|period=quarter|year"
Output: JSON {entity, period, filings: [...], deadline_hints: [...]}
"""

from __future__ import annotations

from cli_common import load_ref, require, run_kv_cli  # type: ignore[import-not-found]


CHECKLIST_MAP = {
    ("individual_business", "quarter"): ["quarterly_small_scale"],
    ("individual_business", "year"): ["annual_individual_business"],
    ("sole_proprietor", "quarter"): ["quarterly_small_scale"],
    ("sole_proprietor", "year"): ["annual_individual_business"],
    ("small_scale_company", "quarter"): ["quarterly_small_scale"],
    ("small_scale_company", "year"): ["annual_corporate"],
    ("general_taxpayer_company", "quarter"): ["monthly_general_taxpayer"],
    ("general_taxpayer_company", "year"): ["annual_corporate"],
}

DEADLINE_HINTS = {
    "quarter": [
        "增值税及附加：季度终了次月 15 日前申报（例：Q1 → 4/15）",
        "企业所得税：季度预缴，次月 15 日前",
        "个人经营所得：月度或季度预缴，次月 15 日前",
        "遇法定节假日顺延，请以电子税务局公告为准",
    ],
    "year": [
        "企业所得税年度汇算：次年 5/31 前",
        "个人经营所得年度汇算（B 表）：次年 3/31 前",
        "个人综合所得年度汇算：次年 3/1 - 6/30",
    ],
}


def build_checklist(fields: dict[str, str]) -> dict:
    """Build the filing checklist + deadline hints."""
    entity, period = require(fields, "entity", "period")
    rules = load_ref("rules")
    if entity not in rules["entities"]:
        raise ValueError(f"unknown entity '{entity}'")
    if period not in ("quarter", "year"):
        raise ValueError("period must be quarter or year")

    cl = load_ref("checklists")["checklists"]
    keys = CHECKLIST_MAP.get((entity, period), [])
    filings = []
    for key in keys:
        meta = cl.get(key)
        if not meta:
            continue
        filings.append({
            "id": key,
            "label": meta["label"],
            "items": meta["items"],
        })

    return {
        "entity": entity,
        "entity_label": rules["entities"][entity]["label"],
        "period": period,
        "filings": filings,
        "deadline_hints": DEADLINE_HINTS[period],
        "warning": "本清单为流程参考；具体表单项目以电子税务局当期申报界面为准",
    }


def main() -> int:
    """Entry point for checklist.py."""
    return run_kv_cli(
        'checklist.py "entity=X|period=quarter|year"',
        build_checklist,
    )


if __name__ == "__main__":
    raise SystemExit(main())
