#!/usr/bin/env python3
"""Credential helpers for cn-einvoice.

Supports two providers: nuonuo (诺诺发票) and baiwang (百望发票). The active
provider is selected via CN_EINVOICE_PROVIDER (default: nuonuo).
"""

from __future__ import annotations

import os


PROVIDER_ENV = "CN_EINVOICE_PROVIDER"
SUPPORTED = ("nuonuo", "baiwang")

_REQUIRED_BY_PROVIDER = {
    "nuonuo": (
        "CN_EINVOICE_NUONUO_APP_KEY",
        "CN_EINVOICE_NUONUO_APP_SECRET",
        "CN_EINVOICE_NUONUO_TAX_NUM",
    ),
    "baiwang": (
        "CN_EINVOICE_BAIWANG_APP_KEY",
        "CN_EINVOICE_BAIWANG_APP_SECRET",
        "CN_EINVOICE_BAIWANG_TAX_NUM",
    ),
}

_OPTIONAL = (
    "CN_EINVOICE_NUONUO_TOKEN",
    "CN_EINVOICE_BAIWANG_TOKEN",
    "CN_EINVOICE_DEFAULT_PAYEE",
    "CN_EINVOICE_DEFAULT_REVIEWER",
    "CN_EINVOICE_DEFAULT_DRAWER",
    "CN_EINVOICE_NOTIFY_URL",
    "CN_EINVOICE_SANDBOX",
)


def get_provider() -> str:
    """Return the configured provider name; default 'nuonuo'."""
    value = (os.environ.get(PROVIDER_ENV) or "nuonuo").strip().lower()
    if value not in SUPPORTED:
        raise RuntimeError(
            f"unsupported provider '{value}'; choose one of {SUPPORTED}"
        )
    return value


def get_credentials() -> dict[str, str | None]:
    """Read credentials of the active provider plus optional fields."""
    provider = get_provider()
    creds: dict[str, str | None] = {"provider": provider}
    for key in _REQUIRED_BY_PROVIDER[provider]:
        creds[key] = os.environ.get(key)
    for key in _OPTIONAL:
        creds[key] = os.environ.get(key)
    return creds


def assert_ready() -> dict[str, str]:
    """Raise if any required field is missing for the active provider."""
    creds = get_credentials()
    provider = creds["provider"]
    missing = [k for k in _REQUIRED_BY_PROVIDER[provider] if not creds.get(k)]
    if missing:
        raise RuntimeError(
            "missing credentials: "
            + ", ".join(missing)
            + "\nsee SKILL.md '## Prerequisites' for export commands"
        )
    return {k: v for k, v in creds.items() if v is not None}
