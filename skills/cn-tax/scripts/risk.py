#!/usr/bin/env python3
"""cn-tax: 税务风险自检.

Input:  "scenario=id1,id2"   或留空返回全部
Output: JSON {risks: [{id, level, rule}]}
"""

from __future__ import annotations

from cli_common import load_ref, run_kv_cli  # type: ignore[import-not-found]


def build_risks(fields: dict[str, str]) -> dict:
    """Build a list of risk descriptions."""
    raw = fields.get("scenario", "").strip()
    selected_ids = [s.strip() for s in raw.split(",") if s.strip()] if raw else []

    items = load_ref("risk_alerts")["items"]
    by_id = {item["id"]: item for item in items}

    if not selected_ids:
        risks = items
    else:
        unknown = [i for i in selected_ids if i not in by_id]
        if unknown:
            raise ValueError(
                f"unknown risk id(s): {unknown}; valid: {sorted(by_id)}"
            )
        risks = [by_id[i] for i in selected_ids]

    return {
        "risks": risks,
        "warning": "出现以上风险点请优先咨询专业税务师 / 注册会计师，本 skill 仅作提醒",
    }


def main() -> int:
    """Entry point for risk.py."""
    return run_kv_cli(
        'risk.py "scenario=id1,id2,..."  (omit scenario to list all)',
        build_risks,
    )


if __name__ == "__main__":
    raise SystemExit(main())
