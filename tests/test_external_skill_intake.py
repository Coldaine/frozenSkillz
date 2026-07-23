import json
import re
import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "plugins" / "frozen-skills" / "skills" / "external-skill-intake"


class ExternalSkillIntakeContractTests(unittest.TestCase):
    def test_manifest_listed_skills_have_discovery_frontmatter(self):
        manifest_path = (
            REPO_ROOT / "plugins" / "frozen-skills" / ".codex-plugin" / "plugin.json"
        )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        plugin_root = manifest_path.parents[1]

        for entry in manifest["skills"]:
            skill_file = plugin_root / entry["path"] / "SKILL.md"
            skill = skill_file.read_text(encoding="utf-8")
            self.assertTrue(skill.startswith("---\n"), skill_file)
            frontmatter = skill.split("---", 2)[1]
            self.assertRegex(frontmatter, rf"(?m)^name: {re.escape(entry['name'])}$")
            self.assertRegex(frontmatter, r"(?m)^description: (?:.+|>-)$")

    def test_active_skill_is_discoverable_and_portable(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertTrue(skill.startswith("---\n"))
        frontmatter = skill.split("---", 2)[1]
        self.assertRegex(frontmatter, r"(?m)^name: external-skill-intake$")
        self.assertRegex(frontmatter, r"(?m)^description: .+$")
        self.assertNotIn("docs/workflows/", skill)

        bundled_links = re.findall(r"`((?:references|templates)/[^`]+)`", skill)
        self.assertTrue(bundled_links)
        for relative_path in bundled_links:
            self.assertTrue((SKILL_ROOT / relative_path).is_file(), relative_path)

    def test_superpowers_snapshot_includes_archive_excluded_files(self):
        source_root = (
            REPO_ROOT / "_incubator" / "scout" / "2026-07-23-obra-superpowers" / "source"
        )
        source_files = [path for path in source_root.rglob("*") if path.is_file()]

        self.assertEqual(172, len(source_files))
        self.assertTrue((source_root / ".opencode" / "INSTALL.md").is_file())
        self.assertTrue(
            (source_root / ".opencode" / "plugins" / "superpowers.js").is_file()
        )

    def test_superpowers_snapshot_matches_persisted_git_tree(self):
        scout_root = REPO_ROOT / "_incubator" / "scout" / "2026-07-23-obra-superpowers"
        prefix = "_incubator/scout/2026-07-23-obra-superpowers/source/"
        expected = {}
        for line in (scout_root / "source-tree.tsv").read_text(encoding="utf-8").splitlines():
            if not line or line.startswith("#"):
                continue
            mode_blob, path = line.split("\t", 1)
            expected[path] = mode_blob

        result = subprocess.run(
            ["git", "ls-files", "--stage", "--", prefix],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        actual = {}
        for line in result.stdout.splitlines():
            mode, blob, _stage_and_path = line.split(maxsplit=2)
            full_path = _stage_and_path.split("\t", 1)[1]
            actual[full_path.removeprefix(prefix)] = f"{mode} {blob}"

        self.assertEqual(172, len(expected))
        self.assertEqual(expected, actual)

    def test_completed_forensic_records_use_canonical_statuses(self):
        forensic_root = (
            REPO_ROOT
            / "_incubator"
            / "scout"
            / "2026-07-23-obra-superpowers"
            / "evals"
            / "forensic"
        )
        record_paths = sorted(forensic_root.glob("*-real-agent-evidence.md"))
        allowed = {"current", "fixed", "historical", "unresolved", "unclear"}

        self.assertEqual(
            {
                "2026-07-23-brainstorming-real-agent-evidence.md",
                "2026-07-23-dispatching-parallel-agents-real-agent-evidence.md",
            },
            {path.name for path in record_paths},
        )
        for record_path in record_paths:
            record = record_path.read_text(encoding="utf-8")
            self.assertIn(
                "| Source | Type | Captured | Version or revision | Harness, model, and OS | Status | Result |",
                record,
            )
            evidence_rows = [line for line in record.splitlines() if line.startswith("| [")]
            self.assertTrue(evidence_rows, record_path)
            for row in evidence_rows:
                columns = [column.strip() for column in row.strip("|").split("|")]
                self.assertEqual(7, len(columns), row)
                self.assertRegex(columns[2], r"^\d{4}-\d{2}-\d{2}$")
                self.assertTrue(columns[3], row)
                self.assertTrue(columns[4], row)
                self.assertIn(columns[5], allowed)

            aggregate_status = re.search(r"(?m)^- Status: ([a-z]+)[.;]", record)
            self.assertIsNotNone(aggregate_status, record_path)
            self.assertIn(aggregate_status.group(1), allowed)

        design = (
            REPO_ROOT
            / "docs"
            / "superpowers"
            / "specs"
            / "2026-07-23-live-or-forensic-evaluations-design.md"
        ).read_text(encoding="utf-8")
        template = (SKILL_ROOT / "templates" / "forensic-evaluation.md").read_text(
            encoding="utf-8"
        )
        canonical_list = "`current`, `fixed`, `historical`, `unresolved`, or `unclear`"
        self.assertIn(canonical_list, design)
        self.assertIn("| Status | Observed behavior", template)
        for status in allowed:
            self.assertIn(status, template)

    def test_supports_live_or_forensic_evaluations(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        workflow = (REPO_ROOT / "docs" / "workflows" / "external-skill-intake.md").read_text(
            encoding="utf-8"
        )
        protocol = (SKILL_ROOT / "references" / "evaluation-protocol.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("live or forensic evaluations", skill)
        self.assertIn("## Live or Forensic Evaluations", workflow)
        self.assertTrue((SKILL_ROOT / "references" / "evaluation-protocol.md").is_file())
        self.assertTrue((SKILL_ROOT / "templates" / "forensic-evaluation.md").is_file())
        self.assertIn("Baseline: agent output without candidate material", protocol)
        self.assertIn("user task prompt", protocol)
        self.assertIn("Comparative improvement claims require live comparative evidence", protocol)


if __name__ == "__main__":
    unittest.main()
