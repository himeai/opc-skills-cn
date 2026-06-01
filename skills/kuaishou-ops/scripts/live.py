#!/usr/bin/env python3
"""kuaishou-ops: 直播带货 30 分钟话术骨架.

Input:  "<product>|<category>|<audience>"
Output: JSON: {product, category, audience, duration_min, phases: [...]}

合规提示：本输出不包含夸大、绝对化用语；主播仍需对货品质量与广告法合规自行负责。
"""

from __future__ import annotations

import json
from pathlib import Path

from cli_common import run_three_field_cli  # type: ignore[import-not-found]


ROOT = Path(__file__).resolve().parents[1]
LIVE_PATH = ROOT / "references" / "live_templates.json"


def _load() -> dict:
    return json.loads(LIVE_PATH.read_text(encoding="utf-8"))


def _format(pattern: str, ctx: dict) -> str:
    out = pattern
    for key, value in ctx.items():
        out = out.replace("{" + key + "}", str(value))
    return out


def _default_ctx(product: str, category: str, audience: str) -> dict:
    return {
        "product": product or "今天主推款",
        "category": category or "好物",
        "audience": audience or "老铁们",
        "point1": "用料/参数",
        "point2": "使用场景",
        "point3": "性价比",
        "duration": "一段时间",
        "feeling": "确实够用",
        "pain": "踩坑",
        "old_way": "随便挑",
        "old_way_problem": "买回家不合适",
        "market_price": "原价",
        "live_price": "直播间专属价",
        "limit": "100",
        "gift": "搭赠小样",
        "after_sale": "7 天无理由",
        "stock": "200",
        "time": "晚上 8 点",
    }


def build_live(product: str, category: str, audience: str) -> dict:
    data = _load()
    ctx = _default_ctx(product, category, audience)

    phases = []
    for phase in data.get("phases", []):
        phases.append({
            "id": phase["id"],
            "label": phase["label"],
            "minutes": phase["minutes"],
            "goals": phase.get("goals", []),
            "lines": [_format(line, ctx) for line in phase.get("lines", [])],
        })

    return {
        "product": product,
        "category": category,
        "audience": audience,
        "duration_min": data.get("duration_min", 30),
        "phases": phases,
        "compliance_reminders": data.get("compliance_reminders", []),
    }


def main() -> int:
    return run_three_field_cli(
        "live.py \"<product>|<category>|<audience>\"",
        build_live,
    )


if __name__ == "__main__":
    raise SystemExit(main())
