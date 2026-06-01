#!/usr/bin/env python3
"""douyin-ops: 把口播脚本扩成 6 镜分镜表.

Input:  "<topic>|<style>|<audience>"
Output: JSON {duration_sec, shots: [{index, duration, voiceover, visual, subtitle}]}
"""

from __future__ import annotations

import json
from pathlib import Path

from cli_common import run_three_field_cli  # type: ignore[import-not-found]
from script import build_script  # type: ignore[import-not-found]


ROOT = Path(__file__).resolve().parents[1]
STYLE_META_PATH = ROOT / "references" / "style_meta.json"


def _load_style_meta() -> dict:
    return json.loads(STYLE_META_PATH.read_text(encoding="utf-8"))


def _split_durations(total: int, count: int) -> list[int]:
    base = total // count
    remainder = total - base * count
    durations = [base] * count
    for i in range(remainder):
        durations[i] += 1
    return durations


def _voiceovers_from_sections(sections: dict) -> list[str]:
    return [
        sections.get("opening", ""),
        sections.get("hook", ""),
        sections.get("twist", ""),
        sections.get("twist", ""),
        sections.get("conclusion", ""),
        sections.get("cta", ""),
    ]


def build_storyboard(topic: str, style: str, audience: str) -> dict:
    meta = _load_style_meta()
    duration = int(meta.get("default_duration_sec", 60))
    shot_count = int(meta.get("default_shot_count", 6))
    style_meta = meta.get("styles", {}).get(style) or meta.get("styles", {}).get("knowhow", {})
    visuals = style_meta.get("shot_visuals", [])

    sections = build_script(topic, style, audience)["sections"]
    voiceovers = _voiceovers_from_sections(sections)
    while len(voiceovers) < shot_count:
        voiceovers.append("")
    voiceovers = voiceovers[:shot_count]
    durations = _split_durations(duration, shot_count)

    shots = [
        {
            "index": idx + 1,
            "duration": durations[idx],
            "voiceover": voiceovers[idx],
            "visual": visuals[idx] if idx < len(visuals) else "正脸口播",
            "subtitle": voiceovers[idx],
        }
        for idx in range(shot_count)
    ]

    return {
        "topic": topic,
        "style": style,
        "audience": audience,
        "duration_sec": duration,
        "shot_count": shot_count,
        "subtitle_color": style_meta.get("subtitle_color", "#FFFFFF"),
        "subtitle_bg": style_meta.get("subtitle_bg", "#000000"),
        "subtitle_font_size": style_meta.get("subtitle_font_size", 64),
        "bgm_keyword": style_meta.get("bgm_keyword", ""),
        "shots": shots,
    }


def main() -> int:
    return run_three_field_cli(
        "storyboard.py \"<topic>|<style>|<audience>\"",
        build_storyboard,
    )


if __name__ == "__main__":
    raise SystemExit(main())
