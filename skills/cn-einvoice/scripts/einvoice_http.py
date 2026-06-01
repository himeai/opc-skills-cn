#!/usr/bin/env python3
"""HTTP / signing layer for cn-einvoice providers.

Both 诺诺 and 百望 use HMAC-style signed JSON over HTTPS. We avoid pulling in
their official SDKs (heavy and provider-locked) and re-implement the minimal
contract using stdlib only. If the provider's signing rule is updated, only
this module needs to change.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import secrets
import time
from typing import Any
from urllib import error as urlerror
from urllib import parse as urlparse
from urllib import request as urlrequest

from credential import assert_ready  # type: ignore[import-not-found]


USER_AGENT = "opc-skills-cn/cn-einvoice/0.1.0 (+stdlib)"

_PROVIDER_BASE = {
    "nuonuo": {
        "prod": "https://sdk.nuonuo.com/open/v1/services",
        "sandbox": "https://sandbox.nuonuocs.cn/open/v1/services",
    },
    "baiwang": {
        "prod": "https://openapi.baiwang.com/router/rest",
        "sandbox": "https://sandbox.baiwang.com/router/rest",
    },
}


def _is_sandbox(creds: dict[str, str]) -> bool:
    return (creds.get("CN_EINVOICE_SANDBOX") or "").lower() in ("1", "true", "yes")


def _base_url(creds: dict[str, str]) -> str:
    provider = creds["provider"]
    env = "sandbox" if _is_sandbox(creds) else "prod"
    return _PROVIDER_BASE[provider][env]


def _sign_nuonuo(
    method_name: str,
    body: str,
    creds: dict[str, str],
) -> tuple[dict[str, str], str]:
    """Build query params + Authorization header for 诺诺.

    Reference: https://open.nuonuo.com/document
    Signature = HMAC-SHA1(appSecret, base_string), base64-encoded.
    """
    app_key = creds["CN_EINVOICE_NUONUO_APP_KEY"]
    app_secret = creds["CN_EINVOICE_NUONUO_APP_SECRET"]
    nonce = secrets.token_hex(8)
    timestamp = str(int(time.time()))
    token = creds.get("CN_EINVOICE_NUONUO_TOKEN") or ""

    query: dict[str, str] = {
        "method": method_name,
        "appkey": app_key,
        "nonce": nonce,
        "timestamp": timestamp,
        "token": token,
    }
    sorted_params = "&".join(f"{k}={v}" for k, v in sorted(query.items()))
    base_string = f"{sorted_params}\n{body}"
    digest = hmac.new(
        app_secret.encode("utf-8"),
        base_string.encode("utf-8"),
        hashlib.sha1,
    ).digest()
    signature = digest.hex()
    query["signature"] = signature
    return query, "application/json;charset=utf-8"


def _sign_baiwang(
    method_name: str,
    body: str,
    creds: dict[str, str],
) -> tuple[dict[str, str], str]:
    """Build query params for 百望.

    Reference: https://open.baiwang.com/doc
    Signature = MD5(secret + concat(sorted(k+v for k,v in params)) + body + secret)
    upper-cased hex.
    """
    app_key = creds["CN_EINVOICE_BAIWANG_APP_KEY"]
    app_secret = creds["CN_EINVOICE_BAIWANG_APP_SECRET"]
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    query: dict[str, str] = {
        "method": method_name,
        "app_key": app_key,
        "format": "json",
        "v": "2.0",
        "timestamp": timestamp,
    }
    concat = "".join(f"{k}{v}" for k, v in sorted(query.items()))
    base_string = f"{app_secret}{concat}{body}{app_secret}"
    signature = hashlib.md5(base_string.encode("utf-8")).hexdigest().upper()
    query["sign"] = signature
    return query, "application/json;charset=utf-8"


_SIGNERS = {"nuonuo": _sign_nuonuo, "baiwang": _sign_baiwang}


def call(method_name: str, payload: dict[str, Any]) -> dict:
    """Send a signed request to the active provider; return parsed JSON.

    `method_name` is the provider-specific API name (e.g. 'nuonuo.electronic.invoice').
    """
    creds = assert_ready()
    provider = creds["provider"]
    body = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    query, content_type = _SIGNERS[provider](method_name, body, creds)
    url = _base_url(creds) + "?" + urlparse.urlencode(query)
    headers = {
        "Content-Type": content_type,
        "Accept": "application/json",
        "User-Agent": USER_AGENT,
    }
    req = urlrequest.Request(
        url,
        data=body.encode("utf-8"),
        method="POST",
        headers=headers,
    )
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
