#!/usr/bin/env python3
"""cn-geo: 给定品牌输出 GEO 全景行动清单.

Input:  "brand=Acme|category=saas_b2b|stage=early|website=acme.example.com"
Output: JSON {brand, category, stage, dimensions: [...], top_3_next_actions: [...]}
"""

from __future__ import annotations

from cli_common import load_ref, require, run_kv_cli  # type: ignore[import-not-found]


VALID_STAGES = ("pre_launch", "early", "growth", "mature")


def build_audit(fields: dict[str, str]) -> dict:
    """Build a GEO audit report for the given brand."""
    brand, category = require(fields, "brand", "category")
    stage = fields.get("stage", "early")
    if stage not in VALID_STAGES:
        raise ValueError(f"stage must be one of {VALID_STAGES}, got '{stage}'")
    website = fields.get("website", "")

    categories = load_ref("categories")["categories"]
    if category not in categories:
        raise ValueError(
            f"unknown category '{category}', see references/categories.json"
        )
    cat_meta = categories[category]

    rules = load_ref("audit_rules")["dimensions"]
    dimensions: list[dict] = []
    flat_actions: list[dict] = []
    for dim in rules:
        applicable = [a for a in dim["actions"] if stage in a["stage"]]
        applicable.sort(key=lambda a: a["priority"])
        dimensions.append({
            "name": dim["name"],
            "label": dim["label"],
            "why": dim["why"],
            "actions": [
                {"id": a["id"], "label": a["label"], "priority": a["priority"]}
                for a in applicable
            ],
        })
        for action in applicable:
            flat_actions.append({
                "dimension": dim["name"],
                "id": action["id"],
                "label": action["label"],
                "priority": action["priority"],
            })

    flat_actions.sort(key=lambda a: a["priority"])
    top3 = flat_actions[:3]

    return {
        "brand": brand,
        "category": category,
        "category_label": cat_meta["label"],
        "stage": stage,
        "website": website,
        "dimensions": dimensions,
        "top_3_next_actions": top3,
        "primary_audience": cat_meta.get("primary_audience", []),
    }


def main() -> int:
    """Entry point for audit.py."""
    return run_kv_cli(
        'audit.py "brand=X|category=X|stage=pre_launch|early|growth|mature|website=X"',
        build_audit,
    )


if __name__ == "__main__":
    raise SystemExit(main())
