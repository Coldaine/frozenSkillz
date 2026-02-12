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

## Design Decisions

Full decision records with rationale, alternatives considered, and consequences live in `docs/decisions/`. Here's the index with the key takeaway from each:

| ADR | Decision | Key Takeaway |
|-----|----------|-------------|
| [001](docs/decisions/001-llm-only-classification.md) | LLM-only classification, no keywords | Intent is ambiguous without context. Keywords rot. A wrong suggestion is worse than a slow one. |
| [002](docs/decisions/002-gemini-flash-cli-mvp.md) | Gemini Flash 3 via CLI for MVP | Zero setup beats fast — validate the architecture first, optimize latency second. `classify()` is isolated for backend swaps. |
| [003](docs/decisions/003-hook-output-format.md) | `additionalContext` with `<user-prompt-submit-hook>` tags | Documented pattern for UserPromptSubmit. Doesn't conflict with superpowers' system-level injection. Tags carry authority. |
| [004](docs/decisions/004-silent-passthrough-failure-mode.md) | Silent passthrough on every failure | No suggestion is better than a wrong suggestion or a blocked prompt. The hook must never degrade the user experience. |
| [005](docs/decisions/005-two-layer-skill-activation.md) | Two-layer architecture (Policy + Discovery) | Policy alone = Claude knows it should use skills but can't pick one. Discovery alone = Claude gets a suggestion but might ignore it. Both together close the loop. |
| [006](docs/decisions/006-transcript-parsing-strategy.md) | JSONL parsing, 10 messages, 500 char truncation | Transcript is JSONL (not JSON). Skip `isMeta`. Handle content-block lists. 10 msgs × 500 chars ≈ 2,200 tokens total. |

ADR-002 also documents the Windows subprocess gotchas (npm `.cmd` shims, long prompt escaping via temp files) discovered during implementation.

## File Structure

> **Updated** to include cross-project skills and rules directories.

```
frozenSkillz/
├── CLAUDE.md                # This file — project docs and decision index
├── skill_classifier.py      # The hook script (entry point)
├── test_classifier.py       # Manual test harness (5 scenarios + latency batch)
├── mock_input.json          # Test fixture: debugging scenario payload
├── mock_transcript.jsonl    # Test fixture: 4-message auth conversation
├── .gitignore               # Ignores .skills_cache.json and __pycache__
├── .claude/
│   └── settings.json        # Hook registration (project-scoped)
└── docs/
    └── decisions/           # Architecture Decision Records (ADRs)
        ├── 001-llm-only-classification.md
        ├── 002-gemini-flash-cli-mvp.md
        ├── 003-hook-output-format.md
        ├── 004-silent-passthrough-failure-mode.md
        ├── 005-two-layer-skill-activation.md
        └── 006-transcript-parsing-strategy.md
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

---

## Cross-Project Assets (skills/ and rules/)

In addition to the skill classifier hook, this repo serves as the **canonical source for cross-project agent skills and rules**. These are universal assets that get deployed to every project via the git submodule.

### Skills (`skills/`)

Portable workflow capsules with `SKILL.md` + optional references. These are tool-agnostic and project-agnostic.

| Skill | Purpose |
|-------|---------|
| `agent-config-megaref` | Definitive reference for configuring any AI coding tool — config locations, precedence, schemas, verification |
| `mcp-deployment-guide` | MCP server deployment across all tools — config formats, secrets patterns, common pitfalls |

### Rules (`rules/`)

Universal rule templates that can be deployed to any project's `.claude/rules/` (or equivalent). Each rule has a `paths:` trigger and a "Project Customization" section explaining what to override per-project.

| Rule | Triggers On | What It Enforces |
|------|------------|------------------|
| `documentation-frontmatter.md` | `docs/**/*.md` | All docs need YAML frontmatter with required fields |
| `ansible-playbooks.md` | `ansible/**/*.yml` | Playbook headers, no hardcoded secrets, no agent execution |
| `submodule-workflow.md` | `**/skills/frozen/**`, `**/.gitmodules` | Don't modify submodule files directly + full workflow guide |

### Deploying to a Project

1. Add this repo as a submodule: `git submodule add https://github.com/Coldaine/frozenSkillz.git skills/frozen`
2. Copy rules you want: `cp skills/frozen/rules/documentation-frontmatter.md .claude/rules/`
3. Customize the copy with project-specific values (subsystems, exempt files, etc.)
4. Skills are referenced directly from the submodule path — no copying needed
