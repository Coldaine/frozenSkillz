import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_skills import SkillDiscoveryError, discover_skill_paths


class ValidateSkillsDiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary.name)
        self.plugin = self.repo / "plugins/example"
        self.skill = self.plugin / "skills/alpha"
        self.skill.mkdir(parents=True)
        self.manifest = self.plugin / ".codex-plugin/plugin.json"
        self.manifest.parent.mkdir()
        self._write_manifest({"name": "alpha", "path": "skills/alpha"})

    def tearDown(self):
        self.temporary.cleanup()

    def _write_manifest(self, entry):
        self.manifest.write_text(
            json.dumps(
                {
                    "name": "example",
                    "version": "1.0.0",
                    "description": "test",
                    "skills": [entry],
                }
            ),
            encoding="utf-8",
        )

    def test_valid_contained_same_name_path_is_discovered(self):
        result = discover_skill_paths(self.repo)

        self.assertEqual(result, {self.skill.resolve(): "alpha"})

    def test_escaping_path_is_rejected(self):
        self._write_manifest({"name": "outside", "path": "../outside"})

        with self.assertRaisesRegex(SkillDiscoveryError, "escapes plugin root"):
            discover_skill_paths(self.repo)

    def test_malformed_entry_is_rejected(self):
        self._write_manifest({"name": "alpha"})

        with self.assertRaisesRegex(SkillDiscoveryError, "has no path"):
            discover_skill_paths(self.repo)

    def test_manifest_must_contain_an_object(self):
        self.manifest.write_text("[]", encoding="utf-8")

        with self.assertRaisesRegex(SkillDiscoveryError, "must contain an object"):
            discover_skill_paths(self.repo)

    def test_directory_name_must_match_manifest_name(self):
        self._write_manifest({"name": "beta", "path": "skills/alpha"})

        with self.assertRaisesRegex(SkillDiscoveryError, "does not match"):
            discover_skill_paths(self.repo)

    def test_missing_plugins_directory_is_rejected(self):
        empty_repo = self.repo / "empty"
        empty_repo.mkdir()

        with self.assertRaisesRegex(SkillDiscoveryError, "Plugins directory is missing"):
            discover_skill_paths(empty_repo)


if __name__ == "__main__":
    unittest.main()
