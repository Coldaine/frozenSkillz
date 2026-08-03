import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/sync_codex_global_config.py"
SPEC = importlib.util.spec_from_file_location("sync_codex_global_config", SCRIPT)
sync_module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(sync_module)


class SyncCodexGlobalConfigTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "source"
        (self.source / "agents").mkdir(parents=True)
        self.fragment = "## Required\n\nAlways delegate browser work.\n"
        (self.source / "AGENTS.browser-delegation.md").write_text(
            self.fragment, encoding="utf-8"
        )
        (self.source / "agents/chrome-pilot.toml").write_text(
            'name = "chrome_pilot"\n', encoding="utf-8"
        )
        self.codex_home = self.root / ".codex"
        self.codex_home.mkdir()

    def test_apply_preserves_unmanaged_prompt_content(self):
        target = self.codex_home / "AGENTS.md"
        target.write_text("# Existing policy\n", encoding="utf-8")

        clean, changes = sync_module.synchronize(
            self.source, self.codex_home, apply=True
        )

        self.assertFalse(clean)
        self.assertEqual(2, len(changes))
        result = target.read_text(encoding="utf-8")
        self.assertIn("# Existing policy", result)
        self.assertIn(sync_module.START_MARKER, result)
        self.assertIn(self.fragment.strip(), result)
        self.assertTrue((self.codex_home / "agents/chrome-pilot.toml").is_file())

    def test_apply_adopts_matching_unmarked_fragment_without_duplication(self):
        target = self.codex_home / "AGENTS.md"
        target.write_text(f"# Existing\n\n{self.fragment}", encoding="utf-8")

        sync_module.synchronize(self.source, self.codex_home, apply=True)

        result = target.read_text(encoding="utf-8")
        self.assertEqual(1, result.count("Always delegate browser work."))
        self.assertEqual(1, result.count(sync_module.START_MARKER))

    def test_apply_updates_only_managed_block(self):
        target = self.codex_home / "AGENTS.md"
        target.write_text(
            "before\n"
            f"{sync_module.START_MARKER}\nold\n{sync_module.END_MARKER}\n"
            "after\n",
            encoding="utf-8",
        )

        sync_module.synchronize(self.source, self.codex_home, apply=True)

        result = target.read_text(encoding="utf-8")
        self.assertEqual(
            "before\n"
            f"{sync_module.START_MARKER}\n{self.fragment.strip()}\n"
            f"{sync_module.END_MARKER}\n"
            "after\n",
            result,
        )

    def test_check_reports_drift_without_writing(self):
        target = self.codex_home / "AGENTS.md"
        target.write_text("unchanged\n", encoding="utf-8")

        clean, changes = sync_module.synchronize(
            self.source, self.codex_home, apply=False
        )

        self.assertFalse(clean)
        self.assertEqual(2, len(changes))
        self.assertEqual("unchanged\n", target.read_text(encoding="utf-8"))

    def test_malformed_markers_fail_hard(self):
        (self.codex_home / "AGENTS.md").write_text(
            f"{sync_module.START_MARKER}\n", encoding="utf-8"
        )

        with self.assertRaises(sync_module.ConfigError):
            sync_module.synchronize(self.source, self.codex_home, apply=True)


if __name__ == "__main__":
    unittest.main()
