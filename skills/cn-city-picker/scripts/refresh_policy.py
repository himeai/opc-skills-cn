#!/usr/bin/env python3
"""Placeholder policy refresh command."""

from __future__ import annotations

import argparse
import json
import sys

from credential import has_realtime_credentials


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh policy cache placeholder.")
    parser.add_argument("city", nargs="?", help="Optional city name")
    args = parser.parse_args()
    result = {
        "status": "pending",
        "city": args.city,
        "message": "功能待接入：当前 MVP 不实现政策抓取，仅使用静态种子数据。",
        "has_optional_credentials": has_realtime_credentials(),
        "todo": "后续仅接入政府公开接口或人工维护数据，不实现爬虫、绕过登录或协议逆向。",
    }
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
