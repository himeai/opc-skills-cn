#!/usr/bin/env python3
"""opc-plan-b: 公司体面下车清单（个体 / 个独 / 一人有限 / 有限公司）.

Input (`|` 分隔，`=` 键值):
  entity=个独|location=杭州|has_employees=no|has_debt=no|has_abnormal=no

Output: JSON {entity, recommended_path, steps, typical_weeks, common_blockers, warnings}
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "references" / "entity_shutdown.json"


def _load() -> dict:
    return json.loads(TEMPLATES.read_text(encoding="utf-8"))


def _parse_kv(raw: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for chunk in raw.split("|"):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "=" not in chunk:
            raise ValueError(f"bad field '{chunk}'")
        key, value = chunk.split("=", 1)
        fields[key.strip()] = value.strip()
    return fields


def _is_yes(value: str) -> bool:
    return value.strip().lower() in {"yes", "y", "true", "1", "是", "有"}


def build_shutdown(fields: dict[str, str]) -> dict:
    data = _load()
    entity_key = fields.get("entity", "个独")
    entities = data["entities"]
    if entity_key not in entities:
        # try fuzzy match
        for key in entities:
            if entity_key in key or key in entity_key:
                entity_key = key
                break
        else:
            entity_key = "个人独资企业"
    entity = entities[entity_key]

    has_employees = _is_yes(fields.get("has_employees", "no"))
    has_debt = _is_yes(fields.get("has_debt", "no"))
    has_abnormal = _is_yes(fields.get("has_abnormal", "no"))

    paths = list(entity["shutdown_paths"])
    simple_eligible = (
        not has_employees
        and not has_debt
        and not has_abnormal
        and "简易注销" in paths
    )
    if simple_eligible:
        recommended = "简易注销"
    elif "普通注销" in paths:
        recommended = "普通注销"
    else:
        recommended = paths[0] if paths else "普通注销"

    extra_warnings = []
    if has_employees:
        extra_warnings.append("有员工 → 必须先结清工资 / 经济补偿金 / 社保 / 公积金，并完成劳动关系解除手续")
    if has_debt:
        extra_warnings.append("有未结债务 → 简易注销不适用；建议先结债或聘请律师走清算 / 破产程序")
    if has_abnormal:
        extra_warnings.append("已列入异常名录 / 失信名单 → 必须先解除异常状态才能注销")

    return {
        "entity": entity["display"],
        "location": fields.get("location", "未指定"),
        "recommended_path": recommended,
        "all_paths": paths,
        "simple_eligible": simple_eligible,
        "simple_eligible_when": list(entity["simple_eligible_when"]),
        "steps": list(entity["steps"]),
        "typical_weeks": entity["typical_weeks"],
        "common_blockers": list(entity["common_blockers"]),
        "extra_warnings": extra_warnings,
        "general_warnings": list(data["general_warnings"]),
        "disclaimer": "本清单不构成法律 / 税务建议；复杂案例建议聘请律师或注销代办。",
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(
            "usage: shutdown.py 'entity=个独|location=杭州|has_employees=no|has_debt=no'",
            file=sys.stderr,
        )
        return 1
    try:
        fields = _parse_kv(sys.argv[1].strip())
        result = build_shutdown(fields)
    except (OSError, json.JSONDecodeError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
