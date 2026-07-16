import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "plugins/frozen-skills/skills/chat-history/scripts/conversation_inventory.py"
DEPLOY_PATH = ROOT / "scripts/deploy_frozen_skill.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")


class ConversationInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventory = load_module("conversation_inventory", INVENTORY_PATH)

    def test_codex_workers_collapse_under_one_user_conversation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            parent = root / "rollout-parent.jsonl"
            write_jsonl(parent, [
                {"timestamp": "2026-07-16T12:00:00Z", "type": "session_meta", "payload": {"id": "parent", "cwd": "D:/work", "thread_source": "user"}},
                {"timestamp": "2026-07-16T12:01:00Z", "type": "event_msg", "payload": {"type": "user_message", "message": "Review every workflow"}},
                {"timestamp": "2026-07-16T12:59:00Z", "type": "event_msg", "payload": {"type": "task_complete"}},
            ])
            paths = [parent]
            for index in range(39):
                child = root / f"rollout-child-{index}.jsonl"
                write_jsonl(child, [
                    {"timestamp": "2026-07-16T12:02:00Z", "type": "session_meta", "payload": {"id": f"child-{index}", "parent_thread_id": "parent", "thread_source": "subagent", "cwd": "D:/work"}},
                    {"timestamp": "2026-07-16T12:30:00Z", "type": "event_msg", "payload": {"type": "task_complete"}},
                ])
                paths.append(child)

            records = self.inventory.parse_codex_files(paths)
            report = self.inventory.build_report(records, at=datetime(2026, 7, 16, 12, 45, tzinfo=timezone.utc))

            self.assertEqual(report["user_conversation_count"], 1)
            self.assertEqual(report["execution_record_count"], 40)
            self.assertEqual(report["conversations"][0]["child_count"], 39)
            self.assertEqual(report["conversations"][0]["state_at_cutoff"], "active")
            self.assertEqual(report["conversations"][0]["current_state"], "completed")
            self.assertEqual(report["conversations"][0]["last_user_at_cutoff"], "Review every workflow")

    def test_history_index_and_ui_event_do_not_become_conversations(self):
        records = [
            self.inventory.SessionRecord(tool="codex", native_id="chat", kind="conversation", started_at=datetime(2026, 7, 16, 12, tzinfo=timezone.utc), last_activity=datetime(2026, 7, 16, 13, tzinfo=timezone.utc)),
            self.inventory.SessionRecord(tool="codex", native_id="history-row", kind="index", started_at=datetime(2026, 7, 16, 12, tzinfo=timezone.utc), last_activity=datetime(2026, 7, 16, 13, tzinfo=timezone.utc)),
            self.inventory.SessionRecord(tool="antigravity", native_id="appx-update", kind="event", started_at=datetime(2026, 7, 16, 12, tzinfo=timezone.utc), last_activity=datetime(2026, 7, 16, 13, tzinfo=timezone.utc)),
        ]
        report = self.inventory.build_report(records)
        self.assertEqual(report["user_conversation_count"], 1)
        self.assertEqual(report["evidence_record_count"], 2)

    def test_missing_terminal_marker_is_not_claimed_active_without_later_evidence(self):
        record = self.inventory.SessionRecord(tool="claude-code", native_id="uncertain", kind="conversation", started_at=datetime(2026, 7, 16, 12, tzinfo=timezone.utc), last_activity=datetime(2026, 7, 16, 12, 30, tzinfo=timezone.utc))
        self.assertEqual(self.inventory.state_at(record, datetime(2026, 7, 16, 12, 45, tzinfo=timezone.utc)), "active_or_interrupted")

    def test_markdown_is_windows_console_safe(self):
        record = self.inventory.SessionRecord(tool="codex", native_id="root", kind="conversation", started_at=datetime(2026, 7, 16, 12, tzinfo=timezone.utc), last_activity=datetime(2026, 7, 16, 13, tzinfo=timezone.utc))
        child = self.inventory.SessionRecord(tool="codex", native_id="child", parent_id="root", kind="subagent", started_at=datetime(2026, 7, 16, 12, tzinfo=timezone.utc), last_activity=datetime(2026, 7, 16, 13, tzinfo=timezone.utc))
        report = self.inventory.build_report([record, child])
        output = self.inventory.render_markdown(report, {"codex": {"status": "searched", "files": 2}}, explain=True)
        output.encode("cp1252")

    def test_title_prefers_real_user_event_and_extracts_goal_argument(self):
        self.assertEqual(self.inventory.clean_title("<command-name>/goal</command-name><command-args>deploy Codex</command-args>"), "deploy Codex")
        self.assertEqual(self.inventory.clean_title("# AGENTS.md instructions <INSTRUCTIONS>noise"), "")

    def test_claude_tool_result_is_not_a_human_prompt(self):
        item = {"type": "user", "message": {"content": [{"type": "tool_result", "content": "(Bash completed with no output)"}]}, "toolUseResult": {"stdout": ""}}
        self.assertFalse(self.inventory.is_human_claude_user(item))

    def test_middle_prompt_remains_visible_when_session_is_reused(self):
        record = self.inventory.SessionRecord(
            tool="claude-code",
            native_id="reused",
            kind="conversation",
            started_at=datetime(2026, 7, 16, 11, tzinfo=timezone.utc),
            last_activity=datetime(2026, 7, 16, 13, tzinfo=timezone.utc),
            user_prompts=[
                (datetime(2026, 7, 16, 11, 10, tzinfo=timezone.utc), "evaluate profiles"),
                (datetime(2026, 7, 16, 12, 20, tzinfo=timezone.utc), "deploy the new Codex configuration"),
                (datetime(2026, 7, 16, 12, 40, tzinfo=timezone.utc), "remember repo stars"),
            ],
        )
        report = self.inventory.build_report([record], at=datetime(2026, 7, 16, 12, 50, tzinfo=timezone.utc), window_start=datetime(2026, 7, 16, 12, tzinfo=timezone.utc))
        prompts = [item["text"] for item in report["conversations"][0]["incident_window_prompts"]]
        self.assertIn("deploy the new Codex configuration", prompts)

    def test_claude_subagent_is_attached_not_flattened(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "project"
            parent = project / "session.jsonl"
            child = project / "session" / "subagents" / "agent-a.jsonl"
            write_jsonl(parent, [
                {"type": "user", "sessionId": "session", "timestamp": "2026-07-16T12:00:00Z", "cwd": "D:/work", "message": {"role": "user", "content": "Deploy the new Codex version"}},
                {"type": "assistant", "sessionId": "session", "timestamp": "2026-07-16T12:30:00Z", "message": {"role": "assistant", "content": "Working"}},
            ])
            write_jsonl(child, [
                {"type": "assistant", "sessionId": "session", "agentId": "agent-a", "timestamp": "2026-07-16T12:10:00Z", "message": {"role": "assistant", "content": "Child work"}},
            ])
            records = self.inventory.parse_claude_files([parent, child])
            report = self.inventory.build_report(records)
            self.assertEqual(report["user_conversation_count"], 1)
            self.assertEqual(report["conversations"][0]["child_count"], 1)


class DeploymentDirectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.deploy = load_module("deploy_frozen_skill", DEPLOY_PATH)

    def test_destination_cannot_be_inside_repository_source(self):
        source = ROOT / "plugins/frozen-skills/skills/chat-history"
        with self.assertRaises(ValueError):
            self.deploy.validate_direction(source, source / "runtime-copy")

    def test_check_detects_destination_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "repo" / "skill"
            destination = root / "runtime" / "skill"
            source.mkdir(parents=True)
            destination.mkdir(parents=True)
            (source / "SKILL.md").write_text("upstream", encoding="utf-8")
            (destination / "SKILL.md").write_text("drift", encoding="utf-8")
            self.assertFalse(self.deploy.trees_match(source, destination))

    def test_deploy_copies_only_from_source_to_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "repo" / "skill"
            destination = root / "runtime" / "skill"
            source.mkdir(parents=True)
            (source / "SKILL.md").write_text("reviewed", encoding="utf-8")
            self.deploy.deploy(source, destination)
            self.assertTrue(self.deploy.trees_match(source, destination))
            self.assertEqual((destination / "SKILL.md").read_text(encoding="utf-8"), "reviewed")


if __name__ == "__main__":
    unittest.main()
