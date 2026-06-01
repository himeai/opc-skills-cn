#!/usr/bin/env python3
"""cn-einvoice: 查询发票状态.

Input:  "order_no=..."           # 按订单号查
        "invoice_no=..."         # 按发票号查
Output: JSON {provider, response}
"""

from __future__ import annotations

import os

from cli_common import run_kv_cli  # type: ignore[import-not-found]
from einvoice_http import call  # type: ignore[import-not-found]
from credential import get_provider  # type: ignore[import-not-found]


_METHOD = {
    "nuonuo": "nuonuo.electronic.invoiceResult",
    "baiwang": "baiwang.invoice.query",
}


def query(fields: dict[str, str]) -> dict:
    provider = get_provider()
    if not fields.get("order_no") and not fields.get("invoice_no"):
        raise ValueError("either order_no or invoice_no is required")
    if provider == "nuonuo":
        payload = {
            "serialNos": [fields.get("order_no") or fields.get("invoice_no")],
            "salerTaxNum": os.environ["CN_EINVOICE_NUONUO_TAX_NUM"],
        }
    else:
        payload = {
            "request": {
                "orderNo": fields.get("order_no", ""),
                "invoiceNo": fields.get("invoice_no", ""),
                "salerTaxNum": os.environ["CN_EINVOICE_BAIWANG_TAX_NUM"],
            }
        }
    return {"provider": provider, "response": call(_METHOD[provider], payload)}


def main() -> int:
    return run_kv_cli(
        'query.py "order_no=..." | "invoice_no=..."',
        query,
    )


if __name__ == "__main__":
    raise SystemExit(main())
