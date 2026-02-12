# ADR-001: LLM-Only Classification (No Keywords)

**Status:** Accepted
**Date:** 2026-02-08
**Deciders:** pmacl

## Context

We need a mechanism to decide which of 14 Claude Code skills is relevant to a given user prompt. The two candidate approaches are:

1. **Keyword/regex matching** — map known trigger words ("bug", "error", "plan", "refactor") to skill names.
2. **LLM classification** — send the prompt + conversation context to a fast LLM and ask it to pick the relevant skill(s).

## Decision

LLM-only classification. No keyword layer, no hybrid.

## Rationale

### Intent is ambiguous without context

"The tests are failing" could mean:
- **Debugging** — there's a bug, find it (`systematic-debugging`)
- **TDD** — tests don't exist yet, write them first (`test-driven-development`)
- **Verification** — I just changed something, are tests still passing? (`verification-before-completion`)

A keyword matcher sees "tests" and "failing" and has to guess. An LLM reads the prior 10 messages and knows that the user just refactored the auth module, so this is debugging — not TDD.

### Keyword lists rot

Every new skill requires updating the keyword map. Every false positive ("plan" in "I plan to fix this" triggering `writing-plans`) requires adding negative rules. The maintenance burden scales linearly with skill count and quadratically with ambiguity between skills. With 14 skills today and potentially more later, this becomes untenable.

### Re-suggestion suppression requires understanding

A keyword matcher doesn't know that `systematic-debugging` was already invoked 3 messages ago. It would re-trigger on every message that mentions "error". The LLM reads the conversation and sees the skill is already active.

### The latency tradeoff is acceptable

Keywords match in microseconds. An LLM call takes ~300ms (REST API) to ~10s (CLI). We accept this because:
- A wrong suggestion is worse than a slow one — it erodes trust and trains users to ignore suggestions.
- The target latency (REST API, Phase 2) is 300ms, which is imperceptible in a coding workflow where the user is about to wait 5-30s for Claude's response anyway.
- The MVP's 10s latency is too slow for production but acceptable for validating the approach.

## Alternatives Considered

### Hybrid (keywords + LLM confirmation)

Use keywords for fast pre-filtering, then LLM to confirm. Rejected because:
- Still requires maintaining keyword lists
- The LLM is fast enough to do both jobs
- Adds complexity for marginal latency gain

### Embedding similarity

Embed all skill descriptions, embed the user prompt, find nearest neighbors. Rejected because:
- Requires an embedding model (additional dependency)
- Doesn't benefit from conversation context the way a generative LLM does
- Similarity ≠ relevance (a prompt about "reviewing code" is *similar* to `requesting-code-review` but the relevant skill might be `receiving-code-review` depending on who's reviewing whom)

## Consequences

- **Positive:** Classification quality scales with LLM capability, not with our keyword engineering effort. New skills are automatically understood.
- **Negative:** Every prompt incurs an LLM call. If the backend is slow or down, the user experiences delay or no suggestion. Mitigated by silent passthrough on failure.
- **Negative:** Classification quality depends on prompt engineering. The classification prompt itself needs maintenance.
