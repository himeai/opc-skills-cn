#!/usr/bin/env python3
"""Alipay OpenAPI HTTP client with RSA2 signing.

Reference: https://opendocs.alipay.com/open/02e7gq

This is the only module that touches the application private key. All
business scripts go through `call(method, biz_content, ...)`.
"""

from __future__ import annotations

import base64
import json
import time
from typing import Any
from urllib import error as urlerror
from urllib import parse as urlparse
from urllib import request as urlrequest

try:
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "missing dependency: cryptography\ninstall via: pip install cryptography"
    ) from exc

from credential import assert_ready, is_sandbox  # type: ignore[import-not-found]


GATEWAY_PROD = "https://openapi.alipay.com/gateway.do"
GATEWAY_SANDBOX = "https://openapi-sandbox.dl.alipaydev.com/gateway.do"
USER_AGENT = "opc-skills-cn/alipay/0.1.0 (+stdlib+cryptography)"


def _gateway() -> str:
    return GATEWAY_SANDBOX if is_sandbox() else GATEWAY_PROD


def _hash_for(sign_type: str):
    return hashes.SHA256() if sign_type.upper() == "RSA2" else hashes.SHA1()


def _sign(message: str, private_key_pem: str, sign_type: str) -> str:
    pkey = serialization.load_pem_private_key(
        private_key_pem.encode("utf-8"), password=None,
    )
    sig = pkey.sign(
        message.encode("utf-8"),
        padding.PKCS1v15(),
        _hash_for(sign_type),
    )
    return base64.b64encode(sig).decode("ascii")


def _build_string_to_sign(params: dict[str, str]) -> str:
    pairs = sorted((k, v) for k, v in params.items() if v != "" and k != "sign")
    return "&".join(f"{k}={v}" for k, v in pairs)


def build_params(
    method: str,
    biz_content: dict[str, Any],
    notify_url: str | None = None,
    return_url: str | None = None,
) -> dict[str, str]:
    """Return signed common params dict (excluding gateway URL)."""
    creds = assert_ready()
    sign_type = (creds.get("ALIPAY_SIGN_TYPE") or "RSA2").upper()
    params: dict[str, str] = {
        "app_id": creds["ALIPAY_APP_ID"],
        "method": method,
        "format": "JSON",
        "charset": "utf-8",
        "sign_type": sign_type,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "version": "1.0",
        "biz_content": json.dumps(biz_content, ensure_ascii=False, separators=(",", ":")),
    }
    if notify_url:
        params["notify_url"] = notify_url
    if return_url:
        params["return_url"] = return_url
    string_to_sign = _build_string_to_sign(params)
    params["sign"] = _sign(string_to_sign, creds["app_private_key"], sign_type)
    return params


def call(
    method: str,
    biz_content: dict[str, Any],
    notify_url: str | None = None,
) -> dict:
    """POST to alipay gateway and return parsed JSON."""
    params = build_params(method, biz_content, notify_url=notify_url)
    body = urlparse.urlencode(params).encode("utf-8")
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        "Accept": "application/json",
        "User-Agent": USER_AGENT,
    }
    req = urlrequest.Request(_gateway(), data=body, method="POST", headers=headers)
    try:
        with urlrequest.urlopen(req, timeout=30) as resp:  # nosec B310 - fixed host
            raw = resp.read().decode("utf-8")
    except urlerror.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {err_body}") from exc

    try:
        return json.loads(raw) if raw else {}
    except json.JSONDecodeError:
        return {"raw": raw}


def build_redirect_url(
    method: str,
    biz_content: dict[str, Any],
    notify_url: str | None = None,
    return_url: str | None = None,
) -> str:
    """Build a signed GET URL for `alipay.trade.page.pay` / `wap.pay`.

    These two methods don't return JSON; the gateway URL itself is the
    payment page the user gets redirected to.
    """
    params = build_params(method, biz_content, notify_url=notify_url, return_url=return_url)
    return _gateway() + "?" + urlparse.urlencode(params)


def verify_callback(form_fields: dict[str, str]) -> bool:
    """Verify an async notify (POST form-urlencoded) using Alipay's public key."""
    creds = assert_ready(require_alipay_pubkey=True)
    sign = form_fields.get("sign", "")
    sign_type = form_fields.get("sign_type", "RSA2").upper()
    payload = {k: v for k, v in form_fields.items() if k not in ("sign", "sign_type")}
    string_to_verify = _build_string_to_sign(payload)
    pubkey = serialization.load_pem_public_key(
        creds["alipay_public_key"].encode("utf-8"),
    )
    try:
        pubkey.verify(
            base64.b64decode(sign),
            string_to_verify.encode("utf-8"),
            padding.PKCS1v15(),
            _hash_for(sign_type),
        )
        return True
    except (ValueError, TypeError):
        return False
