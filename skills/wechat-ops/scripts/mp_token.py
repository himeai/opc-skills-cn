#!/usr/bin/env python3
"""Fetch & cache WeChat Official Account access_token.

Usage:
    python3 scripts/token.py            # fetch (or refresh if expiring) and print token info
    python3 scripts/token.py --check    # verify cached token without forcing refresh
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from credential import require_credentials


TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token"
REFRESH_THRESHOLD_SECONDS = 5 * 60


def _http_get_json(url: str) -> dict:
    request = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(request, timeout=15) as response:
        body = response.read().decode("utf-8")
    data = json.loads(body)
    if not isinstance(data, dict):
        raise RuntimeError(f"unexpected response: {body}")
    return data


def _read_cache(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _write_cache(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def _is_fresh(cache: dict | None) -> bool:
    if not cache:
        return False
    expires_at = cache.get("expires_at")
    token = cache.get("access_token")
    if not isinstance(expires_at, (int, float)) or not isinstance(token, str):
        return False
    return expires_at - time.time() > REFRESH_THRESHOLD_SECONDS


def fetch_token(app_id: str, app_secret: str) -> dict:
    query = urllib.parse.urlencode(
        {"grant_type": "client_credential", "appid": app_id, "secret": app_secret}
    )
    data = _http_get_json(f"{TOKEN_URL}?{query}")
    if "access_token" not in data:
        raise RuntimeError(f"fetch token failed: {data}")
    expires_in = int(data.get("expires_in", 7200))
    return {
        "access_token": data["access_token"],
        "expires_in": expires_in,
        "expires_at": int(time.time()) + expires_in,
    }


def get_token(force_refresh: bool = False) -> dict:
    creds = require_credentials()
    cache_path = Path(creds["token_cache"])
    cache = _read_cache(cache_path)
    if not force_refresh and _is_fresh(cache):
        assert cache is not None
        return cache
    fresh = fetch_token(creds["app_id"], creds["app_secret"])
    _write_cache(cache_path, fresh)
    return fresh


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch/cache WeChat MP access_token.")
    parser.add_argument("--check", action="store_true",
                        help="only check the cached token validity without refreshing")
    args = parser.parse_args()

    try:
        if args.check:
            creds = require_credentials()
            cache = _read_cache(Path(creds["token_cache"]))
            fresh = _is_fresh(cache)
            payload = {
                "status": "ok" if fresh else "expired",
                "fresh": fresh,
                "remaining_seconds": (
                    int(cache["expires_at"] - time.time()) if fresh and cache else 0
                ),
            }
        else:
            token = get_token()
            payload = {
                "status": "ok",
                "access_token_prefix": token["access_token"][:6] + "***",
                "expires_at": token["expires_at"],
                "remaining_seconds": int(token["expires_at"] - time.time()),
            }
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except (urllib.error.URLError, OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
