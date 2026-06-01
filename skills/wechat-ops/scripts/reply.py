#!/usr/bin/env python3
"""Send a customer-service text message within the 48-hour window.

Usage:
    python3 scripts/reply.py "<openid>|<text>"
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.parse

from mp_token import get_token
from wxhttp import cli_error_exit, post_json


API_URL = "https://api.weixin.qq.com/cgi-bin/message/custom/send"


def send_text(access_token: str, openid: str, text: str) -> dict:
    url = f"{API_URL}?access_token={urllib.parse.quote(access_token)}"
    payload = {
        "touser": openid,
        "msgtype": "text",
        "text": {"content": text},
    }
    return post_json(url, payload)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: reply.py \"<openid>|<text>\"", file=sys.stderr)
        return 1
    parts = sys.argv[1].split("|", 1)
    if len(parts) != 2 or not parts[0].strip() or not parts[1].strip():
        print("error: expected '<openid>|<text>' with both parts non-empty", file=sys.stderr)
        return 1
    openid = parts[0].strip()
    text = parts[1].strip()
    if len(text) > 600:
        print("error: text exceeds 600 character soft limit", file=sys.stderr)
        return 1

    try:
        token = get_token()["access_token"]
        send_text(token, openid, text)
    except (RuntimeError, urllib.error.URLError, OSError, json.JSONDecodeError) as exc:
        return cli_error_exit(exc)

    print(json.dumps({"status": "ok", "touser": openid}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
