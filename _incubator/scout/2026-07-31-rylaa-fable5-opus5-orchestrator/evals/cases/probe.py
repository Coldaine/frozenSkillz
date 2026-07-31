#!/usr/bin/env python3
"""Passive instrument: log spawn prompt sizes, never deny.

Baseline control for the ledger-guard eval. Registered on the same
PreToolUse matcher as the guard (^(Agent|Task|Workflow|TaskCreate)$),
so it is invoked on the same calls, but it always exits 0 with no
output and nothing is ever blocked.

It does NOT replicate the guard's internal filtering, and deliberately
so — it is the uncensored control, and the guard is not a measurement
instrument:

  - The guard exempts subagent_type == "fork"; this logs forks.
  - The guard routes TaskCreate to a separate count-based path and
    never measures its length; this logs a TaskCreate row (chars 0,
    since TaskCreate carries no `prompt`).
  - The guard emits a metric only when a prompt EXCEEDS its threshold,
    so its log is left-censored; this logs every spawn at any length.

That last difference is the point: sub-threshold spawns are exactly
what the guard cannot see and what the eval needs counted. Filter the
resulting JSONL by `tool`/`subagent_type` when you want a
guard-comparable subset.
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
