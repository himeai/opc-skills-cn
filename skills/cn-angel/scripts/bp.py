#!/usr/bin/env python3
"""cn-angel: 生成中国天使轮 BP 10 页骨架 + 行业差异化要点 + 反例陷阱.

Input (`|` 分隔，`=` 键值):
  industry=SaaS|stage=天使|model=订阅|north_star_metric=MRR|company=酱油科技
  |one_liner=AI Agent 客户成功平台|round_size_cny_w=600

Output: JSON {industry, stage, deck:[{page, section, must_have, common_pitfalls, ...}], industry_focus, ...}
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "references" / "bp_templates.json"


def _load() -> dict:
    return json.loads(TEMPLATES.read_text(encoding="utf-8"))


def build_bp(fields: dict[str, str]) -> dict:
    data = _load()
    industry = fields.get("industry", "AI 应用")
    stage = fields.get("stage", "天使")

    industry_meta = data["industry_focus"].get(industry) or data["industry_focus"]["AI 应用"]
    stage_meta = data["stage_focus"].get(stage, data["stage_focus"]["天使"])

    company = fields.get("company", "<公司中文名>")
    one_liner = fields.get("one_liner", "<X 行业的 Y>")
    nsm = fields.get("north_star_metric") or industry_meta["north_star_metric_examples"][0]
    round_size = fields.get("round_size_cny_w", "<本轮金额（万元）>")

    deck = []
    for page in data["deck_skeleton"]:
        item = {
            "page": page["page"],
            "section": page["section"],
            "must_have": list(page["must_have"]),
            "common_pitfalls": list(page["common_pitfalls"]),
        }
        if page["section"] == "封面":
            item["fill_in_hint"] = {
                "company": company,
                "one_liner": one_liner,
                "round_size_cny_w": round_size,
            }
        if page["section"] == "数据 / 进展":
            item["north_star_metric"] = nsm
            item["industry_key_metrics"] = industry_meta["key_metrics"]
        if page["section"] == "融资计划":
            item["target_pre_money_hint"] = "用 valuation.py 估算后填入"
        deck.append(item)

    extra_pages_hint = list(industry_meta.get("extra_pages", []))

    return {
        "industry": industry,
        "stage": stage,
        "company": company,
        "one_liner": one_liner,
        "north_star_metric": nsm,
        "round_size_cny_w": round_size,
        "deck": deck,
        "industry_focus": {
            "key_metrics": industry_meta["key_metrics"],
            "extra_pages": extra_pages_hint,
            "prefer_investor": industry_meta["prefer_investor"],
        },
        "stage_focus": stage_meta,
        "disclaimer": "本骨架仅作 BP 撰写参考，不构成投资建议；正式版必须由创始人本人撰写。",
    }


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


def main() -> int:
    if len(sys.argv) != 2:
        print(
            "usage: bp.py 'industry=SaaS|stage=天使|model=订阅|north_star_metric=MRR|...'",
            file=sys.stderr,
        )
        return 1
    try:
        fields = _parse_kv(sys.argv[1].strip())
        result = build_bp(fields)
    except (OSError, json.JSONDecodeError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
