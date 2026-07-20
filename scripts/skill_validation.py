"""Validate the discovery metadata required by active SKILL.md files."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote, urlsplit


SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_FIELD_PATTERN = re.compile(
    r"^([A-Za-z][A-Za-z0-9_-]*):(?:[ \t]*(.*))?$"
)
RESOURCE_REFERENCE_PATTERN = re.compile(
    r"`((?:references|templates|scripts|assets)/[^`\r\n]+)`"
    r"|\]\(((?:references|templates|scripts|assets)/[^)\s]+)\)"
)
MAX_SKILL_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
ALLOWED_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}


class SkillMetadataError(ValueError):
    """Raised when a SKILL.md cannot be discovered safely by agent clients."""


def _plain_scalar(value: str) -> str:
    """Return a simple quoted or unquoted YAML scalar for required metadata."""

    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1].strip()
    return value


def validate_skill_metadata(skill_md: Path, expected_name: str) -> None:
    """Validate frozenSkillz's portable metadata subset against the manifest."""

    try:
        content = skill_md.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise SkillMetadataError(f"cannot read UTF-8 SKILL.md: {exc}") from exc

    lines = content.splitlines()
    if not lines or lines[0] != "---":
        raise SkillMetadataError("missing YAML frontmatter delimited by ---")

    try:
        closing_index = lines.index("---", 1)
    except ValueError as exc:
        raise SkillMetadataError("YAML frontmatter has no closing --- delimiter") from exc

    fields: dict[str, str] = {}
    for line in lines[1:closing_index]:
        if not line.strip() or line.lstrip().startswith("#") or line[0].isspace():
            continue
        match = FRONTMATTER_FIELD_PATTERN.fullmatch(line)
        if not match:
            raise SkillMetadataError(f"invalid YAML frontmatter line: {line!r}")
        key, value = match.groups()
        if key in fields:
            raise SkillMetadataError(f"duplicate {key!r} frontmatter field")
        fields[key] = value or ""

    for required_field in ("name", "description"):
        if fields.get(required_field, "").strip().startswith((">", "|")):
            raise SkillMetadataError(
                f"block scalars are not supported for {required_field!r} metadata"
            )

    name = _plain_scalar(fields.get("name", ""))
    description = _plain_scalar(fields.get("description", ""))
    unexpected_fields = set(fields) - ALLOWED_FIELDS
    if unexpected_fields:
        raise SkillMetadataError(
            "unexpected frontmatter field(s): "
            + ", ".join(sorted(unexpected_fields))
        )
    if not name:
        raise SkillMetadataError("missing non-empty 'name' frontmatter field")
    if not description:
        raise SkillMetadataError("missing non-empty 'description' frontmatter field")
    if len(description) > MAX_DESCRIPTION_LENGTH:
        raise SkillMetadataError(
            f"frontmatter description exceeds {MAX_DESCRIPTION_LENGTH} characters"
        )
    if len(name) > MAX_SKILL_NAME_LENGTH or not SKILL_NAME_PATTERN.fullmatch(name):
        raise SkillMetadataError(
            "frontmatter name must be 1-64 characters of lowercase letters, "
            "digits, and single hyphens"
        )
    if name != expected_name:
        raise SkillMetadataError(
            f"frontmatter name {name!r} does not match manifest name {expected_name!r}"
        )

    skill_root = skill_md.parent.resolve()
    for match in RESOURCE_REFERENCE_PATTERN.finditer(content):
        reference = match.group(1) or match.group(2)
        resource_path = unquote(urlsplit(reference).path)
        candidate = (skill_root / resource_path).resolve()
        try:
            candidate.relative_to(skill_root)
        except ValueError as exc:
            raise SkillMetadataError(
                f"bundled resource reference escapes skill root: {reference!r}"
            ) from exc
        if not candidate.exists():
            raise SkillMetadataError(
                f"bundled resource reference does not exist: {reference!r}"
            )
