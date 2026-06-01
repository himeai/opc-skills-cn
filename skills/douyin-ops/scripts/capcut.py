#!/usr/bin/env python3
"""douyin-ops: 把分镜导出为剪映 (CapCut) 工程 JSON 骨架.

Input:  "<topic>|<style>|<audience>"
Output: JSON: {project, tracks: [{type, items: [...]}, ...]}

仅作骨架参考，剪映闭源格式可能版本变更，正式导入需用户对齐自己版本。
"""

from __future__ import annotations

import uuid

from cli_common import run_three_field_cli  # type: ignore[import-not-found]
from storyboard import build_storyboard  # type: ignore[import-not-found]


def _ms(seconds: int) -> int:
    return seconds * 1000


def build_capcut(topic: str, style: str, audience: str) -> dict:
    sb = build_storyboard(topic, style, audience)
    duration_ms = _ms(sb["duration_sec"])

    cursor = 0
    video_items = []
    subtitle_items = []
    for shot in sb["shots"]:
        shot_ms = _ms(shot["duration"])
        video_items.append({
            "id": uuid.uuid4().hex,
            "shot_index": shot["index"],
            "start": cursor,
            "duration": shot_ms,
            "placeholder_visual": shot["visual"],
        })
        subtitle_items.append({
            "id": uuid.uuid4().hex,
            "shot_index": shot["index"],
            "start": cursor,
            "duration": shot_ms,
            "text": shot["subtitle"],
        })
        cursor += shot_ms

    return {
        "schema": "douyin-ops-capcut-skeleton-v1",
        "project": {
            "id": uuid.uuid4().hex,
            "name": f"{topic or 'untitled'}-{style or 'knowhow'}",
            "duration": duration_ms,
            "fps": 30,
            "resolution": {"width": 1080, "height": 1920},
        },
        "style": {
            "subtitle_color": sb.get("subtitle_color", "#FFFFFF"),
            "subtitle_bg": sb.get("subtitle_bg", "#000000"),
            "subtitle_font_size": sb.get("subtitle_font_size", 64),
            "bgm_keyword": sb.get("bgm_keyword", ""),
        },
        "tracks": [
            {"type": "video_placeholder", "items": video_items},
            {"type": "subtitle", "items": subtitle_items},
        ],
        "notes": [
            "本 JSON 仅为骨架参考；剪映正式工程格式以剪映客户端导出为准。",
            "video_placeholder 为占位轨：用户在剪映里替换为真实素材。",
        ],
    }


def main() -> int:
    return run_three_field_cli(
        "capcut.py \"<topic>|<style>|<audience>\"",
        build_capcut,
    )


if __name__ == "__main__":
    raise SystemExit(main())
