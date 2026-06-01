#!/usr/bin/env python3
"""Credential helpers for xiaohongshu-ops."""

from __future__ import annotations

import os


def get_credentials() -> dict[str, str | None]:
    """Read optional Dandelion API token from environment variables only."""
    return {
        "dandelion_token": os.environ.get("XIAOHONGSHU_OPS_DANDELION_TOKEN"),
    }


def has_dandelion_token() -> bool:
    return bool(os.environ.get("XIAOHONGSHU_OPS_DANDELION_TOKEN"))
