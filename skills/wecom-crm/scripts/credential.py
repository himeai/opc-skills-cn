#!/usr/bin/env python3
"""Credential helpers for wecom-crm (WeCom / 企业微信)."""

from __future__ import annotations

import os


CORP_ID_ENV = "WECOM_CORP_ID"
DEFAULT_TOKEN_DIR = "./.wecom_tokens"

# 企业微信不同模块的 secret 不同：
#   - external_contact: 外部联系人（客户联系）API：客户列表 / 标签 / 群发
#   - customer_group:    客户群（群聊）相关接口（多数与 external_contact 共用 secret）
#   - moments:           企业朋友圈相关接口
#   - app:               自建应用（菜单、消息推送、模板）
SECRET_ENVS = {
    "external_contact": "WECOM_SECRET_EXTERNAL_CONTACT",
    "customer_group":   "WECOM_SECRET_CUSTOMER_GROUP",
    "moments":          "WECOM_SECRET_MOMENTS",
    "app":              "WECOM_SECRET_APP",
}


def get_corp_id() -> str:
    """Return WECOM_CORP_ID or raise."""
    corp_id = os.environ.get(CORP_ID_ENV)
    if not corp_id:
        raise RuntimeError(
            f"missing credential env: {CORP_ID_ENV}; "
            "see SKILL.md '## Prerequisites' for export commands"
        )
    return corp_id


def get_secret(module: str) -> str:
    """Return secret for a module (external_contact / customer_group / moments / app)."""
    if module not in SECRET_ENVS:
        raise ValueError(
            f"unknown module '{module}', expected one of {list(SECRET_ENVS.keys())}"
        )
    env_name = SECRET_ENVS[module]
    secret = os.environ.get(env_name)
    if not secret:
        raise RuntimeError(
            f"missing credential env: {env_name}; "
            "see SKILL.md '## Prerequisites' for export commands"
        )
    return secret


def get_token_cache_dir() -> str:
    """Return token cache directory (overridable via WECOM_TOKEN_CACHE_DIR)."""
    return os.environ.get("WECOM_TOKEN_CACHE_DIR", DEFAULT_TOKEN_DIR)


def get_agent_id() -> str | None:
    """Return WECOM_AGENT_ID (only required for self-built app pushes)."""
    return os.environ.get("WECOM_AGENT_ID")
