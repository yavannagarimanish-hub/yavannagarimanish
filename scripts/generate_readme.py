#!/usr/bin/env python3
"""Generate README.md from profile.json and a markdown template.

The script enforces a predictable README format and fails fast when required
fields are missing, improving reliability for CI and local updates.
"""

from __future__ import annotations

import json
from pathlib import Path
from string import Template
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "profile.json"
TEMPLATE_PATH = ROOT / "templates" / "README.template.md"
README_PATH = ROOT / "README.md"

REQUIRED_FIELDS = {
    "name",
    "headline",
    "mission",
    "focus_areas",
    "current_projects",
    "impact_metrics",
    "contact",
}


def load_profile(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    missing = REQUIRED_FIELDS.difference(data)
    if missing:
        raise ValueError(f"Missing required fields in profile.json: {sorted(missing)}")
    return data


def as_bulleted(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def projects_bulleted(projects: list[dict[str, str]]) -> str:
    lines = []
    for project in projects:
        name = project.get("name", "Unnamed Project")
        description = project.get("description", "No description provided.")
        lines.append(f"- **{name}**: {description}")
    return "\n".join(lines)


def metrics_bulleted(metrics: list[dict[str, str]]) -> str:
    return "\n".join(f"- **{m.get('value', '-') }** {m.get('label', 'Metric')}" for m in metrics)


def contact_bulleted(contact: dict[str, str]) -> str:
    lines = []
    if contact.get("email"):
        lines.append(f"- Email: {contact['email']}")
    if contact.get("linkedin"):
        lines.append(f"- LinkedIn: {contact['linkedin']}")
    if contact.get("website"):
        lines.append(f"- Website: {contact['website']}")
    return "\n".join(lines)


def render(profile: dict[str, Any], template_text: str) -> str:
    values = {
        "name": profile["name"],
        "headline": profile["headline"],
        "mission": profile["mission"],
        "focus_areas": as_bulleted(profile["focus_areas"]),
        "current_projects": projects_bulleted(profile["current_projects"]),
        "impact_metrics": metrics_bulleted(profile["impact_metrics"]),
        "contact": contact_bulleted(profile["contact"]),
    }
    return Template(template_text).safe_substitute(values).strip() + "\n"


def main() -> None:
    profile = load_profile(PROFILE_PATH)
    template_text = TEMPLATE_PATH.read_text(encoding="utf-8")
    rendered = render(profile, template_text)
    README_PATH.write_text(rendered, encoding="utf-8")
    print(f"README generated at {README_PATH}")


if __name__ == "__main__":
    main()
