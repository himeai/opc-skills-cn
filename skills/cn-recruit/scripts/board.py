#!/usr/bin/env python3
"""cn-recruit: 招聘看板汇总与告警.

Input: JSON 字符串描述当前的岗位 + 候选人 pipeline。

例：
  python3 scripts/board.py '{
    "positions": [
      {
        "id": "P-001", "title": "后端工程师", "open_days": 18,
        "candidates": [
          {"name": "A", "stage": "screening", "days_in_stage": 4},
          {"name": "B", "stage": "tech1", "days_in_stage": 7},
          {"name": "C", "stage": "offer", "days_in_stage": 9}
        ]
      }
    ]
  }'

Output: JSON {board:[{position, by_stage:{...}, warnings:[...]}], kpis:[...]}
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "references" / "board_config.json"


def _load() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def _eval_rule(expr: str, ctx: dict) -> bool:
    allowed = {k: v for k, v in ctx.items() if isinstance(v, (int, float, bool, str))}
    try:
        return bool(eval(expr, {"__builtins__": {}}, allowed))  # nosec B307
    except (NameError, SyntaxError, TypeError):
        return False


def _stage_meta(stages: list[dict], key: str) -> dict | None:
    for stage in stages:
        if stage["key"] == key:
            return stage
    return None


def build_board(positions: list[dict]) -> dict:
    cfg = _load()
    stages = cfg["stages"]

    board = []
    for pos in positions:
        by_stage: dict[str, list[dict]] = {s["key"]: [] for s in stages}
        warnings: list[dict] = []
        active_count = 0

        for cand in pos.get("candidates", []):
            stage_key = cand.get("stage", "screening")
            stage_meta = _stage_meta(stages, stage_key)
            if not stage_meta:
                continue
            days_in_stage = int(cand.get("days_in_stage", 0))
            sla_days = int(stage_meta["sla_days"])

            entry = {
                "name": cand.get("name", ""),
                "stage": stage_key,
                "days_in_stage": days_in_stage,
                "overdue": days_in_stage > sla_days,
            }
            by_stage[stage_key].append(entry)
            if stage_key not in ("offer", "onboard"):
                active_count += 1

            ctx = {
                "stage": stage_key,
                "days_in_stage": days_in_stage,
                "sla_days": sla_days,
                "open_days": int(pos.get("open_days", 0)),
                "active_candidates": 0,
            }
            for rule in cfg["warning_rules"]:
                if rule["key"] == "stage_overdue" and _eval_rule(rule["rule"], ctx):
                    warnings.append({
                        "level": rule["level"],
                        "key": rule["key"],
                        "candidate": entry["name"],
                        "stage": stage_key,
                        "days_in_stage": days_in_stage,
                        "advice": rule["advice"],
                    })
                if rule["key"] == "offer_long_silence" and _eval_rule(rule["rule"], ctx):
                    warnings.append({
                        "level": rule["level"],
                        "key": rule["key"],
                        "candidate": entry["name"],
                        "advice": rule["advice"],
                    })

        # pipeline_too_thin: 看一次就够
        thin_ctx = {"active_candidates": active_count, "open_days": int(pos.get("open_days", 0))}
        for rule in cfg["warning_rules"]:
            if rule["key"] == "pipeline_too_thin" and _eval_rule(rule["rule"], thin_ctx):
                warnings.append({
                    "level": rule["level"],
                    "key": rule["key"],
                    "active_candidates": active_count,
                    "advice": rule["advice"],
                })

        board.append({
            "id": pos.get("id", ""),
            "title": pos.get("title", ""),
            "open_days": int(pos.get("open_days", 0)),
            "active_candidates": active_count,
            "by_stage": by_stage,
            "warnings": warnings,
        })

    return {
        "stages": stages,
        "kpis": cfg["default_kpis"],
        "board": board,
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: board.py '<json payload>'", file=sys.stderr)
        return 1
    try:
        payload = json.loads(sys.argv[1])
        result = build_board(payload.get("positions", []))
    except (json.JSONDecodeError, OSError, KeyError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
