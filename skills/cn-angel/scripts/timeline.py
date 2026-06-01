#!/usr/bin/env python3
"""cn-angel: 12 周融资时间表 + 关键节点 + SLA 告警.

Input (`|` 分隔，`=` 键值):
  start_date=2026-06-01|target_close_weeks=12

Output: JSON {timeline:[{week, date, name, deliverables, common_blockers}], sla_alerts}
"""

from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "references" / "timeline_milestones.json"


def _load() -> dict:
    return json.loads(TEMPLATES.read_text(encoding="utf-8"))


def _parse_kv(raw: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for chunk in raw.split("|"):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "=" not in chunk:
            raise ValueError(f"bad field '{chunk}'")
        key, value = chunk.split("=", 1)
        fields[key.strip()] = value.strip()
    return fields


def _parse_date(s: str) -> datetime.date:
    return datetime.date.fromisoformat(s)


def build_timeline(fields: dict[str, str]) -> dict:
    data = _load()
    start_str = fields.get("start_date", datetime.date.today().isoformat())
    try:
        start = _parse_date(start_str)
    except ValueError as exc:
        raise ValueError(f"bad start_date '{start_str}': {exc}") from exc

    target_str = fields.get("target_close_weeks", str(data["default_total_weeks"]))
    try:
        target_weeks = int(target_str)
    except ValueError as exc:
        raise ValueError(f"bad target_close_weeks '{target_str}': {exc}") from exc

    scale = target_weeks / data["default_total_weeks"]

    timeline = []
    for ms in data["milestones"]:
        week = round(ms["week_offset"] * scale, 1)
        date = start + datetime.timedelta(days=int(week * 7))
        timeline.append({
            "week_offset": week,
            "date": date.isoformat(),
            "name": ms["name"],
            "deliverables": list(ms["deliverables"]),
            "common_blockers": list(ms["common_blockers"]),
        })

    sla_alerts = []
    for name, alert in data["sla_alerts"].items():
        if not isinstance(alert, dict):
            continue
        max_week = round(alert["max_weeks"] * scale, 1)
        sla_alerts.append({
            "milestone": name,
            "max_week_offset": max_week,
            "deadline_date": (start + datetime.timedelta(days=int(max_week * 7))).isoformat(),
            "alert": alert["alert"],
        })

    target_close_date = start + datetime.timedelta(days=int(target_weeks * 7))

    return {
        "start_date": start.isoformat(),
        "target_close_weeks": target_weeks,
        "target_close_date": target_close_date.isoformat(),
        "timeline": timeline,
        "sla_alerts": sla_alerts,
        "tips": [
            "周一发周报给所有进行中投资人（不暴露具体数字）",
            "保留 1-2 周 buffer 应对 ODI / 工商变更延期",
            "拿到首份 TS 后给其他机构 7-10 天决策窗口",
            "DD 阶段所有材料过律师 + 财务两道",
        ],
        "disclaimer": "本时间表仅作排期参考，实际节奏取决于投资人 IC 节奏和市场环境。",
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(
            "usage: timeline.py 'start_date=2026-06-01|target_close_weeks=12'",
            file=sys.stderr,
        )
        return 1
    try:
        fields = _parse_kv(sys.argv[1].strip())
        result = build_timeline(fields)
    except (OSError, json.JSONDecodeError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
