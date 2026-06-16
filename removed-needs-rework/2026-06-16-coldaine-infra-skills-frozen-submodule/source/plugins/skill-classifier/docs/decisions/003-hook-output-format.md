# ADR-003: Hook Output Format — additionalContext with user-prompt-submit-hook Tags

**Status:** Accepted
**Date:** 2026-02-08
**Deciders:** pmacl

## Context

Claude Code's hook system accepts two output fields from `UserPromptSubmit` hooks:

- **`systemMessage`** — injected as a system-level message. Higher perceived authority.
- **`additionalContext`** — injected alongside the user's prompt as additional context.

We also need to choose how to format the injected content so Claude actually follows the suggestion.

## Decision

Use `additionalContext` with `<user-prompt-submit-hook>` XML tags:

```json
{
  "additionalContext": "<user-prompt-submit-hook>\nSkill match detected: `systematic-debugging`. You MUST invoke these using the Skill tool before responding.\n</user-prompt-submit-hook>"
}
```

## Rationale

### additionalContext is the documented pattern

Claude Code's hook documentation specifies `additionalContext` for `UserPromptSubmit` hooks. Using `systemMessage` works but isn't the intended use — it's more appropriate for `SessionStart` or system-level policy injection.

### user-prompt-submit-hook tags carry authority

Claude's system prompt tells it: "Tags contain information from the system." The `<user-prompt-submit-hook>` tag is specifically mentioned in Claude's system instructions as a source of hook-injected context. Claude treats content in these tags as authoritative — equivalent to a system instruction for the current turn.

### Previous prototype used mixed approach

The previous `intelligent_suggester.py` used `systemMessage` with `<system-reminder>` tags for regular prompts and `additionalContext` for subagent contexts. This created two code paths for the same concept. We simplified to one path: `additionalContext` everywhere.

### systemMessage can conflict

If multiple hooks inject `systemMessage`, they may conflict or override each other. The superpowers `SessionStart` hook already uses system-level injection for the policy layer. Having frozenSkillz also inject system messages risks interaction effects. `additionalContext` is additive and doesn't conflict.

## Output Phrasing

The injected text says:

> Skill match detected: `systematic-debugging`. You MUST invoke these using the Skill tool before responding.

Key choices:
- **"You MUST"** — directive language that Claude follows. Softer phrasing ("you might want to consider...") gets ignored.
- **"using the Skill tool"** — explicit instruction on *how* to activate the skill. Without this, Claude might just mention the skill name without actually loading it.
- **"before responding"** — temporal ordering. Load the skill first, then act on the user's prompt with the skill's guidance.

## Consequences

- **Positive:** Single output path, no branching logic for subagent vs regular.
- **Positive:** Doesn't conflict with superpowers' system-level injection.
- **Positive:** Claude treats the suggestion as authoritative via the tag convention.
- **Negative:** If Claude's handling of `<user-prompt-submit-hook>` tags changes in a future version, the authority mechanism breaks. Low risk — it's part of Claude Code's documented hook contract.
