#!/usr/bin/env python3
"""wechatpay: 查询订单 / 关闭订单.

Input:  "action=get|out_trade_no=..."        # 按商户订单号查询
        "action=get|transaction_id=..."      # 按微信订单号查询
        "action=close|out_trade_no=..."      # 关闭订单
Output: JSON of WeChat Pay API response
"""

from __future__ import annotations

import os

from cli_common import run_kv_cli  # type: ignore[import-not-found]
from wxpay_http import request_v3  # type: ignore[import-not-found]


def query_or_close(fields: dict[str, str]) -> dict:
    action = fields.get("action", "get").lower()
    mch_id = os.environ["WECHATPAY_MCH_ID"]

    if action == "get":
        if fields.get("transaction_id"):
            txn_id = fields["transaction_id"]
            path = f"/v3/pay/transactions/id/{txn_id}?mchid={mch_id}"
        elif fields.get("out_trade_no"):
            otn = fields["out_trade_no"]
            path = f"/v3/pay/transactions/out-trade-no/{otn}?mchid={mch_id}"
        else:
            raise ValueError("either transaction_id or out_trade_no is required")
        return {"action": "get", "response": request_v3("GET", path)}

    if action == "close":
        if not fields.get("out_trade_no"):
            raise ValueError("out_trade_no is required for close")
        otn = fields["out_trade_no"]
        path = f"/v3/pay/transactions/out-trade-no/{otn}/close"
        request_v3("POST", path, {"mchid": mch_id})
        return {"action": "close", "out_trade_no": otn, "status": "ok"}

    raise ValueError(f"unknown action: {action}")


def main() -> int:
    return run_kv_cli(
        'query.py "action=get|out_trade_no=..." | "action=close|out_trade_no=..."',
        query_or_close,
    )


if __name__ == "__main__":
    raise SystemExit(main())
