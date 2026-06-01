#!/usr/bin/env python3
"""zhihu-ops: 专栏长文骨架生成.

Input: topic=...|style=深度分析|industry=AI|year=2026|n=5|target=...|benchmark=...|duration=半年

Output: JSON {topic, style, title_candidates, outline, length_hint}
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "references" / "column_templates.json"


def _load() -> dict:
    return json.loads(TEMPLATES.read_text(encoding="utf-8"))


def _format(text: str, ctx: dict) -> str:
    out = text
    for key, value in ctx.items():
        out = out.replace("{" + key + "}", str(value))
    return out


def build_column(fields: dict[str, str]) -> dict:
    data = _load()
    style_key = fields.get("style", "深度分析")
    style = data["column_styles"].get(style_key) or data["column_styles"]["深度分析"]

    ctx = {
        "topic": fields.get("topic", "话题"),
        "industry": fields.get("industry", "互联网"),
        "year": fields.get("year", "2026"),
        "n": fields.get("n", "5"),
        "target": fields.get("target", fields.get("topic", "目标")),
        "benchmark": fields.get("benchmark", "对照组"),
        "duration": fields.get("duration", "半年"),
    }

    rng = random.Random(hash(ctx["topic"]) & 0xFFFFFFFF)
    titles = [_format(p, ctx) for p in data["title_patterns"]]
    titles = rng.sample(titles, k=min(3, len(titles)))

    return {
        "topic": ctx["topic"],
        "style": style_key,
        "style_label": style["label"],
        "title_candidates": titles,
        "outline": list(style["outline"]),
        "length_hint_chars": list(style["length_hint_chars"]),
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: column.py 'topic=...|style=深度分析|industry=...'", file=sys.stderr)
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
        result = build_column(fields)
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
