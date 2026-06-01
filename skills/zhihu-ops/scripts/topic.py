#!/usr/bin/env python3
"""zhihu-ops: 选题工厂.

Input: domain=AI / 大模型|target=AI Agent|year=2026|n=5|industry=AI|scene=客服|benchmark=Copilot

Output: JSON {domain, audiences, suggested_tags, topics:[{angle, title}], quality_filters}
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SEEDS = ROOT / "references" / "topic_seeds.json"


def _load() -> dict:
    return json.loads(SEEDS.read_text(encoding="utf-8"))


def _format(text: str, ctx: dict) -> str:
    out = text
    for key, value in ctx.items():
        out = out.replace("{" + key + "}", str(value))
    return out


def build_topics(fields: dict[str, str]) -> dict:
    data = _load()
    domain_key = fields.get("domain", "互联网产品")
    domain = data["domains"].get(domain_key) or data["domains"]["互联网产品"]

    ctx = {
        "target": fields.get("target", "目标"),
        "year": fields.get("year", "2026"),
        "n": fields.get("n", "5"),
        "industry": fields.get("industry", domain_key),
        "scene": fields.get("scene", "日常工作"),
        "benchmark": fields.get("benchmark", "对照组"),
    }

    rng = random.Random(hash(ctx["target"]) & 0xFFFFFFFF)
    topics: list[dict] = []
    for angle in domain["angles"]:
        chosen = rng.sample(angle["templates"], k=min(2, len(angle["templates"])))
        for tpl in chosen:
            topics.append({
                "angle": angle["angle"],
                "title": _format(tpl, ctx),
            })

    return {
        "domain": domain_key,
        "audiences": list(domain["audiences"]),
        "suggested_tags": list(domain["tags"]),
        "topics": topics,
        "quality_filters": list(data["default_quality_filters"]),
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: topic.py 'domain=...|target=...|year=...'", file=sys.stderr)
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
        result = build_topics(fields)
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
