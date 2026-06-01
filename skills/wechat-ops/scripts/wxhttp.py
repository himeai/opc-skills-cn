#!/usr/bin/env python3
"""Tiny HTTP helpers shared by wechat-ops scripts (stdlib only)."""

from __future__ import annotations

import json
import mimetypes
import sys
import urllib.error
import urllib.request
import uuid
from pathlib import Path


def _decode(response_text: str) -> dict:
    data = json.loads(response_text)
    if not isinstance(data, dict):
        raise RuntimeError(f"unexpected response: {response_text}")
    if data.get("errcode") not in (None, 0):
        raise RuntimeError(f"api error: {data}")
    return data


def post_json(url: str, payload: dict, timeout: int = 15) -> dict:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url, data=body, method="POST",
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return _decode(response.read().decode("utf-8"))


def get_json(url: str, timeout: int = 15) -> dict:
    request = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return _decode(response.read().decode("utf-8"))


def post_multipart(url: str, file_path: Path, field: str = "media", timeout: int = 60) -> dict:
    boundary = f"----wechatops{uuid.uuid4().hex}"
    mime, _ = mimetypes.guess_type(file_path.name)
    mime = mime or "application/octet-stream"
    file_bytes = file_path.read_bytes()

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="{field}"; filename="{file_path.name}"\r\n'
        f"Content-Type: {mime}\r\n\r\n"
    ).encode("utf-8") + file_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")

    request = urllib.request.Request(
        url, data=body, method="POST",
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return _decode(response.read().decode("utf-8"))


def cli_error_exit(exc: Exception) -> int:
    """Map an exception to a stderr-printed error and exit code."""
    print(f"error: {exc}", file=sys.stderr)
    if isinstance(exc, RuntimeError) and "missing credential" in str(exc):
        return 2
    if isinstance(exc, (RuntimeError, urllib.error.URLError, OSError, json.JSONDecodeError)):
        return 1
    return 1
