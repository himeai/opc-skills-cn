#!/usr/bin/env python3
"""alipay: 创建支付订单（当面付 / PC 网站 / 手机网站 / APP）.

Input:  "type=face_to_face|out_trade_no=...|amount=12.50|subject=咨询服务|auth_code=..."
        type 可选：
          face_to_face   当面付（条码支付，需 auth_code）
          precreate      当面付（扫码支付，返回 qr_code）
          page           PC 网站支付（返回跳转 URL）
          wap            手机网站支付（返回跳转 URL）
          app            APP 支付（返回 orderString）
Output: JSON {type, out_trade_no, amount_yuan, response | redirect_url}
"""

from __future__ import annotations

import os

from cli_common import require, run_kv_cli  # type: ignore[import-not-found]
from alipay_http import build_redirect_url, call  # type: ignore[import-not-found]


_METHOD = {
    "face_to_face": "alipay.trade.pay",
    "precreate": "alipay.trade.precreate",
    "page": "alipay.trade.page.pay",
    "wap": "alipay.trade.wap.pay",
    "app": "alipay.trade.app.pay",
}


def _amount_yuan(fields: dict[str, str]) -> str:
    if fields.get("amount_yuan"):
        return fields["amount_yuan"]
    if fields.get("amount"):
        return f"{float(fields['amount']):.2f}"
    raise ValueError("must provide amount (yuan)")


def _biz_content(pay_type: str, fields: dict[str, str]) -> dict:
    out_trade_no, subject = require(fields, "out_trade_no", "subject")
    biz: dict = {
        "out_trade_no": out_trade_no,
        "subject": subject,
        "total_amount": _amount_yuan(fields),
    }
    if pay_type == "face_to_face":
        auth_code, = require(fields, "auth_code")
        biz["scene"] = fields.get("scene", "bar_code")
        biz["auth_code"] = auth_code
    elif pay_type == "page":
        biz["product_code"] = fields.get("product_code", "FAST_INSTANT_TRADE_PAY")
    elif pay_type == "wap":
        biz["product_code"] = fields.get("product_code", "QUICK_WAP_WAY")
    elif pay_type == "app":
        biz["product_code"] = fields.get("product_code", "QUICK_MSECURITY_PAY")
    if fields.get("body"):
        biz["body"] = fields["body"]
    if fields.get("timeout_express"):
        biz["timeout_express"] = fields["timeout_express"]
    return biz


def create_order(fields: dict[str, str]) -> dict:
    pay_type = fields.get("type", "page").lower()
    if pay_type not in _METHOD:
        raise ValueError(f"unknown type: {pay_type}")
    biz = _biz_content(pay_type, fields)
    notify_url = fields.get("notify_url") or os.environ.get("ALIPAY_NOTIFY_URL")
    return_url = fields.get("return_url") or os.environ.get("ALIPAY_RETURN_URL")

    if pay_type in ("page", "wap"):
        url = build_redirect_url(
            _METHOD[pay_type], biz,
            notify_url=notify_url, return_url=return_url,
        )
        return {
            "type": pay_type,
            "out_trade_no": fields["out_trade_no"],
            "amount_yuan": biz["total_amount"],
            "redirect_url": url,
        }

    resp = call(_METHOD[pay_type], biz, notify_url=notify_url)
    return {
        "type": pay_type,
        "out_trade_no": fields["out_trade_no"],
        "amount_yuan": biz["total_amount"],
        "response": resp,
    }


def main() -> int:
    return run_kv_cli(
        'order.py "type=page|out_trade_no=...|amount=12.50|subject=..." '
        '| "type=face_to_face|out_trade_no=...|amount=12.50|subject=...|auth_code=..."',
        create_order,
    )


if __name__ == "__main__":
    raise SystemExit(main())
