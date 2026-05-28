# ADR-008: Subagent Prompt Quality Gate

**Status:** Accepted
**Date:** 2026-05-28
**Deciders:** pmacl
**Issue:** [#4 — Add subagent prompt quality gate hook](https://github.com/Coldaine/frozenSkillz/issues/4)

## Context

A vague, multi-part research prompt invites a subagent to pad its answer and
fabricate specifics. The motivating failure: a 6-question research prompt about
lightweight vision models produced 2000+ words of invented latency numbers and
unverified comparisons. The prompt mixed lookup ("what exists") with speculation
("how fast is it"), gave no "don't guess" instruction, set no length constraint,
and supplied no prior context.

This is the same two-layer pattern as the skill classifier (a fast local LLM
that injects guidance), applied to a different event: instead of suggesting a
skill on `UserPromptSubmit`, review the subagent prompt on `PreToolUse` for the
`Agent`/`Task` tool.

The issue left three questions open: hard gate vs soft guidance; fire on all
agents vs research/explore only; and how to avoid latency on every agent call.

## Decision

A `PreToolUse` hook (`scripts/prompt_quality_gate.py`) on `matcher: "Agent|Task"`
that sends the subagent prompt to the shared `llm_backend` with a checklist and
injects the result as advisory context.

1. **Soft guidance, never a hard gate.** The hook emits
   `hookSpecificOutput.additionalContext` with `permissionDecision` omitted, so
   the dispatch always proceeds. The model judges; it is never blocked. The
   model can return `OK` to suppress output entirely.
2. **Fire on all `Agent`/`Task` dispatches, gated by length.** Rather than
   maintain a list of "research-like" subagent types, the hook skips prompts
   shorter than `SUBAGENT_PROMPT_GATE_MIN_CHARS` (default 200) — a trivial
   dispatch cannot meaningfully violate the checklist — and lets the model
   return `OK` for well-formed longer prompts. The checklist is phrased so
   non-research prompts pass cleanly.
3. **Latency is bounded and opt-out.** The gate adds one LLM round-trip per
   (non-trivial) dispatch. It is mitigated by: the min-length skip; the backend's
   fast-fail when the LLM is unreachable (~1s) plus silent passthrough; an
   `SUBAGENT_PROMPT_GATE=0` kill switch; and an 8s hook-level `timeout` backstop
   in `hooks.json`.

## The checklist

- one focused ask vs a wishlist (>2 distinct questions)
- says what NOT to do / NOT to guess; report "unknown" instead of estimating
- constrains response length / format
- provides context about what is already known
- does not mix lookup ("what exists") with speculation ("how fast is it")

## Rationale

- **Soft over hard:** prompt "quality" is a judgment call, and a false positive
  that blocks a legitimate dispatch is far more disruptive than an ignorable
  suggestion. Advisory context preserves agency and matches ADR-004's
  best-effort, silent-on-failure philosophy.
- **Defensive field extraction:** the subagent tool's input field names are not
  guaranteed across versions, so `extract_prompt()` collects every known
  string-valued key (`description`, `prompt`, `instructions`, `task`) rather than
  assuming one — fittingly, hard-coding a single guessed field name is exactly
  the kind of fragile assumption this gate exists to discourage.
- **Reuse, not duplication:** the gate shares `llm_backend.complete()` with the
  classifier, so backend selection, the reachability guard, and the
  silent-passthrough contract are identical and tested once.

## Consequences

- **Positive:** Catches low-quality research prompts before they waste a subagent
  run, with zero blocking risk and a one-env-var off switch.
- **Negative:** Adds an LLM round-trip per non-trivial agent dispatch. Acceptable
  with a resident Ollama; mitigated by the min-length gate, fast-fail, and kill
  switch. Users who dispatch many agents and don't want the latency disable it.
- **Neutral:** The advisory is only as good as the small model's judgment; it is
  explicitly framed as advice ("apply your judgment"), not an authority.
