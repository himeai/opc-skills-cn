#!/usr/bin/env python3
"""Show a single city profile."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]


def load_cities() -> list[dict[str, Any]]:
    with (SKILL_ROOT / "references" / "cities.json").open("r", encoding="utf-8") as file_obj:
        return json.load(file_obj)


def find_city(name: str) -> dict[str, Any] | None:
    for city in load_cities():
        names = [city["city"], *city.get("aliases", [])]
        if name in names:
            return city
    return None


def build_profile(city: dict[str, Any]) -> dict[str, Any]:
    dimensions = city["dimensions"]
    return {
        "status": "ok",
        "city": city["city"],
        "province": city["province"],
        "tier": city["tier"],
        "region": city["region"],
        "monthly_cost_estimate_cny": city["monthly_cost_base"],
        "medical_resource_score": city.get("medical_resource_score"),
        "hukou_friendliness": city.get("hukou_friendliness"),
        "digital_nomad_score": city.get("digital_nomad_score"),
        "dimension_scores": {key: value["score"] for key, value in dimensions.items()},
        "dimension_details": dimensions,
        "policy_links": city.get("policy_links", []),
        "next_steps_template": city.get("next_steps_template", []),
        "data_source_note": city.get("data_source_note", "种子数据，待人工核校"),
        "disclaimer": "城市档案为种子数据，不构成法律、税务、投资或落户建议。",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Show city profile as JSON.")
    parser.add_argument("city", help="Chinese city name")
    args = parser.parse_args()
    city = find_city(args.city)
    if not city:
        print(f"error: city not found: {args.city}", file=sys.stderr)
        return 1
    json.dump(build_profile(city), sys.stdout, ensure_ascii=False, indent=2)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
