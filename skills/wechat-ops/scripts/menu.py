#!/usr/bin/env python3
"""Sync WeChat MP custom menu (delete then create).

Usage:
    python3 scripts/menu.py <menu.json>
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.parse
from pathlib import Path

from mp_token import get_token
from wxhttp import cli_error_exit, get_json, post_json


API_BASE = "https://api.weixin.qq.com/cgi-bin"


def delete_menu(access_token: str) -> None:
    url = f"{API_BASE}/menu/delete?access_token={urllib.parse.quote(access_token)}"
    get_json(url)


def create_menu(access_token: str, payload: dict) -> dict:
    url = f"{API_BASE}/menu/create?access_token={urllib.parse.quote(access_token)}"
    return post_json(url, payload)


def main() -> int:  # pylint: disable=too-many-return-statements
    if len(sys.argv) != 2:
        print("usage: menu.py <menu.json>", file=sys.stderr)
        return 1
    menu_path = Path(sys.argv[1])
    if not menu_path.is_file():
        print(f"error: menu file not found: {menu_path}", file=sys.stderr)
        return 1
    try:
        payload = json.loads(menu_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"error: invalid menu JSON: {exc}", file=sys.stderr)
        return 1
    if not isinstance(payload, dict) or "button" not in payload:
        print("error: menu JSON must be an object with 'button' key", file=sys.stderr)
        return 1

    try:
        token = get_token()["access_token"]
        delete_menu(token)
        create_menu(token, payload)
    except (RuntimeError, urllib.error.URLError, OSError, json.JSONDecodeError) as exc:
        return cli_error_exit(exc)

    print(json.dumps(
        {"status": "ok", "buttons": len(payload.get("button", []))},
        ensure_ascii=False,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
