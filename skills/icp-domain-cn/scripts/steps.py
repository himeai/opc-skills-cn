#!/usr/bin/env python3
"""icp-domain-cn: 备案分步指引.

Input:  "filing=icp|psb"
Output: JSON {filing, steps: [...]}
"""

from __future__ import annotations

from cli_common import load_ref, require, run_kv_cli  # type: ignore[import-not-found]


STEP_KEY = {"icp": "icp_filing_steps", "psb": "psb_filing_steps"}


def build_steps(fields: dict[str, str]) -> dict:
    """Return step-by-step filing instructions."""
    (filing,) = require(fields, "filing")
    if filing not in STEP_KEY:
        raise ValueError("filing must be 'icp' or 'psb'")

    rules = load_ref("rules")
    steps = rules[STEP_KEY[filing]]
    return {
        "filing": filing,
        "steps": steps,
        "note": "本流程为通用口径；各省 / 各云厂商系统略有差异，以系统提示为准",
    }


def main() -> int:
    """Entry point for steps.py."""
    return run_kv_cli(
        'steps.py "filing=icp|psb"',
        build_steps,
    )


if __name__ == "__main__":
    raise SystemExit(main())
