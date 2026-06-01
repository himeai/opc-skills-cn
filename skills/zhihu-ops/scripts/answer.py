#!/usr/bin/env python3
"""zhihu-ops: 知乎长回答结构化生成.

Input (`|` 分隔，`=` 键值):
  question=如何评价 X？|style=科普|industry=AI|years=4|column_name=AI Agent 周记

Output: JSON {question, style, hook_candidates, outline:[{section, guide}], modules, length_hint, closing_candidates}
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "references" / "answer_templates.json"


def _load() -> dict:
    return json.loads(TEMPLATES.read_text(encoding="utf-8"))


def _format(text: str, ctx: dict) -> str:
    out = text
    for key, value in ctx.items():
        out = out.replace("{" + key + "}", str(value))
    return out


def build_answer(fields: dict[str, str]) -> dict:
    data = _load()
    style_key = fields.get("style", "干货")
    style = data["answer_styles"].get(style_key) or data["answer_styles"]["干货"]

    ctx = {
        "industry": fields.get("industry", "互联网"),
        "years": fields.get("years", "3"),
        "column_name": fields.get("column_name", "我的专栏"),
    }

    rng = random.Random(hash(fields.get("question", "")) & 0xFFFFFFFF)
    hooks = data["common_modules"]["钩子模式"]
    closings = data["common_modules"]["结尾互动模板"]

    return {
        "question": fields.get("question", ""),
        "style": style_key,
        "style_label": style["label"],
        "hook_candidates": [_format(h, ctx) for h in rng.sample(hooks, k=min(3, len(hooks)))],
        "outline": list(style["outline"]),
        "structured_quote_modules": list(data["common_modules"]["结构化引用模式"]),
        "length_hint_chars": list(style["length_hint_chars"]),
        "closing_candidates": [_format(c, ctx) for c in rng.sample(closings, k=min(2, len(closings)))],
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: answer.py 'question=...|style=科普|industry=...'", file=sys.stderr)
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
        result = build_answer(fields)
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
