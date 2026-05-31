#!/usr/bin/env python3
"""Validate SKILL.md frontmatter for opc-skills-cn."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ALLOWED_KEYS = ("name", "description")
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def _fail(message: str) -> int:
    print(f"error: {message}", file=sys.stderr)
    return 1


def _parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md must start with YAML frontmatter delimiter '---'")

    end_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_index = index
            break
    if end_index is None:
        raise ValueError("frontmatter closing delimiter '---' not found")

    data: dict[str, str] = {}
    for line_number, raw_line in enumerate(lines[1:end_index], start=2):
        line = raw_line.strip()
        if not line:
            continue
        if ":" not in line:
            raise ValueError(f"frontmatter line {line_number} is not a key-value pair")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key in data:
            raise ValueError(f"duplicate frontmatter key: {key}")
        data[key] = value
    return data


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"file not found: {path}"]
    if path.name != "SKILL.md":
        errors.append("file name must be SKILL.md")

    try:
        data = _parse_frontmatter(path)
    except ValueError as exc:
        return [str(exc)]

    keys = set(data)
    allowed = set(ALLOWED_KEYS)
    extra = sorted(keys - allowed)
    missing = [key for key in ALLOWED_KEYS if key not in data]
    if extra:
        errors.append(f"frontmatter contains unsupported keys: {', '.join(extra)}")
    if missing:
        errors.append(f"frontmatter missing required keys: {', '.join(missing)}")

    name = data.get("name", "")
    description = data.get("description", "")
    if name and not NAME_PATTERN.fullmatch(name):
        errors.append("name must be kebab-case lowercase letters and digits")
    if description and "Use when" not in description:
        errors.append("description must include 'Use when' trigger guidance")

    parts = path.resolve().parts
    if "skills" in parts and path.parent.name != name:
        errors.append("frontmatter name must match skills/<name> directory")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SKILL.md frontmatter.")
    parser.add_argument("file", help="Path to SKILL.md")
    args = parser.parse_args()

    path = Path(args.file)
    errors = validate(path)
    if errors:
        for error in errors:
            _fail(error)
        return 1
    print(f"OK: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
