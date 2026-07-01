import json
from pathlib import Path


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
        for skill in data.get("skills", []):
            skill_path = skill.get("path")
            if not skill_path:
                print("  FAILED: Skill entry missing path")
                return False
            if not (plugin_root / skill_path).exists():
                print(f"  FAILED: Missing skill path {plugin_root / skill_path}")
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


def main():
    manifests = discover_manifests()
    results = [validate_manifest(manifest) for manifest in manifests]

    if manifests and all(results):
        print(f"\nAll {len(manifests)} manifests validated successfully.")
        return

    print(f"\nValidation failed. Found {len(manifests)} manifests.")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
