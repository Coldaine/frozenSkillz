# frozenSkillz — LLM-Powered Skill Classifier Hook

## The Problem This Solves

Claude Code has a skill system — 14 skills covering debugging, planning, TDD, code review, etc. — but the model ignores them ~80% of the time. The superpowers project added a `SessionStart` hook that tells Claude "you must use skills" (the **policy** layer), but that only solves half the problem. Claude still doesn't know *which* skill applies to *this specific prompt* (the **discovery** layer).

This is why you can tell Claude "always use skills" and it'll still dive straight into debugging without invoking `systematic-debugging`, or start building a feature without `brainstorming` first.

**frozenSkillz adds the discovery layer:** a `UserPromptSubmit` hook that reads the conversation, decides which skill is relevant *right now*, and injects a targeted "use THIS skill" directive before Claude sees the prompt.

### Two-Layer Architecture

| Layer | Hook | Project | What It Does |
|-------|------|---------|-------------|
| **Policy** | `SessionStart` | superpowers | "You must use skills" (general instruction) |
| **Discovery** | `UserPromptSubmit` | frozenSkillz | "Use `systematic-debugging` NOW" (specific, contextual) |

Policy without discovery = Claude knows it should use skills but doesn't know which one. Discovery without policy = Claude gets a suggestion but might ignore it. Together they close the loop.

## Architecture

```
User hits Enter
    ↓
UserPromptSubmit fires → skill_classifier.py receives stdin JSON
    ↓
Parse payload → extract prompt + transcript_path
    ↓
Load skill catalog (disk-cached, 5-min TTL)
    ↓
Read last 10 messages from JSONL transcript
    ↓
Build classification prompt → call Gemini Flash 3 via CLI
    ↓
Parse JSON array response → validate against known skill names
    ↓
No match / error / timeout? → exit silently (zero output = no disruption)
Match found? → output {"additionalContext": "<user-prompt-submit-hook>..."}
```

## Design Decisions and Why

### Why LLM classification, not keyword matching?

Keyword matching was the obvious first approach — map "bug", "error", "failing" to `systematic-debugging`, map "plan", "design" to `writing-plans`, etc. We rejected this because:

1. **Intent is ambiguous.** "The tests are failing" could mean debugging (fix the bug) or TDD (write tests first). "Let's plan the auth system" could mean `writing-plans` or `brainstorming`. Only an LLM can read the conversation context and disambiguate.
2. **Keyword lists rot.** Every new skill requires updating the keyword map. Every false positive requires adding exceptions. The maintenance burden scales linearly with skill count.
3. **Context matters.** If the user is already mid-debugging and says "now fix the other test", a keyword matcher would re-trigger `systematic-debugging`. An LLM sees the conversation and knows the skill is already active.

The tradeoff is latency — an LLM call takes seconds, keyword matching takes microseconds. We accept this tradeoff because a wrong suggestion is worse than a slow one, and the Gemini REST API (Phase 2) will bring latency to ~300ms.

### Why Gemini Flash 3 via CLI for MVP?

We needed an LLM that's (a) fast, (b) cheap/free, (c) already authenticated on this machine. Options considered:

| Backend | Pros | Cons | Decision |
|---------|------|------|----------|
| **Gemini CLI** | Already installed (v0.27.3), handles auth, Flash 3 is smart enough | ~10s startup on Windows (Node.js bootstrap) | **MVP default** — works today, good enough to validate the approach |
| **Gemini REST API** | ~300ms latency, no CLI overhead | Requires API key management, urllib code | **Phase 2** — clear upgrade path |
| **Anthropic SDK (Haiku)** | Very fast, ANTHROPIC_API_KEY in env | Costs money per call, SDK dependency | **Test alternative** — good for accuracy comparison |

The `classify()` function is deliberately isolated so swapping backends requires changing only one function. The CLI was chosen for MVP because it already works with zero setup.

### Why the temp file approach for the prompt?

We discovered during implementation that passing a long multi-line prompt as a `-p` argument to `gemini` via `subprocess.run(shell=True)` on Windows causes the process to hang indefinitely. The prompt contains quotes, newlines, brackets, and special characters that Windows cmd.exe can't handle in shell argument expansion.

**Solution:** Write the prompt to a temp file, pipe it via stdin to gemini, clean up the temp file in a `finally` block. This avoids all shell quoting issues regardless of prompt content.

This is a Windows-specific gotcha. On Linux/macOS, `shell=False` with list args would work fine, but npm-installed CLIs on Windows require `shell=True` to resolve `.cmd` shims (the actual executable is `gemini.cmd`, not `gemini`).

### Why `additionalContext` and not `systemMessage`?

Claude Code's hook system supports two output fields:
- `systemMessage` — injected as a system-level message (higher authority)
- `additionalContext` — injected as additional context alongside the user's prompt

We use `additionalContext` because:
1. It's the documented pattern for `UserPromptSubmit` hooks
2. It wraps naturally with `<user-prompt-submit-hook>` tags which Claude treats as authoritative user-side context
3. `systemMessage` can conflict with other system-level injections

The previous prototype (`intelligent_suggester.py`) used `systemMessage` with `<system-reminder>` tags for regular prompts and `additionalContext` for subagents. We simplified to `additionalContext` for everything since the `<user-prompt-submit-hook>` tag provides sufficient authority.

### Why 5-minute cache TTL for the skill catalog?

Skills don't change often (maybe once a week), so why not cache forever? Because:
1. During development, you're actively editing skills and need changes picked up
2. 5 minutes is long enough that consecutive prompts (the common case) never re-scan
3. Disk scan of ~14 SKILL.md files takes <50ms anyway — the cache is about avoiding unnecessary I/O, not about a slow operation

The previous prototype used the same 5-min TTL and it worked well in practice.

### Why 10 messages of context, truncated to 500 chars each?

The classifier needs enough context to understand what's happening but not so much that it overwhelms the LLM or bloats the prompt:
- **10 messages** covers ~5 user/assistant exchanges — enough to understand the current task
- **500 chars** per message keeps the total prompt under ~8K tokens even with all 14 skills listed
- The previous prototype used 5 messages at 200 chars, which sometimes missed relevant context

### Why JSONL transcript parsing?

Claude Code's transcript format is JSONL (one JSON object per line), not a single JSON document. Each line contains:
```json
{"type":"user","message":{"role":"user","content":"..."},"uuid":"...","timestamp":"..."}
```

Key parsing decisions:
- **Skip `isMeta` entries** — these are internal Claude Code messages (skill loads, error notices), not conversation
- **Handle content as string or content-block list** — assistant messages often use `[{"type":"text","text":"..."},{"type":"tool_use",...}]` format
- **Tool uses become `[tool: name]`** — gives the classifier signal about what Claude is doing without the verbose tool input/output

### Why silent passthrough on failure?

The #1 rule: **no suggestion is better than a wrong suggestion or a blocked prompt.** If anything goes wrong — network down, gemini not installed, timeout, malformed response, no matching skills — the hook exits with zero output, which Claude Code treats as "nothing to inject." The user never knows the hook ran and failed.

This is critical for trust. A hook that occasionally blocks or delays your prompt would be uninstalled immediately.

## File Structure

```
frozenSkillz/
├── CLAUDE.md               # This file — project docs and decision rationale
├── skill_classifier.py     # The hook script (entry point)
├── test_classifier.py      # Manual test harness (5 scenarios + latency batch)
├── mock_input.json          # Test fixture: debugging scenario payload
├── mock_transcript.jsonl    # Test fixture: 4-message auth conversation
├── .gitignore               # Ignores .skills_cache.json and __pycache__
└── .claude/
    └── settings.json        # Hook registration (project-scoped)
```

## How to Test

### Quick smoke test
```bash
# Should output JSON with systematic-debugging suggestion
python skill_classifier.py < mock_input.json

# Should produce zero output (silent passthrough)
echo '{"prompt":"hello","transcript_path":""}' | python skill_classifier.py
```

### Full test suite
```bash
python test_classifier.py
```

Tests 5 scenarios: trivial message (silent), empty prompt (silent), debugging (should suggest), creative work (should suggest brainstorming), planning (should suggest writing-plans). Optional latency batch at the end.

### Live testing

Open a Claude Code session in this directory. The hook auto-registers from `.claude/settings.json`. Every prompt you submit will go through the classifier.

## Hook Registration

### Project-scoped (current)
Already in `.claude/settings.json`. Only active when Claude Code is launched from this directory.

### Global deployment
Copy the hook entry to `~/.claude/settings.json` (merging with existing hooks). The script uses absolute paths so it works from any working directory.

## Relationship to Other Projects

- **superpowers** (`C:/_projects/EVALUATION/superpowers/`) — The skill host. frozenSkillz reads skills *from* superpowers' `skills/` directory. superpowers' `SessionStart` hook provides the policy layer; frozenSkillz provides the discovery layer.
- **intelligent_suggester.py** (`C:/_projects/EVALUATION/analysis/intelligent_suggester.py`) — The previous prototype. Used Gemini 2.0 Flash REST API directly. frozenSkillz inherits the caching pattern and prompt structure but improves transcript parsing (JSONL-aware), context window (10 msgs vs 5), and output format (user-prompt-submit-hook tags).

## Phase 2 Roadmap

- **Gemini REST API backend** — Drop CLI overhead from ~10s to ~300ms. The `classify()` function is already isolated for this swap.
- **SubagentStart hook** — Inject suggestions into spawned subagents (Plan, Explore, etc.) which currently get 0% skill activation.
- **Take over SessionStart** — Once discovery proves reliable, absorb the policy layer too, giving frozenSkillz full control of both layers.
- **Response caching** — Cache LLM responses by conversation-state hash to avoid redundant calls.

## Known Limitations

- **Latency:** Gemini CLI has ~10s startup on Windows (Node.js bootstrap + credential loading). This makes the hook synchronous and blocking. The REST API backend (Phase 2) is the fix.
- **Skill paths are hardcoded:** `SUPERPOWERS_SKILLS_DIR` points to `C:/_projects/EVALUATION/superpowers/skills`. If the superpowers project moves, this breaks. Could be made configurable via env var.
- **No SubagentStart support yet:** Only fires on `UserPromptSubmit`. Subagents spawned by Claude don't get skill suggestions.
