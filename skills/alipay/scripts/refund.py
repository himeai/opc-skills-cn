#!/usr/bin/env python3
"""alipay: 退款 / 退款查询.

Input:  "action=refund|out_trade_no=...|out_request_no=...|amount=12.50|reason=..."
        "action=query|out_trade_no=...|out_request_no=..."
Output: JSON of alipay API response
"""

from __future__ import annotations

from cli_common import require, run_kv_cli  # type: ignore[import-not-found]
from alipay_http import call  # type: ignore[import-not-found]


_METHOD = {
    "refund": "alipay.trade.refund",
    "query": "alipay.trade.fastpay.refund.query",
}


def refund(fields: dict[str, str]) -> dict:
    action = fields.get("action", "refund").lower()
    if action not in _METHOD:
        raise ValueError(f"unknown action: {action}")

    if action == "refund":
        out_trade_no, out_request_no, amount = require(
            fields, "out_trade_no", "out_request_no", "amount",
        )
        biz: dict = {
            "out_trade_no": out_trade_no,
            "out_request_no": out_request_no,
            "refund_amount": f"{float(amount):.2f}",
        }
        if fields.get("reason"):
            biz["refund_reason"] = fields["reason"]
        return {"action": "refund", "response": call(_METHOD["refund"], biz)}

    out_trade_no, out_request_no = require(fields, "out_trade_no", "out_request_no")
    biz = {"out_trade_no": out_trade_no, "out_request_no": out_request_no}
    return {"action": "query", "response": call(_METHOD["query"], biz)}


def main() -> int:
    return run_kv_cli(
        'refund.py "action=refund|out_trade_no=...|out_request_no=...|amount=12.50"',
        refund,
    )


if __name__ == "__main__":
    raise SystemExit(main())
