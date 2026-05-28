#!/usr/bin/env python3
"""frozenSkillz — Subagent Prompt Quality Gate (PreToolUse hook).

Fires before the Agent/Task tool dispatches a subagent. Sends the subagent
prompt to the shared LLM backend, which checks it against a quality checklist,
and injects SOFT advisory guidance. It NEVER blocks the dispatch — it only adds
context the model can choose to act on. Silent passthrough whenever the prompt
looks fine, the backend is unavailable, or anything goes wrong.

Why (issue #4): a vague, multi-part research prompt invites a subagent to pad
answers and fabricate specifics. The checklist below is distilled from a real
failure where a 6-question research prompt produced 2000+ words of invented
latency numbers.

Checklist:
- one focused ask vs a wishlist (>2 distinct questions)
- says what NOT to do / NOT to guess; report "unknown" instead of estimating
- constrains response length / format
- provides context about what is already known
- does not mix lookup ("what exists") with speculation ("how fast is it")

Configuration (env):
- SUBAGENT_PROMPT_GATE          "0"/"off"/"false" disables the gate (default on)
- SUBAGENT_PROMPT_GATE_MIN_CHARS  skip prompts shorter than this (default 200)
- (backend selection/timeouts come from llm_backend / SKILL_CLASSIFIER_* env)
"""

import json
import sys

import llm_backend

# Tool names that dispatch a subagent across Claude Code versions.
AGENT_TOOLS = {"Agent", "Task"}
DEFAULT_MIN_CHARS = 200
MAX_ADVISORY_CHARS = 800
# Candidate keys that may hold the subagent's prompt/task text.
PROMPT_KEYS = ("description", "prompt", "instructions", "task")


def _gate_enabled() -> bool:
    import os
    val = os.environ.get("SUBAGENT_PROMPT_GATE", "").strip().lower()
    return val not in ("0", "off", "false", "no")


def _min_chars() -> int:
    import os
    try:
        return int(os.environ.get("SUBAGENT_PROMPT_GATE_MIN_CHARS", DEFAULT_MIN_CHARS))
    except (TypeError, ValueError):
        return DEFAULT_MIN_CHARS


def extract_prompt(tool_input: dict) -> str:
    """Pull the subagent prompt text out of the tool input, defensively.

    Field names vary by tool/version, so collect every known string-valued key
    rather than assuming one. Deduplicates identical fragments.
    """
    if not isinstance(tool_input, dict):
        return ""
    parts = []
    for key in PROMPT_KEYS:
        val = tool_input.get(key)
        if isinstance(val, str) and val.strip() and val.strip() not in parts:
            parts.append(val.strip())
    return "\n\n".join(parts)


def build_review_prompt(agent_prompt: str) -> str:
    return f"""You are reviewing a prompt that an AI agent is about to send to a SUBAGENT. Flag only REAL problems against this checklist:

1. Wishlist: does it cram more than ~2 distinct questions/tasks into one dispatch?
2. No-guess: does it tell the subagent what NOT to do, and to report "unknown" instead of guessing or estimating?
3. Output constraint: does it constrain the response length or format?
4. Known context: does it state what is already known so the subagent does not re-derive or fabricate it?
5. Lookup vs speculation: does it mix "what exists" (lookup) with "how good/fast/reliable is it" (speculation) in a single ask?

SUBAGENT PROMPT TO REVIEW:
\"\"\"
{agent_prompt}
\"\"\"

If the prompt is well-formed (no significant issues), output exactly: OK
Otherwise output 1-3 short, specific, actionable suggestions as plain lines starting with "- ". Do not restate the checklist, do not explain, do not exceed 3 lines."""


def review(agent_prompt: str) -> str:
    """Return advisory text, or "" if the prompt is fine / backend unavailable."""
    raw = llm_backend.complete(build_review_prompt(agent_prompt))
    if not raw:
        return ""
    text = raw.strip()
    # Model judged it fine.
    if text.upper() == "OK" or text.upper().startswith("OK\n") or text.upper().startswith("OK "):
        return ""
    # Keep only advisory bullet lines; bound length.
    lines = [ln.strip() for ln in text.splitlines() if ln.strip().startswith("-")]
    advisory = "\n".join(lines) if lines else text
    return advisory[:MAX_ADVISORY_CHARS].strip()


def main() -> None:
    try:
        raw = sys.stdin.read().strip()
        if not raw:
            return
        payload = json.loads(raw)
    except Exception:
        return

    try:
        if not _gate_enabled():
            return
        if payload.get("tool_name") not in AGENT_TOOLS:
            return

        agent_prompt = extract_prompt(payload.get("tool_input", {}) or {})
        if len(agent_prompt) < _min_chars():
            return  # too small to meaningfully violate the checklist

        advisory = review(agent_prompt)
        if not advisory:
            return

        hint = (
            "<agent-prompt-review>\n"
            "Advisory on the subagent prompt you are about to dispatch "
            "(non-blocking — apply your judgment):\n"
            f"{advisory}\n"
            "</agent-prompt-review>"
        )
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": hint,
            }
        }
        json.dump(output, sys.stdout)
    except Exception:
        # Best-effort guidance only: never block or corrupt a dispatch.
        return


if __name__ == "__main__":
    main()
