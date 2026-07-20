import json
from pathlib import Path

try:
    import sync_frozen_skills
except ModuleNotFoundError:  # Direct execution: python scripts/validate_manifests.py
    from scripts import sync_frozen_skills

try:
    from scripts.skill_validation import SkillMetadataError, validate_skill_metadata
except ModuleNotFoundError:  # Direct execution: python scripts/validate_manifests.py
    from skill_validation import SkillMetadataError, validate_skill_metadata


PLUGIN_MANIFESTS = [
    ".claude-plugin/plugin.json",
    ".codex-plugin/plugin.json",
    ".cursor-plugin/plugin.json",
    "gemini-extension.json",
]


def load_json(filepath):
    with filepath.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_manifest(filepath):
    print(f"Validating {filepath}...")
    try:
        data = load_json(filepath)
        required_fields = ["name", "version", "description"]
        missing = [field for field in required_fields if field not in data]
        if missing:
            print(f"  FAILED: Missing fields {missing}")
            return False

        plugin_root = filepath.parent.parent if filepath.name == "plugin.json" else filepath.parent
        resolved_plugin_root = plugin_root.resolve()
        for skill in data.get("skills", []):
            skill_name = skill.get("name")
            if not skill_name:
                print("  FAILED: Skill entry missing name")
                return False
            skill_path = skill.get("path")
            if not skill_path:
                print("  FAILED: Skill entry missing path")
                return False

            candidate_path = Path(skill_path)
            if candidate_path.is_absolute():
                print(f"  FAILED: Skill path must be relative: {skill_path}")
                return False

            resolved_skill_path = (plugin_root / candidate_path).resolve()
            try:
                resolved_skill_path.relative_to(resolved_plugin_root)
            except ValueError:
                print(f"  FAILED: Skill path escapes plugin root: {skill_path}")
                return False

            if not resolved_skill_path.exists():
                print(f"  FAILED: Missing skill path {resolved_skill_path}")
                return False
            if resolved_skill_path.name != skill_name:
                print(
                    "  FAILED: Skill directory name does not match manifest name: "
                    f"{resolved_skill_path.name!r} != {skill_name!r}"
                )
                return False

            skill_md = resolved_skill_path / "SKILL.md"
            if not skill_md.is_file():
                print(f"  FAILED: Missing SKILL.md {skill_md}")
                return False
            try:
                validate_skill_metadata(skill_md, skill_name)
            except SkillMetadataError as exc:
                print(f"  FAILED: Invalid {skill_md}: {exc}")
                return False

        print("  PASSED")
        return True
    except Exception as exc:
        print(f"  FAILED: {exc}")
        return False


def discover_manifests():
    manifests = []
    for plugin_root in sorted(Path("plugins").iterdir()):
        if not plugin_root.is_dir():
            continue
        for relative_manifest in PLUGIN_MANIFESTS:
            manifest = plugin_root / relative_manifest
            if manifest.exists():
                manifests.append(manifest)
    return manifests


def validate_profiles(repo_root):
    profile_paths = sorted((repo_root / "profiles").glob("*.json"))
    if not profile_paths:
        return True, 0
    try:
        _, _, sources = sync_frozen_skills.load_distribution(repo_root)
        for profile_path in profile_paths:
            print(f"Validating {profile_path}...")
            sync_frozen_skills.load_profile(repo_root, profile_path.stem, sources)
            print("  PASSED")
        return True, len(profile_paths)
    except sync_frozen_skills.SyncError as exc:
        print(f"  FAILED: {exc}")
        return False, len(profile_paths)


def main():
    manifests = discover_manifests()
    results = [validate_manifest(manifest) for manifest in manifests]
    profiles_valid, profile_count = validate_profiles(Path.cwd().resolve())

    if manifests and all(results) and profiles_valid:
        print(
            f"\nAll {len(manifests)} manifests and {profile_count} profiles "
            "validated successfully."
        )
        return

    print(f"\nValidation failed. Found {len(manifests)} manifests.")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
