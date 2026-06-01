#!/usr/bin/env python3
"""Credential helpers for alipay (支付宝 OpenAPI)."""

from __future__ import annotations

import os
from pathlib import Path


REQUIRED = ("ALIPAY_APP_ID",)
APP_PRIVATE_KEY_PATH_ENV = "ALIPAY_APP_PRIVATE_KEY_PATH"
APP_PRIVATE_KEY_INLINE_ENV = "ALIPAY_APP_PRIVATE_KEY"
ALIPAY_PUBLIC_KEY_PATH_ENV = "ALIPAY_PUBLIC_KEY_PATH"
ALIPAY_PUBLIC_KEY_INLINE_ENV = "ALIPAY_PUBLIC_KEY"
SANDBOX_ENV = "ALIPAY_SANDBOX"
NOTIFY_URL_ENV = "ALIPAY_NOTIFY_URL"
RETURN_URL_ENV = "ALIPAY_RETURN_URL"
SIGN_TYPE_ENV = "ALIPAY_SIGN_TYPE"  # RSA2 (default) / RSA


def _read_key(inline_env: str, path_env: str) -> str | None:
    inline = os.environ.get(inline_env)
    if inline:
        return inline
    path = os.environ.get(path_env)
    if path and Path(path).exists():
        return Path(path).read_text(encoding="utf-8")
    return None


def get_credentials() -> dict[str, str | None]:
    """Read credentials from env."""
    creds: dict[str, str | None] = {key: os.environ.get(key) for key in REQUIRED}
    creds["app_private_key"] = _read_key(
        APP_PRIVATE_KEY_INLINE_ENV, APP_PRIVATE_KEY_PATH_ENV,
    )
    creds["alipay_public_key"] = _read_key(
        ALIPAY_PUBLIC_KEY_INLINE_ENV, ALIPAY_PUBLIC_KEY_PATH_ENV,
    )
    creds[SANDBOX_ENV] = os.environ.get(SANDBOX_ENV)
    creds[NOTIFY_URL_ENV] = os.environ.get(NOTIFY_URL_ENV)
    creds[RETURN_URL_ENV] = os.environ.get(RETURN_URL_ENV)
    creds[SIGN_TYPE_ENV] = os.environ.get(SIGN_TYPE_ENV) or "RSA2"
    return creds


def is_sandbox() -> bool:
    return (os.environ.get(SANDBOX_ENV) or "").lower() in ("1", "true", "yes")


def assert_ready(require_alipay_pubkey: bool = False) -> dict[str, str]:
    """Return creds dict or raise; pubkey only required for verifying responses."""
    creds = get_credentials()
    missing = [k for k in REQUIRED if not creds.get(k)]
    if not creds.get("app_private_key"):
        missing.append(
            f"{APP_PRIVATE_KEY_PATH_ENV} or {APP_PRIVATE_KEY_INLINE_ENV}",
        )
    if require_alipay_pubkey and not creds.get("alipay_public_key"):
        missing.append(
            f"{ALIPAY_PUBLIC_KEY_PATH_ENV} or {ALIPAY_PUBLIC_KEY_INLINE_ENV}",
        )
    if missing:
        raise RuntimeError(
            "missing credentials: "
            + ", ".join(missing)
            + "\nsee SKILL.md '## Prerequisites' for export commands"
        )
    return {k: v for k, v in creds.items() if v is not None}
