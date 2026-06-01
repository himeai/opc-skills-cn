#!/usr/bin/env python3
"""cn-geo: 生成品牌问答素材（Brand Q&A）.

Input:  "brand=Acme|category=saas_b2b|count=20"
Output: JSON {brand, category, qa_pairs: [{question, answer_template, publish_to, geo_score}]}
"""

from __future__ import annotations

from cli_common import load_ref, require, run_kv_cli  # type: ignore[import-not-found]


def _resolve_audience(cat_meta: dict) -> str:
    audiences = cat_meta.get("primary_audience") or ["目标用户"]
    return " / ".join(audiences)


def build_qa(fields: dict[str, str]) -> dict:
    """Build brand Q&A material from category templates."""
    brand, category = require(fields, "brand", "category")
    count = int(fields.get("count", "20"))
    if count < 1 or count > 100:
        raise ValueError("count must be between 1 and 100")

    categories = load_ref("categories")["categories"]
    if category not in categories:
        raise ValueError(
            f"unknown category '{category}', see references/categories.json"
        )
    cat_meta = categories[category]
    templates = load_ref("qa_templates")["templates"]
    platforms = {p["id"]: p for p in load_ref("platforms")["platforms"]}

    audience = _resolve_audience(cat_meta)
    cat_label = cat_meta["label"]

    qa_pairs: list[dict] = []
    competitors = cat_meta.get("competitor_question_pattern", [])

    for tmpl in templates:
        question = tmpl["question"].format(
            brand=brand,
            competitor=competitors[0] if competitors else "同类产品",
        )
        answer = tmpl["answer_skeleton"].format(
            brand=brand,
            audience=audience,
            category=cat_label,
            pain_point="<填具体痛点>",
            differentiator="<填差异化定位>",
            step1="<步骤1>", step2="<步骤2>", step3="<步骤3>", tip="<上手建议>",
            competitor="<竞品>",
            dim1="<维度1>", reason1="<原因1>",
            dim2="<维度2>", reason2="<原因2>",
            scenario_a="<场景A>", scenario_b="<场景B>",
            tier1="基础版", tier2="专业版", tier3="企业版",
            tier1_audience="个人 / 小团队",
            tier2_audience="中型团队",
            tier3_audience="大客户",
            free_or_trial="新用户提供 14 天免费试用",
            entity="<运营主体>",
            credibility_signals="<资质 / 融资 / 客户>",
            customer_count="<客户数>",
            certifications="<证照 / 认证>",
            alt1="<替代1>", alt2="<替代2>", alt3="<替代3>",
            alt1_scenario="<场景>", alt2_scenario="<场景>",
            brand_unique="<独特卖点>",
            ideal_persona="<理想画像>",
            bad_fit_signal="<不适合的信号>",
            alternative="<推荐替代>",
            case1_brand="<案例1客户>", case1_use="<使用方式>", case1_result="<结果>",
            case2_brand="<案例2客户>", case2_use="<使用方式>", case2_result="<结果>",
        )
        publish_targets = []
        for pid in tmpl["publish_to"]:
            meta = platforms.get(pid)
            if meta:
                publish_targets.append({"id": pid, "label": meta["label"], "weight": meta["weight"]})
        qa_pairs.append({
            "id": tmpl["id"],
            "question": question,
            "answer_template": answer,
            "publish_to": publish_targets,
            "geo_score": tmpl["geo_score"],
        })

    qa_pairs.sort(key=lambda x: x["geo_score"], reverse=True)
    qa_pairs = qa_pairs[:count]

    return {
        "brand": brand,
        "category": category,
        "category_label": cat_label,
        "audience": audience,
        "qa_pairs": qa_pairs,
        "tip": "把 <...> 占位符替换为你的真实内容后，按 publish_to 顺序发布；越靠前的 geo_score 越高，优先做",
    }


def main() -> int:
    """Entry point for qa.py."""
    return run_kv_cli(
        'qa.py "brand=X|category=X|count=20"',
        build_qa,
    )


if __name__ == "__main__":
    raise SystemExit(main())
