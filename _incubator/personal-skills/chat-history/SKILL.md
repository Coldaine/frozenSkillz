---
name: chat-history
description: Retrieve and analyze prior AI-agent conversations across Codex, Claude Code, Cursor, OpenCode, and other harnesses. Use when a request depends on past sessions, such as locating a decision, reconstructing earlier work, comparing runs, or reviewing recurring outcomes. Prefer AgentsView; use Pieces for web-chat localization and raw transcript parsers only for recovery gaps.
---

# Chat History

## Operating principle

Get the needed context quickly from the indexed conversation archive. Do not manually parse
per-harness transcript formats when AgentsView can search and retrieve the same sessions.

Do not add evidence ladders, coverage matrices, durable reports, or forensic labels unless the
user explicitly requests an audit, acceptance review, or exact reconstruction of a disputed event.
For recent context already visible in the active conversation, answer directly without invoking
this skill's retrieval workflow.

## Primary route: AgentsView

Prefer the AgentsView MCP tools when they are available:

1. Use `search_content` or `search_sessions` to find candidate sessions.
2. Use `get_session_overview` to check each candidate's project, agent, time, and scope.
3. Use `get_messages` around the matching ordinals to read the relevant conversation.
4. Use `get_usage_summary` only when the request concerns cost or token use.

Otherwise use the AgentsView CLI. Resolve it from `PATH`, then use the standard Windows install
location if necessary:

```powershell
$agentsView = (Get-Command agentsview -ErrorAction SilentlyContinue).Source
if (-not $agentsView) {
    $agentsView = Join-Path $env:LOCALAPPDATA 'AgentsView\agentsview.exe'
}

& $agentsView session search 'exact phrase or topic' --json --context 3 --include-children
& $agentsView session list --project 'project-name' --since 30d --json
& $agentsView session get '<session-id>' --json
& $agentsView session messages '<session-id>' --around 42 --before 8 --after 12 --json
```

Use the search filters to reduce the result set before reading messages: `--project`, `--agent`,
`--machine`, `--date`, `--date-from`, `--date-to`, `--since`, `--include-children`,
`--include-one-shot`, and `--include-automated`. Use `--fts` for fast tokenized search,
`--regex` for known variants, and `--semantic` or `--hybrid` when exact wording is unknown.
Keep `--limit` small until the query is well targeted so large JSON responses do not obscure the
useful matches. If a project filter returns suspiciously few results, run `agentsview projects` or
search without the filter; project labels can differ by harness and may use hyphens or underscores.

Use `--pg` when the configured PostgreSQL archive has broader fleet coverage than the local
archive. Do not assume configured enrollment or credentials prove that every machine is actively
syncing.

If the daemon is performing an initial sync, inspect it with:

```powershell
& $agentsView daemon status
& $agentsView doctor sync
```

Allow normal indexing to finish or query the configured PostgreSQL archive. Do not switch to raw
JSONL parsing merely because the first daemon-backed query is still warming up.

## Reading and synthesis

For a targeted lookup, read only the matching session and message window. Search snippets locate
content; the retrieved messages establish what the participants actually said and what happened
next.

For any multi-session comparison, retrospective, or pattern analysis, dispatch subagents by
default after AgentsView produces a broad candidate set. If the archive narrows the question to two
or three representative sessions, read them directly. Otherwise partition non-overlapping session
IDs among subagents and ask each subagent to return:

- which sessions are relevant;
- the decisions, corrections, actions, and outcomes that matter to the question;
- the session IDs and message ordinals supporting those observations;
- uncertainties or nearby false matches.

Keep candidate discovery in the primary agent so every subagent receives a bounded set. The
primary agent reconciles the returned summaries and answers the user's actual question. Do not
dispatch subagents for a single known session, a two-or-three-session sample, or a small
exact-message lookup.

## Fallback order

Use fallbacks only when the preceding route cannot provide the requested content.

1. **Broaden AgentsView retrieval.** Try query variants, session filters, child/one-shot inclusion,
   semantic or hybrid search, and the local-versus-PostgreSQL archive.
2. **Repair an indexing gap.** Use `agentsview session sync <path-or-id>` for a known local source,
   or `agentsview import` for a supported conversation export. Re-run the query afterward.
3. **Locate external web-app chats with Pieces.** Use Pieces LTM when the conversation lived in
   ChatGPT, Claude.ai, Gemini, or another browser application that AgentsView does not ingest.
   Treat Pieces OCR, window titles, and URLs as localization hints. Open the strongest candidate
   in the authenticated browser only when the actual body is needed.
4. **Read the raw source through AgentsView.** Use `agentsview session export <session-id>` when an
   exact source record or parser diagnosis is required.
5. **Use bundled parsers as recovery tools.** Run `extract_chat_history.py` only when AgentsView is
   unavailable or cannot ingest the relevant harness. Run `scripts/artifact_hunt.py` when the
   target may be a nearby file, Chrome-history entry, or other artifact rather than a session.

Do not build a parallel transcript index or rewrite harness parsers during an ordinary history
lookup. If AgentsView repeatedly misses supported sessions, report the ingestion defect separately
from the answer the user requested.

## Response discipline

Lead with the recovered information or retrospective conclusion. Include session IDs, timestamps,
or short excerpts only when they help the user inspect a consequential claim. For negative results,
briefly name the archive and filters searched plus any known ingestion gap; do not manufacture an
exhaustive proof-of-absence ceremony.
