#!/usr/bin/env python3
"""icp-domain-cn: 占位凭证模块（本 skill 无需凭证）."""

from __future__ import annotations


def assert_ready() -> dict[str, str]:
    """Return empty credentials; icp-domain-cn runs fully offline."""
    return {}
