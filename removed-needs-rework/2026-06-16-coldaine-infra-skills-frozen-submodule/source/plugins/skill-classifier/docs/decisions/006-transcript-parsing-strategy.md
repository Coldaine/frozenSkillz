# ADR-006: Transcript Parsing Strategy

**Status:** Accepted
**Date:** 2026-02-08
**Deciders:** pmacl

## Context

The classifier needs conversation context to make good decisions. Claude Code stores conversation history in transcript files. We need to decide:
1. How to parse the transcript format
2. How much context to include
3. How to handle the various content formats

## Decision

- Parse transcript as JSONL (one JSON object per line)
- Include last 10 messages (user + assistant only, skip meta)
- Truncate each message to 500 characters
- Handle content as string or content-block list
- Represent tool uses as `[tool: name]` summaries

## Rationale

### JSONL, not JSON

The transcript format is JSONL — each line is an independent JSON object. The previous prototype (`intelligent_suggester.py`) parsed it as a single JSON document with `json.loads()`, which would fail on real transcripts. Each line looks like:

```json
{"type":"user","message":{"role":"user","content":"..."},"uuid":"...","timestamp":"...","isMeta":false}
```

We parse line-by-line with individual `json.loads()` calls so a malformed line doesn't break the entire transcript read.

### 10 messages, not 5

The previous prototype used the last 5 messages. During design review, we identified scenarios where 5 messages wasn't enough:
- User discusses a feature across 3-4 exchanges, then asks to plan it → the planning request makes sense only with the feature discussion as context
- User starts debugging, gets a suggestion, continues debugging → with only 5 messages, the classifier might not see the original skill activation and re-suggest

10 messages (~5 exchanges) covers most multi-turn tasks without excessive prompt size.

### 500 chars per message, not 200

The previous prototype truncated at 200 characters. This often cut off the meaningful part of a message. Consider: "I've been working on the authentication module and noticed that the JWT token validation in `src/auth/validate.py` is failing when..." — that's 140 chars before you even reach the actual problem description.

500 characters captures enough of the message to understand intent without bloating the classification prompt. With 10 messages at 500 chars + 14 skill descriptions, the total prompt stays under ~8K tokens — well within any model's capacity.

### Skip isMeta entries

Transcript entries with `"isMeta": true` are internal Claude Code bookkeeping — skill load confirmations, error notices, system messages. They're not part of the conversation the user is having and would confuse the classifier. Example:

```json
{"type":"user","message":{"role":"user","content":"Unknown skill: moe"},"isMeta":true}
```

This is Claude Code reporting an error, not the user typing "Unknown skill: moe."

### Content-block list handling

Assistant messages often use a content-block list instead of a plain string:

```json
{"content": [
  {"type": "text", "text": "I'll fix that bug..."},
  {"type": "tool_use", "name": "Edit", "input": {...}},
  {"type": "text", "text": "Done, the fix is applied."}
]}
```

We extract text blocks and summarize tool uses as `[tool: Edit]`. This gives the classifier signal about what Claude is doing (editing, reading, running commands) without the verbose tool input/output that would blow up the context window.

## Token Budget

Worst case calculation:
- 10 messages × 500 chars ≈ 5,000 chars ≈ ~1,500 tokens
- 14 skills × ~100 chars each ≈ 1,400 chars ≈ ~400 tokens
- Classification prompt template ≈ ~300 tokens
- **Total: ~2,200 tokens input**

This is trivial for any modern LLM. Gemini Flash 3 has a 1M token context window.

## Consequences

- **Positive:** Classifier has enough context to understand multi-turn conversations.
- **Positive:** Token budget is well within limits, even for the cheapest models.
- **Positive:** Tool use summaries give behavioral signal without verbose content.
- **Negative:** Reading the entire transcript file to get the last 10 messages is O(n) on transcript length. For very long sessions (1000+ messages), this could add latency. Mitigated by the fact that file I/O is fast compared to the LLM call.
