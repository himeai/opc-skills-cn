#!/usr/bin/env python3
"""wecom-crm: 客户联系（外部联系人）.

action=list_followers   列出配置了客户联系的成员 userid 列表
action=list_external    列出某成员的外部客户 external_userid 列表
action=get              获取单个客户详情（external_userid 可来自 list_external）

Inputs:
  action=list_followers
  action=list_external|userid=xxx
  action=get|external_userid=xxx
"""

from __future__ import annotations

import sys

from wecom_http import call, require, run_kv_cli  # type: ignore[import-not-found]


MODULE = "external_contact"


def _list_followers(_: dict[str, str]) -> dict:
    return call(MODULE, "GET", "/externalcontact/get_follow_user_list")


def _list_external(fields: dict[str, str]) -> dict:
    (userid,) = require(fields, "userid")
    return call(MODULE, "GET", "/externalcontact/list", query={"userid": userid})


def _get(fields: dict[str, str]) -> dict:
    (external_userid,) = require(fields, "external_userid")
    return call(
        MODULE, "GET", "/externalcontact/get",
        query={"external_userid": external_userid},
    )


ACTIONS = {
    "list_followers": _list_followers,
    "list_external": _list_external,
    "get": _get,
}


def build(fields: dict[str, str]) -> dict:
    action = fields.get("action") or "list_followers"
    if action not in ACTIONS:
        raise ValueError(
            f"unknown action '{action}', expected one of {list(ACTIONS.keys())}"
        )
    return ACTIONS[action](fields)


if __name__ == "__main__":
    sys.exit(run_kv_cli(
        "scripts/contact.py 'action=list_followers|...'",
        build,
    ))
