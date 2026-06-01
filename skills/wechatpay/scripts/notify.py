#!/usr/bin/env python3
"""wechatpay: 校验回调通知 + AES-GCM 解密 resource.

Input:  "headers_b64=<base64 of headers JSON>|body=<raw body string>"
        - 也支持从 stdin 读取整个回调 JSON：'stdin=1'
Output: JSON {verified, event_type, decrypted: {...}}

回调验签需要平台证书；本脚本要求 WECHATPAY_PLATFORM_CERT_PATH 指向已下载的 PEM。
首次部署时请用 `python3 scripts/cert.py download` 拉取并保存。
"""

from __future__ import annotations

import base64
import json
import os
import sys

try:
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography import x509
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "missing dependency: cryptography\ninstall via: pip install cryptography"
    ) from exc

from cli_common import run_kv_cli  # type: ignore[import-not-found]


def _verify_signature(timestamp: str, nonce: str, body: str, signature: str) -> bool:
    cert_path = os.environ.get("WECHATPAY_PLATFORM_CERT_PATH")
    if not cert_path or not os.path.exists(cert_path):
        raise RuntimeError(
            "missing WECHATPAY_PLATFORM_CERT_PATH; "
            "first download via `scripts/cert.py download`"
        )
    with open(cert_path, "rb") as fh:
        cert = x509.load_pem_x509_certificate(fh.read())
    pubkey = cert.public_key()
    message = f"{timestamp}\n{nonce}\n{body}\n".encode("utf-8")
    sig = base64.b64decode(signature)
    try:
        pubkey.verify(sig, message, padding.PKCS1v15(), hashes.SHA256())
        return True
    except (ValueError, TypeError):
        return False


def _decrypt_resource(resource: dict) -> dict:
    apiv3_key = os.environ["WECHATPAY_APIV3_KEY"].encode("utf-8")
    nonce = resource["nonce"].encode("utf-8")
    ciphertext = base64.b64decode(resource["ciphertext"])
    aad = resource.get("associated_data", "").encode("utf-8")
    plaintext = AESGCM(apiv3_key).decrypt(nonce, ciphertext, aad)
    return json.loads(plaintext.decode("utf-8"))


def verify_and_decrypt(fields: dict[str, str]) -> dict:
    if fields.get("stdin") == "1":
        raw_input_data = sys.stdin.read()
        envelope = json.loads(raw_input_data)
        headers = envelope.get("headers", {})
        body = envelope.get("body", "")
        if isinstance(body, dict):
            body = json.dumps(body, ensure_ascii=False, separators=(",", ":"))
    else:
        if not fields.get("headers_b64") or "body" not in fields:
            raise ValueError("must provide headers_b64 and body, or stdin=1")
        headers = json.loads(
            base64.b64decode(fields["headers_b64"]).decode("utf-8"),
        )
        body = fields["body"]

    headers_lower = {k.lower(): v for k, v in headers.items()}
    timestamp = headers_lower.get("wechatpay-timestamp", "")
    nonce = headers_lower.get("wechatpay-nonce", "")
    signature = headers_lower.get("wechatpay-signature", "")

    verified = _verify_signature(timestamp, nonce, body, signature)
    parsed = json.loads(body) if body else {}
    decrypted: dict = {}
    if verified and parsed.get("resource"):
        decrypted = _decrypt_resource(parsed["resource"])

    return {
        "verified": verified,
        "event_type": parsed.get("event_type"),
        "summary": parsed.get("summary"),
        "decrypted": decrypted,
    }


def main() -> int:
    return run_kv_cli(
        'notify.py "headers_b64=...|body=..." | "stdin=1" (then pipe JSON to stdin)',
        verify_and_decrypt,
    )


if __name__ == "__main__":
    raise SystemExit(main())
