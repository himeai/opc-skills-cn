#!/usr/bin/env python3
"""cn-festival-calendar: 判断给定日期对该行业是否处于监管 / 平台敏感期.

Input:  "<date>|<industry>"
Output: JSON {date, industry, alerts: [...], safe: bool}
"""

from __future__ import annotations

from datetime import date as _date

from cli_common import (  # type: ignore[import-not-found]
    BLACKOUT_PATH,
    date_in_range,
    load_json,
    parse_date,
    parse_industry,
    run_pipe_cli,
)


def _annual_hits(target: _date, industry: str, data: dict) -> list[dict]:
    out: list[dict] = []
    for item in data.get("annual", []):
        industries = item.get("industries", [])
        if industries and "general" not in industries and industry not in industries:
            continue
        if date_in_range(target, item["start"], item["end"]):
            out.append({
                "id": item["id"],
                "name": item["name"],
                "level": item.get("level", "medium"),
                "industries": industries,
                "blackout_topics": item.get("blackout_topics", []),
                "safe_alternatives": item.get("safe_alternatives", []),
                "law_ref": item.get("law_ref", ""),
            })
    return out


def _platform_hits(target: _date, data: dict) -> list[dict]:
    out: list[dict] = []
    for item in data.get("platform_specific", []):
        for window in item.get("windows", []):
            if date_in_range(target, window["start"], window["end"]):
                out.append({
                    "id": item["id"],
                    "name": item["name"],
                    "platform": item.get("platform", ""),
                    "level": item.get("level", "low"),
                    "blackout_topics": item.get("blackout_topics", []),
                    "safe_alternatives": item.get("safe_alternatives", []),
                })
                break
    return out


def find_blackouts(target: _date, industry: str) -> list[dict]:
    """Return all annual + platform blackout windows that hit the target date / industry."""
    data = load_json(BLACKOUT_PATH)
    return _annual_hits(target, industry, data) + _platform_hits(target, data)


def check(date_arg: str, industry_arg: str) -> dict:
    target = parse_date(date_arg)
    industry = parse_industry(industry_arg)
    alerts = find_blackouts(target, industry)
    high_or_medium = [a for a in alerts if a.get("level") in ("high", "medium")]
    return {
        "date": target.isoformat(),
        "industry": industry,
        "alerts": alerts,
        "safe": len(high_or_medium) == 0,
        "highest_level": _highest(alerts),
    }


def _highest(alerts: list[dict]) -> str:
    order = {"low": 1, "medium": 2, "high": 3}
    best = "none"
    for alert in alerts:
        if order.get(alert.get("level", "low"), 0) > order.get(best, 0):
            best = alert.get("level", "low")
    return best


def main() -> int:
    return run_pipe_cli(
        'blackout.py "<date>|<industry>"',
        2,
        check,
    )


if __name__ == "__main__":
    raise SystemExit(main())
