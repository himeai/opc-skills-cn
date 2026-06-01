#!/usr/bin/env python3
"""WeChat Pay V3 HTTP client with RSA-SHA256 request signing.

This is the only module that touches credentials and signing logic; all
business scripts go through `request_v3()`.
"""

from __future__ import annotations

import base64
import json
import secrets
import time
from typing import Any
from urllib import error as urlerror
from urllib import request as urlrequest

try:
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "missing dependency: cryptography\n"
        "install via: pip install cryptography"
    ) from exc

from credential import assert_ready  # type: ignore[import-not-found]


API_BASE = "https://api.mch.weixin.qq.com"
USER_AGENT = "opc-skills-cn/wechatpay/0.1.0 (+stdlib+cryptography)"


def _sign(message: str, private_key_pem: str) -> str:
    pkey = serialization.load_pem_private_key(
        private_key_pem.encode("utf-8"), password=None,
    )
    sig = pkey.sign(message.encode("utf-8"), padding.PKCS1v15(), hashes.SHA256())
    return base64.b64encode(sig).decode("ascii")


def _auth_header(method: str, path: str, body: str, creds: dict[str, str]) -> str:
    nonce = secrets.token_hex(16)
    timestamp = str(int(time.time()))
    message = f"{method}\n{path}\n{timestamp}\n{nonce}\n{body}\n"
    signature = _sign(message, creds["private_key"])
    return (
        'WECHATPAY2-SHA256-RSA2048 '
        f'mchid="{creds["WECHATPAY_MCH_ID"]}",'
        f'nonce_str="{nonce}",'
        f'timestamp="{timestamp}",'
        f'serial_no="{creds["WECHATPAY_CERT_SERIAL_NO"]}",'
        f'signature="{signature}"'
    )


def request_v3(method: str, path: str, payload: dict[str, Any] | None = None) -> dict:
    """Send a signed request to WeChat Pay V3 and return parsed JSON."""
    creds = assert_ready()
    method = method.upper()
    body = json.dumps(payload, ensure_ascii=False) if payload is not None else ""
    headers = {
        "Authorization": _auth_header(method, path, body, creds),
        "Accept": "application/json",
        "User-Agent": USER_AGENT,
    }
    if body:
        headers["Content-Type"] = "application/json"

    url = API_BASE + path
    data = body.encode("utf-8") if body else None
    req = urlrequest.Request(url, data=data, method=method, headers=headers)

    try:
        with urlrequest.urlopen(req, timeout=30) as resp:  # nosec B310 - fixed host
            payload_bytes = resp.read()
            return _decode_body(payload_bytes)
    except urlerror.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {err_body}") from exc


def _decode_body(payload_bytes: bytes) -> dict:
    if not payload_bytes:
        return {}
    text = payload_bytes.decode("utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw": text}


def get_app_id(prefer: str | None = None) -> str:
    """Return appid; either from arg, env, or raise."""
    if prefer:
        return prefer
    creds = assert_ready()
    app_id = creds.get("WECHATPAY_APP_ID")
    if not app_id:
        raise RuntimeError(
            "missing WECHATPAY_APP_ID; pass appid=<...> or export the env var"
        )
    return app_id
