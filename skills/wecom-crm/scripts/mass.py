#!/usr/bin/env python3
"""wecom-crm: 客户群发（add_msg_template / get_groupmsg_*）.

注意：本脚本仅包装企业微信「客户群发」官方 API。群发频率与触达对象遵循
企业微信平台规则（每个客户每自然月最多 1 条），严禁批量骚扰、刷量。

Actions:
  action=create        创建群发任务（externalcontact/add_msg_template）
  action=list          列出群发记录（externalcontact/get_groupmsg_list_v2）
  action=get_result    查询群发结果（externalcontact/get_groupmsg_result）
  action=get_task      获取群发成员发送任务（externalcontact/get_groupmsg_task）

Inputs:
  action=create|sender=userid|text=...|external_userids=ext1,ext2|chat_type=single|allow_select=0
  action=list|chat_type=single|start_time=1717200000|end_time=1719792000|creator=userid
  action=get_result|msgid=msgGCxxxxx|userid=zhangsan
  action=get_task|msgid=msgGCxxxxx
"""

from __future__ import annotations

import sys

from wecom_http import call, parse_list, require, run_kv_cli  # type: ignore[import-not-found]


MODULE = "external_contact"


def _create(fields: dict[str, str]) -> dict:
    """创建客户群发. 至少需要 sender + text；可指定 external_userids 限定客户."""
    (sender,) = require(fields, "sender")
    chat_type = fields.get("chat_type", "single")  # single / group
    payload: dict = {
        "chat_type": chat_type,
        "sender": sender,
        "allow_select": int(fields.get("allow_select", "0") or 0),
    }
    if chat_type == "single":
        ext_ids = parse_list(fields.get("external_userids", ""))
        if ext_ids:
            payload["external_userid"] = ext_ids
    if fields.get("text"):
        payload["text"] = {"content": fields["text"]}

    attachments: list[dict] = []
    if fields.get("image_media_id"):
        attachments.append({
            "msgtype": "image",
            "image": {"media_id": fields["image_media_id"]},
        })
    if fields.get("link_url"):
        link = {
            "title": fields.get("link_title", ""),
            "url": fields["link_url"],
        }
        if fields.get("link_picurl"):
            link["picurl"] = fields["link_picurl"]
        if fields.get("link_desc"):
            link["desc"] = fields["link_desc"]
        attachments.append({"msgtype": "link", "link": link})
    if fields.get("miniprogram_appid"):
        miniprogram = {
            "appid": fields["miniprogram_appid"],
            "title": fields.get("miniprogram_title", ""),
            "page": fields.get("miniprogram_page", ""),
            "pic_media_id": fields.get("miniprogram_pic_media_id", ""),
        }
        attachments.append({"msgtype": "miniprogram", "miniprogram": miniprogram})
    if attachments:
        payload["attachments"] = attachments

    return call(
        MODULE, "POST", "/externalcontact/add_msg_template",
        payload=payload,
    )


def _list(fields: dict[str, str]) -> dict:
    """列出客户群发记录. 时间窗口必填."""
    chat_type = fields.get("chat_type", "single")
    start_time, end_time = require(fields, "start_time", "end_time")
    payload: dict = {
        "chat_type": chat_type,
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
        MODULE, "POST", "/externalcontact/get_groupmsg_list_v2",
        payload=payload,
    )


def _get_result(fields: dict[str, str]) -> dict:
    """查询群发结果（按成员维度，看每个客户的发送状态）."""
    msgid, userid = require(fields, "msgid", "userid")
    payload = {"msgid": msgid, "userid": userid}
    if fields.get("limit"):
        payload["limit"] = int(fields["limit"])
    if fields.get("cursor"):
        payload["cursor"] = fields["cursor"]
    return call(
        MODULE, "POST", "/externalcontact/get_groupmsg_send_result",
        payload=payload,
    )


def _get_task(fields: dict[str, str]) -> dict:
    """获取群发任务（按 msgid 拉所有 sender 的执行情况）."""
    (msgid,) = require(fields, "msgid")
    payload = {"msgid": msgid}
    if fields.get("limit"):
        payload["limit"] = int(fields["limit"])
    if fields.get("cursor"):
        payload["cursor"] = fields["cursor"]
    return call(
        MODULE, "POST", "/externalcontact/get_groupmsg_task",
        payload=payload,
    )


ACTIONS = {
    "create": _create,
    "list": _list,
    "get_result": _get_result,
    "get_task": _get_task,
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
        "scripts/mass.py 'action=create|sender=zhangsan|text=...|external_userids=ext1,ext2'",
        build,
    ))
