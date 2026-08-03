import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/sync_codex_global_config.py"
SPEC = importlib.util.spec_from_file_location("sync_codex_global_config", SCRIPT)
sync_module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = sync_module
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

    def _apply(self):
        changes, conflicts, state = sync_module.plan(self.source, self.codex_home)
        self.assertEqual([], conflicts)
        transaction = sync_module.apply_changes(self.codex_home, changes, state)
        return changes, transaction

    def test_apply_preserves_unmanaged_prompt_content_and_records_state(self):
        target = self.codex_home / "AGENTS.md"
        target.write_text("# Existing policy\n", encoding="utf-8")

        changes, transaction = self._apply()

        self.assertEqual(2, len(changes))
        self.assertIsNotNone(transaction)
        result = target.read_text(encoding="utf-8")
        self.assertIn("# Existing policy", result)
        self.assertIn(sync_module.START_MARKER, result)
        state = sync_module._load_state(self.codex_home)
        self.assertIn("AGENTS.md#browser-delegation", state["managed"])

    def test_apply_adopts_matching_unmarked_fragment_without_duplication(self):
        target = self.codex_home / "AGENTS.md"
        target.write_text(f"# Existing\n\n{self.fragment}", encoding="utf-8")

        self._apply()

        result = target.read_text(encoding="utf-8")
        self.assertEqual(1, result.count("Always delegate browser work."))
        self.assertEqual(1, result.count(sync_module.START_MARKER))

    def test_locally_modified_managed_block_is_a_conflict(self):
        self._apply()
        target = self.codex_home / "AGENTS.md"
        target.write_text(
            target.read_text(encoding="utf-8").replace(
                "Always delegate browser work.", "locally changed"
            ),
            encoding="utf-8",
        )
        self.fragment = "## Required\n\nUpdated reviewed rule.\n"
        (self.source / "AGENTS.browser-delegation.md").write_text(
            self.fragment, encoding="utf-8"
        )

        _changes, conflicts, _state = sync_module.plan(self.source, self.codex_home)

        self.assertEqual(
            ["managed browser-delegation block was modified locally"], conflicts
        )

    def test_unmanaged_different_agent_file_is_a_conflict(self):
        target = self.codex_home / "agents/chrome-pilot.toml"
        target.parent.mkdir()
        target.write_text('name = "somebody_elses_agent"\n', encoding="utf-8")

        _changes, conflicts, _state = sync_module.plan(self.source, self.codex_home)

        self.assertEqual(1, len(conflicts))
        self.assertIn("unmanaged or locally modified agent file", conflicts[0])

    def test_check_plan_does_not_write(self):
        target = self.codex_home / "AGENTS.md"
        target.write_text("unchanged\n", encoding="utf-8")

        changes, conflicts, _state = sync_module.plan(self.source, self.codex_home)

        self.assertEqual([], conflicts)
        self.assertEqual(2, len(changes))
        self.assertEqual("unchanged\n", target.read_text(encoding="utf-8"))

    def test_rollback_restores_shared_file_and_removes_created_agent(self):
        target = self.codex_home / "AGENTS.md"
        target.write_text("original\n", encoding="utf-8")
        _changes, transaction = self._apply()
        self.assertIsNotNone(transaction)

        sync_module.rollback(self.codex_home, transaction)

        self.assertEqual("original\n", target.read_text(encoding="utf-8"))
        self.assertFalse((self.codex_home / "agents/chrome-pilot.toml").exists())
        self.assertFalse(
            (self.codex_home / sync_module.MANAGEMENT_ROOT / sync_module.STATE_FILE).exists()
        )

    def test_malformed_markers_fail_hard(self):
        (self.codex_home / "AGENTS.md").write_text(
            f"{sync_module.START_MARKER}\n", encoding="utf-8"
        )

        with self.assertRaises(sync_module.ConfigError):
            sync_module.plan(self.source, self.codex_home)


if __name__ == "__main__":
    unittest.main()
