#!/usr/bin/env python3
"""wechatpay: 申请退款.

Input:  "out_trade_no=...|out_refund_no=...|refund=12.50|total=12.50|reason=..."
        - refund: 退款金额（元）；refund_fen=1250 直接传分
        - total: 原订单总额（元）；total_fen=1250 直接传分
        - notify_url: 退款异步通知（默认从 WECHATPAY_REFUND_NOTIFY_URL 取）
Output: JSON {refund_id, status, ...}
"""

from __future__ import annotations

import os

from cli_common import require, run_kv_cli  # type: ignore[import-not-found]
from wxpay_http import request_v3  # type: ignore[import-not-found]


def _fen(fields: dict[str, str], yuan_key: str, fen_key: str) -> int:
    if fields.get(fen_key):
        return int(fields[fen_key])
    if fields.get(yuan_key):
        return int(round(float(fields[yuan_key]) * 100))
    raise ValueError(f"must provide {yuan_key} or {fen_key}")


def refund(fields: dict[str, str]) -> dict:
    out_trade_no, out_refund_no = require(fields, "out_trade_no", "out_refund_no")
    refund_fen = _fen(fields, "refund", "refund_fen")
    total_fen = _fen(fields, "total", "total_fen")
    payload = {
        "out_trade_no": out_trade_no,
        "out_refund_no": out_refund_no,
        "amount": {"refund": refund_fen, "total": total_fen, "currency": "CNY"},
    }
    if fields.get("reason"):
        payload["reason"] = fields["reason"]
    notify_url = fields.get("notify_url") or os.environ.get(
        "WECHATPAY_REFUND_NOTIFY_URL",
    )
    if notify_url:
        payload["notify_url"] = notify_url

    resp = request_v3("POST", "/v3/refund/domestic/refunds", payload)
    return {
        "out_refund_no": out_refund_no,
        "out_trade_no": out_trade_no,
        "refund_fen": refund_fen,
        "response": resp,
    }


def main() -> int:
    return run_kv_cli(
        'refund.py "out_trade_no=...|out_refund_no=...|refund=12.50|total=12.50|reason=..."',
        refund,
    )


if __name__ == "__main__":
    raise SystemExit(main())
