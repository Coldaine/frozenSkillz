#!/usr/bin/env python3
"""Passive instrument: log spawn prompt sizes, never deny.

Baseline control for the ledger-guard eval. Same PreToolUse matcher as
the guard so it observes exactly what the guard would observe, but it
always exits 0 with no output, so nothing is ever blocked.
"""
import json
import os
import sys

LOG = os.environ.get("PROBE_LOG") or os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "probe.jsonl")


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    if not isinstance(data, dict):
        return
    try:
        ti = data.get("tool_input")
        if not isinstance(ti, dict):
            ti = {}
        tool = data.get("tool_name") or ""
        text = ti.get("script") if tool == "Workflow" else ti.get("prompt")
        rec = {
            "tool": tool,
            "chars": len(text) if isinstance(text, str) else 0,
            "subagent_type": ti.get("subagent_type") or "",
        }
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
    except Exception:
        return


if __name__ == "__main__":
    main()
