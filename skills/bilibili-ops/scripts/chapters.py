#!/usr/bin/env python3
"""bilibili-ops: 把脚本切为章节大纲（含时间码）.

Input:  "<topic>|<style>|<audience>"
Output: JSON {duration_min, chapters: [{index, start_sec, title, hook}]}
"""

from __future__ import annotations

from pathlib import Path

from cli_common import load_json, run_three_field_cli  # type: ignore[import-not-found]
from script import build_script  # type: ignore[import-not-found]


ROOT = Path(__file__).resolve().parents[1]
META_PATH = ROOT / "references" / "chapter_meta.json"


def _load_meta() -> dict:
    return load_json(META_PATH)


def _split_durations(total: int, count: int) -> list[int]:
    base = total // count
    remainder = total - base * count
    durations = [base] * count
    for i in range(remainder):
        durations[i] += 1
    return durations


def _format_timecode(total_sec: int) -> str:
    minutes = total_sec // 60
    seconds = total_sec % 60
    return f"{minutes:02d}:{seconds:02d}"


def _build_titles_and_hooks(
    script: dict,
    intro_label: str,
    outro_label: str,
    chapter_count: int,
) -> tuple[list[str], list[str]]:
    body = script["sections"]["body"]
    titles = [intro_label] + [ch["title"] for ch in body] + [outro_label]
    intro_hook = script["sections"]["intro"]
    outro_hook = script["sections"]["outro"]
    hooks = [intro_hook] + [ch["hook"] for ch in body] + [outro_hook]
    titles = titles[:chapter_count]
    hooks = hooks[:chapter_count]
    while len(titles) < chapter_count:
        titles.append("正文")
        hooks.append("继续讲解")
    return titles, hooks


def _assemble_chapters(
    titles: list[str],
    hooks: list[str],
    durations_sec: list[int],
) -> list[dict]:
    chapters = []
    cursor = 0
    for idx, dur in enumerate(durations_sec):
        chapters.append({
            "index": idx + 1,
            "start_sec": cursor,
            "start_tc": _format_timecode(cursor),
            "duration_sec": dur,
            "title": titles[idx],
            "hook": hooks[idx],
        })
        cursor += dur
    return chapters


def build_chapters(topic: str, style: str, audience: str) -> dict:
    meta = _load_meta()
    duration_min = int(meta.get("default_duration_min", 12))
    chapter_count = int(meta.get("default_chapter_count", 6))
    intro_label = meta.get("intro_label", "开场")
    outro_label = meta.get("outro_label", "总结")

    script = build_script(topic, style, audience)
    titles, hooks = _build_titles_and_hooks(
        script, intro_label, outro_label, chapter_count,
    )
    durations_sec = _split_durations(duration_min * 60, chapter_count)
    chapters = _assemble_chapters(titles, hooks, durations_sec)

    return {
        "topic": topic,
        "style": style,
        "audience": audience,
        "duration_min": duration_min,
        "chapter_count": chapter_count,
        "chapters": chapters,
    }


def main() -> int:
    return run_three_field_cli(
        "chapters.py \"<topic>|<style>|<audience>\"",
        build_chapters,
    )


if __name__ == "__main__":
    raise SystemExit(main())
