import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "plugins" / "frozen-skills" / "skills" / "external-skill-intake"


class ExternalSkillIntakeContractTests(unittest.TestCase):
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
