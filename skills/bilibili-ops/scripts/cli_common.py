#!/usr/bin/env python3
"""Shared CLI helpers for bilibili-ops scripts."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Callable


def load_json(path: Path) -> dict:
    """Read a JSON file (UTF-8) and return the parsed dict."""
    return json.loads(path.read_text(encoding="utf-8"))


def format_pattern(pattern: str, ctx: dict) -> str:
    """Substitute {key} placeholders from ctx into pattern."""
    out = pattern
    for key, value in ctx.items():
        out = out.replace("{" + key + "}", str(value))
    return out


def run_three_field_cli(
    usage: str,
    builder: Callable[[str, str, str], dict],
) -> int:
    """Parse a single '|'-separated string with 3 fields, run builder, print JSON."""
    if len(sys.argv) != 2:
        print(f"usage: {usage}", file=sys.stderr)
        return 1
    parts = sys.argv[1].split("|")
    if len(parts) != 3:
        print("error: expected 3 '|'-separated fields", file=sys.stderr)
        return 1
    field_a, field_b, field_c = (part.strip() for part in parts)

    try:
        result = builder(field_a, field_b, field_c)
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False))
    return 0
