#!/usr/bin/env python3
"""Shared helpers for opc-property scripts."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFS = ROOT / "references"


def load_ref(name: str) -> dict:
    return json.loads((REFS / name).read_text(encoding="utf-8"))


def parse_kv(raw: str) -> dict[str, str]:
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


def parse_int_cny(raw: str) -> int:
    """Parse '1000w' / '1.2 亿' / '12000000' style budget strings into CNY int."""
    s = raw.strip().replace(",", "").replace("¥", "").replace(" ", "")
    if not s:
        raise ValueError("empty budget")
    if s.endswith("亿"):
        return int(float(s[:-1]) * 100_000_000)
    if s.endswith("w") or s.endswith("W") or s.endswith("万"):
        return int(float(s[:-1]) * 10_000)
    return int(float(s))


DISCLAIMER = (
    "本工具仅作信息整理与本地推理，不构成投资 / 移民 / 税务 / 法律建议。"
    "请以当地律师 / 持牌中介 / 银行私行 / 税务师测算为准。"
)
