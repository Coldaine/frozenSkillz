import tempfile
import unittest
from pathlib import Path

from scripts.openai_validation import OpenAiMetadataError, validate_openai_metadata


class OpenAiMetadataTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.skill = Path(self.temporary.name) / "alpha"
        self.agents = self.skill / "agents"
        self.agents.mkdir(parents=True)

    def tearDown(self):
        self.temporary.cleanup()

    def _write_metadata(self, short_description, *, extra="", prompt=None):
        default_prompt = prompt or "Use $alpha for a test."
        (self.agents / "openai.yaml").write_text(
            "interface:\n"
            '  display_name: "Alpha"\n'
            f'  short_description: "{short_description}"\n'
            f'  default_prompt: "{default_prompt}"\n'
            f"{extra}",
            encoding="utf-8",
        )

    def test_absent_metadata_is_optional(self):
        validate_openai_metadata(self.skill, "alpha")

    def test_description_boundaries_are_valid(self):
        for length in (25, 64):
            with self.subTest(length=length):
                self._write_metadata("x" * length)
                validate_openai_metadata(self.skill, "alpha")

    def test_description_outside_boundaries_is_rejected(self):
        for length in (24, 65):
            with self.subTest(length=length):
                self._write_metadata("x" * length)
                with self.assertRaisesRegex(OpenAiMetadataError, "25-64"):
                    validate_openai_metadata(self.skill, "alpha")

    def test_default_prompt_must_name_the_skill(self):
        self._write_metadata("A valid short description", prompt="Run the test.")

        with self.assertRaisesRegex(OpenAiMetadataError, "must mention \\$alpha"):
            validate_openai_metadata(self.skill, "alpha")

    def test_missing_icon_is_rejected(self):
        self._write_metadata(
            "A valid short description",
            extra='  icon_small: "./assets/missing.png"\n',
        )

        with self.assertRaisesRegex(OpenAiMetadataError, "does not resolve"):
            validate_openai_metadata(self.skill, "alpha")

    def test_dependency_tools_must_be_mappings(self):
        self._write_metadata(
            "A valid short description",
            extra="dependencies:\n  tools:\n    - 42\n",
        )

        with self.assertRaisesRegex(OpenAiMetadataError, "must be a mapping"):
            validate_openai_metadata(self.skill, "alpha")


if __name__ == "__main__":
    unittest.main()
