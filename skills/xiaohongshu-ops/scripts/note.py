#!/usr/bin/env python3
"""xiaohongshu-ops: 把选题扩成结构化笔记草稿.

Input:  "<topic>|<industry>|<audience>|<tone>"
Output: JSON {title_candidates, cover_copy, body_outline, tags}
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTE_PATH = ROOT / "references" / "note_templates.json"
KEYWORD_PATH = ROOT / "references" / "keyword_seeds.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _format(pattern: str, ctx: dict) -> str:
    out = pattern
    for key, value in ctx.items():
        out = out.replace("{" + key + "}", str(value))
    return out


def build_note(topic: str, industry: str, audience: str, tone: str) -> dict:
    note_seeds = _load(NOTE_PATH)
    keyword_seeds = _load(KEYWORD_PATH)

    tones = note_seeds.get("tones", {})
    tone_meta = tones.get(tone) or tones.get("经验分享")
    emojis = note_seeds.get("default_emojis", ["✨"])
    rng = random.Random(hash(topic) & 0xFFFFFFFF)
    emoji = rng.choice(emojis)

    ctx = {
        "topic": topic,
        "audience": audience or "新手",
        "category": industry or "好物",
        "action": f"做{topic}",
        "n": rng.choice(["3", "5", "7"]),
        "emoji": emoji,
    }

    titles = [_format(pattern, ctx) for pattern in tone_meta["title_patterns"]]
    industry_keywords = keyword_seeds.get("industries", {}).get(industry, {})
    tags = industry_keywords.get("tags", [])

    return {
        "topic": topic,
        "tone": tone,
        "title_candidates": titles,
        "cover_copy": tone_meta["cover_copy"],
        "body_outline": list(tone_meta["body_outline"]),
        "tags": tags,
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: note.py \"<topic>|<industry>|<audience>|<tone>\"", file=sys.stderr)
        return 1
    parts = sys.argv[1].split("|")
    if len(parts) != 4:
        print("error: expected 4 '|'-separated fields", file=sys.stderr)
        return 1
    topic, industry, audience, tone = (part.strip() for part in parts)

    try:
        note = build_note(topic, industry, audience, tone)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(note, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
