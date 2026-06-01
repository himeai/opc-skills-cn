#!/usr/bin/env python3
"""cn-festival-calendar: 给定节日生成多平台错峰发布排期表.

Input:  "<festival_id>|<industry>|<platforms>"
        festival_id: chunjie / duanwu / zhongqiu / 618 / shuang_shi_yi / ...
Output: JSON {festival, target_date, schedule: [...], notes}
"""

from __future__ import annotations

from datetime import date as _date, timedelta

from cli_common import (  # type: ignore[import-not-found]
    FESTIVALS_PATH,
    TIMING_PATH,
    load_json,
    lunar_to_solar,
    parse_industry,
    parse_md,
    parse_platforms,
    run_pipe_cli,
)


def _resolve_festival(fest_id: str, year: int) -> tuple[str, _date | None, dict]:
    """Resolve festival id to (display_name, anchor_date, meta)."""
    data = load_json(FESTIVALS_PATH)

    for item in data.get("solar", []):
        if item["id"] == fest_id:
            anchor = parse_md(f"{item['month']:02d}-{item['day']:02d}", year)
            if anchor is not None and anchor < _date.today():
                anchor = parse_md(f"{item['month']:02d}-{item['day']:02d}", year + 1)
            return item["name"], anchor, item

    for item in data.get("lunar", []):
        if item["id"] == fest_id:
            anchor = lunar_to_solar(year, fest_id)
            if anchor is not None and anchor < _date.today():
                anchor = lunar_to_solar(year + 1, fest_id)
            return item["name"], anchor, item

    for item in data.get("ecommerce", []):
        if item["id"] == fest_id:
            anchor = parse_md(item["peak_end"], year)
            if anchor is not None and anchor < _date.today():
                anchor = parse_md(item["peak_end"], year + 1)
            return item["name"], anchor, item

    raise KeyError(f"unknown festival id: {fest_id}")


def _angles_for(festival_id: str, platform: str, timing: dict) -> list[str]:
    angles_map = timing.get("platform_angles", {})
    if festival_id in angles_map and platform in angles_map[festival_id]:
        return angles_map[festival_id][platform]
    return angles_map.get("_default", {}).get(platform, [])


def _build_schedule_row(
    platform: str,
    anchor: _date,
    timing: dict,
    festival_id: str,
) -> dict:
    platform_meta = timing.get("platforms", {}).get(platform, {})
    lead = platform_meta.get("lead_time_days", 7)
    post_by = anchor - timedelta(days=lead)
    return {
        "platform": platform,
        "platform_display": platform_meta.get("display_name", platform),
        "post_by": post_by.isoformat(),
        "festival_date": anchor.isoformat(),
        "lead_time_days": lead,
        "angles": _angles_for(festival_id, platform, timing),
        "best_post_types": platform_meta.get("best_post_types", []),
        "weekday_windows": platform_meta.get("weekday_windows", []),
        "weekend_windows": platform_meta.get("weekend_windows", []),
        "notes": platform_meta.get("notes", ""),
    }


def plan(festival_arg: str, industry_arg: str, platforms_arg: str) -> dict:
    industry = parse_industry(industry_arg)
    platforms = parse_platforms(platforms_arg)
    festival_id = festival_arg.strip()
    today = _date.today()
    name, anchor, meta = _resolve_festival(festival_id, today.year)
    if anchor is None:
        raise ValueError(f"could not resolve date for festival: {festival_id}")

    timing = load_json(TIMING_PATH)
    schedule = [
        _build_schedule_row(platform, anchor, timing, festival_id)
        for platform in platforms
    ]
    schedule.sort(key=lambda row: row["post_by"])

    days_to_go = (anchor - today).days
    return {
        "festival": name,
        "festival_id": festival_id,
        "festival_date": anchor.isoformat(),
        "days_to_go": days_to_go,
        "industry": industry,
        "tier": meta.get("tier", "C"),
        "themes": meta.get("themes", []),
        "blackout_topics": meta.get("blackout", []),
        "schedule": schedule,
        "earliest_action": schedule[0]["post_by"] if schedule else None,
    }


def main() -> int:
    return run_pipe_cli(
        'plan.py "<festival_id>|<industry>|<platforms>"',
        3,
        plan,
    )


if __name__ == "__main__":
    raise SystemExit(main())
