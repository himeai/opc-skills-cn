#!/usr/bin/env python3
"""HTTP 客户端（stdlib only）+ KV CLI helper for wecom-crm."""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Callable

from wecom_token import get_token  # type: ignore[import-not-found]


API_BASE = "https://qyapi.weixin.qq.com/cgi-bin"
USER_AGENT = "opc-skills-cn/wecom-crm/0.1.0 (+stdlib)"


def _decode(body: bytes) -> dict:
    if not body:
        return {}
    text = body.decode("utf-8")
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"unexpected response: {text}") from exc
    if isinstance(data, dict) and data.get("errcode") not in (None, 0):
        raise RuntimeError(f"api error: {data}")
    return data


def _build_url(path: str, token: str, query: dict[str, str] | None = None) -> str:
    params = {"access_token": token}
    if query:
        params.update(query)
    return f"{API_BASE}{path}?{urllib.parse.urlencode(params)}"


def call(
    module: str,
    method: str,
    path: str,
    payload: dict[str, Any] | None = None,
    query: dict[str, str] | None = None,
) -> dict:
    """Call a WeCom API endpoint with auto token refresh on 40014/42001."""
    method = method.upper()
    body = (
        json.dumps(payload, ensure_ascii=False).encode("utf-8")
        if payload is not None
        else None
    )
    headers = {"User-Agent": USER_AGENT}
    if body is not None:
        headers["Content-Type"] = "application/json; charset=utf-8"

    for attempt in (1, 2):
        token = get_token(module, force_refresh=(attempt == 2))
        url = _build_url(path, token, query)
        req = urllib.request.Request(url, data=body, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:  # nosec B310
                return _decode(resp.read())
        except urllib.error.HTTPError as exc:
            err_body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP {exc.code}: {err_body}") from exc
        except RuntimeError as exc:
            msg = str(exc)
            if attempt == 1 and ("40014" in msg or "42001" in msg):
                continue
            raise
    raise RuntimeError("unreachable")


def run_kv_cli(usage: str, builder: Callable[[dict[str, str]], dict]) -> int:
    """Parse argv[1] of the form 'k1=v1|k2=v2|...' and dispatch to builder."""
    if len(sys.argv) != 2:
        print(f"usage: {usage}", file=sys.stderr)
        return 1
    raw = sys.argv[1].strip()
    if not raw:
        print(f"usage: {usage}", file=sys.stderr)
        return 1

    fields: dict[str, str] = {}
    for chunk in raw.split("|"):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "=" not in chunk:
            print(f"error: bad field '{chunk}', expected k=v", file=sys.stderr)
            return 1
        key, value = chunk.split("=", 1)
        fields[key.strip()] = value.strip()

    try:
        result = builder(fields)
    except RuntimeError as exc:
        msg = str(exc)
        print(f"error: {msg}", file=sys.stderr)
        if "missing credential" in msg:
            return 2
        return 1
    except (ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False))
    return 0


def require(fields: dict[str, str], *names: str) -> tuple[str, ...]:
    """Return values for required keys or raise."""
    missing = [n for n in names if not fields.get(n)]
    if missing:
        raise ValueError(f"missing fields: {', '.join(missing)}")
    return tuple(fields[n] for n in names)


def parse_list(value: str) -> list[str]:
    """Parse comma-separated list."""
    if not value:
        return []
    return [v.strip() for v in value.split(",") if v.strip()]
