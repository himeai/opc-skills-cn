#!/usr/bin/env python3
"""cn-angel: 投资人画像匹配（仅给类型 / 接洽节奏，不给具体机构联系方式）.

Input (`|` 分隔，`=` 键值):
  industry=SaaS|stage=天使|round_size_cny_w=600|region=北京|prefer=usd

Output: JSON {recommended_personas:[{persona, score, reasons, ...}], approach_strategy}
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "references" / "investor_personas.json"


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


def _check_size_fit(persona: dict, round_size: float) -> tuple[bool, str]:
    lo, hi = persona["typical_check_cny_w"]
    if hi == 0:
        # FA 等中介，不出钱
        return True, "中介机构，不直接出资"
    if lo <= round_size <= hi:
        return True, f"出手区间 {lo}-{hi} 万元，本轮 {round_size} 万元在区间内"
    if round_size < lo:
        return False, f"本轮 {round_size} 万元低于该机构最小 ticket {lo} 万元"
    return False, f"本轮 {round_size} 万元高于该机构最大 ticket {hi} 万元，需要联合投资"


def match_investors(fields: dict[str, str]) -> dict:
    data = _load()
    industry = fields.get("industry", "AI 应用")
    stage = fields.get("stage", "天使")
    round_size_str = fields.get("round_size_cny_w", "")
    try:
        round_size = float(round_size_str) if round_size_str else 0.0
    except ValueError:
        round_size = 0.0
    prefer = fields.get("prefer", "").lower()

    stage_recs = data["stage_persona_recommendations"].get(stage, [])
    industry_recs = data["industry_persona_recommendations"].get(industry, [])

    scored = []
    for name, persona in data["personas"].items():
        score = 0
        reasons = []
        if name in stage_recs:
            score += 30
            reasons.append(f"匹配阶段 {stage}")
        if name in industry_recs:
            score += 30
            reasons.append(f"匹配行业 {industry}")
        if industry in persona.get("good_fit", []):
            score += 15
            reasons.append(f"明确适合 {industry}")
        if industry in persona.get("bad_fit", []):
            score -= 30
            reasons.append(f"不适合 {industry}")
        if stage in persona.get("typical_stage", []):
            score += 10
            reasons.append(f"覆盖 {stage} 阶段")

        size_ok, size_note = _check_size_fit(persona, round_size) if round_size > 0 else (True, "未提供 round_size")
        if round_size > 0 and not size_ok:
            score -= 20
        reasons.append(size_note)

        if prefer:
            if prefer in persona["key"].lower():
                score += 15
                reasons.append(f"匹配 prefer={prefer}")

        if score > 0:
            scored.append({
                "persona": name,
                "key": persona["key"],
                "score": score,
                "typical_check_cny_w": persona["typical_check_cny_w"],
                "decision_weeks": persona["decision_weeks"],
                "care_about": persona["care_about"],
                "approach_style": persona["approach_style"],
                "red_flags": persona["red_flags"],
                "reasons": reasons,
            })

    scored.sort(key=lambda x: -x["score"])
    top = scored[:5]

    approach_strategy = [
        "1. 列出每类 persona 下的 5-8 个目标对象（自行通过公开信息筛选）",
        "2. 优先 warm intro（共同认识的人引荐）；cold outreach 用 1-pager 不要附 BP 全文",
        "3. 同时接触 8-15 家保持谈判筹码，但不要过早暴露 TS 进度",
        "4. 每场会后 24h 内补充材料 + 复盘讲法",
        "5. 拿到第一份 TS 后给其他高潜机构 deadline 决策",
    ]

    return {
        "industry": industry,
        "stage": stage,
        "round_size_cny_w": round_size,
        "recommended_personas": top,
        "all_scored": scored,
        "approach_strategy": approach_strategy,
        "compliance_note": "本 skill 不提供具体投资人 / 机构 / 个人的联系方式；具体名单请通过公开渠道（IT 桔子 / 36Kr / 公众号）自行筛选。",
        "disclaimer": "本匹配为基于规则的画像建议，不构成具体投资人推荐。",
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(
            "usage: match.py 'industry=SaaS|stage=天使|round_size_cny_w=600|region=北京|prefer=usd'",
            file=sys.stderr,
        )
        return 1
    try:
        fields = _parse_kv(sys.argv[1].strip())
        result = match_investors(fields)
    except (OSError, json.JSONDecodeError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
