#!/usr/bin/env python3
"""alipay: 查询订单 / 关闭订单 / 撤销订单.

Input:  "action=query|out_trade_no=..."
        "action=query|trade_no=..."
        "action=close|out_trade_no=..."
        "action=cancel|out_trade_no=..."   # 仅当面付场景
Output: JSON of alipay API response
"""

from __future__ import annotations

from cli_common import run_kv_cli  # type: ignore[import-not-found]
from alipay_http import call  # type: ignore[import-not-found]


_METHOD = {
    "query": "alipay.trade.query",
    "close": "alipay.trade.close",
    "cancel": "alipay.trade.cancel",
}


def query_or_close(fields: dict[str, str]) -> dict:
    action = fields.get("action", "query").lower()
    if action not in _METHOD:
        raise ValueError(f"unknown action: {action}")
    if not fields.get("out_trade_no") and not fields.get("trade_no"):
        raise ValueError("either out_trade_no or trade_no is required")
    biz: dict = {}
    if fields.get("out_trade_no"):
        biz["out_trade_no"] = fields["out_trade_no"]
    if fields.get("trade_no"):
        biz["trade_no"] = fields["trade_no"]
    return {"action": action, "response": call(_METHOD[action], biz)}


def main() -> int:
    return run_kv_cli(
        'query.py "action=query|out_trade_no=..." | "action=close|out_trade_no=..."',
        query_or_close,
    )


if __name__ == "__main__":
    raise SystemExit(main())
