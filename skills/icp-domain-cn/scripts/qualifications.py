#!/usr/bin/env python3
"""icp-domain-cn: 行业前置许可清单.

Input:  "industry=ecommerce,education"
Output: JSON {industries: [{id, requirements: [...]}]}
"""

from __future__ import annotations

from cli_common import load_ref, require, run_kv_cli  # type: ignore[import-not-found]


def build_quals(fields: dict[str, str]) -> dict:
    """Return industry-specific qualification requirements."""
    (raw,) = require(fields, "industry")
    ids = [s.strip() for s in raw.split(",") if s.strip()]
    if not ids:
        raise ValueError("industry must be non-empty, comma-separated")

    rules = load_ref("rules")
    table = rules["industry_extra_qualifications"]
    unknown = [i for i in ids if i not in table]
    if unknown:
        raise ValueError(
            f"unknown industry id(s): {unknown}; valid: {sorted(table)}"
        )

    industries = [
        {"id": i, "requirements": table[i]} for i in ids
    ]

    return {
        "industries": industries,
        "note": "拿到 ICP 备案后才能申办大多数行业许可证；建议同步规划",
    }


def main() -> int:
    """Entry point for qualifications.py."""
    return run_kv_cli(
        'qualifications.py "industry=ecommerce,live_audio_video,news,...'
        '|publication|medical|education|finance|game"',
        build_quals,
    )


if __name__ == "__main__":
    raise SystemExit(main())
