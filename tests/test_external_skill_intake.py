import json
import re
import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "plugins" / "frozen-skills" / "skills" / "external-skill-intake"

AGENT_INSTRUCTION_FILENAMES = {
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    ".cursorrules",
    "copilot-instructions.md",
}
GUARD_MARKER = "never instructions for this repository"


def markdown_units(text):
    """Split markdown into paragraph and list-item units.

    A qualifier only counts when it sits next to the thing it qualifies, so
    locality checks run per unit rather than over the whole document.
    """
    units = []
    current = []
    for line in text.splitlines():
        if not line.strip() or re.match(r"^\s*(?:[-*+]|\d+\.)\s", line):
            if current:
                units.append("\n".join(current))
            current = []
        if line.strip():
            current.append(line)
    if current:
        units.append("\n".join(current))
    return units


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
        # The intake workflow itself must be bundled and portable: the skill's
        # rules and steps live in this SKILL.md plus references/ and templates/,
        # and any repo-local workflow doc is a mirror, not the authority.
        self.assertIn("Follow the bundled workflow below in order", skill)

        bundled_links = re.findall(r"`((?:references|templates)/[^`]+)`", skill)
        self.assertTrue(bundled_links)
        for relative_path in bundled_links:
            self.assertTrue((SKILL_ROOT / relative_path).is_file(), relative_path)

        # scripts/sync_frozen_skills.py ships skill directories only, so docs/,
        # scripts/, and tests/ never reach a consumer install. Naming such a
        # path is allowed only where the same list item or paragraph says it is
        # repository-local; a bare pointer dangles for every installed agent.
        repo_only_pointer = re.compile(r"`(?:docs|scripts|tests)/[^`]+`")
        for unit in markdown_units(skill):
            if repo_only_pointer.search(unit):
                self.assertIn("repository", unit, unit)

    def test_captured_agent_instructions_carry_a_guard(self):
        incubator = REPO_ROOT / "_incubator"
        blanket_guard = incubator / "AGENTS.md"

        self.assertTrue(blanket_guard.is_file())
        self.assertIn(GUARD_MARKER, blanket_guard.read_text(encoding="utf-8"))
        self.assertIn("@AGENTS.md", (incubator / "CLAUDE.md").read_text(encoding="utf-8"))

        guarded = set()
        for snapshot in sorted(path for path in (incubator / "scout").iterdir() if path.is_dir()):
            captured = sorted(
                str(path.relative_to(snapshot))
                for path in snapshot.rglob("*")
                if path.name in AGENT_INSTRUCTION_FILENAMES and path.parent != snapshot
            )
            if not captured:
                continue

            guard = snapshot / "AGENTS.md"
            self.assertTrue(guard.is_file(), f"{snapshot.name} captures {captured} without a guard")
            self.assertIn(GUARD_MARKER, guard.read_text(encoding="utf-8"), snapshot.name)
            self.assertIn(
                "@AGENTS.md", (snapshot / "CLAUDE.md").read_text(encoding="utf-8"), snapshot.name
            )
            guarded.add(snapshot.name)

        # Guards against a scan that silently matches nothing.
        self.assertIn("2026-07-23-obra-superpowers", guarded)

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
