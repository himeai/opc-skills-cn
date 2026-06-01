#!/usr/bin/env python3
"""Credential helpers for wechatpay (WeChat Pay V3)."""

from __future__ import annotations

import os
from pathlib import Path


REQUIRED = ("WECHATPAY_MCH_ID", "WECHATPAY_APIV3_KEY", "WECHATPAY_CERT_SERIAL_NO")
KEY_PATH_ENV = "WECHATPAY_PRIVATE_KEY_PATH"
KEY_INLINE_ENV = "WECHATPAY_PRIVATE_KEY"
APP_ID_ENV = "WECHATPAY_APP_ID"
PLATFORM_CERT_ENV = "WECHATPAY_PLATFORM_CERT_PATH"


def get_credentials() -> dict[str, str | None]:
    """Read credentials from env. The private key may be supplied inline or via path."""
    creds: dict[str, str | None] = {key: os.environ.get(key) for key in REQUIRED}
    creds[APP_ID_ENV] = os.environ.get(APP_ID_ENV)

    inline = os.environ.get(KEY_INLINE_ENV)
    if inline:
        creds["private_key"] = inline
    else:
        path = os.environ.get(KEY_PATH_ENV)
        if path and Path(path).exists():
            creds["private_key"] = Path(path).read_text(encoding="utf-8")
        else:
            creds["private_key"] = None

    creds[PLATFORM_CERT_ENV] = os.environ.get(PLATFORM_CERT_ENV)
    return creds


def assert_ready() -> dict[str, str]:
    """Return creds dict or raise with a friendly message."""
    creds = get_credentials()
    missing = [k for k in REQUIRED if not creds.get(k)]
    if not creds.get("private_key"):
        missing.append(f"{KEY_PATH_ENV} or {KEY_INLINE_ENV}")
    if missing:
        raise RuntimeError(
            "missing credentials: "
            + ", ".join(missing)
            + "\nsee SKILL.md '## Prerequisites' for export commands"
        )
    return {k: v for k, v in creds.items() if v is not None}
