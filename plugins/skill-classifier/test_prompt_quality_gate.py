#!/usr/bin/env python3
"""Automated tests for the subagent prompt quality gate (issue #4).

Drives the hook's main() with stubbed stdin/stdout and a stubbed LLM backend so
the tests are deterministic and need no network, subprocess, or live model.

Run: python test_prompt_quality_gate.py    (exits non-zero on failure)
"""

import io
import json
import sys
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import llm_backend  # noqa: E402
import prompt_quality_gate as gate  # noqa: E402

LONG_PROMPT = (
    "Research the fastest vision models and tell me their latency, accuracy, "
    "framework support, license terms, and which one I should pick for my app. "
    "Give me a full comparison with numbers." * 2
)


def run_main(payload: dict, completion: str, env: dict = None) -> str:
    """Invoke gate.main() with a stubbed backend and captured stdout."""
    real_complete = llm_backend.complete
    real_stdin, real_stdout = sys.stdin, sys.stdout
    real_environ = dict(__import__("os").environ)
    try:
        llm_backend.complete = lambda *a, **k: completion
        sys.stdin = io.StringIO(json.dumps(payload))
        sys.stdout = io.StringIO()
        if env:
            __import__("os").environ.update(env)
        gate.main()
        return sys.stdout.getvalue()
    finally:
        llm_backend.complete = real_complete
        sys.stdin, sys.stdout = real_stdin, real_stdout
        os = __import__("os")
        os.environ.clear()
        os.environ.update(real_environ)


class TestExtractPrompt(unittest.TestCase):
    def test_prompt_key(self):
        self.assertEqual(gate.extract_prompt({"prompt": "hello"}), "hello")

    def test_combines_description_and_prompt(self):
        out = gate.extract_prompt({"description": "label", "prompt": "body"})
        self.assertIn("label", out)
        self.assertIn("body", out)

    def test_alt_field_names(self):
        self.assertEqual(gate.extract_prompt({"instructions": "do x"}), "do x")
        self.assertEqual(gate.extract_prompt({"task": "do y"}), "do y")

    def test_dedupes_identical(self):
        out = gate.extract_prompt({"prompt": "same", "instructions": "same"})
        self.assertEqual(out, "same")

    def test_non_dict(self):
        self.assertEqual(gate.extract_prompt(None), "")
        self.assertEqual(gate.extract_prompt("str"), "")


class TestReview(unittest.TestCase):
    def test_ok_means_no_advisory(self):
        llm_backend_complete = llm_backend.complete
        try:
            llm_backend.complete = lambda *a, **k: "OK"
            self.assertEqual(gate.review("anything"), "")
        finally:
            llm_backend.complete = llm_backend_complete

    def test_empty_backend_no_advisory(self):
        c = llm_backend.complete
        try:
            llm_backend.complete = lambda *a, **k: ""
            self.assertEqual(gate.review("anything"), "")
        finally:
            llm_backend.complete = c

    def test_bullets_returned(self):
        c = llm_backend.complete
        try:
            llm_backend.complete = lambda *a, **k: "- Split into one question\n- Say what not to guess"
            out = gate.review("anything")
            self.assertIn("Split into one question", out)
            self.assertIn("Say what not to guess", out)
        finally:
            llm_backend.complete = c


class TestMain(unittest.TestCase):
    def test_non_agent_tool_silent(self):
        out = run_main({"tool_name": "Read", "tool_input": {"prompt": LONG_PROMPT}},
                       completion="- bad prompt")
        self.assertEqual(out, "")

    def test_short_prompt_silent(self):
        out = run_main({"tool_name": "Agent", "tool_input": {"prompt": "fix bug"}},
                       completion="- bad prompt")
        self.assertEqual(out, "")

    def test_ok_is_silent(self):
        out = run_main({"tool_name": "Agent", "tool_input": {"prompt": LONG_PROMPT}},
                       completion="OK")
        self.assertEqual(out, "")

    def test_disabled_via_env(self):
        out = run_main({"tool_name": "Agent", "tool_input": {"prompt": LONG_PROMPT}},
                       completion="- bad prompt", env={"SUBAGENT_PROMPT_GATE": "0"})
        self.assertEqual(out, "")

    def test_advisory_emitted(self):
        out = run_main({"tool_name": "Agent", "tool_input": {"prompt": LONG_PROMPT}},
                       completion="- Split the 5 questions into focused lookups\n- Tell it to report unknown")
        self.assertNotEqual(out, "")
        data = json.loads(out)
        ctx = data["hookSpecificOutput"]["additionalContext"]
        self.assertEqual(data["hookSpecificOutput"]["hookEventName"], "PreToolUse")
        self.assertNotIn("permissionDecision", data["hookSpecificOutput"])
        self.assertIn("agent-prompt-review", ctx)
        self.assertIn("Split the 5 questions", ctx)

    def test_task_tool_also_gated(self):
        out = run_main({"tool_name": "Task", "tool_input": {"prompt": LONG_PROMPT}},
                       completion="- needs an output constraint")
        self.assertIn("agent-prompt-review", out)

    def test_malformed_stdin_silent(self):
        real_stdin, real_stdout = sys.stdin, sys.stdout
        try:
            sys.stdin = io.StringIO("not json")
            sys.stdout = io.StringIO()
            gate.main()
            self.assertEqual(sys.stdout.getvalue(), "")
        finally:
            sys.stdin, sys.stdout = real_stdin, real_stdout


if __name__ == "__main__":
    unittest.main(verbosity=2)
