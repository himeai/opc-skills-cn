#!/usr/bin/env python3
"""cn-einvoice: 开具电子发票（普票 / 专票）.

Input:  "order_no=...|amount=99.00|tax_rate=0.06|buyer_name=...|buyer_tax_num=...|
         buyer_phone=...|buyer_email=...|item_name=技术咨询服务|invoice_type=normal"
        - amount: 含税总额（元），单项目
        - tax_rate: 税率，如 0.06 / 0.03 / 0.13
        - invoice_type: normal(普票) / special(专票)
        - 多商品时改用 items_json='[{...},{...}]'
Output: JSON {invoice_id, status, response}

合规提示：开票方必须为已经实名认证、税控接入完成的真实纳税人；本 skill
不替你校验抬头真伪，请在业务侧做基本一致性核对（名称 / 税号 / 行业代码）。
"""

from __future__ import annotations

import json
import os

from cli_common import require, run_kv_cli  # type: ignore[import-not-found]
from einvoice_http import call  # type: ignore[import-not-found]
from credential import get_provider  # type: ignore[import-not-found]


_INVOICE_TYPE = {
    "normal": {"nuonuo": "1", "baiwang": "1"},   # 普票
    "special": {"nuonuo": "2", "baiwang": "2"},  # 专票
    "etoll": {"nuonuo": "51", "baiwang": "51"},  # 全电普票（不同服务商代码各异，按官方文档微调）
}

_METHOD = {
    "nuonuo": "nuonuo.electronic.invoiceIssue",
    "baiwang": "baiwang.invoice.issue",
}


def _items(fields: dict[str, str]) -> list[dict]:
    if fields.get("items_json"):
        return json.loads(fields["items_json"])
    item_name, amount, tax_rate = require(fields, "item_name", "amount", "tax_rate")
    return [{
        "name": item_name,
        "amount": float(amount),
        "tax_rate": float(tax_rate),
        "spec": fields.get("spec", ""),
        "unit": fields.get("unit", ""),
        "quantity": float(fields.get("quantity", "1")),
    }]


def _payload_nuonuo(fields: dict[str, str], items: list[dict]) -> dict:
    order_no, buyer_name = require(fields, "order_no", "buyer_name")
    invoice_kind = _INVOICE_TYPE[fields.get("invoice_type", "normal")]["nuonuo"]
    return {
        "order": {
            "buyerName": buyer_name,
            "buyerTaxNum": fields.get("buyer_tax_num", ""),
            "buyerTel": fields.get("buyer_phone", ""),
            "buyerEmail": fields.get("buyer_email", ""),
            "salerTaxNum": os.environ["CN_EINVOICE_NUONUO_TAX_NUM"],
            "orderNo": order_no,
            "invoiceLine": invoice_kind,
            "callBackUrl": fields.get("notify_url")
                or os.environ.get("CN_EINVOICE_NOTIFY_URL", ""),
            "clerkId": os.environ.get("CN_EINVOICE_DEFAULT_DRAWER", ""),
            "remark": fields.get("remark", ""),
            "invoiceDetail": [
                {
                    "goodsName": it["name"],
                    "specType": it.get("spec", ""),
                    "unit": it.get("unit", ""),
                    "num": it.get("quantity", 1),
                    "price": it["amount"] / max(it.get("quantity", 1) or 1, 1),
                    "taxRate": it["tax_rate"],
                    "taxIncludedAmount": it["amount"],
                }
                for it in items
            ],
        }
    }


def _payload_baiwang(fields: dict[str, str], items: list[dict]) -> dict:
    order_no, buyer_name = require(fields, "order_no", "buyer_name")
    invoice_kind = _INVOICE_TYPE[fields.get("invoice_type", "normal")]["baiwang"]
    return {
        "request": {
            "orderNo": order_no,
            "invoiceType": invoice_kind,
            "salerTaxNum": os.environ["CN_EINVOICE_BAIWANG_TAX_NUM"],
            "buyerName": buyer_name,
            "buyerTaxNum": fields.get("buyer_tax_num", ""),
            "buyerPhone": fields.get("buyer_phone", ""),
            "buyerEmail": fields.get("buyer_email", ""),
            "callbackUrl": fields.get("notify_url")
                or os.environ.get("CN_EINVOICE_NOTIFY_URL", ""),
            "drawer": os.environ.get("CN_EINVOICE_DEFAULT_DRAWER", ""),
            "remark": fields.get("remark", ""),
            "items": [
                {
                    "name": it["name"],
                    "spec": it.get("spec", ""),
                    "unit": it.get("unit", ""),
                    "num": it.get("quantity", 1),
                    "amount": it["amount"],
                    "taxRate": it["tax_rate"],
                }
                for it in items
            ],
        }
    }


def issue(fields: dict[str, str]) -> dict:
    provider = get_provider()
    items = _items(fields)
    if provider == "nuonuo":
        payload = _payload_nuonuo(fields, items)
    else:
        payload = _payload_baiwang(fields, items)
    resp = call(_METHOD[provider], payload)
    return {
        "provider": provider,
        "order_no": fields["order_no"],
        "items_count": len(items),
        "response": resp,
    }


def main() -> int:
    return run_kv_cli(
        'issue.py "order_no=...|amount=99|tax_rate=0.06|buyer_name=...|item_name=..."',
        issue,
    )


if __name__ == "__main__":
    raise SystemExit(main())
