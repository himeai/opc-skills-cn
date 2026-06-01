#!/usr/bin/env python3
"""cn-einvoice: 红冲发票（开具红字发票）.

Input:  "invoice_code=...|invoice_no=...|reason=...|red_apply_no=..."
        - 红冲条件视服务商与税务局规则差异较大；普票全额红冲、专票需要走红字信息表
Output: JSON {provider, response}

合规提示：红冲一旦提交无法撤销，本 skill 不在客户端做二次确认；调用前请
在你的业务系统里加确认弹窗 / 审批环节。
"""

from __future__ import annotations

import os

from cli_common import require, run_kv_cli  # type: ignore[import-not-found]
from einvoice_http import call  # type: ignore[import-not-found]
from credential import get_provider  # type: ignore[import-not-found]


_METHOD = {
    "nuonuo": "nuonuo.electronic.invoiceRed",
    "baiwang": "baiwang.invoice.red",
}


def redflush(fields: dict[str, str]) -> dict:
    provider = get_provider()
    invoice_no, reason = require(fields, "invoice_no", "reason")
    if provider == "nuonuo":
        payload = {
            "salerTaxNum": os.environ["CN_EINVOICE_NUONUO_TAX_NUM"],
            "invoiceCode": fields.get("invoice_code", ""),
            "invoiceNo": invoice_no,
            "reason": reason,
            "redApplyNo": fields.get("red_apply_no", ""),
        }
    else:
        payload = {
            "request": {
                "salerTaxNum": os.environ["CN_EINVOICE_BAIWANG_TAX_NUM"],
                "invoiceCode": fields.get("invoice_code", ""),
                "invoiceNo": invoice_no,
                "reason": reason,
                "redApplyNo": fields.get("red_apply_no", ""),
            }
        }
    return {
        "provider": provider,
        "invoice_no": invoice_no,
        "response": call(_METHOD[provider], payload),
    }


def main() -> int:
    return run_kv_cli(
        'redflush.py "invoice_code=...|invoice_no=...|reason=客户要求重开"',
        redflush,
    )


if __name__ == "__main__":
    raise SystemExit(main())
