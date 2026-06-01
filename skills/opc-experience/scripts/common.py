#!/usr/bin/env python3
"""Shared helpers for opc-experience scripts."""

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
    s = raw.strip().replace(",", "").replace("¥", "").replace(" ", "")
    if not s:
        raise ValueError("empty number")
    if s.endswith("亿"):
        return int(float(s[:-1]) * 100_000_000)
    if s.endswith("w") or s.endswith("W") or s.endswith("万"):
        return int(float(s[:-1]) * 10_000)
    return int(float(s))


def parse_list(raw: str) -> list[str]:
    return [x.strip() for x in raw.split(",") if x.strip()]


DISCLAIMER = (
    "本工具不推荐具体俱乐部 / 教练 / 中介 / 拍卖行；"
    "极限 / 高奢 / 太空体验请独立完成法律 / 保险 / 体检 / 持牌律师评估。"
)
