#!/usr/bin/env python3
"""Credential helpers for cn-festival-calendar.

This skill performs purely local rule matching and requires no credentials.
The module exists to keep the per-skill convention consistent.
"""

from __future__ import annotations


def get_credentials() -> dict[str, str | None]:
    """Return an empty credential mapping; this skill needs no secrets."""
    return {}
