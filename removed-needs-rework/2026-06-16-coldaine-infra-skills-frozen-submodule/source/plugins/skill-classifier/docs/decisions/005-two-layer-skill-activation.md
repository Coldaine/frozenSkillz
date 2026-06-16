# ADR-005: Two-Layer Skill Activation Architecture (Policy + Discovery)

**Status:** Accepted
**Date:** 2026-02-08
**Deciders:** pmacl

## Context

Claude Code has a skill system with 14 skills, but the model ignores them ~80% of the time. The root cause has two parts:

1. **Policy failure:** Claude doesn't know it's *supposed* to use skills. Its default behavior is to answer directly without checking if a skill applies.
2. **Discovery failure:** Even when told "use skills", Claude doesn't know *which* skill applies to *this specific prompt*. It can't search 14 skill descriptions mid-response and pick the right one.

The superpowers project already solved problem #1 with a `SessionStart` hook that tells Claude "you must use skills." But skill activation rate remained low because problem #2 was unsolved.

## Decision

Two separate hooks, in two separate projects, each solving one problem:

| Layer | Hook Type | Project | Injection |
|-------|-----------|---------|-----------|
| **Policy** | `SessionStart` | superpowers | "You have skills. You must use them." |
| **Discovery** | `UserPromptSubmit` | frozenSkillz | "Use `systematic-debugging` for this prompt." |

## Rationale

### Why two layers, not one?

A single hook could theoretically do both — inject policy AND identify the relevant skill. We separated them because:

1. **Different lifecycles.** Policy is set once per session. Discovery runs on every prompt. Combining them means either running the LLM classifier on session start (wasteful — no prompt to classify yet) or re-injecting policy on every prompt (redundant and token-expensive).

2. **Different failure modes.** If the policy hook fails, Claude doesn't know skills exist — catastrophic. If the discovery hook fails, Claude knows skills exist but doesn't get a specific suggestion — degraded but functional. Separating them means a frozenSkillz failure doesn't take down the policy layer.

3. **Independent development.** superpowers is stable and well-tested. frozenSkillz is experimental. Coupling them means a bug in the classifier could break session initialization.

### Why both layers are needed

**Policy alone (superpowers only):**
Claude knows it should use skills but has to figure out which one applies. With 14 skills, it rarely picks the right one — or any at all. It's like telling someone "use the right tool" without showing them the toolbox. Observed activation rate: ~20%.

**Discovery alone (frozenSkillz only):**
Claude gets told "use `systematic-debugging`" but doesn't have the general instruction to take skill suggestions seriously. It might acknowledge the suggestion but proceed without actually loading the skill. The suggestion is a hint, not a mandate.

**Both together:**
Claude has standing orders to use skills (policy) AND a specific recommendation for this prompt (discovery). The policy layer makes it receptive; the discovery layer tells it what to do. Expected activation rate: >80%.

### Why separate projects?

- **superpowers** owns the skill files themselves, the SessionStart hook, and the skill resolution infrastructure. It's the skill platform.
- **frozenSkillz** is purely a classifier — it reads skills from superpowers but doesn't own them. It's a consumer of the platform.

This separation means frozenSkillz can be uninstalled without affecting the skill system. It's an accelerator, not a dependency.

## Future: Consolidation

If frozenSkillz proves reliable and superpowers' policy injection becomes redundant (because the discovery layer is strong enough on its own), we may consolidate:
- frozenSkillz takes over SessionStart injection
- superpowers becomes purely the skill host (no hooks)
- One project owns both layers

This is Phase 2+ and depends on validation data.

## Consequences

- **Positive:** Each layer can be developed, tested, and deployed independently.
- **Positive:** Failure in one layer doesn't cascade to the other.
- **Positive:** Clear ownership — superpowers = platform, frozenSkillz = intelligence.
- **Negative:** Two projects to maintain. Two hooks firing per prompt. Marginal complexity cost.
- **Negative:** The two hooks need to not conflict. Currently they don't — one fires on SessionStart, the other on UserPromptSubmit — but future changes could create interaction effects.
