#!/usr/bin/env python3
"""Upload cover image and create a WeChat MP article draft.

Input format (single string, '|' separated):
    "<title>|<author>|<markdown_path>|<cover_path>"

Output: JSON with media_id (cover) and draft media_id.
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.parse
from pathlib import Path

from mp_token import get_token
from wxhttp import cli_error_exit, post_json, post_multipart


API_BASE = "https://api.weixin.qq.com/cgi-bin"


def _markdown_to_html(md_text: str) -> str:
    """Very small md-to-html for headings/paragraphs/lists.

    The WeChat draft API accepts HTML; we only handle the most common
    constructs to keep the skill stdlib-only. Authors who need richer
    formatting should pre-render HTML themselves.
    """
    lines = md_text.splitlines()
    html_parts: list[str] = []
    in_list = False
    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append("")
            continue
        if line.startswith("# "):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append(f"<h1>{line[2:].strip()}</h1>")
        elif line.startswith("## "):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append(f"<h2>{line[3:].strip()}</h2>")
        elif line.startswith("- "):
            if not in_list:
                html_parts.append("<ul>")
                in_list = True
            html_parts.append(f"<li>{line[2:].strip()}</li>")
        else:
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append(f"<p>{line.strip()}</p>")
    if in_list:
        html_parts.append("</ul>")
    return "\n".join(html_parts)


def upload_cover(access_token: str, cover_path: Path) -> str:
    token = urllib.parse.quote(access_token)
    url = f"{API_BASE}/material/add_material?access_token={token}&type=image"
    data = post_multipart(url, cover_path)
    media_id = data.get("media_id")
    if not media_id:
        raise RuntimeError(f"no media_id in response: {data}")
    return media_id


def add_draft(access_token: str, title: str, author: str, html: str, thumb_media_id: str) -> str:
    url = f"{API_BASE}/draft/add?access_token={urllib.parse.quote(access_token)}"
    payload = {
        "articles": [
            {
                "title": title,
                "author": author,
                "content": html,
                "thumb_media_id": thumb_media_id,
                "need_open_comment": 0,
                "only_fans_can_comment": 0,
            }
        ]
    }
    data = post_json(url, payload)
    draft_id = data.get("media_id")
    if not draft_id:
        raise RuntimeError(f"no draft media_id in response: {data}")
    return draft_id


def main() -> int:  # pylint: disable=too-many-return-statements
    if len(sys.argv) != 2:
        print("usage: publish.py \"<title>|<author>|<md_path>|<cover_path>\"", file=sys.stderr)
        return 1
    parts = sys.argv[1].split("|")
    if len(parts) != 4:
        print("error: expected 4 '|'-separated fields", file=sys.stderr)
        return 1

    title, author, md_path_str, cover_path_str = (part.strip() for part in parts)
    md_path = Path(md_path_str)
    cover_path = Path(cover_path_str)
    if not md_path.is_file():
        print(f"error: markdown file not found: {md_path}", file=sys.stderr)
        return 1
    if not cover_path.is_file():
        print(f"error: cover image not found: {cover_path}", file=sys.stderr)
        return 1

    try:
        token = get_token()["access_token"]
        thumb_media_id = upload_cover(token, cover_path)
        html = _markdown_to_html(md_path.read_text(encoding="utf-8"))
        draft_id = add_draft(token, title, author, html, thumb_media_id)
    except (RuntimeError, urllib.error.URLError, OSError, json.JSONDecodeError) as exc:
        return cli_error_exit(exc)

    print(json.dumps(
        {"status": "ok", "media_id": thumb_media_id, "draft_id": draft_id},
        ensure_ascii=False,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
