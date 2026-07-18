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

def main() -> None:
    """Validate plugin allowlists rather than gated or scout snapshots."""

    skill_paths: dict[Path, str] = {}
    for plugin_root in sorted(Path("plugins").iterdir()):
        if not plugin_root.is_dir():
            continue
        manifests = (
            plugin_root / ".claude-plugin/plugin.json",
            plugin_root / ".codex-plugin/plugin.json",
            plugin_root / ".cursor-plugin/plugin.json",
            plugin_root / "gemini-extension.json",
        )
        for manifest in manifests:
            if not manifest.is_file():
                continue
            data = json.loads(manifest.read_text(encoding="utf-8"))
            for entry in data.get("skills", []):
                skill_path = (plugin_root / entry["path"]).resolve()
                previous_name = skill_paths.setdefault(skill_path, entry["name"])
                if previous_name != entry["name"]:
                    raise SystemExit(
                        f"Manifest names disagree for {skill_path}: "
                        f"{previous_name!r} and {entry['name']!r}"
                    )

    failures = 0
    for skill_path, skill_name in sorted(
        skill_paths.items(), key=lambda item: item[0].as_posix()
    ):
        problems = validate(skill_path)
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
