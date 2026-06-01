#!/usr/bin/env python3
"""alipay: 校验异步通知 (notify) 签名.

Input:  "form_b64=<base64 of form-urlencoded body>"
        "stdin=1"  then pipe x-www-form-urlencoded body via stdin
Output: JSON {verified, fields}

支付宝异步通知是 application/x-www-form-urlencoded，包含 sign 与 sign_type；
本脚本用 ALIPAY_PUBLIC_KEY 验签，不解密（支付宝通知不加密）。
"""

from __future__ import annotations

import base64
import sys
from urllib import parse as urlparse

from cli_common import run_kv_cli  # type: ignore[import-not-found]
from alipay_http import verify_callback  # type: ignore[import-not-found]


def _parse_form(text: str) -> dict[str, str]:
    return {k: v[0] for k, v in urlparse.parse_qs(text, keep_blank_values=True).items()}


def verify(fields: dict[str, str]) -> dict:
    if fields.get("stdin") == "1":
        body = sys.stdin.read()
    elif fields.get("form_b64"):
        body = base64.b64decode(fields["form_b64"]).decode("utf-8")
    else:
        raise ValueError("must provide form_b64=... or stdin=1")
    form = _parse_form(body)
    ok = verify_callback(form)
    return {
        "verified": ok,
        "trade_status": form.get("trade_status"),
        "out_trade_no": form.get("out_trade_no"),
        "trade_no": form.get("trade_no"),
        "total_amount": form.get("total_amount"),
        "fields": form,
    }


def main() -> int:
    return run_kv_cli(
        'notify.py "form_b64=..." | "stdin=1" (then pipe form body)',
        verify,
    )


if __name__ == "__main__":
    raise SystemExit(main())
