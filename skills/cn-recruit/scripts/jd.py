#!/usr/bin/env python3
"""cn-recruit: 从结构化输入生成 JD（岗位描述）.

Input (`|` 分隔，`=` 键值):
  role=后端工程师|family=工程|seniority=中级|location=远程|salary=25-40k*15|tone=活泼
  |industry=SaaS|primary_stack=Go|product_line=客户成功平台|channel=小红书
  |hr_email=hr@example.com|company_short_desc=AI Agent 创业团队|years=4

Output: JSON {role, sections:[...], must_have, nice_to_have, responsibilities, ...}
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "references" / "jd_templates.json"


def _load() -> dict:
    return json.loads(TEMPLATES.read_text(encoding="utf-8"))


def _format(text: str, ctx: dict) -> str:
    out = text
    for key, value in ctx.items():
        out = out.replace("{" + key + "}", str(value))
    return out


def _pick_pool(pool: list[str], take: int) -> list[str]:
    return list(pool[:take])


def build_jd(fields: dict[str, str]) -> dict:
    data = _load()
    family = fields.get("family", "通用")
    family_meta = data["role_families"].get(family) or data["role_families"]["通用"]
    seniority = fields.get("seniority", "中级")
    seniority_meta = data["seniority_modifiers"].get(seniority) or data["seniority_modifiers"]["中级"]
    tone = fields.get("tone", "正式")
    tone_meta = data["tone_presets"].get(tone) or data["tone_presets"]["正式"]

    ctx = {
        "role": fields.get("role", "岗位"),
        "industry": fields.get("industry", "互联网"),
        "primary_stack": fields.get("primary_stack", "主语言/框架"),
        "product_line": fields.get("product_line", "核心产品线"),
        "channel": fields.get("channel", "全渠道"),
        "hr_email": fields.get("hr_email", "hr@example.com"),
        "company_short_desc": fields.get("company_short_desc", "我们的"),
        "seniority": seniority,
        "years": fields.get("years", seniority_meta["years"]),
    }

    must_have = [_format(item, ctx) for item in family_meta["must_have_pool"]]
    must_have.extend(_format(item, ctx) for item in seniority_meta["extra_must"])

    nice_to_have = [_format(item, ctx) for item in family_meta["nice_to_have_pool"]]
    nice_to_have.extend(_format(item, ctx) for item in seniority_meta["extra_nice"])

    responsibilities = [_format(item, ctx) for item in family_meta["responsibility_pool"]]

    return {
        "role": ctx["role"],
        "family": family,
        "seniority": seniority,
        "tone": tone,
        "location": fields.get("location", "远程"),
        "salary": fields.get("salary", "面议"),
        "intro": _format(tone_meta["intro"], ctx),
        "responsibilities": responsibilities,
        "must_have": _pick_pool(must_have, 6),
        "nice_to_have": _pick_pool(nice_to_have, 4),
        "skill_axes": list(family_meta["skill_axes"]),
        "closing": _format(tone_meta["closing"], ctx),
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(
            "usage: jd.py 'role=...|family=工程|seniority=中级|...'",
            file=sys.stderr,
        )
        return 1
    raw = sys.argv[1].strip()
    fields: dict[str, str] = {}
    for chunk in raw.split("|"):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "=" not in chunk:
            print(f"error: bad field '{chunk}'", file=sys.stderr)
            return 1
        key, value = chunk.split("=", 1)
        fields[key.strip()] = value.strip()

    try:
        result = build_jd(fields)
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
