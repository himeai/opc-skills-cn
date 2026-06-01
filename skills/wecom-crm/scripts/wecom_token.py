#!/usr/bin/env python3
"""企业微信 access_token 获取与本地缓存（按 module 隔离）."""

from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

from credential import (  # type: ignore[import-not-found]
    get_corp_id,
    get_secret,
    get_token_cache_dir,
)


TOKEN_URL = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
REFRESH_THRESHOLD_SECONDS = 5 * 60


def _cache_path(module: str) -> Path:
    return Path(get_token_cache_dir()) / f"{module}.json"


def _read(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _write(path: Path, data: dict) -> None:
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


def _fetch(corp_id: str, secret: str) -> dict:
    query = urllib.parse.urlencode({"corpid": corp_id, "corpsecret": secret})
    url = f"{TOKEN_URL}?{query}"
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=15) as resp:  # nosec B310 - fixed host
        body = resp.read().decode("utf-8")
    data = json.loads(body)
    if data.get("errcode") not in (None, 0):
        raise RuntimeError(f"gettoken failed: {data}")
    expires_in = int(data.get("expires_in", 7200))
    return {
        "access_token": data["access_token"],
        "expires_in": expires_in,
        "expires_at": int(time.time()) + expires_in,
    }


def get_token(module: str, force_refresh: bool = False) -> str:
    """Return a fresh access_token for the given module."""
    path = _cache_path(module)
    cache = _read(path)
    if not force_refresh and _is_fresh(cache):
        assert cache is not None
        return cache["access_token"]
    fresh = _fetch(get_corp_id(), get_secret(module))
    _write(path, fresh)
    return fresh["access_token"]
