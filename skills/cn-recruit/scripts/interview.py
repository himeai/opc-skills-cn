#!/usr/bin/env python3
"""cn-recruit: 结构化面试题生成.

Input: family=工程|dimensions=技术深度,项目经验,解决问题|primary_stack=Go|product_line=...|channel=小红书

Output: JSON {family, dimensions:[{key, label, weight, questions:[{q, follow_up, look_for}]}], star}
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BANK = ROOT / "references" / "interview_bank.json"


def _load() -> dict:
    return json.loads(BANK.read_text(encoding="utf-8"))


def _format(text: str, ctx: dict) -> str:
    out = text
    for key, value in ctx.items():
        out = out.replace("{" + key + "}", str(value))
    return out


def build_kit(fields: dict[str, str]) -> dict:
    data = _load()
    family = fields.get("family", "通用")
    dim_csv = fields.get("dimensions", "项目经验,解决问题,沟通协作")
    requested_dims = [d.strip() for d in dim_csv.split(",") if d.strip()]

    ctx = {
        "primary_stack": fields.get("primary_stack", "主语言/框架"),
        "product_line": fields.get("product_line", "核心产品线"),
        "channel": fields.get("channel", "全渠道"),
    }

    family_bank = data["banks"].get(family) or data["banks"]["通用"]
    dim_specs = data["dimensions"]

    out_dims: list[dict] = []
    for dim_key in requested_dims:
        dim_spec = dim_specs.get(dim_key)
        if not dim_spec:
            continue
        applicable = dim_spec.get("applicable", [])
        if "all" not in applicable and family not in applicable:
            continue
        questions_raw = family_bank.get(dim_key) \
            or data["banks"]["通用"].get(dim_key) \
            or []
        questions = [
            {
                "q": _format(item["q"], ctx),
                "follow_up": [_format(f, ctx) for f in item.get("follow_up", [])],
                "look_for": item.get("look_for", ""),
            }
            for item in questions_raw
        ]
        out_dims.append({
            "key": dim_key,
            "label": dim_key,
            "weight": dim_spec["weight"],
            "questions": questions,
        })

    return {
        "family": family,
        "dimensions": out_dims,
        "star_template": data["behavioral_star"],
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(
            "usage: interview.py 'family=工程|dimensions=技术深度,项目经验|...'",
            file=sys.stderr,
        )
        return 1
    raw = sys.argv[1].strip()
    fields: dict[str, str] = {}
    for chunk in raw.split("|"):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "=" not in chunk:
            print(f"error: bad field '{chunk}'", file=sys.stderr)
            return 1
        key, value = chunk.split("=", 1)
        fields[key.strip()] = value.strip()

    try:
        result = build_kit(fields)
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
