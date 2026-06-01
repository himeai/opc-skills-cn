#!/usr/bin/env python3
"""season.py — 按月份反查推荐目的地。

input format:
  month=4|themes=自然,海岛|continents=亚洲,欧洲
"""

from __future__ import annotations

import json
import sys

from common import DISCLAIMER, load_ref, parse_kv, parse_list


def recommend(input_str: str) -> dict:
    fields = parse_kv(input_str)
    month = int(fields.get("month", "4"))
    themes = parse_list(fields.get("themes", ""))
    continents = parse_list(fields.get("continents", ""))

    if not 1 <= month <= 12:
        raise ValueError("month must be 1..12")

    season_ref = load_ref("seasons.json")
    dests_ref = load_ref("destinations.json")

    month_meta = season_ref["by_month"][str(month)]

    matched = []
    for d in dests_ref["destinations"]:
        if month not in d.get("best_months", []):
            continue
        if continents and d["continent"] not in continents:
            continue
        if themes and not (set(d.get("themes", [])) & set(themes)):
            continue
        matched.append({
            "city": d["city"],
            "country": d["country"],
            "continent": d["continent"],
            "themes": d["themes"],
            "highlights": d["highlights"],
            "stay_days_recommended": d.get("stay_days_recommended", 3),
            "avg_daily_cny_mid": d.get("avg_daily_cny_mid", 1000),
        })

    festivals = [f for f in season_ref["festival_calendar"] if f["month"] == month]

    return {
        "month": month,
        "month_name": month_meta["name"],
        "northern_hemisphere": month_meta["northern_hemisphere"],
        "southern_hemisphere": month_meta["southern_hemisphere"],
        "themes_strong": month_meta.get("themes_strong", []),
        "avoid": month_meta.get("avoid", []),
        "recommended_curated": month_meta.get("recommended", []),
        "all_matched": matched,
        "matched_count": len(matched),
        "festivals_this_month": festivals,
        "hemisphere_swap_tip": season_ref["hemisphere_swap_tip"],
        "disclaimer": DISCLAIMER,
    }


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: season.py 'month=4|themes=...|continents=...'", file=sys.stderr)
        return 2
    try:
        out = recommend(sys.argv[1])
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
