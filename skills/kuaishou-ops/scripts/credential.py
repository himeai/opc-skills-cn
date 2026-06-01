#!/usr/bin/env python3
"""Credential helpers for kuaishou-ops."""

from __future__ import annotations

import os


def get_credentials() -> dict[str, str | None]:
    """Read optional Kuaishou Open Platform token from environment variables only."""
    return {
        "open_token": os.environ.get("KUAISHOU_OPS_OPEN_TOKEN"),
    }


def has_open_token() -> bool:
    return bool(os.environ.get("KUAISHOU_OPS_OPEN_TOKEN"))
