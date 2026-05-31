#!/usr/bin/env python3
"""Check consistency across skill directories and registries."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def _load_json(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as file_obj:
            data = json.load(file_obj)
    except FileNotFoundError as exc:
        raise ValueError(f"missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return data


def _names_from_entries(entries: Any, source: str) -> set[str]:
    if entries is None:
        return set()
    if not isinstance(entries, list):
        raise ValueError(f"{source} must be a list")
    names: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise ValueError(f"{source}[{index}] must be an object")
        name = entry.get("name") or entry.get("id") or entry.get("slug")
        if not isinstance(name, str) or not name:
            raise ValueError(f"{source}[{index}] missing non-empty name/id/slug")
        names.add(name)
    return names


def _marketplace_names(data: dict[str, Any]) -> set[str]:
    for key in ("skills", "plugins", "items"):
        if key in data:
            return _names_from_entries(data[key], f"marketplace.json:{key}")
    return set()


def _implemented_skill_dirs() -> set[str]:
    skills_dir = ROOT / "skills"
    if not skills_dir.exists():
        return set()
    names: set[str] = set()
    for child in skills_dir.iterdir():
        if not child.is_dir() or child.name.startswith("."):
            continue
        if (child / "scripts" / "credential.py").exists():
            names.add(child.name)
    return names


def _format_set(values: set[str]) -> str:
    return ", ".join(sorted(values)) if values else "<empty>"


def main() -> int:
    try:
        skills_json = _load_json(ROOT / "skills.json")
        marketplace_json = _load_json(ROOT / ".claude-plugin" / "marketplace.json")
        dir_names = _implemented_skill_dirs()
        registry_names = _names_from_entries(skills_json.get("skills"), "skills.json:skills")
        marketplace_names = _marketplace_names(marketplace_json)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    expected = dir_names
    errors: list[str] = []
    if registry_names != expected:
        errors.append(
            "skills.json mismatch: "
            f"expected {_format_set(expected)}, got {_format_set(registry_names)}"
        )
    if marketplace_names != expected:
        errors.append(
            "marketplace.json mismatch: "
            f"expected {_format_set(expected)}, got {_format_set(marketplace_names)}"
        )
    if registry_names != marketplace_names:
        errors.append(
            "registry mismatch: "
            f"skills.json={_format_set(registry_names)}, "
            f"marketplace.json={_format_set(marketplace_names)}"
        )

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"OK: {len(expected)} implemented skill(s) registered consistently")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
