#!/usr/bin/env python3
"""Automated tests for the swappable LLM backend.

Exercises the Ollama code path end-to-end against a local HTTP stub (no real
model required), the fast-fail guard when Ollama is down, backend ordering,
and the classifier's JSON-array parsing.

Run: python test_llm_backend.py        (exits non-zero on failure)
"""

import json
import os
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import llm_backend  # noqa: E402
import skill_classifier  # noqa: E402


# --- Ollama HTTP stub ---------------------------------------------------------

class _OllamaStubHandler(BaseHTTPRequestHandler):
    response_text = '["agent-config-megaref"]'

    def do_POST(self):  # noqa: N802 (http.server API)
        length = int(self.headers.get("Content-Length", 0))
        _ = self.rfile.read(length)  # drain request body
        payload = json.dumps({"response": self.response_text}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *args):  # silence the stub server
        pass


class _StubServer:
    def __enter__(self):
        self.httpd = HTTPServer(("127.0.0.1", 0), _OllamaStubHandler)
        self.port = self.httpd.server_address[1]
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        return self

    def __exit__(self, *exc):
        self.httpd.shutdown()
        self.httpd.server_close()


def _clear_backend_env():
    for k in ("SKILL_CLASSIFIER_BACKEND", "OLLAMA_HOST", "SKILL_CLASSIFIER_MODEL"):
        os.environ.pop(k, None)


# --- Tests --------------------------------------------------------------------

class TestLlmBackend(unittest.TestCase):
    def setUp(self):
        _clear_backend_env()

    def tearDown(self):
        _clear_backend_env()

    def test_empty_prompt_is_noop(self):
        self.assertEqual(llm_backend.complete(""), "")
        self.assertEqual(llm_backend.complete("   "), "")

    def test_ollama_happy_path(self):
        with _StubServer() as srv:
            os.environ["SKILL_CLASSIFIER_BACKEND"] = "ollama"
            os.environ["OLLAMA_HOST"] = f"http://127.0.0.1:{srv.port}"
            out = llm_backend.complete("classify this")
        self.assertEqual(out, '["agent-config-megaref"]')

    def test_ollama_down_fast_fail(self):
        # Bind+release a port to get one that is almost certainly closed.
        import socket
        s = socket.socket()
        s.bind(("127.0.0.1", 0))
        closed_port = s.getsockname()[1]
        s.close()
        os.environ["OLLAMA_HOST"] = f"http://127.0.0.1:{closed_port}"
        self.assertFalse(
            llm_backend._ollama_reachable(f"http://127.0.0.1:{closed_port}", 0.5)
        )
        self.assertEqual(llm_backend._ollama_complete("hi", 10), "")

    def test_reachable_true_against_stub(self):
        with _StubServer() as srv:
            self.assertTrue(
                llm_backend._ollama_reachable(f"http://127.0.0.1:{srv.port}", 0.5)
            )

    def test_backend_order_resolution(self):
        self.assertEqual(llm_backend._backend_order(), ["ollama", "gemini"])
        os.environ["SKILL_CLASSIFIER_BACKEND"] = "gemini"
        self.assertEqual(llm_backend._backend_order(), ["gemini", "ollama"])
        os.environ["SKILL_CLASSIFIER_BACKEND"] = "bogus"
        self.assertEqual(llm_backend._backend_order(), ["ollama", "gemini"])

    def test_classify_parses_ollama_output(self):
        # Full classify() path: real skills catalog + stubbed model output.
        with _StubServer() as srv:
            os.environ["SKILL_CLASSIFIER_BACKEND"] = "ollama"
            os.environ["OLLAMA_HOST"] = f"http://127.0.0.1:{srv.port}"
            result = skill_classifier.classify("anything", "", [
                {"name": "agent-config-megaref", "description": "x"},
            ])
        self.assertEqual(result, ["agent-config-megaref"])


class TestSkillArrayParsing(unittest.TestCase):
    def test_clean_array(self):
        self.assertEqual(skill_classifier._parse_skill_array('["a", "b"]'), ["a", "b"])

    def test_filters_non_strings(self):
        self.assertEqual(skill_classifier._parse_skill_array('["a", 1, "b"]'), ["a", "b"])

    def test_extracts_from_noise(self):
        self.assertEqual(skill_classifier._parse_skill_array('Sure: ["x"] done'), ["x"])

    def test_junk_returns_empty(self):
        self.assertEqual(skill_classifier._parse_skill_array("no array"), [])
        self.assertEqual(skill_classifier._parse_skill_array(""), [])

    def test_decoy_bracket_before_real_array(self):
        # Small local models emit reasoning text with decoy brackets; the parser
        # must skip them and find the real array (regression: non-greedy regex).
        self.assertEqual(
            skill_classifier._parse_skill_array('thinking [step 1] then ["systematic-debugging"]'),
            ["systematic-debugging"],
        )
        self.assertEqual(
            skill_classifier._parse_skill_array('Here is [the answer]: ["a", "b"]'),
            ["a", "b"],
        )


class TestSkillCache(unittest.TestCase):
    def setUp(self):
        os.environ.pop("SKILL_CLASSIFIER_SKILL_DIRS", None)
        self._cache = skill_classifier.CACHE_FILE
        if self._cache.exists():
            self._cache.unlink()

    def tearDown(self):
        os.environ.pop("SKILL_CLASSIFIER_SKILL_DIRS", None)
        if self._cache.exists():
            self._cache.unlink()

    def test_cache_invalidates_on_dir_change(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d1, tempfile.TemporaryDirectory() as d2:
            (Path(d1) / "SKILL.md").write_text(
                "---\nname: tmp-skill\ndescription: x\n---\n", encoding="utf-8")
            os.environ["SKILL_CLASSIFIER_SKILL_DIRS"] = d1
            first = skill_classifier.get_skills()
            self.assertEqual([s["name"] for s in first], ["tmp-skill"])
            # Same TTL window, different dirs -> must NOT serve the stale cache.
            os.environ["SKILL_CLASSIFIER_SKILL_DIRS"] = d2
            self.assertEqual(skill_classifier.get_skills(), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
