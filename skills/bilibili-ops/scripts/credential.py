#!/usr/bin/env python3
"""Credential helpers for bilibili-ops."""

from __future__ import annotations

import os


def get_credentials() -> dict[str, str | None]:
    """Read optional Bilibili Open Platform token from environment variables only."""
    return {
        "open_token": os.environ.get("BILIBILI_OPS_OPEN_TOKEN"),
    }


def has_open_token() -> bool:
    return bool(os.environ.get("BILIBILI_OPS_OPEN_TOKEN"))
