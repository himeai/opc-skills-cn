#!/usr/bin/env python3
"""kuaishou-ops: 60 秒老铁口播脚本生成.

Input:  "<topic>|<style>|<audience>"
Output: JSON {topic, style, audience, sections: {opening, empathy, fact, twist, cta}}
"""

from __future__ import annotations

import json
from pathlib import Path

from cli_common import run_three_field_cli  # type: ignore[import-not-found]


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_PATH = ROOT / "references" / "script_templates.json"


def _load() -> dict:
    return json.loads(TEMPLATES_PATH.read_text(encoding="utf-8"))


def _format(pattern: str, ctx: dict) -> str:
    out = pattern
    for key, value in ctx.items():
        out = out.replace("{" + key + "}", str(value))
    return out


def build_script(topic: str, style: str, audience: str) -> dict:
    data = _load()
    styles = data.get("styles", {})
    style_meta = styles.get(style) or styles.get("老铁")
    fillers = data.get("default_filler", {})

    ctx = {"topic": topic or "今天的事", "audience": audience or "老铁们", **fillers}
    templates = style_meta["templates"]
    sections = {key: _format(templates[key], ctx) for key in data.get("sections", [])}

    return {
        "topic": topic,
        "style": style,
        "style_label": style_meta.get("label", style),
        "audience": audience,
        "tone": style_meta.get("tone", ""),
        "subtitle_style": style_meta.get("subtitle_style", ""),
        "bgm_hint": style_meta.get("bgm_hint", ""),
        "sections": sections,
    }


def main() -> int:
    return run_three_field_cli(
        "script.py \"<topic>|<style>|<audience>\"",
        build_script,
    )


if __name__ == "__main__":
    raise SystemExit(main())
