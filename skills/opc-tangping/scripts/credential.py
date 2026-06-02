#!/usr/bin/env python3
"""Credential helpers for opc-tangping (local-rules skill, no external API)."""

from __future__ import annotations


def get_credentials() -> dict:
    """No credentials required for opc-tangping."""
    return {}


def has_credentials() -> bool:
    return True
