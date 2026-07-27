import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "codex-thread-organizer"
SKILL_ROOT = ROOT / "_incubator" / "frozen-skills" / "skills" / SKILL_NAME


class CodexThreadOrganizerPackagingTests(unittest.TestCase):
    def test_skill_is_gated_codex_only_and_not_auto_installed(self):
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
        self.assertIn("manual install", tracker_text.lower())

        manifests = [
            ROOT / "plugins" / "frozen-skills" / ".claude-plugin" / "plugin.json",
            ROOT / "plugins" / "frozen-skills" / ".codex-plugin" / "plugin.json",
            ROOT / "plugins" / "frozen-skills" / ".cursor-plugin" / "plugin.json",
            ROOT / "plugins" / "frozen-skills" / "gemini-extension.json",
        ]
        for manifest in manifests:
            data = json.loads(manifest.read_text(encoding="utf-8"))
            active_names = {entry["name"] for entry in data["skills"]}
            active_paths = {entry["path"] for entry in data["skills"]}
            self.assertNotIn(SKILL_NAME, active_names, manifest.as_posix())
            self.assertNotIn(f"skills/{SKILL_NAME}", active_paths, manifest.as_posix())

        synchronizer = (ROOT / "scripts" / "sync_frozen_skills.py").read_text(
            encoding="utf-8"
        )
        self.assertNotIn(SKILL_NAME, synchronizer)


if __name__ == "__main__":
    unittest.main()
