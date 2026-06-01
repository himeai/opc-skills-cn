#!/usr/bin/env python3
"""wecom-crm: 客户群（外部群）.

action=list                                列出客户群
action=get|chat_id=xxx                     查群详情
action=stats|day_begin=YYYY-MM-DD|day_end=YYYY-MM-DD  统计
"""

from __future__ import annotations

import sys
from datetime import datetime

from wecom_http import call, require, run_kv_cli  # type: ignore[import-not-found]


MODULE = "customer_group"


def _list(fields: dict[str, str]) -> dict:
    payload: dict = {"limit": int(fields.get("limit", 100))}
    if fields.get("cursor"):
        payload["cursor"] = fields["cursor"]
    return call(MODULE, "POST", "/externalcontact/groupchat/list", payload=payload)


def _get(fields: dict[str, str]) -> dict:
    (chat_id,) = require(fields, "chat_id")
    return call(
        MODULE, "POST", "/externalcontact/groupchat/get",
        payload={"chat_id": chat_id, "need_name": 1},
    )


def _to_ts(d: str) -> int:
    return int(datetime.strptime(d, "%Y-%m-%d").timestamp())


def _stats(fields: dict[str, str]) -> dict:
    day_begin, day_end = require(fields, "day_begin", "day_end")
    payload = {
        "day_begin_time": _to_ts(day_begin),
        "day_end_time":   _to_ts(day_end),
        "owner_filter": {"userid_list": []},  # 全部群主
    }
    return call(
        MODULE, "POST", "/externalcontact/groupchat/statistic",
        payload=payload,
    )


ACTIONS = {
    "list": _list,
    "get": _get,
    "stats": _stats,
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
        "scripts/group.py 'action=list|...'",
        build,
    ))
