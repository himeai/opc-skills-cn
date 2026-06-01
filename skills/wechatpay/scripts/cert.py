#!/usr/bin/env python3
"""wechatpay: 下载 / 列出微信支付平台证书.

Input:  "action=download|out_dir=./platform_certs"   # 拉取并保存最新证书
        "action=list"                                # 仅打印不保存
Output: JSON {certs: [{serial_no, effective_time, expire_time, path?}, ...]}

平台证书用于 notify.py 的回调验签。建议每月跑一次 download，避免到期。
"""

from __future__ import annotations

import base64
import os
from pathlib import Path

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "missing dependency: cryptography\ninstall via: pip install cryptography"
    ) from exc

from cli_common import run_kv_cli  # type: ignore[import-not-found]
from wxpay_http import request_v3  # type: ignore[import-not-found]


def _decrypt(resource: dict, apiv3_key: bytes) -> str:
    nonce = resource["nonce"].encode("utf-8")
    ciphertext = base64.b64decode(resource["ciphertext"])
    aad = resource.get("associated_data", "").encode("utf-8")
    return AESGCM(apiv3_key).decrypt(nonce, ciphertext, aad).decode("utf-8")


def manage_certs(fields: dict[str, str]) -> dict:
    action = fields.get("action", "list").lower()
    apiv3_key = os.environ["WECHATPAY_APIV3_KEY"].encode("utf-8")
    resp = request_v3("GET", "/v3/certificates")
    certs_raw = resp.get("data", [])

    out_dir: Path | None = None
    if action == "download":
        out_dir = Path(fields.get("out_dir", "./platform_certs"))
        out_dir.mkdir(parents=True, exist_ok=True)

    certs: list[dict] = []
    for item in certs_raw:
        pem = _decrypt(item["encrypt_certificate"], apiv3_key)
        entry = {
            "serial_no": item.get("serial_no"),
            "effective_time": item.get("effective_time"),
            "expire_time": item.get("expire_time"),
        }
        if out_dir is not None:
            file_path = out_dir / f"{item['serial_no']}.pem"
            file_path.write_text(pem, encoding="utf-8")
            entry["path"] = str(file_path)
        certs.append(entry)
    return {"action": action, "certs": certs}


def main() -> int:
    return run_kv_cli(
        'cert.py "action=download|out_dir=./platform_certs" | "action=list"',
        manage_certs,
    )


if __name__ == "__main__":
    raise SystemExit(main())
