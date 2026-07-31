"""Validate the discovery metadata required by active SKILL.md files."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment setup failure
    # Hard dependency, deliberately not optional: this re-raises instead of
    # degrading to a weaker check. A validator that silently skips YAML parsing
    # when PyYAML is absent would report PASSED for frontmatter that no agent
    # client can load, which is the exact failure this module exists to catch.
    raise ImportError(
        "PyYAML is required to validate SKILL.md frontmatter; install it with "
        "'python -m pip install -r requirements-validation.txt'"
    ) from exc


SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
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


class _StrictSafeLoader(yaml.SafeLoader):
    """``SafeLoader`` that rejects duplicate mapping keys.

    PyYAML silently keeps the last of a set of duplicate keys. Agent clients
    disagree about which value wins, so treat duplicates as an authoring error
    rather than letting the ambiguity ship.
    """

    def construct_mapping(self, node, deep: bool = False):
        seen: set[Any] = set()
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                duplicate = key in seen
            except TypeError:  # unhashable key; construct_mapping reports it
                continue
            if duplicate:
                raise SkillMetadataError(
                    f"duplicate {key!r} frontmatter field"
                )
            seen.add(key)
        return super().construct_mapping(node, deep=deep)


def _parse_frontmatter_fields(block: str, offset: int) -> dict[str, Any]:
    """Parse the frontmatter block with a real YAML parser.

    ``block`` is the text between the ``---`` delimiters and ``offset`` is the
    1-based file line number it starts on. The block is padded with leading
    newlines so that line/column numbers in PyYAML errors point at the real
    location in the SKILL.md rather than at an offset inside the slice.
    """

    padded = "\n" * (offset - 1) + block
    try:
        # _StrictSafeLoader subclasses SafeLoader, so this is not yaml.unsafe_load.
        document = yaml.load(padded, Loader=_StrictSafeLoader)
    except yaml.YAMLError as exc:
        detail = " ".join(str(exc).split())
        raise SkillMetadataError(f"invalid YAML frontmatter: {detail}") from exc

    if document is None:
        return {}
    if not isinstance(document, dict):
        raise SkillMetadataError(
            "YAML frontmatter must be a mapping of fields, got "
            f"{type(document).__name__}"
        )

    non_string_keys = sorted(
        repr(key) for key in document if not isinstance(key, str)
    )
    if non_string_keys:
        raise SkillMetadataError(
            "frontmatter field name(s) must be strings: "
            + ", ".join(non_string_keys)
        )
    return document


def _required_text(fields: dict[str, Any], key: str) -> str:
    """Return a required string field, or '' when absent or explicitly null."""

    value = fields.get(key)
    if value is None:
        return ""
    if not isinstance(value, str):
        raise SkillMetadataError(
            f"frontmatter {key!r} must be a string, got {type(value).__name__}"
        )
    return value.strip()


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

    fields = _parse_frontmatter_fields(
        "\n".join(lines[1:closing_index]), offset=2
    )

    name = _required_text(fields, "name")
    description = _required_text(fields, "description")
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
