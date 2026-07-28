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


if __name__ == "__main__":
    unittest.main()
