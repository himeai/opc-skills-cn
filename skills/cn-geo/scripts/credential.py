#!/usr/bin/env python3
"""cn-geo: 占位凭证模块（本 skill 无需凭证）."""

from __future__ import annotations


def assert_ready() -> dict[str, str]:
    """Return empty credentials; cn-geo runs fully offline."""
    return {}
