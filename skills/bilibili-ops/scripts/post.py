#!/usr/bin/env python3
"""bilibili-ops: 生成 B 站动态或专栏文案.

Input:  "<topic>|<category>|<format>"
Output: JSON {topic, category, format, title, body, tags}
"""

from __future__ import annotations

from pathlib import Path

from cli_common import (  # type: ignore[import-not-found]
    format_pattern,
    load_json,
    run_three_field_cli,
)


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_PATH = ROOT / "references" / "post_templates.json"


def _default_ctx(topic: str, category: str, summary: str) -> dict:
    return {
        "topic": topic or "今天的主题",
        "category": category or "创业",
        "audience": "B 站观众",
        "summary": summary,
        "point1": "把目标拆得足够小",
        "point2": "用最小可行版本试错",
        "point3": "复盘比执行更重要",
        "body": "正文请在脚本基础上补充细节，建议穿插弹幕互动设计、章节切换、案例与图表说明。",
    }


def build_post(topic: str, category: str, fmt: str) -> dict:
    data = load_json(TEMPLATES_PATH)
    formats = data.get("formats", {})
    fmt_meta = formats.get(fmt) or formats.get("动态")
    cat_meta = data.get("categories", {}).get(category, {})

    summary = cat_meta.get("summary", "今天聊一个最近做的事情")
    ctx = _default_ctx(topic, category, summary)

    title = format_pattern(fmt_meta.get("title_pattern", ""), ctx)
    body = format_pattern(fmt_meta.get("body_pattern", ""), ctx)

    tag_count = int(fmt_meta.get("tag_count", 5))
    tags = cat_meta.get("tags", [])[:tag_count]

    return {
        "topic": topic,
        "category": category,
        "format": fmt,
        "format_label": fmt_meta.get("label", fmt),
        "max_chars": int(fmt_meta.get("max_chars", 233)),
        "title": title,
        "body": body,
        "tags": tags,
    }


def main() -> int:
    return run_three_field_cli(
        "post.py \"<topic>|<category>|<format>\"",
        build_post,
    )


if __name__ == "__main__":
    raise SystemExit(main())
