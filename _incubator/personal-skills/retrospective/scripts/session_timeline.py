#!/usr/bin/env python3
"""
Extract a compact session timeline for retrospectives.

Two modes:

1. Codex JSONL mode (default) — parse a rollout file from ~/.codex/sessions.
   Use --session <path> or --find "<phrase>" (scans JSONL files under --root).

2. AgentsView DB mode (--db) — query the cross-harness archive at
   ~/.agentsview/sessions.db (read-only). Covers every harness AgentsView
   ingests (claude, codex, cursor, opencode, kilo, gemini, ...).
   --db --find "<phrase>"    lists sessions whose messages contain the exact
                             phrase (FTS), with agent / project / date / id.
   --db --session-id <id>    emits the message/tool-call timeline for one
                             session (exact id, or unique prefix).

Use this during retrospectives before synthesis so the account can cite actual
messages and tool calls instead of relying on memory or compacted summaries.
On Windows set PYTHONUTF8=1 to avoid console encoding failures.
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
from dataclasses import asdict, dataclass
from pathlib import Path

DEFAULT_DB = Path.home() / ".agentsview" / "sessions.db"


@dataclass
class TimelineItem:
    line: int
    timestamp: str
    item_type: str
    actor: str
    name: str
    summary: str


def compact(text: str, limit: int) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 1)] + "..."


def normalize_backslashes(text: str) -> str:
    """AgentsView input_json stores JSON-escaped Windows paths, so a decoded
    value can still carry doubled backslashes (C:\\\\Users\\\\...). Collapse
    them for display only."""
    return (text or "").replace("\\\\", "\\")


def parse_arguments(value: object) -> object:
    if not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def summarize_arguments(args: object) -> str:
    if isinstance(args, dict):
        for key in ("question", "query", "command", "cmd", "url", "title", "code",
                    "file_path", "path", "pattern", "prompt"):
            if key in args:
                return str(args[key])
        return json.dumps(args, ensure_ascii=False)
    return str(args)


# --------------------------------------------------------------------------
# Codex JSONL mode
# --------------------------------------------------------------------------

def message_text(payload: dict) -> str:
    parts: list[str] = []
    for item in payload.get("content", []) or []:
        if isinstance(item, dict):
            parts.append(str(item.get("text") or item.get("input_text") or item.get("output_text") or ""))
        else:
            parts.append(str(item))
    return " ".join(parts)


def iter_timeline(path: Path, include_outputs: bool, limit: int) -> list[TimelineItem]:
    items: list[TimelineItem] = []
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line_no, line in enumerate(handle, 1):
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue

            payload = obj.get("payload", {})
            payload_type = payload.get("type") or obj.get("type") or ""
            timestamp = obj.get("timestamp", "")

            if payload_type == "message":
                role = payload.get("role", "")
                items.append(
                    TimelineItem(
                        line_no,
                        timestamp,
                        "message",
                        role,
                        "",
                        compact(message_text(payload), limit),
                    )
                )
            elif payload_type == "function_call":
                name = payload.get("name", "")
                namespace = payload.get("namespace", "")
                full_name = f"{namespace}.{name}" if namespace else name
                args = parse_arguments(payload.get("arguments", ""))
                items.append(
                    TimelineItem(
                        line_no,
                        timestamp,
                        "tool-call",
                        "assistant",
                        full_name,
                        compact(summarize_arguments(args), limit),
                    )
                )
            elif payload_type == "function_call_output" and include_outputs:
                items.append(
                    TimelineItem(
                        line_no,
                        timestamp,
                        "tool-output",
                        "tool",
                        payload.get("call_id", ""),
                        compact(str(payload.get("output", "")), limit),
                    )
                )
            elif payload_type == "event_msg":
                event_payload = payload.get("payload", {})
                event_type = event_payload.get("type", "")
                if event_type in {"user_message", "mcp_tool_call_end", "thread_compacted"}:
                    items.append(
                        TimelineItem(
                            line_no,
                            timestamp,
                            f"event:{event_type}",
                            "event",
                            "",
                            compact(json.dumps(event_payload, ensure_ascii=False), limit),
                        )
                    )

    return items


def find_sessions(root: Path, phrase: str) -> list[Path]:
    matches: list[tuple[float, Path]] = []
    phrase_lower = phrase.lower()
    for path in root.rglob("*.jsonl"):
        try:
            with path.open("r", encoding="utf-8", errors="replace") as handle:
                if any(phrase_lower in line.lower() for line in handle):
                    matches.append((path.stat().st_mtime, path))
        except OSError:
            continue
    return [path for _, path in sorted(matches, reverse=True)]


# --------------------------------------------------------------------------
# AgentsView DB mode
# --------------------------------------------------------------------------

def open_db(db_path: Path) -> sqlite3.Connection:
    if not db_path.exists():
        raise SystemExit(f"AgentsView DB not found: {db_path}")
    # as_uri() yields file:///C:/... — the leading slash before the drive letter
    # is required for SQLite URI filenames on Windows.
    return sqlite3.connect(db_path.resolve().as_uri() + "?mode=ro", uri=True)


def db_find_sessions(con: sqlite3.Connection, phrase: str, limit: int) -> list[dict]:
    fts_query = '"' + phrase.replace('"', '""') + '"'
    rows = con.execute(
        """
        SELECT s.id, s.agent, s.project, s.started_at, s.user_message_count,
               COUNT(*) AS matches
        FROM messages_fts f
        JOIN messages m ON m.id = f.rowid
        JOIN sessions s ON s.id = m.session_id
        WHERE f.messages_fts MATCH ?
          AND s.deleted_at IS NULL
        GROUP BY s.id
        ORDER BY s.started_at DESC
        LIMIT ?
        """,
        (fts_query, limit),
    ).fetchall()
    return [
        {
            "session_id": r[0],
            "agent": r[1],
            "project": r[2],
            "started_at": r[3] or "",
            "user_messages": r[4],
            "matches": r[5],
        }
        for r in rows
    ]


def db_resolve_session(con: sqlite3.Connection, session_id: str) -> str:
    row = con.execute("SELECT id FROM sessions WHERE id = ?", (session_id,)).fetchone()
    if row:
        return row[0]
    rows = con.execute(
        "SELECT id FROM sessions WHERE id LIKE ? || '%' ORDER BY started_at DESC LIMIT 5",
        (session_id,),
    ).fetchall()
    if len(rows) == 1:
        return rows[0][0]
    if not rows:
        raise SystemExit(f"No session matched id or prefix: {session_id}")
    ids = ", ".join(r[0] for r in rows)
    raise SystemExit(f"Ambiguous session prefix {session_id!r}; candidates: {ids}")


def db_timeline(
    con: sqlite3.Connection,
    session_id: str,
    include_outputs: bool,
    include_system: bool,
    limit: int,
) -> list[TimelineItem]:
    session_id = db_resolve_session(con, session_id)

    calls_by_ordinal: dict[int, list[tuple]] = {}
    for row in con.execute(
        """
        SELECT m.ordinal, m.timestamp, t.tool_name, t.skill_name, t.file_path,
               t.input_json, t.result_content, t.call_index
        FROM tool_calls t
        JOIN messages m ON m.id = t.message_id
        WHERE t.session_id = ?
        ORDER BY m.ordinal, t.call_index
        """,
        (session_id,),
    ):
        calls_by_ordinal.setdefault(row[0], []).append(row)

    items: list[TimelineItem] = []
    for ordinal, role, is_system, timestamp, content in con.execute(
        """
        SELECT ordinal, role, is_system, timestamp, content
        FROM messages
        WHERE session_id = ?
        ORDER BY ordinal
        """,
        (session_id,),
    ):
        if is_system and not include_system:
            continue  # suppresses the message AND its attached tool-calls
        if content and content.strip():
            items.append(
                TimelineItem(ordinal, timestamp or "", "message", role, "",
                             compact(content, limit))
            )
        for call in calls_by_ordinal.get(ordinal, []):
            (_, call_ts, tool_name, skill_name, file_path, input_json,
             result_content, _) = call
            name = tool_name or ""
            if skill_name:
                name = f"{name}[skill:{skill_name}]"
            summary = summarize_arguments(parse_arguments(input_json))
            if (not summary or summary in ("None", "null", "{}")) and file_path:
                summary = file_path
            summary = normalize_backslashes(summary)
            items.append(
                TimelineItem(ordinal, call_ts or timestamp or "", "tool-call",
                             "assistant", name, compact(summary, limit))
            )
            if include_outputs and result_content:
                items.append(
                    TimelineItem(ordinal, call_ts or timestamp or "", "tool-output",
                                 "tool", name, compact(result_content, limit))
                )
    return items


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------

def render_markdown(items: list[TimelineItem]) -> str:
    lines = [
        "| Line | Timestamp | Type | Actor | Name | Summary |",
        "|---:|---|---|---|---|---|",
    ]
    for item in items:
        summary = item.summary.replace("|", "\\|")
        lines.append(
            f"| {item.line} | {item.timestamp} | {item.item_type} | {item.actor} | `{item.name}` | {summary} |"
        )
    return "\n".join(lines)


def render_jsonl(items: list[TimelineItem]) -> str:
    return "\n".join(json.dumps(asdict(item), ensure_ascii=False) for item in items)


def render_session_list_markdown(rows: list[dict]) -> str:
    lines = [
        "| Session | Agent | Project | Started | User msgs | Matches |",
        "|---|---|---|---|---:|---:|",
    ]
    for r in rows:
        lines.append(
            f"| `{r['session_id']}` | {r['agent']} | {r['project']} | "
            f"{r['started_at']} | {r['user_messages']} | {r['matches']} |"
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract a compact session timeline (codex JSONL or AgentsView DB).")
    parser.add_argument("--session", help="JSONL mode: path to a rollout JSONL file.")
    parser.add_argument("--find", help="Exact phrase. JSONL mode: extract the newest matching rollout. DB mode: list matching sessions (FTS).")
    parser.add_argument("--root", default=str(Path.home() / ".codex" / "sessions"), help="JSONL mode: root used with --find.")
    parser.add_argument("--db", nargs="?", const=str(DEFAULT_DB), default=None, metavar="PATH",
                        help=f"AgentsView DB mode (read-only). Optional path, default {DEFAULT_DB}.")
    parser.add_argument("--session-id", help="DB mode: session id (or unique prefix) to emit a timeline for.")
    parser.add_argument("--format", choices=["markdown", "jsonl"], default="markdown")
    parser.add_argument("--include-outputs", action="store_true", help="Include tool output rows. Noisy; off by default.")
    parser.add_argument("--include-system", action="store_true", help="DB mode: include system messages. Off by default.")
    parser.add_argument("--summary-chars", type=int, default=220)
    parser.add_argument("--limit", type=int, default=200)
    args = parser.parse_args()

    if args.db:
        con = open_db(Path(args.db))
        try:
            if args.session_id:
                items = db_timeline(con, args.session_id, args.include_outputs,
                                    args.include_system, args.summary_chars)[: args.limit]
                print(render_jsonl(items) if args.format == "jsonl" else render_markdown(items))
            elif args.find:
                rows = db_find_sessions(con, args.find, args.limit)
                if not rows:
                    raise SystemExit(f"No session matched phrase: {args.find}")
                if args.format == "jsonl":
                    print("\n".join(json.dumps(r, ensure_ascii=False) for r in rows))
                else:
                    print(render_session_list_markdown(rows))
            else:
                parser.error("DB mode needs --find or --session-id")
        finally:
            con.close()
        return 0

    if args.session:
        session = Path(args.session)
    elif args.find:
        sessions = find_sessions(Path(args.root), args.find)
        if not sessions:
            raise SystemExit(f"No session matched phrase: {args.find}")
        session = sessions[0]
    else:
        parser.error("Provide --session or --find (or --db)")

    items = iter_timeline(session, args.include_outputs, args.summary_chars)[: args.limit]
    if args.format == "jsonl":
        print(render_jsonl(items))
    else:
        print(render_markdown(items))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
