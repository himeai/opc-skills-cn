#!/usr/bin/env python3
"""Credential helpers for wechat-ops."""

from __future__ import annotations

import os


DEFAULT_TOKEN_CACHE = "./.wechat_mp_token.json"


def get_credentials() -> dict[str, str | None]:
    """Read WeChat MP credentials from environment variables only."""
    return {
        "app_id": os.environ.get("WECHAT_MP_APP_ID"),
        "app_secret": os.environ.get("WECHAT_MP_APP_SECRET"),
        "token_cache": os.environ.get("WECHAT_MP_TOKEN_CACHE", DEFAULT_TOKEN_CACHE),
    }


def require_credentials() -> dict[str, str]:
    """Return credentials with app_id/app_secret guaranteed non-empty.

    Raises RuntimeError when required env vars are missing so callers can
    surface a friendly error and exit with code 2.
    """
    creds = get_credentials()
    missing = [
        env for env, key in (
            ("WECHAT_MP_APP_ID", "app_id"),
            ("WECHAT_MP_APP_SECRET", "app_secret"),
        )
        if not creds.get(key)
    ]
    if missing:
        raise RuntimeError(
            "missing credential env: " + ", ".join(missing)
            + "; please export them before running wechat-ops scripts"
        )
    return {
        "app_id": creds["app_id"] or "",
        "app_secret": creds["app_secret"] or "",
        "token_cache": creds["token_cache"] or DEFAULT_TOKEN_CACHE,
    }
