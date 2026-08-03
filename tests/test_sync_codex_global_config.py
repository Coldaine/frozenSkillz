import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/sync_codex_global_config.py"
SPEC = importlib.util.spec_from_file_location("sync_codex_global_config", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Cannot load synchronization module from {SCRIPT}")
sync_module = importlib.util.module_from_spec(SPEC)
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
            'name = "chrome_pilot"\n'
            'description = "Browser worker"\n'
            'developer_instructions = "Use Chrome."\n',
            encoding="utf-8",
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

    def test_rollback_rejects_a_non_current_transaction(self):
        _changes, first = self._apply()
        self.assertIsNotNone(first)
        (self.source / "AGENTS.browser-delegation.md").write_text(
            "## Required\n\nUpdated reviewed rule.\n", encoding="utf-8"
        )
        _changes, second = self._apply()
        self.assertIsNotNone(second)

        with self.assertRaises(sync_module.ConfigError):
            sync_module.rollback(self.codex_home, first)

    def test_rollback_rejects_unrelated_post_apply_edit(self):
        target = self.codex_home / "AGENTS.md"
        target.write_text("original\n", encoding="utf-8")
        _changes, transaction = self._apply()
        target.write_text(target.read_text(encoding="utf-8") + "later\n", encoding="utf-8")

        with self.assertRaises(sync_module.ConfigError):
            sync_module.rollback(self.codex_home, transaction)

        self.assertIn("later", target.read_text(encoding="utf-8"))

    def test_matching_files_without_state_are_not_current(self):
        self._apply()
        state_path = self.codex_home / sync_module.MANAGEMENT_ROOT / sync_module.STATE_FILE
        state_path.unlink()

        self.assertEqual(
            1,
            sync_module.main(
                ["--check", "--source", str(self.source), "--codex-home", str(self.codex_home)]
            ),
        )

    def test_invalid_agent_toml_fails_hard(self):
        (self.source / "agents/chrome-pilot.toml").write_text("name = [\n", encoding="utf-8")
        with self.assertRaises(sync_module.ConfigError):
            sync_module.plan(self.source, self.codex_home)

    def test_agent_toml_requires_codex_agent_fields(self):
        (self.source / "agents/chrome-pilot.toml").write_text(
            'name = "chrome_pilot"\n', encoding="utf-8"
        )
        with self.assertRaises(sync_module.ConfigError):
            sync_module.plan(self.source, self.codex_home)

    def test_malformed_markers_fail_hard(self):
        (self.codex_home / "AGENTS.md").write_text(
            f"{sync_module.START_MARKER}\n", encoding="utf-8"
        )

        with self.assertRaises(sync_module.ConfigError):
            sync_module.plan(self.source, self.codex_home)

    def test_reversed_markers_fail_with_config_error(self):
        (self.codex_home / "AGENTS.md").write_text(
            f"{sync_module.END_MARKER}\n{sync_module.START_MARKER}\n",
            encoding="utf-8",
        )

        with self.assertRaises(sync_module.ConfigError):
            sync_module.plan(self.source, self.codex_home)

    def test_symlinked_agents_file_is_rejected(self):
        real = self.root / "real-agents.md"
        real.write_text("outside\n", encoding="utf-8")
        target = self.codex_home / "AGENTS.md"
        try:
            target.symlink_to(real)
        except OSError:
            self.skipTest("symlink creation is unavailable")

        with self.assertRaises(sync_module.ConfigError):
            sync_module.plan(self.source, self.codex_home)

    def test_symlinked_agents_directory_is_rejected(self):
        real = self.root / "outside-agents"
        real.mkdir()
        target = self.codex_home / "agents"
        try:
            target.symlink_to(real, target_is_directory=True)
        except OSError:
            self.skipTest("symlink creation is unavailable")

        with self.assertRaises(sync_module.ConfigError):
            sync_module.plan(self.source, self.codex_home)

    def test_failed_second_target_rolls_back_first_target(self):
        agents_target = self.codex_home / "AGENTS.md"
        agents_target.write_text("original\n", encoding="utf-8")
        changes, conflicts, state = sync_module.plan(self.source, self.codex_home)
        self.assertEqual([], conflicts)
        real_atomic_write = sync_module._atomic_write
        agent_target = self.codex_home / "agents/chrome-pilot.toml"

        def fail_agent_write(path, content):
            if path == agent_target:
                raise OSError("simulated agent write failure")
            return real_atomic_write(path, content)

        with (
            mock.patch.object(sync_module, "_atomic_write", side_effect=fail_agent_write),
            self.assertRaises(sync_module.ConfigError),
        ):
            sync_module.apply_changes(self.codex_home, changes, state)

        self.assertEqual("original\n", agents_target.read_text(encoding="utf-8"))
        self.assertFalse(agent_target.exists())


if __name__ == "__main__":
    unittest.main()
