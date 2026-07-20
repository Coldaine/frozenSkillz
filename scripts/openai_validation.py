"""Validate optional Codex UI metadata distributed with an Agent Skill."""

from __future__ import annotations

import re
from pathlib import Path

import yaml


REQUIRED_INTERFACE_FIELDS = {
    "display_name",
    "short_description",
    "default_prompt",
}


class OpenAiMetadataError(ValueError):
    """Raised when optional agents/openai.yaml metadata is malformed."""


def _require_string(mapping: dict, field: str, owner: str) -> str:
    """Return a required, non-empty string field from an Agent Skills mapping."""

    value = mapping.get(field)
    if not isinstance(value, str) or not value.strip():
        raise OpenAiMetadataError(f"{owner}.{field} must be a non-empty string")
    return value.strip()


def _validate_optional_icon(skill_root: Path, interface: dict, field: str) -> None:
    """Require optional interface icon paths to remain inside the skill bundle."""

    value = interface.get(field)
    if value is None:
        return
    if not isinstance(value, str) or not value.strip():
        raise OpenAiMetadataError(f"interface.{field} must be a non-empty string")
    candidate = (skill_root / value).resolve()
    try:
        candidate.relative_to(skill_root)
    except ValueError as exc:
        raise OpenAiMetadataError(f"interface.{field} escapes the skill root") from exc
    if not candidate.is_file():
        raise OpenAiMetadataError(f"interface.{field} does not resolve to a file")


def validate_openai_metadata(skill_root: Path, expected_name: str) -> None:
    """Validate agents/openai.yaml when a skill distributes the optional file."""

    skill_root = skill_root.resolve()
    metadata_path = skill_root / "agents/openai.yaml"
    if not metadata_path.exists():
        return
    if not metadata_path.is_file():
        raise OpenAiMetadataError("agents/openai.yaml must be a regular file")
    try:
        document = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise OpenAiMetadataError(
            f"cannot read valid agents/openai.yaml: {exc}"
        ) from exc
    if not isinstance(document, dict):
        raise OpenAiMetadataError("agents/openai.yaml must contain a mapping")

    interface = document.get("interface")
    if not isinstance(interface, dict):
        raise OpenAiMetadataError("agents/openai.yaml interface must be a mapping")
    missing_interface = REQUIRED_INTERFACE_FIELDS - set(interface)
    if missing_interface:
        raise OpenAiMetadataError(
            "agents/openai.yaml is missing interface field(s): "
            + ", ".join(sorted(missing_interface))
        )

    _require_string(interface, "display_name", "interface")
    short_description = _require_string(
        interface, "short_description", "interface"
    )
    if not 25 <= len(short_description) <= 64:
        raise OpenAiMetadataError(
            "interface.short_description must contain 25-64 characters"
        )
    default_prompt = _require_string(interface, "default_prompt", "interface")
    if f"${expected_name}" not in default_prompt:
        raise OpenAiMetadataError(
            f"interface.default_prompt must mention ${expected_name}"
        )

    for icon_field in ("icon_small", "icon_large"):
        _validate_optional_icon(skill_root, interface, icon_field)
    brand_color = interface.get("brand_color")
    if brand_color is not None and (
        not isinstance(brand_color, str)
        or not re.fullmatch(r"#[0-9A-Fa-f]{6}", brand_color)
    ):
        raise OpenAiMetadataError(
            "interface.brand_color must be a six-digit hex color"
        )

    dependencies = document.get("dependencies")
    if dependencies is not None:
        if not isinstance(dependencies, dict):
            raise OpenAiMetadataError(
                "agents/openai.yaml dependencies must be a mapping"
            )
        tools = dependencies.get("tools")
        if tools is not None and not isinstance(tools, list):
            raise OpenAiMetadataError("dependencies.tools must be a list")

    policy = document.get("policy")
    if policy is not None:
        if not isinstance(policy, dict):
            raise OpenAiMetadataError(
                "agents/openai.yaml policy must be a mapping"
            )
        implicit = policy.get("allow_implicit_invocation")
        if implicit is not None and not isinstance(implicit, bool):
            raise OpenAiMetadataError(
                "policy.allow_implicit_invocation must be a boolean"
            )
