#!/usr/bin/env python3
"""opc-plan-b: 复业准备清单 + 决策树 + 6 类轻资产复业方向.

Input (`|` 分隔，`=` 键值):
  runway_months=8|burnout=5|asset=技术能力|family=条件支持|gap_months=3|prev_industry=SaaS

Output: JSON {decision, recommended_paths, exit_red_lines, action_list}
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "references" / "comeback_paths.json"


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


def _decide(runway_months: float, burnout: int, family: str) -> dict:
    if runway_months < 6:
        verdict = "暂缓复业"
        reason = "跑道 < 6 个月，先零工 / 摆摊回血"
    elif burnout >= 7:
        verdict = "暂缓复业"
        reason = "精神疲惫度过高，先休息 6-12 个月"
    elif "反对" in family:
        verdict = "暂缓复业"
        reason = "家庭明确反对，先打工 6-12 个月修复信任"
    elif runway_months >= 12 and burnout <= 3:
        verdict = "可以复业"
        reason = "跑道充足 + 精神在线，可启动轻资产复业"
    else:
        verdict = "并行模式"
        reason = "跑道一般 / 心力一般 → 零工 + 复业并行，不要 all in"
    return {"verdict": verdict, "reason": reason}


def _recommend_paths(asset: str, paths_data: dict) -> list[dict]:
    asset_to_paths = {
        "技术能力": ["自由职业", "一人 SaaS", "代运营 / Agency"],
        "内容能力": ["内容创作", "知识付费", "代运营 / Agency"],
        "人脉资源": ["代运营 / Agency", "跨境店铺", "知识付费"],
        "资金": ["跨境店铺", "一人 SaaS"],
        "什么都没剩下": [],
    }
    keys = []
    for k, v in asset_to_paths.items():
        if k in asset:
            keys = v
            break
    if not keys:
        return []
    out = []
    for key in keys:
        if key in paths_data:
            entry = dict(paths_data[key])
            entry["path"] = key
            out.append(entry)
    return out


def build_restart(fields: dict[str, str]) -> dict:
    data = _load()
    try:
        runway_months = float(fields.get("runway_months", "6"))
        burnout = int(fields.get("burnout", "5"))
    except ValueError as exc:
        raise ValueError(f"bad number: {exc}") from exc

    asset = fields.get("asset", "什么都没剩下")
    family = fields.get("family", "条件支持")
    gap_months = fields.get("gap_months", "3")
    prev_industry = fields.get("prev_industry", "未指定")

    decision = _decide(runway_months, burnout, family)
    recommended = _recommend_paths(asset, data["comeback_paths"])

    action_list = []
    if decision["verdict"] == "暂缓复业":
        action_list.append("先去 gig.py 找一份零工，3-6 个月后再回来重新评估")
        action_list.append("用空出来的时间陪家人 / 调休 / 体检")
        action_list.append("把上次创业的复盘写成长文（小红书 / 公众号 / 内部文档），将来是 IP 起点")
    elif decision["verdict"] == "并行模式":
        action_list.append("零工每周占 3-4 天保现金流")
        action_list.append("剩余 2-3 天用于复业冷启动")
        action_list.append("3 个月后用 KPI 决定是否 all in")
    else:
        action_list.append("先列退出红线（时间 + 资金 + 心力 + 家庭 4 项）")
        action_list.append("最小可行启动（不重新办公司、不招人、不订阅 SaaS）")
        action_list.append("第 1-3 个月只做用户访谈 + 单点验证，不放大投入")

    return {
        "input": {
            "runway_months": runway_months,
            "burnout": burnout,
            "asset": asset,
            "family": family,
            "gap_months": gap_months,
            "prev_industry": prev_industry,
        },
        "decision": decision,
        "decision_tree": data["decision_tree"],
        "recommended_paths": recommended,
        "exit_red_lines": data["exit_red_lines"],
        "action_list": action_list,
        "general_notes": list(data["general_notes"]),
        "disclaimer": "本清单不构成职业 / 心理 / 财务建议；连续创业失败叠加风险高，请慎重。",
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(
            "usage: restart.py 'runway_months=8|burnout=5|asset=技术能力|family=条件支持'",
            file=sys.stderr,
        )
        return 1
    try:
        fields = _parse_kv(sys.argv[1].strip())
        result = build_restart(fields)
    except (OSError, json.JSONDecodeError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
