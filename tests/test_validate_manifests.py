import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/validate_manifests.py"
SPEC = importlib.util.spec_from_file_location("validate_manifests", SCRIPT)
validate_module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = validate_module
SPEC.loader.exec_module(validate_module)


class ValidateManifestsTests(unittest.TestCase):
    def test_contract_reports_missing_or_invalid_json_without_traceback(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            manifests = {}
            for consumer in validate_module.FROZEN_CONSUMER_MANIFESTS:
                manifest = root / f"{consumer}.json"
                manifest.write_text(
                    json.dumps(
                        {
                            "name": "frozen-skills",
                            "version": "1.0.0",
                            "description": "test",
                            "skills": [],
                        }
                    ),
                    encoding="utf-8",
                )
                manifests[consumer] = manifest

            invalid = root / "invalid.json"
            invalid.write_text("{", encoding="utf-8")
            for broken_distribution in (root / "missing.json", invalid):
                with self.subTest(distribution=broken_distribution.name):
                    output = io.StringIO()
                    with (
                        mock.patch.object(
                            validate_module,
                            "FROZEN_CONSUMER_MANIFESTS",
                            manifests,
                        ),
                        mock.patch.object(
                            validate_module,
                            "FROZEN_DISTRIBUTION",
                            broken_distribution,
                        ),
                        redirect_stdout(output),
                    ):
                        self.assertFalse(
                            validate_module.validate_frozen_consumer_contract()
                        )
                    self.assertIn("FAILED", output.getvalue())

    def test_contract_rejects_the_shared_package_in_a_consumer_lane(self):
        distribution = validate_module.load_json(
            validate_module.FROZEN_DISTRIBUTION
        )
        distribution["consumer_packages"]["codex"] = ["frozen-skills"]
        real_load_json = validate_module.load_json

        def load_with_invalid_distribution(path):
            if path == validate_module.FROZEN_DISTRIBUTION:
                return distribution
            return real_load_json(path)

        output = io.StringIO()
        with (
            mock.patch.object(
                validate_module,
                "load_json",
                side_effect=load_with_invalid_distribution,
            ),
            redirect_stdout(output),
        ):
            self.assertFalse(validate_module.validate_frozen_consumer_contract())
        self.assertIn("reserved for shared skills", output.getvalue())


class SkillMetadataValidationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
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

    def validate(self):
        with redirect_stdout(io.StringIO()) as output:
            result = validate_module.validate_manifest(self.manifest)
        return result, output.getvalue()

    def test_valid_skill_metadata_passes(self):
        (self.skill / "SKILL.md").write_text(
            "---\nname: alpha\ndescription: Test skill.\n---\n\n# Alpha\n",
            encoding="utf-8",
        )

        result, _ = self.validate()
        self.assertTrue(result)

    def test_folded_block_scalar_description_passes(self):
        (self.skill / "SKILL.md").write_text(
            "---\n"
            "name: alpha\n"
            "description: >-\n"
            "  Use when testing folded block scalars\n"
            "  across multiple frontmatter lines.\n"
            "---\n\n# Alpha\n",
            encoding="utf-8",
        )

        result, _ = self.validate()
        self.assertTrue(result)

    def test_missing_frontmatter_fails_manifest_validation(self):
        (self.skill / "SKILL.md").write_text("# Alpha\n", encoding="utf-8")

        result, output = self.validate()
        self.assertFalse(result)
        self.assertIn("missing YAML frontmatter", output)

    def test_frontmatter_name_must_match_manifest_name(self):
        (self.skill / "SKILL.md").write_text(
            "---\nname: beta\ndescription: Test skill.\n---\n",
            encoding="utf-8",
        )

        result, output = self.validate()
        self.assertFalse(result)
        self.assertIn("does not match manifest name", output)

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

        result, output = self.validate()
        self.assertFalse(result)
        self.assertIn("same-name directory", output)

    def test_missing_bundled_reference_fails(self):
        (self.skill / "SKILL.md").write_text(
            "---\nname: alpha\ndescription: Test skill.\n---\n\n"
            "Read `references/missing.md` first.\n",
            encoding="utf-8",
        )

        result, output = self.validate()
        self.assertFalse(result)
        self.assertIn("does not exist", output)

    def test_skill_root_string_validates_discovered_skill_metadata(self):
        data = json.loads(self.manifest.read_text(encoding="utf-8"))
        data["skills"] = "./skills/"
        self.manifest.write_text(json.dumps(data), encoding="utf-8")
        (self.skill / "SKILL.md").write_text("# Alpha\n", encoding="utf-8")

        result, output = self.validate()
        self.assertFalse(result)
        self.assertIn("missing YAML frontmatter", output)


if __name__ == "__main__":
    unittest.main()
