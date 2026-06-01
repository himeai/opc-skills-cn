#!/usr/bin/env python3
"""Shared helpers for cn-festival-calendar scripts."""

from __future__ import annotations

import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]
FESTIVALS_PATH = ROOT / "references" / "festivals.json"
BLACKOUT_PATH = ROOT / "references" / "blackout_periods.json"
TIMING_PATH = ROOT / "references" / "platform_timing.json"
DATES_PATH = ROOT / "references" / "dates.json"

ALL_PLATFORMS = ("xiaohongshu", "douyin", "kuaishou", "bilibili", "wechat_mp")
ALL_INDUSTRIES = ("general", "finance", "medical", "cosmetics", "food", "education")


def load_json(path: Path) -> dict:
    """Read a JSON file (UTF-8) and return the parsed dict."""
    return json.loads(path.read_text(encoding="utf-8"))


def parse_date(text: str) -> date:
    """Parse YYYY-MM-DD; default to today on 'today' or empty."""
    text = (text or "").strip().lower()
    if not text or text == "today":
        return date.today()
    return datetime.strptime(text, "%Y-%m-%d").date()


def parse_platforms(text: str) -> list[str]:
    """Parse a comma-separated list of platforms; default to all."""
    text = (text or "").strip()
    if not text or text in {"all", "*"}:
        return list(ALL_PLATFORMS)
    out = []
    for token in text.split(","):
        token = token.strip()
        if token in ALL_PLATFORMS and token not in out:
            out.append(token)
    return out or list(ALL_PLATFORMS)


def parse_industry(text: str) -> str:
    """Normalize industry name; fall back to 'general'."""
    text = (text or "").strip()
    return text if text in ALL_INDUSTRIES else "general"


def lunar_to_solar(year: int, festival_id: str) -> date | None:
    """Look up the Gregorian date for a lunar festival id in a given year."""
    table = load_json(DATES_PATH).get("lunar_to_solar", {})
    year_table = table.get(str(year), {})
    iso = year_table.get(festival_id)
    if not iso:
        return None
    return datetime.strptime(iso, "%Y-%m-%d").date()


def parse_md(token: str, year: int) -> date | None:
    """Parse 'MM-DD' relative to a given year."""
    try:
        month_str, day_str = token.split("-")
        return date(year, int(month_str), int(day_str))
    except (ValueError, KeyError):
        return None


def date_in_range(target: date, start_md: str, end_md: str) -> bool:
    """Check whether target falls within MM-DD..MM-DD (year-agnostic, wraps year)."""
    start = parse_md(start_md, target.year)
    end = parse_md(end_md, target.year)
    if start is None or end is None:
        return False
    if start <= end:
        return start <= target <= end
    # wrap (e.g., 12-20 → 01-25)
    next_year_end = parse_md(end_md, target.year + 1)
    prev_year_start = parse_md(start_md, target.year - 1)
    if next_year_end is not None and start <= target <= date(target.year, 12, 31):
        return True
    if prev_year_start is not None and target <= end:
        return True
    return False


def run_pipe_cli(
    usage: str,
    expected_fields: int,
    builder: Callable[..., dict],
) -> int:
    """Parse '|'-separated argv[1] into N fields, run builder, print JSON."""
    if len(sys.argv) != 2:
        print(f"usage: {usage}", file=sys.stderr)
        return 1
    parts = sys.argv[1].split("|")
    if len(parts) != expected_fields:
        print(
            f"error: expected {expected_fields} '|'-separated fields",
            file=sys.stderr,
        )
        return 1
    fields = [part.strip() for part in parts]

    try:
        result = builder(*fields)
    except (OSError, ValueError, json.JSONDecodeError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False))
    return 0


def festivals_on(target: date) -> list[dict]:
    """Return all festivals on target (solar / lunar / solar_term / ecommerce)."""
    data = load_json(FESTIVALS_PATH)
    out: list[dict] = []

    for item in data.get("solar", []):
        match_date = parse_md(f"{item['month']:02d}-{item['day']:02d}", target.year)
        if match_date == target:
            out.append({
                "id": item["id"],
                "name": item["name"],
                "type": "solar",
                "tier": item.get("tier", "C"),
                "themes": item.get("themes", []),
                "blackout": item.get("blackout", []),
            })

    for item in data.get("lunar", []):
        solar_date = lunar_to_solar(target.year, item["id"])
        if solar_date == target:
            out.append({
                "id": item["id"],
                "name": item["name"],
                "type": "lunar",
                "tier": item.get("tier", "C"),
                "themes": item.get("themes", []),
                "blackout": item.get("blackout", []),
            })

    for item in data.get("solar_term", []):
        match_date = parse_md(
            f"{item['approx_month']:02d}-{item['approx_day']:02d}",
            target.year,
        )
        if match_date == target:
            out.append({
                "id": item["id"],
                "name": item["name"],
                "type": "solar_term",
                "tier": "C",
                "themes": item.get("themes", []),
            })

    for item in data.get("ecommerce", []):
        if date_in_range(target, item["peak_start"], item["peak_end"]):
            out.append({
                "id": item["id"],
                "name": item["name"],
                "type": "ecommerce_peak",
                "tier": item.get("tier", "A"),
                "themes": item.get("themes", []),
            })
        elif date_in_range(target, item["warmup_start"], item["peak_start"]):
            out.append({
                "id": item["id"],
                "name": item["name"] + "（预热期）",
                "type": "ecommerce_warmup",
                "tier": "A",
                "themes": item.get("themes", []),
            })

    return out


def upcoming_festivals(target: date, days_ahead: int) -> list[dict]:
    """List festivals occurring within the next N days, with a 'in_days' annotation."""
    out: list[dict] = []
    for offset in range(1, days_ahead + 1):
        future = target + timedelta(days=offset)
        for fest in festivals_on(future):
            fest = dict(fest)
            fest["date"] = future.isoformat()
            fest["in_days"] = offset
            out.append(fest)
    return out
