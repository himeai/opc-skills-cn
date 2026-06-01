#!/usr/bin/env python3
"""bilibili-ops: 12 分钟长视频三段式脚本生成.

Input:  "<topic>|<style>|<audience>"
Output: JSON {topic, style, audience, duration_min, sections: {intro, body, outro}}
"""

from __future__ import annotations

from pathlib import Path

from cli_common import (  # type: ignore[import-not-found]
    format_pattern,
    load_json,
    run_three_field_cli,
)


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_PATH = ROOT / "references" / "script_templates.json"


def build_script(topic: str, style: str, audience: str) -> dict:
    data = load_json(TEMPLATES_PATH)
    duration = int(data.get("default_duration_min", 12))
    styles = data.get("styles", {})
    style_meta = styles.get(style) or styles.get("knowhow")
    fillers = data.get("default_filler", {})

    ctx = {
        "topic": topic or "今天的主题",
        "audience": audience or "朋友",
        "duration": str(duration),
        **fillers,
    }

    intro = format_pattern(style_meta["intro_pattern"], ctx)
    outro = format_pattern(style_meta["outro_pattern"], ctx)
    body = [
        {"title": format_pattern(ch["title"], ctx),
         "hook": format_pattern(ch["hook"], ctx)}
        for ch in style_meta.get("body_chapters", [])
    ]

    return {
        "topic": topic,
        "style": style,
        "style_label": style_meta.get("label", style),
        "audience": audience,
        "tone": style_meta.get("tone", ""),
        "duration_min": duration,
        "sections": {"intro": intro, "body": body, "outro": outro},
    }


def main() -> int:
    return run_three_field_cli(
        "script.py \"<topic>|<style>|<audience>\"",
        build_script,
    )


if __name__ == "__main__":
    raise SystemExit(main())
