#!/usr/bin/env python3
"""cn-geo: 输出指定品类 + 角色的内容主题矩阵.

Input:  "category=saas_b2b|persona=solo_founder"
Output: JSON {category, persona, themes: [{type, label, geo_benefit, topics, best_platforms}]}
"""

from __future__ import annotations

from cli_common import load_ref, require, run_kv_cli  # type: ignore[import-not-found]


VALID_PERSONAS = ("solo_founder", "indie_brand", "studio", "creator", "mcn")


def _expand_seeds(seeds: list[str], category_label: str) -> list[str]:
    out = []
    for seed in seeds:
        out.append(seed.replace("{category}", category_label)
                       .replace("{brand}", "{你的品牌}")
                       .replace("{competitor}", "{竞品名}")
                       .replace("{duration}", "30 天")
                       .replace("{scenario}", "{典型场景}")
                       .replace("{year}", "2026"))
    return out


def build_matrix(fields: dict[str, str]) -> dict:
    """Build the content theme matrix for a category and persona."""
    (category,) = require(fields, "category")
    persona = fields.get("persona", "solo_founder")
    if persona not in VALID_PERSONAS:
        raise ValueError(f"persona must be one of {VALID_PERSONAS}")

    categories = load_ref("categories")["categories"]
    if category not in categories:
        raise ValueError(
            f"unknown category '{category}', see references/categories.json"
        )
    cat_label = categories[category]["label"]

    matrix = load_ref("theme_matrix")
    overrides = matrix.get("persona_overrides", {}).get(persona, {})
    prefer = set(overrides.get("prefer") or [])
    skip = set(overrides.get("skip") or [])

    platforms = {p["id"]: p for p in load_ref("platforms")["platforms"]}

    themes: list[dict] = []
    for theme in matrix["theme_types"]:
        if theme["id"] in skip:
            continue
        themes.append({
            "type": theme["id"],
            "label": theme["label"],
            "geo_benefit": theme["geo_benefit"],
            "preferred_for_persona": theme["id"] in prefer,
            "topics": _expand_seeds(theme["topic_seeds"], cat_label),
            "best_platforms": [
                {"id": pid, "label": platforms[pid]["label"], "weight": platforms[pid]["weight"]}
                for pid in theme["best_platforms"] if pid in platforms
            ],
        })

    themes.sort(
        key=lambda t: (not t["preferred_for_persona"], -t["geo_benefit"])
    )

    return {
        "category": category,
        "category_label": cat_label,
        "persona": persona,
        "themes": themes,
    }


def main() -> int:
    """Entry point for matrix.py."""
    return run_kv_cli(
        'matrix.py "category=X|persona=solo_founder|indie_brand|studio|creator|mcn"',
        build_matrix,
    )


if __name__ == "__main__":
    raise SystemExit(main())
