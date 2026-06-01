#!/usr/bin/env python3
"""wechatpay: 创建支付订单（支持 jsapi / native / h5 / app）.

Input:  "type=jsapi|out_trade_no=...|amount=12.50|description=...|openid=..."
        - type: jsapi / native / h5 / app
        - amount: 元，自动转分；或 amount_fen=1250 直接传分
        - openid: jsapi 必填
        - notify_url: 异步通知地址（默认从 WECHATPAY_NOTIFY_URL 环境变量取）
Output: JSON {prepay_id, qr_code_url(if native), h5_url(if h5)}
"""

from __future__ import annotations

import os

from cli_common import require, run_kv_cli  # type: ignore[import-not-found]
from wxpay_http import get_app_id, request_v3  # type: ignore[import-not-found]


_PATH_BY_TYPE = {
    "jsapi": "/v3/pay/transactions/jsapi",
    "native": "/v3/pay/transactions/native",
    "h5": "/v3/pay/transactions/h5",
    "app": "/v3/pay/transactions/app",
}


def _amount_fen(fields: dict[str, str]) -> int:
    if fields.get("amount_fen"):
        return int(fields["amount_fen"])
    if fields.get("amount"):
        return int(round(float(fields["amount"]) * 100))
    raise ValueError("must provide amount (yuan) or amount_fen")


def create_order(fields: dict[str, str]) -> dict:
    pay_type = fields.get("type", "jsapi").lower()
    if pay_type not in _PATH_BY_TYPE:
        raise ValueError(f"unknown type: {pay_type}")
    out_trade_no, description = require(fields, "out_trade_no", "description")
    notify_url = fields.get("notify_url") or os.environ.get("WECHATPAY_NOTIFY_URL")
    if not notify_url:
        raise ValueError("missing notify_url (or WECHATPAY_NOTIFY_URL env)")

    payload = {
        "appid": get_app_id(fields.get("appid")),
        "mchid": os.environ["WECHATPAY_MCH_ID"],
        "out_trade_no": out_trade_no,
        "description": description,
        "notify_url": notify_url,
        "amount": {"total": _amount_fen(fields), "currency": "CNY"},
    }
    if pay_type == "jsapi":
        openid, = require(fields, "openid")
        payload["payer"] = {"openid": openid}
    if pay_type == "h5":
        payload["scene_info"] = {
            "payer_client_ip": fields.get("client_ip", "0.0.0.0"),
            "h5_info": {"type": fields.get("h5_type", "Wap")},
        }

    resp = request_v3("POST", _PATH_BY_TYPE[pay_type], payload)
    return {
        "type": pay_type,
        "out_trade_no": out_trade_no,
        "amount_fen": _amount_fen(fields),
        "response": resp,
    }


def main() -> int:
    return run_kv_cli(
        'order.py "type=jsapi|out_trade_no=...|amount=12.50|description=...|openid=..."',
        create_order,
    )


if __name__ == "__main__":
    raise SystemExit(main())
