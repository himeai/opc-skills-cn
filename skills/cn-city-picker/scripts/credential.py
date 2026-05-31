#!/usr/bin/env python3
"""Credential helpers for cn-city-picker."""

from __future__ import annotations

import os


def get_credentials() -> dict[str, str | None]:
    """Read optional API keys from environment variables only."""
    return {
        "tianyancha_api_key": os.environ.get("TIANYANCHA_API_KEY"),
        "amap_api_key": os.environ.get("AMAP_API_KEY"),
    }


def has_realtime_credentials() -> bool:
    """Return whether any optional realtime data credential is configured."""
    credentials = get_credentials()
    return any(credentials.values())
