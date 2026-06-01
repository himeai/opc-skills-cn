#!/usr/bin/env python3
"""Shared CLI helpers for wechatpay scripts."""

from __future__ import annotations

import json
import sys
from typing import Callable


def run_kv_cli(usage: str, builder: Callable[[dict[str, str]], dict]) -> int:
    """Parse argv[1] of the form 'k1=v1|k2=v2|...' and dispatch to builder."""
    if len(sys.argv) != 2:
        print(f"usage: {usage}", file=sys.stderr)
        return 1
    raw = sys.argv[1].strip()
    if not raw:
        print(f"usage: {usage}", file=sys.stderr)
        return 1

    fields: dict[str, str] = {}
    for chunk in raw.split("|"):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "=" not in chunk:
            print(f"error: bad field '{chunk}', expected k=v", file=sys.stderr)
            return 1
        key, value = chunk.split("=", 1)
        fields[key.strip()] = value.strip()

    try:
        result = builder(fields)
    except (RuntimeError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False))
    return 0


def require(fields: dict[str, str], *names: str) -> tuple[str, ...]:
    """Return values for required keys or raise."""
    missing = [n for n in names if not fields.get(n)]
    if missing:
        raise ValueError(f"missing fields: {', '.join(missing)}")
    return tuple(fields[n] for n in names)
