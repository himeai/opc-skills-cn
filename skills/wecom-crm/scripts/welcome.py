#!/usr/bin/env python3
"""wecom-crm: 配置 / 查看「客户欢迎语」.

action=set|userid=xxx|text=hello
   注意：企业微信欢迎语只能在「客户添加事件」回调里调用 send_welcome_msg；
   本脚本提供的是「入群欢迎语模板」（add_join_way 之外的另一条路径）。

action=add_template|text=xxx|agentid=...
action=del_template|template_id=xxx
action=get_template|template_id=xxx
action=list_templates
"""

from __future__ import annotations

import sys

from wecom_http import call, require, run_kv_cli  # type: ignore[import-not-found]


MODULE = "external_contact"


def _add_template(fields: dict[str, str]) -> dict:
    (text,) = require(fields, "text")
    payload: dict = {"text": {"content": text}}
    if fields.get("agentid"):
        payload["agentid"] = int(fields["agentid"])
    return call(
        MODULE, "POST", "/externalcontact/group_welcome_template/add",
        payload=payload,
    )


def _del_template(fields: dict[str, str]) -> dict:
    (template_id,) = require(fields, "template_id")
    return call(
        MODULE, "POST", "/externalcontact/group_welcome_template/del",
        payload={"template_id": template_id},
    )


def _get_template(fields: dict[str, str]) -> dict:
    (template_id,) = require(fields, "template_id")
    return call(
        MODULE, "POST", "/externalcontact/group_welcome_template/get",
        payload={"template_id": template_id},
    )


def _send_welcome(fields: dict[str, str]) -> dict:
    """直接调用 send_welcome_msg；welcome_code 来自客户添加事件回调."""
    welcome_code, text = require(fields, "welcome_code", "text")
    return call(
        MODULE, "POST", "/externalcontact/send_welcome_msg",
        payload={"welcome_code": welcome_code, "text": {"content": text}},
    )


ACTIONS = {
    "add_template": _add_template,
    "del_template": _del_template,
    "get_template": _get_template,
    "send": _send_welcome,
}


def build(fields: dict[str, str]) -> dict:
    action = fields.get("action") or "add_template"
    if action not in ACTIONS:
        raise ValueError(
            f"unknown action '{action}', expected one of {list(ACTIONS.keys())}"
        )
    return ACTIONS[action](fields)


if __name__ == "__main__":
    sys.exit(run_kv_cli(
        "scripts/welcome.py 'action=add_template|text=...'",
        build,
    ))
