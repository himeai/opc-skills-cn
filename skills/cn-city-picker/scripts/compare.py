#!/usr/bin/env python3
"""Compare multiple Chinese cities."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
DIMENSION_LABELS = {
    "tax_policy": "税收",
    "living_cost": "生活成本",
    "startup_policy": "创业政策",
    "climate": "气候",
    "digital_infra": "数字基建",
    "industry": "产业",
    "talent": "人才",
    "admin_efficiency": "行政效率",
}


def load_cities() -> list[dict[str, Any]]:
    with (SKILL_ROOT / "references" / "cities.json").open("r", encoding="utf-8") as file_obj:
        return json.load(file_obj)


def city_lookup() -> dict[str, dict[str, Any]]:
    lookup: dict[str, dict[str, Any]] = {}
    for city in load_cities():
        lookup[city["city"]] = city
        for alias in city.get("aliases", []):
            lookup[alias] = city
    return lookup


def markdown_table(cities: list[dict[str, Any]]) -> str:
    headers = ["城市", "省份", "等级", "月成本估算", *DIMENSION_LABELS.values(), "数字游民", "数据说明"]
    rows = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for city in cities:
        dims = city["dimensions"]
        values = [
            city["city"],
            city["province"],
            city["tier"],
            str(city["monthly_cost_base"]),
            *[str(dims[key]["score"]) for key in DIMENSION_LABELS],
            str(city.get("digital_nomad_score", "")),
            city.get("data_source_note", "种子数据，待人工核校"),
        ]
        rows.append("| " + " | ".join(values) + " |")
    return "\n".join(rows)


def radar_data(cities: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    return {
        city["city"]: {
            label: city["dimensions"][key]["score"]
            for key, label in DIMENSION_LABELS.items()
        }
        for city in cities
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare cities with Markdown table and radar data."
    )
    parser.add_argument("cities", nargs="+", help="Chinese city names")
    args = parser.parse_args()
    lookup = city_lookup()
    selected = []
    missing = []
    for name in args.cities:
        city = lookup.get(name)
        if city:
            selected.append(city)
        else:
            missing.append(name)
    if missing:
        print(f"error: city not found: {', '.join(missing)}", file=sys.stderr)
        return 1
    print(markdown_table(selected))
    print("\n## 雷达图原始数据")
    print("```json")
    json.dump(radar_data(selected), sys.stdout, ensure_ascii=False, indent=2)
    print("\n```")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
