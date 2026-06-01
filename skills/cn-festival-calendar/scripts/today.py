#!/usr/bin/env python3
"""cn-festival-calendar: 给定日期的节日 / 内容机会 / 敏感期决策报告.

Input:  "<date>|<industry>|<platforms>"
        - date: YYYY-MM-DD or 'today'
        - industry: general / finance / medical / cosmetics / food / education
        - platforms: comma-separated (xiaohongshu,douyin,...) or 'all'
Output: JSON {date, festivals, content_opportunities, blackout_alerts, upcoming_7d}
"""

from __future__ import annotations

from datetime import date as _date, datetime, timedelta

from cli_common import (  # type: ignore[import-not-found]
    TIMING_PATH,
    festivals_on,
    load_json,
    parse_date,
    parse_industry,
    parse_platforms,
    run_pipe_cli,
    upcoming_festivals,
)
from blackout import find_blackouts  # type: ignore[import-not-found]


def _angles_for(festival_id: str, platform: str, timing: dict) -> list[str]:
    angles_map = timing.get("platform_angles", {})
    if festival_id in angles_map and platform in angles_map[festival_id]:
        return angles_map[festival_id][platform]
    return angles_map.get("_default", {}).get(platform, [])


def _post_by(target_iso: str, lead_days: int) -> str:
    target_date = datetime.fromisoformat(target_iso).date()
    return (target_date - timedelta(days=lead_days)).isoformat()


def _build_opportunities(
    festivals: list[dict],
    upcoming: list[dict],
    platforms: list[str],
    timing: dict,
) -> list[dict]:
    out: list[dict] = []
    platform_meta = timing.get("platforms", {})
    pool: list[tuple[dict, str]] = []
    for fest in festivals:
        pool.append((fest, "今天"))
    for fest in upcoming:
        pool.append((fest, f"还有 {fest['in_days']} 天"))

    for fest, when_label in pool:
        for platform in platforms:
            angles = _angles_for(fest["id"], platform, timing)
            if not angles:
                continue
            lead = platform_meta.get(platform, {}).get("lead_time_days", 7)
            target_iso = fest.get("date") or _date.today().isoformat()
            out.append({
                "festival": fest["name"],
                "festival_id": fest["id"],
                "tier": fest.get("tier", "C"),
                "platform": platform,
                "when": when_label,
                "angles": angles,
                "post_by": _post_by(target_iso, lead),
                "best_windows": platform_meta.get(platform, {}).get(
                    "weekday_windows", [],
                )[:2],
            })
    return out


def report(date_arg: str, industry_arg: str, platforms_arg: str) -> dict:
    target = parse_date(date_arg)
    industry = parse_industry(industry_arg)
    platforms = parse_platforms(platforms_arg)
    timing = load_json(TIMING_PATH)

    today_festivals = festivals_on(target)
    upcoming = upcoming_festivals(target, 14)
    opportunities = _build_opportunities(
        today_festivals, upcoming, platforms, timing,
    )
    blackouts = find_blackouts(target, industry)

    return {
        "date": target.isoformat(),
        "industry": industry,
        "platforms": platforms,
        "festivals": today_festivals,
        "content_opportunities": opportunities,
        "blackout_alerts": blackouts,
        "upcoming_14d": upcoming,
    }


def main() -> int:
    return run_pipe_cli(
        'today.py "<date>|<industry>|<platforms>"',
        3,
        report,
    )


if __name__ == "__main__":
    raise SystemExit(main())
