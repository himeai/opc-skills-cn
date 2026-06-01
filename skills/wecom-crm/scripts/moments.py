#!/usr/bin/env python3
"""wecom-crm: 企业朋友圈（externalcontact/add_moment_task / get_*）.

仅包装企业微信「朋友圈」官方 API。投放频率与可见范围由企业微信平台管控；
本 skill 不做绕过、不做规模化轰炸。

Actions:
  action=create        创建朋友圈任务（add_moment_task）
  action=get_task      查询任务状态（get_moment_task_result）
  action=list          列出朋友圈记录（get_moment_list）
  action=customers     列出朋友圈可见客户（get_moment_customer_list）
  action=send_result   查询朋友圈成员执行情况（get_moment_send_result）
  action=comments      查询朋友圈评论与点赞（get_moment_comments）

Inputs:
  action=create|text=...|image_media_ids=mid1,mid2|sender_userids=u1,u2|visible_range=ALL
  action=get_task|jobid=jobxxx
  action=list|start_time=1717200000|end_time=1719792000|creator=userid|filter_type=0
  action=customers|moment_id=mom_xxx|userid=zhangsan
  action=send_result|moment_id=mom_xxx|userid=zhangsan
  action=comments|moment_id=mom_xxx|userid=zhangsan
"""

from __future__ import annotations

import sys

from wecom_http import call, parse_list, require, run_kv_cli  # type: ignore[import-not-found]


MODULE = "moments"


def _build_attachments(fields: dict[str, str]) -> list[dict]:
    attachments: list[dict] = []
    image_ids = parse_list(fields.get("image_media_ids", ""))
    for mid in image_ids:
        attachments.append({"msgtype": "image", "image": {"media_id": mid}})
    if fields.get("video_media_id"):
        attachments.append({
            "msgtype": "video",
            "video": {"media_id": fields["video_media_id"]},
        })
    if fields.get("link_url"):
        attachments.append({
            "msgtype": "link",
            "link": {
                "title": fields.get("link_title", ""),
                "url": fields["link_url"],
            },
        })
    return attachments


def _build_visible_range(fields: dict[str, str]) -> dict | None:
    """visible_range=ALL / PART_VISIBLE。PART_VISIBLE 时需要 visible_user/tag 列表."""
    visible_range = fields.get("visible_range", "ALL").upper()
    if visible_range == "ALL":
        return None
    visible_user = parse_list(fields.get("visible_user", ""))
    visible_tag = parse_list(fields.get("visible_tag", ""))
    return {
        "visible_to_user": {"user_list": visible_user, "tag_list": visible_tag},
    }


def _create(fields: dict[str, str]) -> dict:
    """创建朋友圈任务. 文本与附件至少给一种."""
    text_content = fields.get("text", "")
    sender_userids = parse_list(fields.get("sender_userids", ""))
    sender_dept_ids = parse_list(fields.get("sender_dept_ids", ""))
    if not sender_userids and not sender_dept_ids:
        raise ValueError("missing fields: sender_userids or sender_dept_ids")

    payload: dict = {
        "text": {"content": text_content},
        "attachments": _build_attachments(fields),
        "visible_range": {
            "sender_list": {
                "user_list": sender_userids,
                "department_list": [int(x) for x in sender_dept_ids if x.isdigit()],
            },
        },
    }
    extra_visible = _build_visible_range(fields)
    if extra_visible:
        payload["visible_range"].update(extra_visible)

    return call(
        MODULE, "POST", "/externalcontact/add_moment_task",
        payload=payload,
    )


def _get_task(fields: dict[str, str]) -> dict:
    (jobid,) = require(fields, "jobid")
    return call(
        MODULE, "GET", "/externalcontact/get_moment_task_result",
        query={"jobid": jobid},
    )


def _list(fields: dict[str, str]) -> dict:
    start_time, end_time = require(fields, "start_time", "end_time")
    payload: dict = {
        "start_time": int(start_time),
        "end_time": int(end_time),
    }
    if fields.get("creator"):
        payload["creator"] = fields["creator"]
    if fields.get("filter_type"):
        payload["filter_type"] = int(fields["filter_type"])
    if fields.get("limit"):
        payload["limit"] = int(fields["limit"])
    if fields.get("cursor"):
        payload["cursor"] = fields["cursor"]
    return call(
        MODULE, "POST", "/externalcontact/get_moment_list",
        payload=payload,
    )


def _customers(fields: dict[str, str]) -> dict:
    moment_id, userid = require(fields, "moment_id", "userid")
    payload = {"moment_id": moment_id, "userid": userid}
    if fields.get("limit"):
        payload["limit"] = int(fields["limit"])
    if fields.get("cursor"):
        payload["cursor"] = fields["cursor"]
    return call(
        MODULE, "POST", "/externalcontact/get_moment_customer_list",
        payload=payload,
    )


def _send_result(fields: dict[str, str]) -> dict:
    moment_id, userid = require(fields, "moment_id", "userid")
    payload = {"moment_id": moment_id, "userid": userid}
    if fields.get("limit"):
        payload["limit"] = int(fields["limit"])
    if fields.get("cursor"):
        payload["cursor"] = fields["cursor"]
    return call(
        MODULE, "POST", "/externalcontact/get_moment_send_result",
        payload=payload,
    )


def _comments(fields: dict[str, str]) -> dict:
    moment_id, userid = require(fields, "moment_id", "userid")
    return call(
        MODULE, "POST", "/externalcontact/get_moment_comments",
        payload={"moment_id": moment_id, "userid": userid},
    )


ACTIONS = {
    "create": _create,
    "get_task": _get_task,
    "list": _list,
    "customers": _customers,
    "send_result": _send_result,
    "comments": _comments,
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
        "scripts/moments.py 'action=create|text=...|sender_userids=u1,u2|image_media_ids=mid1'",
        build,
    ))
