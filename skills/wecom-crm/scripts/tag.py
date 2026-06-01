#!/usr/bin/env python3
"""wecom-crm: 客户标签管理.

action=list                  获取企业标签库
action=add_group|name=xxx    新建标签分组（可选 order）
action=add_tag|group_id=xxx|name=yyy  新建标签
action=mark|userid=xxx|external_userid=yyy|add=tagid1,tagid2|remove=tagid3
"""

from __future__ import annotations

import sys

from wecom_http import call, parse_list, require, run_kv_cli  # type: ignore[import-not-found]


MODULE = "external_contact"


def _list(_: dict[str, str]) -> dict:
    return call(MODULE, "POST", "/externalcontact/get_corp_tag_list", payload={})


def _add_group(fields: dict[str, str]) -> dict:
    (name,) = require(fields, "name")
    payload = {"group_name": name}
    if fields.get("order"):
        payload["order"] = int(fields["order"])
    return call(MODULE, "POST", "/externalcontact/add_corp_tag", payload=payload)


def _add_tag(fields: dict[str, str]) -> dict:
    group_id, name = require(fields, "group_id", "name")
    payload = {"group_id": group_id, "tag": [{"name": name}]}
    return call(MODULE, "POST", "/externalcontact/add_corp_tag", payload=payload)


def _mark(fields: dict[str, str]) -> dict:
    userid, external_userid = require(fields, "userid", "external_userid")
    payload = {
        "userid": userid,
        "external_userid": external_userid,
        "add_tag": parse_list(fields.get("add", "")),
        "remove_tag": parse_list(fields.get("remove", "")),
    }
    if not payload["add_tag"] and not payload["remove_tag"]:
        raise ValueError("at least one of add= / remove= must be provided")
    return call(MODULE, "POST", "/externalcontact/mark_tag", payload=payload)


ACTIONS = {
    "list": _list,
    "add_group": _add_group,
    "add_tag": _add_tag,
    "mark": _mark,
}


def build(fields: dict[str, str]) -> dict:
    action = fields.get("action") or "list"
    if action not in ACTIONS:
        raise ValueError(
            f"unknown action '{action}', expected one of {list(ACTIONS.keys())}"
        )
    return ACTIONS[action](fields)


if __name__ == "__main__":
    sys.exit(run_kv_cli(
        "scripts/tag.py 'action=list|...'",
        build,
    ))
