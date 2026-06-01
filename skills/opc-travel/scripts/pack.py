#!/usr/bin/env python3
"""pack.py — 跨气候打包清单生成。

input format:
  climates=tropical,alpine|themes=diving,trekking|days=21
"""

from __future__ import annotations

import json
import sys

from common import DISCLAIMER, load_ref, parse_kv, parse_int, parse_list


def pack(input_str: str) -> dict:
    fields = parse_kv(input_str)
    climates = parse_list(fields.get("climates", ""))
    themes = parse_list(fields.get("themes", ""))
    days = parse_int(fields.get("days", "14"))

    ref = load_ref("packing.json")

    base = ref["base_kit"]

    climate_modules = []
    for c in climates:
        if c in ref["climate_modules"]:
            climate_modules.append(ref["climate_modules"][c])

    theme_modules = []
    for t in themes:
        if t in ref["theme_modules"]:
            theme_modules.append(ref["theme_modules"][t])

    # 行李策略
    if days <= 14:
        lug = ref["luggage_strategy"]["短期 ≤ 14 天"]
        bracket = "短期 ≤ 14 天"
    elif days <= 45:
        lug = ref["luggage_strategy"]["中期 15-45 天"]
        bracket = "中期 15-45 天"
    elif days <= 90:
        lug = ref["luggage_strategy"]["长期 > 45 天"]
        bracket = "长期 > 45 天"
    else:
        lug = ref["luggage_strategy"]["环球 > 90 天"]
        bracket = "环球 > 90 天"

    return {
        "climates_input": climates,
        "themes_input": themes,
        "days": days,
        "duration_bracket": bracket,
        "luggage_strategy": lug,
        "base_kit": base,
        "climate_modules": climate_modules,
        "theme_modules": theme_modules,
        "tsa_redlines": ref["tsa_redlines"],
        "disclaimer": DISCLAIMER,
    }


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: pack.py 'climates=tropical,alpine|themes=diving,trekking|days=21'", file=sys.stderr)
        return 2
    try:
        out = pack(sys.argv[1])
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
