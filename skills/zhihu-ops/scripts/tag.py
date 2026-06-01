#!/usr/bin/env python3
"""zhihu-ops: 领域 tag 推荐.

Input: domain=AI / 大模型|keywords=AI Agent,Prompt,SaaS|max=5

Output: JSON {tags, related, rules, dropped}
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEXICON = ROOT / "references" / "tag_lexicon.json"


def _load() -> dict:
    return json.loads(LEXICON.read_text(encoding="utf-8"))


def _resolve(keyword: str, clusters: dict[str, list[str]]) -> str | None:
    """Map a free keyword to its canonical tag via cluster aliases."""
    kw = keyword.strip()
    if not kw:
        return None
    for canonical, aliases in clusters.items():
        if kw == canonical:
            return canonical
        for alias in aliases:
            if alias.lower() == kw.lower():
                return canonical
    return None


def recommend_tags(fields: dict[str, str]) -> dict:
    data = _load()
    domain = fields.get("domain", "")
    keywords_csv = fields.get("keywords", "")
    keywords = [k.strip() for k in keywords_csv.split(",") if k.strip()]
    max_per_post = int(fields.get("max", data["tag_rules"]["max_per_post"]))

    clusters = data["tag_clusters"]
    domain_to_tags = data["domain_to_tags"]

    resolved: list[str] = []
    dropped: list[str] = []

    for kw in keywords:
        canonical = _resolve(kw, clusters)
        if canonical and canonical not in resolved:
            resolved.append(canonical)
        elif not canonical:
            dropped.append(kw)

    if domain in domain_to_tags:
        for tag in domain_to_tags[domain]:
            if tag not in resolved:
                resolved.append(tag)

    final_tags = resolved[:max_per_post]
    related = [tag for tag in resolved[max_per_post:]]

    return {
        "domain": domain,
        "tags": final_tags,
        "related_tags": related,
        "dropped": dropped,
        "rules": data["tag_rules"],
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: tag.py 'domain=...|keywords=...,...|max=5'", file=sys.stderr)
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
        result = recommend_tags(fields)
    except (OSError, json.JSONDecodeError, KeyError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
