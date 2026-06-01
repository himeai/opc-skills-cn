#!/usr/bin/env python3
"""Shared CLI helpers for kuaishou-ops scripts."""

from __future__ import annotations

import json
import sys
from typing import Callable


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
