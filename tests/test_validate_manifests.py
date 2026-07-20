import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/validate_manifests.py"
SPEC = importlib.util.spec_from_file_location("validate_manifests", SCRIPT)
validate_module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validate_module)


class ValidateManifestsTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.plugin = Path(self.temporary.name) / "plugin"
        self.skill = self.plugin / "skills/alpha"
        self.skill.mkdir(parents=True)
        self.manifest = self.plugin / ".codex-plugin/plugin.json"
        self.manifest.parent.mkdir()
        self.manifest.write_text(
            json.dumps(
                {
                    "name": "frozen-skills",
                    "version": "1.0.0",
                    "description": "test",
                    "skills": [{"name": "alpha", "path": "skills/alpha"}],
                }
            ),
            encoding="utf-8",
        )

    def tearDown(self):
        self.temporary.cleanup()

    def test_valid_skill_metadata_passes(self):
        (self.skill / "SKILL.md").write_text(
            "---\nname: alpha\ndescription: Test skill.\n---\n\n# Alpha\n",
            encoding="utf-8",
        )

        self.assertTrue(validate_module.validate_manifest(self.manifest))

    def test_missing_frontmatter_fails_manifest_validation(self):
        (self.skill / "SKILL.md").write_text("# Alpha\n", encoding="utf-8")

        self.assertFalse(validate_module.validate_manifest(self.manifest))

    def test_directory_name_must_match_manifest_name(self):
        other_skill = self.plugin / "skills/beta"
        other_skill.mkdir()
        (other_skill / "SKILL.md").write_text(
            "---\nname: alpha\ndescription: Test skill.\n---\n",
            encoding="utf-8",
        )
        data = json.loads(self.manifest.read_text(encoding="utf-8"))
        data["skills"][0]["path"] = "skills/beta"
        self.manifest.write_text(json.dumps(data), encoding="utf-8")

        self.assertFalse(validate_module.validate_manifest(self.manifest))


if __name__ == "__main__":
    unittest.main()
