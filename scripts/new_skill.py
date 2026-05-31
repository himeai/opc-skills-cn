#!/usr/bin/env python3
"""Create a new skill skeleton from template/SKILL.md."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


CREDENTIAL_TEMPLATE = '''#!/usr/bin/env python3
"""Credential helpers for {skill_name}."""

from __future__ import annotations

import os


def get_credentials() -> dict[str, str | None]:
    """Read credentials from environment variables only."""
    return {{
        "api_key": os.environ.get("{env_prefix}_API_KEY"),
    }}
'''


def _env_prefix(skill_name: str) -> str:
    return skill_name.upper().replace("-", "_")


def create_skill(skill_name: str) -> Path:
    if not NAME_PATTERN.fullmatch(skill_name):
        raise ValueError("skill name must be kebab-case lowercase letters and digits")

    target = ROOT / "skills" / skill_name
    if target.exists():
        raise ValueError(f"skill already exists: {target}")

    template = ROOT / "template" / "SKILL.md"
    if not template.exists():
        raise ValueError(f"template not found: {template}")

    scripts_dir = target / "scripts"
    examples_dir = target / "examples"
    references_dir = target / "references"
    scripts_dir.mkdir(parents=True)
    examples_dir.mkdir()
    references_dir.mkdir()

    skill_md = target / "SKILL.md"
    shutil.copyfile(template, skill_md)
    text = skill_md.read_text(encoding="utf-8")
    text = text.replace("name: skill-name-here", f"name: {skill_name}", 1)
    skill_md.write_text(text, encoding="utf-8")

    credential_py = scripts_dir / "credential.py"
    credential_py.write_text(
        CREDENTIAL_TEMPLATE.format(
            skill_name=skill_name,
            env_prefix=_env_prefix(skill_name),
        ),
        encoding="utf-8",
    )
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a new skill skeleton.")
    parser.add_argument("name", help="Skill name in kebab-case")
    args = parser.parse_args()

    try:
        target = create_skill(args.name)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"created: {target.relative_to(ROOT)}")
    print("next: update SKILL.md, add logo, register skills.json and marketplace.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
