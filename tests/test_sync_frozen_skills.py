import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/sync_frozen_skills.py"
SPEC = importlib.util.spec_from_file_location("sync_frozen_skills", SCRIPT)
sync_module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = sync_module
SPEC.loader.exec_module(sync_module)


class SyncFrozenSkillsTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.repo = self.root / "repo"
        self.destination = self.root / "skills"
        self.plugin = self.repo / "plugins/frozen-skills"
        self._write_skill("alpha", "alpha v1")
        self._write_manifests(["alpha"])

    def tearDown(self):
        self.temporary.cleanup()

    def _write_skill(self, name, body):
        skill = self.plugin / "skills" / name
        skill.mkdir(parents=True, exist_ok=True)
        (skill / "SKILL.md").write_text(body, encoding="utf-8")

    def _write_manifests(self, names, *, divergent_cursor=False):
        manifest_paths = sync_module.MANIFEST_PATHS
        for relative in manifest_paths:
            names_for_manifest = ["different"] if divergent_cursor and "cursor" in str(relative) else names
            data = {
                "name": "frozen-skills",
                "version": "1.0.0",
                "description": "test",
                "skills": [
                    {"name": name, "path": f"skills/{name}"} for name in names_for_manifest
                ],
            }
            path = self.plugin / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(data), encoding="utf-8")

    def _sync(self, *, apply=False, prune=False, force=False):
        return sync_module.sync(
            self.repo,
            self.destination,
            apply=apply,
            prune=prune,
            force=force,
        )

    def test_fresh_install_then_check_is_current(self):
        planned = self._sync()
        self.assertEqual([action.kind for action in planned.actions], ["install"])

        applied = self._sync(apply=True)
        self.assertFalse(applied.conflicts)
        self.assertEqual(
            (self.destination / "alpha/SKILL.md").read_text(encoding="utf-8"),
            "alpha v1",
        )
        self.assertTrue((self.destination / sync_module.STATE_FILE).is_file())

        checked = self._sync()
        self.assertEqual([action.kind for action in checked.actions], ["current"])
        self.assertFalse(checked.changes)

    def test_managed_copy_updates_when_source_changes(self):
        self._sync(apply=True)
        self._write_skill("alpha", "alpha v2")

        planned = self._sync()
        self.assertEqual([action.kind for action in planned.actions], ["update"])
        self._sync(apply=True)
        self.assertEqual(
            (self.destination / "alpha/SKILL.md").read_text(encoding="utf-8"),
            "alpha v2",
        )

    def test_local_modification_is_a_conflict_unless_forced(self):
        self._sync(apply=True)
        (self.destination / "alpha/SKILL.md").write_text("local edit", encoding="utf-8")

        refused = self._sync(apply=True)
        self.assertEqual([action.kind for action in refused.actions], ["conflict"])
        self.assertEqual(
            (self.destination / "alpha/SKILL.md").read_text(encoding="utf-8"),
            "local edit",
        )

        forced = self._sync(apply=True, force=True)
        self.assertEqual([action.kind for action in forced.actions], ["update"])
        self.assertEqual(
            (self.destination / "alpha/SKILL.md").read_text(encoding="utf-8"),
            "alpha v1",
        )

    def test_unmanaged_matching_copy_is_adopted(self):
        self.destination.mkdir(parents=True)
        target = self.destination / "alpha"
        target.mkdir()
        (target / "SKILL.md").write_text("alpha v1", encoding="utf-8")

        result = self._sync(apply=True)
        self.assertEqual([action.kind for action in result.actions], ["adopt"])
        state = json.loads(
            (self.destination / sync_module.STATE_FILE).read_text(encoding="utf-8")
        )
        self.assertIn("alpha", state["skills"])

    def test_prune_only_removes_unchanged_managed_skills(self):
        self._write_skill("beta", "beta v1")
        self._write_manifests(["alpha", "beta"])
        self._sync(apply=True)

        self._write_manifests(["alpha"])
        without_prune = self._sync(apply=True)
        self.assertTrue((self.destination / "beta").is_dir())
        self.assertNotIn("remove", [action.kind for action in without_prune.actions])

        with_prune = self._sync(apply=True, prune=True)
        self.assertIn("remove", [action.kind for action in with_prune.actions])
        self.assertFalse((self.destination / "beta").exists())

    def test_manifest_divergence_is_rejected(self):
        self._write_skill("different", "different")
        self._write_manifests(["alpha"], divergent_cursor=True)
        with self.assertRaises(sync_module.SyncError):
            self._sync()

    def test_cli_exit_codes_distinguish_drift_current_and_conflict(self):
        common = [
            "--repo-root",
            str(self.repo),
            "--destination",
            str(self.destination),
        ]
        self.assertEqual(sync_module.main(["--check", *common]), 1)
        self.assertEqual(sync_module.main(["--apply", *common]), 0)
        self.assertEqual(sync_module.main(["--check", *common]), 0)

        (self.destination / "alpha/SKILL.md").write_text("local edit", encoding="utf-8")
        self.assertEqual(sync_module.main(["--check", *common]), 2)

    def test_unsafe_managed_skill_name_is_rejected(self):
        self.destination.mkdir(parents=True)
        state = {
            "schema": 1,
            "plugin": "frozen-skills",
            "skills": {"../outside": {"digest": "0" * 64}},
        }
        (self.destination / sync_module.STATE_FILE).write_text(
            json.dumps(state), encoding="utf-8"
        )
        with self.assertRaises(sync_module.SyncError):
            self._sync(prune=True)


if __name__ == "__main__":
    unittest.main()
