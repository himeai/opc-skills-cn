#!/usr/bin/env python3
"""train.py — 体能 / 资格证训练路径规划。

input format:
  goal=everest|current_fitness=3
  goal=ppl_us_faa|current_fitness=2
  goal=marathon_bmw6|current_fitness=4
"""

from __future__ import annotations

import json
import sys

from common import DISCLAIMER, load_ref, parse_kv


def plan(input_str: str) -> dict:
    fields = parse_kv(input_str)
    goal = fields.get("goal", "")
    current = int(fields.get("current_fitness", "3"))

    ref = load_ref("training.json")
    paths = ref["training_paths"]

    if not goal or goal not in paths:
        return {
            "error": f"goal '{goal}' 未匹配；可选: {list(paths.keys())}",
            "disclaimer": DISCLAIMER,
        }

    p = paths[goal]
    baseline = ref["fitness_baseline_by_tier"]

    # 提示当前体能差距
    target_fitness = 5 if goal in ("everest", "freediving_pro") else 4 if goal in ("marathon_bmw6", "ironman", "ppl_us_faa") else 3
    gap = max(0, target_fitness - current)

    return {
        "goal": goal,
        "goal_name": p["name"],
        "training": p,
        "your_current_fitness": current,
        "target_fitness": target_fitness,
        "gap": gap,
        "gap_advice": (
            "体能已达标，可直接进入资格 / 装备阶段" if gap == 0
            else f"建议先把基础体能从 tier {current} 提升到 tier {target_fitness}（约需 6-18 个月）"
        ),
        "current_baseline": baseline.get(str(current), {}),
        "target_baseline": baseline.get(str(target_fitness), {}),
        "license_table": ref["license_table"],
        "disclaimer": DISCLAIMER,
    }


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: train.py 'goal=everest|ppl_us_faa|marathon_bmw6|freediving_pro|ironman|f1_grid|current_fitness=1..5'", file=sys.stderr)
        return 2
    try:
        out = plan(sys.argv[1])
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
