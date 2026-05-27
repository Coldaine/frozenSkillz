---
name: session-skill-inferencer
description: >
  Analyze agentic coding sessions to discover friction patterns and generate skills, 
  rules, and hooks. Use when running /insight across multiple sessions or optimizing 
  AI assistant configuration. Do NOT use for single sessions or non-agentic tasks.
license: MIT
version: "1.0.0"
tags: ["analysis", "skills", "session", "insights", "cross-tool"]
---

# Session Skill Inferencer

Analyze agentic coding sessions across tools, extract structured facets via LLM analysis, and generate actionable skills, rules, and hooks from recurring patterns.

## Workflow

1. Discover session files across all installed agentic tools
2. Parse and normalize sessions into a unified format
3. Run LLM facet extraction on each session (friction, effective patterns, decisions, learnings)
4. Aggregate facets across sessions and run cross-session LLM analysis
5. Generate CLAUDE.md rules, hook configs, and SKILL.md files from recurring patterns
6. Validate generated skills against quality criteria

## Session Discovery

Discover session files at these locations:

| Tool | Unix/macOS | Windows |
|------|------------|---------|
| **Claude Code** | `~/.claude/projects/<encoded-path>/*.jsonl` | `%USERPROFILE%\.claude\projects\<encoded-path>\*.jsonl` |
| **Codex CLI** | `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl` | `%USERPROFILE%\.codex\sessions\YYYY\MM\DD\rollout-*.jsonl` |
| **Cursor** | `~/.cursor/projects/<project>/agent-transcripts/*.jsonl` | `%USERPROFILE%\.cursor\projects\<project>\agent-transcripts\*.jsonl` |
| **Copilot CLI** | `~/.copilot/session-state/*/events.jsonl` | `%USERPROFILE%\.copilot\session-state\*\events.jsonl` |
| **VS Code Copilot** | `workspaceStorage/<hash>/chatSessions/*.json` | Same (relative to workspace) |
| **Gemini CLI** | `~/.gemini/tmp/*/chats/session-*.json` | `%USERPROFILE%\.gemini\tmp\*\chats\session-*.json` |
| **Kiro CLI** | `~/.kiro/sessions/cli/*.jsonl` | `%USERPROFILE%\.kiro\sessions\cli\*.jsonl` |
| **OpenCode** | `~/.opencode/sessions/*.jsonl` | `%USERPROFILE%\.opencode\sessions\*.jsonl` |

**Note:** Cursor also stores data in SQLite at `state.vscdb` (cross-platform).

**Unix/macOS:**

```bash
find ~/.claude/projects -name "*.jsonl" -type f 2>/dev/null | wc -l
find ~/.codex/sessions -name "*.jsonl" -type f 2>/dev/null | wc -l
find ~/.cursor/projects -name "*.jsonl" -type f 2>/dev/null | wc -l
```

**Windows (PowerShell):**

```powershell
(Get-ChildItem -Path "$env:USERPROFILE\.claude\projects" -Filter "*.jsonl" -Recurse -ErrorAction SilentlyContinue).Count
(Get-ChildItem -Path "$env:USERPROFILE\.codex\sessions" -Filter "*.jsonl" -Recurse -ErrorAction SilentlyContinue).Count
(Get-ChildItem -Path "$env:USERPROFILE\.cursor\projects" -Filter "*.jsonl" -Recurse -ErrorAction SilentlyContinue).Count
```

## Session Parsing

For each session file, extract into this unified structure:

| Field | Source |
|-------|--------|
| `session_id` | Filename UUID, tool-prefixed if needed |
| `tool` | claude-code, codex, cursor, copilot, etc. |
| `project` | Decoded from directory path |
| `started_at`, `ended_at` | Timestamps from entries |
| `message_count` | Total entries (filter out tool results from Claude `user` entries) |
| `tool_calls` | `tool_use` / `function_call` blocks |
| `token_usage` | Per-message usage fields if present |
| `model` | From metadata or usage entries |
| `first_user_message` | First real human message (not tool result), truncated 200 chars |

**Parsing rules:** Claude `user` entries are ~80% tool results (filter by content type). Cursor content may be Lexical JSON (extract via `root.children[].children[].text`). Codex turns accumulate until `task_complete`. Gemini is single-JSON, not JSONL.

## LLM Facet Extraction

For each session (after parsing), send the transcript to an LLM using the prompt in [references/facet-extraction-prompt.md](references/facet-extraction-prompt.md). The prompt extracts:

- **Friction points** (up to 5): category, attribution (user-actionable / ai-capability / environmental), severity, resolution, description
- **Effective patterns** (up to 3): category, confidence, driver (user-driven / ai-driven / collaborative), description
- **Decisions** (up to 3): choice, reasoning, alternatives, trade-offs, revisit conditions
- **Learnings** (up to 5): symptom, root cause, takeaway, applies_when, confidence

Only include insights rated 70+ confidence. Each must cite evidence from the transcript (e.g., `User#5`, `Assistant#12`).

## Cross-Session Aggregation

After extracting facets from all sessions, aggregate into frequency-ranked lists:

1. **Friction categories**: Count occurrences per category, weight by severity (high=3, medium=2, low=1). Sort by frequency x severity.
2. **Effective patterns**: Count occurrences per category. Sort by frequency.
3. **Recurring insights**: Find semantically similar decisions/learnings across different sessions. Group by theme.

Then run the cross-session synthesis prompts from [references/cross-session-prompts.md](references/cross-session-prompts.md):
- **Friction & Wins narrative**: 3-5 most significant patterns with root cause and trend
- **Rules & Skills generation**: CLAUDE.md rules and hook configs from patterns with 3+ occurrences
- **Working style profile**: Archetype tagline and behavioral description

## Skill Generation

For each friction cluster with 3+ occurrences, generate a SKILL.md using the prompt in [references/skill-generation-prompt.md](references/skill-generation-prompt.md).

### Generated skill structure

```yaml
---
name: <kebab-case-name-matching-folder>
description: >
  <Action verb> <what it does>.
  Use when <trigger conditions>.
  Do NOT use for <negative triggers>.
license: MIT
---
```

### Domain-specific step templates

**CSS/Styling:** Audit selectors → Map affected components → Apply scoped fix → Visual check → Refine if needed

**Testing:** Read sibling tests → Run baseline → Implement following existing patterns → Run and verify → Check coverage

**Debugging:** Reproduce first → Gather evidence (no guessing) → Confirm root cause with evidence → Apply targeted fix → Verify fix and regression

**Data/SQL:** Inspect schema → Validate query logic → Test with sample data → Implement fix → Verify results

**Imports/Dependencies:** Check sibling conventions → Verify module resolution → Apply import change → Build check → Verify runtime

**Architecture/Scope:** Map boundaries → Check scope constraints → Assess cross-cutting impact → Implement within bounds → Verify boundaries held

**General (fallback):** Diagnose → Identify constraints → Propose approach → Implement minimal change → Verify

### Quality checklist for generated skills

- [ ] Name is kebab-case and matches parent folder
- [ ] Description has action verb + trigger phrases + negative triggers, under 300 chars
- [ ] Body has numbered steps
- [ ] Body has examples or code blocks
- [ ] Includes "What Goes Wrong" section with real session examples
- [ ] Includes verification checklist
- [ ] Under 5000 words
- [ ] No overlap with existing skills

## CLAUDE.md Rule Generation

For friction patterns with 3+ occurrences, generate rules in imperative mood. Group by domain. Include `> _Why: <evidence from session analysis>_` attribution.

## Hook Configuration Generation

Map friction domains to hooks:

- **CSS/Styling**: PreToolUse prompt — audit selectors before editing
- **Testing**: PostToolUse command
  - Unix: `npm test 2>&1 | tail -20`
  - Windows: `npm test 2>&1 | Select-Object -Last 20`
- **Debugging**: Stop prompt — verify root cause confirmed with evidence
- **Scope/Boundary**: PreToolUse prompt — confirm scope boundaries before changes
- **Imports**: PreToolUse prompt — verify against sibling conventions

## Integration with Existing Tools

- **claude-insights** (`npm install -g claude-insights`): Parses `/insight` HTML reports → generates deterministic skills from 7 domain templates. Claude-only, no LLM.
- **code-insights** (`npx code-insights`): Multi-tool parser (5 tools) + `reflect` command with real LLM analysis. The only tool that does cross-tool LLM-powered session analysis.
- **agentsview** (`go install`): 22-tool session viewer with analytics dashboard. Pure stats, no LLM skill generation.
- **Claude `/insight`**: Built-in Claude Code command. Haiku-powered multi-stage pipeline. Claude-only.

## Related Tools

This skill is conceptually related to **claude-insights** (npm package), which parses Claude Code `/insight` HTML reports into actionable improvements including CLAUDE.md rules, hook settings, MCP recommendations, and custom skills. While claude-insights is Claude-only and deterministic, this skill works across all agentic tools and uses LLM analysis for deeper pattern extraction.

## Troubleshooting

- **No sessions found**: Check that the agentic tool has been used recently. Session files are only created when you actually run a session.
- **Cursor sessions are empty**: Cursor stores data in SQLite (`state.vscdb`), not flat files. Use `sqlite3` to extract from `cursorDiskKV` table looking for `composerData:*` keys.
- **Gemini sessions fail to parse**: Gemini uses single-JSON format, not JSONL. Parse the entire file as one JSON object.
- **Claude `user` entries are 80% tool results**: Filter by checking if the content array contains `tool_result` type blocks.
- **Generated skills don't trigger**: Ensure the folder name matches the `name` field in frontmatter exactly. Place in `.claude/skills/<name>/SKILL.md`.
