import json
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "codex-thread-organizer"
SHARED_PLUGIN_ROOT = ROOT / "plugins" / "frozen-skills"
ORGANIZER_PLUGIN_ROOT = ROOT / "plugins" / "codex-thread-organizer"
SKILL_ROOT = ORGANIZER_PLUGIN_ROOT / "skills" / SKILL_NAME
SYNC_SCRIPT = ROOT / "scripts" / "sync_frozen_skills.py"
SYNC_SPEC = importlib.util.spec_from_file_location("organizer_sync", SYNC_SCRIPT)
sync_module = importlib.util.module_from_spec(SYNC_SPEC)
assert SYNC_SPEC.loader is not None
sys.modules[SYNC_SPEC.name] = sync_module
SYNC_SPEC.loader.exec_module(sync_module)


class CodexThreadOrganizerPackagingTests(unittest.TestCase):
    def test_skill_is_active_for_codex_only(self):
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        openai_metadata = (SKILL_ROOT / "agents" / "openai.yaml").read_text(
            encoding="utf-8"
        )
        tracker_text = (ROOT / "docs" / "skill-review" / "tracker.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("Codex-only", skill_text)
        self.assertIn("$codex-thread-organizer", openai_metadata)
        self.assertIn("Codex-only", tracker_text)

        manifests = {
            "claude": ROOT / "plugins" / "frozen-skills" / ".claude-plugin" / "plugin.json",
            "codex": ROOT / "plugins" / "frozen-skills" / ".codex-plugin" / "plugin.json",
            "cursor": ROOT / "plugins" / "frozen-skills" / ".cursor-plugin" / "plugin.json",
            "gemini": ROOT / "plugins" / "frozen-skills" / "gemini-extension.json",
        }
        for consumer, manifest in manifests.items():
            data = json.loads(manifest.read_text(encoding="utf-8"))
            active_names = {entry["name"] for entry in data.get("skills", [])}
            self.assertNotIn(SKILL_NAME, active_names, manifest.as_posix())

        self.assertFalse(
            (ROOT / "_incubator" / "frozen-skills" / "skills" / SKILL_NAME).exists()
        )
        self.assertFalse((SHARED_PLUGIN_ROOT / "skills" / SKILL_NAME).exists())

        organizer_plugin = json.loads(
            (ORGANIZER_PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(organizer_plugin["name"], SKILL_NAME)
        self.assertEqual(organizer_plugin["skills"], "./skills/")

        distribution = json.loads(
            (ROOT / "plugins" / "distribution.json").read_text(encoding="utf-8")
        )
        shared_names = {entry["name"] for entry in distribution["shared"]}
        self.assertNotIn(SKILL_NAME, shared_names)
        for consumer, entries in distribution["consumers"].items():
            names = {entry["name"] for entry in entries}
            assertion = self.assertIn if consumer == "codex" else self.assertNotIn
            assertion(SKILL_NAME, names, consumer)

        selected = {}
        for consumer in manifests:
            _plugin_root, _version, sources = sync_module.load_distribution(
                ROOT, consumer
            )
            selected[consumer] = {source.name for source in sources}

        self.assertIn(SKILL_NAME, selected["codex"])
        for consumer in ("claude", "cursor", "gemini"):
            self.assertNotIn(SKILL_NAME, selected[consumer])

    def test_real_distribution_smoke_installs_organizer_only_for_codex(self):
        shared = {
            "doppler",
            "external-skill-intake",
            "omc-reference",
            "pdm-cli-operations",
        }
        with tempfile.TemporaryDirectory() as temporary:
            smoke_root = Path(temporary)
            for consumer in ("claude", "codex", "cursor", "gemini"):
                destination = smoke_root / consumer
                applied = sync_module.sync(
                    ROOT,
                    destination,
                    consumer=consumer,
                    apply=True,
                    prune=False,
                    force=False,
                )
                self.assertFalse(applied.conflicts, consumer)

                checked = sync_module.sync(
                    ROOT,
                    destination,
                    consumer=consumer,
                    apply=False,
                    prune=False,
                    force=False,
                )
                self.assertFalse(checked.changes, consumer)
                installed = {
                    path.name
                    for path in destination.iterdir()
                    if (path / "SKILL.md").is_file()
                }
                expected = shared | ({SKILL_NAME} if consumer == "codex" else set())
                self.assertEqual(installed, expected, consumer)

                state = json.loads(
                    (destination / sync_module.STATE_FILE).read_text(encoding="utf-8")
                )
                self.assertEqual(state["consumer"], consumer)


if __name__ == "__main__":
    unittest.main()
