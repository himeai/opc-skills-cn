#!/usr/bin/env python3
"""cn-recruit: 候选人筛选评分.

Input: JSON 字符串描述候选人结构化简历，匹配 JD must_have 关键词。

例：
  python3 scripts/score.py '{
    "must_have_keywords": ["Go", "微服务", "K8s", "高并发"],
    "candidate": {
      "skills": ["Go", "K8s", "微服务"],
      "years": 4,
      "target_band": "中级",
      "industry": "SaaS",
      "target_industry": "SaaS",
      "tenures_years": [2.5, 3.1, 1.8],
      "highlights": ["开源贡献者", "技术博客"],
      "title_seniority": "中级",
      "actual_seniority": "中级",
      "max_gap_months": 0,
      "gap_explained": true
    }
  }'

Output: JSON {axes, total_score, verdict, advice, red_flags}
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / "references" / "score_rules.json"


SENIORITY_ORDER = ["实习", "初级", "中级", "高级", "专家"]


def _load() -> dict:
    return json.loads(RULES.read_text(encoding="utf-8"))


def _must_have_hit_ratio(must_have: list[str], skills: list[str]) -> float:
    if not must_have:
        return 1.0
    skills_lower = {s.lower() for s in skills}
    hits = sum(1 for kw in must_have if kw.lower() in skills_lower)
    return hits / len(must_have)


def _years_band(years: float, target_band: str) -> tuple[bool, bool]:
    bands = {"实习": (0, 1), "初级": (1, 3), "中级": (3, 5), "高级": (5, 8), "专家": (8, 50)}
    target = bands.get(target_band, (3, 5))
    in_band = target[0] <= years < target[1]
    one_off = (target[0] - 1 <= years < target[1] + 2)
    return in_band, (one_off and not in_band)


def _avg_tenure(tenures: list[float]) -> float:
    return sum(tenures) / len(tenures) if tenures else 0.0


def _eval_axis(axis: dict, ctx: dict) -> int:
    for rule in axis["rules"]:
        if rule.get("else"):
            return int(rule["score"])
        if _eval_cond(rule["if"], ctx):
            return int(rule["score"])
    return 0


def _eval_cond(expr: str, ctx: dict) -> bool:
    """Tiny safe expression evaluator: supports comparisons + boolean and/or against ctx keys."""
    allowed = {k: v for k, v in ctx.items() if isinstance(v, (int, float, bool))}
    try:
        return bool(eval(expr, {"__builtins__": {}}, allowed))  # nosec B307 - controlled inputs
    except (NameError, SyntaxError, TypeError):
        return False


def _check_red_flags(rules: list[dict], ctx: dict) -> list[dict]:
    flags = []
    for rule in rules:
        if _eval_cond(rule["rule"], ctx):
            flags.append({"key": rule["key"], "note": rule["note"]})
    return flags


def _verdict(total: int, verdicts: list[dict]) -> dict:
    for v in verdicts:
        if total >= v["min_score"]:
            return {"verdict": v["verdict"], "advice": v["advice"]}
    return {"verdict": "未知", "advice": ""}


def score_candidate(must_have: list[str], candidate: dict) -> dict:
    rules = _load()

    skills = candidate.get("skills", [])
    years = float(candidate.get("years", 0))
    target_band = candidate.get("target_band", "中级")
    in_band, one_off = _years_band(years, target_band)
    avg_tenure = _avg_tenure(candidate.get("tenures_years", []))
    title_idx = SENIORITY_ORDER.index(candidate.get("title_seniority", target_band)) \
        if candidate.get("title_seniority") in SENIORITY_ORDER else SENIORITY_ORDER.index(target_band)
    actual_idx = SENIORITY_ORDER.index(candidate.get("actual_seniority", target_band)) \
        if candidate.get("actual_seniority") in SENIORITY_ORDER else SENIORITY_ORDER.index(target_band)

    ctx = {
        "must_have_hit_ratio": _must_have_hit_ratio(must_have, skills),
        "years_in_band": in_band,
        "years_one_band_off": one_off,
        "industry_match": candidate.get("industry") == candidate.get("target_industry"),
        "industry_adjacent": bool(candidate.get("industry_adjacent", False)),
        "avg_tenure_years": avg_tenure,
        "highlights_count": len(candidate.get("highlights", [])),
        "title_seniority": title_idx,
        "actual_seniority": actual_idx,
        "job_count": len(candidate.get("tenures_years", [])),
        "max_gap_months": int(candidate.get("max_gap_months", 0)),
        "gap_explained": bool(candidate.get("gap_explained", True)),
    }

    axes_results = []
    total = 0.0
    for key, axis in rules["axes"].items():
        score = _eval_axis(axis, ctx)
        weight = axis["weight"]
        weighted = score * weight / 100.0
        total += weighted
        axes_results.append({
            "key": key,
            "label": axis["label"],
            "score": score,
            "weight": weight,
            "weighted": round(weighted, 1),
        })

    total_int = int(round(total))
    verdict = _verdict(total_int, rules["verdicts"])

    return {
        "must_have_hit_ratio": round(ctx["must_have_hit_ratio"], 2),
        "total_score": total_int,
        "axes": axes_results,
        "verdict": verdict["verdict"],
        "advice": verdict["advice"],
        "red_flags": _check_red_flags(rules["red_flags"], ctx),
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: score.py '<json payload>'", file=sys.stderr)
        return 1
    try:
        payload = json.loads(sys.argv[1])
        result = score_candidate(
            payload.get("must_have_keywords", []),
            payload.get("candidate", {}),
        )
    except (json.JSONDecodeError, OSError, KeyError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
