"""Validate every manifest-listed skill against the Agent Skills specification."""

import json
from pathlib import Path

try:
    from skills_ref import validate
except ImportError as exc:
    raise SystemExit(
        "skills-ref is required. Run: "
        "python -m pip install -r requirements-validation.txt"
    ) from exc

try:
    from scripts.openai_validation import (
        OpenAiMetadataError,
        validate_openai_metadata,
    )
    from scripts.skill_validation import SkillMetadataError, validate_skill_metadata
except ModuleNotFoundError:  # Direct execution: python scripts/validate_skills.py
    from openai_validation import OpenAiMetadataError, validate_openai_metadata
    from skill_validation import SkillMetadataError, validate_skill_metadata


MANIFEST_PATHS = (
    Path(".claude-plugin/plugin.json"),
    Path(".codex-plugin/plugin.json"),
    Path(".cursor-plugin/plugin.json"),
    Path("gemini-extension.json"),
)


class SkillDiscoveryError(ValueError):
    """Raised when plugin manifests cannot define a portable validation set."""


def discover_skill_paths(repo_root: Path) -> dict[Path, str]:
    """Return contained, same-name skill paths from every plugin allowlist."""

    plugins_dir = (repo_root / "plugins").resolve()
    if not plugins_dir.is_dir():
        raise SkillDiscoveryError(f"Plugins directory is missing: {plugins_dir}")

    skill_paths: dict[Path, str] = {}
    paths_by_name: dict[str, Path] = {}
    for plugin_root in sorted(plugins_dir.iterdir()):
        if not plugin_root.is_dir():
            continue
        resolved_plugin_root = plugin_root.resolve()
        for relative_manifest in MANIFEST_PATHS:
            manifest = plugin_root / relative_manifest
            if not manifest.is_file():
                continue
            try:
                data = json.loads(manifest.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, json.JSONDecodeError) as exc:
                raise SkillDiscoveryError(f"Cannot read {manifest}: {exc}") from exc
            if not isinstance(data, dict):
                raise SkillDiscoveryError(f"Manifest must contain an object: {manifest}")
            entries = data.get("skills")
            if entries is None:
                continue
            if not isinstance(entries, list):
                raise SkillDiscoveryError(f"Manifest has no skills list: {manifest}")
            for entry in entries:
                if not isinstance(entry, dict):
                    raise SkillDiscoveryError(
                        f"Manifest has an invalid skill entry: {manifest}"
                    )
                name = entry.get("name")
                relative_path = entry.get("path")
                if not isinstance(name, str) or not name:
                    raise SkillDiscoveryError(
                        f"Manifest skill has no name: {manifest}"
                    )
                if not isinstance(relative_path, str) or not relative_path:
                    raise SkillDiscoveryError(
                        f"Manifest skill {name!r} has no path: {manifest}"
                    )
                candidate = Path(relative_path)
                if candidate.is_absolute():
                    raise SkillDiscoveryError(
                        f"Manifest skill path must be relative: {relative_path}"
                    )
                skill_path = (plugin_root / candidate).resolve()
                try:
                    skill_path.relative_to(resolved_plugin_root)
                except ValueError as exc:
                    raise SkillDiscoveryError(
                        f"Manifest skill path escapes plugin root: {relative_path}"
                    ) from exc
                if skill_path.name != name:
                    raise SkillDiscoveryError(
                        f"Skill directory name does not match {name!r}: {skill_path}"
                    )

                previous_name = skill_paths.setdefault(skill_path, name)
                if previous_name != name:
                    raise SkillDiscoveryError(
                        f"Manifest names disagree for {skill_path}: "
                        f"{previous_name!r} and {name!r}"
                    )
                previous_path = paths_by_name.setdefault(name, skill_path)
                if previous_path != skill_path:
                    raise SkillDiscoveryError(
                        f"Manifest paths disagree for {name!r}: "
                        f"{previous_path} and {skill_path}"
                    )
    return skill_paths


def main() -> None:
    """Validate plugin allowlists rather than gated or scout snapshots."""

    repo_root = Path(__file__).resolve().parents[1]
    try:
        skill_paths = discover_skill_paths(repo_root)
    except SkillDiscoveryError as exc:
        raise SystemExit(str(exc)) from exc

    failures = 0
    for skill_path, skill_name in sorted(
        skill_paths.items(), key=lambda item: item[0].as_posix()
    ):
        problems = list(validate(skill_path))
        try:
            validate_skill_metadata(skill_path / "SKILL.md", skill_name)
            validate_openai_metadata(skill_path, skill_name)
        except (OpenAiMetadataError, SkillMetadataError) as exc:
            problems.append(str(exc))
        if problems:
            failures += 1
            print(f"FAILED {skill_name}")
            for problem in problems:
                print(f"  - {problem}")
        else:
            print(f"PASSED {skill_name}")

    if failures:
        raise SystemExit(
            f"\n{failures} manifest-listed skill(s) failed Agent Skills validation."
        )
    print(
        f"\nAll {len(skill_paths)} manifest-listed skills follow the "
        "Agent Skills specification."
    )


if __name__ == "__main__":
    main()
