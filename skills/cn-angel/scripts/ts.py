#!/usr/bin/env python3
"""cn-angel: Term Sheet 条款解读 + 谈判建议.

Input (`|` 分隔，`=` 键值):
  - 列出所有条款：term=all
  - 解读单个：term=优先清算 | term=对赌
  - 解读多个：term=优先清算,反稀释,回购

Output: JSON {clauses:[{name, market_standard, aggressive, negotiation_room, warn_level, ...}]}
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "references" / "ts_clauses.json"


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


def _fmt_clause(name: str, meta: dict) -> dict:
    return {
        "name": name,
        "key": meta["key"],
        "what": meta["what"],
        "market_standard": meta["market_standard"],
        "aggressive": meta["aggressive"],
        "negotiation_room": meta["negotiation_room"],
        "warn_level": meta["warn_level"],
    }


def explain_terms(fields: dict[str, str]) -> dict:
    data = _load()
    clauses = data["clauses"]
    levels = data["warn_level_meaning"]
    requested = fields.get("term", "all").strip()

    if requested == "all" or requested == "":
        names = list(clauses.keys())
    else:
        names = [n.strip() for n in requested.split(",") if n.strip()]

    output = []
    unknown = []
    for name in names:
        if name in clauses:
            output.append(_fmt_clause(name, clauses[name]))
        else:
            unknown.append(name)

    return {
        "requested": names,
        "unknown_terms": unknown,
        "clauses": output,
        "warn_level_meaning": levels,
        "available_terms": list(clauses.keys()),
        "disclaimer": "本解读仅作谈判参考，正式 TS 与 SPA 必须由专业律师起草和审查。",
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: ts.py 'term=优先清算' | term=all", file=sys.stderr)
        return 1
    try:
        fields = _parse_kv(sys.argv[1].strip())
        result = explain_terms(fields)
    except (OSError, json.JSONDecodeError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
